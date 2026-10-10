with open('index.html', 'r') as f:
    html = f.read()

target = """            const imgEl = document.getElementById('dafitmatch-tryon-image');
            if(imgEl) {
                imgEl.style.setProperty('--tryon-scale', scale);
                imgEl.style.setProperty('--tryon-x', x + 'px');
                imgEl.style.setProperty('--tryon-y', y + 'px');
            }"""

replacement = """            const imgEl = document.getElementById('dafitmatch-tryon-image');
            if(imgEl) {
                imgEl.style.setProperty('--tryon-scale', scale);
                imgEl.style.setProperty('--tryon-x', x + 'px');
                imgEl.style.setProperty('--tryon-y', y + 'px');
            }
            
            const vidEl = document.getElementById('dafitmatch-tryon-video');
            if(vidEl) {
                vidEl.style.setProperty('--tryon-scale', scale);
                vidEl.style.setProperty('--tryon-x', x + 'px');
                vidEl.style.setProperty('--tryon-y', y + 'px');
            }"""

html = html.replace(target, replacement)

with open('index.html', 'w') as f:
    f.write(html)
print("Calibration UI patched for video.")
