import re

with open('index.html', 'r') as f:
    html = f.read()

target = r'<script>\nconsole\.log\(\n\s*\'\[DaFitMatch DEMO\] RUNTIME selectOutfit =.*?<\/script>\n\n'
html = re.sub(target, '', html, flags=re.DOTALL)

# Let me also remove the extra console.log at 1943 since the user said:
# "REMOVE the temporary logs: [DaFitMatch DEMO] RUNTIME selectOutfit, [DaFitMatch DEMO] FINAL selectOutFit"

html = re.sub(r'console\.log\(\'\[DaFitMatch DEMO\] selectOutfit global:\', typeof window\.selectOutfit\);\n', '', html)

with open('index.html', 'w') as f:
    f.write(html)
