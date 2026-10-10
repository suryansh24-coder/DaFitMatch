import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Update the CSS block
css_target = r'\.apple-card:active \{\n.*?\}'
css_replacement = """.apple-card:active {
    transform: scale(0.98);
    transition: all 150ms cubic-bezier(0.16, 1, 0.3, 1);
}

.apple-card-active {
    background: rgba(255, 255, 255, 0.85) !important;
    border-color: rgba(14, 165, 233, 0.5) !important; /* sky-500 */
    box-shadow: 0 8px 24px rgba(14, 165, 233, 0.15) !important;
}"""
html = re.sub(css_target, css_replacement, html, flags=re.DOTALL)

# 2. Update selectCatalogue
select_target = r'document\.querySelectorAll\(\'\.catalogue-option\'\)\.forEach\(opt => \{\n\s*opt\.classList\.remove\(\'border-sky-400\', \'bg-sky-50\', \'shadow-md\'\);\n\s*opt\.classList\.add\(\'border-slate-200/60\', \'bg-white/50\'\);\n\s*\}\);\n\s*if\(el\) \{\n\s*el\.classList\.remove\(\'border-slate-200/60\', \'bg-white/50\'\);\n\s*el\.classList\.add\(\'border-sky-400\', \'bg-sky-50\', \'shadow-md\'\);\n\s*\}'
select_replacement = """document.querySelectorAll('.catalogue-option').forEach(opt => {
        opt.classList.remove('apple-card-active');
    });
    if(el) {
        el.classList.add('apple-card-active');
    }"""
html = re.sub(select_target, select_replacement, html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(html)
