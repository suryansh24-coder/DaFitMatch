import re
import os

# Read code1.html
with open('code1.html', 'r') as f:
    code_html = f.read()

# Read pristine fit-check/index.html
with open('fit-check/index.html', 'r') as f:
    fit_check_html = f.read()

# 1. Apply UI changes to pristine app (DaFitMatch instead of The Fit Check, remove Try Now)
target_header = """    <header>
      <div class="meta" style="margin-left: 0; font-size: 36px; font-weight: 700; letter-spacing: -0.06em; text-transform: uppercase; display: flex; align-items: center;">
        <span>The Fit Check</span>
      </div>
      <div></div>
      <a href="https://app.ltx.io/" target="_blank" rel="noopener noreferrer" class="try-btn">Try now</a>
    </header>"""
replacement_header = """    <header>
      <div class="meta" style="margin-left: 0; font-size: 36px; font-weight: 700; letter-spacing: -0.06em; display: flex; align-items: center;">
        <span>DaFitMatch</span>
      </div>
    </header>"""
fit_check_html = fit_check_html.replace(target_header, replacement_header)

# 2. Extract CSS from fit-check
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

# 3. Extract HTML/JS from fit-check
html_match = re.search(r'(<div class="stage">.*)</body>', fit_check_html, re.DOTALL)
if html_match:
    original_body = html_match.group(1)
    original_body = original_body.replace('<div class="stage">', '<div id="playground-area" class="stage w-full">')
else:
    original_body = "<!-- ERROR EXTRACTING EXISTING APP -->"

# 4. Inject CSS into code1.html <head>
code_html = code_html.replace('</head>', f'{wrapped_css}</head>')

# 5. Replace placeholder in code1.html
# The placeholder is: <div class="w-full mt-12 p-8 ... id="replace-me-with-app"> ... </div>\n</div>\n</section>
placeholder_pattern = r'<div class="w-full mt-12[^>]*id="replace-me-with-app"[^>]*>.*?</div>\s*</div>\s*</section>'
replacement_body = f'</div>\n</section>\n{original_body}'
code_html = re.sub(placeholder_pattern, replacement_body, code_html, flags=re.DOTALL)

