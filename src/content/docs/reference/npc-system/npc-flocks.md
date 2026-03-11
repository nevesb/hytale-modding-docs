---
title: NPC Flocks
description: Flock definitions that control how many NPCs spawn together as a group, with weighted size selection.
---

## Overview

Flock files define group spawning behavior — how many NPCs appear together when a spawn event triggers. The system supports two modes: **Weighted** (randomly selects a group size from weighted probabilities) and **Range** (picks a random size within a min/max range). Flocks are referenced by spawn rules via the `Flock` field.

## How Flock Sizing Works

```mermaid
flowchart TD;
    A[Spawn Event Triggers] --> B{Flock Type?};

    B -->|"Weighted"| C[Roll Weighted Sizes];
    B -->|"Range / Size array"| D["Pick Random<br>in Range"];

    C --> E["MinSize = 3<br>Weights: 60, 25, 15"];
    E --> F{Roll};
    F -->|"60%"| G[Spawn 3 NPCs];
    F -->|"25%"| H[Spawn 4 NPCs];
    F -->|"15%"| I[Spawn 5 NPCs];

    D --> J[Size: 2, 3];
    J --> K[Spawn 2-3 NPCs];

    G --> L["MaxGrowSize<br>Defined?"];
    H --> L;
    I --> L;
    K --> L;

    L -->|"Yes"| M["Group can grow<br>up to MaxGrowSize<br>over time"];
    L -->|"No"| N["Group stays<br>at spawned size"];

    style A fill:darkgreen,color:white;
    style G fill:steelblue,color:white;
    style H fill:steelblue,color:white;
    style I fill:steelblue,color:white;```

## File Location

```
Assets/Server/NPC/Flocks/
  Group_Small.json
  Group_Medium.json
  Group_Large.json
  Group_Tiny.json
  Pack_Small.json
  One_Or_Two.json
  Parent_And_Young_75_25.json
  EasterEgg_Pair.json
```

## Schema

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Type` | string | No | — | Sizing mode. `"Weighted"` uses `MinSize` + `SizeWeights`. Omit for simple range mode. |
| `MinSize` | integer | Yes* | — | Minimum group size. Required for `Weighted` type. Starting size for weight index 0. |
| `SizeWeights` | number[] | Yes* | — | Relative weights for each size starting at `MinSize`. Required for `Weighted` type. |
| `Size` | [number, number] | No | — | Simple min/max range for group size (alternative to Weighted). |
| `MaxGrowSize` | integer | No | — | Maximum size the group can grow to over time (e.g. through breeding). |

### How SizeWeights Work

For `MinSize: 3` and `SizeWeights: [60, 25, 15]`:

| Index | Size | Weight | Probability |
|-------|------|--------|-------------|
| 0 | 3 (MinSize + 0) | 60 | 60% |
| 1 | 4 (MinSize + 1) | 25 | 25% |
| 2 | 5 (MinSize + 2) | 15 | 15% |

## Examples

### Small group (3-5 NPCs, weighted)

```json
{
  "Type": "Weighted",
  "MinSize": 3,
  "SizeWeights": [60, 25, 15]
}
```

60% chance of 3, 25% chance of 4, 15% chance of 5.

### Large group (5-7 NPCs, weighted)

```json
{
  "Type": "Weighted",
  "MinSize": 5,
  "SizeWeights": [60, 20, 20]
}
```

### Parent and young (1-2, growable)

```json
{
  "Type": "Weighted",
  "MinSize": 1,
  "SizeWeights": [75, 25],
  "MaxGrowSize": 8
}
```

75% chance of 1, 25% chance of 2. Group can grow up to 8 over time.

### Simple range (2-3 NPCs)

```json
{
  "Size": [2, 3]
}
```

No weights — just a random pick between 2 and 3.

## Available Flocks

| Flock ID | Type | Sizes | Notes |
|----------|------|-------|-------|
| `Group_Tiny` | Weighted | 1-2 | Very small groups |
| `Group_Small` | Weighted | 3-5 | Common passive animals |
| `Group_Medium` | Weighted | 4-6 | Medium herds |
| `Group_Large` | Weighted | 5-7 | Large herds |
| `Pack_Small` | Range | 2-3 | Predator packs |
| `One_Or_Two` | Range | 1-2 | Solitary or paired |
| `Parent_And_Young_75_25` | Weighted | 1-2 | Breeding pairs, grows to 8 |
| `EasterEgg_Pair` | Range | 2 | Easter egg spawns |

## Related Pages

- [NPC Spawn Rules](/hytale-modding-docs/reference/npc-system/npc-spawn-rules/) — Where flocks are referenced via the `Flock` field
- [NPC Groups](/hytale-modding-docs/reference/npc-system/npc-groups/) — Logical grouping of NPC types
- [Weight System](/hytale-modding-docs/reference/concepts/weight-system/) — How weighted selection works
