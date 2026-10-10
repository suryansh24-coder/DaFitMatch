import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Remove mask from .stage
stage_css_pattern = r'(\.stage\s*\{[^}]*)background:\s*#a5c8e4;\s*-webkit-mask-image:[^;]+;\s*mask-image:[^;]+;'
def stage_replacer(match):
    return match.group(1) + "background: #a5c8e4;"
html = re.sub(stage_css_pattern, stage_replacer, html)

# 2. Add .stage::before
# Let's just insert it after `.stage { ... }`
insert_overlay = """
    .stage::before {
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0;
      height: 25vh;
      background: linear-gradient(to bottom, #a5c8e4 0%, transparent 100%);
      pointer-events: none;
      z-index: 10;
    }
"""
html = html.replace('background: #a5c8e4;\n    }', 'background: #a5c8e4;\n    }' + insert_overlay)

with open('index.html', 'w') as f:
    f.write(html)

print("Overlay fixed!")
