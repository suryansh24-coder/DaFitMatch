with open('index.html', 'r') as f:
    html = f.read()

target = "const imgAvailable = await new Promise((resolve) => {"
log = 'console.log("[DaFitMatch Try-On] Loading image:", selectedOutfit.tryOnImage);\n            '
html = html.replace(target, log + target)

with open('index.html', 'w') as f:
    f.write(html)
print("Log injected.")
