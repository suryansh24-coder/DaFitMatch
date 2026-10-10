import re

with open('index.html', 'r') as f:
    html = f.read()

old_func = """    // Update button text
    const catBtn = document.querySelector('.option-btn[data-id="clothing"]');
    if(catBtn) {
        catBtn.textContent = 'Catalogue → ' + name;
    }"""

new_func = """    // Update button text
    const catBtn = document.querySelector('.option-btn[data-id="clothing"]');
    if(catBtn) {
        catBtn.textContent = 'Catalogue → ' + name;
        
        // Let the DOM update first
        setTimeout(() => {
            if (catBtn.classList.contains('active')) {
                const activeBg = document.querySelector('.active-bg');
                if (activeBg) {
                    const rect = catBtn.getBoundingClientRect();
                    const parentRect = catBtn.parentElement.getBoundingClientRect();
                    activeBg.style.width = rect.width + 'px';
                    activeBg.style.height = rect.height + 'px';
                    const dx = rect.left - parentRect.left - 6;
                    const dy = rect.top - parentRect.top - 6;
                    activeBg.style.transform = `translate(${dx}px, ${dy}px)`;
                }
            }
        }, 50);
    }"""

if old_func in html:
    html = html.replace(old_func, new_func)
    with open('index.html', 'w') as f:
        f.write(html)
    print("Function updated!")
else:
    print("Could not find the function to update.")
