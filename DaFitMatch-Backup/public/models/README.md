# DaFitMatch 3D Assets

This directory contains the required 3D assets for the real-time fashion fitting room.

## BASE CHARACTER
**Path:** `public/models/character/base-character.glb`

**Requirements:**
- High-quality humanoid character suitable for a premium fashion aesthetic.
- Must contain a real skeleton (bones).
- Must use `SkinnedMesh`.
- Must include at least one animation clip (e.g., an idle or breathing loop).
- Neutral/fashion pose.
- Suitable for skinned clothing replacement (body parts underneath clothing should ideally be masked or the clothing should fit tightly over the skin without clipping).

## FIRST OUTFIT
**Path:** `public/models/outfits/casual-01.glb`

**Visual Representation:**
- Sage green linen shirt
- Cream trousers
- White sneakers

**Technical Requirements:**
- Must use `SkinnedMesh` geometry.
- Must be rigged to be **100% compatible with the base character skeleton** (same bone names, hierarchy, and rest pose).
- The clothing meshes must follow the character's animation perfectly when bound to the base skeleton.
