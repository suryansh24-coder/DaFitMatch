import re

with open('index.html', 'r') as f:
    html = f.read()

# I need to modify selectOutfit where it assigns the src.
old_logic = """
        // 3. Check Try-On Image
        if (selectedOutfit.tryOnImage) {
            const imgAvailable = await new Promise((resolve) => {
                const img = new Image();
                img.onload = () => resolve(true);
                img.onerror = () => resolve(false);
                img.src = selectedOutfit.tryOnImage;
            });
"""

new_logic = """
        // 3. Check Try-On Image
        if (selectedOutfit.tryOnImage) {
            const tryOnUrl = selectedOutfit.tryOnImage + "?tryonDebug=" + Date.now();
            console.log("[DaFitMatch Try-On] Loading image:", tryOnUrl);
            
            const imgAvailable = await new Promise((resolve) => {
                const img = new Image();
                img.onload = () => {
                    console.log("[DaFitMatch] TRY-ON IMAGE ONLOAD", img.naturalWidth, img.naturalHeight);
                    resolve(true);
                };
                img.onerror = (e) => {
                    console.error("[DaFitMatch] TRY-ON IMAGE ONERROR", e, img.src);
                    resolve(false);
                };
                img.src = tryOnUrl;
            });
"""

old_assignment = """
            if (imgAvailable) {
                devDiag.imgAvailable = true;
                devDiag.displayMode = 'TRY-ON IMAGE';
                
                tryOnImageEl.src = selectedOutfit.tryOnImage;
                tryOnImageEl.classList.remove('opacity-0');
"""

new_assignment = """
            if (imgAvailable) {
                devDiag.imgAvailable = true;
                devDiag.displayMode = 'TRY-ON IMAGE';
                
                const finalUrl = selectedOutfit.tryOnImage + "?tryonDebug=" + Date.now();
                tryOnImageEl.src = finalUrl;
                
                // Debugging styles
                tryOnImageEl.style.position = "absolute";
                tryOnImageEl.style.inset = "0";
                tryOnImageEl.style.width = "100%";
                tryOnImageEl.style.height = "100%";
                tryOnImageEl.style.objectFit = "contain";
                tryOnImageEl.style.zIndex = "9999";
                tryOnImageEl.style.opacity = "1";
                tryOnImageEl.style.display = "block";
                tryOnImageEl.style.visibility = "visible";
                tryOnImageEl.style.outline = "5px solid red";
                
                console.log("TRY-ON ELEMENT", tryOnImageEl);
                console.log("SRC", tryOnImageEl.src);
                console.log("CURRENT SRC ATTRIBUTE", tryOnImageEl.getAttribute("src"));
                console.log("NATURAL WIDTH", tryOnImageEl.naturalWidth);
                console.log("NATURAL HEIGHT", tryOnImageEl.naturalHeight);
                
                const styles = window.getComputedStyle(tryOnImageEl);
                console.log("DISPLAY", styles.display);
                console.log("VISIBILITY", styles.visibility);
                console.log("OPACITY", styles.opacity);
                console.log("Z-INDEX", styles.zIndex);
                console.log("POSITION", styles.position);

                const existingVideo = document.getElementById('vid-clothing-fwd');
                if (existingVideo) {
                    console.log("MP4 ELEMENT", existingVideo);
                    const videoStyles = window.getComputedStyle(existingVideo);
                    console.log("VIDEO DISPLAY", videoStyles.display);
                    console.log("VIDEO VISIBILITY", videoStyles.visibility);
                    console.log("VIDEO OPACITY", videoStyles.opacity);
                    console.log("VIDEO Z-INDEX", videoStyles.zIndex);
                }
                
                console.log("TRY-ON PARENT", tryOnImageEl.parentElement);

                tryOnImageEl.classList.remove('opacity-0');
"""

html = html.replace(old_logic.strip(), new_logic.strip())
html = html.replace(old_assignment.strip(), new_assignment.strip())

with open('index.html', 'w') as f:
    f.write(html)

print("Injected visual debug and cache buster.")
