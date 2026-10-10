import re

with open('index.html', 'r') as f:
    html = f.read()

# I will replace everything between `<script>` and `function updateTryOnDiagnostics`
# Wait, let's locate `function setOriginalAnimationActive(active) { ... }` up to `function updateTryOnDiagnostics`
# First, let's find the script block.

# The safest way is to use regex to find the start of the Javascript section
# and replace the relevant parts. Let's just grab the whole script tag if possible.
# I'll use BeautifulSoup to find the script containing `window.dafitmatchTryOnState`.

import bs4
soup = bs4.BeautifulSoup(html, 'html.parser')
for script in soup.find_all('script'):
    if script.string and 'dafitmatchTryOnState' in script.string:
        content = script.string
        
        # We replace the old controller functions
        target_funcs = re.compile(r'window\.dafitmatchTryOnState.*?(?=function updateTryOnDiagnostics)', re.DOTALL)
        
        new_funcs = """
window.dafitmatchTryOnState = 'NORMAL';

function hideALLOriginalCharacterRendering() {
  const selectors = [
    '#playground-area video[id^="vid-"]',
    '#playground-area .media',
    '#playground-area video.media',
    '#playground-area canvas'
  ];

  document.querySelectorAll(selectors.join(',')).forEach(el => {
    // NEVER hide the try-on renderer
    if (
      el.id === 'dafitmatch-tryon-video' ||
      el.id === 'dafitmatch-tryon-image' ||
      el.closest('#dafitmatch-tryon-overlay')
    ) return;

    if (el.tagName === 'VIDEO') {
      el.pause();
      el.currentTime = el.currentTime;
    }

    el.style.setProperty('display', 'none', 'important');
    el.style.setProperty('visibility', 'hidden', 'important');
    el.style.setProperty('opacity', '0', 'important');
    el.style.setProperty('pointer-events', 'none', 'important');
  });
}

function restoreALLOriginalCharacterRendering() {
  const selectors = [
    '#playground-area video[id^="vid-"]',
    '#playground-area .media',
    '#playground-area video.media',
    '#playground-area canvas'
  ];

  document.querySelectorAll(selectors.join(',')).forEach(el => {
    if (
      el.id === 'dafitmatch-tryon-video' ||
      el.id === 'dafitmatch-tryon-image' ||
      el.closest('#dafitmatch-tryon-overlay')
    ) return;
    
    // Clear our !important overrides
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

    video.pause();
    video.muted = true;
  });
}

// Watchdog
setInterval(() => {
  if (window.dafitmatchTryOnState !== 'TRY_ON_ACTIVE') return;

  stopALLOriginalVideos();
  hideALLOriginalCharacterRendering();

  const overlay = document.getElementById('dafitmatch-tryon-overlay');

  if (overlay) {
    overlay.style.setProperty('display', 'block', 'important');
    overlay.style.setProperty('visibility', 'visible', 'important');
    overlay.style.setProperty('opacity', '1', 'important');
    overlay.style.setProperty('z-index', '999999', 'important');
  }
}, 100);

"""
        
        content = re.sub(target_funcs, new_funcs, content)
        
        # Replace deactivateTryOnLayer and activateTryOnLayer and normalFallback
        content = content.replace("setOriginalAnimationActive(true)", "restoreALLOriginalCharacterRendering()")
        content = content.replace("setOriginalAnimationActive(false)", "stopALLOriginalVideos();\n                hideALLOriginalCharacterRendering();")
        
        # Add exact requested logs
        log_view_look = r'console\.log\("\[DaFitMatch\] VIEW LOOK CLICKED", "outfitId:", outfitId\);'
        new_log_view_look = "console.log('[DaFitMatch FINAL] VIEW LOOK CLICKED', outfitId);"
        content = re.sub(log_view_look, new_log_view_look, content)
        
        # "When try-on asset is ready:" -> after bounding client rect succeeds
        content = content.replace("const success = await activateTryOnLayer(false);", "console.log('[DaFitMatch FINAL] TRY-ON ASSET READY');\n                const success = await activateTryOnLayer(false);")
        content = content.replace("const success = await activateTryOnLayer(true);", "console.log('[DaFitMatch FINAL] TRY-ON ASSET READY');\n                const success = await activateTryOnLayer(true);")
        
        # "When original layers are hidden" -> inside activateTryOnLayer, after hideALLOriginalCharacterRendering
        log_hidden = """
            if (desiredOpacity >= 1.0) {
                stopALLOriginalVideos();
                hideALLOriginalCharacterRendering();
                
                console.log(
                  '[DaFitMatch FINAL] ORIGINAL LAYERS HIDDEN',
                  Array.from(document.querySelectorAll('#playground-area video')).map(v => ({
                    id: v.id,
                    paused: v.paused,
                    display: getComputedStyle(v).display,
                    visibility: getComputedStyle(v).visibility,
                    opacity: getComputedStyle(v).opacity
                  }))
                );
                
            } else {
"""
        target_activate = r'if \(desiredOpacity >= 1\.0\) \{\n\s*stopALLOriginalVideos\(\);\n\s*hideALLOriginalCharacterRendering\(\);\n\s*\} else \{'
        content = re.sub(target_activate, log_hidden.strip() + " else {", content, flags=re.DOTALL)
        
        content = content.replace('console.log("[DaFitMatch] TRY-ON ACTIVE");', 'console.log("[DaFitMatch FINAL] TRY-ON ACTIVE");')
        
        script.string.replace_with(content)

with open('index.html', 'w') as f:
    f.write(str(soup))
