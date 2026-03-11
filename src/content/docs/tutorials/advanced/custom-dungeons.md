---
title: Create Custom Dungeon Instances
description: How to create custom dungeon instances with prefabs, portals, gameplay configs, loot tables, and NPC encounters.
---

## Goal

Build a complete custom dungeon instance called the **Sunken Vault** — a self-contained instanced area that players enter through a portal, fight through NPC encounters, collect loot from containers, and exit upon death or completion. You will create a gameplay config for the instance, define portal entry and exit points, configure dungeon loot tables, and wire up NPC spawns inside the instance.

## Prerequisites

- A mod folder with a valid `manifest.json` (see [Setup Your Dev Environment](/hytale-modding-docs/tutorials/beginner/setup-dev-environment))
- Familiarity with JSON template inheritance (see [Inheritance and Templates](/hytale-modding-docs/reference/concepts/inheritance-and-templates))
- Understanding of NPC roles and spawn rules (see [Create a Custom NPC](/hytale-modding-docs/tutorials/beginner/create-an-npc))
- Understanding of drop tables (see [Drop Tables](/hytale-modding-docs/reference/economy-and-progression/drop-tables))

---

## How Instances Work

Hytale instances are isolated world zones with their own gameplay rules. When a player enters a portal linked to an instance, the engine creates (or reuses) a copy of that instance and teleports the player into it. Instances have their own gameplay config that can override death penalties, block interaction, and respawn behaviour independently from the overworld.

Key components:

| Component | File Location | Purpose |
|-----------|--------------|---------|
| Gameplay Config | `Server/GameplayConfigs/` | Rules for death, block breaking, respawn inside the instance |
| Portal Type | `Server/PortalTypes/` | Defines the portal block that transports players into the instance |
| Environment | `Server/Environments/` | Weather and atmosphere inside the instance |
| NPC Spawn Rules | `Server/NPC/Spawn/` | Which NPCs appear inside the instance |
| Drop Tables | `Server/Drops/` | Loot from containers and NPCs in the instance |

---

## Step 1: Create the Instance Gameplay Config

Instance gameplay configs inherit from `Default_Instance` which disables block breaking and prevents item loss on death. The player is ejected from the instance when they die.

Create `YourMod/Assets/Server/GameplayConfigs/SunkenVault.json`:

```json
{
  "Parent": "Default_Instance",
  "World": {
    "AllowBlockBreaking": false,
    "AllowBlockGathering": false,
    "DaytimeDurationSeconds": 0,
    "NighttimeDurationSeconds": 0
  },
  "Death": {
    "LoseItems": false,
    "RespawnController": {
      "Type": "ExitInstance"
    }
  },
  "Player": {
    "MovementConfig": "Default",
    "HitboxCollisionConfig": "SoftCollision",
    "ArmorVisibilityOption": "All"
  }
}
```

### Config fields explained

| Field | Purpose |
|-------|---------|
| `Parent` | Inherits all defaults from `Default_Instance`, which already disables block interaction |
| `AllowBlockBreaking` | Prevents players from destroying the dungeon structure |
| `AllowBlockGathering` | Prevents resource gathering inside the dungeon |
| `DaytimeDurationSeconds: 0` | Freezes the day/night cycle so the dungeon has a fixed lighting state |
| `LoseItems: false` | Players keep all items when dying inside the instance |
| `RespawnController.Type: "ExitInstance"` | Dying ejects the player back to the overworld portal location |

Compare to the vanilla `Default_Instance.json` which uses the same pattern. Your config adds the frozen time cycle and explicit player settings.

---

## Step 2: Create the Instance Environment

The instance environment controls weather and atmosphere. For a dungeon, you typically want a single static weather with no variation.

Create `YourMod/Assets/Server/Environments/SunkenVault.json`:

```json
{
  "WaterTint": "#0a3d6b",
  "SpawnDensity": 0.8,
  "Tags": {
    "Dungeon": [],
    "SunkenVault": []
  },
  "WeatherForecasts": {
    "0":  [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "1":  [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "2":  [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "3":  [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "4":  [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "5":  [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "6":  [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "7":  [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "8":  [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "9":  [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "10": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "11": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "12": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "13": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "14": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "15": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "16": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "17": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "18": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "19": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "20": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "21": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "22": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "23": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }]
  }
}
```

Using a single weather ID at weight 100 for every hour creates a constant atmosphere. The `WaterTint` gives underground water a dark blue-green tint appropriate for a sunken dungeon. `SpawnDensity` at `0.8` slightly reduces ambient NPC spawns compared to the overworld default of `0.5` (higher values mean more spawns in instanced content where encounters are controlled).

---

## Step 3: Define the Portal Type

Portal types define the block that players interact with to enter the instance. The portal references the gameplay config and environment you created.

Create `YourMod/Assets/Server/PortalTypes/Portal_SunkenVault.json`:

