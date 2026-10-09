import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Update the transition section
old_transition = r'<section class="bg-gradient-to-b from-\[#f4f8fb\] to-\[#ffffff\] py-16 text-center relative" data-purpose="scroll-transition" id="playground">.*?</div>\n</section>'
new_transition = """<section class="w-full h-32 md:h-48 relative" style="background: linear-gradient(to bottom, #f4f8fb 0%, #a5c8e4 100%);" data-purpose="scroll-transition" id="playground">
</section>"""
html = re.sub(old_transition, new_transition, html, flags=re.DOTALL)

# 2. Update .stage CSS to have the matching background and a mask
# Find .stage { ... }
stage_css_pattern = r'(\.stage\s*\{[^}]*)background:\s*#[0-9a-fA-F]+;'
# We replace background: #000; with our new background and add mask
def stage_replacer(match):
    prefix = match.group(1)
    return prefix + """background: #a5c8e4;
      -webkit-mask-image: linear-gradient(to bottom, transparent 0%, black 15%);
      mask-image: linear-gradient(to bottom, transparent 0%, black 15%);"""

html = re.sub(stage_css_pattern, stage_replacer, html)

with open('index.html', 'w') as f:
    f.write(html)

print("Transition fixed!")
