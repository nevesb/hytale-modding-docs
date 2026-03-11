---
title: Create a Custom Item (Weapon)
description: Step-by-step tutorial for adding a custom weapon to Hytale, including item definition JSON, a crafting recipe, and translation keys.
---

## Goal

Add a custom dagger called the **Thornwood Dagger** to the game. You will create the item definition JSON with damage values and a crafting recipe, add translation keys for the name and description, and test it in-game.

## Prerequisites

- A mod folder with a valid `manifest.json` (see [Setup Your Dev Environment](/hytale-modding-docs/tutorials/beginner/setup-dev-environment))
- Blockbench installed for creating the 3D model (optional — you can reference a vanilla model to start)
- Familiarity with JSON (see [JSON Basics](/hytale-modding-docs/getting-started/json-basics))

---

## Step 1: Create the Item Model in Blockbench

Hytale uses the `.blockymodel` format for item 3D models. If you do not yet have Blockbench set up, skip this step and reference an existing vanilla model to get your item working first, then replace it later.

Vanilla dagger models live at paths like:

```
Items/Weapons/Dagger/Bronze.blockymodel
Items/Weapons/Dagger/Bronze_Texture.png
```

For your custom item, create and export:

```
YourMod/Assets/Common/Models/Items/Weapons/Dagger/Thornwood.blockymodel
YourMod/Assets/Common/Models/Items/Weapons/Dagger/Thornwood_Texture.png
```

**Blockbench tips:**
- Keep the model centred at the origin — Hytale uses the pivot point for hand positioning
- Export as **Hytale Blocky Model** using the Hytale plugin (see [Setup Your Dev Environment](/hytale-modding-docs/tutorials/beginner/setup-dev-environment))
- The texture file must be a PNG and its dimensions must be a power of two (e.g. 16x16, 32x32, 64x64)

---

## Step 2: Create the Item Definition JSON

Weapon item definitions follow the pattern established by files in `Assets/Server/Item/Items/Weapon/`. The bronze daggers file (`Weapon_Daggers_Bronze.json`) shows the structure: a `Parent` template handles shared behaviour while the child file overrides damage values, model paths, quality, and translation keys.

Create:

```
YourMod/Assets/Server/Item/Items/MyMod/Weapon_Daggers_Thornwood.json
```

```json
{
  "Parent": "Template_Weapon_Daggers",
  "TranslationProperties": {
    "Name": "server.items.Weapon_Daggers_Thornwood.name",
    "Description": "server.items.Weapon_Daggers_Thornwood.description"
  },
  "Model": "Items/Weapons/Dagger/Thornwood.blockymodel",
  "Texture": "Items/Weapons/Dagger/Thornwood_Texture.png",
  "Icon": "Icons/MyMod/Weapon_Daggers_Thornwood.png",
  "Quality": "Uncommon",
  "ItemLevel": 20,
  "MaxDurability": 80,
  "DurabilityLossOnHit": 0.5,
  "Tags": {
    "Type": ["Weapon"],
    "Family": ["Daggers"]
  },
  "InteractionVars": {
    "Swing_Left_Damage": {
      "Interactions": [
        {
          "Parent": "Weapon_Daggers_Primary_Swing_Left_Damage",
          "DamageCalculator": {
            "BaseDamage": {
              "Physical": 4
            }
          },
          "DamageEffects": {
            "WorldSoundEventId": "SFX_Daggers_T2_Slash_Impact",
            "LocalSoundEventId": "SFX_Daggers_T2_Slash_Impact"
          }
        }
      ]
    },
    "Swing_Right_Damage": {
      "Interactions": [
        {
          "Parent": "Weapon_Daggers_Primary_Swing_Right_Damage",
          "DamageCalculator": {
            "BaseDamage": {
              "Physical": 4
            }
          },
          "DamageEffects": {
            "WorldSoundEventId": "SFX_Daggers_T2_Slash_Impact",
            "LocalSoundEventId": "SFX_Daggers_T2_Slash_Impact"
          }
        }
      ]
    },
    "Stab_Left_Damage": {
      "Interactions": [
        {
          "Parent": "Weapon_Daggers_Primary_Stab_Left_Damage",
          "DamageCalculator": {
            "BaseDamage": {
              "Physical": 9
            }
          },
          "DamageEffects": {
            "WorldSoundEventId": "SFX_Daggers_T2_Slash_Impact",
            "LocalSoundEventId": "SFX_Daggers_T2_Slash_Impact"
          }
        }
      ]
    },
    "Stab_Right_Damage": {
      "Interactions": [
        {
          "Parent": "Weapon_Daggers_Primary_Stab_Right_Damage",
          "DamageCalculator": {
            "BaseDamage": {
              "Physical": 12
            }
          },
          "DamageEffects": {
            "WorldSoundEventId": "SFX_Daggers_T2_Slash_Impact",
            "LocalSoundEventId": "SFX_Daggers_T2_Slash_Impact"
          }
        }
      ]
    }
  }
}
```

