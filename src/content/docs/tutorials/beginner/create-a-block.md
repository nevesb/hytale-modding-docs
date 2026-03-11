---
title: Create a Custom Block
description: Step-by-step tutorial for adding a new placeable block to Hytale using real block definition JSON.
---

## Goal

Build a glowing crystal block that players can craft, place, and collect. You will create a texture, define the block in JSON, register it in a BlockTypeList, and create an item definition so it can appear in the player's inventory.

## Prerequisites

- A mod folder set up with a valid `manifest.json` (see [Setup Your Dev Environment](/hytale-modding-docs/tutorials/beginner/setup-dev-environment))
- A PNG image editor (Aseprite, Photoshop, GIMP, or similar) capable of exporting 16x16 or 32x32 PNGs
- Basic familiarity with JSON (see [JSON Basics](/hytale-modding-docs/getting-started/json-basics))

---

## Step 1: Create the Texture

Block textures in Hytale are standard PNG files. The engine supports both **16x16** and **32x32** pixel textures. All vanilla textures live under `Assets/Common/BlockTextures/` — your mod textures follow the same convention but inside your mod's folder.

Create a 16x16 PNG and save it to:

```
YourMod/Assets/Common/BlockTextures/MyMod/Crystal_Glow.png
```

**Texture guidelines:**
- Keep the pixel art style consistent with vanilla blocks (solid colours, no anti-aliasing)
- 16x16 is the standard resolution; 32x32 works for high-detail blocks
- The filename becomes part of your texture reference path

If you want different textures on the top, bottom, and sides, create three files:

```
YourMod/Assets/Common/BlockTextures/MyMod/Crystal_Glow_Top.png
YourMod/Assets/Common/BlockTextures/MyMod/Crystal_Glow_Side.png
YourMod/Assets/Common/BlockTextures/MyMod/Crystal_Glow_Bottom.png
```

---

## Step 2: Create the Block Definition JSON

Every block needs a JSON definition file. The engine looks for block files in:

```
Assets/Server/Item/Block/Blocks/
```

Create your block file at:

```
YourMod/Assets/Server/Item/Block/Blocks/MyMod/Block_Crystal_Glow.json
```

The simplest block definition — matching the pattern from `Assets/Server/Item/Block/Blocks/_Debug/Debug_Test_Block.json` — uses a single `"All"` texture key to apply the same texture to every face:

```json
{
  "Textures": [
    {
      "All": "MyMod/Crystal_Glow.png"
    }
  ],
  "Material": "Solid",
  "Light": {
    "Color": "#88ccff"
  }
}
```

### Texture keys

| Key | Which faces it applies to |
|-----|--------------------------|
| `All` | Every face |
| `Top` | Top face only |
| `Bottom` | Bottom face only |
| `Side` | All four side faces |
| `North` / `South` / `East` / `West` | Individual side faces |

For a block with a distinct top texture:

```json
{
  "Textures": [
    {
      "Top": "MyMod/Crystal_Glow_Top.png",
      "Side": "MyMod/Crystal_Glow_Side.png",
      "Bottom": "MyMod/Crystal_Glow_Bottom.png"
    }
  ],
  "Material": "Solid",
  "Light": {
    "Color": "#88ccff"
  }
}
```

### Material values

| Value | Behaviour |
|-------|-----------|
| `Solid` | Fully opaque, standard collision |
| `Transparent` | See-through (glass) |
| `Liquid` | Fluid physics |
| `Empty` | No collision (used for item world models) |

### Light

The optional `Light` object makes the block emit light. `Color` is a hex colour string — the RGB values control the tint and brightness of the emitted light. Omit `Light` entirely for a non-glowing block.

---

## Step 3: Register in a BlockTypeList

The engine discovers blocks through **BlockTypeList** files in `Assets/Server/BlockTypeList/`. Each list is a JSON object containing a `"Blocks"` array of block IDs. The block ID is the filename of your block JSON without the `.json` extension.

Create a new list file for your mod:

```
YourMod/Assets/Server/BlockTypeList/MyMod_Blocks.json
```

```json
{
  "Blocks": [
    "Block_Crystal_Glow"
  ]
}
```

Add more entries to this same list as your mod grows. You do not need to modify any vanilla BlockTypeList files — the engine merges all list files from all mods automatically.

---

## Step 4: Create the Item Definition

A block in the world and an item in the player's inventory are two separate concepts. You need an **item definition** that tells the engine how the block looks in hand, what quality it is, and (optionally) how it is crafted.

Create:

```
YourMod/Assets/Server/Item/Items/MyMod/Block_Crystal_Glow.json
```

```json
{
  "TranslationProperties": {
    "Name": "server.items.Block_Crystal_Glow.name",
    "Description": "server.items.Block_Crystal_Glow.description"
  },
  "Quality": "Uncommon",
  "Icon": "Icons/MyMod/Block_Crystal_Glow.png",
  "BlockType": {
    "Material": "Solid",
    "DrawType": "Block",
    "Opacity": "Opaque"
  },
  "MaxStack": 64,
  "Recipe": {
    "Input": [
      {
        "ItemId": "Ingredient_Crystal",
        "Quantity": 4
      }
    ],
    "Output": [
      {
        "ItemId": "Block_Crystal_Glow",
        "Quantity": 4
      }
    ],
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Id": "Craftingbench",
        "Categories": [
          "Blocks"
        ]
      }
    ],
    "TimeSeconds": 3
  }
}
```

**Translation keys** are resolved from your mod's language file. Create:

```
YourMod/Assets/Languages/en-US.lang
```

```
server.items.Block_Crystal_Glow.name=Glowing Crystal Block
server.items.Block_Crystal_Glow.description=A crystal block that radiates soft blue light.
```

**Icon:** The `Icon` path points to a PNG inside your mod's assets. At minimum, export a 64x64 PNG of your block for the inventory slot icon.

---

## Step 5: Test In-Game

1. Place your mod folder inside the server's mod directory.
2. Start the server. Watch the console for JSON validation errors — they always include the filename and field name.
3. Use the in-game item spawner (developer mode) to give yourself `Block_Crystal_Glow`.
4. Place it in the world and confirm the texture and light emission appear correctly.

**Common errors and fixes:**

| Error | Cause | Fix |
|-------|-------|-----|
| `Unknown block id` | Block not in any BlockTypeList | Add it to `MyMod_Blocks.json` |
| `Texture not found` | Wrong path in `"All"` / `"Top"` etc. | Check the path relative to `BlockTextures/` |
| `Missing field: Material` | Block JSON incomplete | Add `"Material": "Solid"` |
| Item not showing in crafting | Wrong bench `Id` | Match the exact bench ID from vanilla data |

---

## Complete Files

### `YourMod/Assets/Common/BlockTextures/MyMod/Crystal_Glow.png`
*(your 16x16 PNG texture — not shown)*

### `YourMod/Assets/Server/Item/Block/Blocks/MyMod/Block_Crystal_Glow.json`
```json
{
  "Textures": [
    {
      "All": "MyMod/Crystal_Glow.png"
    }
  ],
  "Material": "Solid",
  "Light": {
    "Color": "#88ccff"
  }
}
```

### `YourMod/Assets/Server/BlockTypeList/MyMod_Blocks.json`
```json
{
  "Blocks": [
    "Block_Crystal_Glow"
  ]
}
```

### `YourMod/Assets/Server/Item/Items/MyMod/Block_Crystal_Glow.json`
```json
{
  "TranslationProperties": {
    "Name": "server.items.Block_Crystal_Glow.name",
    "Description": "server.items.Block_Crystal_Glow.description"
  },
  "Quality": "Uncommon",
  "Icon": "Icons/MyMod/Block_Crystal_Glow.png",
  "BlockType": {
    "Material": "Solid",
    "DrawType": "Block",
    "Opacity": "Opaque"
  },
  "MaxStack": 64,
  "Recipe": {
    "Input": [
      {
        "ItemId": "Ingredient_Crystal",
        "Quantity": 4
      }
    ],
    "Output": [
      {
        "ItemId": "Block_Crystal_Glow",
        "Quantity": 4
      }
    ],
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Id": "Craftingbench",
        "Categories": [
          "Blocks"
        ]
      }
    ],
    "TimeSeconds": 3
  }
}
```

### `YourMod/Assets/Languages/en-US.lang`
```
server.items.Block_Crystal_Glow.name=Glowing Crystal Block
server.items.Block_Crystal_Glow.description=A crystal block that radiates soft blue light.
```

---

## Next Steps

- [Create a Custom Item](/hytale-modding-docs/tutorials/beginner/create-an-item) — add a weapon or tool that players can craft
- [Create a Custom NPC](/hytale-modding-docs/tutorials/beginner/create-an-npc) — spawn a creature that drops your new block
- [JSON Basics](/hytale-modding-docs/getting-started/json-basics) — deeper explanation of templates, computed values, and weight-based selection
