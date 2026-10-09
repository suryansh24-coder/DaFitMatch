import re

with open('index.html', 'r') as f:
    html = f.read()

# Bust the cache for catalogue.json
html = html.replace("fetch('catalogue.json')", "fetch('catalogue.json?v=' + Date.now())")

with open('index.html', 'w') as f:
    f.write(html)
