---
title: Farming & Coops
description: Reference for farming coop definitions and growth modifiers in Hytale, including resident NPC groups, produce drop tables, roam schedules, and environmental modifiers.
---

## Overview

The farming system has two asset types: **Coops** and **Modifiers**. Coops define pens that house NPC animals and produce drops over time — they specify which NPC groups can live in the coop, how many residents are allowed, and which drop table each species produces. Modifiers define environmental multipliers (water, light, fertilizer) that accelerate plant or animal growth rates.

## File Location

```
Assets/Server/Farming/
  Coops/
    Coop_Chicken.json
  Modifiers/
    Darkness.json
    Fertilizer.json
    LightLevel.json
    Water.json
```

## Coop Schema

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `MaxResidents` | `number` | Yes | — | Maximum number of NPC residents the coop can hold simultaneously. |
| `ProduceDrops` | `object` | Yes | — | Map of NPC group ID → drop table ID. Each resident species has its own produce drop table. |
| `ResidentRoamTime` | `[number, number]` | Yes | — | In-game hour range `[start, end]` during which residents roam freely inside the coop. |
| `ResidentSpawnOffset` | `Vector3` | No | — | Local offset applied when spawning a resident inside the coop structure. |
| `AcceptedNpcGroups` | `string[]` | Yes | — | List of NPC group IDs that can be placed into or captured into this coop type. |
| `CaptureWildNPCsInRange` | `boolean` | No | `false` | If `true`, wild NPCs of accepted groups within range are automatically captured into the coop. |
| `WildCaptureRadius` | `number` | No | — | Radius in units within which wild NPCs are auto-captured when `CaptureWildNPCsInRange` is `true`. |

### Vector3

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `X` | `number` | Yes | — | Lateral offset. |
| `Y` | `number` | Yes | — | Vertical offset. |
| `Z` | `number` | Yes | — | Forward offset. |

## Modifier Schema

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Type` | `"Water" \| "Fertilizer" \| "LightLevel" \| "Darkness"` | Yes | — | Category of modifier, used to match the modifier against applicable growth systems. |
| `Modifier` | `number` | Yes | — | Growth rate multiplier applied when this modifier's conditions are satisfied (e.g. `2.5` = 2.5× faster). |
| `Fluids` | `string[]` | No | — | `Water` type only. Fluid block IDs whose presence satisfies the water condition. |
| `Weathers` | `string[]` | No | — | `Water` type only. Weather IDs that also count as a water source (e.g. rain). |
| `ArtificialLight` | `LightRange` | No | — | `LightLevel` type only. RGB channel ranges that must be met by artificial light sources. |
| `Sunlight` | `SunlightRange` | No | — | `LightLevel` type only. Sunlight level range that must be met. |
| `RequireBoth` | `boolean` | No | `false` | `LightLevel` type only. If `true`, both `ArtificialLight` and `Sunlight` conditions must be met simultaneously. |

### LightRange (per RGB channel)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Min` | `number` | Yes | — | Minimum light level (0–255). |
| `Max` | `number` | Yes | — | Maximum light level (0–255). |

### SunlightRange

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Min` | `number` | Yes | — | Minimum sunlight level (0–15). |
| `Max` | `number` | Yes | — | Maximum sunlight level (0–15). |

## Examples

**Chicken coop** (`Assets/Server/Farming/Coops/Coop_Chicken.json`):

```json
{
  "MaxResidents": 6,
  "ProduceDrops": {
    "Chicken": "Drop_Chicken_Produce",
    "Chicken_Desert": "Drop_Chicken_Produce",
    "Skrill": "Drop_Chicken_Produce"
  },
  "ResidentRoamTime": [6, 18],
  "ResidentSpawnOffset": {
    "X": 0,
    "Y": 0,
    "Z": 3
  },
  "AcceptedNpcGroups": [
    "Chicken",
    "Chicken_Desert",
    "Skrill"
  ],
  "CaptureWildNPCsInRange": true,
  "WildCaptureRadius": 10
}
```

**Water modifier** (`Assets/Server/Farming/Modifiers/Water.json`):

```json
{
  "Type": "Water",
  "Modifier": 2.5,
  "Fluids": ["Water_Source", "Water"],
  "Weathers": ["Zone1_Rain", "Zone1_Rain_Light", "Zone1_Storm", "Zone3_Rain"]
}
```

**Fertilizer modifier** (`Assets/Server/Farming/Modifiers/Fertilizer.json`):

```json
{
  "Type": "Fertilizer",
  "Modifier": 2
}
```

**Light level modifier** (`Assets/Server/Farming/Modifiers/LightLevel.json`):

```json
{
  "Type": "LightLevel",
  "Modifier": 2,
  "ArtificialLight": {
    "Red":   { "Min": 5, "Max": 127 },
    "Green": { "Min": 5, "Max": 127 },
    "Blue":  { "Min": 5, "Max": 127 }
  },
  "Sunlight": {
    "Min": 5.0,
    "Max": 15.0
  },
  "RequireBoth": false
}
```

## Related Pages

- [Drop Tables](/hytale-modding-docs/reference/economy-and-progression/drop-tables) — drop table format used in `ProduceDrops`
- [Weather System](/hytale-modding-docs/reference/world-and-environment/weather-system) — weather IDs referenced in `Water.Weathers`
- [Barter Shops](/hytale-modding-docs/reference/economy-and-progression/barter-shops) — selling farm produce
