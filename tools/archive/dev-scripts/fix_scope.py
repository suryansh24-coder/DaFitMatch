import re

with open('index.html', 'r') as f:
    html = f.read()

target = r'async function selectOutfit\(outfitId\) \{'
replacement = 'window.selectOutfit = async function(outfitId) {'

html = re.sub(target, replacement, html)

# Also add the temporary verification right after the assignment
target2 = r'window\.selectOutfit = async function\(outfitId\) \{'
replacement2 = "console.log('[DaFitMatch DEMO] selectOutfit global:', typeof window.selectOutfit);\n\nwindow.selectOutfit = async function(outfitId) {"
html = re.sub(target2, replacement2, html)

# Let's just put the console.log outside the function so it runs on load.
# The previous line did put it before the assignment. Wait, if it runs before assignment, it prints 'undefined'.
# Better to put it AFTER the function block.
# Actually, wait, it's easier to put `console.log(...)` inside the script block or inside DOMContentLoaded.

html = html.replace("console.log('[DaFitMatch DEMO] selectOutfit global:', typeof window.selectOutfit);", "")
target_verification = "window.dafitmatchTryOnState = 'NORMAL';"
html = html.replace(target_verification, target_verification + "\nconsole.log('[DaFitMatch DEMO] selectOutfit global:', typeof window.selectOutfit);")


with open('index.html', 'w') as f:
    f.write(html)
