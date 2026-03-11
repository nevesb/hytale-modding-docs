---
title: Create a Custom Crafting Bench
description: Step-by-step tutorial for adding a custom crafting bench with recipe categories, tier upgrades, and item recipes that use it.
---

## Goal

Build a custom **Runecrafting Bench** that players can place in the world and use to craft magical items. You will define the bench item with crafting categories, set up tier-based upgrades, and create item recipes that require the bench.

## What You'll Learn

- How crafting benches are defined using the `Bench` block type property
- How to create categories that organise recipes within the bench UI
- How tier levels unlock progressively harder recipes
- How item recipes reference a bench via `BenchRequirement`

## Prerequisites

- A mod folder with a valid `manifest.json` (see [Setup Your Dev Environment](/hytale-modding-docs/tutorials/beginner/setup-dev-environment))
- Familiarity with block definitions (see [Create a Custom Block](/hytale-modding-docs/tutorials/beginner/create-a-block))
- Familiarity with item definitions (see [Create a Custom Item](/hytale-modding-docs/tutorials/beginner/create-an-item))

---

## Step 1: Create the Bench Item Definition

Crafting benches in Hytale are items with a `BlockType` that contains a `Bench` object. The `Bench` object defines the bench's type, unique ID, categories, and tier levels. The vanilla Farming Bench (`Bench_Farming.json`) and Weapon Bench (`Bench_Weapon.json`) both follow this pattern.

Create your bench definition at:

```
YourMod/Assets/Server/Item/Items/Bench/Bench_Runecrafting.json
```

```json
{
  "TranslationProperties": {
    "Name": "server.items.Bench_Runecrafting.name",
    "Description": "server.items.Bench_Runecrafting.description"
  },
  "Icon": "Icons/ItemsGenerated/Bench_Runecrafting.png",
  "Categories": [
    "Furniture.Benches"
  ],
  "MaxStack": 1,
  "ItemLevel": 4,
  "BlockType": {
    "Material": "Solid",
    "DrawType": "Model",
    "Opacity": "Transparent",
    "CustomModel": "Blocks/Benches/Runecrafting.blockymodel",
    "CustomModelTexture": [
      {
        "Texture": "Blocks/Benches/Runecrafting_Texture.png",
        "Weight": 1
      }
    ],
    "HitboxType": "Bench_Runecrafting",
    "VariantRotation": "NESW",
    "Bench": {
      "Type": "Crafting",
      "Id": "Runecraftingbench",
      "Categories": [
        {
          "Id": "Runes",
          "Icon": "Icons/CraftingCategories/Runecrafting/Runes.png",
          "Name": "server.benchCategories.runecraftingbench.runes"
        },
        {
          "Id": "Enchantments",
          "Icon": "Icons/CraftingCategories/Runecrafting/Enchantments.png",
          "Name": "server.benchCategories.runecraftingbench.enchantments"
        },
        {
          "Id": "Scrolls",
          "Icon": "Icons/CraftingCategories/Runecrafting/Scrolls.png",
          "Name": "server.benchCategories.runecraftingbench.scrolls"
        }
      ],
      "LocalOpenSoundEventId": "SFX_Bench_Placeholder",
      "LocalCloseSoundEventId": "SFX_Bench_Placeholder",
      "CompletedSoundEventId": "SFX_Bench_Placeholder",
      "BenchUpgradeSoundEventId": "SFX_Workbench_Upgrade_Start_Default",
      "BenchUpgradeCompletedSoundEventId": "SFX_Workbench_Upgrade_Complete_Default",
      "TierLevels": [
        {
          "CraftingTimeReductionModifier": 0.0,
          "UpgradeRequirement": {
            "Material": [
              {
                "ItemId": "Ingredient_Crystal_Cyan",
                "Quantity": 10
              },
              {
                "ItemId": "Ingredient_Bar_Iron",
                "Quantity": 5
              }
            ],
            "TimeSeconds": 3
          }
        },
        {
          "CraftingTimeReductionModifier": 0.15,
          "UpgradeRequirement": {
            "Material": [
              {
                "ItemId": "Ingredient_Crystal_Cyan",
                "Quantity": 25
              },
              {
                "ItemId": "Ingredient_Bar_Thorium",
                "Quantity": 10
              }
            ],
            "TimeSeconds": 3
          }
        },
        {
          "CraftingTimeReductionModifier": 0.3
        }
      ]
    },
    "State": {
      "Id": "crafting",
      "Definitions": {
        "CraftCompleted": {}
      }
    },
    "Gathering": {
      "Breaking": {
        "GatherType": "Benches"
      }
    },
    "BlockParticleSetId": "Stone",
    "ParticleColor": "#4488cc",
    "Support": {
      "Down": [
        {
          "FaceType": "Full"
        }
      ]
    },
    "BlockSoundSetId": "Stone"
  },
  "Recipe": {
    "TimeSeconds": 3,
    "Input": [
      {
        "ResourceTypeId": "Rock",
        "Quantity": 10
      },
      {
        "ItemId": "Ingredient_Crystal_Cyan",
        "Quantity": 5
      }
    ],
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Id": "Workbench",
        "Categories": [
          "Workbench_Crafting"
        ]
      }
    ]
  },
  "PlayerAnimationsId": "Block",
  "Tags": {
    "Type": [
      "Bench"
    ]
  },
  "ItemSoundSetId": "ISS_Blocks_Wood"
}
```

### Key bench fields explained

