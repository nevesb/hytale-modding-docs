---
title: Create a Custom Crafting Bench
description: Step-by-step tutorial for adding a Crystal Anvil crafting bench with custom model, recipe categories, and crafting UI.
sidebar:
  order: 4
---

## Goal

Build a **Crystal Anvil** — a custom crafting bench that players can place in the world and use to forge crystal weapons. You will define the bench item with an inline `BlockType`, set up crafting categories, configure the required `State` for the crafting UI, and add translation keys.

## What You'll Learn

- How crafting benches are defined using the `Bench` block type property
- How `State` with `Id: "crafting"` is **required** for the bench UI to open
- How to create categories that organise recipes within the bench UI
- How tier levels and `CraftingTimeReductionModifier` control crafting speed
- How item recipes reference a bench via `BenchRequirement`

## Prerequisites

- A mod folder with a valid `manifest.json` (see [Setup Your Dev Environment](/hytale-modding-docs/tutorials/beginner/setup-dev-environment))
- Familiarity with block definitions (see [Create a Custom Block](/hytale-modding-docs/tutorials/beginner/create-a-block))
- Familiarity with item definitions (see [Create a Custom Item](/hytale-modding-docs/tutorials/beginner/create-an-item))

**Companion mod repository:** [hytale-mods-custom-bench](https://github.com/nevesb/hytale-mods-custom-bench)

---

## Crafting Bench Overview

Crafting benches in Hytale are **items** that contain an inline `BlockType` with a `Bench` configuration. Unlike pure blocks that need a separate Block JSON and `BlockTypeList`, benches define everything in a single Item JSON file — the same pattern used by vanilla benches like `Bench_Weapon` and `Bench_Armory`.

Key differences from regular blocks:
- **No separate Block JSON** in `Server/Item/Block/Blocks/`
- **No `BlockTypeList` entry** needed
- The `State` block with `Id: "crafting"` is **mandatory** for the crafting UI to work
- The `Bench` object defines the crafting type, categories, and tier levels

---

## Step 1: Set Up the Mod File Structure

```text
CreateACraftingBench/
├── manifest.json
├── Common/
│   ├── Blocks/
│   │   └── HytaleModdingManual/
│   │       └── Armory_Crystal_Glow.blockymodel
│   └── BlockTextures/
│       └── HytaleModdingManual/
│           └── Armory_Crystal_Glow.png
└── Server/
    ├── Item/
    │   └── Items/
    │       └── HytaleModdingManual/
    │           └── Bench_Armory_Crystal_Glow.json
    └── Languages/
        ├── en-US/
        │   └── server.lang
        ├── es/
        │   └── server.lang
        └── pt-BR/
            └── server.lang
```

### manifest.json

```json
{
  "Group": "HytaleModdingManual",
  "Name": "CreateACraftingBench",
  "Version": "1.0.0",
  "Description": "Crystal Anvil crafting bench for forging crystal weapons",
  "Authors": [
    {
      "Name": "HytaleModdingManual"
    }
  ],
  "Dependencies": {},
  "OptionalDependencies": {},
  "IncludesAssetPack": true
}
```

Note that `IncludesAssetPack` is `true` because we have Common assets (model and texture).

---

## Step 2: Create the Bench Item Definition

Create the bench at `Server/Item/Items/HytaleModdingManual/Bench_Armory_Crystal_Glow.json`:

```json
{
  "TranslationProperties": {
    "Name": "server.items.Bench_Armory_Crystal_Glow.name",
    "Description": "server.items.Bench_Armory_Crystal_Glow.description"
  },
  "Quality": "Rare",
  "Icon": "Icons/ItemsGenerated/Bench_Armory_Crystal_Glow.png",
  "Categories": [
    "Furniture.Benches"
  ],
  "Recipe": {
    "TimeSeconds": 10.0,
    "KnowledgeRequired": false,
    "Input": [
      {
        "ItemId": "Ore_Crystal_Glow",
        "Quantity": 3
      },
      {
        "ItemId": "Wood_Enchanted_Trunk",
        "Quantity": 10
      },
      {
        "ItemId": "Ingredient_Bar_Gold",
        "Quantity": 5
      }
    ],
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Categories": [
          "Workbench_Crafting"
        ],
        "Id": "Workbench",
        "RequiredTierLevel": 2
      }
    ]
  },
  "BlockType": {
    "Material": "Solid",
    "DrawType": "Model",
    "Opacity": "Transparent",
    "CustomModel": "Blocks/HytaleModdingManual/Armory_Crystal_Glow.blockymodel",
    "CustomModelTexture": [
      {
        "Texture": "BlockTextures/HytaleModdingManual/Armory_Crystal_Glow.png",
        "Weight": 1
      }
    ],
    "VariantRotation": "NESW",
    "HitboxType": "Bench_Weapon",
    "State": {
      "Id": "crafting",
      "Definitions": {
        "CraftCompleted": {
          "Looping": true
        },
        "CraftCompletedInstant": {}
      }
    },
    "Gathering": {
      "Breaking": {
        "GatherType": "Benches",
        "ItemId": "Bench_Armory_Crystal_Glow"
      }
    },
    "Light": {
      "Color": "#88ccff"
    },
    "Bench": {
      "Type": "Crafting",
      "LocalOpenSoundEventId": "SFX_Weapon_Bench_Open",
      "LocalCloseSoundEventId": "SFX_Weapon_Bench_Close",
      "CompletedSoundEventId": "SFX_Weapon_Bench_Craft",
      "Id": "Armory_Crystal_Glow",
      "Categories": [
        {
          "Id": "Crystal_Glow_Sword",
          "Name": "server.benchCategories.crystal_glow_sword",
          "Icon": "Icons/CraftingCategories/Armory/Sword.png"
        }
      ],
      "TierLevels": [
        {
          "CraftingTimeReductionModifier": 0.0
        }
      ]
    },
    "BlockSoundSetId": "Crystal",
    "ParticleColor": "#88ccff",
    "Support": {
      "Down": [
        {
          "FaceType": "Full"
        }
      ]
    },
    "BlockParticleSetId": "Crystal"
  },
  "PlayerAnimationsId": "Block",
  "IconProperties": {
    "Scale": 0.5,
    "Rotation": [
      22.5,
      45,
      22.5
    ],
    "Translation": [
      13,
      -14
    ]
  },
  "Tags": {
    "Type": [
      "Bench"
    ]
  },
  "MaxStack": 1,
  "ItemSoundSetId": "ISS_Items_Gems"
}
```

### Key bench fields explained

| Field | Purpose |
|-------|---------|
| `Bench.Type` | Must be `"Crafting"` for recipe-based benches |
| `Bench.Id` | Unique identifier that recipes reference in their `BenchRequirement` |
| `Bench.Categories` | Array of category tabs shown in the bench UI. Each has an `Id`, `Icon`, and translation `Name` |
| `Bench.TierLevels` | Array of upgrade tiers. Each can have `CraftingTimeReductionModifier` (percentage faster) and `UpgradeRequirement` |
| `State` | **Required.** Must have `"Id": "crafting"` for the bench UI to open on interaction |
| `VariantRotation` | `"NESW"` lets the bench face four directions when placed |
| `HitboxType` | Reuses `"Bench_Weapon"` hitbox for the interaction area |
| `Light.Color` | Emits a soft blue glow (`#88ccff`) |
| `Support.Down` | Requires a full block face below to place |

:::caution[State is mandatory]
Without the `State` block, the bench will place in the world but **the crafting UI will not open** when you interact with it. There is no error in the logs — it silently fails. Every vanilla bench (`Bench_Weapon`, `Bench_Armory`, `Bench_Campfire`) includes this `State` configuration.
:::

### Category structure

Each category in the `Categories` array defines a tab in the crafting UI:

```json
{
  "Id": "Crystal_Glow_Sword",
  "Name": "server.benchCategories.crystal_glow_sword",
  "Icon": "Icons/CraftingCategories/Armory/Sword.png"
}
```

- **`Id`** — The category identifier that recipes reference to appear under this tab
- **`Icon`** — Path to the icon PNG displayed on the category tab (we reuse the vanilla Sword icon)
- **`Name`** — Translation key for the category label text

---

## Step 3: Create a Recipe That Uses the Bench

Any item with a `Recipe` can reference your bench through `BenchRequirement`. The connection is made by matching `BenchRequirement.Id` to your bench's `Bench.Id`, and `Categories` to the category tabs the recipe appears under.

For example, the Crystal Glow Sword recipe references our bench:

```json
{
  "Recipe": {
    "TimeSeconds": 8.0,
    "Input": [
      {
        "ItemId": "Ore_Crystal_Glow",
        "Quantity": 10
      },
      {
        "ItemId": "Wood_Enchanted_Trunk",
        "Quantity": 50
      },
      {
        "ItemId": "Ingredient_Leather_Heavy",
        "Quantity": 10
      }
    ],
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Id": "Armory_Crystal_Glow",
        "Categories": [
          "Crystal_Glow_Sword"
        ]
      }
    ]
  }
}
```

### BenchRequirement fields

| Field | Purpose |
|-------|---------|
| `Type` | Must be `"Crafting"` to match a crafting bench |
| `Id` | Must exactly match the `Bench.Id` from your bench definition (case-sensitive) |
| `Categories` | Array of category IDs this recipe appears under. Must match a category `Id` from the bench |
| `RequiredTierLevel` | Minimum bench tier required. Omit for tier 0 (no upgrade needed) |

---

## Step 4: Add Translation Keys

Create language files at `Server/Languages/<locale>/server.lang`:

### English (`en-US/server.lang`)

```
items.Bench_Armory_Crystal_Glow.name = Crystal Anvil
items.Bench_Armory_Crystal_Glow.description = A crystal anvil for forging crystal weapons.
benchCategories.crystal_glow_sword = Crystal Sword
```

### Spanish (`es/server.lang`)

```
items.Bench_Armory_Crystal_Glow.name = Yunque de Cristal
items.Bench_Armory_Crystal_Glow.description = Un yunque de cristal para forjar armas de cristal.
benchCategories.crystal_glow_sword = Espada de Cristal
```

### Portuguese BR (`pt-BR/server.lang`)

```
items.Bench_Armory_Crystal_Glow.name = Bigorna de Cristal
items.Bench_Armory_Crystal_Glow.description = Uma bigorna de cristal para forjar armas de cristal.
benchCategories.crystal_glow_sword = Espada de Cristal
```

Note the translation key format: `items.<ItemId>.name` and `benchCategories.<category_id>`. The `server.` prefix in the JSON (`"Name": "server.items.Bench_Armory_Crystal_Glow.name"`) maps to the lang file key without the `server.` prefix.

---

## Step 5: Add the Custom Model

The bench uses a custom `.blockymodel` and texture. Place them in the `Common/` folder:

- **Model:** `Common/Blocks/HytaleModdingManual/Armory_Crystal_Glow.blockymodel`
- **Texture:** `Common/BlockTextures/HytaleModdingManual/Armory_Crystal_Glow.png`

You can create the model using [Blockbench](https://www.blockbench.net/) with the **Hytale Block** format. The model should fit within the block boundary (32 units = 1 block). For a 2-block-wide bench, use the `"HitboxType": "Bench_Weapon"` hitbox which covers the wider area.

:::tip[Common Asset Paths]
Common assets must be inside one of these root directories: `Blocks/`, `BlockTextures/`, `Items/`, `Resources/`, `NPC/`, `VFX/`, or `Consumable/`. Putting files outside these folders causes a load error.
:::

---

## Step 6: Test In-Game

1. Place the mod folder in your mods directory (`%APPDATA%/Hytale/UserData/Mods/`).
2. Start the server and check the logs for validation errors.
3. Use the command `/spawnitem Bench_Armory_Crystal_Glow` to give yourself the bench.
4. Place the bench and right-click to open the crafting UI.
5. Confirm the Crystal Sword category tab appears.

![Crystal Anvil placed in the world](/hytale-modding-docs/images/tutorials/create-a-crafting-bench/crystal-anvil-ingame.png)

![Crystal Anvil crafting UI showing the Crystal Sword recipe](/hytale-modding-docs/images/tutorials/create-a-crafting-bench/crystal-anvil-crafting-ui.png)

**Common errors and fixes:**

| Error | Cause | Fix |
|-------|-------|-----|
| Bench places but UI doesn't open | Missing `State` block | Add `"State": { "Id": "crafting", "Definitions": { "CraftCompleted": { "Looping": true }, "CraftCompletedInstant": {} } }` |
| Recipe not appearing in bench | `BenchRequirement.Id` mismatch | Ensure `Id` exactly matches `Bench.Id` (case-sensitive) |
| Category tab missing | Category `Id` not in bench definition | Add the category to the bench's `Categories` array |
| `StackOverflowError` on load | Using `Parent` inheritance with `State` | Make the bench standalone — copy all fields instead of inheriting from `Bench_Weapon` |
| Bench not placeable | Missing `Support` block | Add `"Support": { "Down": [{ "FaceType": "Full" }] }` |
| Common asset load error | Wrong asset path | Ensure assets are inside `Blocks/`, `BlockTextures/`, etc. — not `Animations/` or custom folders |

---

## Vanilla Bench Reference

For reference, here are the bench types used in the vanilla game:

| Bench | `Bench.Type` | `Bench.Id` | Categories |
|-------|-------------|------------|------------|
| Weapon Bench | `Crafting` | `Weapon_Bench` | Sword, Mace, Battleaxe, Daggers, Bow |
| Armory | `DiagramCrafting` | `Armory` | Weapons (Sword, Club, Axe, etc.), Armor (Head, Chest, etc.) |
| Campfire | `Crafting` | `Campfire` | Cooking |
| Workbench | `Crafting` | `Workbench` | Workbench_Crafting |

---

## Next Steps

- [Create a Custom Block](/hytale-modding-docs/tutorials/beginner/create-a-block) — learn how blocks and items connect
- [Custom Loot Tables](/hytale-modding-docs/tutorials/intermediate/custom-loot-tables) — set up drops that include your crafted items
- [NPC Shops and Trading](/hytale-modding-docs/tutorials/intermediate/npc-shops-and-trading) — sell bench-crafted items through NPC merchants
