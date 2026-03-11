---
title: Drop Tables
description: Reference for drop table definitions in Hytale, covering container types, item entries, weights, and nested container structures.
---

## Overview

Drop tables define what items are produced when a container is opened, an NPC is killed, or a resource node is harvested. The system uses a recursive `Container` structure that supports three selection modes: `Single` (always produces one item), `Choice` (randomly picks one child by weight), and `Multiple` (evaluates all children). Nesting these types enables complex weighted loot tables with guaranteed and optional drops.

## How Drop Tables Work

```mermaid
flowchart TD;
    A[NPC Dies / Block Breaks] --> B[Lookup Drop Table];
    B --> C{Container Type?};

    C -->|"Multiple"| D[Evaluate ALL Children];
    C -->|"Choice"| E[Pick ONE by Weight];
    C -->|"Single"| F[Always Drop This Item];

    D --> G["Child 1: Guaranteed<br>Single → 3x Bone"];
    D --> H["Child 2: Random Loot<br>Choice → Weighted Pool"];

    H --> I{Roll Weights};
    I -->|"Weight: 60"| J["Common:<br>5x Stone"];
    I -->|"Weight: 30"| K["Uncommon:<br>1x Iron"];
    I -->|"Weight: 10"| L["Rare:<br>1x Diamond"];

    G --> M[Final Drops];
    J --> M;
    K --> M;
    L --> M;

    style A fill:darkred,color:white;
    style M fill:darkgreen,color:white;
    style L fill:darkgoldenrod,color:white;```

### Container Nesting Example

```mermaid
flowchart TD;
    A[Root: Multiple] --> B["Single<br>1x XP Orb<br>Guaranteed"];
    A --> C["Choice<br>Weighted random"];
    A --> D["Choice<br>Weighted random"];

    C -->|"70%"| E[Nothing];
    C -->|"30%"| F[1x Feather];

    D -->|"90%"| G[Nothing];
    D -->|"10%"| H[1x Rare Egg];

    style B fill:darkgreen,color:white;
    style F fill:steelblue,color:white;
    style H fill:darkgoldenrod,color:white;```

## File Location

```
Assets/Server/Drops/
  Items/          (world containers: barrels, pots, coffins)
  NPCs/
    Beast/
    Boss/
    Critter/
    Elemental/
    Flying_Beast/
    Flying_Critter/
    Flying_Wildlife/
    Intelligent/
    Inventory/
  Objectives/
  Plant/
  Rock/
  Wood/
```

## Schema

### Top-level

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Container` | `Container` | Yes | — | Root container node that defines the loot logic. |

### Container

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Type` | `"Single" \| "Multiple" \| "Choice" \| "Empty"` | Yes | — | Selection mode for this container node. |
| `Item` | `ItemEntry` | No | — | The item to produce. Only valid when `Type` is `"Single"`. |
| `Containers` | `Container[]` | No | — | Child containers. Used by `Multiple` and `Choice` types. |
| `Weight` | `number` | No | — | Relative probability weight. Used by parent `Choice` containers when selecting among siblings. |

### Container Types

| Type | Behaviour |
|------|-----------|
| `Single` | Always produces exactly the item defined in `Item`. |
| `Multiple` | Evaluates every child container independently and combines all results. |
| `Choice` | Randomly selects one child container weighted by each child's `Weight` field. |
| `Empty` | Produces nothing. Used as a weighted "no drop" option inside `Choice` nodes. |

### ItemEntry

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `ItemId` | `string` | Yes | — | ID of the item to produce. |
| `QuantityMin` | `number` | Yes | — | Minimum stack size produced. |
| `QuantityMax` | `number` | Yes | — | Maximum stack size produced. Actual quantity is chosen uniformly between min and max. |

## Examples

**World container with weighted choice drops** (`Assets/Server/Drops/Items/Barrels.json`):

```json
{
  "Container": {
    "Type": "Choice",
    "Containers": [
      {
        "Type": "Choice",
        "Weight": 100,
        "Containers": [
          {
            "Type": "Single",
            "Item": {
              "ItemId": "Plant_Fruit_Apple",
              "QuantityMin": 1,
              "QuantityMax": 1
            }
          }
        ]
      },
      {
        "Type": "Choice",
        "Weight": 25,
        "Containers": [
          {
            "Type": "Single",
            "Item": {
              "ItemId": "Weapon_Arrow_Crude",
              "QuantityMin": 1,
              "QuantityMax": 5
            }
          }
        ]
      },
      {
        "Type": "Empty",
        "Weight": 800
      }
    ]
  }
}
```

**NPC drop with guaranteed multiple drops** (`Assets/Server/Drops/NPCs/Beast/Drop_Bear_Grizzly.json`):

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

The `Multiple` root ensures the bear always drops both hide and meat. Each child uses a `Choice` with weight 100 (the only non-empty option), making each individual drop guaranteed.

## Related Pages

- [Barter Shops](/hytale-modding-docs/reference/economy-and-progression/barter-shops) — merchant trade slots
- [Farming & Coops](/hytale-modding-docs/reference/economy-and-progression/farming-coops) — `ProduceDrops` field references drop table IDs
- [Recipes](/hytale-modding-docs/reference/crafting-system/recipes) — crafting as an alternative to drops