### Key fields explained

| Field | Purpose |
|-------|---------|
| `Parent` | Inherits all attack animations, interactions, and base stats from the template |
| `TranslationProperties` | Keys resolved from your `.lang` file for the item name and tooltip |
| `Model` | Path to the `.blockymodel` file |
| `Texture` | Path to the model's texture PNG |
| `Icon` | Inventory slot icon PNG |
| `Quality` | Rarity tier — controls border colour and drop particle. Valid values: `Junk`, `Common`, `Uncommon`, `Rare`, `Epic`, `Legendary` |
| `ItemLevel` | Determines progression tier; affects loot table weighting |
| `MaxDurability` | How many hits before the item breaks |
| `DurabilityLossOnHit` | Durability subtracted per hit (supports decimals) |
| `InteractionVars` | Override specific attack damage values from the parent template |

### Damage calculator

Each `InteractionVars` entry overrides one attack phase. `BaseDamage` takes a damage type key:

| Damage type | Description |
|-------------|-------------|
| `Physical` | Standard melee damage |
| `Fire` | Elemental fire damage |
| `Poison` | Applies a damage-over-time effect |
| `Ice` | Cold damage |

You can combine types in one hit:

```json
"BaseDamage": {
  "Physical": 4,
  "Poison": 2
}
```

---

## Step 3: Add a Crafting Recipe

Recipes can be defined inline inside the item JSON (as seen in `Food_Bread.json`) or in a separate recipe file. Inline is simpler for one-off items. Add a `Recipe` block to your item definition:

