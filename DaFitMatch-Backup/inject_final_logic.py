with open('index.html', 'r') as f:
    html = f.read()

new_script = """
<script>
let selectedOutfit = null;

function setOriginalCharacterVideosVisible(visible) {
    const videos = document.querySelectorAll('.media video, video.media, video[id^="vid-"]');
    videos.forEach(video => {
        // Explicitly skip try-on video just in case it matches the selector
        if (video.id === 'try-on-video') return;
        
        if (visible) {
            video.style.opacity = '';
            video.style.visibility = '';
        } else {
            video.style.opacity = '0';
            video.style.visibility = 'hidden';
        }
    });
}

async function selectOutfit(outfitId) {
    if(!catalogueData) return;
    
    selectedOutfit = catalogueData.catalogues.flatMap(c => c.outfits).find(o => o.id === outfitId);
    if (!selectedOutfit) return;

    showOutfitToast("Fitting your look...");

    const tryOnVideoEl = document.getElementById('try-on-video');
    const tryOnImageEl = document.getElementById('try-on-image');

    // Diagnostic State
    let devDiag = {
        id: outfitId,
        vidAvailable: false,
        imgAvailable: false,
        displayMode: 'MP4 FALLBACK'
    };

    const resetTryOn = () => {
        tryOnVideoEl.classList.add('opacity-0');
        tryOnImageEl.classList.add('opacity-0');
        
        // Restore original MP4 visibility
        setOriginalCharacterVideosVisible(true);
        
        setTimeout(() => {
            tryOnVideoEl.src = '';
            tryOnImageEl.src = '';
        }, 500);
    };

    try {
        // 1. Check 3D GLB
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

        // 2. Check Try-On Video
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

        // 3. Check Try-On Image
        if (selectedOutfit.tryOnImage) {
            const tryOnUrl = selectedOutfit.tryOnImage + "?tryonDebug=" + Date.now();
            
            const imgAvailable = await new Promise((resolve) => {
                const img = new Image();
                img.onload = () => resolve(true);
                img.onerror = () => resolve(false);
                img.src = tryOnUrl;
            });
            
            if (imgAvailable) {
                devDiag.imgAvailable = true;
                devDiag.displayMode = 'TRY-ON IMAGE';
                
                tryOnImageEl.src = tryOnUrl;
                
                // Hide original MP4s completely so they don't peek through
                setOriginalCharacterVideosVisible(false);
                
                tryOnImageEl.classList.remove('opacity-0');
                tryOnVideoEl.classList.add('opacity-0');
                setTimeout(() => tryOnVideoEl.src = '', 500);
                
                updateTryOnDiagnostics(devDiag);
                showOutfitToast(selectedOutfit.name + " applied.");
                return;
            }
        }

        // 4. Fallback to MP4
        resetTryOn();
        updateTryOnDiagnostics(devDiag);

    } catch (error) {
        console.error("Asset loading failed gracefully:", error);
        resetTryOn();
        updateTryOnDiagnostics(devDiag);
    }
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
    
    overlay.textContent = `TRY-ON DIAGNOSTICS:

OUTFIT:
ID: ${diag.id}

VIDEO:
${diag.vidAvailable ? '✓ available' : '✗ unavailable'}

IMAGE:
${diag.imgAvailable ? '✓ available' : '✗ unavailable'}

DISPLAY:
${diag.displayMode}`;
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
</script>
</body>
"""

html = html.replace('</body>', new_script)
with open('index.html', 'w') as f:
    f.write(html)
print("Injected final authoritative logic.")
