import re

with open('index.html', 'r') as f:
    html = f.read()

target = r'function handleEmailSignIn.*?\}\n\n'
html = re.sub(target, '', html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(html)
