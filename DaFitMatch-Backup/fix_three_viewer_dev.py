with open('three-viewer.js', 'r') as f:
    code = f.read()

dev_logic = """
    createDiagnosticOverlay() {
        if (!this.isDevMode) return;
        
        let overlay = document.getElementById('dev-diagnostic-overlay');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.id = 'dev-diagnostic-overlay';
            overlay.className = 'fixed bottom-4 left-4 bg-slate-900/95 backdrop-blur text-green-400 font-mono text-xs p-4 rounded-xl shadow-2xl z-50 border border-slate-700/50 whitespace-pre-wrap';
            document.body.appendChild(overlay);
        }
        this.diagnosticElement = overlay;
        this.updateDiagnostics();
    }

    updateDiagnostics() {
        if (!this.isDevMode || !this.diagnosticElement) return;
        
        const text = `DEVELOPMENT DIAGNOSTICS:

CHARACTER:
${this.diagState.charFound ? '✓ base-character.glb found' : '✗ base-character.glb missing'}

OUTFIT:
${this.diagState.outfitFound ? '✓ ' + this.diagState.outfitName + ' found' : '✗ ' + this.diagState.outfitName + ' missing'}

SKELETON:
${this.diagState.skeletonFound ? '✓ skeleton detected' : '✗ skeleton missing'}

ANIMATION:
${this.diagState.animFound ? '✓ animation detected' : '✗ animation missing'}

OUTFIT COMPATIBILITY:
${this.diagState.outfitCompat}`;
        
        this.diagnosticElement.textContent = text;
    }
"""

init_updates = """
        this.outfitCache = new Map();
        
        // Development Diagnostics
        this.isDevMode = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
        this.diagState = {
            charFound: false,
            outfitFound: false,
            outfitName: 'casual-01.glb',
            skeletonFound: false,
            animFound: false,
            outfitCompat: '? unable to verify'
        };
        this.createDiagnosticOverlay();
"""

code = code.replace("this.outfitCache = new Map();", init_updates)
code = code.replace("setupLighting() {", dev_logic + "\n    setupLighting() {")

# Update load character logic to set diagnostics
old_load_char = """
            this.baseCharacter.traverse((child) => {
                if (child.isSkinnedMesh) {
                    child.castShadow = true;
                    child.receiveShadow = true;
                    if (!this.baseSkeleton) {
                        this.baseSkeleton = child.skeleton;
                    }
                }
            });
"""
new_load_char = """
            this.diagState.charFound = true;
            this.baseCharacter.traverse((child) => {
                if (child.isSkinnedMesh) {
                    child.castShadow = true;
                    child.receiveShadow = true;
                    if (!this.baseSkeleton) {
                        this.baseSkeleton = child.skeleton;
                        this.diagState.skeletonFound = true;
                    }
                }
            });
"""
code = code.replace(old_load_char, new_load_char)

old_anim_check = """
            if (gltf.animations && gltf.animations.length > 0) {
                this.mixer = new THREE.AnimationMixer(this.baseCharacter);
                // Assume first animation is idle
                const action = this.mixer.clipAction(gltf.animations[0]);
                action.play();
            }
"""
new_anim_check = """
            if (gltf.animations && gltf.animations.length > 0) {
                this.diagState.animFound = true;
                this.mixer = new THREE.AnimationMixer(this.baseCharacter);
                // Assume first animation is idle
                const action = this.mixer.clipAction(gltf.animations[0]);
                action.play();
            }
            this.updateDiagnostics();
"""
code = code.replace(old_anim_check, new_anim_check)

old_outfit_load = """
                const gltf = await this.loadModelAsync(modelPath);
                this.outfitCache.set(modelPath, gltf.scene);
                outfitScene = gltf.scene.clone();
"""
new_outfit_load = """
                const gltf = await this.loadModelAsync(modelPath);
                this.outfitCache.set(modelPath, gltf.scene);
                outfitScene = gltf.scene.clone();
                this.diagState.outfitFound = true;
                this.diagState.outfitName = modelPath.split('/').pop();
"""
code = code.replace(old_outfit_load, new_outfit_load)

old_outfit_fail = """
            } catch (e) {
                console.error("Failed to load outfit GLB:", modelPath);
                return false;
            }
"""
new_outfit_fail = """
            } catch (e) {
                console.error("Failed to load outfit GLB:", modelPath);
                this.diagState.outfitFound = false;
                this.diagState.outfitName = modelPath.split('/').pop();
                this.diagState.outfitCompat = '? unable to verify';
                this.updateDiagnostics();
                return false;
            }
"""
code = code.replace(old_outfit_fail, new_outfit_fail)

old_outfit_bind = """
                // Add to scene but attached to base character's transforms
                this.scene.add(newSkinnedMesh);
                this.currentOutfitMeshes.push(newSkinnedMesh);
"""
new_outfit_bind = """
                // Add to scene but attached to base character's transforms
                this.scene.add(newSkinnedMesh);
                this.currentOutfitMeshes.push(newSkinnedMesh);
                
                // Extremely crude check: if bones array length matches loosely, mark compatible
                if (child.skeleton && this.baseSkeleton && child.skeleton.bones.length === this.baseSkeleton.bones.length) {
                    this.diagState.outfitCompat = '✓ compatible';
                } else {
                    // It will try to bind anyway, but warn if bones mismatch
                    this.diagState.outfitCompat = child.skeleton ? '✗ incompatible (bone count mismatch)' : '? unable to verify';
                }
"""
code = code.replace(old_outfit_bind, new_outfit_bind)

old_outfit_end = """
        console.log("Outfit successfully applied:", outfit.id);
        return true;
"""
new_outfit_end = """
        console.log("Outfit successfully applied:", outfit.id);
        this.updateDiagnostics();
        return true;
"""
code = code.replace(old_outfit_end, new_outfit_end)

with open('three-viewer.js', 'w') as f:
    f.write(code)

print("Updated three-viewer.js with diagnostic overlay.")
