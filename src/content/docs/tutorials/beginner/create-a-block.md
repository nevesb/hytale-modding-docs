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

- `https://github.com/nevesb/hytale-mods-custom-block/blob/master/source-assets/blockbench/Crystal_Glow.bbmodel`
- `https://github.com/nevesb/hytale-mods-custom-block/blob/master/Assets/Common/Blocks/HytaleModdingManual/Crystal_Glow.blockymodel`
- `https://github.com/nevesb/hytale-mods-custom-block/blob/master/Assets/Common/BlockTextures/HytaleModdingManual/Crystal_Glow.png`
- `https://github.com/nevesb/hytale-mods-custom-block/blob/master/Assets/Server/Item/Block/Blocks/HytaleModdingManual/Block_Crystal_Glow.json`
- `https://github.com/nevesb/hytale-mods-custom-block/blob/master/Assets/Server/Item/Items/HytaleModdingManual/Block_Crystal_Glow.json`
- `https://github.com/nevesb/hytale-mods-custom-block/blob/master/Assets/Server/Languages/en-US/server.lang`

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

Instead of using a plain cube with a single texture, start from a real Blockbench model.

For the crystal example, the authoring file is:

```text
source-assets/blockbench/Crystal_Glow.bbmodel
```

This source model contains:

- the custom crystal silhouette
- the final UV layout
- the painted texture atlas used by the exported block

When your model is ready, export it to:

```text
Assets/Common/Blocks/HytaleModdingManual/Crystal_Glow.blockymodel
```

## Step 2: Save the Texture and Icon

The block texture used by the exported model goes here:

```text
Assets/Common/BlockTextures/HytaleModdingManual/Crystal_Glow.png
```

The inventory icon goes here:

```text
Assets/Common/Icons/ItemsGenerated/Block_Crystal_Glow.png
```

In the worked crystal example:

- the block uses a custom painted texture atlas
- the item icon is generated from the final block art

## Step 3: Create the Standalone Block Definition

Create the block definition at:

```text
Assets/Server/Item/Block/Blocks/HytaleModdingManual/Block_Crystal_Glow.json
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
Assets/Server/BlockTypeList/HytaleModdingManual_Blocks.json
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
Assets/Server/Item/Items/HytaleModdingManual/Block_Crystal_Glow.json
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
Assets/Server/Languages/en-US/server.lang
Assets/Server/Languages/pt-BR/server.lang
Assets/Server/Languages/es/server.lang
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

In this worked project, the packaged output lives at:

```text
dist/CreateACustomBlock
```

That folder is the version you copy into the Hytale mods directory.

## Step 8: Test In Game

1. Copy `dist/CreateACustomBlock` into your Hytale mods folder.
2. Start the game or reload the mod environment.
3. Spawn `Block_Crystal_Glow`.
4. Place the block in the world.
5. Confirm:
   - the custom crystal model appears
   - the block emits light
   - the crystal sound set is used
   - the block drops itself when broken

### Final Result

Add a real in-game screenshot to:

```text
../tutorials/hytale-guide-create-a-block/qa/screenshots/create-a-block/final-result.png
```

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
Assets/Common/Blocks/HytaleModdingManual/Crystal_Glow.blockymodel
Assets/Common/BlockTextures/HytaleModdingManual/Crystal_Glow.png
Assets/Common/Icons/ItemsGenerated/Block_Crystal_Glow.png
Assets/Server/BlockTypeList/HytaleModdingManual_Blocks.json
Assets/Server/Item/Block/Blocks/HytaleModdingManual/Block_Crystal_Glow.json
Assets/Server/Item/Items/HytaleModdingManual/Block_Crystal_Glow.json
Assets/Server/Languages/en-US/server.lang
source-assets/blockbench/Crystal_Glow.bbmodel
```

## Next Steps

- [Create a Custom Item](/hytale-modding-docs/tutorials/beginner/create-an-item)
- [Create a Custom NPC](/hytale-modding-docs/tutorials/beginner/create-an-npc)
- [JSON Basics](/hytale-modding-docs/getting-started/json-basics)
