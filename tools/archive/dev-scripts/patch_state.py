import re

with open('index.html', 'r') as f:
    html = f.read()

target = r'if \(desiredOpacity >= 1\.0\) \{\n\s*stopALLOriginalVideos'
replacement = "if (desiredOpacity >= 1.0) {\n                window.dafitmatchTryOnState = 'TRY_ON_ACTIVE';\n                stopALLOriginalVideos"

html = re.sub(target, replacement, html)

# Also ensure deactivateTryOnLayer and normalFallback reset it.
# They both call restoreALLOriginalCharacterRendering() which sets it?
# Let's check restoreALLOriginalCharacterRendering.
# Wait, I didn't set window.dafitmatchTryOnState = 'NORMAL' inside restoreALLOriginalCharacterRendering.
# Let's set it at the top of deactivateTryOnLayer and normalFallback.

target_deact = r'const deactivateTryOnLayer = \(\) => \{'
replacement_deact = "const deactivateTryOnLayer = () => {\n        window.dafitmatchTryOnState = 'TRY_ON_FAILED';"
html = re.sub(target_deact, replacement_deact, html)

target_norm = r'const normalFallback = \(\) => \{'
replacement_norm = "const normalFallback = () => {\n        window.dafitmatchTryOnState = 'NORMAL';"
html = re.sub(target_norm, replacement_norm, html)


with open('index.html', 'w') as f:
    f.write(html)
