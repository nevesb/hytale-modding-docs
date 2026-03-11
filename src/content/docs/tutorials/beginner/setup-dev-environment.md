---
title: Setup Your Dev Environment
description: Install the required tools and create a minimal working mod structure to start making Hytale mods.
---

## Goal

Install the tools you need, create a mod folder with a valid `manifest.json`, and load a minimal test mod into the game. By the end you will have a working foundation to build every subsequent tutorial on.

## Prerequisites

- Hytale installed (the game client or a local server build)
- Administrator or write access to the game's mods directory
- An internet connection to download tools

---

## Step 1: Install Required Tools

You need three tools to work with Hytale mods efficiently.

### Hytale (game client or server)

The game is required to load and test mods. Mods are loaded from a `mods/` folder in the game's data directory — the exact path appears in the launcher settings.

### Visual Studio Code

VS Code is the recommended editor for Hytale JSON files. It provides syntax highlighting, error detection, and JSON schema validation.

Download from: **https://code.visualstudio.com/**

After installing, add the following extensions from the VS Code Extensions panel (`Ctrl+Shift+X`):

| Extension | Purpose |
|-----------|---------|
| **JSON** (built-in) | Syntax highlighting and bracket matching |
| **Error Lens** | Inline display of JSON validation errors |
| **Prettier** | Auto-formats JSON on save so structure stays consistent |

### Blockbench

Blockbench is the 3D modelling tool used to create `.blockymodel` files for items, NPCs, and decorations. The Hytale plugin adds export support for Hytale's native format.

Download from: **https://www.blockbench.net/**

After installing Blockbench:

1. Open Blockbench
2. Go to **File > Plugins**
3. Search for `Hytale`
4. Install the **Hytale Exporter** plugin
5. Restart Blockbench

The plugin adds a **Hytale Blocky Model** export option under **File > Export**.

---

## Step 2: Create Your Mod Folder Structure

Every Hytale mod is a folder with a `manifest.json` at its root. The folder name becomes your mod's internal identifier — use only letters, numbers, and underscores.

Create the following folder structure:

```
MyMod/
  manifest.json
  Assets/
    Common/
      BlockTextures/
        MyMod/
      Models/
        Items/
        NPCs/
    Server/
      Item/
        Block/
          Blocks/
            MyMod/
        Items/
          MyMod/
        Recipes/
          MyMod/
      NPC/
        Roles/
          MyMod/
        Spawn/
          World/
      Drops/
        NPCs/
          MyMod/
      BlockTypeList/
    Languages/
```

You do not need every folder immediately — create them as you add content. The minimum required is `manifest.json` and the `Assets/` folder.

---

## Step 3: Create manifest.json

The `manifest.json` file identifies your mod to the game. The engine reads it on startup to register the mod and its asset paths.

Create `MyMod/manifest.json`:

```json
{
  "Group": "MyMod",
  "Name": "My First Hytale Mod"
}
```

| Field | Purpose |
|-------|---------|
| `Group` | Internal namespace for your mod. Used to avoid naming conflicts with other mods. Match this to your folder name |
| `Name` | Display name shown in the mod list |

Compare to the vanilla `manifest.json` at `Assets/manifest.json`:

```json
{
  "Group": "Hytale",
  "Name": "Hytale"
}
```

Your `Group` value should be unique — avoid using `Hytale` or generic names like `Mod` that might conflict with other mods.

---

## Step 4: Set Up VS Code for JSON Editing

Open your mod folder in VS Code:

```
File > Open Folder > select MyMod/
```

### Configure auto-format on save

