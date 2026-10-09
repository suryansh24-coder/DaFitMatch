import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Inject the state machine into the animation loop.
# Before `activeVid = video;`, let's add the check.
target_anim = """
            if (activeVid !== video) {
              activeVid.style.visibility = 'hidden';
              video.style.visibility = 'visible';
              activeVid = video;
            }
"""

replacement_anim = """
            if (activeVid !== video) {
              activeVid.style.visibility = 'hidden';
              if (window.dafitmatchTryOnState !== 'TRY_ON_ACTIVE') {
                  video.style.visibility = 'visible';
                  video.style.opacity = '1';
              }
              activeVid = video;
            }
"""

if target_anim.strip() in html:
    html = html.replace(target_anim.strip(), replacement_anim.strip())

# Also in checkHold, let's make sure it pauses if state switches?
# Actually, the user says "When active === false: FOR EVERY ORIGINAL CHARACTER VIDEO: video.pause(); video.style.display = 'none'; video.style.visibility = 'hidden'; video.style.opacity = '0'; video.style.pointerEvents = 'none';"
# We'll put this logic into the authoritative controller.

controller_logic = """
window.dafitmatchTryOnState = 'NORMAL';

function setOriginalAnimationActive(active) {
    const videos = document.querySelectorAll('.media video, video.media, video[id^="vid-"]');
    
    if (active) {
        window.dafitmatchTryOnState = 'NORMAL';
        videos.forEach(video => {
            if (video.id === 'dafitmatch-tryon-video') return;
            // Restore visibility ONLY to the active video to avoid flickering all 8 videos
            // Actually, just clear the inline display/opacity/visibility styles, 
            // the animation loop will manage it.
            video.style.display = '';
            video.style.visibility = '';
            video.style.opacity = '';
            video.style.pointerEvents = '';
            
            // If this is the currently active video tracked by the animation loop, resume it!
            // Wait, we can just play them all safely, the hidden ones won't matter, 
            // OR we can just let the animation loop recover naturally.
            if (video === window.activeVid && video.paused) {
                video.play().catch(e=>{});
            }
        });
    } else {
        window.dafitmatchTryOnState = 'TRY_ON_ACTIVE';
        videos.forEach(video => {
            if (video.id === 'dafitmatch-tryon-video') return;
            
            video.pause();
            video.style.display = 'none';
            video.style.visibility = 'hidden';
            video.style.opacity = '0';
            video.style.pointerEvents = 'none';
        });
    }
}
"""

# Find setOriginalCharacterVideosVisible and replace it
target_controller = r'function setOriginalCharacterVideosVisible\(visible\)\s*\{.*?\}\s*'
html = re.sub(target_controller, controller_logic, html, flags=re.DOTALL)


# Now update selectOutfit to use this state machine rigorously.
# We replace selectOutfit entirely.

