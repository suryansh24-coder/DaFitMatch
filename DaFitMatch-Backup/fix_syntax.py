import re

with open('index.html', 'r') as f:
    html = f.read()

target = r'function openCataloguePanel\(\) \{.*?\}\n\}\n\nfunction closeCataloguePanel\(\) \{'
replacement = """function openCataloguePanel() {
    const drawer = document.getElementById('catalogue-drawer');
    const backdrop = document.getElementById('catalogue-backdrop');
    if(drawer && backdrop) {
        drawer.classList.remove('translate-x-full');
        backdrop.classList.remove('opacity-0', 'invisible');
        
        drawer.classList.add('drawer-open');
        
        const cards = drawer.querySelectorAll('.apple-card');
        cards.forEach((card, index) => {
            card.style.transitionDelay = `${index * 60}ms`;
        });
    }
}

function closeCataloguePanel() {"""

html = re.sub(target, replacement, html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(html)
