---
title: Complete Farming System
description: Build a complete farming system with custom coops, growth modifiers, animal management, produce drop tables, and crop integration.
---

## Goal

Build a complete farming system for a custom animal called the **Silkworm**. You will create a coop that houses Silkworms, configure produce drop tables, set up growth modifiers for environmental conditions, create the Silkworm NPC role with taming support, and integrate with the crafting system. By the end you will have a self-contained farming loop: catch wild Silkworms, place them in a coop, and collect silk fibre for crafting.

## Prerequisites

- A mod folder with a valid `manifest.json` (see [Setup Your Dev Environment](/hytale-modding-docs/tutorials/beginner/setup-dev-environment))
- Understanding of NPC roles (see [NPC Roles](/hytale-modding-docs/reference/npc-system/npc-roles) and [Create a Custom NPC](/hytale-modding-docs/tutorials/beginner/create-an-npc))
- Understanding of drop tables (see [Drop Tables](/hytale-modding-docs/reference/economy-and-progression/drop-tables))
- Familiarity with the farming system (see [Farming & Coops](/hytale-modding-docs/reference/economy-and-progression/farming-coops))

---

## How the Farming System Works

The farming system has two main components:

### Coops

Coops are structures that house NPC animals and produce drops on a timer. Each coop defines:
- Which NPC groups can be placed inside
- Maximum number of residents
- What each species produces (via drop table references)
- When residents roam freely vs stay inside

### Modifiers

Growth modifiers are environmental conditions that speed up or slow down produce cycles. Four modifier types exist:

| Modifier | Source | Effect |
|----------|--------|--------|
| `Water` | Nearby water blocks or rain weather | Multiplies growth rate (vanilla: 2.5x) |
| `Fertilizer` | Fertilizer item applied to coop or soil | Multiplies growth rate (vanilla: 2x) |
| `LightLevel` | Artificial light or sunlight | Multiplies growth rate when sufficient light is present |
| `Darkness` | Absence of light | Multiplies growth rate in dark conditions (for cave-dwelling species) |

### Produce Cycle

```
Animal placed in coop
    → Timer starts (based on ProduceTimeout range)
    → Modifiers apply (Water, Light, Fertilizer speed it up)
    → Timer completes
    → Produce drop table is rolled
    → Items appear in coop output
    → Timer resets
```

---

## Step 1: Create the Silkworm NPC Role

The Silkworm is a passive critter that can be tamed and placed in coops. It uses the `Template_Beasts_Passive_Critter` base for simple wandering and fleeing behaviour.

Create `YourMod/Assets/Server/NPC/Roles/MyMod/Silkworm.json`:

```json
{
  "Type": "Variant",
  "Reference": "Template_Beasts_Passive_Critter",
  "Modify": {
    "Appearance": "Gecko",
    "DropList": "Drop_Silkworm",
    "MaxHealth": 8,
    "MaxSpeed": 3,
    "ViewRange": 6,
    "HearingRange": 4,
    "IsTameable": true,
    "TameRoleChange": "Tamed_Silkworm",
    "AttractiveItemSet": ["Plant_Crop_Cotton_Item"],
    "AttractiveItemSetParticles": "Want_Food_Plant",
    "ProduceItem": "Ingredient_Silk_Fibre",
    "ProduceTimeout": ["PT12H", "PT36H"],
    "IsMemory": true,
    "MemoriesCategory": "Critter",
    "MemoriesNameOverride": "Silkworm",
    "NameTranslationKey": {
      "Compute": "NameTranslationKey"
    }
  },
  "Parameters": {
    "NameTranslationKey": {
      "Value": "server.npcRoles.Silkworm.name",
      "Description": "Translation key for NPC name display"
    }
  }
}
```

### Key farming fields

| Field | Value | Purpose |
|-------|-------|---------|
| `IsTameable: true` | Enables taming interaction | Players can tame wild Silkworms by feeding attractive items |
| `TameRoleChange` | `"Tamed_Silkworm"` | When tamed, the NPC switches to a tamed variant with different behaviour |
| `AttractiveItemSet` | `["Plant_Crop_Cotton_Item"]` | Silkworms are attracted to cotton — holding cotton near one starts the taming process |
| `ProduceItem` | `"Ingredient_Silk_Fibre"` | Free-roaming Silkworms periodically drop silk fibre on the ground |
| `ProduceTimeout` | `["PT12H", "PT36H"]` | ISO 8601 duration: produces every 12-36 in-game hours when free-roaming |

