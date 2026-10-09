with open('index.html', 'r') as f:
    html = f.read()

new_css = """
<style>
#dafitmatch-tryon-overlay {
  position: absolute !important;
  inset: 0 !important;
  width: 100% !important;
  height: 100% !important;
  z-index: 999999 !important;
  pointer-events: none !important;
  overflow: hidden !important;
}
#dafitmatch-tryon-overlay img,
#dafitmatch-tryon-overlay video {
  position: absolute !important;
  z-index: 1000000 !important;
}
</style>
</head>
"""

html = html.replace('</head>', new_css)

# Check if there's any remaining `if (window.dafitmatchTryOnState !== 'TRY_ON_ACTIVE')` checks needed.
# The user said: "Any code that restores original character visibility MUST be guarded: if (window.dafitmatchTryOnState === 'TRY_ON_ACTIVE') { return; }"
# I added that earlier to the animation loop.
# Let's make absolutely sure.
if 'if (window.dafitmatchTryOnState !== \'TRY_ON_ACTIVE\')' in html:
    print("Guard found.")

with open('index.html', 'w') as f:
    f.write(html)
