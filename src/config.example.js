/*
 * DaFitMatch — Example environment configuration
 * -------------------------------------------------------------------------
 * Copy this file to `src/config.js` and fill in real values. `src/config.js`
 * is git-ignored so secrets and environment-specific IDs are never committed.
 *
 *   cp src/config.example.js src/config.js
 */

window.ENV = Object.freeze({
  /* Google OAuth Web client ID.
   * Authorised JavaScript origins must include the host serving the app,
   * e.g. http://localhost:8000 and the deployed domain. */
  GOOGLE_CLIENT_ID: 'YOUR_GOOGLE_CLIENT_ID_HERE.apps.googleusercontent.com',

  APP_NAME: 'DaFitMatch',

  /* Storage namespace for persisted onboarding / aesthetic profiles. */
  STORAGE_NAMESPACE: 'dafitmatch_profiles_v1',

  /* Development/demo flag. When true, unavailable AI or product services must
   * be surfaced as "demo mode", never as a successful live call. */
  DEMO_MODE: true,

  /* --- AI Fit Studio / try-on -------------------------------------------
   * Pick ONE provider (leave both unset for clearly-labelled demo mode):
   *
   * 1) Hugging Face (free) — recommended, no backend required.
   *      TRY_ON_PROVIDER  = 'huggingface'
   *      TRY_ON_HF_TOKEN  = free token from
   *        https://huggingface.co/settings/tokens (read access is enough).
   *      TRY_ON_HF_SPACE  = the IDM-VTON Space to call (default below).
   *
   * 2) Your own endpoint — an HTTPS URL you control that accepts a
   *    multipart/form-data POST (image, outfit_id, prompt) and returns JSON
   *    { image: "<url>" } or an image blob. Set TRY_ON_ENDPOINT for this.
   */
  TRY_ON_PROVIDER: 'huggingface',
  TRY_ON_HF_TOKEN: '',
  TRY_ON_HF_SPACE: 'yisol/IDM-VTON',

  TRY_ON_ENDPOINT: '',
  TRY_ON_MAX_BYTES: 5 * 1024 * 1024
});
