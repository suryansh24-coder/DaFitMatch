import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Inject HTML elements for the Try-On Viewer
try_on_elements = """
    <!-- Try-On Virtual Assets -->
    <video id="try-on-video" muted playsinline loop preload="metadata" aria-hidden="true" class="media z-10 transition-opacity duration-500 opacity-0" style="object-fit: cover;"></video>
    <img id="try-on-image" aria-hidden="true" class="media z-10 transition-opacity duration-500 opacity-0" style="object-fit: cover;" />
"""
if 'id="try-on-video"' not in html:
    html = html.replace('id="webgl-container"', 'id="webgl-container"')
    html = html.replace('<!-- Base / Clothing FWD -->', try_on_elements + '\n    <!-- Base / Clothing FWD -->')

# 2. Update selectOutfit logic
old_script = """async function selectOutfit(outfitId) {
    if(!catalogueData) return;
    
    // Single source of truth for selected outfit
    selectedOutfit = catalogueData.catalogues.flatMap(c => c.outfits).find(o => o.id === outfitId);
    if (!selectedOutfit) return;

    // Show subtle loading state
    showOutfitToast("Fitting your look...");

    // Architecture: Check if actual 3D asset is available
    const modelPath = selectedOutfit.model3D;
    
    try {
        // Attempt to check if the file exists (it won't, but this implements the requested architecture)
        const response = await fetch(modelPath, { method: 'HEAD' });
        
        if (response.ok) {
            if (window.fittingRoom) {
                const success = await window.fittingRoom.loadOutfit(selectedOutfit);
                if (success) {
                    showOutfitToast("Outfit applied to character.");
                    return;
                }
            }
            showOutfitToast("Outfit applied to character.");
        } else {
            // Step 10: If clothing assets are not currently available
            setTimeout(() => {
                showOutfitToast("3D outfit preview coming soon");
            }, 800);
        }
    } catch (error) {
        console.error("3D model loading failed gracefully:", error);
        setTimeout(() => {
            showOutfitToast("3D outfit preview coming soon");
        }, 800);
    }
}"""

new_script = """async function selectOutfit(outfitId) {
    if(!catalogueData) return;
    
    selectedOutfit = catalogueData.catalogues.flatMap(c => c.outfits).find(o => o.id === outfitId);
    if (!selectedOutfit) return;

    showOutfitToast("Fitting your look...");

    const tryOnVideoEl = document.getElementById('try-on-video');
    const tryOnImageEl = document.getElementById('try-on-image');
    const baseVideos = document.querySelectorAll('.media[id^="vid-"]');

    // Diagnostic State
    let devDiag = {
        id: outfitId,
        vidAvailable: false,
        imgAvailable: false,
        displayMode: 'MP4 FALLBACK'
    };

    // Helper to hide custom try-on layers
    const resetTryOn = () => {
        tryOnVideoEl.classList.add('opacity-0');
        tryOnImageEl.classList.add('opacity-0');
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
            const resVid = await fetch(selectedOutfit.tryOnVideo, { method: 'HEAD' }).catch(()=>({ok:false}));
            if (resVid.ok) {
                devDiag.vidAvailable = true;
                devDiag.displayMode = 'TRY-ON VIDEO';
                
                tryOnVideoEl.src = selectedOutfit.tryOnVideo;
                tryOnVideoEl.play().catch(e=>console.warn("Autoplay prevented:", e));
                tryOnVideoEl.classList.remove('opacity-0');
                tryOnImageEl.classList.add('opacity-0');
                
                updateTryOnDiagnostics(devDiag);
                showOutfitToast("Try-on video active.");
                return;
            }
        }

        // 3. Check Try-On Image
        if (selectedOutfit.tryOnImage) {
            const resImg = await fetch(selectedOutfit.tryOnImage, { method: 'HEAD' }).catch(()=>({ok:false}));
            if (resImg.ok) {
                devDiag.imgAvailable = true;
                devDiag.displayMode = 'TRY-ON IMAGE';
                
                tryOnImageEl.src = selectedOutfit.tryOnImage;
                tryOnImageEl.classList.remove('opacity-0');
                tryOnVideoEl.classList.add('opacity-0');
                setTimeout(() => tryOnVideoEl.src = '', 500);
                
                updateTryOnDiagnostics(devDiag);
                showOutfitToast("Try-on image active.");
                return;
            }
        }

        // 4. Fallback to MP4
        resetTryOn();
        updateTryOnDiagnostics(devDiag);
        showOutfitToast("Try-on preview unavailable — showing default model.");

    } catch (error) {
        console.error("Asset loading failed gracefully:", error);
        resetTryOn();
        updateTryOnDiagnostics(devDiag);
        showOutfitToast("Try-on preview unavailable — showing default model.");
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
"""

if "updateTryOnDiagnostics" not in html:
    html = html.replace(old_script, new_script)

with open('index.html', 'w') as f:
    f.write(html)

print("Injected visual fallback cascade logic.")
