import re

with open('index.html', 'r') as f:
    html = f.read()

target = r'<script>\n// Escape key to close.*?<\/script>'

new_script = """<script>
// Escape key to close
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        if (typeof closeAuthModal === 'function') closeAuthModal();
    }
});
</script>"""

html = re.sub(target, new_script, html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(html)
