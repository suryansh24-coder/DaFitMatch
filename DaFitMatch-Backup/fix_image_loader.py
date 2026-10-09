import re

with open('index.html', 'r') as f:
    html = f.read()

# I will replace the image fetching block:
old_img_check = """
        // 3. Check Try-On Image
        if (selectedOutfit.tryOnImage) {
            const resImg = await fetch(selectedOutfit.tryOnImage, { method: 'HEAD' }).catch(()=>({ok:false}));
            if (resImg.ok) {
                devDiag.imgAvailable = true;
                devDiag.displayMode = 'TRY-ON IMAGE';
                
                tryOnImageEl.src = selectedOutfit.tryOnImage;
                tryOnImageEl.classList.remove('opacity-0');
                tryOnVideoEl.classList.add('opacity-0');
                setTimeout(() => tryOnVideoEl.src = '', 500);
                
                updateTryOnDiagnostics(devDiag);
                showOutfitToast(selectedOutfit.name + " applied.");
                return;
            }
        }
"""

new_img_check = """
        // 3. Check Try-On Image
        if (selectedOutfit.tryOnImage) {
            const imgAvailable = await new Promise((resolve) => {
                const img = new Image();
                img.onload = () => resolve(true);
                img.onerror = () => resolve(false);
                img.src = selectedOutfit.tryOnImage;
            });
            
            if (imgAvailable) {
                devDiag.imgAvailable = true;
                devDiag.displayMode = 'TRY-ON IMAGE';
                
                tryOnImageEl.src = selectedOutfit.tryOnImage;
                tryOnImageEl.classList.remove('opacity-0');
                tryOnVideoEl.classList.add('opacity-0');
                setTimeout(() => tryOnVideoEl.src = '', 500);
                
                updateTryOnDiagnostics(devDiag);
                showOutfitToast(selectedOutfit.name + " applied.");
                return;
            }
        }
"""

# Let's also do the same for tryOnVideo just in case, but they only asked for Image.
# "Do NOT use HEAD to determine whether the try-on image exists."
# For video:
old_vid_check = """
        // 2. Check Try-On Video
        if (selectedOutfit.tryOnVideo) {
            const resVid = await fetch(selectedOutfit.tryOnVideo, { method: 'HEAD' }).catch(()=>({ok:false}));
            if (resVid.ok) {
"""
new_vid_check = """
        // 2. Check Try-On Video
        if (selectedOutfit.tryOnVideo) {
            const vidAvailable = await new Promise((resolve) => {
                const vid = document.createElement('video');
                vid.onloadedmetadata = () => resolve(true);
                vid.onerror = () => resolve(false);
                vid.src = selectedOutfit.tryOnVideo;
            });
            if (vidAvailable) {
"""

html = html.replace(old_img_check.strip(), new_img_check.strip())
html = html.replace(old_vid_check.strip(), new_vid_check.strip())

with open('index.html', 'w') as f:
    f.write(html)

print("Updated try-on asset detection logic.")
