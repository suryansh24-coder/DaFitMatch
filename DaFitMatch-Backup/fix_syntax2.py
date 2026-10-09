import re

with open('index.html', 'r') as f:
    html = f.read()

target = r'\$\{finalState\}`;\\n\}'
replacement = '${finalState}`;\n}'

html = re.sub(target, replacement, html)

with open('index.html', 'w') as f:
    f.write(html)
