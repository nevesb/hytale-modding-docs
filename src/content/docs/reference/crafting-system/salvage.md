---
title: Salvage
description: Reference for salvage recipe definitions in Hytale, which break down items into their constituent materials at a Salvage Bench.
---

## Overview

Salvage recipes define how existing items are broken down into raw materials at the Salvage Bench. They use the same base recipe schema as crafting recipes but always have exactly one input item, multiple outputs, and a `BenchRequirement` pointing to the `"Salvagebench"` processing bench. The `PrimaryOutput` field identifies the most valuable recovered material shown in the UI.

## File Location

```
Assets/Server/Item/Recipes/Salvage/
```

One JSON file per salvageable item, named `Salvage_<ItemId>.json`, e.g. `Salvage_Armor_Adamantite_Chest.json`.

## Schema

Salvage recipes share the full [recipe schema](/hytale-modding-docs/reference/crafting-system/recipes). The fields used in practice are:

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Input` | `InputEntry[]` | Yes | — | Single-element array identifying the item to salvage. Always uses `ItemId`. |
| `Input[].ItemId` | `string` | Yes | — | The item ID being salvaged. |
| `Input[].Quantity` | `number` | Yes | — | Always `1` for salvage. |
| `PrimaryOutput` | `OutputEntry` | Yes | — | The primary recovered material shown as the headline result in the UI. |
| `PrimaryOutput.ItemId` | `string` | Yes | — | Item ID of the primary recovered material. |
| `PrimaryOutput.Quantity` | `number` | Yes | — | Amount of the primary material recovered. |
| `Output` | `OutputEntry[]` | Yes | — | Full list of all materials recovered, including the primary output and any secondary materials. |
| `Output[].ItemId` | `string` | Yes | — | Item ID of the recovered material. |
| `Output[].Quantity` | `number` | Yes | — | Amount recovered. |
| `BenchRequirement` | `BenchRequirement[]` | Yes | — | Always `[{ "Type": "Processing", "Id": "Salvagebench" }]`. |
| `TimeSeconds` | `number` | Yes | — | Processing time in seconds at the Salvage Bench. |

## Examples

**Adamantite chest piece** (`Salvage_Armor_Adamantite_Chest.json`):

```json
{
  "Input": [
    {
      "ItemId": "Armor_Adamantite_Chest",
      "Quantity": 1
    }
  ],
  "PrimaryOutput": {
    "ItemId": "Ore_Adamantite",
    "Quantity": 6
  },
  "Output": [
    {
      "ItemId": "Ore_Adamantite",
      "Quantity": 6
    },
    {
      "ItemId": "Ingredient_Hide_Heavy",
      "Quantity": 2
    },
    {
      "ItemId": "Ingredient_Fabric_Scrap_Cindercloth",
      "Quantity": 2
    }
  ],
  "BenchRequirement": [
    {
      "Type": "Processing",
      "Id": "Salvagebench"
    }
  ],
  "TimeSeconds": 4
}
```

**Cotton cloth chest piece** (`Salvage_Armor_Cloth_Cotton_Chest.json`):

```json
{
  "Input": [
    {
      "ItemId": "Armor_Cloth_Cotton_Chest",
      "Quantity": 1
    }
  ],
  "PrimaryOutput": {
    "ItemId": "Ingredient_Fabric_Scrap_Cotton",
    "Quantity": 4
  },
  "Output": [
    {
      "ItemId": "Ingredient_Fabric_Scrap_Cotton",
      "Quantity": 4
    }
  ],
  "BenchRequirement": [
    {
      "Type": "Processing",
      "Id": "Salvagebench"
    }
  ],
  "TimeSeconds": 2
}
```

## Related Pages

- [Recipes](/hytale-modding-docs/reference/crafting-system/recipes) — base recipe schema
- [Bench Definitions](/hytale-modding-docs/reference/crafting-system/bench-definitions) — Salvage Bench item definition