Create `.vscode/settings.json` inside your mod folder:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "[json]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "files.associations": {
    "*.lang": "properties"
  }
}
```

This ensures your JSON is always validly formatted — trailing commas and syntax errors are caught before you try to load the mod.

### Enable JSON validation hints

VS Code's built-in JSON language server flags syntax errors inline. When you open a `.json` file:

- Red underlines indicate syntax errors (missing commas, mismatched brackets)
- Yellow underlines from Error Lens indicate warnings

**Tip:** Hytale JSON uses a superset of standard JSON in some places — field names and string values are case-sensitive. The engine will reject `"material": "solid"` but accept `"Material": "Solid"`.

---

## Step 5: Configure Blockbench for Hytale

After installing the Hytale Exporter plugin:

1. Open Blockbench
2. Create a new model: **File > New > Hytale Blocky Model**
3. Build your model using cubes and bone groups
4. Set the texture in the **Textures** panel on the right side
5. Export with **File > Export > Export Hytale Blocky Model**

### Model conventions

| Convention | Detail |
|------------|--------|
| Scale | 1 Blockbench unit = 1/16th of a Hytale block |
| Pivot point | Centre the model at `[0, 0, 0]` for correct hand positioning |
| Texture size | Powers of two only: 16x16, 32x32, 64x64, 128x128 |
| Bone naming | Follow vanilla naming patterns (`Root`, `Body`, `Head`) for animation compatibility |
| File format | Export as `.blockymodel`; textures export separately as `.png` |

---

## Step 6: Create a Minimal Test Mod

With your folder structure and manifest in place, add a single block to verify the full pipeline works end to end.

Create `MyMod/Assets/Server/Item/Block/Blocks/MyMod/Block_Test.json`:

```json
{
  "Textures": [
    {
      "All": "Blocks/_Debug/Texture.png"
    }
  ],
  "Material": "Solid"
}
```

This references the vanilla debug texture so you do not need to create any art yet.

Create `MyMod/Assets/Server/BlockTypeList/MyMod_Blocks.json`:

```json
{
  "Blocks": [
    "Block_Test"
  ]
}
```

Create `MyMod/Assets/Server/Item/Items/MyMod/Block_Test.json`:

```json
{
  "TranslationProperties": {
    "Name": "server.items.Block_Test.name"
  },
  "Quality": "Common",
  "Icon": "Icons/Items/Block_Rock_Grey.png",
  "BlockType": {
    "Material": "Solid",
    "DrawType": "Block",
    "Opacity": "Opaque"
  },
  "MaxStack": 64
}
```

Create `MyMod/Assets/Languages/en-US.lang`:

```
server.items.Block_Test.name=Test Block
```

Your final minimal mod structure:

```
MyMod/
  manifest.json
  Assets/
    Server/
      Item/
        Block/
          Blocks/
            MyMod/
              Block_Test.json
        Items/
          MyMod/
            Block_Test.json
      BlockTypeList/
        MyMod_Blocks.json
    Languages/
      en-US.lang
```

---

## Step 7: Load and Test the Mod

1. Copy your `MyMod/` folder into the game's `mods/` directory. The path varies by installation — check the launcher or server configuration for the exact location.
2. Start the game or server.
3. Watch the startup log for lines referencing your mod files. Errors always include the file path and the problematic field name.
4. Once loaded, use the in-game developer console or item spawner to give yourself `Block_Test`.
5. Place the block and confirm it renders with the debug texture.

### Reading startup errors

| Log pattern | Meaning |
|-------------|---------|
| `Loaded mod: MyMod` | Manifest found and read successfully |
| `Unknown block id: Block_Test` | Block not registered in any BlockTypeList |
| `Texture not found: Blocks/_Debug/Texture.png` | Path typo or vanilla assets not loading |
| `JSON parse error in Block_Test.json` | Syntax error — open in VS Code to find the red underline |

---

## Complete Files

### `MyMod/manifest.json`
```json
{
  "Group": "MyMod",
  "Name": "My First Hytale Mod"
}
```

### `MyMod/.vscode/settings.json`
```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "[json]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "files.associations": {
    "*.lang": "properties"
  }
}
```

### `MyMod/Assets/Server/Item/Block/Blocks/MyMod/Block_Test.json`
```json
{
  "Textures": [
    {
      "All": "Blocks/_Debug/Texture.png"
    }
  ],
  "Material": "Solid"
}
```

### `MyMod/Assets/Server/BlockTypeList/MyMod_Blocks.json`
```json
{
  "Blocks": [
    "Block_Test"
  ]
}
```

### `MyMod/Assets/Server/Item/Items/MyMod/Block_Test.json`
```json
{
  "TranslationProperties": {
    "Name": "server.items.Block_Test.name"
  },
  "Quality": "Common",
  "Icon": "Icons/Items/Block_Rock_Grey.png",
  "BlockType": {
    "Material": "Solid",
    "DrawType": "Block",
    "Opacity": "Opaque"
  },
  "MaxStack": 64
}
```

### `MyMod/Assets/Languages/en-US.lang`
```
server.items.Block_Test.name=Test Block
```

---

## Next Steps

- [Create a Custom Block](/hytale-modding-docs/tutorials/beginner/create-a-block) — build a full glowing block with texture, recipe, and item definition
- [Create a Custom Item](/hytale-modding-docs/tutorials/beginner/create-an-item) — add a craftable weapon with damage stats
- [Create a Custom NPC](/hytale-modding-docs/tutorials/beginner/create-an-npc) — spawn a passive critter with a drop table
- [JSON Basics](/hytale-modding-docs/getting-started/json-basics) — deeper reference for template inheritance and validation
