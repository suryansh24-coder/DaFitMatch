import re

with open('index.html', 'r') as f:
    html = f.read()

target1 = r'video\.pause\(\);\n\s*video\.muted = true;'
replacement1 = 'try { video.pause(); } catch(e){} try { video.muted = true; } catch(e){}'
html = re.sub(target1, replacement1, html)

target2 = r'if \(el\.tagName === \'VIDEO\'\) \{\n\s*el\.pause\(\);\n\s*el\.currentTime = el\.currentTime;\n\s*\}'
replacement2 = 'if (el.tagName === \'VIDEO\') { try { el.pause(); } catch(e){} try { el.currentTime = el.currentTime; } catch(e){} }'
html = re.sub(target2, replacement2, html)

with open('index.html', 'w') as f:
    f.write(html)
print("Patched potential crash.")
