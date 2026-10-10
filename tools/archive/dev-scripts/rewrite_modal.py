import re

with open('index.html', 'r') as f:
    html = f.read()

# Replace the entire modal
modal_target = r'<!-- Auth Modal -->.*?</div>\n</div>\n\n<script>'

new_modal = """<!-- Auth Modal -->
<div id="auth-modal" class="fixed inset-0 z-[9999] bg-slate-900/40 backdrop-blur-sm opacity-0 invisible transition-all duration-300 flex items-center justify-center p-4" onclick="if(event.target === this) closeAuthModal()">
    <div id="auth-modal-content" class="bg-white/95 backdrop-blur-xl w-full max-w-sm rounded-[24px] shadow-2xl p-8 relative scale-95 transition-transform duration-300 border border-white/50 text-center">
        
        <!-- Close Button -->
        <button onclick="closeAuthModal()" class="absolute top-6 right-6 text-slate-400 hover:text-slate-900 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12"></path></svg>
        </button>

        <!-- Header -->
        <div class="mb-8 mt-2">
            <h1 class="text-xl font-black tracking-tight text-slate-900 uppercase mb-4">DaFitMatch</h1>
            <h2 class="text-2xl font-extrabold text-slate-900 tracking-tight mb-2">Welcome to DaFitMatch</h2>
        </div>

        <div id="auth-error-message" class="hidden mb-6 p-3 rounded-xl bg-red-50 text-red-600 text-sm font-semibold text-center border border-red-100"></div>

        <!-- Google OAuth -->
        <div class="flex justify-center mb-6">
            <div id="google-signin-button"></div>
        </div>

        <p class="text-sm text-slate-500 font-medium">
            Sign in securely with your Google account
        </p>
    </div>
</div>

<script>"""

html = re.sub(modal_target, new_modal, html, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(html)
