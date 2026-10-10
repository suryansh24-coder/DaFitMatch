import re

with open('index.html', 'r') as f:
    html = f.read()

target = r'function openCataloguePanel\(\) \{'
replacement = """function openCataloguePanel() {
    console.log('[DaFitMatch Catalogue] OPEN CLICKED');
    setTimeout(() => {
        const drawer = document.getElementById('catalogue-drawer');
        console.log('[DaFitMatch Catalogue] DRAWER OPENED', {
            exists: !!drawer,
            className: drawer?.className,
            display: drawer ? getComputedStyle(drawer).display : null,
            visibility: drawer ? getComputedStyle(drawer).visibility : null,
            opacity: drawer ? getComputedStyle(drawer).opacity : null,
            transform: drawer ? getComputedStyle(drawer).transform : null,
            zIndex: drawer ? getComputedStyle(drawer).zIndex : null
        });
    }, 50);
"""

html = html.replace(target, replacement)

with open('index.html', 'w') as f:
    f.write(html)
