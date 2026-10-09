import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Inject Import Map
import_map = """
<script type="importmap">
  {
    "imports": {
      "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
      "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"
    }
  }
</script>
"""
if "importmap" not in html:
    html = html.replace('</head>', import_map + '\n</head>')

# 2. Inject webgl container
if 'id="webgl-container"' not in html:
    container_html = '\n    <div id="webgl-container" class="media" style="z-index: 5; pointer-events: none; visibility: visible;"></div>\n'
    html = html.replace('<!-- Base / Clothing FWD -->', container_html + '    <!-- Base / Clothing FWD -->')

# 3. Inject Module script and update selectOutfit
script_update = """
<script type="module">
  import { FittingRoom3D } from './three-viewer.js';
  window.fittingRoom = new FittingRoom3D('webgl-container');
</script>
"""
if "FittingRoom3D" not in html:
    html = html.replace('</body>', script_update + '\n</body>')

# 4. Modify existing selectOutfit to call the 3D viewer
old_select = """
        if (response.ok) {
            // CLOTHING LOADING SYSTEM (Stubbed for future WebGL implementation)
"""
new_select = """
        if (response.ok) {
            if (window.fittingRoom) {
                const success = await window.fittingRoom.loadOutfit(selectedOutfit);
                if (success) {
                    showOutfitToast("Outfit applied to character.");
                    return;
                }
            }
"""
html = html.replace(old_select, new_select)

with open('index.html', 'w') as f:
    f.write(html)
print("Updated index.html with 3D integration.")
