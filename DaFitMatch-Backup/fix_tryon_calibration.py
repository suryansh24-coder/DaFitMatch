import re

with open('index.html', 'r') as f:
    html = f.read()

# I need to add CSS variables to the overlay
html = html.replace('id="dafitmatch-tryon-overlay"', 'id="dafitmatch-tryon-overlay" style="--tryon-scale: 1; --tryon-x: 0px; --tryon-y: 0px; position: absolute; inset: 0; width: 100%; height: 100%; z-index: 100; display: none; visibility: hidden; opacity: 0; pointer-events: none;"')
# Remove previous inline style if there are duplicates (I'll just find and replace properly).

# Let's fix the overlay inline styles and image inline styles exactly
overlay_regex = r'<div id="dafitmatch-tryon-overlay".*?>\s*<img id="dafitmatch-tryon-image".*?/>\s*<video id="dafitmatch-tryon-video".*?></video>\s*</div>'
new_overlay = """
<div id="dafitmatch-tryon-overlay" style="--tryon-scale: 1; --tryon-x: 0px; --tryon-y: 0px; position: absolute; inset: 0; width: 100%; height: 100%; z-index: 100; display: none; visibility: hidden; opacity: 0; pointer-events: none;">
    <img id="dafitmatch-tryon-image" style="width: 100%; height: 100%; object-fit: contain; object-position: center; transform: translate(var(--tryon-x), var(--tryon-y)) scale(var(--tryon-scale));" />
    <video id="dafitmatch-tryon-video" muted playsinline loop style="width: 100%; height: 100%; object-fit: contain; object-position: center; display: none; transform: translate(var(--tryon-x), var(--tryon-y)) scale(var(--tryon-scale));"></video>
</div>
"""
html = re.sub(overlay_regex, new_overlay.strip(), html, flags=re.DOTALL)


# Now inject the calibration UI into Javascript
# Find the end of selectOutfit and inject createCalibrationUI()
# Also load calibration values from localStorage inside selectOutfit if available

calibration_logic = """
function loadTryOnCalibration() {
    try {
        const saved = localStorage.getItem('dafitmatch_tryon_calibration');
        if (saved) {
            const data = JSON.parse(saved);
            const overlay = document.getElementById('dafitmatch-tryon-overlay');
            if (overlay && data.scale !== undefined) {
                overlay.style.setProperty('--tryon-scale', data.scale);
                overlay.style.setProperty('--tryon-x', data.x + 'px');
                overlay.style.setProperty('--tryon-y', data.y + 'px');
            }
        }
    } catch (e) {}
}

function initCalibrationUI() {
    if (window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') return;
    
    // Auto load on init
    loadTryOnCalibration();
    
    let panel = document.getElementById('tryon-calibration-panel');
    if (!panel) {
        panel = document.createElement('div');
        panel.id = 'tryon-calibration-panel';
        panel.className = 'fixed top-4 left-4 bg-slate-900/95 backdrop-blur text-white font-mono text-xs p-4 rounded-xl shadow-2xl z-50 border border-slate-700/50 w-64 flex flex-col gap-3';
        
        panel.innerHTML = `
            <div class="font-bold text-sky-400 mb-1 border-b border-slate-700 pb-1">TRY-ON CALIBRATION</div>
            
            <label class="flex flex-col gap-1">
                <div class="flex justify-between"><span>Scale</span> <span id="cal-scale-val">1.00</span></div>
                <input type="range" id="cal-scale" min="0.5" max="2.5" step="0.01" value="1.0" class="w-full">
            </label>
            
            <label class="flex flex-col gap-1">
                <div class="flex justify-between"><span>X Offset</span> <span id="cal-x-val">0px</span></div>
                <input type="range" id="cal-x" min="-500" max="500" step="1" value="0" class="w-full">
            </label>
            
            <label class="flex flex-col gap-1">
                <div class="flex justify-between"><span>Y Offset</span> <span id="cal-y-val">0px</span></div>
                <input type="range" id="cal-y" min="-500" max="500" step="1" value="0" class="w-full">
            </label>
            
            <label class="flex flex-col gap-1">
                <div class="flex justify-between text-yellow-400"><span>Overlay Opacity (Debug)</span> <span id="cal-op-val">1.0</span></div>
                <input type="range" id="cal-opacity" min="0" max="1" step="0.05" value="1.0" class="w-full accent-yellow-400">
            </label>
            
            <button id="cal-save" class="mt-2 w-full py-1.5 bg-sky-600 hover:bg-sky-500 rounded text-white font-bold transition-colors">SAVE CALIBRATION</button>
            <button id="cal-reset" class="w-full py-1.5 bg-slate-700 hover:bg-slate-600 rounded text-white font-bold transition-colors">RESET</button>
        `;
        document.body.appendChild(panel);
        
        const overlay = document.getElementById('dafitmatch-tryon-overlay');
        
        // Sync inputs with saved values if any
        try {
            const saved = localStorage.getItem('dafitmatch_tryon_calibration');
            if (saved) {
                const data = JSON.parse(saved);
                document.getElementById('cal-scale').value = data.scale;
                document.getElementById('cal-x').value = data.x;
                document.getElementById('cal-y').value = data.y;
                document.getElementById('cal-scale-val').textContent = parseFloat(data.scale).toFixed(2);
                document.getElementById('cal-x-val').textContent = data.x + 'px';
                document.getElementById('cal-y-val').textContent = data.y + 'px';
            }
        } catch(e) {}
        
        const updateCSS = () => {
            const scale = document.getElementById('cal-scale').value;
            const x = document.getElementById('cal-x').value;
            const y = document.getElementById('cal-y').value;
            const op = document.getElementById('cal-opacity').value;
            
            document.getElementById('cal-scale-val').textContent = parseFloat(scale).toFixed(2);
            document.getElementById('cal-x-val').textContent = x + 'px';
            document.getElementById('cal-y-val').textContent = y + 'px';
            document.getElementById('cal-op-val').textContent = parseFloat(op).toFixed(2);
            
            overlay.style.setProperty('--tryon-scale', scale);
            overlay.style.setProperty('--tryon-x', x + 'px');
            overlay.style.setProperty('--tryon-y', y + 'px');
            
            // Override opacity explicitly for calibration
            if (overlay.style.display !== 'none') {
                overlay.style.opacity = op;
                
                // If opacity is < 1, explicitly FORCE original videos to be visible so we can compare
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
            const data = {
                scale: parseFloat(document.getElementById('cal-scale').value),
                x: parseInt(document.getElementById('cal-x').value),
                y: parseInt(document.getElementById('cal-y').value)
            };
            localStorage.setItem('dafitmatch_tryon_calibration', JSON.stringify(data));
            console.log("TRY-ON CALIBRATION SAVED\\n", JSON.stringify(data, null, 2));
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
"""

# Append logic to the end of the final script tag
script_closing = "</script>\n</body>"
html = html.replace(script_closing, calibration_logic + "\n" + script_closing)

# Also ensure setOriginalCharacterVideosVisible forces correctly based on calibration panel opacity
# In selectOutfit(), we set opacities. But the user explicitly requested:
# "4. Show try-on image at ~50% opacity temporarily. 5. Confirm alignment. 6. Fade try-on image to 100%. 7. Hide original MP4."
# Wait, they want a calibration mode for development. The calibration panel opacity slider achieves this.

with open('index.html', 'w') as f:
    f.write(html)
print("Injected calibration panel.")
