---
title: Create a Custom Block
description: Build a custom block in Blockbench, wire it into Hytale JSON, and test it in game.
---

## Goal

In this tutorial you will build a real custom block workflow:

1. model the block in Blockbench
2. export the runtime `.blockymodel`
3. save the texture and icon
4. register the block and item in JSON
5. package the mod and test it in game

The worked example used here is a glowing crystal block called `Block_Crystal_Glow`.

Worked example repository:

- `https://github.com/nevesb/hytale-mods-custom-block`

Key files from that repository:

- `https://github.com/nevesb/hytale-mods-custom-block/blob/master/Common/Blocks/HytaleModdingManual/Crystal_Glow.blockymodel`
- `https://github.com/nevesb/hytale-mods-custom-block/blob/master/Common/BlockTextures/HytaleModdingManual/Crystal_Glow.png`
- `https://github.com/nevesb/hytale-mods-custom-block/blob/master/Server/Item/Block/Blocks/HytaleModdingManual/Block_Crystal_Glow.json`
- `https://github.com/nevesb/hytale-mods-custom-block/blob/master/Server/Item/Items/HytaleModdingManual/Block_Crystal_Glow.json`
- `https://github.com/nevesb/hytale-mods-custom-block/blob/master/Server/Languages/en-US/server.lang`

## Prerequisites

- A mod folder with a valid `manifest.json`
- Blockbench for authoring the source model
- A Hytale build compatible with your `TargetServerVersion`
- Basic familiarity with JSON

For an asset-only tutorial mod, your manifest should look like this:

```json
{
  "Group": "HytaleModdingManual",
  "Name": "CreateACustomBlock",
  "Version": "1.0.0",
  "Description": "Implements the Create A Block tutorial with a custom crystal block",
  "Authors": [
    {
      "Name": "HytaleModdingManual"
    }
  ],
  "Dependencies": {},
  "OptionalDependencies": {},
  "IncludesAssetPack": true,
  "TargetServerVersion": "2026.02.19-1a311a592"
}
```

## Step 1: Build the Block in Blockbench

Instead of using a plain cube with a single texture, start from a real Blockbench model and export the runtime asset.

For the crystal example, the public repository keeps only the runtime-ready mod files. Model locally in Blockbench, then export to:

```text
Common/Blocks/HytaleModdingManual/Crystal_Glow.blockymodel
```

## Step 2: Save the Texture and Icon

The block texture used by the exported model goes here:

```text
Common/BlockTextures/HytaleModdingManual/Crystal_Glow.png
```

The inventory icon goes here:

```text
Common/Icons/ItemsGenerated/Block_Crystal_Glow.png
```

In the worked crystal example:

- the block uses a custom painted texture atlas
- the item icon is generated from the final block art

## Step 3: Create the Standalone Block Definition

Create the block definition at:

```text
Server/Item/Block/Blocks/HytaleModdingManual/Block_Crystal_Glow.json
```

For the custom-model workflow, the block should point to the exported `.blockymodel` and texture:

```json
{
  "Material": "Solid",
  "DrawType": "Model",
  "Opacity": "Transparent",
  "VariantRotation": "NESW",
  "CustomModel": "Blocks/HytaleModdingManual/Crystal_Glow.blockymodel",
  "CustomModelTexture": [
    {
      "Texture": "BlockTextures/HytaleModdingManual/Crystal_Glow.png",
      "Weight": 1
    }
  ],
  "HitboxType": "Full",
  "Gathering": {
    "Breaking": {
      "GatherType": "Rocks",
      "ItemId": "Block_Crystal_Glow"
    }
  },
  "Light": {
    "Color": "#88ccff",
    "Level": 14
  },
  "BlockSoundSetId": "Crystal",
  "ParticleColor": "#88ccff"
}
```

Notes:

- `DrawType: "Model"` tells Hytale to use the exported custom model instead of a default cube
- `CustomModel` points to the `.blockymodel`
- `CustomModelTexture` points to the texture used by that model
- `Gathering.Breaking.ItemId` makes the block drop itself when broken

## Step 4: Register the Block in a BlockTypeList

Create the list file at:

```text
Server/BlockTypeList/HytaleModdingManual_Blocks.json
```

```json
{
  "Blocks": [
    "Block_Crystal_Glow"
  ]
}
```

Hytale merges block lists from mods automatically. You do not need to modify any vanilla file.

## Step 5: Create the Item Definition

The item definition makes the block appear in inventory and tells the game how to place it.

Create:

```text
Server/Item/Items/HytaleModdingManual/Block_Crystal_Glow.json
```

