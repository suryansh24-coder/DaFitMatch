import re

with open('index.html', 'r') as f:
    html = f.read()

img_tag = """<img src="${outfit.image}" alt="${outfit.name}" class="absolute inset-0 w-full h-full object-cover" onerror="this.onerror=null; this.src='data:image/svg+xml;utf8,<svg xmlns=\\'http://www.w3.org/2000/svg\\' width=\\'100%\\' height=\\'100%\\'><rect width=\\'100%\\' height=\\'100%\\' fill=\\'%23f1f5f9\\'/><text x=\\'50%\\' y=\\'50%\\' font-family=\\'sans-serif\\' font-size=\\'14\\' fill=\\'%2394a3b8\\' text-anchor=\\'middle\\' dominant-baseline=\\'middle\\'>Image coming soon</text></svg>';" />"""

old_span = '<span class="text-slate-400 text-sm font-medium">Image coming soon</span>'

if old_span in html:
    html = html.replace(old_span, img_tag)
    with open('index.html', 'w') as f:
        f.write(html)
    print("Images injected into UI successfully!")
else:
    print("Could not find the placeholder span.")

