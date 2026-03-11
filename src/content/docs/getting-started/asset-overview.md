---
title: Asset Overview
description: Understanding Hytale's asset types and file formats.
---

## File Formats

Hytale uses several custom file formats alongside standard ones:

### JSON Configuration (`.json`)

The primary format for all game data. Used for:
- NPC role definitions
- Item and block definitions
- Recipes and loot tables
- Spawn rules and world generation
- Model definitions (server-side)
- Gameplay configurations

### Blocky Model (`.blockymodel`)

Hytale's 3D model format. JSON-based internally, containing:
- Cuboid geometry (position, size, rotation)
- UV mapping to texture sheets
- Bone hierarchy for animation
- Attachment points for equipment

Created and edited with **Blockbench** using the Hytale plugin.

### Blocky Animation (`.blockyanim`)

Hytale's animation format. JSON-based, containing:
- Keyframe data for bones
- Position, rotation, and scale channels
- Loop settings and timing

### Textures (`.png`)

Standard PNG images used for:
- Block faces
- Model textures (resolution varies by model complexity)
- UI elements and icons
- Particle effects

Hytale uses pixel-art style textures. Common resolutions:
- **32 px density** — Standard cube blocks
- **64 px density** — Player models and most character-scale equipment
- **64 px density (best current assumption)** — NPCs and mobs, based on the Hytale Modding community reference

When choosing a texture size, match the target asset's pixel density first. For example, a block face may be `32x32`, while a character sheet may be `64x64` or `128x128` if it preserves the same density.

## Key Concepts

### Namespace

Every asset is identified by its mod namespace: `Group:Name`. For example, `Hytale:Sword_Iron` refers to the iron sword in the base game.

### Inheritance

Many JSON files support inheritance via `Parent` or `Reference` fields. This lets you create new content by extending existing definitions rather than writing everything from scratch. See [Inheritance and Templates](/hytale-modding-docs/reference/concepts/inheritance-and-templates/) for details.

### Localization

All player-facing text uses translation keys rather than hardcoded strings. Keys are defined in `.lang` files under the `Languages/` directories. See [Localization Keys](/hytale-modding-docs/reference/concepts/localization-keys/) for the format.
