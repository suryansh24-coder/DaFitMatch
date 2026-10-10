import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Update the overlay HTML
overlay_regex = r'<div id="dafitmatch-tryon-overlay".*?</div>'
new_overlay = """
<div id="dafitmatch-tryon-overlay" style="position: absolute; inset: 0; width: 100%; height: 100%; z-index: 100; display: none; visibility: hidden; opacity: 0; pointer-events: none;">
    <img id="dafitmatch-tryon-image" style="position: absolute; transform: translate(var(--tryon-x), var(--tryon-y)) scale(var(--tryon-scale)); transform-origin: center center;" />
    <video id="dafitmatch-tryon-video" muted playsinline loop style="position: absolute; display: none; transform: translate(var(--tryon-x), var(--tryon-y)) scale(var(--tryon-scale)); transform-origin: center center;"></video>
</div>
"""
html = re.sub(overlay_regex, new_overlay.strip(), html, flags=re.DOTALL)


# 2. Update the javascript
# We need to wipe the old alignTryOnImage, loadTryOnCalibration, initCalibrationUI
script_start = html.find('function setOriginalCharacterVideosVisible')

# Let's just find everything from setOriginalCharacterVideosVisible down to the end and replace it.
# Actually, I'll just use a clean script replacement.
html = html[:script_start]

