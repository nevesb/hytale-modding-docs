---
title: Custom Loot Tables
description: Step-by-step tutorial for creating loot and drop tables with weighted entries, nested containers, and conditional drops.
---

## Goal

Create a set of custom loot tables that demonstrate the full range of Hytale's drop system. You will build a guaranteed drop, a weighted random drop, a nested table with rare equipment, and a resource harvesting drop table.

## What You'll Learn

- How `Container` types (`Multiple`, `Choice`, `Single`) work together to create drop logic
- How `Weight` controls probability of random drops
- How to nest containers for complex loot tables with guaranteed and rare drops
- How `QuantityMin` and `QuantityMax` create variable drop amounts
- How different drop table categories (NPCs, Wood, Rock, Crop) are organised

## Prerequisites

- A mod folder with a valid `manifest.json` (see [Setup Your Dev Environment](/hytale-modding-docs/tutorials/beginner/setup-dev-environment))
- At least one custom item (see [Create a Custom Item](/hytale-modding-docs/tutorials/beginner/create-an-item))

---

## Drop System Overview

Drop tables live in `Assets/Server/Drops/` and are organised by source type:

```
Assets/Server/Drops/
  NPCs/
    Beast/
    Boss/
    Critter/
    Elemental/
    Intelligent/
      Feran/
      Goblin/
      Trork/
    Livestock/
    Undead/
    Void/
  Crop/
  Wood/
  Rock/
  Plant/
  Items/
  Prefabs/
  Traps/
```

Every drop table is a JSON file with a root `Container` object. The container system uses three types that can be nested to create any drop logic.

### Container types

| Type | Behaviour |
|------|-----------|
| `Multiple` | Evaluates **all** child containers in order. Each child runs independently |
| `Choice` | Picks **one** child at random, weighted by `Weight` values |
| `Single` | Terminal node. Yields the specified `Item` with a random quantity between `QuantityMin` and `QuantityMax` |

---

## Step 1: Create a Guaranteed Drop

The simplest drop table guarantees one or more items every time. This pattern is used by `Rock_Crystal_Blue.json` for crystal deposits.

Create:

```
YourMod/Assets/Server/Drops/NPCs/Beast/Drop_Thornbeast.json
```

```json
{
  "Container": {
    "Type": "Multiple",
    "Containers": [
      {
        "Type": "Single",
        "Item": {
          "ItemId": "Ingredient_Hide_Heavy",
          "QuantityMin": 2,
          "QuantityMax": 4
        }
      }
    ]
  }
}
```

A `Multiple` container with a single `Single` child guarantees the drop every time. The quantity is randomly chosen between `QuantityMin` and `QuantityMax` (inclusive).

---

## Step 2: Create a Multi-Drop Table with Guaranteed Items

This pattern -- used by `Drop_Bear_Grizzly.json` -- guarantees multiple different drops by using a `Multiple` container with several children:

```
YourMod/Assets/Server/Drops/NPCs/Beast/Drop_Crystalbeast.json
```

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
              "ItemId": "Ingredient_Hide_Heavy",
              "QuantityMin": 1,
              "QuantityMax": 2
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
              "ItemId": "Food_Wildmeat_Raw",
              "QuantityMin": 2,
              "QuantityMax": 3
            }
          }
        ]
      }
    ]
  }
}
```

The `Multiple` container runs both `Choice` groups. Since each `Choice` group has only one option with `Weight: 100`, both items are guaranteed. This structure is used instead of two plain `Single` containers because the `Weight` field on `Choice` containers also controls whether the group drops at all -- a `Weight` of 100 means 100% chance.

---

## Step 3: Create a Weighted Random Drop with Rare Loot

This pattern -- used by `Drop_Trork_Warrior.json` -- combines guaranteed drops with rare equipment. The `Choice` container picks one child based on relative weights:

```
YourMod/Assets/Server/Drops/NPCs/Intelligent/Drop_Crystal_Guardian.json
```

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
              "ItemId": "Ingredient_Crystal_Cyan",
              "QuantityMin": 2,
              "QuantityMax": 5
            }
          }
        ]
      },
      {
        "Type": "Choice",
        "Weight": 15,
        "Containers": [
          {
            "Weight": 40,
            "Type": "Single",
            "Item": {
              "ItemId": "Armor_Crystal_Head",
              "QuantityMin": 1,
              "QuantityMax": 1
            }
          },
          {
            "Weight": 40,
            "Type": "Single",
            "Item": {
              "ItemId": "Armor_Crystal_Chest",
              "QuantityMin": 1,
              "QuantityMax": 1
            }
          },
          {
            "Weight": 20,
            "Type": "Single",
            "Item": {
              "ItemId": "Weapon_Sword_Crystal",
              "QuantityMin": 1,
              "QuantityMax": 1
            }
          }
        ]
      }
    ]
  }
}
```

