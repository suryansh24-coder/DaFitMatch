import re

with open('index.html', 'r') as f:
    html = f.read()

# Replace the condition to only move it if it's inside a .media element
target = r'document\.getElementById\(\'dafitmatch-tryon-overlay\'\)\.parentElement !== document\.body'
replacement = 'document.getElementById("dafitmatch-tryon-overlay").closest(".media") !== null'
html = re.sub(target, replacement, html)

with open('index.html', 'w') as f:
    f.write(html)
