with open('index.html', 'r') as f:
    html = f.read()

# I will remove all these debug lines
debug_lines = [
    'tryOnImageEl.style.position = "absolute";',
    'tryOnImageEl.style.inset = "0";',
    'tryOnImageEl.style.width = "100%";',
    'tryOnImageEl.style.height = "100%";',
    'tryOnImageEl.style.objectFit = "contain";',
    'tryOnImageEl.style.zIndex = "9999";',
    'tryOnImageEl.style.opacity = "1";',
    'tryOnImageEl.style.display = "block";',
    'tryOnImageEl.style.visibility = "visible";',
    'tryOnImageEl.style.outline = "5px solid red";'
]

for line in debug_lines:
    html = html.replace(line, "")

with open('index.html', 'w') as f:
    f.write(html)

print("Cleaned up debug styles.")
