---
title: Custom NPC Spawn Rules
description: Step-by-step tutorial for creating custom NPC spawn rules with environments, time ranges, moon phases, and biome conditions.
---

## Goal

Create advanced spawn rules that control where, when, and how your NPCs appear in the world. You will build spawn files for daytime forest creatures, nocturnal void enemies with moon phase modifiers, and zone-specific predators with light level restrictions.

## What You'll Learn

- How spawn rule files connect environments to NPC roles
- How to use `DayTimeRange` for time-of-day restrictions
- How `Weight` and `Flock` control spawn frequency and group size
- How `SpawnBlockSet` determines the surface type for spawning
- How `MoonPhaseWeightModifiers`, `LightRanges`, and `Despawn` create advanced spawn behaviour

## Prerequisites

- A mod folder with a valid `manifest.json` (see [Setup Your Dev Environment](/hytale-modding-docs/tutorials/beginner/setup-dev-environment))
- At least one custom NPC role (see [Create a Custom NPC](/hytale-modding-docs/tutorials/beginner/create-an-npc))

---

## Spawn System Overview

Spawn rules live in `Assets/Server/NPC/Spawn/World/` and are organised by zone. The engine reads every JSON file in these directories and merges them. Each file associates a list of environments (biomes) with a list of NPCs that can spawn there.

```
Assets/Server/NPC/Spawn/World/
  Zone0/
  Zone1/
    Spawns_Zone1_Forests_Critter.json
    Spawns_Zone1_Forests_Predator.json
    Spawns_Zone1_Mountains_Animal.json
  Zone2/
  Zone3/
  Zone4/
  Void/
  Unique/
```

---

## Step 1: Create a Basic Daytime Spawn Rule

This example spawns critters in Zone 1 forest biomes during the day -- matching the pattern used by vanilla files like `Spawns_Zone1_Forests_Critter.json`.

Create:

```
YourMod/Assets/Server/NPC/Spawn/World/Zone1/Spawns_Zone1_MyMod_Critter.json
```

```json
{
  "Environments": [
    "Env_Zone1_Forests",
    "Env_Zone1_Autumn",
    "Env_Zone1_Azure"
  ],
  "NPCs": [
    {
      "Weight": 4,
      "SpawnBlockSet": "Soil",
      "Id": "Mossbug",
      "Flock": "One_Or_Two"
    },
    {
      "Weight": 2,
      "SpawnBlockSet": "Birds",
      "Id": "Glowfly",
      "Flock": "Group_Small"
    }
  ],
  "DayTimeRange": [
    6,
    18
  ]
}
```

### Field reference

| Field | Purpose |
|-------|---------|
| `Environments` | Array of environment IDs this spawn file applies to. The engine matches these against the world generator's biome map |
| `NPCs` | Array of NPC entries that can spawn in the listed environments |
| `NPCs[].Weight` | Relative spawn likelihood. Higher values mean more common. Vanilla critters use 2-6 typically |
| `NPCs[].SpawnBlockSet` | Surface type for spawning: `"Soil"` (ground), `"Birds"` (air), `"Water"` (aquatic) |
| `NPCs[].Id` | NPC role ID -- matches the filename of the role JSON without `.json` |
| `NPCs[].Flock` | Group size. String values: `"One_Or_Two"`, `"Group_Small"`, `"Group_Large"` |
| `DayTimeRange` | `[start, end]` hours (0-24) during which spawning is active. `[6, 18]` = 6 AM to 6 PM |

---

## Step 2: Create a Nocturnal Spawn Rule with Moon Phases

Void creatures in Hytale use advanced spawn settings including moon phase weight modifiers and despawn rules. This pattern comes from files in `Assets/Server/NPC/Spawn/World/Void/`.

Create:

```
YourMod/Assets/Server/NPC/Spawn/World/Void/Spawns_MyMod_Night_Void.json
```

```json
{
  "Environments": [
    "Env_Zone1_Plains",
    "Env_Zone2_Savanna",
    "Env_Zone3_Tundra"
  ],
  "Despawn": {
    "DayTimeRange": [
      5,
      19
    ]
  },
  "MoonPhaseWeightModifiers": [
    0.5,
    1,
    1.5,
    1.5,
    1
  ],
  "NPCs": [
    {
      "Weight": 20,
      "SpawnBlockSet": "Soil",
      "Id": "Shadow_Crawler",
      "Flock": {
        "Size": [
          2,
          3
        ]
      }
    }
  ],
  "DayTimeRange": [
    19,
    5
  ],
  "LightRanges": {
    "Light": [
      0,
      8
    ]
  }
}
```

### Advanced spawn fields

