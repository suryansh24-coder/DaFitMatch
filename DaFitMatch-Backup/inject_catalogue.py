import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. HTML Markup
catalogue_html = """
<!-- Catalogue Drawer -->
<div id="catalogue-backdrop" onclick="closeCataloguePanel()" class="fixed inset-0 bg-slate-900/10 backdrop-blur-[2px] z-[190] opacity-0 invisible transition-all duration-300 cursor-pointer"></div>

<div id="catalogue-drawer" class="fixed inset-y-0 right-0 w-full sm:w-[380px] md:w-[440px] bg-white/80 backdrop-blur-2xl border-l border-white/60 shadow-2xl z-[200] transform translate-x-full transition-transform duration-300 ease-out flex flex-col">
  <!-- Header -->
  <div class="px-8 py-6 border-b border-slate-200/50 flex items-center justify-between bg-white/40">
    <div>
      <h2 class="text-xs font-bold tracking-widest text-slate-400 uppercase mb-1">Catalogue</h2>
      <h3 class="text-xl font-semibold text-slate-800">Choose your style direction</h3>
    </div>
    <button onclick="closeCataloguePanel()" class="w-10 h-10 rounded-full bg-slate-100/80 text-slate-500 flex items-center justify-center hover:bg-slate-200 hover:text-slate-800 transition-colors">
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M6 18L18 6M6 6l12 12" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
    </button>
  </div>
  
  <!-- Content (Scrollable) -->
  <div class="flex-1 overflow-y-auto p-6 sm:p-8 space-y-4">
    <!-- 01 Casual -->
    <div onclick="selectCatalogue('Casual', this)" class="catalogue-option group relative p-5 rounded-2xl border border-slate-200/60 bg-white/50 hover:bg-white hover:shadow-lg hover:border-sky-300 cursor-pointer transition-all duration-200">
      <div class="text-xs font-bold text-sky-600 mb-1 font-mono">01</div>
      <h4 class="text-lg font-semibold text-slate-800 mb-1">Casual</h4>
      <p class="text-sm text-slate-500 font-medium leading-relaxed">Everyday relaxed fashion</p>
    </div>
    
    <!-- 02 Formal -->
    <div onclick="selectCatalogue('Formal', this)" class="catalogue-option group relative p-5 rounded-2xl border border-slate-200/60 bg-white/50 hover:bg-white hover:shadow-lg hover:border-sky-300 cursor-pointer transition-all duration-200">
      <div class="text-xs font-bold text-sky-600 mb-1 font-mono">02</div>
      <h4 class="text-lg font-semibold text-slate-800 mb-1">Formal</h4>
      <p class="text-sm text-slate-500 font-medium leading-relaxed">Office, business and elegant occasions</p>
    </div>
    
    <!-- 03 Wedding & Festive -->
    <div onclick="selectCatalogue('Wedding & Festive', this)" class="catalogue-option group relative p-5 rounded-2xl border border-slate-200/60 bg-white/50 hover:bg-white hover:shadow-lg hover:border-sky-300 cursor-pointer transition-all duration-200">
      <div class="text-xs font-bold text-sky-600 mb-1 font-mono">03</div>
      <h4 class="text-lg font-semibold text-slate-800 mb-1">Wedding & Festive</h4>
      <p class="text-sm text-slate-500 font-medium leading-relaxed">Sherwanis, sarees, lehengas, suits and festivewear</p>
    </div>
    
    <!-- 04 Date Night -->
    <div onclick="selectCatalogue('Date Night', this)" class="catalogue-option group relative p-5 rounded-2xl border border-slate-200/60 bg-white/50 hover:bg-white hover:shadow-lg hover:border-sky-300 cursor-pointer transition-all duration-200">
      <div class="text-xs font-bold text-sky-600 mb-1 font-mono">04</div>
      <h4 class="text-lg font-semibold text-slate-800 mb-1">Date Night</h4>
      <p class="text-sm text-slate-500 font-medium leading-relaxed">Sophisticated evening outfits</p>
    </div>
    
    <!-- 05 Streetwear -->
    <div onclick="selectCatalogue('Streetwear', this)" class="catalogue-option group relative p-5 rounded-2xl border border-slate-200/60 bg-white/50 hover:bg-white hover:shadow-lg hover:border-sky-300 cursor-pointer transition-all duration-200">
      <div class="text-xs font-bold text-sky-600 mb-1 font-mono">05</div>
      <h4 class="text-lg font-semibold text-slate-800 mb-1">Streetwear</h4>
      <p class="text-sm text-slate-500 font-medium leading-relaxed">Modern urban and oversized styling</p>
    </div>
    
    <!-- 06 Couple Coordinated -->
    <div onclick="selectCatalogue('Couple Coordinated', this)" class="catalogue-option group relative p-5 rounded-2xl border border-slate-200/60 bg-white/50 hover:bg-white hover:shadow-lg hover:border-sky-300 cursor-pointer transition-all duration-200">
      <div class="text-xs font-bold text-sky-600 mb-1 font-mono">06</div>
      <h4 class="text-lg font-semibold text-slate-800 mb-1">Couple Coordinated</h4>
      <p class="text-sm text-slate-500 font-medium leading-relaxed">Complementary outfits for two people</p>
    </div>
  </div>
</div>
"""

# Insert HTML before </body>
if "id=\"catalogue-drawer\"" not in html:
    html = html.replace('</body>', catalogue_html + '\n</body>')

# 2. JS Logic
catalogue_js = """
<script>
window.dafitmatchState = window.dafitmatchState || {};

function openCataloguePanel() {
    const drawer = document.getElementById('catalogue-drawer');
    const backdrop = document.getElementById('catalogue-backdrop');
    if(drawer && backdrop) {
        drawer.classList.remove('translate-x-full');
        backdrop.classList.remove('opacity-0', 'invisible');
    }
}

function closeCataloguePanel() {
    const drawer = document.getElementById('catalogue-drawer');
    const backdrop = document.getElementById('catalogue-backdrop');
    if(drawer && backdrop) {
        drawer.classList.add('translate-x-full');
        backdrop.classList.add('opacity-0', 'invisible');
    }
}

function selectCatalogue(name, el) {
    // Visual highlight
    document.querySelectorAll('.catalogue-option').forEach(opt => {
        opt.classList.remove('border-sky-400', 'bg-sky-50', 'shadow-md');
        opt.classList.add('border-slate-200/60', 'bg-white/50');
    });
    el.classList.remove('border-slate-200/60', 'bg-white/50');
    el.classList.add('border-sky-400', 'bg-sky-50', 'shadow-md');
    
    // Store in state
    window.dafitmatchState.catalogue = name;
    
    // Update button text
    const catBtn = document.querySelector('.option-btn[data-id="clothing"]');
    if(catBtn) {
        catBtn.textContent = 'Catalogue → ' + name;
    }
    
    // Close panel with slight delay
    setTimeout(() => {
        closeCataloguePanel();
    }, 250);
}

document.addEventListener('DOMContentLoaded', () => {
    // Escape key listener
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeCataloguePanel();
        }
    });

    // Hook to the Catalogue button
    const catBtn = document.querySelector('.option-btn[data-id="clothing"]');
    if(catBtn) {
        catBtn.addEventListener('click', () => {
            openCataloguePanel();
        });
    }
});
</script>
"""

# Insert JS before </body>
if "function openCataloguePanel" not in html:
    html = html.replace('</body>', catalogue_js + '\n</body>')

with open('index.html', 'w') as f:
    f.write(html)

print("Catalogue logic injected!")
