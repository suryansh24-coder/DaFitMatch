import re

with open('index.html', 'r') as f:
    html = f.read()

forensic_script = """
    // FORENSIC INJECTION
    setTimeout(() => {
        try {
            const vp = document.querySelector('#playground-area').getBoundingClientRect();
            const center = document.elementsFromPoint(vp.left + vp.width / 2, vp.top + vp.height / 2);
            const centerData = center.map(el => ({
                tag: el.tagName,
                id: el.id,
                class: el.className,
                zIndex: getComputedStyle(el).zIndex,
                display: getComputedStyle(el).display,
                visibility: getComputedStyle(el).visibility,
                opacity: getComputedStyle(el).opacity,
                src: el.src || el.currentSrc || ''
            }));
            
            const all = [...document.querySelectorAll('#playground-area *')];
            const activeEls = all.map(el => {
                const r = el.getBoundingClientRect();
                const s = getComputedStyle(el);
                return {
                    tag: el.tagName,
                    id: el.id,
                    class: typeof el.className === 'string' ? el.className : '',
                    display: s.display,
                    visibility: s.visibility,
                    opacity: s.opacity,
                    zIndex: s.zIndex,
                    width: Math.round(r.width),
                    height: Math.round(r.height)
                };
            }).filter(x => x.width > 100 && x.height > 100 && x.display !== 'none' && x.visibility !== 'hidden' && Number(x.opacity) > 0);
            
            const report = { center: centerData, active: activeEls };
            
            // Send to python server logs
            fetch('/FORENSIC_REPORT?data=' + encodeURIComponent(JSON.stringify(report)));
            
            // Also print to page so user sees it
            let pre = document.getElementById('forensic-output');
            if(!pre) {
                pre = document.createElement('pre');
                pre.id = 'forensic-output';
                pre.style.cssText = 'position:fixed;top:0;left:0;right:0;height:50vh;background:rgba(0,0,0,0.9);color:lime;font-size:10px;z-index:9999999;overflow:auto;padding:20px;';
                document.body.appendChild(pre);
            }
            pre.textContent = JSON.stringify(report, null, 2);
            
        } catch(e) {}
    }, 1000);
"""

# Inject into activateTryOnLayer when success is true
target = r'if \(desiredOpacity >= 1\.0\) \{\n\s*window\.dafitmatchTryOnState = \'TRY_ON_ACTIVE\';'
html = re.sub(target, target + forensic_script, html)

with open('index.html', 'w') as f:
    f.write(html)
