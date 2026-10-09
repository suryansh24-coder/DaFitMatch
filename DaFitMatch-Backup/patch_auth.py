import re

with open('auth.js', 'r') as f:
    js = f.read()

target = r'if \(!window\.googleBtnRendered && window\.google && window\.google\.accounts\) \{\n\s*try \{\n\s*google\.accounts\.id\.initialize\(\{\n\s*client_id: window\.ENV\.GOOGLE_CLIENT_ID,'

replacement = """if (!window.googleBtnRendered && window.google && window.google.accounts) {
    const clientId = window.ENV?.GOOGLE_CLIENT_ID;
    
    // Clear error handling for missing/invalid client ID
    if (!clientId || clientId === '' || clientId.includes('YOUR_GOOGLE_CLIENT_ID_HERE')) {
        document.getElementById('auth-error-message').textContent = 'Google Sign-In is not configured yet.';
        document.getElementById('auth-error-message').classList.remove('hidden');
        return;
    }

    try {
      google.accounts.id.initialize({
        client_id: clientId,"""

js = re.sub(target, replacement, js)

with open('auth.js', 'w') as f:
    f.write(js)
