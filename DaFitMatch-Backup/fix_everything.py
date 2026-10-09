import re

with open('index.html', 'r') as f:
    html = f.read()

# I will cleanly re-inject `window.selectOutfit` from scratch, targeting whatever mess is there now.
# The mess starts at `window.selectOutfit = async function(outfitId) {` and ends at the FIRST `</script>` following it.

target = r'window\.selectOutfit = async function\(outfitId\) \{.*?restoreALLOriginalCharacterRendering\(\);\n\}'

new_select_outfit = """window.selectOutfit = async function(outfitId) {
    console.log('[DaFitMatch DEMO] VIEW LOOK CLICKED:', outfitId);
    if(!catalogueData) return;
    
    selectedOutfit = catalogueData.catalogues.flatMap(c => c.outfits).find(o => o.id === outfitId);
    if (!selectedOutfit) return;

    const drawer = document.querySelector('#catalogue-drawer, .catalogue-drawer, [class*="catalogue"], aside');
    if (drawer && typeof drawer.classList !== 'undefined') {
        drawer.style.transform = 'translateX(100%)';
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
                }
            } catch(e) {}

            try {
                await overlayVideo.play();
                
                window.dafitmatchTryOnState = 'TRY_ON_ACTIVE';
                console.log('[DaFitMatch DEMO] TRY-ON VIDEO ACTIVE:', tryOnUrl);
                hideALLOriginalCharacterRendering();
                stopALLOriginalVideos();
                
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
            
            if (typeof alignTryOnImage === 'function') {
                alignTryOnImage(overlayImage, viewport, selectedOutfit.id);
            }
            
            window.dafitmatchTryOnState = 'TRY_ON_ACTIVE';
            console.log('[DaFitMatch DEMO] TRY-ON IMAGE ACTIVE:', imagePath);
            hideALLOriginalCharacterRendering();
            stopALLOriginalVideos();
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
}"""

html = re.sub(target, new_select_outfit, html, flags=re.DOTALL)

# Now completely remove the test wrapper from the bottom of body
target_wrapper = r'<script>\nconsole\.log\(\n\s*\'\[DaFitMatch DEMO\] RUNTIME selectOutfit =.*?</script>\n</body>'
html = re.sub(target_wrapper, '</body>', html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(html)
