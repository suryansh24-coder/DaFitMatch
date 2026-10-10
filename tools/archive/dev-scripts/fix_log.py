with open('index.html', 'r') as f:
    html = f.read()

# Remove all occurrences
html = html.replace("console.log('[DaFitMatch DEMO] selectOutfit global:', typeof window.selectOutfit);", "")

# Add it exactly right after the assignment
target = "window.selectOutfit = async function(outfitId) {"
replacement = "window.selectOutfit = async function(outfitId) {\n"
html = html.replace(target, replacement)

# Add it at the end of the script block
target2 = "window.selectOutfit = async function(outfitId) {"
# Actually, the user asked: "After the page loads, add this temporary verification"
# So let's add it in the DOMContentLoaded block
html = html.replace("window.addEventListener('DOMContentLoaded', initCalibrationUI);", "window.addEventListener('DOMContentLoaded', initCalibrationUI);\nconsole.log('[DaFitMatch DEMO] selectOutfit global:', typeof window.selectOutfit);")

with open('index.html', 'w') as f:
    f.write(html)
