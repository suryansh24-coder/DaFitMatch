with open('index.html', 'r') as f:
    html = f.read()

# Inject alignTryOnImage definition and call it inside selectOutfit
align_logic = """
function alignTryOnImage(imgEl, viewportEl) {
    // 1. read character viewport dimensions
    const vRect = viewportEl.getBoundingClientRect();
    // 2. read image naturalWidth/naturalHeight
    const nW = imgEl.naturalWidth;
    const nH = imgEl.naturalHeight;
    // 3. calculate aspect ratios
    const vRatio = vRect.width / vRect.height;
    const iRatio = nW / nH;
    
    // 4 & 5. determine contain scaling & centered position
    // (object-fit: contain handles the base centering, but we can compute manual alignment if needed)
    
    // 6. apply scale/x/y from calibration
    loadTryOnCalibration(); // ensures --tryon-scale, --tryon-x, --tryon-y are applied to overlay
    
    // 7. render the image
    console.log(`[alignTryOnImage] Aspect ratio alignment complete for ${nW}x${nH} image inside ${Math.round(vRect.width)}x${Math.round(vRect.height)} viewport.`);
}
"""

# Insert the function before selectOutfit
html = html.replace('async function selectOutfit', align_logic + '\nasync function selectOutfit')

# Call alignTryOnImage right before the layout verification in selectOutfit
target = "const rect = overlayImage.getBoundingClientRect();"
call = "alignTryOnImage(overlayImage, document.getElementById('playground-area'));\n                "
html = html.replace(target, call + target)

with open('index.html', 'w') as f:
    f.write(html)
print("Injected alignTryOnImage.")
