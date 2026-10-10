import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Update the Catalogue HTML to have an id="catalogue-content" so we can swap its contents.
content_old = '<!-- Content (Scrollable) -->\n  <div class="flex-1 overflow-y-auto p-6 sm:p-8 space-y-4">'
content_new = '<!-- Content (Scrollable) -->\n  <div id="catalogue-content" class="flex-1 overflow-y-auto p-6 sm:p-8 space-y-4">'
if content_old in html:
    html = html.replace(content_old, content_new)

# 2. Update the inline selectCatalogue arguments to pass the ID.
html = html.replace("selectCatalogue('Casual'", "selectCatalogue('casual', 'Casual'")
html = html.replace("selectCatalogue('Formal'", "selectCatalogue('formal', 'Formal'")
html = html.replace("selectCatalogue('Wedding & Festive'", "selectCatalogue('wedding-festive', 'Wedding & Festive'")
html = html.replace("selectCatalogue('Date Night'", "selectCatalogue('date-night', 'Date Night'")
html = html.replace("selectCatalogue('Streetwear'", "selectCatalogue('streetwear', 'Streetwear'")
html = html.replace("selectCatalogue('Couple Coordinated'", "selectCatalogue('couple-coordinated', 'Couple Coordinated'")


# 3. Update the JavaScript
old_js_pattern = re.compile(r'function selectCatalogue\(name, el\) \{.*?\}(?=\s*document\.addEventListener\(\'DOMContentLoaded\')', re.DOTALL)

