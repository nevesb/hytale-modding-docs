---
title: Installation
description: Set up the tools needed for Hytale modding.
---

## Prerequisites

Before creating Hytale mods, you need the following tools installed:

- **Hytale** — The game itself (with access to the modding system)
- **Blockbench** — Free 3D model editor for creating `.blockymodel` and `.blockyanim` files ([blockbench.net](https://www.blockbench.net))
- **Text Editor** — VS Code recommended for JSON editing with syntax highlighting
- **Image Editor** — Any pixel art editor for creating textures (Aseprite, GIMP, or Piskel)

## Hytale Mod Folder Structure

Hytale mods are organized as folders placed in the game's mod directory. Each mod contains a `manifest.json` at its root:

```json
{
  "Group": "MyStudio",
  "Name": "MyMod"
}
```

The `Group` identifies the author/organization, and `Name` is the mod's unique identifier. Together they form the mod's namespace: `MyStudio:MyMod`.

## Mod Folder Layout

A typical mod follows this structure:

```
MyMod/
├── manifest.json
├── Server/
│   ├── Models/
│   │   └── Beast/
│   ├── NPC/
│   │   ├── Roles/
│   │   └── Spawn/
│   ├── Item/
│   │   ├── Items/
│   │   ├── Block/
│   │   └── Recipes/
│   ├── Drops/
│   └── GameplayConfigs/
└── Common/
    ├── Blocks/
    ├── Items/
    ├── NPC/
    ├── Sounds/
    └── Icons/
```

- **`Server/`** — Server-side data: NPC roles, item definitions, recipes, loot tables, spawn rules
- **`Common/`** — Client-side assets: models, textures, animations, sounds, UI

## Next Steps

- [Server Setup](/hytale-modding-docs/getting-started/server-setup/) — Configure a local server for testing
- [Project Structure](/hytale-modding-docs/getting-started/project-structure/) — Detailed breakdown of every folder
- [JSON Basics](/hytale-modding-docs/getting-started/json-basics/) — How Hytale uses JSON for configuration
