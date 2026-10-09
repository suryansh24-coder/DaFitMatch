import re

with open('index.html', 'r') as f:
    html = f.read()

css_target = r'\.apple-drawer \{\n\s*background: rgba\(255, 255, 255, 0\.72\);'
css_replacement = """.apple-drawer {
    background: rgba(255, 255, 255, 0.72);
    /* Strict Visibility Constraints */
    visibility: hidden;
    opacity: 0;
    pointer-events: none;
    transform: translateX(100%);
}

.apple-drawer.drawer-open {
    visibility: visible !important;
    opacity: 1 !important;
    pointer-events: auto !important;
    transform: translateX(0) !important;
}

.apple-drawer {"""
html = re.sub(css_target, css_replacement, html, count=1)

html = html.replace('translate-x-full', '')

with open('index.html', 'w') as f:
    f.write(html)
