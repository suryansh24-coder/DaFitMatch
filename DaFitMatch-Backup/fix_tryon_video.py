import re
from bs4 import BeautifulSoup

with open('index.html', 'r') as f:
    html = f.read()

# I will replace the "2. Try-On Video" block entirely inside the html string using python.
old_video_block = """
        // 2. Try-On Video
        if (selectedOutfit.tryOnVideo) {
            const vidAvailable = await new Promise((resolve) => {
                const vid = document.createElement('video');
                vid.onloadedmetadata = () => resolve(true);
                vid.onerror = () => resolve(false);
                vid.src = selectedOutfit.tryOnVideo;
            });
            if (vidAvailable) {
                devDiag.vidAvailable = true;
                devDiag.displayMode = 'TRY-ON VIDEO';
                
                tryOnVideoEl.src = selectedOutfit.tryOnVideo;
                tryOnVideoEl.play().catch(e=>console.warn("Autoplay prevented:", e));
                
                // Hide original MP4s
                setOriginalCharacterVideosVisible(false);
                
                tryOnVideoEl.classList.remove('opacity-0');
                tryOnImageEl.classList.add('opacity-0');
                
                updateTryOnDiagnostics(devDiag);
                showOutfitToast(selectedOutfit.name + " applied.");
                return;
            }
        }
"""

new_video_block = """
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
                
                // Show overlay
                overlay.style.display = 'block';
                overlay.style.visibility = 'visible';
                
                // We'll align the video similarly to how we align the image,
                // so it uses the calibration offsets and precise centering.
                // Wait, alignTryOnImage expects naturalWidth/Height, but video uses videoWidth/Height.
                // Let's manually do it here to avoid breaking alignTryOnImage for images.
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
                
                // Load calibration onto the overlayVideo element instead of image
                try {
                    const saved = localStorage.getItem('dafitmatch_tryon_calibration_' + selectedOutfit.id);
                    if (saved) {
                        const data = JSON.parse(saved);
                        if (data.scale !== undefined) {
                            overlayVideo.style.setProperty('--tryon-scale', data.scale);
                            overlayVideo.style.setProperty('--tryon-x', data.x + 'px');
                            overlayVideo.style.setProperty('--tryon-y', data.y + 'px');
                        }
                    } else {
                        overlayVideo.style.setProperty('--tryon-scale', '1');
                        overlayVideo.style.setProperty('--tryon-x', '0px');
                        overlayVideo.style.setProperty('--tryon-y', '0px');
                    }
                } catch(e) {}

                // Check calibration opacity slider
                const opSlider = document.getElementById('cal-opacity');
                const desiredOpacity = opSlider ? opSlider.value : '1';
                overlay.style.opacity = desiredOpacity;
                
                // Wait for the layout to paint
                await new Promise(r => setTimeout(r, 50));
                
                const rect = overlayVideo.getBoundingClientRect();
                const computed = window.getComputedStyle(overlay);
                
                if (rect.width > 0 && rect.height > 0 && computed.display !== 'none' && computed.visibility !== 'hidden') {
                    // Force playback and wait for it to actually start
                    try {
                        await overlayVideo.play();
                        
                        // PLAYBACK STARTED SUCCESSFULLY, SAFE TO HIDE
                        if (parseFloat(desiredOpacity) < 1.0) {
                            setOriginalCharacterVideosVisible(true);
                        } else {
                            setOriginalCharacterVideosVisible(false);
                        }
                        
                        devDiag.vidAvailable = true;
                        devDiag.displayMode = 'TRY-ON VIDEO';
                        updateTryOnDiagnostics(devDiag);
                        showOutfitToast(selectedOutfit.name + " applied.");
                        return;
                    } catch (e) {
                        console.error("Video playback failed/prevented:", e);
                        failSafeRestore();
                        return;
                    }
                } else {
                    console.error("Video rendering verification failed. Dimensions or visibility invalid.");
                    failSafeRestore();
                    return;
                }
            }
        }
"""

# Wait, `tryOnVideoEl` vs `overlayVideo`. My previous rewrite changed `tryOnVideoEl` to `overlayVideo` up at the top:
# `const overlayVideo = document.getElementById('dafitmatch-tryon-video');`
# So the old code in the file might look slightly different if I used overlayVideo. Let me dynamically find the block.

import textwrap

# Read the file and isolate the selectOutfit function
match = re.search(r'// 2\. Try-On Video(.*?)// 3\. Try-On Image', html, flags=re.DOTALL)
if match:
    old = match.group(0)
    # Ensure it's correctly swapped without losing trailing comments
    html = html.replace(old, new_video_block.strip() + "\n\n        // 3. Try-On Image")
    
with open('index.html', 'w') as f:
    f.write(html)
print("Injected strict Try-On Video fallback logic.")
