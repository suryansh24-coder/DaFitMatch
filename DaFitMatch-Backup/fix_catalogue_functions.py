import re

with open('index.html', 'r') as f:
    html = f.read()

# I will replace the entire block from function openCataloguePanel() to the start of document.addEventListener('DOMContentLoaded'
target = r'function openCataloguePanel\(\) \{.*?(?=document\.addEventListener\(\'DOMContentLoaded\', \(\) => \{)'
replacement = """function openCataloguePanel() {
    const drawer = document.getElementById('catalogue-drawer');
    const backdrop = document.getElementById('catalogue-backdrop');
    if(drawer && backdrop) {
        backdrop.classList.remove('opacity-0', 'invisible');
        drawer.classList.add('drawer-open');
        
        const cards = drawer.querySelectorAll('.apple-card');
        cards.forEach((card, index) => {
            card.style.transitionDelay = `${index * 60}ms`;
        });
    }
}

function closeCataloguePanel() {
    const drawer = document.getElementById('catalogue-drawer');
    const backdrop = document.getElementById('catalogue-backdrop');
    if(drawer && backdrop) {
        backdrop.classList.add('opacity-0', 'invisible');
        drawer.classList.remove('drawer-open');
        
        const cards = drawer.querySelectorAll('.apple-card');
        cards.forEach(card => {
            card.style.transitionDelay = '0ms';
        });
    }
}

"""

html = re.sub(target, replacement, html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(html)