| Field | Purpose |
|-------|---------|
| `Bench.Type` | Must be `"Crafting"` for recipe-based benches |
| `Bench.Id` | Unique identifier that recipes reference in their `BenchRequirement`. This is the string that connects recipes to this bench |
| `Bench.Categories` | Array of category tabs shown in the bench UI. Each has an `Id`, `Icon`, and translation `Name` |
| `Bench.TierLevels` | Array of upgrade tiers. Each tier can have a `CraftingTimeReductionModifier` (percentage faster) and an `UpgradeRequirement` with materials and time |
| `VariantRotation` | `"NESW"` lets the bench face four directions when placed |
| `State` | Defines visual states like `CraftCompleted` for animations while crafting |

### Category structure

Each category in the `Categories` array is an object with three fields:

```json
{
  "Id": "Runes",
  "Icon": "Icons/CraftingCategories/Runecrafting/Runes.png",
  "Name": "server.benchCategories.runecraftingbench.runes"
}
```

- **`Id`** -- The category identifier that recipes reference to appear under this tab
- **`Icon`** -- Path to the icon PNG displayed on the category tab
- **`Name`** -- Translation key for the category label text

---

## Step 2: Create Recipes That Use the Bench

Any item definition with a `Recipe` block can reference your bench. The connection is made through the `BenchRequirement` array, where `Id` matches your bench's `Bench.Id` and `Categories` lists which category tabs the recipe appears under.

Create an item that is crafted at the Runecrafting Bench:

```
YourMod/Assets/Server/Item/Items/Rune/Rune_Fire.json
```

```json
{
  "TranslationProperties": {
    "Name": "server.items.Rune_Fire.name",
    "Description": "server.items.Rune_Fire.description"
  },
  "Icon": "Icons/MyMod/Rune_Fire.png",
  "Quality": "Rare",
  "MaxStack": 16,
  "ItemLevel": 3,
  "Recipe": {
    "TimeSeconds": 5,
    "Input": [
      {
        "ItemId": "Ingredient_Fire_Essence",
        "Quantity": 3
      },
      {
        "ItemId": "Ingredient_Crystal_Cyan",
        "Quantity": 2
      }
    ],
    "OutputQuantity": 1,
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Id": "Runecraftingbench",
        "Categories": [
          "Runes"
        ],
        "RequiredTierLevel": 1
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
| `RequiredTierLevel` | Minimum bench tier required. Tier levels are 1-indexed from the `TierLevels` array. Omit for tier 0 (no upgrade needed) |

---

## Step 3: Add a Tier-Gated Recipe

To create a recipe that only unlocks after the player upgrades their bench, set `RequiredTierLevel` to a higher value:

```
YourMod/Assets/Server/Item/Items/Rune/Rune_Void.json
```

```json
{
  "TranslationProperties": {
    "Name": "server.items.Rune_Void.name",
    "Description": "server.items.Rune_Void.description"
  },
  "Icon": "Icons/MyMod/Rune_Void.png",
  "Quality": "Epic",
  "MaxStack": 8,
  "ItemLevel": 6,
  "Recipe": {
    "TimeSeconds": 10,
    "Input": [
      {
        "ItemId": "Ingredient_Void_Essence",
        "Quantity": 5
      },
      {
        "ItemId": "Ingredient_Crystal_Cyan",
        "Quantity": 8
      }
    ],
    "OutputQuantity": 1,
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Id": "Runecraftingbench",
        "Categories": [
          "Runes"
        ],
        "RequiredTierLevel": 2
      }
    ]
  }
}
```

This recipe appears greyed out until the player upgrades the Runecrafting Bench to tier 2.

---

## Step 4: Add Translation Keys

Add all translation keys to your language file:

```
YourMod/Assets/Languages/en-US.lang
```

```
server.items.Bench_Runecrafting.name=Runecrafting Bench
server.items.Bench_Runecrafting.description=A bench for crafting runes and enchantments.
server.benchCategories.runecraftingbench.runes=Runes
server.benchCategories.runecraftingbench.enchantments=Enchantments
server.benchCategories.runecraftingbench.scrolls=Scrolls
server.items.Rune_Fire.name=Fire Rune
server.items.Rune_Fire.description=A rune imbued with the essence of fire.
server.items.Rune_Void.name=Void Rune
server.items.Rune_Void.description=A rune channelling void energy.
```

---

## Step 5: Test In-Game

1. Place your mod folder in the server mods directory.
2. Start the server and watch for JSON validation errors.
3. Use the developer item spawner to give yourself `Bench_Runecrafting`.
4. Place the bench and right-click to open the crafting UI.
5. Confirm all three category tabs (Runes, Enchantments, Scrolls) appear.
6. Verify `Rune_Fire` appears under the Runes tab and can be crafted.
7. Confirm `Rune_Void` appears greyed out until you upgrade the bench to tier 2.
8. Upgrade the bench by providing the required materials and verify the tier 2 recipe unlocks.

**Common errors and fixes:**

| Error | Cause | Fix |
|-------|-------|-----|
| Recipe not appearing in bench | `BenchRequirement.Id` mismatch | Ensure `Id` exactly matches `Bench.Id` (case-sensitive) |
| Category tab missing | Category `Id` not in bench definition | Add the category to the bench's `Categories` array |
| Recipe always greyed out | `RequiredTierLevel` too high | Check that tier level exists in the bench's `TierLevels` array |
| Bench not placeable | Missing `Support` block | Add `"Support": { "Down": [{ "FaceType": "Full" }] }` |

---

## Next Steps

- [Create a Custom Block](/hytale-modding-docs/tutorials/beginner/create-a-block) -- learn how blocks and items connect
- [Custom Loot Tables](/hytale-modding-docs/tutorials/intermediate/custom-loot-tables) -- set up drops that include your crafted items
- [NPC Shops and Trading](/hytale-modding-docs/tutorials/intermediate/npc-shops-and-trading) -- sell bench-crafted items through NPC merchants
