const AuthState = {
  isAuthenticated: false,
  user: null,
  
  init() {
    const stored = localStorage.getItem('dafitmatch_session');
    if (stored) {
      try {
        const session = JSON.parse(stored);
        // Basic expiration check (JWT exp is in seconds)
        if (session.exp * 1000 > Date.now()) {
          this.isAuthenticated = true;
          this.user = session.user;
          this.updateUI();
          return;
        } else {
          this.signOut(true); // silent
        }
      } catch (e) {
        this.signOut(true);
      }
    }
  },

  signIn(jwtResponse) {
    try {
      // Decode JWT payload (base64url)
      const base64Url = jwtResponse.credential.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
          return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
      }).join(''));
      const payload = JSON.parse(jsonPayload);

      this.user = {
        sub: payload.sub,
        name: payload.name,
        email: payload.email,
        picture: payload.picture
      };
      this.isAuthenticated = true;
      
      localStorage.setItem('dafitmatch_session', JSON.stringify({
        user: this.user,
        exp: payload.exp
      }));

      this.updateUI();
      showToast(`Welcome to DaFitMatch, ${this.user.name.split(' ')[0]}`);
      closeAuthModal();
    } catch (e) {
      console.error("Auth decoding failed", e);
      document.getElementById('auth-error-message').textContent = 'We couldn\'t sign you in. Please try again.';
      document.getElementById('auth-error-message').classList.remove('hidden');
    }
  },

  signOut(silent = false) {
    this.isAuthenticated = false;
    this.user = null;
    localStorage.removeItem('dafitmatch_session');
    this.updateUI();
    if (!silent) {
        showToast('You have been signed out.');
    }
  },

  updateUI() {
    const signInBtn = document.getElementById('nav-signin-btn');
    const userProfile = document.getElementById('nav-user-profile');
    
    if (this.isAuthenticated) {
      if (signInBtn) signInBtn.classList.add('hidden');
      if (signInBtn) signInBtn.classList.remove('sm:inline-block');
      
      if (userProfile) {
        userProfile.classList.remove('hidden');
        userProfile.classList.add('flex');
        const img = userProfile.querySelector('img');
        const name = userProfile.querySelector('.user-name');
        if (img) img.src = this.user.picture;
        if (name) name.textContent = this.user.name.split(' ')[0];
      }
    } else {
      if (signInBtn) signInBtn.classList.remove('hidden');
      if (signInBtn) signInBtn.classList.add('sm:inline-block');
      
      if (userProfile) {
        userProfile.classList.add('hidden');
        userProfile.classList.remove('flex');
      }
    }
  }
};

function openAuthModal() {
  const modal = document.getElementById('auth-modal');
  const content = document.getElementById('auth-modal-content');
  if (!modal || !content) return;
  
  modal.classList.remove('opacity-0', 'invisible');
  content.classList.remove('scale-95');
  content.classList.add('scale-100');
  
  document.getElementById('auth-error-message').classList.add('hidden');
  
  // Render Google Button if not rendered yet
  if (!window.googleBtnRendered && window.google && window.google.accounts) {
    const clientId = window.ENV?.GOOGLE_CLIENT_ID;
    console.log('[DaFitMatch Auth] Google Client ID configured:', Boolean(clientId));
    
    // Clear error handling for missing/invalid client ID
    if (!clientId || clientId === '' || clientId.includes('YOUR_GOOGLE_CLIENT_ID_HERE') || clientId.includes('YOUR_CLIENT_ID')) {
        document.getElementById('auth-error-message').textContent = 'Google Sign-In is not configured.';
        document.getElementById('auth-error-message').classList.remove('hidden');
        return;
    }

    try {
      google.accounts.id.initialize({
        client_id: clientId,
        callback: (response) => AuthState.signIn(response),
        cancel_on_tap_outside: false
      });
      google.accounts.id.renderButton(
        document.getElementById('google-signin-button'),
        { theme: 'outline', size: 'large', type: 'standard', shape: 'pill', text: 'continue_with' }
      );
      window.googleBtnRendered = true;
    } catch (e) {
      console.error("GSI Error", e);
      document.getElementById('auth-error-message').textContent = 'Could not initialize Google Sign-In. Check Client ID.';
      document.getElementById('auth-error-message').classList.remove('hidden');
    }
  }
}

function closeAuthModal() {
  const modal = document.getElementById('auth-modal');
  const content = document.getElementById('auth-modal-content');
  if (!modal || !content) return;
  
  modal.classList.add('opacity-0', 'invisible');
  content.classList.remove('scale-100');
  content.classList.add('scale-95');
}

function showToast(message) {
  const toast = document.createElement('div');
  toast.className = 'fixed bottom-6 right-6 bg-slate-900/90 text-white px-4 py-3 rounded-2xl shadow-2xl backdrop-blur-md z-50 text-sm font-semibold tracking-wide flex items-center gap-3 transform translate-y-10 opacity-0 transition-all duration-300';
  toast.innerHTML = `<span class="w-2 h-2 rounded-full bg-emerald-400"></span> ${message}`;
  document.body.appendChild(toast);
  
  requestAnimationFrame(() => {
    toast.classList.remove('translate-y-10', 'opacity-0');
  });
  
  setTimeout(() => {
    toast.classList.add('translate-y-10', 'opacity-0');
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

document.addEventListener('DOMContentLoaded', () => {
  AuthState.init();
});
