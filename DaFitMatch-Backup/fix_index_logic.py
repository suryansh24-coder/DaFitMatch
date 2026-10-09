import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. We must delete any <script> block that defines selectOutfit.
# Let's extract everything except the <script> tags that contain "async function selectOutfit"

blocks = html.split('<script>')
new_html = blocks[0]

for block in blocks[1:]:
    if 'async function selectOutfit' in block:
        # Skip this block entirely (assuming it ends at the next </script>)
        # Wait, if there are multiple functions in that block, we might delete too much!
        # Let's see what else is in that block.
        pass
