import re
from bs4 import BeautifulSoup

with open('index.html', 'r') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Remove old try-on elements
old_img = soup.find(id='try-on-image')
if old_img: old_img.decompose()
old_vid = soup.find(id='try-on-video')
if old_vid: old_vid.decompose()

# Find the playground-area
playground_area = soup.find(id='playground-area')

if playground_area:
    # Create the new overlay div
    overlay_html = """
    <div id="dafitmatch-tryon-overlay" style="position: absolute; inset: 0; width: 100%; height: 100%; z-index: 100; display: none; visibility: hidden; opacity: 0; pointer-events: none;">
        <img id="dafitmatch-tryon-image" style="width: 100%; height: 100%; object-fit: contain; object-position: center;" />
        <video id="dafitmatch-tryon-video" muted playsinline loop style="width: 100%; height: 100%; object-fit: contain; object-position: center; display: none;"></video>
    </div>
    """
    overlay_soup = BeautifulSoup(overlay_html, 'html.parser')
    playground_area.append(overlay_soup)

with open('index.html', 'w') as f:
    f.write(str(soup))

print("Overlay injected.")
