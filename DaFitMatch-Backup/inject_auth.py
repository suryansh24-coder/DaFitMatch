import re

with open('index.html', 'r') as f:
    html = f.read()

# 1. Inject scripts into head
scripts_to_inject = """
<!-- Google Identity Services & Auth -->
<script src="https://accounts.google.com/gsi/client" async defer></script>
<script src="config.js"></script>
<script src="auth.js"></script>
"""
if "auth.js" not in html:
    html = html.replace('</head>', scripts_to_inject + '</head>')

# 2. Replace Sign In button and add Profile dropdown
old_signin = r'<a class="text-sm font-medium text-white/90 hover:text-white transition-colors duration-150 hidden sm:inline-block" href="#signin">\s*Sign In\s*</a>'
new_signin = """<!-- Auth Controls -->
    <a id="nav-signin-btn" class="text-sm font-medium text-white/90 hover:text-white transition-colors duration-150 hidden sm:inline-block cursor-pointer" onclick="openAuthModal()">
      Sign In
    </a>
    <div id="nav-user-profile" class="hidden items-center gap-2 relative group cursor-pointer">
      <img src="" alt="Profile" class="w-8 h-8 rounded-full border border-white/40 shadow-sm object-cover">
      <span class="text-sm font-medium text-white/90 user-name hidden md:inline-block"></span>
      <!-- Dropdown -->
      <div class="absolute top-full right-0 mt-2 w-48 bg-white/90 backdrop-blur-xl border border-slate-200/50 rounded-2xl shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 overflow-hidden transform origin-top-right scale-95 group-hover:scale-100 z-50">
        <div class="p-2">
          <div class="px-3 py-2 text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1">Account</div>
          <a href="#" class="block px-3 py-2 text-sm text-slate-700 hover:bg-slate-100/80 rounded-xl transition-colors font-medium">Profile</a>
          <a href="#" class="block px-3 py-2 text-sm text-slate-700 hover:bg-slate-100/80 rounded-xl transition-colors font-medium">Saved Outfits</a>
          <div class="h-px w-full bg-slate-200/50 my-1"></div>
          <a href="#" onclick="AuthState.signOut(); return false;" class="block px-3 py-2 text-sm text-red-600 hover:bg-red-50 rounded-xl transition-colors font-medium">Sign Out</a>
        </div>
      </div>
    </div>"""

html = re.sub(old_signin, new_signin, html)

# 3. Inject Auth Modal before closing body
auth_modal = """
<!-- Auth Modal -->
<div id="auth-modal" class="fixed inset-0 z-[100] flex items-center justify-center opacity-0 invisible transition-all duration-300">
  <div class="absolute inset-0 bg-slate-900/40 backdrop-blur-sm cursor-pointer" onclick="closeAuthModal()"></div>
  <div class="relative bg-white/90 backdrop-blur-xl border border-slate-200/50 rounded-3xl shadow-2xl p-8 max-w-sm w-full mx-4 transform scale-95 transition-transform duration-300" id="auth-modal-content">
    <button onclick="closeAuthModal()" class="absolute top-4 right-4 text-slate-400 hover:text-slate-600 transition-colors">
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M6 18L18 6M6 6l12 12" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
    </button>
    <div class="text-center mb-6">
      <div class="w-12 h-12 bg-sky-100 text-sky-600 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-inner border border-sky-200/50">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path></svg>
      </div>
      <h3 class="text-xl font-bold text-slate-900 tracking-tight">Welcome to DaFitMatch</h3>
      <p class="text-sm text-slate-500 mt-2 font-medium">Sign in to save your style profile, outfits and wardrobe.</p>
    </div>
    
    <div class="flex justify-center mt-6 min-h-[44px]">
      <div id="google-signin-button"></div>
    </div>
    
    <div id="auth-error-message" class="mt-4 text-xs font-semibold text-red-500 text-center hidden"></div>
  </div>
</div>
"""
if "id=\"auth-modal\"" not in html:
    html = html.replace('</body>', auth_modal + '</body>')

with open('index.html', 'w') as f:
    f.write(html)

print("HTML modified for auth!")
