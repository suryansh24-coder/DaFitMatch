import re
import bs4

with open('index.html', 'r') as f:
    html = f.read()

soup = bs4.BeautifulSoup(html, 'html.parser')

# Move overlay to body in HTML string directly or via JS.
# The user asked for a JS execution:
# "After creating the overlay, execute: if (...) { document.body.appendChild(...) }"
# I can just put it right at the start of initCalibrationUI or just inside a DOMContentLoaded block.
move_overlay_js = """
window.addEventListener('DOMContentLoaded', () => {
    if (
      document.getElementById('dafitmatch-tryon-overlay') &&
      document.getElementById('dafitmatch-tryon-overlay').parentElement !== document.body
    ) {
      document.body.appendChild(
        document.getElementById('dafitmatch-tryon-overlay')
      );
    }
});
"""

# Let's find the script block containing `function hideALLOriginalCharacterRendering`
for script in soup.find_all('script'):
    if script.string and 'hideALLOriginalCharacterRendering' in script.string:
        content = script.string
        
        # We need to replace hideALLOriginalCharacterRendering, restoreALLOriginalCharacterRendering, stopALLOriginalVideos, and the setInterval
        
        target_funcs = re.compile(r'function hideALLOriginalCharacterRendering\(\).*?(?=\nfunction updateTryOnDiagnostics)', re.DOTALL)
        
        new_funcs = """
function hideALLOriginalCharacterRendering() {
  // Hide EVERY video except the try-on renderer.
  document.querySelectorAll('video').forEach(el => {
    if (
      el.id === 'dafitmatch-tryon-video' ||
      el.closest('#dafitmatch-tryon-overlay')
    ) return;

    try { el.pause(); } catch(e) {}

    el.style.setProperty('display', 'none', 'important');
    el.style.setProperty('visibility', 'hidden', 'important');
    el.style.setProperty('opacity', '0', 'important');
    el.style.setProperty('pointer-events', 'none', 'important');
  });

  // Hide original media containers GLOBALLY.
  document.querySelectorAll('.media').forEach(el => {
    if (
      el.id === 'dafitmatch-tryon-overlay' ||
      el.closest('#dafitmatch-tryon-overlay')
    ) return;

    el.style.setProperty('display', 'none', 'important');
    el.style.setProperty('visibility', 'hidden', 'important');
    el.style.setProperty('opacity', '0', 'important');
    el.style.setProperty('pointer-events', 'none', 'important');
  });

  // Hide any original elements explicitly named vid-*.
  document.querySelectorAll('[id^="vid-"]').forEach(el => {
    if (el.closest('#dafitmatch-tryon-overlay')) return;

    el.style.setProperty('display', 'none', 'important');
    el.style.setProperty('visibility', 'hidden', 'important');
    el.style.setProperty('opacity', '0', 'important');
    el.style.setProperty('pointer-events', 'none', 'important');
  });

  // Make absolutely sure the try-on overlay is visible.
  const overlay = document.getElementById('dafitmatch-tryon-overlay');
  if (overlay) {
    overlay.style.setProperty('display', 'block', 'important');
    overlay.style.setProperty('visibility', 'visible', 'important');
    overlay.style.setProperty('opacity', '1', 'important');
    overlay.style.setProperty('z-index', '9999999', 'important');
  }
}

function restoreALLOriginalCharacterRendering() {
  document.querySelectorAll('video').forEach(el => {
    if (
      el.id === 'dafitmatch-tryon-video' ||
      el.closest('#dafitmatch-tryon-overlay')
    ) return;

    el.style.removeProperty('display');
    el.style.removeProperty('visibility');
    el.style.removeProperty('opacity');
    el.style.removeProperty('pointer-events');
  });

  document.querySelectorAll('.media, [id^="vid-"]').forEach(el => {
    if (el.closest('#dafitmatch-tryon-overlay')) return;

    el.style.removeProperty('display');
    el.style.removeProperty('visibility');
    el.style.removeProperty('opacity');
    el.style.removeProperty('pointer-events');
  });
}

function stopALLOriginalVideos() {
  document.querySelectorAll('video').forEach(video => {
    if (
      video.id === 'dafitmatch-tryon-video' ||
      video.closest('#dafitmatch-tryon-overlay')
    ) return;

    try { video.pause(); } catch(e) {}
    video.muted = true;
  });
}

setInterval(() => {
  if (window.dafitmatchTryOnState !== 'TRY_ON_ACTIVE') return;

  document.querySelectorAll('video').forEach(video => {
    if (
      video.id === 'dafitmatch-tryon-video' ||
      video.closest('#dafitmatch-tryon-overlay')
    ) return;

    try { video.pause(); } catch(e) {}

    video.style.setProperty('display', 'none', 'important');
    video.style.setProperty('visibility', 'hidden', 'important');
    video.style.setProperty('opacity', '0', 'important');
  });

  document.querySelectorAll('.media, [id^="vid-"]').forEach(el => {
    if (el.closest('#dafitmatch-tryon-overlay')) return;

    el.style.setProperty('display', 'none', 'important');
    el.style.setProperty('visibility', 'hidden', 'important');
    el.style.setProperty('opacity', '0', 'important');
  });
}, 100);
"""
        content = re.sub(target_funcs, new_funcs + "\n", content)
        
        # Now remove any stopALLOriginalVideos inside updateTryOnDiagnostics or below if any
        # (It shouldn't be there, but just in case)
        
        # Inject move_overlay_js at the very top of the script
        content = move_overlay_js + content
        
        script.string.replace_with(content)

with open('index.html', 'w') as f:
    f.write(str(soup))