```json
{
  "Parent": "Template_Weapon_Daggers",
  "TranslationProperties": {
    "Name": "server.items.Weapon_Daggers_Thornwood.name",
    "Description": "server.items.Weapon_Daggers_Thornwood.description"
  },
  "Model": "Items/Weapons/Dagger/Thornwood.blockymodel",
  "Texture": "Items/Weapons/Dagger/Thornwood_Texture.png",
  "Icon": "Icons/MyMod/Weapon_Daggers_Thornwood.png",
  "Quality": "Uncommon",
  "ItemLevel": 20,
  "MaxDurability": 80,
  "DurabilityLossOnHit": 0.5,
  "Tags": {
    "Type": ["Weapon"],
    "Family": ["Daggers"]
  },
  "Recipe": {
    "Input": [
      {
        "ResourceTypeId": "Wood_Trunk",
        "Quantity": 3
      },
      {
        "ItemId": "Ingredient_Fibre",
        "Quantity": 2
      },
      {
        "ItemId": "Ingredient_Bar_Copper",
        "Quantity": 1
      }
    ],
    "Output": [
      {
        "ItemId": "Weapon_Daggers_Thornwood"
      }
    ],
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Categories": ["Weapon_Daggers"],
        "Id": "Weapon_Bench"
      }
    ],
    "TimeSeconds": 4
  },
  "InteractionVars": {
    "Swing_Left_Damage": {
      "Interactions": [
        {
          "Parent": "Weapon_Daggers_Primary_Swing_Left_Damage",
          "DamageCalculator": {
            "BaseDamage": {
              "Physical": 4
            }
          },
          "DamageEffects": {
            "WorldSoundEventId": "SFX_Daggers_T2_Slash_Impact",
            "LocalSoundEventId": "SFX_Daggers_T2_Slash_Impact"
          }
        }
      ]
    },
    "Swing_Right_Damage": {
      "Interactions": [
        {
          "Parent": "Weapon_Daggers_Primary_Swing_Right_Damage",
          "DamageCalculator": {
            "BaseDamage": {
              "Physical": 4
            }
          },
          "DamageEffects": {
            "WorldSoundEventId": "SFX_Daggers_T2_Slash_Impact",
            "LocalSoundEventId": "SFX_Daggers_T2_Slash_Impact"
          }
        }
      ]
    },
    "Stab_Left_Damage": {
      "Interactions": [
        {
          "Parent": "Weapon_Daggers_Primary_Stab_Left_Damage",
          "DamageCalculator": {
            "BaseDamage": {
              "Physical": 9
            }
          },
          "DamageEffects": {
            "WorldSoundEventId": "SFX_Daggers_T2_Slash_Impact",
            "LocalSoundEventId": "SFX_Daggers_T2_Slash_Impact"
          }
        }
      ]
    },
    "Stab_Right_Damage": {
      "Interactions": [
        {
          "Parent": "Weapon_Daggers_Primary_Stab_Right_Damage",
          "DamageCalculator": {
            "BaseDamage": {
              "Physical": 12
            }
          },
          "DamageEffects": {
            "WorldSoundEventId": "SFX_Daggers_T2_Slash_Impact",
            "LocalSoundEventId": "SFX_Daggers_T2_Slash_Impact"
          }
        }
      ]
    }
  }
}
```

### Recipe fields

| Field | Purpose |
|-------|---------|
| `Input` | List of required ingredients. Use `ItemId` for a specific item, or `ResourceTypeId` for a resource category (e.g. any wood log counts as `Wood_Trunk`) |
| `Output` | What the player receives. Omitting `Quantity` defaults to 1 |
| `BenchRequirement` | Which crafting station is needed. `Id` is the bench identifier; `Categories` filters which bench tab it appears in |
| `TimeSeconds` | How long the craft takes |
| `KnowledgeRequired` | Set to `true` if the recipe must be learned from a scroll before appearing |

---

## Step 4: Add Translation Keys

Create or append to your mod's language file:

```
YourMod/Assets/Languages/en-US.lang
```

```
server.items.Weapon_Daggers_Thornwood.name=Thornwood Dagger
server.items.Weapon_Daggers_Thornwood.description=A light blade carved from thornwood. Fast and precise.
```

Translation key format used throughout vanilla: `server.items.<ItemId>.name` and `server.items.<ItemId>.description`. Match this pattern exactly — the engine is case-sensitive.

---

## Step 5: Test In-Game

1. Copy your mod folder into the server mods directory.
2. Start the server and check the console for errors referencing your item file.
3. Use the developer item spawner to give yourself `Weapon_Daggers_Thornwood`.
4. Confirm the model, texture, icon, and name display correctly.
5. Attack a training dummy or critter to verify damage numbers match your `BaseDamage` values.
6. Check the Weapon Bench recipe list for your item.

**Common errors and fixes:**

| Error | Cause | Fix |
|-------|-------|-----|
| `Unknown parent: Template_Weapon_Daggers` | Template not loaded | Ensure vanilla assets are present |
| Model appears as default cube | Wrong `.blockymodel` path | Double-check the `Model` path |
| Recipe not appearing at bench | Wrong `BenchRequirement.Id` | Use `Weapon_Bench` exactly |
| Name shows raw key | Missing `.lang` entry | Add the key to `en-US.lang` |

---

## Complete Files

