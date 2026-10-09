import re
import os

with open('code.html', 'r') as f:
    code_html = f.read()

with open('fit-check/index.html', 'r') as f:
    fit_check_html = f.read()

# 1. Extract CSS from fit-check
css_match = re.search(r'<style>(.*?)</style>', fit_check_html, re.DOTALL)
if css_match:
    original_css = css_match.group(1)
    
    # Prefix global selectors
    original_css = original_css.replace('\n    h1 {', '\n    .stage h1 {')
    original_css = original_css.replace('\n    p {', '\n    .stage p {')
    original_css = original_css.replace('\n    button {', '\n    .stage button {')
    
    original_css = original_css.replace('\n      h1 {', '\n      .stage h1 {')
    original_css = original_css.replace('\n      p {', '\n      .stage p {')
    
    wrapped_css = f"\n<style data-purpose=\"existing-app-styles\">\n{original_css}\n</style>\n"
else:
    wrapped_css = ""

# 2. Extract HTML/JS from fit-check
html_match = re.search(r'(<div class="stage">.*)</body>', fit_check_html, re.DOTALL)
if html_match:
    original_body = html_match.group(1)
    original_body = original_body.replace('<div class="stage">', '<div id="playground-area" class="stage w-full">')
else:
    original_body = "<!-- ERROR EXTRACTING EXISTING APP -->"

# 3. Inject CSS into code.html <head>
code_html = code_html.replace('</head>', f'{wrapped_css}</head>')

# 4. Inject Body into code.html
# Replace <div id="replace-me-with-app"></div>\n</div>\n</section>
# with </div>\n</section>\n{original_body}
target = '<div id="replace-me-with-app"></div>\n</div>\n</section>'
replacement = f'</div>\n</section>\n{original_body}'

if target in code_html:
    code_html = code_html.replace(target, replacement)
else:
    # Try regex fallback if whitespace is different
    code_html = re.sub(r'<div id="replace-me-with-app"></div>\s*</div>\s*</section>', replacement, code_html)

with open('index.html', 'w') as f:
    f.write(code_html)