```json
{
  "TranslationProperties": {
    "Name": "server.items.Block_Crystal_Glow.name",
    "Description": "server.items.Block_Crystal_Glow.description"
  },
  "Interactions": {
    "Primary": "Block_Primary",
    "Secondary": "Block_Secondary"
  },
  "Quality": "Uncommon",
  "Icon": "Icons/ItemsGenerated/Block_Crystal_Glow.png",
  "PlayerAnimationsId": "Block",
  "BlockType": {
    "Material": "Solid",
    "DrawType": "Model",
    "Opacity": "Transparent",
    "VariantRotation": "NESW",
    "CustomModel": "Blocks/HytaleModdingManual/Crystal_Glow.blockymodel",
    "CustomModelTexture": [
      {
        "Texture": "BlockTextures/HytaleModdingManual/Crystal_Glow.png",
        "Weight": 1
      }
    ],
    "HitboxType": "Full",
    "Flags": {},
    "Gathering": {
      "Breaking": {
        "GatherType": "Rocks",
        "ItemId": "Block_Crystal_Glow"
      }
    },
    "Light": {
      "Color": "#88ccff",
      "Level": 14
    },
    "BlockParticleSetId": "Stone",
    "BlockSoundSetId": "Crystal",
    "ParticleColor": "#88ccff"
  },
  "MaxStack": 64,
  "IconProperties": {
    "Scale": 0.58823,
    "Rotation": [22.5, 45, 22.5],
    "Translation": [0, -13.5]
  }
}
```

This is the key difference from a simple “textured cube” tutorial: the item and the standalone block both point to the same custom exported model and texture.

## Step 6: Add Localisation

Create a language file for each locale you want to support:

```text
Server/Languages/en-US/server.lang
Server/Languages/pt-BR/server.lang
Server/Languages/es/server.lang
```

Example:

```text
items.Block_Crystal_Glow.name = Glowing Crystal Block
items.Block_Crystal_Glow.description = A crystal block that radiates soft blue light.
```

And in the item JSON, keep the translation keys as:

```json
{
  "TranslationProperties": {
    "Name": "server.items.Block_Crystal_Glow.name",
    "Description": "server.items.Block_Crystal_Glow.description"
  }
}
```

## Step 7: Package the Mod

For runtime, the mod folder should be flat:

```text
CreateACustomBlock/
  Common/
  Server/
  manifest.json
```

The example repository is already in runtime layout. Copy the mod folder contents into your Hytale mods directory.

## Step 8: Test In Game

1. Copy the runtime mod folder into your Hytale mods directory.
2. Start the game or reload the mod environment.
3. Spawn `Block_Crystal_Glow`.
4. Place the block in the world.
5. Confirm:
   - the custom crystal model appears
   - the block emits light
   - the crystal sound set is used
   - the block drops itself when broken

### Final Result

Add a real in-game screenshot to your tutorial evidence set.

Recommended caption:

> Custom crystal block placed in game with its exported Blockbench model, texture, and light emission.

## Common Problems

| Problem | Cause | Fix |
|---|---|---|
| The block appears as a cube | `DrawType` or `CustomModel` is wrong, or the `.blockymodel` failed to parse | Re-export the model and verify `DrawType: "Model"` |
| The mod fails to load with a parent error | The block JSON has an accidental `Parent` field | Remove the invalid inheritance entry |
| The icon is missing | The `Icon` path is wrong | Use a valid path under `Icons/Items` or `Icons/ItemsGenerated` |
| The block texture is wrong | UVs or texture path are incorrect | Recheck Blockbench UVs and `CustomModelTexture` |
| The name shows as a key instead of text | Localisation path or key format is wrong | Verify `Server/Languages/<locale>/server.lang` and the `server.items.*` JSON keys |

## Complete File Set

```text
manifest.json
Common/Blocks/HytaleModdingManual/Crystal_Glow.blockymodel
Common/BlockTextures/HytaleModdingManual/Crystal_Glow.png
Common/Icons/ItemsGenerated/Block_Crystal_Glow.png
Server/BlockTypeList/HytaleModdingManual_Blocks.json
Server/Item/Block/Blocks/HytaleModdingManual/Block_Crystal_Glow.json
Server/Item/Items/HytaleModdingManual/Block_Crystal_Glow.json
Server/Languages/en-US/server.lang
```

## Next Steps

- [Create a Custom Item](/hytale-modding-docs/tutorials/beginner/create-an-item)
- [Create a Custom NPC](/hytale-modding-docs/tutorials/beginner/create-an-npc)
- [JSON Basics](/hytale-modding-docs/getting-started/json-basics)
