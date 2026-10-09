import re

with open('index.html', 'r') as f:
    html = f.read()

target = r'function updateTryOnDiagnostics\(diag\) \{'
replacement = 'function updateTryOnDiagnostics(diag) {\n    const overlay = document.getElementById("tryon-diagnostic-overlay");\n    if (overlay) overlay.remove();\n    return; // DEMO: Remove diagnostics from screen\n'

html = re.sub(target, replacement, html)

with open('index.html', 'w') as f:
    f.write(html)
