import re

with open('index.html', 'r') as f:
    html = f.read()

target = r'if \(!selectedOutfit\) return;\n'
replacement = 'if (!selectedOutfit) return;\n\n    // DEMO OVERRIDE: Delete tryOnVideo unconditionally to force image path and avoid 404s\n    delete selectedOutfit.tryOnVideo;\n'

html = re.sub(target, replacement, html)

with open('index.html', 'w') as f:
    f.write(html)
