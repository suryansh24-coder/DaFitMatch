import re

with open('index.html', 'r') as f:
    html = f.read()

# Remove the internal header
header_pattern = r'<header>\s*<div class="meta".*?<span>The Fit Check</span>.*?</div>.*?<a href="https://app.ltx.io/"[^>]*>Try now</a>\s*</header>'
new_html = re.sub(header_pattern, '', html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(new_html)

print("Inner header removed!")