Compare to the vanilla Chicken which uses `"ProduceItem": "Food_Egg"` and `"ProduceTimeout": ["PT18H", "PT48H"]`.

Create the tamed variant at `YourMod/Assets/Server/NPC/Roles/MyMod/Tamed_Silkworm.json`:

```json
{
  "Type": "Variant",
  "Reference": "Template_Beasts_Passive_Critter",
  "Modify": {
    "Appearance": "Gecko",
    "DropList": "Drop_Silkworm",
    "MaxHealth": 8,
    "MaxSpeed": 2,
    "ViewRange": 4,
    "HearingRange": 3,
    "DefaultPlayerAttitude": "Neutral",
    "ProduceItem": "Ingredient_Silk_Fibre",
    "ProduceTimeout": ["PT8H", "PT24H"],
    "IsMemory": false,
    "NameTranslationKey": {
      "Compute": "NameTranslationKey"
    }
  },
  "Parameters": {
    "NameTranslationKey": {
      "Value": "server.npcRoles.Tamed_Silkworm.name",
      "Description": "Translation key for NPC name display"
    }
  }
}
```

The tamed variant has a shorter produce timeout (8-24 hours vs 12-36), slower speed (less likely to wander away), and a neutral attitude toward players (will not flee when approached).

---

## Step 2: Create NPC Groups

NPC groups define which animals a coop accepts. Coops reference groups, not individual roles.

Create `YourMod/Assets/Server/NPC/Groups/Silkworm.json`:

```json
{
  "Id": "Silkworm",
  "Members": [
    "Silkworm",
    "Tamed_Silkworm"
  ]
}
```

Both the wild and tamed variants belong to the same group. This means the coop accepts both — a wild Silkworm placed in a coop is treated the same as a tamed one for produce purposes.

---

## Step 3: Create the Silkworm Coop

The coop definition specifies capacity, accepted NPC groups, produce drop tables, and roaming schedules.

Create `YourMod/Assets/Server/Farming/Coops/Coop_Silkworm.json`:

```json
{
  "MaxResidents": 8,
  "ProduceDrops": {
    "Silkworm": "Drop_Silkworm_Produce",
    "Tamed_Silkworm": "Drop_Silkworm_Produce"
  },
  "ResidentRoamTime": [8, 16],
  "ResidentSpawnOffset": {
    "X": 0,
    "Y": 0,
    "Z": 2
  },
  "AcceptedNpcGroups": [
    "Silkworm"
  ],
  "CaptureWildNPCsInRange": true,
  "WildCaptureRadius": 8
}
```

### Coop design decisions

| Field | Value | Rationale |
|-------|-------|-----------|
| `MaxResidents: 8` | Higher than Chicken coop (6) | Silkworms are small, more can fit |
| `ProduceDrops` | Maps both variants to same drop table | Wild and tamed produce the same items |
| `ResidentRoamTime: [8, 16]` | Daytime roaming only | Silkworms roam from 8 AM to 4 PM, stay inside otherwise |
| `CaptureWildNPCsInRange: true` | Auto-captures nearby wild Silkworms | Convenience feature: wild Silkworms wandering near the coop are automatically captured |
| `WildCaptureRadius: 8` | 8-block capture range | Moderate range — players need to lure Silkworms somewhat close |

Compare to the vanilla Chicken coop:
- Chicken coop has `MaxResidents: 6`, `WildCaptureRadius: 10`
- Chicken coop accepts 3 NPC groups: `Chicken`, `Chicken_Desert`, `Skrill`
- Silkworm coop is simpler with one group but higher capacity

---

## Step 4: Create Produce Drop Tables

The produce drop table defines what items a coop resident generates each produce cycle.

Create `YourMod/Assets/Server/Drops/NPCs/Critter/Drop_Silkworm_Produce.json`:

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
              "ItemId": "Ingredient_Silk_Fibre",
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
              "ItemId": "Ingredient_Silk_Thread",
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

Each produce cycle, a Silkworm always drops 1-3 Silk Fibre and has a 15% chance to also drop 1 Silk Thread (a higher-tier crafting material).

Also create the NPC kill drop table at `YourMod/Assets/Server/Drops/NPCs/Critter/Drop_Silkworm.json`:

