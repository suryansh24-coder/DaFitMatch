import re

# Read the original app
with open('fit-check/index.html', 'r') as f:
    fit_html = f.read()

stage_start = fit_html.find('<div class="stage">')
original_app = fit_html[stage_start:]

# Modify it to match the state before replace_app.py
original_app = original_app.replace('<div class="stage">', '<div id="playground-area" class="stage w-full">')
original_app = original_app.replace('>Clothing</button>', '>Catalogue</button>')

# Remove the internal header
header_pattern = r'<header>.*?<span>DaFitMatch</span>.*?</header>'
original_app = re.sub(header_pattern, '', original_app, flags=re.DOTALL)

# Read the current index.html
with open('index.html', 'r') as f:
    index_html = f.read()

# Find the bad replaced app
bad_app_start = index_html.find('<div id="playground-area" class="relative w-full h-screen')
if bad_app_start == -1:
    print("Could not find the bad app to replace.")
    exit(1)

auth_start = index_html.find('<!-- Auth Modal -->')
if auth_start == -1:
    print("Could not find the auth modal.")
    exit(1)

# Replace the bad app with the rebuilt original app
new_index = index_html[:bad_app_start] + original_app + "\n" + index_html[auth_start:]

with open('index.html', 'w') as f:
    f.write(new_index)

print("App restored successfully!")