new_script = """
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

function loadTryOnCalibration(outfitId) {
    const imgEl = document.getElementById('dafitmatch-tryon-image');
    if (!imgEl) return;
    
    try {
        const saved = localStorage.getItem('dafitmatch_tryon_calibration_' + outfitId);
        if (saved) {
            const data = JSON.parse(saved);
            if (data.scale !== undefined) {
                imgEl.style.setProperty('--tryon-scale', data.scale);
                imgEl.style.setProperty('--tryon-x', data.x + 'px');
                imgEl.style.setProperty('--tryon-y', data.y + 'px');
                
                if(document.getElementById('cal-scale')) {
                    document.getElementById('cal-scale').value = data.scale;
                    document.getElementById('cal-x').value = data.x;
                    document.getElementById('cal-y').value = data.y;
                    document.getElementById('cal-scale-val').textContent = parseFloat(data.scale).toFixed(2);
                    document.getElementById('cal-x-val').textContent = data.x + 'px';
                    document.getElementById('cal-y-val').textContent = data.y + 'px';
                }
                return;
            }
        }
    } catch (e) {}
    
    // Defaults if nothing saved
    imgEl.style.setProperty('--tryon-scale', '1');
    imgEl.style.setProperty('--tryon-x', '0px');
    imgEl.style.setProperty('--tryon-y', '0px');
    if(document.getElementById('cal-scale')) {
        document.getElementById('cal-scale').value = 1;
        document.getElementById('cal-x').value = 0;
        document.getElementById('cal-y').value = 0;
        document.getElementById('cal-scale-val').textContent = '1.00';
        document.getElementById('cal-x-val').textContent = '0px';
        document.getElementById('cal-y-val').textContent = '0px';
    }
}

function alignTryOnImage(imgEl, viewportEl, outfitId) {
    const vRect = viewportEl.getBoundingClientRect();
    const nW = imgEl.naturalWidth;
    const nH = imgEl.naturalHeight;
    
    if (nW === 0 || nH === 0 || vRect.width === 0 || vRect.height === 0) return false;
    
    const vRatio = vRect.width / vRect.height;
    const iRatio = nW / nH;
    
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
    
    imgEl.style.width = `${renderedWidth}px`;
    imgEl.style.height = `${renderedHeight}px`;
    imgEl.style.left = `${centerX}px`;
    imgEl.style.top = `${centerY}px`;
    
    loadTryOnCalibration(outfitId);
    return true;
}

function initCalibrationUI() {
    if (window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') return;
    
    let panel = document.getElementById('tryon-calibration-panel');
    if (!panel) {
        panel = document.createElement('div');
        panel.id = 'tryon-calibration-panel';
        panel.className = 'fixed top-4 left-4 bg-slate-900/95 backdrop-blur text-white font-mono text-xs p-4 rounded-xl shadow-2xl z-50 border border-slate-700/50 w-64 flex flex-col gap-3';
        
        panel.innerHTML = `
            <div class="font-bold text-sky-400 mb-1 border-b border-slate-700 pb-1">TRY-ON CALIBRATION</div>
            
            <label class="flex flex-col gap-1">
                <div class="flex justify-between"><span>Scale</span> <span id="cal-scale-val">1.00</span></div>
                <input type="range" id="cal-scale" min="0.5" max="1.5" step="0.01" value="1.0" class="w-full">
            </label>
            
            <label class="flex flex-col gap-1">
                <div class="flex justify-between"><span>X Offset</span> <span id="cal-x-val">0px</span></div>
                <input type="range" id="cal-x" min="-300" max="300" step="1" value="0" class="w-full">
            </label>
            
            <label class="flex flex-col gap-1">
                <div class="flex justify-between"><span>Y Offset</span> <span id="cal-y-val">0px</span></div>
                <input type="range" id="cal-y" min="-300" max="300" step="1" value="0" class="w-full">
            </label>
            
            <label class="flex flex-col gap-1">
                <div class="flex justify-between text-yellow-400"><span>Overlay Opacity (Debug)</span> <span id="cal-op-val">1.0</span></div>
                <input type="range" id="cal-opacity" min="0" max="1" step="0.05" value="1.0" class="w-full accent-yellow-400">
            </label>
            
            <button id="cal-save" class="mt-2 w-full py-1.5 bg-sky-600 hover:bg-sky-500 rounded text-white font-bold transition-colors">SAVE CALIBRATION</button>
            <button id="cal-reset" class="w-full py-1.5 bg-slate-700 hover:bg-slate-600 rounded text-white font-bold transition-colors">RESET</button>
        `;
        document.body.appendChild(panel);
        
        const updateCSS = () => {
            const scale = document.getElementById('cal-scale').value;
            const x = document.getElementById('cal-x').value;
            const y = document.getElementById('cal-y').value;
            const op = document.getElementById('cal-opacity').value;
            
            document.getElementById('cal-scale-val').textContent = parseFloat(scale).toFixed(2);
            document.getElementById('cal-x-val').textContent = x + 'px';
            document.getElementById('cal-y-val').textContent = y + 'px';
            document.getElementById('cal-op-val').textContent = parseFloat(op).toFixed(2);
            
            const imgEl = document.getElementById('dafitmatch-tryon-image');
            if(imgEl) {
                imgEl.style.setProperty('--tryon-scale', scale);
                imgEl.style.setProperty('--tryon-x', x + 'px');
                imgEl.style.setProperty('--tryon-y', y + 'px');
            }
            
            const overlay = document.getElementById('dafitmatch-tryon-overlay');
            if (overlay && overlay.style.display !== 'none') {
                overlay.style.opacity = op;
                if (parseFloat(op) < 1.0) {
                    setOriginalCharacterVideosVisible(true);
                } else {
                    setOriginalCharacterVideosVisible(false);
                }
            }
        };
        
        document.getElementById('cal-scale').addEventListener('input', updateCSS);
        document.getElementById('cal-x').addEventListener('input', updateCSS);
        document.getElementById('cal-y').addEventListener('input', updateCSS);
        document.getElementById('cal-opacity').addEventListener('input', updateCSS);
        
        document.getElementById('cal-save').addEventListener('click', () => {
            if(!selectedOutfit) return;
            const data = {
                scale: parseFloat(document.getElementById('cal-scale').value),
                x: parseInt(document.getElementById('cal-x').value),
                y: parseInt(document.getElementById('cal-y').value)
            };
            localStorage.setItem('dafitmatch_tryon_calibration_' + selectedOutfit.id, JSON.stringify(data));
            console.log("TRY-ON CALIBRATION SAVED FOR", selectedOutfit.id, "\\n", JSON.stringify(data, null, 2));
            showOutfitToast("Calibration Saved!");
        });
        
        document.getElementById('cal-reset').addEventListener('click', () => {
            document.getElementById('cal-scale').value = 1.0;
            document.getElementById('cal-x').value = 0;
            document.getElementById('cal-y').value = 0;
            updateCSS();
        });
    }
}
window.addEventListener('DOMContentLoaded', initCalibrationUI);

async function selectOutfit(outfitId) {
    if(!catalogueData) return;
    
    selectedOutfit = catalogueData.catalogues.flatMap(c => c.outfits).find(o => o.id === outfitId);
    if (!selectedOutfit) return;

    showOutfitToast("Fitting your look...");

    const overlay = document.getElementById('dafitmatch-tryon-overlay');
    const overlayImage = document.getElementById('dafitmatch-tryon-image');
    const overlayVideo = document.getElementById('dafitmatch-tryon-video');
    const viewport = document.getElementById('playground-area');

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
        // 1. 3D GLB
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

        // 2. Try-On Image
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
                overlayImage.src = tryOnUrl;
                overlayImage.style.display = 'block';
                overlayVideo.style.display = 'none';
                
                // Show overlay
                overlay.style.display = 'block';
                overlay.style.visibility = 'visible';
                
                // Check calibration opacity slider
                const opSlider = document.getElementById('cal-opacity');
                const desiredOpacity = opSlider ? opSlider.value : '1';
                overlay.style.opacity = desiredOpacity;
                
                // Align calculation
                const aligned = alignTryOnImage(overlayImage, viewport, selectedOutfit.id);
                if (!aligned) {
                    failSafeRestore();
                    return;
                }
                
                // Final layout verification
                const rect = overlayImage.getBoundingClientRect();
                const computed = window.getComputedStyle(overlay);
                
                console.log(`[DaFitMatch] Overlay rect: ${rect.width}x${rect.height}`);
                
                if (rect.width > 0 && rect.height > 0 && computed.display !== 'none' && computed.visibility !== 'hidden') {
                    // Safe to hide original! (Unless calibration opacity demands comparison ghosting)
                    if (parseFloat(desiredOpacity) < 1.0) {
                        setOriginalCharacterVideosVisible(true);
                    } else {
                        setOriginalCharacterVideosVisible(false);
                    }
                    
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
</body>
"""

with open('index.html', 'w') as f:
    f.write(html + new_script)

print("Injected actual alignment math and per-outfit calibration.")