```json
{
  "Container": {
    "Type": "Choice",
    "Containers": [
      {
        "Type": "Single",
        "Weight": 80,
        "Item": {
          "ItemId": "Ingredient_Silk_Fibre",
          "QuantityMin": 1,
          "QuantityMax": 1
        }
      },
      {
        "Type": "Empty",
        "Weight": 20
      }
    ]
  }
}
```

Killing a Silkworm has an 80% chance to drop 1 Silk Fibre — far less efficient than farming them in a coop (1-3 fibre per cycle plus chance of thread). This incentivises the farming loop over hunting.

---

## Step 5: Create Growth Modifiers

Growth modifiers accelerate produce cycles when environmental conditions are met. Create modifiers that affect Silkworm production.

The vanilla modifiers in `Assets/Server/Farming/Modifiers/` already apply globally. You can create additional modifiers for your farming system or rely on the vanilla ones.

For Silkworms, create a darkness modifier since they prefer shaded environments:

Create `YourMod/Assets/Server/Farming/Modifiers/Darkness_Silkworm.json`:

```json
{
  "Type": "Darkness",
  "Modifier": 1.8
}
```

This gives Silkworms a 1.8x growth rate multiplier when their coop is in a dark area (underground or in a roofed structure). Compare to the vanilla Light modifier which gives 2x for well-lit areas — Silkworms are the opposite, preferring darkness.

The vanilla Water modifier (`Modifier: 2.5`) and Fertilizer modifier (`Modifier: 2`) also apply to coops. A Silkworm coop near water in a dark cave would benefit from both:

- Base produce rate: 1x
- Darkness bonus: 1.8x
- Water bonus: 2.5x
- Combined: roughly 4.5x faster production

### Understanding modifier stacking

Modifiers apply multiplicatively to the base produce timer. If a Silkworm's `ProduceTimeout` is 24 in-game hours at base rate:

| Modifiers active | Effective produce time |
|-----------------|----------------------|
| None | 24 hours |
| Darkness (1.8x) | ~13.3 hours |
| Water (2.5x) | ~9.6 hours |
| Darkness + Water | ~5.3 hours |
| Darkness + Water + Fertilizer (2x) | ~2.7 hours |

---

## Step 6: Create Spawn Rules for Wild Silkworms

Wild Silkworms need spawn rules so players can find and catch them. Place them in forest environments where they spawn in small groups.

Create `YourMod/Assets/Server/NPC/Spawn/World/Zone1/Spawns_Zone1_Silkworm.json`:

```json
{
  "Environments": [
    "Env_Zone1_Forests",
    "Env_Zone1_Autumn",
    "Env_Zone1_Azure"
  ],
  "NPCs": [
    {
      "Weight": 2,
      "SpawnBlockSet": "Soil",
      "Id": "Silkworm",
      "Flock": "One_Or_Two"
    }
  ],
  "DayTimeRange": [6, 14]
}
```

Weight 2 makes Silkworms uncommon (vanilla Squirrel uses weight 6). They only appear during morning and early afternoon hours, and spawn in pairs at most — making them a resource worth seeking out.

---

## Step 7: Create Crafting Integration

Connect the farming output to the crafting system. Create items that use Silk Fibre and Silk Thread.

Create `YourMod/Assets/Server/Item/Items/MyMod/Ingredient_Silk_Fibre.json`:

```json
{
  "TranslationProperties": {
    "Name": "server.items.Ingredient_Silk_Fibre.name",
    "Description": "server.items.Ingredient_Silk_Fibre.description"
  },
  "Quality": "Common",
  "Icon": "Icons/ItemsGenerated/Ingredient_Silk_Fibre.png",
  "Categories": ["Items.Ingredients"],
  "MaxStack": 50,
  "DropOnDeath": true,
  "ResourceTypes": [
    { "Id": "Fibre" }
  ]
}
```

Create `YourMod/Assets/Server/Item/Items/MyMod/Ingredient_Silk_Thread.json`:

```json
{
  "TranslationProperties": {
    "Name": "server.items.Ingredient_Silk_Thread.name",
    "Description": "server.items.Ingredient_Silk_Thread.description"
  },
  "Quality": "Uncommon",
  "Icon": "Icons/ItemsGenerated/Ingredient_Silk_Thread.png",
  "Categories": ["Items.Ingredients"],
  "MaxStack": 25,
  "DropOnDeath": true,
  "ResourceTypes": [
    { "Id": "Thread" }
  ],
  "Recipe": {
    "Input": [
      { "ItemId": "Ingredient_Silk_Fibre", "Quantity": 3 }
    ],
    "OutputQuantity": 1,
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Id": "Loom",
        "Categories": ["Textiles"]
      }
    ],
    "TimeSeconds": 4
  }
}
```