### How the weights work

The outer `Multiple` container runs both groups:

1. **Group 1** (`Weight: 100`): Always drops 2-5 crystals
2. **Group 2** (`Weight: 15`): 15% chance to run. If it runs, it picks one item:
   - 40% chance: Crystal Helmet
   - 40% chance: Crystal Chestplate
   - 20% chance: Crystal Sword

The inner `Weight` values are relative to each other within the `Choice` group: 40 + 40 + 20 = 100 total, so the sword has a 20/100 = 20% chance *when the group activates*.

The overall chance of getting the sword on any kill is: 15% (group activates) x 20% (sword selected) = 3%.

---

## Step 4: Create a Nested Drop Table with Multiple Outcomes

For complex scenarios, nest `Multiple` inside `Choice` to create branching outcomes. This pattern is used by `Wood_Branch.json`:

```
YourMod/Assets/Server/Drops/Wood/Drop_Crystalwood_Branch.json
```

```json
{
  "Container": {
    "Type": "Choice",
    "Containers": [
      {
        "Type": "Multiple",
        "Weight": 60,
        "Containers": [
          {
            "Type": "Single",
            "Item": {
              "ItemId": "Ingredient_Stick",
              "QuantityMin": 1,
              "QuantityMax": 3
            }
          },
          {
            "Type": "Single",
            "Item": {
              "ItemId": "Ingredient_Crystal_Cyan",
              "QuantityMin": 0,
              "QuantityMax": 1
            }
          }
        ]
      },
      {
        "Type": "Multiple",
        "Weight": 40,
        "Containers": [
          {
            "Type": "Single",
            "Item": {
              "ItemId": "Ingredient_Stick"
            }
          }
        ]
      }
    ]
  }
}
```

This table has two possible outcomes chosen by the outer `Choice`:

- **60% chance**: Drop 1-3 sticks AND 0-1 crystals (both items from the `Multiple`)
- **40% chance**: Drop 1 stick only

Note that when `QuantityMin` is 0, there is a chance the item yields nothing. When `QuantityMin` and `QuantityMax` are omitted, the quantity defaults to 1.

---

## Step 5: Create an Empty Drop Table

Some NPCs (like vanilla Squirrels and Frogs) drop nothing. An empty object achieves this:

```
YourMod/Assets/Server/Drops/NPCs/Critter/Drop_Glowfly.json
```

```json
{}
```

---

## Step 6: Connect the Drop Table to an NPC

Drop tables are referenced by NPC role definitions through the `DropList` field. The value matches the filename without `.json`, and the engine searches all directories under `Assets/Server/Drops/`.

In your NPC role file:

```json
{
  "Type": "Variant",
  "Reference": "Template_Predator",
  "Modify": {
    "Appearance": "Bear_Grizzly",
    "DropList": "Drop_Crystal_Guardian",
    "MaxHealth": 80
  }
}
```

The `DropList` value `"Drop_Crystal_Guardian"` resolves to `Assets/Server/Drops/NPCs/Intelligent/Drop_Crystal_Guardian.json`.

---

## Step 7: Test In-Game

1. Place your mod folder in the server mods directory.
2. Start the server and watch for errors about unknown drop list IDs or invalid item IDs.
3. Spawn the NPC that uses your drop table.
4. Kill the NPC multiple times and verify:
   - Guaranteed drops appear every time
   - Rare drops appear at approximately the expected frequency
   - Quantities fall within the defined min/max ranges
5. For resource drops (wood, rock), break the corresponding block and verify drops.

**Common errors and fixes:**

| Error | Cause | Fix |
|-------|-------|-----|
| `Unknown drop list` | Wrong filename or directory | Verify the drop file exists and `DropList` matches the filename without `.json` |
| `Unknown item id` | Item ID typo in drop table | Check `ItemId` values match actual item definition filenames |
| NPC drops nothing | Empty container or `Weight: 0` | Ensure at least one container has a non-zero weight |
| Always same quantity | `QuantityMin` equals `QuantityMax` | Set different values for variable drops |
| Rare drop never appears | `Weight` too low | Increase the `Weight` value on the `Choice` container or test more kills |

---

## Next Steps

- [Create a Custom NPC](/hytale-modding-docs/tutorials/beginner/create-an-npc) -- build the NPC that uses your drop table
- [Custom NPC Spawning](/hytale-modding-docs/tutorials/intermediate/custom-npc-spawning) -- control where your loot-dropping NPCs appear
- [NPC Shops and Trading](/hytale-modding-docs/tutorials/intermediate/npc-shops-and-trading) -- create merchants that sell items from your loot tables
