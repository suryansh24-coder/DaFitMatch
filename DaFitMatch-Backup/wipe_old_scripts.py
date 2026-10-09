import re

with open('index.html', 'r') as f:
    html = f.read()

# Instead of complex regex, let's find all <script>...</script> blocks
# and remove the ones containing "selectOutfit"
def replacer(match):
    content = match.group(0)
    if 'selectOutfit' in content and 'function selectOutfit' in content:
        return ''  # Delete this script block entirely
    return content

# Match <script>...</script> (non-greedy)
html = re.sub(r'<script.*?</script>', replacer, html, flags=re.DOTALL)

# Also there might be stray closing tags or duplicated </body> tags
html = html.replace('</body>\n</body>', '</body>')

with open('index.html', 'w') as f:
    f.write(html)
print("Removed old scripts")
