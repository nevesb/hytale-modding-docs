---
title: Create a Custom NPC
description: Step-by-step tutorial for adding a custom critter NPC to Hytale, including role definition, drop table, and spawn rules.
---

## Goal

Add a passive critter called the **Mossbug** to the game world. You will create an NPC role JSON that references a model, write a drop table so it yields ingredients when killed, and set up spawn rules so it appears in forest environments.

## Prerequisites

- A mod folder with a valid `manifest.json` (see [Setup Your Dev Environment](/hytale-modding-docs/tutorials/beginner/setup-dev-environment))
- Familiarity with JSON template inheritance (see [JSON Basics](/hytale-modding-docs/getting-started/json-basics))

---

## NPC Types Overview

Hytale organises NPCs into types defined by the template they inherit from. Understanding the available templates helps you choose the right base for your NPC.

| Template | Folder | Behaviour |
|----------|--------|-----------|
| `Template_Beasts_Passive_Critter` | `Creature/Critter/` | Small passive animal — flees when threatened, wanders, can be attracted by food |
| `Template_Animal_Neutral` | `Creature/Mammal/` | Larger neutral beast — attacks when provoked |
| `Template_Predator` | `Creature/` | Actively hunts players within view range |
| `Template_Livestock` | `Creature/Livestock/` | Farmable animal — can be kept in coops or pens |
| `Template_Birds_Passive` | `Avian/` | Flying passive bird |
| `Template_Intelligent` | `Intelligent/` | Human-like NPC with dialogue and quest capacity |
| `Template_Spirit` | `Elemental/` | Elemental or magical creature |

For a small passive critter like the Mossbug, `Template_Beasts_Passive_Critter` is the correct base. It provides wandering, fleeing, and optional curiosity behaviours — matching how vanilla Squirrels and Frogs work.

---

## Step 1: Create or Reference a Model

Your NPC's `Appearance` field names the model set the engine uses for rendering. Vanilla appearance names like `Squirrel`, `Frog_Green`, and `Mouse` map to pre-built rig and animation sets.

For a completely new creature shape, you need a custom appearance asset (a full model, rig, and animation set in Blockbench). For this tutorial, we reference a vanilla appearance to get the NPC working immediately, which you can replace later with a custom model.

We will use `"Appearance": "Gecko"` as a stand-in. All available vanilla appearance names can be found by checking the `Appearance` field in files under `Assets/Server/NPC/Roles/`.

---

## Step 2: Create the NPC Role JSON

NPC roles live in `Assets/Server/NPC/Roles/`. Organise your mod's NPCs in a subfolder.

Create:

```
YourMod/Assets/Server/NPC/Roles/MyMod/Mossbug.json
```

The `Type: "Variant"` pattern — used by every vanilla critter including Squirrel and Frog — inherits all AI logic from the template and overrides only the fields that differ:

```json
{
  "Type": "Variant",
  "Reference": "Template_Beasts_Passive_Critter",
  "Modify": {
    "Appearance": "Gecko",
    "DropList": "Drop_Mossbug",
    "MaxHealth": 12,
    "IsMemory": true,
    "MemoriesCategory": "Critter",
    "MemoriesNameOverride": "Mossbug",
    "NameTranslationKey": {
      "Compute": "NameTranslationKey"
    }
  },
  "Parameters": {
    "NameTranslationKey": {
      "Value": "server.npcRoles.Mossbug.name",
      "Description": "Translation key for NPC name display"
    }
  }
}
```

### Modify fields explained

| Field | Purpose |
|-------|---------|
| `Appearance` | The model and animation set to render. Must match a known appearance name |
| `DropList` | ID of the drop table file (without `.json`). Resolved from `Assets/Server/Drops/` |
| `MaxHealth` | Hit points. Vanilla critters use 10–20. Squirrel and Frog both use 15 |
| `IsMemory` | Whether the player can unlock this creature in their Memories bestiary |
| `MemoriesCategory` | Bestiary category tab: `Critter`, `Beast`, `Livestock`, `Other` |
| `MemoriesNameOverride` | The display name used in the Memories screen |
| `NameTranslationKey` | Translation key for the name shown above the NPC's head |

