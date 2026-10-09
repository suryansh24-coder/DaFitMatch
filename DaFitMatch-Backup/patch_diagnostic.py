import re

with open('index.html', 'r') as f:
    html = f.read()

target = r'function updateTryOnDiagnostics\(diag\)\s*\{.*?\}\n'

new_func = """function updateTryOnDiagnostics(diag) {
    if (window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') return;
    
    let overlay = document.getElementById('tryon-diagnostic-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'tryon-diagnostic-overlay';
        overlay.className = 'fixed bottom-4 right-4 bg-slate-900/95 backdrop-blur text-sky-400 font-mono text-xs p-4 rounded-xl shadow-2xl z-50 border border-slate-700/50 whitespace-pre-wrap';
        document.body.appendChild(overlay);
    }
    
    const videos = Array.from(document.querySelectorAll('.media video, video.media, video[id^="vid-"]'))
        .filter(v => v.id !== 'dafitmatch-tryon-video');
        
    const active = videos.filter(v => v === window.activeVid).length;
    const paused = videos.filter(v => v.paused).length;
    const hidden = videos.filter(v => window.getComputedStyle(v).display === 'none' || window.getComputedStyle(v).visibility === 'hidden').length;
    
    const overlayTryon = document.getElementById('dafitmatch-tryon-overlay');
    const tryonZ = overlayTryon ? window.getComputedStyle(overlayTryon).zIndex : 'N/A';
    
    let originalZ = 'N/A';
    if (window.activeVid) {
        originalZ = window.getComputedStyle(window.activeVid).zIndex;
    }
    
    const isTryOnVisible = overlayTryon && window.getComputedStyle(overlayTryon).display !== 'none';
    
    let finalState = 'ORIGINAL MP4 ACTIVE';
    if (diag.displayMode.includes('FAILED')) finalState = 'TRY-ON FAILED — ORIGINAL RESTORED';
    else if (diag.displayMode.includes('TRY-ON')) finalState = 'TRY-ON ACTIVE';
    
    overlay.textContent = `TRY-ON DIAGNOSTICS

OUTFIT: ${diag.id}
ASSET: ${diag.displayMode}

ORIGINAL CHARACTER VIDEOS:
Found: ${videos.length}
Active: ${active}
Paused: ${paused}
Hidden: ${hidden}

TRY-ON:
${isTryOnVisible ? 'VISIBLE' : 'HIDDEN'}

TRY-ON LAYER:
z-index: ${tryonZ}

ORIGINAL LAYER:
z-index: ${originalZ}

FINAL STATE:
${finalState}`;
}
"""

html = re.sub(target, new_func, html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(html)
