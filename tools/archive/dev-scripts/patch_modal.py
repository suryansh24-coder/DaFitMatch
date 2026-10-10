import re

with open('index.html', 'r') as f:
    html = f.read()

# Remove the old google-config-warning from the HTML
target1 = r'<!-- Missing Client ID warning -->.*?</div>'
html = re.sub(target1, '', html, flags=re.DOTALL)

# Remove the interception logic from the modal
target2 = r'// Intercept modal open to check Google configuration.*?if \(originalCloseAuthModal\) \{'
html = re.sub(target2, 'if (originalCloseAuthModal) {', html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(html)