### Parameters

The `Parameters` block defines values that the template accesses via `{ "Compute": "FieldName" }`. Setting `NameTranslationKey` here feeds into the template's `"NameTranslationKey": { "Compute": "NameTranslationKey" }` expression.

### Optional overrides

The `Template_Beasts_Passive_Critter` template exposes additional parameters you can set under `Modify`:

```json
"Modify": {
  "Appearance": "Gecko",
  "DropList": "Drop_Mossbug",
  "MaxHealth": 12,
  "MaxSpeed": 7,
  "WanderRadius": 8,
  "ViewRange": 12,
  "HearingRange": 12,
  "AttractiveItems": ["Food_Bread", "Ingredient_Fibre"]
}
```

`AttractiveItems` causes the critter to investigate and pick up dropped items from the named list — useful for taming or baiting mechanics.

---

## Step 3: Create a Drop Table

Drop tables live in `Assets/Server/Drops/`. Vanilla NPC drops are organised under `Drops/NPCs/<Category>/`. Create:

```
YourMod/Assets/Server/Drops/NPCs/Critter/Drop_Mossbug.json
```

The `Container` structure uses a weight-based selection system. `Type: "Multiple"` runs all child containers in order. `Type: "Choice"` picks one child at random, weighted by the `Weight` field.

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
              "ItemId": "Ingredient_Fibre",
              "QuantityMin": 1,
              "QuantityMax": 2
            }
          }
        ]
      },
      {
        "Type": "Choice",
        "Weight": 30,
        "Containers": [
          {
            "Type": "Single",
            "Item": {
              "ItemId": "Ingredient_Crystal",
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

This table always drops 1–2 Fibre (weight 100 out of 100 in that group) and has a 30% chance of also dropping 1 Crystal. Compare to `Drop_Bear_Grizzly.json` which uses two separate `Choice` groups each with `Weight: 100` to guarantee both a hide and meat drop.

### Drop container types

| Type | Behaviour |
|------|-----------|
| `Multiple` | Evaluates all child containers |
| `Choice` | Picks one child proportional to `Weight` |
| `Single` | Yields the specified `Item` with a random quantity between `QuantityMin` and `QuantityMax` |

If you want a critter to drop nothing (like vanilla Squirrel and Frog), simply create an empty object:

```json
{}
```

---

## Step 4: Create Spawn Rules

Spawn rules tell the world generator where and when to place your NPC. Spawn files live in `Assets/Server/NPC/Spawn/World/<Zone>/`.

Create:

```
YourMod/Assets/Server/NPC/Spawn/World/Zone1/Spawns_Zone1_MyMod_Critter.json
```

```json
{
  "Environments": [
    "Env_Zone1_Forests",
    "Env_Zone1_Autumn"
  ],
  "NPCs": [
    {
      "Weight": 3,
      "SpawnBlockSet": "Soil",
      "Id": "Mossbug",
      "Flock": "One_Or_Two"
    }
  ],
  "DayTimeRange": [
    6,
    18
  ]
}
```

### Spawn fields explained

| Field | Purpose |
|-------|---------|
| `Environments` | Which environment biomes this file applies to. Matches environment IDs used by world generation |
| `NPCs` | List of NPCs that can spawn in these environments |
| `Weight` | Relative likelihood of this NPC being chosen versus others in the same file. Higher = more common. Squirrel uses `Weight: 6` in Zone 1 forests |
| `SpawnBlockSet` | Surface type the NPC spawns on: `Soil` (ground), `Birds` (air, for flying NPCs), `Water` (aquatic) |
| `Id` | The NPC role ID — matches the filename of your role JSON without `.json` |
| `Flock` | Group size at spawn. Available values: `One_Or_Two`, `Group_Small`, `Group_Large` |
| `DayTimeRange` | Hour range `[start, end]` during which this file's spawns are active. `[6, 18]` = daytime only |

For a nocturnal critter, use `"DayTimeRange": [20, 6]` (wraps midnight).

### Available environments (Zone 1 examples)

| Environment ID | Description |
|----------------|-------------|
| `Env_Zone1_Forests` | Standard temperate forest |
| `Env_Zone1_Autumn` | Autumn coloured forest |
| `Env_Zone1_Azure` | Azure (blue-tinted) forest variant |
| `Env_Zone1_Mountains_Critter` | Mountain terrain |

---

## Step 5: Add Translation Keys

Add NPC name text to your mod's language file:

```
YourMod/Assets/Languages/en-US.lang
```

```
server.npcRoles.Mossbug.name=Mossbug
```

---

## Step 6: Test In-Game

1. Place your mod folder in the server mods directory.
2. Start the server. Watch the console for errors about unknown role IDs, missing appearances, or invalid drop table references.
3. Use the developer NPC spawner to force-spawn `Mossbug` at your location.
4. Confirm the model renders, the NPC wanders, and it flees when you approach.
5. Kill the Mossbug and verify the drop table yields Fibre (and occasionally Crystal).
6. Travel to a Zone 1 Forest biome and confirm Mossbugs appear naturally during the day.

**Common errors and fixes:**

| Error | Cause | Fix |
|-------|-------|-----|
| `Unknown reference: Template_Beasts_Passive_Critter` | Template not found | Ensure vanilla assets are loaded before your mod |
| `Unknown appearance: Gecko` | Appearance name typo | Check `Assets/Server/NPC/Roles/` for valid appearance names |
| `Unknown drop list: Drop_Mossbug` | Drop file path wrong | Confirm file is at `Drops/NPCs/Critter/Drop_Mossbug.json` |
| NPC not spawning naturally | Wrong environment ID | Cross-reference environment names with vanilla spawn files |

---

## Complete Files

### `YourMod/Assets/Server/NPC/Roles/MyMod/Mossbug.json`
```json
{
  "Type": "Variant",
  "Reference": "Template_Beasts_Passive_Critter",
  "Modify": {
    "Appearance": "Gecko",
    "DropList": "Drop_Mossbug",
    "MaxHealth": 12,
    "IsMemory": true,
    "MemoriesCategory": "Critter",
    "MemoriesNameOverride": "Mossbug",
    "NameTranslationKey": {
      "Compute": "NameTranslationKey"
    }
  },
  "Parameters": {
    "NameTranslationKey": {
      "Value": "server.npcRoles.Mossbug.name",
      "Description": "Translation key for NPC name display"
    }
  }
}
```

### `YourMod/Assets/Server/Drops/NPCs/Critter/Drop_Mossbug.json`
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
              "ItemId": "Ingredient_Fibre",
              "QuantityMin": 1,
              "QuantityMax": 2
            }
          }
        ]
      },
      {
        "Type": "Choice",
        "Weight": 30,
        "Containers": [
          {
            "Type": "Single",
            "Item": {
              "ItemId": "Ingredient_Crystal",
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

### `YourMod/Assets/Server/NPC/Spawn/World/Zone1/Spawns_Zone1_MyMod_Critter.json`
```json
{
  "Environments": [
    "Env_Zone1_Forests",
    "Env_Zone1_Autumn"
  ],
  "NPCs": [
    {
      "Weight": 3,
      "SpawnBlockSet": "Soil",
      "Id": "Mossbug",
      "Flock": "One_Or_Two"
    }
  ],
  "DayTimeRange": [
    6,
    18
  ]
}
```

### `YourMod/Assets/Languages/en-US.lang`
```
server.npcRoles.Mossbug.name=Mossbug
```

---

## Next Steps

- [Create a Custom Item](/hytale-modding-docs/tutorials/beginner/create-an-item) — add a weapon that your NPC could potentially drop
- [Create a Custom Block](/hytale-modding-docs/tutorials/beginner/create-a-block) — create a block drop for your NPC's loot table
- [JSON Basics](/hytale-modding-docs/getting-started/json-basics) — reference for weight-based selection and computed values