new_js = """let catalogueData = null;
let originalCategoriesHtml = '';

async function fetchCatalogueData() {
    if (!catalogueData) {
        try {
            const res = await fetch('catalogue.json');
            catalogueData = await res.json();
        } catch(e) {
            console.error("Failed to load catalogue", e);
        }
    }
    return catalogueData;
}

const formatPrice = (price) => {
    return new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(price);
};

async function selectCatalogue(id, name, el) {
    // 1. Visual highlight
    document.querySelectorAll('.catalogue-option').forEach(opt => {
        opt.classList.remove('border-sky-400', 'bg-sky-50', 'shadow-md');
        opt.classList.add('border-slate-200/60', 'bg-white/50');
    });
    if(el) {
        el.classList.remove('border-slate-200/60', 'bg-white/50');
        el.classList.add('border-sky-400', 'bg-sky-50', 'shadow-md');
    }
    
    // Store in state
    window.dafitmatchState.catalogue = id;
    
    // Update button text
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
    }
    
    // Fetch JSON and render outfits in the drawer
    const contentBox = document.getElementById('catalogue-content');
    if(!originalCategoriesHtml && contentBox) {
        originalCategoriesHtml = contentBox.innerHTML;
    }
    
    const data = await fetchCatalogueData();
    if(data) {
        const cat = data.catalogues.find(c => c.id === id);
        if(cat) renderOutfits(cat);
    }
}

function renderOutfits(category) {
    const content = document.getElementById('catalogue-content');
    if(!content) return;
    
    let html = `
    <div class="mb-4">
        <button onclick="renderCategories()" class="text-sm font-semibold text-slate-500 hover:text-slate-800 flex items-center gap-1 mb-3 transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M15 19l-7-7 7-7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>
            Back
        </button>
        <h3 class="text-2xl font-bold text-slate-900">${category.name}</h3>
        <p class="text-sm text-slate-500 mt-1">${category.description}</p>
    </div>
    <div class="space-y-6 pb-12">
    `;

    category.outfits.forEach(outfit => {
        if(outfit.gender === 'couple') {
            html += `
            <div class="bg-white rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden flex flex-col hover:shadow-md transition-shadow">
                <div class="aspect-video bg-slate-100 flex items-center justify-center border-b border-slate-100 relative">
                    <span class="text-slate-400 text-sm font-medium">Image coming soon</span>
                    <div class="absolute top-3 left-3 bg-white/95 backdrop-blur-sm px-2.5 py-1 rounded-lg text-xs font-bold text-slate-800 shadow-sm border border-slate-200/60">
                        ${outfit.matchScore}% Style Match
                    </div>
                </div>
                <div class="p-5">
                    <div class="flex justify-between items-start mb-3">
                        <div>
                            <h4 class="text-lg font-bold text-slate-900">${outfit.name}</h4>
                            <p class="text-xs font-bold text-sky-600 tracking-wider uppercase mt-0.5">${outfit.occasion}</p>
                        </div>
                        <div class="text-right">
                            <span class="text-sm font-bold text-slate-800">${formatPrice(outfit.price)}</span>
                        </div>
                    </div>
                    
                    <div class="grid grid-cols-2 gap-3 mt-4 mb-4">
                        <div class="bg-slate-50 rounded-xl p-3 border border-slate-100">
                            <h5 class="text-[10px] font-bold text-slate-400 tracking-wider mb-2">PERSON 1</h5>
                            <ul class="text-xs font-medium text-slate-600 space-y-1.5">
                                ${outfit.person1.items.map(i => `<li>• ${i}</li>`).join('')}
                            </ul>
                        </div>
                        <div class="bg-slate-50 rounded-xl p-3 border border-slate-100">
                            <h5 class="text-[10px] font-bold text-slate-400 tracking-wider mb-2">PERSON 2</h5>
                            <ul class="text-xs font-medium text-slate-600 space-y-1.5">
                                ${outfit.person2.items.map(i => `<li>• ${i}</li>`).join('')}
                            </ul>
                        </div>
                    </div>
                    
                    <div class="flex flex-wrap items-center gap-1.5 mb-5">
                        <span class="text-[10px] font-bold uppercase tracking-wider text-slate-500 bg-slate-100 px-2 py-1 rounded-md">${outfit.coordination}</span>
                        <span class="text-xs font-medium text-slate-500 ml-1">${outfit.palette.join(' · ')}</span>
                    </div>
                    
                    <button class="w-full py-2.5 bg-slate-900 text-white rounded-xl font-bold text-sm hover:bg-slate-800 transition-colors shadow-sm">
                        View Look
                    </button>
                </div>
            </div>`;
        } else {
            html += `
            <div class="bg-white rounded-2xl border border-slate-200/80 shadow-sm overflow-hidden flex flex-col hover:shadow-md transition-shadow">
                <div class="aspect-[4/3] sm:aspect-video bg-slate-100 flex items-center justify-center border-b border-slate-100 relative">
                    <span class="text-slate-400 text-sm font-medium">Image coming soon</span>
                    <div class="absolute top-3 left-3 bg-white/95 backdrop-blur-sm px-2.5 py-1 rounded-lg text-xs font-bold text-slate-800 shadow-sm border border-slate-200/60">
                        ${outfit.matchScore}% Style Match
                    </div>
                    <div class="absolute top-3 right-3 bg-white/95 backdrop-blur-sm px-2.5 py-1 rounded-lg text-[10px] font-bold uppercase tracking-wider text-slate-500 shadow-sm border border-slate-200/60">
                        ${outfit.platform}
                    </div>
                </div>
                <div class="p-5">
                    <div class="flex justify-between items-start mb-3">
                        <div>
                            <h4 class="text-lg font-bold text-slate-900">${outfit.name}</h4>
                            <p class="text-xs font-bold text-sky-600 tracking-wider uppercase mt-0.5">${outfit.style}</p>
                        </div>
                        <div class="text-right">
                            <span class="text-sm font-bold text-slate-800">${formatPrice(outfit.price)}</span>
                        </div>
                    </div>
                    
                    <div class="mt-4 mb-5">
                        <ul class="text-sm font-medium text-slate-600 space-y-1.5">
                            ${outfit.items.map(i => `<li class="flex items-start gap-2"><span class="text-slate-300">•</span> ${i}</li>`).join('')}
                        </ul>
                    </div>
                    
                    <div class="flex flex-wrap gap-1.5 mb-5">
                        ${outfit.colors.map(c => `<span class="text-xs font-medium text-slate-600 bg-slate-50 px-2 py-1 rounded-md border border-slate-100">${c}</span>`).join('')}
                    </div>
                    
                    <button class="w-full py-2.5 bg-slate-900 text-white rounded-xl font-bold text-sm hover:bg-slate-800 transition-colors shadow-sm">
                        View Look
                    </button>
                </div>
            </div>`;
        }
    });
    
    html += `</div>`;
    content.innerHTML = html;
    content.scrollTop = 0;
}

function renderCategories() {
    const content = document.getElementById('catalogue-content');
    if(content && originalCategoriesHtml) {
        content.innerHTML = originalCategoriesHtml;
    }
}
"""

if old_js_pattern.search(html):
    html = old_js_pattern.sub(new_js, html)
else:
    print("Could not find old JS block to replace.")

with open('index.html', 'w') as f:
    f.write(html)
print("Outfit rendering injected successfully!")