Silk Thread can be crafted from 3 Silk Fibre at a Loom, or obtained rarely from coop produce. This creates two paths: players can either wait for lucky drops or actively craft thread from fibre.

---

## Step 8: Add Translation Keys

Add to `YourMod/Assets/Languages/en-US.lang`:

```
server.npcRoles.Silkworm.name=Silkworm
server.npcRoles.Tamed_Silkworm.name=Silkworm
server.items.Ingredient_Silk_Fibre.name=Silk Fibre
server.items.Ingredient_Silk_Fibre.description=Fine fibre produced by silkworms. Used in textile crafting.
server.items.Ingredient_Silk_Thread.name=Silk Thread
server.items.Ingredient_Silk_Thread.description=Woven silk thread. A premium crafting material for light armour and decoration.
```

---

## Step 9: Test the Farming System

1. Place your mod folder in the server mods directory and start the server.
2. Travel to a Zone 1 forest biome and look for wild Silkworms during the morning.
3. Hold cotton items near a Silkworm to test the attraction and taming mechanic.
4. Build or place a coop structure and test these interactions:

| Test | Expected result |
|------|----------------|
| Place tamed Silkworm in coop | Silkworm appears inside, resident count increases |
| Place 9th Silkworm (over capacity) | Coop rejects — MaxResidents is 8 |
| Wait for produce cycle | Silk Fibre (1-3) appears in coop output. 15% chance of Silk Thread |
| Check roaming hours | Silkworms roam freely 8 AM - 4 PM, return to shelter otherwise |
| Place coop near water | Produce timer should speed up (2.5x Water modifier) |
| Place coop underground | Darkness modifier applies (1.8x) |
| Wild Silkworm wanders within 8 blocks | Auto-captured into coop (CaptureWildNPCsInRange) |
| Kill a wild Silkworm | 80% chance of 1 Silk Fibre drop |
| Craft Silk Thread at Loom | 3 Silk Fibre = 1 Silk Thread |

### Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| Coop does not accept Silkworm | NPC group mismatch | Ensure `AcceptedNpcGroups` matches the group ID in `Groups/Silkworm.json` |
| No produce output | Drop table ID mismatch | Verify `ProduceDrops` keys match the NPC role filenames |
| Produce too slow | No modifiers active | Place coop near water or in darkness to activate modifiers |
| Wild capture not working | Radius too small | Increase `WildCaptureRadius` or lure Silkworms closer |
| Taming fails | Wrong attractive item | Confirm `AttractiveItemSet` contains a valid item ID |
| Silkworms not spawning | Environment mismatch | Verify spawn file `Environments` array contains valid environment IDs |

---

## Complete File Listing

```
YourMod/
  Assets/
    Server/
      NPC/
        Roles/
          MyMod/
            Silkworm.json
            Tamed_Silkworm.json
        Groups/
          Silkworm.json
        Spawn/
          World/
            Zone1/
              Spawns_Zone1_Silkworm.json
      Farming/
        Coops/
          Coop_Silkworm.json
        Modifiers/
          Darkness_Silkworm.json
      Drops/
        NPCs/
          Critter/
            Drop_Silkworm.json
            Drop_Silkworm_Produce.json
      Item/
        Items/
          MyMod/
            Ingredient_Silk_Fibre.json
            Ingredient_Silk_Thread.json
    Languages/
      en-US.lang
```

---

## Next Steps

- [Create a Custom Item](/hytale-modding-docs/tutorials/beginner/create-an-item) — create armour and tools from Silk Thread
- [Recipes](/hytale-modding-docs/reference/crafting-system/recipes) — full crafting recipe reference
- [Farming & Coops](/hytale-modding-docs/reference/economy-and-progression/farming-coops) — complete coop schema reference
- [Drop Tables](/hytale-modding-docs/reference/economy-and-progression/drop-tables) — advanced loot table patterns
- [NPC Groups](/hytale-modding-docs/reference/npc-system/npc-groups) — NPC group definitions
- [Weather System](/hytale-modding-docs/reference/world-and-environment/weather-system) — weather IDs used in Water modifier conditions