```json
{
  "InstanceType": "SunkenVault",
  "GameplayConfig": "SunkenVault",
  "Environment": "SunkenVault",
  "MaxPlayers": 4,
  "PortalAppearance": "Portal_Dungeon",
  "SpawnOffset": {
    "X": 0,
    "Y": 1,
    "Z": 3
  },
  "ExitOffset": {
    "X": 0,
    "Y": 1,
    "Z": -3
  },
  "CooldownSeconds": 30,
  "RequiredItemToEnter": "Key_SunkenVault",
  "ConsumeRequiredItem": true
}
```

### Portal fields explained

| Field | Purpose |
|-------|---------|
| `InstanceType` | Unique identifier for this instance type. Must match across all related config files |
| `GameplayConfig` | References the gameplay config file ID (filename without `.json`) |
| `Environment` | References the environment file ID |
| `MaxPlayers` | Maximum concurrent players allowed in one instance copy |
| `PortalAppearance` | Client-side visual for the portal block |
| `SpawnOffset` | Where players appear relative to the instance origin when entering |
| `ExitOffset` | Where players appear relative to the overworld portal when exiting |
| `CooldownSeconds` | Minimum seconds before a player can re-enter after exiting |
| `RequiredItemToEnter` | Item ID the player must have in inventory to use the portal |
| `ConsumeRequiredItem` | Whether the required item is consumed on entry |

To create a portal without a key requirement, omit both `RequiredItemToEnter` and `ConsumeRequiredItem`.

---

## Step 4: Create Dungeon Loot Tables

Dungeons need loot tables for treasure containers placed inside the instance. Use the `Multiple` and `Choice` container types to create varied loot pools.

Create `YourMod/Assets/Server/Drops/Items/SunkenVault_Chest.json`:

```json
{
  "Container": {
    "Type": "Multiple",
    "Containers": [
      {
        "Type": "Choice",
        "Containers": [
          {
            "Type": "Single",
            "Weight": 60,
            "Item": {
              "ItemId": "Weapon_Sword_Copper",
              "QuantityMin": 1,
              "QuantityMax": 1
            }
          },
          {
            "Type": "Single",
            "Weight": 30,
            "Item": {
              "ItemId": "Weapon_Sword_Iron",
              "QuantityMin": 1,
              "QuantityMax": 1
            }
          },
          {
            "Type": "Single",
            "Weight": 10,
            "Item": {
              "ItemId": "Weapon_Sword_Gold",
              "QuantityMin": 1,
              "QuantityMax": 1
            }
          }
        ]
      },
      {
        "Type": "Choice",
        "Containers": [
          {
            "Type": "Single",
            "Weight": 70,
            "Item": {
              "ItemId": "Food_Bread",
              "QuantityMin": 2,
              "QuantityMax": 5
            }
          },
          {
            "Type": "Empty",
            "Weight": 30
          }
        ]
      },
      {
        "Type": "Choice",
        "Containers": [
          {
            "Type": "Single",
            "Weight": 50,
            "Item": {
              "ItemId": "Weapon_Arrow_Crude",
              "QuantityMin": 5,
              "QuantityMax": 15
            }
          },
          {
            "Type": "Empty",
            "Weight": 50
          }
        ]
      }
    ]
  }
}
```

This loot table uses a `Multiple` root to evaluate three independent pools:

1. **Weapon pool** (guaranteed) — always drops one weapon, weighted toward lower tiers
2. **Food pool** (70% chance) — sometimes includes bread for healing
3. **Ammo pool** (50% chance) — sometimes includes arrows

The `Empty` type with its own weight creates the possibility of no drop from that pool. Compare this pattern to the vanilla `Barrels.json` which uses `Empty` at weight 800 to make drops rare.

Create a boss-tier loot table for the final room:

`YourMod/Assets/Server/Drops/Items/SunkenVault_BossChest.json`:

```json
{
  "Container": {
    "Type": "Multiple",
    "Containers": [
      {
        "Type": "Choice",
        "Weight": 100,
        "Containers": [
          {
            "Type": "Single",
            "Item": {
              "ItemId": "Weapon_Sword_Gold",
              "QuantityMin": 1,
              "QuantityMax": 1
            }
          }
        ]
      },
      {
        "Type": "Choice",
        "Weight": 100,
        "Containers": [
          {
            "Type": "Single",
            "Item": {
              "ItemId": "Ingredient_Crystal",
              "QuantityMin": 3,
              "QuantityMax": 8
            }
          }
        ]
      },
      {
        "Type": "Choice",
        "Weight": 100,
        "Containers": [
          {
            "Type": "Single",
            "Item": {
              "ItemId": "Food_Bread",
              "QuantityMin": 5,
              "QuantityMax": 10
            }
          }
        ]
      }
    ]
  }
}
```

---

## Step 5: Create Dungeon NPC Encounters

Define NPCs that spawn inside the dungeon. Instance NPCs typically use aggressive templates with higher health than their overworld counterparts.

Create `YourMod/Assets/Server/NPC/Roles/MyMod/SunkenVault_Guardian.json`:

```json
{
  "Type": "Variant",
  "Reference": "Template_Intelligent",
  "Modify": {
    "Appearance": "Skeleton_Warrior",
    "DropList": "Drop_SunkenVault_Guardian",
    "MaxHealth": 120,
    "MaxSpeed": 6,
    "ViewRange": 18,
    "HearingRange": 14,
    "AlertedRange": 24,
    "DefaultPlayerAttitude": "Hostile",
    "IsMemory": true,
    "MemoriesCategory": "Undead",
    "MemoriesNameOverride": "Vault Guardian",
    "NameTranslationKey": {
      "Compute": "NameTranslationKey"
    }
  },
  "Parameters": {
    "NameTranslationKey": {
      "Value": "server.npcRoles.SunkenVault_Guardian.name",
      "Description": "Translation key for NPC name display"
    }
  }
}
```

Create the guardian's drop table at `YourMod/Assets/Server/Drops/NPCs/Intelligent/Drop_SunkenVault_Guardian.json`:

```json
{
  "Container": {
    "Type": "Multiple",
    "Containers": [
      {
        "Type": "Choice",
        "Weight": 100,
        "Containers": [
          {
            "Type": "Single",
            "Item": {
              "ItemId": "Ingredient_Bone",
              "QuantityMin": 1,
              "QuantityMax": 3
            }
          }
        ]
      },
      {
        "Type": "Choice",
        "Containers": [
          {
            "Type": "Single",
            "Weight": 15,
            "Item": {
              "ItemId": "Ingredient_Crystal",
              "QuantityMin": 1,
              "QuantityMax": 1
            }
          },
          {
            "Type": "Empty",
            "Weight": 85
          }
        ]
      }
    ]
  }
}
```

---

## Step 6: Create Instance Spawn Rules

Instance spawn rules work like overworld spawns but reference the instance environment. Create spawn rules for the Sunken Vault's guardian NPCs.

Create `YourMod/Assets/Server/NPC/Spawn/Instance/Spawns_SunkenVault.json`:

```json
{
  "Environments": [
    "SunkenVault"
  ],
  "NPCs": [
    {
      "Weight": 8,
      "SpawnBlockSet": "Soil",
      "Id": "SunkenVault_Guardian",
      "Flock": "Group_Small"
    }
  ],
  "DayTimeRange": [0, 24]
}
```

Setting `DayTimeRange` to `[0, 24]` ensures guardians spawn regardless of time, which is important because the instance has a frozen time cycle. The `Flock: "Group_Small"` spawns guardians in small groups of 2-4, creating meaningful encounters.

---

## Step 7: Add Translation Keys

Create `YourMod/Assets/Languages/en-US.lang` (or append to your existing file):

```
server.npcRoles.SunkenVault_Guardian.name=Vault Guardian
```

---

## Step 8: Test the Dungeon

1. Place your mod folder in the server mods directory.
2. Start the server and check the console for errors about missing references.
3. Place the portal block in the overworld using the developer tools.
4. Enter the portal and verify you are transported to the instance.
5. Confirm NPCs spawn and have hostile behaviour.
6. Open a loot container and verify drops match your loot table.
7. Die inside the instance and confirm you are ejected to the overworld without losing items.

### Common errors and fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `Unknown gameplay config: SunkenVault` | Config file not found | Verify file is at `GameplayConfigs/SunkenVault.json` |
| `Unknown environment: SunkenVault` | Environment ID mismatch | Ensure environment filename matches the portal's `Environment` field |
| `Unknown portal type` | Portal type not registered | Check `PortalTypes/Portal_SunkenVault.json` exists and has valid JSON |
| Players not ejected on death | Wrong `RespawnController` | Confirm `"Type": "ExitInstance"` is set in the death config |
| NPCs not spawning | Environment tag mismatch | Verify spawn file `Environments` array matches the instance environment filename |
| Loot table empty | Wrong drop table path | Confirm the file path matches the `DropList` ID pattern |

---

## Complete File Listing

```
YourMod/
  Assets/
    Server/
      GameplayConfigs/
        SunkenVault.json
      Environments/
        SunkenVault.json
      PortalTypes/
        Portal_SunkenVault.json
      Drops/
        Items/
          SunkenVault_Chest.json
          SunkenVault_BossChest.json
        NPCs/
          Intelligent/
            Drop_SunkenVault_Guardian.json
      NPC/
        Roles/
          MyMod/
            SunkenVault_Guardian.json
        Spawn/
          Instance/
            Spawns_SunkenVault.json
    Languages/
      en-US.lang
```

---

## Next Steps

- [NPC AI Behavior Trees](/hytale-modding-docs/tutorials/advanced/npc-ai-behavior-trees) — create complex AI for dungeon bosses
- [Custom Combat System](/hytale-modding-docs/tutorials/advanced/custom-combat-system) — add custom damage types for dungeon hazards
- [World Generation Mods](/hytale-modding-docs/tutorials/advanced/world-generation-mods) — generate dungeon entrances in the overworld
- [Gameplay Configs](/hytale-modding-docs/reference/game-configuration/gameplay-configs) — full reference for instance config fields
- [Drop Tables](/hytale-modding-docs/reference/economy-and-progression/drop-tables) — advanced loot table patterns
