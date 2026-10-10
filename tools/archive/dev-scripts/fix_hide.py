import re

with open('index.html', 'r') as f:
    html = f.read()

target = r'if \(desiredOpacity >= 1\.0\) \{.*?console\.log\(\'\[DaFitMatch DEMO\] TRY-ON IMAGE ACTIVE:\', imagePath\);'

replacement = """
            window.dafitmatchTryOnState = 'TRY_ON_ACTIVE';
            console.log('[DaFitMatch DEMO] TRY-ON IMAGE ACTIVE:', imagePath);
            hideALLOriginalCharacterRendering();
            stopALLOriginalVideos();
"""

html = re.sub(target, replacement, html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(html)
