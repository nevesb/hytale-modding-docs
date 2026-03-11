---
title: World Masks
description: Reference for world mask definitions in Hytale, which control continent shape, temperature gradients, climate zones, and biome-to-colour mapping for procedural world generation.
---

## Overview

World mask files define the large-scale structure of the procedural world. The top-level `Mask.json` ties together continent shape, temperature, intensity, and climate sub-masks, and declares unique zones (spawn points, temples). Sub-mask files use noise generators and distance-based falloffs to produce scalar fields that the world generator samples to decide which biome occupies a given coordinate. A companion `Zones.json` file maps mask colours to named zone lists.

## File Location

```
Assets/Server/World/
  Default/
    Mask.json
    World.json
    Zones.json
    Mask/
      Blend_Inner.json
      Blend_Outer.json
      Continent.json
      Intensity.json
      Temperature.json
      Climate/
        Cold.json
        Hot.json
        Temperate.json
        Island/
          Tier1.json
          Tier2.json
          Tier3.json
      Continent/
        Blend_Inner.json
        Blend_Outer.json
        Continent_Inner.json
        Continent_Outer.json
      Temperature/
        Temperature_Inner.json
        Temperature_Outer.json
  Flat/
  Void/
  Instance_Creative_Hub/
  Instance_Dungeon_Goblin/
  Instance_Forgotten_Temple/
```

## Schema

### Mask.json (top-level)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Randomizer` | `Randomizer` | No | — | Global noise randomizer applied to all mask sampling. |
| `Noise` | `NoiseConfig` | Yes | — | References to continent, temperature, and intensity sub-masks, plus land/ocean thresholds. |
| `Climate` | `ClimateConfig` | Yes | — | Climate zone definitions and blending parameters. |
| `UniqueZones` | `UniqueZone[]` | No | `[]` | Named zones placed at specific world locations (e.g. spawn, temples). |

### Randomizer

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Generators` | `Generator[]` | Yes | — | Array of noise generators contributing to randomisation. |

### Generator

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Seed` | `string` | No | — | Deterministic seed string. |
| `NoiseType` | `string` | Yes | — | Noise algorithm: `"SIMPLEX"`, `"OLD_SIMPLEX"`, `"POINT"`. |
| `Scale` | `number` | Yes | — | Spatial scale of the noise. |
| `Amplitude` | `number` | No | `1` | Output amplitude multiplier. |
| `Octaves` | `number` | No | `1` | Number of fractal octaves. |
| `Persistence` | `number` | No | `0.5` | Amplitude decay per octave. |
| `Lacunarity` | `number` | No | `2.0` | Frequency multiplier per octave. |

### NoiseConfig

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Thresholds` | `Thresholds` | Yes | — | Scalar thresholds that separate land, island, beach, and shallow ocean. |
| `Continent` | `FileRef` | Yes | — | Reference to the continent shape sub-mask. |
| `Temperature` | `FileRef` | Yes | — | Reference to the temperature gradient sub-mask. |
| `Intensity` | `FileRef` | Yes | — | Reference to the intensity sub-mask. |

### Thresholds

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Land` | `number` | Yes | — | Noise value above which terrain is considered land. |
| `Island` | `number` | Yes | — | Noise value above which terrain is considered an island. |
| `BeachSize` | `number` | Yes | — | Width of the beach transition band. |
| `ShallowOceanSize` | `number` | Yes | — | Width of the shallow ocean band around land. |

### ClimateConfig

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `FadeMode` | `string` | No | `"CHILDREN"` | How climate boundaries fade: `"CHILDREN"` uses per-child settings. |
| `FadeRadius` | `number` | No | — | Radius of the climate transition zone. |
| `FadeDistance` | `number` | No | — | Distance over which the fade occurs. |
| `Climates` | `FileRef[]` | Yes | — | References to individual climate definition files. |

### Climate Definition (e.g. Cold.json)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Name` | `string` | Yes | — | Display name for this climate (e.g. `"Zone 3"`). |
| `Color` | `string` | Yes | — | Hex colour used to represent this climate on debug maps. |
| `Points` | `ClimatePoint[]` | Yes | — | Temperature/intensity coordinates that define where this climate appears. |
| `Children` | `ClimateTier[]` | No | `[]` | Sub-tiers within this climate with distinct biome colours and island configs. |

### ClimateTier

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Name` | `string` | Yes | — | Tier display name (e.g. `"Tier 1"`). |
| `Color` | `string` | Yes | — | Hex colour for this tier's land biome. |
| `Shore` | `string` | No | — | Hex colour for shore areas in this tier. |
| `Ocean` | `string` | No | — | Hex colour for deep ocean in this tier. |
| `ShallowOcean` | `string` | No | — | Hex colour for shallow ocean in this tier. |
| `Island` | `FileRef` | No | — | Reference to an island mask file for this tier. |
| `Points` | `ClimatePoint[]` | Yes | — | Climate coordinates with optional `Modifier`. |

### ClimatePoint

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Temperature` | `number` | Yes | — | Temperature axis value (0–1). |
| `Intensity` | `number` | Yes | — | Intensity axis value (0–1). |
| `Modifier` | `number` | No | `1` | Blending modifier for tier transitions. |

