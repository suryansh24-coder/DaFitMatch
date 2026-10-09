import re
from bs4 import BeautifulSoup

with open('index.html', 'r') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Wipe old selectOutfit scripts
for script in soup.find_all('script'):
    if script.string and ('function selectOutfit' in script.string or 'let selectedOutfit = null;' in script.string):
        script.decompose()

# The definitive logic
new_script = """
<script>
let selectedOutfit = null;

function setOriginalCharacterVideosVisible(visible) {
    const videos = document.querySelectorAll('.media video, video.media, video[id^="vid-"]');
    videos.forEach(video => {
        if (video.id === 'dafitmatch-tryon-video') return;
        
        if (visible) {
            video.style.opacity = '';
            video.style.visibility = '';
        } else {
            video.style.opacity = '0';
            video.style.visibility = 'hidden';
        }
    });
}

function updateTryOnDiagnostics(diag) {
    if (window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') return;
    
    let overlay = document.getElementById('tryon-diagnostic-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'tryon-diagnostic-overlay';
        overlay.className = 'fixed bottom-4 right-4 bg-slate-900/95 backdrop-blur text-sky-400 font-mono text-xs p-4 rounded-xl shadow-2xl z-50 border border-slate-700/50 whitespace-pre-wrap';
        document.body.appendChild(overlay);
    }
    
    overlay.textContent = `TRY-ON DIAGNOSTICS\\n\\nOUTFIT:\\nID: ${diag.id}\\n\\nVIDEO:\\n${diag.vidAvailable ? '✓ available' : '✗ unavailable'}\\n\\nIMAGE:\\n${diag.imgAvailable ? '✓ available' : '✗ unavailable'}\\n\\nDISPLAY:\\n${diag.displayMode}`;
}

function showOutfitToast(message) {
    let toast = document.getElementById('outfit-toast');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'outfit-toast';
        toast.className = 'fixed bottom-8 left-1/2 transform -translate-x-1/2 bg-slate-900/90 backdrop-blur-md text-white px-5 py-2.5 rounded-full text-sm font-medium shadow-2xl z-50 transition-opacity duration-300 opacity-0 pointer-events-none border border-slate-700/50';
        document.body.appendChild(toast);
    }
    
    toast.textContent = message;
    toast.classList.remove('opacity-0');
    
    if (window.toastTimeout) clearTimeout(window.toastTimeout);
    
    window.toastTimeout = setTimeout(() => {
        toast.classList.add('opacity-0');
    }, 3000);
}

async function selectOutfit(outfitId) {
    if(!catalogueData) return;
    
    selectedOutfit = catalogueData.catalogues.flatMap(c => c.outfits).find(o => o.id === outfitId);
    if (!selectedOutfit) return;

    showOutfitToast("Fitting your look...");

    const overlay = document.getElementById('dafitmatch-tryon-overlay');
    const overlayImage = document.getElementById('dafitmatch-tryon-image');
    const overlayVideo = document.getElementById('dafitmatch-tryon-video');

    let devDiag = {
        id: outfitId,
        vidAvailable: false,
        imgAvailable: false,
        displayMode: 'MP4 FALLBACK'
    };

    const failSafeRestore = () => {
        overlay.style.opacity = '0';
        overlay.style.visibility = 'hidden';
        overlay.style.display = 'none';
        setOriginalCharacterVideosVisible(true);
        devDiag.displayMode = 'TRY-ON FAILED — ORIGINAL RESTORED';
        updateTryOnDiagnostics(devDiag);
        console.warn("[DaFitMatch] Try-on failed. Original MP4 restored.");
    };

    const resetTryOn = () => {
        overlay.style.opacity = '0';
        overlay.style.visibility = 'hidden';
        overlay.style.display = 'none';
        setOriginalCharacterVideosVisible(true);
        devDiag.displayMode = 'MP4 FALLBACK';
        updateTryOnDiagnostics(devDiag);
        
        setTimeout(() => {
            overlayImage.src = '';
            overlayVideo.src = '';
        }, 500);
    };

    try {
        // 1. 3D GLB (Preserved Architecture)
        if (selectedOutfit.model3D) {
            const res3D = await fetch(selectedOutfit.model3D, { method: 'HEAD' }).catch(()=>({ok:false}));
            if (res3D.ok && window.fittingRoom) {
                const success = await window.fittingRoom.loadOutfit(selectedOutfit);
                if (success) {
                    resetTryOn();
                    devDiag.displayMode = 'THREE.JS 3D';
                    updateTryOnDiagnostics(devDiag);
                    showOutfitToast("Outfit applied to character.");
                    return;
                }
            }
        }

        // 2. Try-On Image (Strict verification)
        if (selectedOutfit.tryOnImage) {
            const tryOnUrl = selectedOutfit.tryOnImage + "?tryonDebug=" + Date.now();
            
            let loaded = false;
            const img = new Image();
            img.src = tryOnUrl;
            
            try {
                await img.decode();
                loaded = true;
            } catch (err) {
                console.error("Image decode failed:", err);
            }
            
            if (loaded && img.naturalWidth > 0 && img.naturalHeight > 0) {
                // Image is verified. Assign to overlay.
                overlayImage.src = tryOnUrl;
                overlayImage.style.display = 'block';
                overlayVideo.style.display = 'none';
                
                // Show overlay
                overlay.style.display = 'block';
                overlay.style.visibility = 'visible';
                overlay.style.opacity = '1';
                
                // Final layout verification
                const rect = overlayImage.getBoundingClientRect();
                const computed = window.getComputedStyle(overlay);
                
                console.log(`[DaFitMatch] Overlay rect: ${rect.width}x${rect.height}`);
                
                if (rect.width > 0 && rect.height > 0 && computed.display !== 'none' && computed.visibility !== 'hidden') {
                    // Safe to hide original!
                    setOriginalCharacterVideosVisible(false);
                    
                    devDiag.imgAvailable = true;
                    devDiag.displayMode = 'TRY-ON IMAGE';
                    updateTryOnDiagnostics(devDiag);
                    showOutfitToast(selectedOutfit.name + " applied.");
                    return;
                } else {
                    console.error("Overlay rendering verification failed. Dimensions or visibility invalid.");
                    failSafeRestore();
                    return;
                }
            }
        }
        
        // 3. Fallback
        resetTryOn();

    } catch (error) {
        console.error("Asset loading failed gracefully:", error);
        failSafeRestore();
    }
}
</script>
"""

new_script_soup = BeautifulSoup(new_script, 'html.parser')
soup.body.append(new_script_soup)

with open('index.html', 'w') as f:
    f.write(str(soup))

print("Injected strict try-on logic.")
