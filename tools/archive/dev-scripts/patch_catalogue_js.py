import re

with open('index.html', 'r') as f:
    html = f.read()

# Replace openCataloguePanel
open_target = r'function openCataloguePanel\(\) \{.*?\}'
open_replacement = """function openCataloguePanel() {
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
}"""
html = re.sub(open_target, open_replacement, html, flags=re.DOTALL)

# Replace closeCataloguePanel
close_target = r'function closeCataloguePanel\(\) \{.*?\}'
close_replacement = """function closeCataloguePanel() {
    const drawer = document.getElementById('catalogue-drawer');
    const backdrop = document.getElementById('catalogue-backdrop');
    if(drawer && backdrop) {
        drawer.classList.add('translate-x-full');
        backdrop.classList.add('opacity-0', 'invisible');
        
        drawer.classList.remove('drawer-open');
        
        const cards = drawer.querySelectorAll('.apple-card');
        cards.forEach(card => {
            card.style.transitionDelay = '0ms';
        });
    }
}"""
html = re.sub(close_target, close_replacement, html, flags=re.DOTALL)

# Inject Mouse Light Effect JS at the end of the script tag that contains openCataloguePanel
script_target = r'(function closeCataloguePanel\(\) \{.*?\})'
script_injection = r"""\1

document.addEventListener('DOMContentLoaded', () => {
    const drawer = document.getElementById('catalogue-drawer');
    const light = document.getElementById('catalogue-light');
    
    if (drawer && light) {
        drawer.addEventListener('mousemove', (e) => {
            if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
            const rect = drawer.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            requestAnimationFrame(() => {
                light.style.transform = `translate(calc(-50% + ${x}px), calc(-50% + ${y}px))`;
                light.style.opacity = '1';
            });
        });
        
        drawer.addEventListener('mouseleave', () => {
            light.style.opacity = '0';
        });
    }
});
"""
html = re.sub(script_target, script_injection, html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(html)
