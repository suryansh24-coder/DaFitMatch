import re

with open('index.html', 'r') as f:
    html = f.read()

modal_html = """
<!-- Auth Modal -->
<div id="auth-modal" class="fixed inset-0 z-[9999] bg-slate-900/40 backdrop-blur-sm opacity-0 invisible transition-all duration-300 flex items-center justify-center p-4" onclick="if(event.target === this) closeAuthModal()">
    <div id="auth-modal-content" class="bg-white/95 backdrop-blur-xl w-full max-w-md rounded-[24px] shadow-2xl p-8 relative scale-95 transition-transform duration-300 border border-white/50">
        
        <!-- Close Button -->
        <button onclick="closeAuthModal()" class="absolute top-6 right-6 text-slate-400 hover:text-slate-900 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12"></path></svg>
        </button>

        <!-- Header -->
        <div class="text-center mb-8">
            <h2 class="text-2xl font-extrabold text-slate-900 tracking-tight mb-2">Welcome back</h2>
            <p class="text-sm text-slate-500 font-medium">Enter your details to access DaFitMatch.</p>
        </div>

        <div id="auth-error-message" class="hidden mb-4 p-3 rounded-xl bg-red-50 text-red-600 text-sm font-semibold text-center border border-red-100"></div>

        <!-- Form -->
        <form onsubmit="handleEmailSignIn(event)" class="space-y-4">
            <div>
                <label class="block text-xs font-bold text-slate-600 uppercase tracking-wider mb-1.5">Email</label>
                <input type="email" required class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-sky-500 focus:border-sky-500 outline-none transition-all text-slate-900 font-medium placeholder-slate-400" placeholder="you@example.com">
            </div>
            <div>
                <label class="block text-xs font-bold text-slate-600 uppercase tracking-wider mb-1.5">Password</label>
                <input type="password" required class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-sky-500 focus:border-sky-500 outline-none transition-all text-slate-900 font-medium placeholder-slate-400" placeholder="••••••••">
            </div>
            
            <button type="submit" class="w-full py-3.5 bg-slate-900 text-white rounded-xl font-bold hover:bg-slate-800 transition-colors shadow-md mt-2 flex items-center justify-center gap-2">
                Sign In
            </button>
        </form>

        <div class="relative my-6 flex items-center justify-center">
            <div class="absolute inset-0 flex items-center"><div class="w-full border-t border-slate-200"></div></div>
            <span class="relative bg-white px-4 text-xs font-bold text-slate-400 uppercase tracking-wider">Or</span>
        </div>

        <!-- Google OAuth -->
        <div class="flex justify-center">
            <div id="google-signin-button"></div>
        </div>

        <!-- Missing Client ID warning -->
        <div id="google-config-warning" class="hidden mt-3 text-[10px] text-amber-600 text-center font-medium bg-amber-50 p-2 rounded-lg border border-amber-100">
            Google Sign-In is not fully configured.<br>
            Please set <code class="font-bold">GOOGLE_CLIENT_ID</code> in <code class="font-bold">config.js</code>.
        </div>

        <p class="text-center mt-8 text-sm text-slate-500 font-medium">
            Don't have an account? <a href="#" class="text-sky-600 hover:text-sky-700 font-bold">Create account</a>
        </p>
    </div>
</div>

<script>
function handleEmailSignIn(e) {
    e.preventDefault();
    const errorEl = document.getElementById('auth-error-message');
    errorEl.textContent = 'Authentication backend not configured.';
    errorEl.classList.remove('hidden');
}

// Escape key to close
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeAuthModal();
    }
});

// Intercept modal open to check Google configuration
const originalOpenAuthModal = window.openAuthModal;
if (originalOpenAuthModal) {
    window.openAuthModal = function() {
        document.body.style.overflow = 'hidden'; // Prevent scrolling
        originalOpenAuthModal();
        
        // Show warning if dummy client ID is used
        if (window.ENV && window.ENV.GOOGLE_CLIENT_ID && window.ENV.GOOGLE_CLIENT_ID.includes('YOUR_GOOGLE_CLIENT_ID_HERE')) {
            document.getElementById('google-config-warning').classList.remove('hidden');
        }
    };
}

const originalCloseAuthModal = window.closeAuthModal;
if (originalCloseAuthModal) {
    window.closeAuthModal = function() {
        document.body.style.overflow = ''; // Restore scrolling
        originalCloseAuthModal();
    };
}
</script>
"""

html = html.replace('</body>', modal_html + '\n</body>')

with open('index.html', 'w') as f:
    f.write(html)
