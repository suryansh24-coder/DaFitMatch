import re

with open('auth.js', 'r') as f:
    js = f.read()

target = r'const clientId = \(typeof VITE_GOOGLE_CLIENT_ID !== \'undefined\' \? VITE_GOOGLE_CLIENT_ID : null\) \|\| window\.ENV\?\.GOOGLE_CLIENT_ID;'

replacement = """const clientId = window.ENV?.GOOGLE_CLIENT_ID;
    console.log('[DaFitMatch Auth] Google Client ID configured:', Boolean(clientId));"""

js = re.sub(target, replacement, js)

with open('auth.js', 'w') as f:
    f.write(js)
