import re

with open('index.html', 'r') as f:
    html = f.read()

target = r'transition: transform 600ms cubic-bezier\(0\.16, 1, 0\.3, 1\);'
replacement = 'transition: transform 600ms cubic-bezier(0.16, 1, 0.3, 1), opacity 400ms ease, visibility 400ms ease;'
html = html.replace(target, replacement)

with open('index.html', 'w') as f:
    f.write(html)
