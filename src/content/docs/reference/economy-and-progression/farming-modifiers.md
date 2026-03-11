---
title: Farming Modifiers
description: Reference for farming growth modifier definitions in Hytale, covering water, fertilizer, and light-level multipliers that accelerate crop growth.
---

## Overview

Farming modifiers define environmental conditions that accelerate or enable plant and animal growth. Each modifier specifies a growth-rate multiplier and the conditions under which it applies. The system supports three modifier types: **Water** (proximity to fluids or rain weather), **Fertilizer** (applied via items), and **LightLevel** (ambient or artificial light thresholds). When multiple modifiers are active simultaneously, their multipliers stack to determine the final growth rate.

## File Location

```
Assets/Server/Farming/Modifiers/
```

One JSON file per modifier:

```
Assets/Server/Farming/Modifiers/
  Darkness.json
  Fertilizer.json
  LightLevel.json
  Water.json
```

## Schema

### Common fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Type` | `"Water" \| "LightLevel" \| "Fertilizer"` | Yes | — | Modifier category. Determines which additional fields are relevant. |
| `Modifier` | `number` | Yes | — | Growth-rate multiplier applied when the modifier's conditions are met. Values greater than `1` accelerate growth; a value of `2` doubles the rate, `2.5` multiplies by 2.5x, etc. |

### Water-specific fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Fluids` | `string[]` | No | — | Block IDs of fluid sources that satisfy the water condition when adjacent (e.g. `"Water_Source"`, `"Water"`). |
| `Weathers` | `string[]` | No | — | Weather IDs that satisfy the water condition globally (e.g. `"Zone1_Rain"`, `"Zone1_Storm"`). |

### LightLevel-specific fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `ArtificialLight` | `LightChannelRange` | No | — | Acceptable range for artificial (placed) light sources, defined per RGB channel. |
| `Sunlight` | `Range` | No | — | Acceptable range for sunlight intensity. |
| `RequireBoth` | `boolean` | No | `false` | If `true`, both `ArtificialLight` and `Sunlight` conditions must be met simultaneously. If `false`, either one is sufficient. |

### LightChannelRange

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Red` | `Range` | Yes | — | Acceptable range for the red light channel. |
| `Green` | `Range` | Yes | — | Acceptable range for the green light channel. |
| `Blue` | `Range` | Yes | — | Acceptable range for the blue light channel. |

### Range

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Min` | `number` | Yes | — | Minimum acceptable value (inclusive). |
| `Max` | `number` | Yes | — | Maximum acceptable value (inclusive). |

## Examples

**Water modifier** (`Assets/Server/Farming/Modifiers/Water.json`):

```json
{
  "Type": "Water",
  "Modifier": 2.5,
  "Fluids": [
    "Water_Source",
    "Water"
  ],
  "Weathers": [
    "Zone1_Rain",
    "Zone1_Rain_Light",
    "Zone1_Storm",
    "Zone3_Rain"
  ]
}
```

Crops adjacent to water blocks or exposed to rain weather grow at 2.5x the base rate.

**Light level modifier** (`Assets/Server/Farming/Modifiers/LightLevel.json`):

```json
{
  "Type": "LightLevel",
  "Modifier": 2,
  "ArtificialLight": {
    "Red": { "Min": 5, "Max": 127 },
    "Green": { "Min": 5, "Max": 127 },
    "Blue": { "Min": 5, "Max": 127 }
  },
  "Sunlight": {
    "Min": 5.0,
    "Max": 15.0
  },
  "RequireBoth": false
}
```

Plants receiving sufficient sunlight OR artificial light grow at 2x the base rate.

**Darkness modifier** (`Assets/Server/Farming/Modifiers/Darkness.json`):

```json
{
  "Type": "LightLevel",
  "Modifier": 2,
  "ArtificialLight": {
    "Red": { "Min": 0, "Max": 4 },
    "Green": { "Min": 0, "Max": 4 },
    "Blue": { "Min": 0, "Max": 4 }
  },
  "Sunlight": {
    "Min": 0,
    "Max": 5
  },
  "RequireBoth": true
}
```

Certain shade-loving plants thrive in darkness. Both artificial light AND sunlight must be within the low ranges for this modifier to apply.

**Fertilizer modifier** (`Assets/Server/Farming/Modifiers/Fertilizer.json`):

```json
{
  "Type": "Fertilizer",
  "Modifier": 2
}
```

When fertilizer is applied to a plot, growth rate doubles. The fertilizer type has no additional conditions beyond being applied.

## Related Pages

- [Farming & Coops](/hytale-modding-docs/reference/economy-and-progression/farming-coops) — coop definitions and produce drops that work alongside growth modifiers
- [Drop Tables](/hytale-modding-docs/reference/economy-and-progression/drop-tables) — produce drop tables referenced by farming coops