### `YourMod/Assets/Server/Item/Items/MyMod/Weapon_Daggers_Thornwood.json`
```json
{
  "Parent": "Template_Weapon_Daggers",
  "TranslationProperties": {
    "Name": "server.items.Weapon_Daggers_Thornwood.name",
    "Description": "server.items.Weapon_Daggers_Thornwood.description"
  },
  "Model": "Items/Weapons/Dagger/Thornwood.blockymodel",
  "Texture": "Items/Weapons/Dagger/Thornwood_Texture.png",
  "Icon": "Icons/MyMod/Weapon_Daggers_Thornwood.png",
  "Quality": "Uncommon",
  "ItemLevel": 20,
  "MaxDurability": 80,
  "DurabilityLossOnHit": 0.5,
  "Tags": {
    "Type": ["Weapon"],
    "Family": ["Daggers"]
  },
  "Recipe": {
    "Input": [
      {
        "ResourceTypeId": "Wood_Trunk",
        "Quantity": 3
      },
      {
        "ItemId": "Ingredient_Fibre",
        "Quantity": 2
      },
      {
        "ItemId": "Ingredient_Bar_Copper",
        "Quantity": 1
      }
    ],
    "Output": [
      {
        "ItemId": "Weapon_Daggers_Thornwood"
      }
    ],
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Categories": ["Weapon_Daggers"],
        "Id": "Weapon_Bench"
      }
    ],
    "TimeSeconds": 4
  },
  "InteractionVars": {
    "Swing_Left_Damage": {
      "Interactions": [
        {
          "Parent": "Weapon_Daggers_Primary_Swing_Left_Damage",
          "DamageCalculator": {
            "BaseDamage": { "Physical": 4 }
          },
          "DamageEffects": {
            "WorldSoundEventId": "SFX_Daggers_T2_Slash_Impact",
            "LocalSoundEventId": "SFX_Daggers_T2_Slash_Impact"
          }
        }
      ]
    },
    "Swing_Right_Damage": {
      "Interactions": [
        {
          "Parent": "Weapon_Daggers_Primary_Swing_Right_Damage",
          "DamageCalculator": {
            "BaseDamage": { "Physical": 4 }
          },
          "DamageEffects": {
            "WorldSoundEventId": "SFX_Daggers_T2_Slash_Impact",
            "LocalSoundEventId": "SFX_Daggers_T2_Slash_Impact"
          }
        }
      ]
    },
    "Stab_Left_Damage": {
      "Interactions": [
        {
          "Parent": "Weapon_Daggers_Primary_Stab_Left_Damage",
          "DamageCalculator": {
            "BaseDamage": { "Physical": 9 }
          },
          "DamageEffects": {
            "WorldSoundEventId": "SFX_Daggers_T2_Slash_Impact",
            "LocalSoundEventId": "SFX_Daggers_T2_Slash_Impact"
          }
        }
      ]
    },
    "Stab_Right_Damage": {
      "Interactions": [
        {
          "Parent": "Weapon_Daggers_Primary_Stab_Right_Damage",
          "DamageCalculator": {
            "BaseDamage": { "Physical": 12 }
          },
          "DamageEffects": {
            "WorldSoundEventId": "SFX_Daggers_T2_Slash_Impact",
            "LocalSoundEventId": "SFX_Daggers_T2_Slash_Impact"
          }
        }
      ]
    }
  }
}
```

### `YourMod/Assets/Languages/en-US.lang`
```
server.items.Weapon_Daggers_Thornwood.name=Thornwood Dagger
server.items.Weapon_Daggers_Thornwood.description=A light blade carved from thornwood. Fast and precise.
```

---

## Next Steps

- [Create a Custom Block](/hytale-modding-docs/tutorials/beginner/create-a-block) — add a placeable block that drops from NPCs
- [Create a Custom NPC](/hytale-modding-docs/tutorials/beginner/create-an-npc) — create a creature that drops your new weapon
- [JSON Basics](/hytale-modding-docs/getting-started/json-basics) — reference for template inheritance and interaction chaining
