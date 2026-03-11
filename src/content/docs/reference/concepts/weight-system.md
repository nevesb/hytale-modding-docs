---
title: Weight System
description: How Hytale uses weighted random selection for drops, spawns, and trade pools.
---

## Overview

Many Hytale systems use weighted random selection to determine outcomes. Weights are relative numbers — a higher weight means a higher probability of being selected. The total doesn't need to equal 100.

## How Weights Work

Given items with weights `[70, 25, 5]`, the probabilities are:
- Item A: 70/100 = 70%
- Item B: 25/100 = 25%
- Item C: 5/100 = 5%

## How Weight Selection Works

```mermaid
flowchart TD;
    A[Weight Pool] --> B["Item A<br>Weight: 70"];
    A --> C["Item B<br>Weight: 25"];
    A --> D["Item C<br>Weight: 5"];

    B --> E[Total = 100];
    C --> E;
    D --> E;

    E --> F["Roll Random<br>0-100"];
    F -->|"0-70"| G["Item A Selected<br>70% chance"];
    F -->|"71-95"| H["Item B Selected<br>25% chance"];
    F -->|"96-100"| I["Item C Selected<br>5% chance"];

    style G fill:darkgreen,color:white;
    style H fill:steelblue,color:white;
    style I fill:darkgoldenrod,color:white;
```

### Nested Weight Example (Drop Tables)

```mermaid
flowchart TD;
    A[Monster Dies] --> B[Drop Table];
    B --> C{Roll Weight Pool};
    C -->|"Weight: 60"| D[Common Drops];
    C -->|"Weight: 30"| E[Uncommon Drops];
    C -->|"Weight: 10"| F[Rare Drops];

    D --> G{Nested Roll};
    G -->|"Weight: 50"| H[5x Stone];
    G -->|"Weight: 50"| I[3x Wood];

    E --> J{Nested Roll};
    J -->|"Weight: 70"| K[1x Iron Ingot];
    J -->|"Weight: 30"| L[1x Gold Nugget];

    F --> M[1x Diamond];

    style D fill:darkgreen,color:white;
    style E fill:steelblue,color:white;
    style F fill:darkgoldenrod,color:white;
    style M fill:rebeccapurple,color:white;
```

## Systems Using Weights

### Drop Tables

Loot drops use weights within `Choice` containers:

```json
{
  "Container": {
    "Type": "Choice",
    "Containers": [
      { "Weight": 80, "Item": { "ItemId": "Coin_Gold", "QuantityMin": 1, "QuantityMax": 3 } },
      { "Weight": 15, "Item": { "ItemId": "Gem_Ruby" } },
      { "Weight": 5, "Item": { "ItemId": "Sword_Rare" } }
    ]
  }
}
```

### NPC Spawning

Spawn rules weight which NPC appears:

```json
{
  "NPCs": [
    { "Weight": 10, "Id": "Chicken", "Flock": "One_Or_Two" },
    { "Weight": 10, "Id": "Rabbit", "Flock": "Group_Small" },
    { "Weight": 5, "Id": "Deer", "Flock": "One_Or_Two" }
  ]
}
```

### Barter Shops (Pool Slots)

Shop inventory pools select trades by weight:

```json
{
  "Type": "Pool",
  "SlotCount": 2,
  "Trades": [
    { "Weight": 10, "Trade": { "Output": [{ "ItemId": "Food_Apple" }], "Input": [{ "ItemId": "Coin_Gold", "Quantity": 5 }] } },
    { "Weight": 5, "Trade": { "Output": [{ "ItemId": "Food_Pie" }], "Input": [{ "ItemId": "Coin_Gold", "Quantity": 12 }] } }
  ]
}
```

### Weather Forecasts

Hourly weather selection uses weights:

```json
{
  "WeatherForecasts": {
    "6": [
      { "WeatherId": "Zone1_Sunny", "Weight": 60 },
      { "WeatherId": "Zone1_Cloudy", "Weight": 30 },
      { "WeatherId": "Zone1_Rain", "Weight": 10 }
    ]
  }
}
```

## Related Pages

- [Drop Tables](/hytale-modding-docs/reference/economy-and-progression/drop-tables/) — loot weight system
- [NPC Spawn Rules](/hytale-modding-docs/reference/npc-system/npc-spawn-rules/) — spawn weights
- [Barter Shops](/hytale-modding-docs/reference/economy-and-progression/barter-shops/) — trade pool weights
