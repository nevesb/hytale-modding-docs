---
title: Custom Trees and Saplings
description: Step-by-step tutorial for creating custom trees with sapling growth mechanics, multi-stage prefab progression, and farming integration.
---

## Goal

Create a custom **Crystalwood** tree that players can grow from a sapling. You will define the sapling item with farming stages, set up prefab references for each growth stage, and configure growth modifiers so the tree responds to water and fertilizer.

## What You'll Learn

- How sapling items use the `Farming` block type property for multi-stage growth
- How growth stages transition from block types to prefabs
- How `Duration`, `ReplaceMaskTags`, and `ActiveGrowthModifiers` control growth behaviour
- How to use `Parent` inheritance to create tree variants efficiently

## Prerequisites

- A mod folder with a valid `manifest.json` (see [Setup Your Dev Environment](/hytale-modding-docs/tutorials/beginner/setup-dev-environment))
- Familiarity with block and item definitions (see [Create a Custom Block](/hytale-modding-docs/tutorials/beginner/create-a-block))
- Tree prefab files created in the Hytale prefab editor (`.prefab.json` files)

---

## Growth System Overview

Hytale trees grow through a series of stages defined in the sapling's `BlockType.Farming` property. The first stage is a block (the sapling itself), and subsequent stages are prefabs (increasingly large tree models). Each stage has a duration range, and the engine automatically transitions between stages.

```
Sapling Block → Small Tree Prefab → Medium Tree Prefab → Full Tree Prefab
   Stage 0          Stage 1              Stage 2             Stage 3
```

The vanilla Oak sapling (`Plant_Sapling_Oak.json`) defines 6 growth stages, while the Birch sapling uses `Parent` inheritance to reuse most of the Oak's structure with different textures and prefabs.

---

## Step 1: Create the Sapling Item Definition

The sapling is an item that places a block with farming components. Create:

```
YourMod/Assets/Server/Item/Items/Plant/Plant_Sapling_Crystalwood.json
```

```json
{
  "TranslationProperties": {
    "Name": "server.items.Plant_Sapling_Crystalwood.name",
    "Description": "server.items.Plant_Sapling_Crystalwood.description"
  },
  "Icon": "Icons/MyMod/Plant_Crystalwood_Sapling.png",
  "Categories": [
    "Blocks.Plants"
  ],
  "Interactions": {
    "Primary": "Block_Primary",
    "Secondary": "Block_Secondary"
  },
  "ItemLevel": 5,
  "Recipe": {
    "TimeSeconds": 0,
    "Input": [
      {
        "ItemId": "Ingredient_Life_Essence",
        "Quantity": 12
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
        "Id": "Farmingbench",
        "Categories": [
          "Saplings"
        ],
        "RequiredTierLevel": 3
      }
    ]
  },
  "BlockType": {
    "DrawType": "Model",
    "CustomModel": "Blocks/Foliage/Tree/Sapling.blockymodel",
    "CustomModelTexture": [
      {
        "Texture": "Blocks/Foliage/Tree/Sapling_Textures/Crystalwood.png",
        "Weight": 1
      }
    ],
    "Group": "Wood",
    "HitboxType": "Plant_Large",
    "Flags": {},
    "RandomRotation": "YawStep1",
    "BlockEntity": {
      "Components": {
        "FarmingBlock": {}
      }
    },
    "Farming": {
      "Stages": {
        "Default": [
          {
            "Block": "Plant_Sapling_Crystalwood",
            "Duration": {
              "Min": 30000,
              "Max": 50000
            },
            "Type": "BlockType"
          },
          {
            "Prefabs": [
              {
                "Path": "Trees/Crystalwood/Stage_0/Crystalwood_Stage0_001.prefab.json",
                "Weight": 1
              }
            ],
            "Duration": {
              "Min": 40000,
              "Max": 60000
            },
            "Type": "Prefab",
            "ReplaceMaskTags": [
              "Soil"
            ],
            "SoundEventId": "SFX_Crops_Grow"
          },
          {
            "Prefabs": [
              {
                "Path": "Trees/Crystalwood/Stage_1/Crystalwood_Stage1_001.prefab.json",
                "Weight": 1
              }
            ],
            "Duration": {
              "Min": 40000,
              "Max": 60000
            },
            "Type": "Prefab",
            "ReplaceMaskTags": [
              "Soil"
            ],
            "SoundEventId": "SFX_Crops_Grow"
          },
          {
            "Prefabs": [
              {
                "Path": "Trees/Crystalwood/Stage_2/Crystalwood_Stage2_001.prefab.json",
                "Weight": 1
              },
              {
                "Path": "Trees/Crystalwood/Stage_2/Crystalwood_Stage2_002.prefab.json",
                "Weight": 1
              }
            ],
            "Duration": {
              "Min": 60000,
              "Max": 80000
            },
            "Type": "Prefab",
            "ReplaceMaskTags": [
              "Soil"
            ],
            "SoundEventId": "SFX_Crops_Grow"
          },
          {
            "Prefabs": [
              {
                "Path": "Trees/Crystalwood/Stage_3/Crystalwood_Stage3_001.prefab.json",
                "Weight": 1
              },
              {
                "Path": "Trees/Crystalwood/Stage_3/Crystalwood_Stage3_002.prefab.json",
                "Weight": 1
              }
            ],
            "Type": "Prefab",
            "ReplaceMaskTags": [
              "Soil"
            ],
            "SoundEventId": "SFX_Crops_Grow"
          }
        ]
      },
      "StartingStageSet": "Default",
      "ActiveGrowthModifiers": [
        "Fertilizer",
        "Water",
        "LightLevel"
      ]
    },
    "Gathering": {
      "Soft": {
        "ItemId": "Plant_Sapling_Crystalwood"
      }
    },
    "Support": {
      "Down": [
        {
          "TagId": "Type=Soil"
        }
      ]
    },
    "BlockParticleSetId": "Flower",
    "BlockSoundSetId": "Bush",
    "ParticleColor": "#44aacc"
  },
  "PlayerAnimationsId": "Item",
  "Tags": {
    "Type": [
      "Plant"
    ],
    "Family": [
      "Sapling"
    ]
  },
  "ItemSoundSetId": "ISS_Items_Foliage"
}
```

