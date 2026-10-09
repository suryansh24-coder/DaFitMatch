import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Update the drawer CSS classes and inject the reflection element
drawer_pattern = r'<div class="fixed inset-y-0 right-0 w-full sm:w-\[380px\] md:w-\[440px\].*?id="catalogue-drawer">'

new_drawer = """
<style>
/* PREMIUM APPLE-STYLE ANIMATIONS & EFFECTS */
.apple-drawer {
    background: rgba(255, 255, 255, 0.72);
    backdrop-filter: blur(30px) saturate(140%);
    -webkit-backdrop-filter: blur(30px) saturate(140%);
    border-left: 1px solid rgba(255, 255, 255, 0.65);
    box-shadow: -10px 0 40px -10px rgba(0, 0, 0, 0.1);
    transition: transform 600ms cubic-bezier(0.16, 1, 0.3, 1);
    overflow: hidden; /* For reflections */
}

/* Glass Reflection */
.glass-reflection {
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(135deg, rgba(255,255,255,0) 30%, rgba(255,255,255,0.15) 50%, rgba(255,255,255,0) 70%);
    pointer-events: none;
    z-index: 10;
    animation: glassSheen 10s ease-in-out infinite;
}

@keyframes glassSheen {
    0% { transform: translate(-30%, -30%); opacity: 0; }
    50% { opacity: 1; }
    100% { transform: translate(30%, 30%); opacity: 0; }
}

/* Mouse Light Effect */
.mouse-light {
    position: absolute;
    width: 400px;
    height: 400px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0) 70%);
    pointer-events: none;
    z-index: 0;
    transform: translate(-50%, -50%);
    opacity: 0;
    transition: opacity 300ms ease;
    will-change: transform;
}

/* Premium Card Interactions */
.apple-card {
    background: rgba(255, 255, 255, 0.5);
    border: 1px solid rgba(255, 255, 255, 0.4);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
    transition: all 400ms cubic-bezier(0.16, 1, 0.3, 1);
    position: relative;
    z-index: 1;
    overflow: hidden;
    opacity: 0;
    transform: translateY(14px) scale(0.98);
}

.apple-card::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(180deg, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0) 100%);
    opacity: 0;
    transition: opacity 400ms ease;
    pointer-events: none;
}

.apple-card:hover {
    transform: translateY(-3px) scale(1.015);
    background: rgba(255, 255, 255, 0.7);
    border-color: rgba(255, 255, 255, 0.8);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.06);
}

.apple-card:hover::after {
    opacity: 1;
}

.apple-card:active {
    transform: scale(0.98);
    transition: all 150ms cubic-bezier(0.16, 1, 0.3, 1);
}

/* Stagger Animation Trigger */
.drawer-open .apple-card {
    opacity: 1;
    transform: translateY(0) scale(1);
}

.drawer-open .apple-header-anim {
    opacity: 1;
    transform: translateY(0);
}

.apple-header-anim {
    opacity: 0;
    transform: translateY(-8px);
    transition: all 500ms cubic-bezier(0.16, 1, 0.3, 1) 100ms;
}

.apple-close-btn {
    transition: all 300ms ease;
}
.apple-close-btn:hover {
    transform: scale(1.1) rotate(90deg);
}

/* Backdrop */
.apple-backdrop {
    background: rgba(10, 20, 40, 0.15);
    backdrop-filter: blur(4px);
    -webkit-backdrop-filter: blur(4px);
    transition: all 500ms ease;
}

@media (prefers-reduced-motion: reduce) {
    .glass-reflection { display: none; }
    .apple-drawer, .apple-card, .apple-header-anim { transition: opacity 300ms ease; transform: none !important; }
}
</style>
<div class="fixed inset-y-0 right-0 w-full sm:w-[380px] md:w-[440px] z-[200] transform translate-x-full flex flex-col apple-drawer" id="catalogue-drawer">
    <div class="glass-reflection"></div>
    <div class="mouse-light" id="catalogue-light"></div>
"""

html = re.sub(drawer_pattern, new_drawer, html, count=1)

# 2. Update Backdrop
backdrop_pattern = r'<div class="fixed inset-0 bg-slate-900/10 backdrop-blur-\[2px\] z-\[190\] opacity-0 invisible transition-all duration-300 cursor-pointer" id="catalogue-backdrop" onclick="closeCataloguePanel\(\)"></div>'
new_backdrop = r'<div class="fixed inset-0 z-[190] opacity-0 invisible cursor-pointer apple-backdrop" id="catalogue-backdrop" onclick="closeCataloguePanel()"></div>'
html = re.sub(backdrop_pattern, new_backdrop, html)

# 3. Update Header
header_pattern = r'<!-- Header -->\s*<div class="px-8 py-6 border-b border-slate-200/50 flex items-center justify-between bg-white/40">\s*<div>\s*<h2 class="text-xs font-bold tracking-widest text-slate-400 uppercase mb-1">Catalogue</h2>\s*<h3 class="text-xl font-semibold text-slate-800">Choose your style direction</h3>\s*</div>\s*<button class="text-slate-400 hover:text-slate-600 transition-colors" onclick="closeCataloguePanel\(\)">\s*<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">\s*<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>\s*</svg>\s*</button>\s*</div>'

new_header = """<!-- Header -->
<div class="px-8 py-6 border-b border-white/40 flex items-center justify-between relative z-10 apple-header-anim">
<div>
<h2 class="text-xs font-bold tracking-widest text-slate-500 uppercase mb-1">Catalogue</h2>
<h3 class="text-xl font-semibold text-slate-800">Choose your style direction</h3>
</div>
<button class="text-slate-400 hover:text-slate-800 apple-close-btn relative z-20" onclick="closeCataloguePanel()">
<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
</svg>
</button>
</div>"""
html = re.sub(header_pattern, new_header, html)


# 4. Update existing cards in the hardcoded HTML list
def replace_card(m):
    # m.group(0) is the full div class="..."
    inner = m.group(0)
    inner = re.sub(r'catalogue-option group relative p-5 rounded-2xl border border-slate-200/60 bg-white/50 hover:bg-white hover:shadow-lg hover:border-sky-300 cursor-pointer transition-all duration-200', 'catalogue-option cursor-pointer apple-card p-5 rounded-2xl', inner)
    return inner

html = re.sub(r'<div class="catalogue-option .*?cursor-pointer.*?"', replace_card, html)

with open('index.html', 'w') as f:
    f.write(html)