# 6. Apply Absolute Centered Navbar Fix
new_header = """<!-- BEGIN: SiteHeader -->
<header class="fixed top-0 left-0 w-full z-50 transition-all duration-300 h-20 md:h-24 pointer-events-none">
  <!-- Zone 1: LEFT -->
  <div class="absolute left-6 md:left-12 lg:left-16 top-1/2 -translate-y-1/2 pointer-events-auto">
    <a class="flex items-center gap-2 group" data-purpose="brand-logo" href="#">
      <span class="text-2xl font-bold tracking-tight text-white drop-shadow-sm flex items-center gap-1.5">
        DaFitMatch
        <span class="inline-block w-2.5 h-2.5 rotate-45 bg-white shadow-[0_0_12px_rgba(255,255,255,0.9)] rounded-sm group-hover:rotate-90 transition-transform duration-500"></span>
      </span>
    </a>
  </div>

  <!-- Zone 2: CENTER -->
  <div class="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 pointer-events-auto hidden lg:block w-max">
    <nav class="flex items-center gap-1 glass-pill-bar p-1.5 rounded-full relative shadow-sm" data-purpose="main-nav" id="main-nav-bar">
      <!-- Sliding Glossy Apple-style Indicator Pill -->
      <div aria-hidden="true" class="nav-indicator-pill opacity-0" id="nav-indicator">
        <div class="glossy-shimmer-sweep"></div>
      </div>
      <a class="nav-link relative z-10 px-4 py-1.5 rounded-full text-sm font-semibold tracking-tight transition-all duration-200 group flex items-center gap-1.5 active-nav" href="#hero">
        <svg class="w-3.5 h-3.5 text-white/90 drop-shadow-sm transition-transform duration-200 group-hover:scale-110" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" stroke-linecap="round" stroke-linejoin="round"></path></svg>
        <span class="inline-block drop-shadow-sm text-white" style="background: linear-gradient(180deg, #FFFFFF 0%, rgba(255, 255, 255, 0.9) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; filter: drop-shadow(0 1px 2px rgba(0,0,0,0.18)); letter-spacing: -0.01em;">Home</span>
      </a>
      <a class="nav-link relative z-10 px-4 py-1.5 rounded-full text-sm font-medium tracking-tight text-white/85 hover:text-white transition-all duration-200 group flex items-center gap-1.5" href="#how-it-works">
        <svg class="w-3.5 h-3.5 text-white/80 drop-shadow-sm transition-transform duration-200 group-hover:scale-110" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M13 10V3L4 14h7v7l9-11h-7z" stroke-linecap="round" stroke-linejoin="round"></path></svg>
        <span class="inline-block transition-all duration-200 group-hover:drop-shadow-sm" style="background: linear-gradient(180deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.72) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; filter: drop-shadow(0 1px 1px rgba(0,0,0,0.12)); letter-spacing: -0.01em;">How It Works</span>
      </a>
      <a class="nav-link relative z-10 px-4 py-1.5 rounded-full text-sm font-medium tracking-tight text-white/85 hover:text-white transition-all duration-200 group flex items-center gap-1.5" href="#solo-styling">
        <svg class="w-3.5 h-3.5 text-white/80 drop-shadow-sm transition-transform duration-200 group-hover:scale-110" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" stroke-linecap="round" stroke-linejoin="round"></path></svg>
        <span class="inline-block transition-all duration-200 group-hover:drop-shadow-sm" style="background: linear-gradient(180deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.72) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; filter: drop-shadow(0 1px 1px rgba(0,0,0,0.12)); letter-spacing: -0.01em;">For Me</span>
      </a>
      <a class="nav-link relative z-10 px-4 py-1.5 rounded-full text-sm font-medium tracking-tight text-white/85 hover:text-white transition-all duration-200 group flex items-center gap-1.5" href="#couple-harmony">
        <svg class="w-3.5 h-3.5 text-white/80 drop-shadow-sm transition-transform duration-200 group-hover:scale-110" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" stroke-linecap="round" stroke-linejoin="round"></path></svg>
        <span class="inline-block transition-all duration-200 group-hover:drop-shadow-sm" style="background: linear-gradient(180deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.72) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; filter: drop-shadow(0 1px 1px rgba(0,0,0,0.12)); letter-spacing: -0.01em;">For Couples</span>
      </a>
      <a class="nav-link relative z-10 px-4 py-1.5 rounded-full text-sm font-medium tracking-tight text-white/85 hover:text-white transition-all duration-200 group flex items-center gap-1.5" href="#features">
        <svg class="w-3.5 h-3.5 text-white/80 drop-shadow-sm transition-transform duration-200 group-hover:scale-110" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" stroke-linecap="round" stroke-linejoin="round"></path></svg>
        <span class="inline-block transition-all duration-200 group-hover:drop-shadow-sm" style="background: linear-gradient(180deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.72) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; filter: drop-shadow(0 1px 1px rgba(0,0,0,0.12)); letter-spacing: -0.01em;">Features</span>
      </a>
    </nav>
  </div>

  <!-- Zone 3: RIGHT -->
  <div class="absolute right-6 md:right-12 lg:right-16 top-1/2 -translate-y-1/2 pointer-events-auto flex items-center gap-4">
    <a class="text-sm font-medium text-white/90 hover:text-white transition-colors duration-150 hidden sm:inline-block" href="#signin">
      Sign In
    </a>
    <a class="px-6 py-2 rounded-full text-sm font-semibold tracking-wide text-white border border-white/60 bg-white/20 hover:bg-white hover:text-slate-900 transition-all duration-300 backdrop-blur-md shadow-lg hover:shadow-xl hover:scale-105 active:scale-95" href="#playground-area">
      Find My Fit
    </a>
  </div>
</header>
<!-- END: SiteHeader -->"""
code_html = re.sub(r'<!-- BEGIN: SiteHeader -->.*?<!-- END: SiteHeader -->', new_header, code_html, flags=re.DOTALL)

# Also fix the Features link
code_html = code_html.replace('href="#features"', 'href="#how-it-works"')

# Also update the href for "Find My Fit" throughout to be #playground-area just in case
code_html = code_html.replace('href="#playground"', 'href="#playground-area"')

# Write the final result
with open('index.html', 'w') as f:
    f.write(code_html)

print("Merge completed!")
