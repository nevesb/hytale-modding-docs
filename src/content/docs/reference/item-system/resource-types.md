---
title: Resource Types
description: Reference for resource type JSON files in Hytale, which define named ingredient categories used as flexible recipe inputs.
---

## Overview

Resource types are named ingredient categories that allow crafting recipes to accept any item belonging to a group rather than requiring a specific item ID. For example, a recipe with `ResourceTypeId: "Meats"` will accept any item tagged with the `Meats` resource type. Items declare their resource type membership via the `ResourceTypes` array in their item definition.

## File Location

```
Assets/Server/Item/ResourceTypes/<ResourceTypeId>.json
```

## Schema

Resource type files are minimal. Most contain only an icon path; the membership list is defined on the item side via `ResourceTypes` in each item definition.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Icon` | string | No | — | Path to the icon image displayed in recipe UI to represent this resource type (e.g. `"Icons/ResourceTypes/Any_Meat.png"`). |

## Available Resource Types (Partial List)

| Resource Type ID | Icon |
|-----------------|------|
| `Bone` | `Icons/ResourceTypes/Any_Bone.png` |
| `Books` | — |
| `Bricks` | — |
| `Charcoal` | — |
| `Clays` | — |
| `Copper_Iron_Bar` | — |
| `Fish` | — |
| `Fish_Common` | — |
| `Fish_Epic` | — |
| `Fish_Legendary` | — |
| `Fish_Rare` | — |
| `Fish_Uncommon` | — |
| `Flowers` | — |
| `Foods` | — |
| `Fruits` | — |
| `Fuel` | `Icons/ResourceTypes/Fuel.png` |
| `Ice` | — |
| `Meats` | `Icons/ResourceTypes/Any_Meat.png` |
| `Metal_Bars` | `Icons/ResourceTypes/Rock.png` |
| `Milk_Bucket` | — |
| `Moss` | — |
| `Mushrooms` | — |
| `Rock` | — |
| `Rubble` | — |
| `Salvage_*` | — |
| `Sands` | — |
| `Soils` | — |
| `Vegetables` | — |
| `Wood_All` | — |
| `Wood_Trunk` | — |

## Examples

`Assets/Server/Item/ResourceTypes/Meats.json`:

```json
{
  "Icon": "Icons/ResourceTypes/Any_Meat.png"
}
```

`Assets/Server/Item/ResourceTypes/Fuel.json`:

```json
{
  "Icon": "Icons/ResourceTypes/Fuel.png"
}
```

`Assets/Server/Item/ResourceTypes/Foods.json`:

```json
{}
```

## How Items Declare Resource Type Membership

In an item definition, add a `ResourceTypes` array with one entry per type the item belongs to:

```json
{
  "ResourceTypes": [
    { "Id": "Meats" }
  ]
}
```

An item can belong to multiple resource types. For example, `Food_Fish_Raw` belongs to both `Fish` and the parent template's food types.

## How Recipes Reference Resource Types

In a recipe `Input` entry, use `ResourceTypeId` instead of `ItemId`:

```json
{
  "Recipe": {
    "Input": [
      {
        "ResourceTypeId": "Fuel",
        "Quantity": 3
      },
      {
        "ResourceTypeId": "Fish",
        "Quantity": 1
      }
    ]
  }
}
```

This allows the recipe to accept any item tagged with the matching resource type, rather than requiring one specific item.

## Related Pages

- [Item Definitions](/hytale-modding-docs/reference/item-system/item-definitions) — Where `ResourceTypes` membership is declared on items
- [Item Groups](/hytale-modding-docs/reference/item-system/item-groups) — Named block sets (complementary grouping system)
- [Item Categories](/hytale-modding-docs/reference/item-system/item-categories) — UI category hierarchy for menus
