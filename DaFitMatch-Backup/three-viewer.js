import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

export class FittingRoom3D {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.USE_3D_CHARACTER = true;
        
        if (!this.container || !this.USE_3D_CHARACTER) return;

        this.scene = new THREE.Scene();
        // Match existing background atmospheric perspective roughly (if transparency doesn't work)
        // this.scene.background = new THREE.Color(0xa5c8e4); // fallback if not transparent
        
        this.camera = new THREE.PerspectiveCamera(45, this.container.clientWidth / this.container.clientHeight, 0.1, 100);
        this.camera.position.set(0, 1.2, 4); // Match framing
        
        this.renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        this.renderer.outputColorSpace = THREE.SRGBColorSpace;
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        this.container.appendChild(this.renderer.domElement);

        this.setupLighting();

        this.loader = new GLTFLoader();
        this.mixer = null;
        this.clock = new THREE.Clock();
        
        this.baseCharacter = null;
        this.baseSkeleton = null;
        this.currentOutfitMeshes = [];
        
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

        
        this.init();
        
        window.addEventListener('resize', this.onWindowResize.bind(this));
    }

    
    createDiagnosticOverlay() {
        // The development diagnostics panel is disabled for the normal UI: it
        // leaked "waiting for base-character.glb" style status onto the
        // user-facing page and, at narrow widths, covered the scene controller.
        // Internal console logging / error handling are untouched; flip this to
        // true while debugging the 3D viewer locally.
        const SHOW_DEV_DIAGNOSTICS = false;
        if (!this.isDevMode || !SHOW_DEV_DIAGNOSTICS) return;
        
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

3D CHARACTER:
${this.diagState.charFound ? '✓ base-character.glb loaded' : 'waiting for base-character.glb'}

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

    setupLighting() {
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        this.scene.add(ambientLight);

        const dirLight = new THREE.DirectionalLight(0xffffff, 1.2);
        dirLight.position.set(2, 5, 3);
        dirLight.castShadow = true;
        dirLight.shadow.mapSize.width = 1024;
        dirLight.shadow.mapSize.height = 1024;
        this.scene.add(dirLight);
        
        const fillLight = new THREE.DirectionalLight(0xe8f2fa, 0.5);
        fillLight.position.set(-2, 3, 2);
        this.scene.add(fillLight);
    }

    async init() {
        // Step 4: Temporary Character Support
        try {
            const gltf = await this.loadModelAsync('/models/character/base-character.glb');
            this.baseCharacter = gltf.scene;
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
            
            // Adjust position to match existing video aesthetic
            this.baseCharacter.position.set(0, -1, 0); 
            this.scene.add(this.baseCharacter);

            if (gltf.animations && gltf.animations.length > 0) {
                this.diagState.animFound = true;
                this.mixer = new THREE.AnimationMixer(this.baseCharacter);
                // Assume first animation is idle
                const action = this.mixer.clipAction(gltf.animations[0]);
                action.play();
            }
            this.updateDiagnostics();

            this.animate();
            console.log("3D Base character loaded and playing.");
            
            // Hide video system if 3D character loads successfully
            const videos = document.querySelectorAll('.media[id^="vid-"]');
            videos.forEach(v => v.style.display = 'none');
            
        } catch (e) {
            console.warn("Base character not found at /models/character/base-character.glb. 3D Viewer is waiting for assets.");
            // We do NOT start rendering loop or hide videos if the character is missing.
        }
    }

    loadModelAsync(url) {
        return new Promise((resolve, reject) => {
            this.loader.load(url, resolve, undefined, reject);
        });
    }

    async loadOutfit(outfit) {
        if (!this.baseCharacter || !this.baseSkeleton) {
            console.warn("Cannot load outfit: Base character skeleton missing.");
            return false;
        }

        const modelPath = outfit.model3D;
        if (!modelPath) return false;

        // Caching
        let outfitScene;
        if (this.outfitCache.has(modelPath)) {
            outfitScene = this.outfitCache.get(modelPath).clone();
        } else {
            try {
                const gltf = await this.loadModelAsync(modelPath);
                this.outfitCache.set(modelPath, gltf.scene);
                outfitScene = gltf.scene.clone();
                this.diagState.outfitFound = true;
                this.diagState.outfitName = modelPath.split('/').pop();
            } catch (e) {
                console.error("Failed to load outfit GLB:", modelPath);
                this.diagState.outfitFound = false;
                this.diagState.outfitName = modelPath.split('/').pop();
                this.diagState.outfitCompat = '? unable to verify';
                this.updateDiagnostics();
                return false;
            }
        }

        // Remove previous clothing
        this.currentOutfitMeshes.forEach(mesh => {
            this.scene.remove(mesh);
            if (mesh.geometry) mesh.geometry.dispose();
            if (mesh.material) {
                if (Array.isArray(mesh.material)) mesh.material.forEach(m => m.dispose());
                else mesh.material.dispose();
            }
        });
        this.currentOutfitMeshes = [];

        // Attach new clothing to existing skeleton
        outfitScene.traverse((child) => {
            if (child.isSkinnedMesh) {
                // Skeleton Compatibility Retargeting
                // We bind the clothing mesh to the base character's skeleton
                const newSkinnedMesh = new THREE.SkinnedMesh(child.geometry, child.material);
                newSkinnedMesh.bind(this.baseSkeleton, newSkinnedMesh.matrixWorld);
                newSkinnedMesh.castShadow = true;
                newSkinnedMesh.receiveShadow = true;
                
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
            }
        });

        console.log("Outfit successfully applied:", outfit.id);
        this.updateDiagnostics();
        return true;
    }

    onWindowResize() {
        if (!this.camera || !this.renderer || !this.container) return;
        this.camera.aspect = this.container.clientWidth / this.container.clientHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
    }

    animate() {
        requestAnimationFrame(this.animate.bind(this));
        const delta = this.clock.getDelta();
        if (this.mixer) this.mixer.update(delta);
        this.renderer.render(this.scene, this.camera);
    }
}
