import re

with open('index.html', 'r') as f:
    html = f.read()

# Replace text-white/90 and text-white/80 inside the specific svg classes
# Pattern for the SVG tags we want to change
# We know they start with <svg class="w-3.5 h-3.5 text-white/
# and they are inside the <nav> block

def svg_replacer(match):
    full_svg = match.group(0)
    # Replace the white text classes with the navy color
    full_svg = full_svg.replace('text-white/90', 'text-[#17233B]')
    full_svg = full_svg.replace('text-white/80', 'text-[#17233B]')
    return full_svg

# Find the nav block first to be safe
nav_pattern = r'(<nav[^>]*id="main-nav-bar".*?</nav>)'
def nav_replacer(match):
    nav_block = match.group(1)
    # Inside the nav block, replace the specific SVGs
    svg_pattern = r'<svg class="w-3\.5 h-3\.5 text-white/[89]0[^>]*>.*?</svg>'
    nav_block = re.sub(svg_pattern, svg_replacer, nav_block, flags=re.DOTALL)
    return nav_block

html = re.sub(nav_pattern, nav_replacer, html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(html)

print("Icons fixed!")
