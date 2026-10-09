import re

with open('index.html', 'r') as f:
    html = f.read()

# Split by <script>
parts = html.split('<script>')
new_parts = [parts[0]]

for part in parts[1:]:
    if 'function selectOutfit' in part or 'let selectedOutfit = null;' in part:
        # skip this script block completely
        # part actually contains everything up to the next <script>, but wait, split('<script>') loses the tag.
        # It's better to split by </script> first.
        pass
    else:
        new_parts.append('<script>' + part)

html = "".join(new_parts)

# Also check if there are <script type="module"> etc that might have been skipped?
# Actually, I'll just do this:

html2 = ""
in_bad_script = False
for line in html.splitlines(True):
    if '<script' in line and 'type="importmap"' not in line and 'type="module"' not in line and 'src=' not in line and 'data-purpose=' not in line:
        # maybe a raw script block
        pass
    
# Let's use BeautifulSoup! It's reliable.
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, 'html.parser')
for script in soup.find_all('script'):
    if script.string and 'function selectOutfit' in script.string:
        script.decompose()
        
with open('index.html', 'w') as f:
    f.write(str(soup))
