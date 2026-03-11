---
title: World Generation
description: Reference for world generation files in Hytale, covering the HytaleGenerator pipeline including biomes, density maps, assignments, block masks, and world structure settings.
---

## Overview

World generation in Hytale is driven by a node-graph-based pipeline called **HytaleGenerator**. It produces terrain through layered noise functions, density maps, biome definitions, and weighted prefab assignments. Each component is defined in a separate JSON file and wired together through import/export references. The system supports procedural continent shapes, climate zones, cave networks, river carving, and per-biome scatter placement.

## File Location

```
Assets/Server/HytaleGenerator/
  Assignments/
    Boreal1/
      Boreal1_Hedera_Trees.json
      Boreal1_Hedera_Mushrooms.json
      ...
    Desert1/
    Plains1/
    Volcanic1/
  Biomes/
    Basic.json
    Boreal1/
      Boreal1_Hedera.json
      Boreal1_Henges.json
    Desert1/
    Plains1/
    Volcanic1/
    Default_Flat/
    Default_Void/
  BlockMasks/
  Density/
    Map_Default.json
    Map_Portals.json
    Map_Tiles.json
    Plains1_Caves_Terrain.json
    ...
  Graphs/
  Settings/
    Settings.json
  WorldStructures/
```

## Schema

### Settings (Settings.json)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `StatsCheckpoints` | `number[]` | No | — | Chunk-count thresholds at which generation statistics are logged. |
| `CustomConcurrency` | `number` | No | `-1` | Thread count for generation. `-1` uses the engine default. |
| `BufferCapacityFactor` | `number` | No | `0.1` | Fraction of total memory allocated to generation buffers. |
| `TargetViewDistance` | `number` | No | `512` | Target view distance in blocks used to pre-compute generation priority. |
| `TargetPlayerCount` | `number` | No | `3` | Expected player count used to size generation queues. |

### Density Node (node-graph files)

Density files define a tree of processing nodes that produce a scalar field used for terrain shape, river carving, or biome mapping. Every node has at minimum:

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `$NodeId` | `string` | Yes | — | Unique identifier for this node in the graph. |
| `Type` | `string` | Yes | — | Node type. See node types below. |
| `Skip` | `boolean` | No | `false` | When `true`, the node is bypassed during generation. |
| `ExportAs` | `string` | No | — | Name under which this node's output is published for import by other graphs. |
| `SingleInstance` | `boolean` | No | `false` | When `true`, the node is evaluated once and cached globally. |
| `Inputs` | `DensityNode[]` | No | `[]` | Child nodes whose outputs feed into this node. |

#### Common Density Node Types

| Type | Description | Key Fields |
|------|-------------|------------|
| `SimplexNoise2D` | 2D simplex noise generator | `Lacunarity`, `Persistence`, `Octaves`, `Scale`, `Seed` |
| `Constant` | Outputs a fixed value | `Value` |
| `Sum` | Adds all input values | — |
| `Min` / `Max` | Returns the minimum or maximum of inputs | — |
| `Clamp` | Clamps input between two walls | `WallA`, `WallB` |
| `Normalizer` | Remaps a value range | `FromMin`, `FromMax`, `ToMin`, `ToMax` |
| `Inverter` | Negates the input | — |
| `Abs` | Absolute value | — |
| `Mix` | Blends two inputs using a third as alpha | — |
| `Scale` | Multiplies input coordinates | `ScaleX`, `ScaleY`, `ScaleZ` |
| `Cache` | Caches the result of child nodes | `Capacity` |
| `YOverride` | Forces a fixed Y coordinate for 2D evaluation | `Value` |
| `Distance` | Distance from origin with a falloff curve | `Curve` |
| `Exported` | Marks a node's output for cross-graph import | `ExportAs`, `SingleInstance` |
| `Imported` | References an exported node by name | `Name` |

### Assignment (scatter/prefab placement)

Assignment files control what decorations, vegetation, or structures are placed in a biome region. They use a field-function approach with delimiters.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Type` | `string` | Yes | — | Top-level type, typically `"FieldFunction"`. |
| `ExportAs` | `string` | No | — | Export name for this assignment. |
| `FieldFunction` | `FieldFunction` | Yes | — | Noise function that produces the placement density field. |
| `Delimiters` | `Delimiter[]` | Yes | — | Ranges within the field function output that trigger placement. |

#### FieldFunction

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Type` | `string` | Yes | — | Noise type, e.g. `"SimplexNoise2D"`. |
| `Skip` | `boolean` | No | `false` | Bypass this function. |
| `Lacunarity` | `number` | No | `2` | Frequency multiplier per octave. |
| `Persistence` | `number` | No | `0.5` | Amplitude multiplier per octave. |
| `Octaves` | `number` | No | `1` | Number of noise octaves. |
| `Scale` | `number` | Yes | — | Spatial scale of the noise. |
| `Seed` | `string` | Yes | — | Seed string for deterministic generation. |

#### Delimiter

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Min` | `number` | Yes | — | Minimum field value for this range. |
| `Max` | `number` | Yes | — | Maximum field value for this range. |
| `Assignments` | `AssignmentNode` | Yes | — | What to place when the field value falls in this range. |

#### AssignmentNode

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Type` | `string` | Yes | — | `"Weighted"`, `"Constant"`, or `"Cluster"`. |
| `SkipChance` | `number` | No | `0` | Probability (0–1) of skipping placement entirely. |
| `Seed` | `string` | No | — | Seed for weighted random selection. |
| `WeightedAssignments` | `WeightedEntry[]` | No | — | Array of weighted options (when `Type` is `"Weighted"`). |
| `Prop` | `PropConfig` | No | — | Prefab/prop to place (when `Type` is `"Constant"` or within a weighted entry). |

## Example

**Density map** (`Assets/Server/HytaleGenerator/Density/Map_Default.json`, condensed to show structure):

```json
{
  "$NodeId": "Exported.Density-ed27c3c9",
  "Type": "Exported",
  "ExportAs": "Biome-Map",
  "SingleInstance": true,
  "Inputs": [
    {
      "Type": "YOverride",
      "Value": 0,
      "Inputs": [
        {
          "Type": "Cache",
          "Capacity": 1,
          "Inputs": [
            {
              "Type": "Mix",
              "Inputs": [
                { "Type": "Imported", "Name": "Biome-Map-Tiles" },
                { "Type": "Constant", "Value": -0.3 },
                {
                  "Type": "Clamp",
                  "WallA": 0,
                  "WallB": 1,
                  "Inputs": [
                    {
                      "Type": "Normalizer",
                      "FromMin": 0.62,
                      "FromMax": 0.62,
                      "ToMin": 0,
                      "ToMax": 1,
                      "Inputs": [
                        { "Type": "Exported", "ExportAs": "World-River-Map" }
                      ]
                    }
                  ]
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

**Generator settings** (`Assets/Server/HytaleGenerator/Settings/Settings.json`):

```json
{
  "StatsCheckpoints": [1, 100, 500, 1000],
  "CustomConcurrency": -1,
  "BufferCapacityFactor": 0.1,
  "TargetViewDistance": 512,
  "TargetPlayerCount": 3
}
```

## Related Pages

- [World Masks](/hytale-modding-docs/reference/world-and-environment/world-masks) — noise masks for continent shape, temperature, and climate
- [Environments](/hytale-modding-docs/reference/world-and-environment/environments) — environment definitions assigned per zone
- [Instances](/hytale-modding-docs/reference/game-configuration/instances) — instance configs that select a world generation profile