### Farming stages explained

The `Farming.Stages.Default` array defines each growth stage in order:

| Stage | Type | Purpose |
|-------|------|---------|
| 0 | `BlockType` | The sapling block itself. `Block` references this item's own block ID |
| 1-2 | `Prefab` | Small and medium tree prefabs placed as the tree grows |
| 3-4 | `Prefab` | Larger tree prefabs. The final stage has no `Duration` (it stays forever) |

### Key farming fields

| Field | Purpose |
|-------|---------|
| `Stages.Default[].Type` | `"BlockType"` for the initial sapling block, `"Prefab"` for tree model stages |
| `Stages.Default[].Block` | For `BlockType` stages: the block ID to place (usually the sapling itself) |
| `Stages.Default[].Prefabs` | For `Prefab` stages: array of prefab paths with weights for random selection |
| `Stages.Default[].Duration.Min` / `Max` | Time range in game ticks before advancing to the next stage. The engine picks a random value within the range |
| `Stages.Default[].ReplaceMaskTags` | Block tags that the prefab is allowed to replace when it grows. `"Soil"` lets roots push into dirt |
| `Stages.Default[].SoundEventId` | Sound played when the stage transition occurs |
| `StartingStageSet` | Which stage set to begin with. `"Default"` is standard |
| `ActiveGrowthModifiers` | Array of modifiers that affect growth speed: `"Fertilizer"` (compost), `"Water"` (rain/irrigation), `"LightLevel"` (sunlight) |

### Multiple prefab variants

When a stage has multiple entries in its `Prefabs` array, the engine picks one randomly based on `Weight`. This creates natural variety:

```json
"Prefabs": [
  {
    "Path": "Trees/Crystalwood/Stage_2/Crystalwood_Stage2_001.prefab.json",
    "Weight": 1
  },
  {
    "Path": "Trees/Crystalwood/Stage_2/Crystalwood_Stage2_002.prefab.json",
    "Weight": 1
  }
]
```

Equal weights give a 50/50 chance. Use different weights to make some variants rarer.

---

## Step 2: Create the Block Entity Component

The `BlockEntity.Components.FarmingBlock` object tells the engine this block uses the farming system. The empty object `{}` inherits default farming behaviour. The `Farming` property on the same `BlockType` provides the actual stage configuration.

```json
"BlockEntity": {
  "Components": {
    "FarmingBlock": {}
  }
}
```

This component is required. Without it, the `Farming` stages will be ignored.

---

## Step 3: Configure Block Support and Gathering

Two additional `BlockType` properties ensure the sapling behaves correctly:

### Support

```json
"Support": {
  "Down": [
    {
      "TagId": "Type=Soil"
    }
  ]
}
```

The sapling requires a block with the `Type=Soil` tag directly below it. If the soil is removed, the sapling breaks and drops itself.

### Gathering

```json
"Gathering": {
  "Soft": {
    "ItemId": "Plant_Sapling_Crystalwood"
  }
}
```

The `Soft` gathering type means players can break the sapling with any tool (or by hand) and receive the sapling item back.

---

## Step 4: Create a Variant Using Parent Inheritance

To create a colour variant of your tree without duplicating the entire file, use `Parent` inheritance. The Birch sapling in vanilla uses this exact pattern:

```
YourMod/Assets/Server/Item/Items/Plant/Plant_Sapling_Crystalwood_Red.json
```