### UniqueZone

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Name` | `string` | Yes | — | Zone identifier referenced by biome and Zones.json colour mapping. |
| `Parent` | `string` | No | — | Name of a parent unique zone for relative placement. |
| `Color` | `string` | Yes | — | Hex colour for debug map rendering. |
| `Radius` | `number` | Yes | — | Radius of the zone in chunks. |
| `OriginX` | `number` | Yes | — | X origin for distance calculations. |
| `OriginY` | `number` | Yes | — | Y origin for distance calculations. |
| `Distance` | `number` | Yes | — | Maximum distance from origin to search for placement. |
| `MinDistance` | `number` | No | `0` | Minimum distance from origin (creates an annular search area). |
| `Rule` | `PlacementRule` | Yes | — | Constraints on continent, temperature, intensity, and fade values. |

### PlacementRule

Each key (`Continent`, `Temperature`, `Intensity`, `Fade`) contains:

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Target` | `number` | Yes | — | Ideal mask value for placement. |
| `Radius` | `number` | Yes | — | Acceptable deviation from the target. |
| `Weight` | `number` | Yes | — | Importance of this constraint relative to others. |

### Sub-mask Types

Sub-mask files use a `Type` field to define their behaviour:

| Type | Description | Key Fields |
|------|-------------|------------|
| `DISTORTED` | Point-based mask with noise distortion | `Noise` (with `NoiseType`, `X`, `Y`, `InnerRadius`, `OuterRadius`), `Randomizer` |
| `BLEND` | Blends two child masks using an alpha mask | `Alpha` (FileRef), `Noise` (FileRef[]), `Thresholds`, `Normalize` |

### Zones.json

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `GridGenerator` | `GridGenerator` | Yes | — | Controls the Voronoi-style grid used to assign zones. |
| `MaskMapping` | `object` | Yes | — | Map of hex colour strings to arrays of zone name strings. |

### GridGenerator

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Scale` | `number` | Yes | — | Grid cell size. |
| `Jitter` | `number` | No | `0` | Random offset applied to grid points (0–1). |
| `Randomizer` | `Randomizer` | No | — | Noise generators for grid jittering. |

### World.json

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Masks` | `string[]` | Yes | — | Array of mask file references (e.g. `["Mask.json"]`). |
| `PrefabStore` | `string` | No | `"ASSETS"` | Source for prefab data: `"ASSETS"` or `"DISK"`. |
| `Height` | `number` | Yes | — | World height in regions. |
| `Width` | `number` | Yes | — | World width in regions. |
| `OffsetX` | `number` | No | `0` | Horizontal origin offset. |
| `OffsetY` | `number` | No | `0` | Vertical origin offset. |
| `Randomizer` | `Randomizer` | No | — | Additional randomizer for world-level noise. |

## Examples

**Top-level mask** (`Assets/Server/World/Default/Mask.json`, condensed):

```json
{
  "Randomizer": {
    "Generators": [
      { "Seed": "RANDOMIZER", "NoiseType": "SIMPLEX", "Scale": 0.01, "Amplitude": 16.0 }
    ]
  },
  "Noise": {
    "Thresholds": {
      "Land": 0.5,
      "Island": 0.75,
      "BeachSize": 0.02,
      "ShallowOceanSize": 0.08
    },
    "Continent": { "File": "Mask.Continent" },
    "Temperature": { "File": "Mask.Temperature" },
    "Intensity": { "File": "Mask.Intensity" }
  },
  "Climate": {
    "FadeMode": "CHILDREN",
    "FadeRadius": 50.0,
    "FadeDistance": 100.0,
    "Climates": [
      { "File": "Mask.Climate.Temperate" },
      { "File": "Mask.Climate.Cold" },
      { "File": "Mask.Climate.Hot" }
    ]
  },
  "UniqueZones": [
    {
      "Name": "Zone1_Spawn",
      "Color": "#ff0000",
      "Radius": 35,
      "OriginX": 0,
      "OriginY": 0,
      "Distance": 3000,
      "Rule": {
        "Continent":   { "Target": 0.0, "Radius": 0.3, "Weight": 1.0 },
        "Temperature": { "Target": 0.5, "Radius": 0.2, "Weight": 1.0 },
        "Intensity":   { "Target": 0.1, "Radius": 0.3, "Weight": 1.0 },
        "Fade":        { "Target": 1.0, "Radius": 0.5, "Weight": 0.5 }
      }
    }
  ]
}
```

**Continent blend sub-mask** (`Assets/Server/World/Default/Mask/Blend_Inner.json`):

```json
{
  "Type": "DISTORTED",
  "Noise": {
    "NoiseType": "POINT",
    "X": 0.0,
    "Y": 0.0,
    "InnerRadius": 1700.0,
    "OuterRadius": 2500.0
  },
  "Randomizer": {
    "Generators": [
      {
        "Seed": "CONTINENT-INNER-WARP-1",
        "NoiseType": "SIMPLEX",
        "Scale": 0.00085,
        "Octaves": 1,
        "Persistence": 0.5,
        "Lacunarity": 2.5,
        "Amplitude": 450
      }
    ]
  }
}
```

## Related Pages

- [World Generation](/hytale-modding-docs/reference/world-and-environment/world-generation) — the HytaleGenerator pipeline that consumes these masks
- [Environments](/hytale-modding-docs/reference/world-and-environment/environments) — environment files assigned to zones defined by masks
- [Instances](/hytale-modding-docs/reference/game-configuration/instances) — instance configs that select a world definition
