import re

with open('index.html', 'r') as f:
    html = f.read()

# We need to find the entire playground-area div.
# Because it's large, we can use a regex that matches from <div id="playground-area" ... down to the end of the script or just the body end.
# Actually, the playground-area div is the last major element before </body> (except maybe the auth modal).
# Let's find where <div id="playground-area" starts and where <div id="auth-modal" starts.

start_str = '<div id="playground-area" class="stage w-full">'
end_str = '<!-- Auth Modal -->'

if start_str in html and end_str in html:
    start_idx = html.find(start_str)
    end_idx = html.find(end_str)
    
    new_app = '''<div id="playground-area" class="relative w-full h-screen overflow-hidden bg-slate-900">
        <!-- Mask overlay to blend with the transition section above -->
        <div class="absolute inset-0 pointer-events-none z-10" style="background: linear-gradient(to bottom, #a5c8e4 0%, transparent 15%);"></div>
        <img src="app-hero.jpg" alt="DaFitMatch Interactive Preview" class="w-full h-full object-cover object-center">
    </div>
    '''
    
    html = html[:start_idx] + new_app + html[end_idx:]
    
    with open('index.html', 'w') as f:
        f.write(html)
    print("Application replaced with static image!")
else:
    print("Could not find start or end bounds.")
