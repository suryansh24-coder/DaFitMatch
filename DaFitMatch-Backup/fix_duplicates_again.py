import re

with open('index.html', 'r') as f:
    html = f.read()

def replacer(match):
    content = match.group(0)
    if 'selectOutfit' in content and 'function selectOutfit' in content:
        return ''
    return content

html = re.sub(r'<script.*?</script>', replacer, html, flags=re.DOTALL)
html = html.replace('</body>\n</body>', '</body>')

new_script = """
<script>
let selectedOutfit = null;

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
            console.log("[DaFitMatch Try-On] Loading image:", tryOnUrl);
            
            const imgAvailable = await new Promise((resolve) => {
                const img = new Image();
                img.onload = () => {
                    console.log("[DaFitMatch] TRY-ON IMAGE ONLOAD", img.naturalWidth, img.naturalHeight);
                    resolve(true);
                };
                img.onerror = (e) => {
                    console.error("[DaFitMatch] TRY-ON IMAGE ONERROR", e, img.src);
                    resolve(false);
                };
                img.src = tryOnUrl;
            });
            
            if (imgAvailable) {
                devDiag.imgAvailable = true;
                devDiag.displayMode = 'TRY-ON IMAGE';
                
                const finalUrl = selectedOutfit.tryOnImage + "?tryonDebug=" + Date.now();
                tryOnImageEl.src = finalUrl;
                
                console.log("TRY-ON ELEMENT", tryOnImageEl);
                console.log("SRC", tryOnImageEl.src);
                console.log("CURRENT SRC ATTRIBUTE", tryOnImageEl.getAttribute("src"));
                console.log("NATURAL WIDTH", tryOnImageEl.naturalWidth);
                console.log("NATURAL HEIGHT", tryOnImageEl.naturalHeight);
                
                const styles = window.getComputedStyle(tryOnImageEl);
                console.log("DISPLAY", styles.display);
                console.log("VISIBILITY", styles.visibility);
                console.log("OPACITY", styles.opacity);
                console.log("Z-INDEX", styles.zIndex);
                console.log("POSITION", styles.position);

                const existingVideo = document.getElementById('vid-clothing-fwd');
                if (existingVideo) {
                    console.log("MP4 ELEMENT", existingVideo);
                    const videoStyles = window.getComputedStyle(existingVideo);
                    console.log("VIDEO DISPLAY", videoStyles.display);
                    console.log("VIDEO VISIBILITY", videoStyles.visibility);
                    console.log("VIDEO OPACITY", videoStyles.opacity);
                    console.log("VIDEO Z-INDEX", videoStyles.zIndex);
                }
                
                console.log("TRY-ON PARENT", tryOnImageEl.parentElement);

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
print("Wiped duplicates and injected final clean logic.")