new_select_outfit = """
async function selectOutfit(outfitId) {
    if(!catalogueData) return;
    
    selectedOutfit = catalogueData.catalogues.flatMap(c => c.outfits).find(o => o.id === outfitId);
    if (!selectedOutfit) return;

    showOutfitToast("Fitting your look...");

    const overlay = document.getElementById('dafitmatch-tryon-overlay');
    const overlayImage = document.getElementById('dafitmatch-tryon-image');
    const overlayVideo = document.getElementById('dafitmatch-tryon-video');
    const viewport = document.getElementById('playground-area');

    window.dafitmatchTryOnState = 'TRY_ON_LOADING';

    let devDiag = {
        id: outfitId,
        vidAvailable: false,
        imgAvailable: false,
        displayMode: 'TRY_ON_LOADING'
    };

    const deactivateTryOnLayer = () => {
        overlay.style.opacity = '0';
        overlay.style.visibility = 'hidden';
        overlay.style.display = 'none';
        
        setOriginalAnimationActive(true);
        
        devDiag.displayMode = 'TRY_ON_FAILED — ORIGINAL RESTORED';
        updateTryOnDiagnostics(devDiag);
        console.warn("[DaFitMatch] Try-on failed or deactivated. Original MP4 restored.");
        
        setTimeout(() => {
            overlayImage.src = '';
            overlayVideo.src = '';
            overlayVideo.pause();
        }, 500);
    };

    const activateTryOnLayer = async (isImage) => {
        // Wait for a layout paint
        await new Promise(r => setTimeout(r, 50));
        
        const el = isImage ? overlayImage : overlayVideo;
        const rect = el.getBoundingClientRect();
        const computed = window.getComputedStyle(overlay);
        
        if (rect.width > 0 && rect.height > 0 && computed.display !== 'none' && computed.visibility !== 'hidden') {
            
            const opSlider = document.getElementById('cal-opacity');
            const desiredOpacity = opSlider ? parseFloat(opSlider.value) : 1.0;
            
            if (desiredOpacity >= 1.0) {
                setOriginalAnimationActive(false);
            } else {
                // Ghost mode calibration overrides hiding
                setOriginalAnimationActive(true);
            }
            
            return true;
        }
        return false;
    };

    const normalFallback = () => {
        overlay.style.opacity = '0';
        overlay.style.visibility = 'hidden';
        overlay.style.display = 'none';
        setOriginalAnimationActive(true);
        devDiag.displayMode = 'MP4 FALLBACK';
        updateTryOnDiagnostics(devDiag);
        
        setTimeout(() => {
            overlayImage.src = '';
            overlayVideo.src = '';
            overlayVideo.pause();
        }, 500);
    };

    try {
        // 1. 3D GLB
        if (selectedOutfit.model3D) {
            const res3D = await fetch(selectedOutfit.model3D, { method: 'HEAD' }).catch(()=>({ok:false}));
            if (res3D.ok && window.fittingRoom) {
                const success = await window.fittingRoom.loadOutfit(selectedOutfit);
                if (success) {
                    normalFallback();
                    devDiag.displayMode = 'THREE.JS 3D';
                    updateTryOnDiagnostics(devDiag);
                    showOutfitToast("Outfit applied to character.");
                    return;
                }
            }
        }

        // 2. Try-On Video
        if (selectedOutfit.tryOnVideo) {
            const tryOnUrl = selectedOutfit.tryOnVideo + "?tryonDebug=" + Date.now();
            let loaded = false;
            let vWidth = 0;
            let vHeight = 0;
            
            const vidAvailable = await new Promise((resolve) => {
                const vid = document.createElement('video');
                vid.onloadedmetadata = () => {
                    vWidth = vid.videoWidth;
                    vHeight = vid.videoHeight;
                    loaded = true;
                    resolve(true);
                };
                vid.onerror = () => resolve(false);
                vid.src = tryOnUrl;
            });
            
            if (vidAvailable && loaded && vWidth > 0 && vHeight > 0) {
                overlayVideo.src = tryOnUrl;
                overlayVideo.style.display = 'block';
                overlayImage.style.display = 'none';
                
                overlay.style.display = 'block';
                overlay.style.visibility = 'visible';
                
                const opSlider = document.getElementById('cal-opacity');
                overlay.style.opacity = opSlider ? opSlider.value : '1';
                
                const vRect = viewport.getBoundingClientRect();
                const vRatio = vRect.width / vRect.height;
                const iRatio = vWidth / vHeight;
                let renderedWidth, renderedHeight;
                if (iRatio > vRatio) {
                    renderedWidth = vRect.width;
                    renderedHeight = vRect.width / iRatio;
                } else {
                    renderedHeight = vRect.height;
                    renderedWidth = vRect.height * iRatio;
                }
                const centerX = (vRect.width - renderedWidth) / 2;
                const centerY = (vRect.height - renderedHeight) / 2;
                
                overlayVideo.style.width = `${renderedWidth}px`;
                overlayVideo.style.height = `${renderedHeight}px`;
                overlayVideo.style.left = `${centerX}px`;
                overlayVideo.style.top = `${centerY}px`;
                
                loadTryOnCalibration(selectedOutfit.id);
                
                try {
                    await overlayVideo.play();
                    
                    const success = await activateTryOnLayer(false);
                    if (success) {
                        devDiag.vidAvailable = true;
                        devDiag.displayMode = 'TRY-ON VIDEO';
                        updateTryOnDiagnostics(devDiag);
                        showOutfitToast(selectedOutfit.name + " applied.");
                        return;
                    } else {
                        console.error("Video activation verified failure.");
                        deactivateTryOnLayer();
                        return;
                    }
                } catch (e) {
                    console.error("Video playback prevented:", e);
                    deactivateTryOnLayer();
                    return;
                }
            }
        }

        // 3. Try-On Image
        if (selectedOutfit.tryOnImage) {
            const tryOnUrl = selectedOutfit.tryOnImage + "?tryonDebug=" + Date.now();
            let loaded = false;
            const img = new Image();
            img.src = tryOnUrl;
            
            try {
                await img.decode();
                loaded = true;
            } catch (err) {}
            
            if (loaded && img.naturalWidth > 0 && img.naturalHeight > 0) {
                overlayImage.src = tryOnUrl;
                overlayImage.style.display = 'block';
                overlayVideo.style.display = 'none';
                
                overlay.style.display = 'block';
                overlay.style.visibility = 'visible';
                
                const opSlider = document.getElementById('cal-opacity');
                overlay.style.opacity = opSlider ? opSlider.value : '1';
                
                alignTryOnImage(overlayImage, viewport, selectedOutfit.id);
                
                const success = await activateTryOnLayer(true);
                if (success) {
                    devDiag.imgAvailable = true;
                    devDiag.displayMode = 'TRY-ON IMAGE';
                    updateTryOnDiagnostics(devDiag);
                    showOutfitToast(selectedOutfit.name + " applied.");
                    return;
                } else {
                    console.error("Image activation verified failure.");
                    deactivateTryOnLayer();
                    return;
                }
            }
        }
        
        // 4. Fallback
        normalFallback();

    } catch (error) {
        console.error("Asset loading failed gracefully:", error);
        deactivateTryOnLayer();
    }
}
"""

target_select_outfit = r'async function selectOutfit\(outfitId\)\s*\{.*?\n\}\n'
html = re.sub(target_select_outfit, new_select_outfit, html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(html)
print("Updated authoritative controller and state machine.")
