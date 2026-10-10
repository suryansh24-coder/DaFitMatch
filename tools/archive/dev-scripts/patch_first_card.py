import re

with open('index.html', 'r') as f:
    html = f.read()

target = r'<!-- 01 Casual -->\n<div class="catalogue-option cursor-pointer apple-card p-5 rounded-2xl"'
replacement = r'<!-- 01 Casual -->\n<div class="catalogue-option cursor-pointer apple-card apple-card-active p-5 rounded-2xl"'
html = re.sub(target, replacement, html)

with open('index.html', 'w') as f:
    f.write(html)
