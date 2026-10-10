import re

# 1. Update index.html to add the code comment
with open('index.html', 'r') as f:
    html = f.read()

comment = """    <!-- 
      IMPORTANT ARCHITECTURE NOTE:
      The following video elements (vid-clothing-fwd, etc.) act as a pre-rendered 
      visual fallback for the hero character. Because they are 2D MP4 files, they 
      cannot receive arbitrary 3D clothing GLBs dynamically via Three.js.
      
      When public/models/character/base-character.glb is eventually supplied, 
      the three-viewer.js module will automatically hide these videos and take 
      over rendering with a real-time WebGL canvas.
    -->"""

if "IMPORTANT ARCHITECTURE NOTE" not in html:
    html = html.replace('<!-- Base / Clothing FWD -->', comment + '\n    <!-- Base / Clothing FWD -->')

with open('index.html', 'w') as f:
    f.write(html)

# 2. Update three-viewer.js to refine the diagnostic text
with open('three-viewer.js', 'r') as f:
    js = f.read()

old_diag_text = """
CHARACTER:
${this.diagState.charFound ? '✓ base-character.glb found' : '✗ base-character.glb missing'}
"""
new_diag_text = """
3D CHARACTER:
${this.diagState.charFound ? '✓ base-character.glb loaded' : 'waiting for base-character.glb'}
"""
js = js.replace(old_diag_text.strip(), new_diag_text.strip())

with open('three-viewer.js', 'w') as f:
    f.write(js)

print("Project finalized with comments and updated diagnostics.")
