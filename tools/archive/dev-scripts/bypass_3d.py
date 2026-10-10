import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. We replace selectOutfit entirely to be extremely lean and strictly prioritize Video -> Image, deleting the 3D block.

new_select_outfit = """
async function selectOutfit(outfitId) {
    console.log('[DaFitMatch DEMO] VIEW LOOK CLICKED:', outfitId);
    if(!catalogueData) return;
    
    selectedOutfit = catalogueData.catalogues.flatMap(c => c.outfits).find(o => o.id === outfitId);
    if (!selectedOutfit) return;

    // Close the catalogue drawer
    const drawer = document.querySelector('#catalogue-drawer, .catalogue-drawer, [class*="catalogue"], aside');
    if (drawer && typeof drawer.classList !== 'undefined') {
        drawer.style.transform = 'translateX(100%)'; // Generic close attempt
        // If there's a specific close function in the page, it might be closeCataloguePanel()
        if (typeof closeCataloguePanel === 'function') closeCataloguePanel();
    }

    showOutfitToast("Fitting your look...");

    const overlay = document.getElementById('dafitmatch-tryon-overlay');
    const overlayImage = document.getElementById('dafitmatch-tryon-image');
    const overlayVideo = document.getElementById('dafitmatch-tryon-video');
    const viewport = document.getElementById('playground-area');

    window.dafitmatchTryOnState = 'TRY_ON_LOADING';

    // 1. Try-On Video (Priority 1)
    if (selectedOutfit.tryOnVideo) {
        const tryOnUrl = selectedOutfit.tryOnVideo + "?tryonDebug=" + Date.now();
        console.log('[DaFitMatch DEMO] TRY-ON VIDEO LOADING:', tryOnUrl);
        
        let loaded = false;
        let vWidth = 0, vHeight = 0;
        
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
            overlayVideo.style.setProperty('display', 'block', 'important');
            overlayVideo.style.setProperty('visibility', 'visible', 'important');
            overlayVideo.style.setProperty('opacity', '1', 'important');
            
            overlayImage.style.display = 'none';
            
            overlay.style.setProperty('display', 'block', 'important');
            overlay.style.setProperty('visibility', 'visible', 'important');
            overlay.style.setProperty('opacity', '1', 'important');
            overlay.style.setProperty('z-index', '9999999', 'important');
            
            // Apply alignment
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
            overlayVideo.style.width = `${renderedWidth}px`;
            overlayVideo.style.height = `${renderedHeight}px`;
            overlayVideo.style.left = `${(vRect.width - renderedWidth) / 2}px`;
            overlayVideo.style.top = `${(vRect.height - renderedHeight) / 2}px`;
            
            try {
                const saved = localStorage.getItem('dafitmatch_tryon_calibration_' + selectedOutfit.id);
                if (saved) {
                    const data = JSON.parse(saved);
                    overlayVideo.style.setProperty('--tryon-scale', data.scale);
                    overlayVideo.style.setProperty('--tryon-x', data.x + 'px');
                    overlayVideo.style.setProperty('--tryon-y', data.y + 'px');
                } else {
                    overlayVideo.style.setProperty('--tryon-scale', '1');
                    overlayVideo.style.setProperty('--tryon-x', '0px');
                    overlayVideo.style.setProperty('--tryon-y', '0px');
                }
            } catch(e) {}

            try {
                await overlayVideo.play();
                
                const opSlider = document.getElementById('cal-opacity');
                const desiredOpacity = opSlider ? parseFloat(opSlider.value) : 1.0;
                
                if (desiredOpacity >= 1.0) {
                    window.dafitmatchTryOnState = 'TRY_ON_ACTIVE';
                    hideALLOriginalCharacterRendering();
                    stopALLOriginalVideos();
                } else {
                    restoreALLOriginalCharacterRendering();
                }
                console.log('[DaFitMatch DEMO] TRY-ON VIDEO ACTIVE:', tryOnUrl);
                return;
            } catch (e) {
                console.error("Video playback prevented:", e);
            }
        }
    }

    // 2. Try-On Image (Priority 2)
    if (selectedOutfit.tryOnImage) {
        const imagePath = selectedOutfit.tryOnImage;
        console.log('[DaFitMatch DEMO] TRY-ON IMAGE LOADING:', imagePath);
        
        overlayImage.onload = () => {
            overlayImage.style.setProperty('display', 'block', 'important');
            overlayImage.style.setProperty('visibility', 'visible', 'important');
            overlayImage.style.setProperty('opacity', '1', 'important');
            
            overlayVideo.style.display = 'none';
            
            overlay.style.setProperty('display', 'block', 'important');
            overlay.style.setProperty('visibility', 'visible', 'important');
            overlay.style.setProperty('opacity', '1', 'important');
            overlay.style.setProperty('z-index', '9999999', 'important');
            
            // Align
            if (typeof alignTryOnImage === 'function') {
                alignTryOnImage(overlayImage, viewport, selectedOutfit.id);
            }
            
            const opSlider = document.getElementById('cal-opacity');
            const desiredOpacity = opSlider ? parseFloat(opSlider.value) : 1.0;
            
            if (desiredOpacity >= 1.0) {
                window.dafitmatchTryOnState = 'TRY_ON_ACTIVE';
                hideALLOriginalCharacterRendering();
                stopALLOriginalVideos();
            } else {
                restoreALLOriginalCharacterRendering();
            }
            console.log('[DaFitMatch DEMO] TRY-ON IMAGE ACTIVE:', imagePath);
        };
        
        overlayImage.onerror = () => {
            console.error('[DaFitMatch DEMO] TRY-ON IMAGE FAILED:', imagePath);
            window.dafitmatchTryOnState = 'TRY_ON_FAILED';
            restoreALLOriginalCharacterRendering();
        };
        
        overlayImage.src = imagePath + "?tryonDebug=" + Date.now();
        return;
    }

    // 3. Fallback
    console.log('[DaFitMatch DEMO] NO TRY-ON ASSET FOUND. RESTORING ORIGINAL.');
    window.dafitmatchTryOnState = 'NORMAL';
    overlay.style.setProperty('display', 'none', 'important');
    restoreALLOriginalCharacterRendering();
}
"""

target_select_outfit = r'async function selectOutfit\(outfitId\)\s*\{.*?\n\}\n'
html = re.sub(target_select_outfit, new_select_outfit, html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(html)
print("selectOutfit patched to bypass 3D.")