| Field | Purpose |
|-------|---------|
| `Despawn.DayTimeRange` | `[start, end]` hours during which spawned NPCs are forcibly despawned. Used to remove night creatures at dawn |
| `MoonPhaseWeightModifiers` | Array of multipliers applied to all `Weight` values based on the current moon phase. Index 0 = new moon, higher indices = fuller moons. Values above 1.0 increase spawns; below 1.0 decrease them |
| `LightRanges.Light` | `[min, max]` light level range (0-15) required at the spawn location. `[0, 8]` means the NPC only spawns in dark areas |
| `Flock.Size` | Alternative to string flock names. `[min, max]` array for custom group sizes |

### Night-time DayTimeRange

When `start > end` (e.g., `[19, 5]`), the range wraps past midnight. This means spawning is active from 7 PM through to 5 AM.

---

## Step 3: Create a Zone-Specific Predator Spawn

Predators use higher weights and typically spawn alone. This pattern matches `Spawns_Zone1_Forests_Predator.json`.

Create:

```
YourMod/Assets/Server/NPC/Spawn/World/Zone1/Spawns_Zone1_MyMod_Predator.json
```

```json
{
  "Environments": [
    "Env_Zone1_Forests",
    "Env_Zone1_Autumn"
  ],
  "NPCs": [
    {
      "Weight": 5,
      "SpawnBlockSet": "Soil",
      "Id": "Thornbeast"
    },
    {
      "Weight": 3,
      "SpawnBlockSet": "Soil",
      "Id": "Venomfang",
      "Flock": "One_Or_Two"
    }
  ],
  "DayTimeRange": [
    6,
    18
  ]
}
```

When no `Flock` is specified (as with Thornbeast above), the NPC spawns individually.

---

## Step 4: Create an Aquatic Spawn Rule

For water-dwelling creatures, use the `Water` spawn block set and the `SpawnFluidTag` field:

```
YourMod/Assets/Server/NPC/Spawn/World/Zone1/Spawns_Zone1_MyMod_Aquatic.json
```

```json
{
  "Environments": [
    "Env_Zone1_Forests",
    "Env_Zone1_Autumn"
  ],
  "NPCs": [
    {
      "Weight": 10,
      "SpawnBlockSet": "Water",
      "SpawnFluidTag": "Water",
      "Id": "Glowfish",
      "Flock": "Group_Small"
    }
  ],
  "DayTimeRange": [
    6,
    18
  ]
}
```

### SpawnFluidTag

The `SpawnFluidTag` field restricts spawning to tiles containing a specific fluid. Use `"Water"` for freshwater spawns. This field is used in vanilla files like `Spawns_Portals_Oasis_Animal.json` for flamingos near water.

---

## Available Environment IDs

Here are common environment IDs by zone:

| Zone | Environment IDs |
|------|----------------|
| Zone 1 | `Env_Zone1_Plains`, `Env_Zone1_Forests`, `Env_Zone1_Autumn`, `Env_Zone1_Azure`, `Env_Zone1_Mountains_Critter` |
| Zone 2 | `Env_Zone2_Savanna`, `Env_Zone2_Desert` |
| Zone 3 | `Env_Zone3_Tundra` |
| Unique | `Env_Portals_Oasis` |

Check the `Environments` field in vanilla spawn files under each zone directory for the complete list.

---

## Step 5: Test In-Game

1. Place your mod folder in the server mods directory.
2. Start the server and watch for errors about unknown NPC IDs or invalid environment names.
3. Use the developer NPC spawner to verify your NPC roles work independently.
4. Travel to the appropriate biome during the correct time of day.
5. For nocturnal spawns, wait until nightfall and move away from light sources.
6. Check that flock sizes match your configuration.
7. For moon phase testing, advance the game clock through multiple days.

**Common errors and fixes:**

| Error | Cause | Fix |
|-------|-------|-----|
| NPC never spawns naturally | Wrong environment ID | Cross-reference environment names with vanilla spawn files in the same zone |
| NPC spawns at wrong time | `DayTimeRange` reversed | For nocturnal, use `[19, 5]` not `[5, 19]` |
| Too many or too few spawns | `Weight` imbalanced | Compare to vanilla weights: critters use 2-6, predators use 3-5 |
| NPC spawns in mid-air | Wrong `SpawnBlockSet` | Use `"Soil"` for ground creatures, `"Birds"` only for flying NPCs |
| Void creatures persist at dawn | Missing `Despawn` | Add `"Despawn": { "DayTimeRange": [5, 19] }` |

---

## Next Steps

- [Create a Custom NPC](/hytale-modding-docs/tutorials/beginner/create-an-npc) -- define the NPC role that your spawn rules reference
- [Custom Loot Tables](/hytale-modding-docs/tutorials/intermediate/custom-loot-tables) -- set up what your spawned NPCs drop when defeated
- [Projectile Weapons](/hytale-modding-docs/tutorials/intermediate/projectile-weapons) -- create weapons for fighting your spawned predators