```json
{
  "TranslationProperties": {
    "Name": "server.items.Plant_Sapling_Crystalwood_Red.name",
    "Description": "server.items.Plant_Sapling_Crystalwood_Red.description"
  },
  "Parent": "Plant_Sapling_Crystalwood",
  "Icon": "Icons/MyMod/Plant_Crystalwood_Red_Sapling.png",
  "ItemLevel": 6,
  "Recipe": {
    "TimeSeconds": 0,
    "Input": [
      {
        "ItemId": "Ingredient_Life_Essence",
        "Quantity": 18
      },
      {
        "ItemId": "Ingredient_Crystal_Cyan",
        "Quantity": 4
      }
    ],
    "OutputQuantity": 1,
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Id": "Farmingbench",
        "Categories": [
          "Saplings"
        ],
        "RequiredTierLevel": 4
      }
    ]
  },
  "BlockType": {
    "CustomModelTexture": [
      {
        "Texture": "Blocks/Foliage/Tree/Sapling_Textures/Crystalwood_Red.png",
        "Weight": 1
      }
    ],
    "Farming": {
      "Stages": {
        "Default": [
          {
            "Block": "Plant_Sapling_Crystalwood_Red",
            "Duration": {
              "Min": 30000,
              "Max": 50000
            },
            "Type": "BlockType"
          },
          {
            "Prefabs": [
              {
                "Path": "Trees/Crystalwood_Red/Stage_0/Crystalwood_Red_Stage0_001.prefab.json",
                "Weight": 1
              }
            ],
            "Duration": {
              "Min": 40000,
              "Max": 60000
            },
            "Type": "Prefab",
            "ReplaceMaskTags": [
              "Soil"
            ],
            "SoundEventId": "SFX_Crops_Grow"
          },
          {
            "Prefabs": [
              {
                "Path": "Trees/Crystalwood_Red/Stage_1/Crystalwood_Red_Stage1_001.prefab.json",
                "Weight": 1
              }
            ],
            "Type": "Prefab",
            "ReplaceMaskTags": [
              "Soil"
            ],
            "SoundEventId": "SFX_Crops_Grow"
          }
        ]
      },
      "StartingStageSet": "Default",
      "ActiveGrowthModifiers": [
        "Fertilizer",
        "Water",
        "LightLevel"
      ]
    },
    "Gathering": {
      "Soft": {
        "ItemId": "Plant_Sapling_Crystalwood_Red"
      }
    },
    "ParticleColor": "#cc4444"
  }
}
```

The `Parent` field inherits all properties from `Plant_Sapling_Crystalwood`. Only the fields you specify are overridden -- the model, hitbox, sound set, support rules, and other properties are all inherited automatically.

---

## Step 5: Add Translation Keys

```
YourMod/Assets/Languages/en-US.lang
```

```
server.items.Plant_Sapling_Crystalwood.name=Crystalwood Sapling
server.items.Plant_Sapling_Crystalwood.description=A sapling that grows into a tree with crystalline bark.
server.items.Plant_Sapling_Crystalwood_Red.name=Red Crystalwood Sapling
server.items.Plant_Sapling_Crystalwood_Red.description=A variant crystalwood sapling with crimson foliage.
```

---

## Step 6: Test In-Game

1. Place your mod folder in the server mods directory.
2. Start the server and watch for errors about missing prefab paths or unknown block IDs.
3. Use the developer item spawner to give yourself `Plant_Sapling_Crystalwood`.
4. Place the sapling on a dirt/soil block and confirm it renders correctly.
5. Wait for the first growth stage (or use time acceleration commands) and verify the sapling transitions to the first tree prefab.
6. Confirm each subsequent stage loads the correct prefab model.
7. Verify the final stage stays permanently (no `Duration` set).
8. Break the sapling before it grows and confirm you receive the sapling item back.
9. Test that removing the soil block beneath the sapling causes it to break.

**Common errors and fixes:**

| Error | Cause | Fix |
|-------|-------|-----|
| Sapling places but never grows | Missing `FarmingBlock` component | Add `"BlockEntity": { "Components": { "FarmingBlock": {} } }` |
| `Unknown prefab path` | Prefab file missing or wrong path | Verify `.prefab.json` files exist at the referenced paths |
| Sapling floats in air | Missing `Support` configuration | Add `"Support": { "Down": [{ "TagId": "Type=Soil" }] }` |
| Growth too fast or slow | `Duration` values need tuning | Vanilla uses 40000-60000 for most stages, 80000-100000 for late stages |
| Variant inherits wrong stages | `Parent` not overriding `Farming` | The variant must provide the complete `Farming.Stages` object to override stages |

---

## Next Steps

- [Create a Custom Block](/hytale-modding-docs/tutorials/beginner/create-a-block) -- understand block definitions that your tree prefabs contain
- [Custom Loot Tables](/hytale-modding-docs/tutorials/intermediate/custom-loot-tables) -- set up drops when players chop your custom trees
- [Create a Crafting Bench](/hytale-modding-docs/tutorials/intermediate/create-a-crafting-bench) -- build the Farming Bench where saplings are crafted
