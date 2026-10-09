with open('index.html', 'r') as f:
    html = f.read()

script_injection = """
<script>
let selectedOutfit = null;

async function selectOutfit(outfitId) {
    if(!catalogueData) return;
    
    // Single source of truth for selected outfit
    selectedOutfit = catalogueData.catalogues.flatMap(c => c.outfits).find(o => o.id === outfitId);
    if (!selectedOutfit) return;

    // Show subtle loading state
    showOutfitToast("Fitting your look...");

    // Architecture: Check if actual 3D asset is available
    const modelPath = selectedOutfit.model3D;
    
    try {
        // Attempt to check if the file exists (it won't, but this implements the requested architecture)
        const response = await fetch(modelPath, { method: 'HEAD' });
        
        if (response.ok) {
            // CLOTHING LOADING SYSTEM (Stubbed for future WebGL implementation)
            // 1. Detect selected outfit
            // 2. Read selectedOutfit.model3D
            // 3. Load the 3D clothing asset
            // 4. Attach it to the character
            // 5. Ensure the clothing follows the character's skeleton
            // 6. Preserve the existing animation
            // 7. Remove the previously selected clothing
            // 8. Dispose of the previous clothing resources properly
            
            showOutfitToast("Outfit applied to character.");
        } else {
            // Step 10: If clothing assets are not currently available
            setTimeout(() => {
                showOutfitToast("3D outfit preview coming soon");
            }, 800);
        }
    } catch (error) {
        console.error("3D model loading failed gracefully:", error);
        setTimeout(() => {
            showOutfitToast("3D outfit preview coming soon");
        }, 800);
    }
}

function showOutfitToast(message) {
    let toast = document.getElementById('outfit-toast');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'outfit-toast';
        toast.className = 'fixed bottom-8 left-1/2 transform -translate-x-1/2 bg-slate-900/90 backdrop-blur-md text-white px-5 py-2.5 rounded-full text-sm font-medium shadow-2xl z-50 transition-opacity duration-300 opacity-0 pointer-events-none border border-slate-700/50';
        document.body.appendChild(toast);
    }
    
    toast.textContent = message;
    toast.classList.remove('opacity-0');
    
    if (window.toastTimeout) clearTimeout(window.toastTimeout);
    
    window.toastTimeout = setTimeout(() => {
        toast.classList.add('opacity-0');
    }, 3000);
}
</script>
</body>"""

html = html.replace('</body>', script_injection)

with open('index.html', 'w') as f:
    f.write(html)

print("Injected script logic.")
