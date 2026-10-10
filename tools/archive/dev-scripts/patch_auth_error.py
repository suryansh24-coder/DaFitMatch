import re

with open('auth.js', 'r') as f:
    js = f.read()

target = r"if \(\!clientId \|\| clientId === '' \|\| clientId\.includes\('YOUR_GOOGLE_CLIENT_ID_HERE'\)\) \{.*?return;\n    \}"

replacement = """if (!clientId || clientId === '' || clientId.includes('YOUR_GOOGLE_CLIENT_ID_HERE') || clientId.includes('YOUR_CLIENT_ID')) {
        document.getElementById('auth-error-message').textContent = 'Google Sign-In is not configured.';
        document.getElementById('auth-error-message').classList.remove('hidden');
        return;
    }"""

js = re.sub(target, replacement, js, flags=re.DOTALL)

with open('auth.js', 'w') as f:
    f.write(js)
