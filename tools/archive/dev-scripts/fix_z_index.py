import re

with open('index.html', 'r') as f:
    html = f.read()

# Update Backdrop z-index
html = html.replace('z-[190]', 'z-[9999]')

# Update Drawer z-index
html = html.replace('z-[200]', 'z-[10000]')

with open('index.html', 'w') as f:
    f.write(html)
