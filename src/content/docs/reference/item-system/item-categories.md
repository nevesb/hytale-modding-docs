---
title: Item Categories
description: Reference for item category JSON files in Hytale, defining the hierarchical category tree used in crafting menus and creative library.
---

## Overview

Item categories define the tree structure that organizes items in crafting menus and the creative library. Each JSON file represents one top-level category node and contains an ordered list of child category entries. Items are assigned to categories via the `Categories` array in their item definition.

## File Location

```
Assets/Server/Item/Category/<LibraryId>/<CategoryId>.json
```

The two library roots are:
- `Assets/Server/Item/Category/CreativeLibrary/` — Creative mode item browser (Blocks, Furniture, Items, Tool)
- `Assets/Server/Item/Category/Fieldcraft/` — Survival crafting menus (Tools)

## Schema

### Category File Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Icon` | string | Yes | — | Path to the icon image for this top-level category (e.g. `"Icons/ItemCategories/Natural.png"`). |
| `Order` | number | No | `0` | Sort order of this category relative to its siblings. Lower values appear first. |
| `Name` | string | No | — | Localization key for the category display name (used on leaf/sub-category nodes). |
| `Children` | object[] | No | — | Ordered array of child category entries. |

### Children Entry Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Id` | string | Yes | — | Unique identifier for this child category. Used as the second segment in item `Categories` values (e.g. `"Foods"` maps to `"Items.Foods"`). |
| `Name` | string | Yes | — | Localization key for the child category's display label (e.g. `"server.ui.itemcategory.foods"`). |
| `Icon` | string | Yes | — | Path to the icon image for this child category. |

## Example

`Assets/Server/Item/Category/CreativeLibrary/Blocks.json`:

```json
{
  "Icon": "Icons/ItemCategories/Natural.png",
  "Order": 0,
  "Children": [
    {
      "Id": "Rocks",
      "Name": "server.ui.itemcategory.rocks",
      "Icon": "Icons/ItemCategories/Blocks.png"
    },
    {
      "Id": "Structural",
      "Name": "server.ui.itemcategory.structural",
      "Icon": "Icons/ItemCategories/Build-Roofs.png"
    },
    {
      "Id": "Soils",
      "Name": "server.ui.itemcategory.soils",
      "Icon": "Icons/ItemCategories/Soil.png"
    },
    {
      "Id": "Ores",
      "Name": "server.ui.itemcategory.ores",
      "Icon": "Icons/ItemCategories/Natural-Ore.png"
    },
    {
      "Id": "Plants",
      "Name": "server.ui.itemcategory.plants",
      "Icon": "Icons/ItemCategories/Natural-Vegetal.png"
    },
    {
      "Id": "Fluids",
      "Name": "server.ui.itemcategory.fluids",
      "Icon": "Icons/ItemCategories/Natural-Fluid.png"
    },
    {
      "Id": "Portals",
      "Name": "server.ui.itemcategory.portals",
      "Icon": "Icons/ItemCategories/Portal.png"
    },
    {
      "Id": "Deco",
      "Name": "server.ui.itemcategory.deco",
      "Icon": "Icons/ItemCategories/Natural-Fire.png"
    }
  ]
}
```

`Assets/Server/Item/Category/CreativeLibrary/Items.json`:

```json
{
  "Icon": "Icons/ItemCategories/Items.png",
  "Order": 2,
  "Children": [
    {
      "Id": "Tools",
      "Name": "server.ui.itemcategory.tools",
      "Icon": "Icons/ItemCategories/Items-Tools.png"
    },
    {
      "Id": "Weapons",
      "Name": "server.ui.itemcategory.weapons",
      "Icon": "Icons/ItemCategories/Items-Weapons.png"
    },
    {
      "Id": "Armors",
      "Name": "server.ui.itemcategory.armors",
      "Icon": "Icons/ItemCategories/Items-Armor.png"
    },
    {
      "Id": "Foods",
      "Name": "server.ui.itemcategory.foods",
      "Icon": "Icons/ItemCategories/Items-Food.png"
    },
    {
      "Id": "Potions",
      "Name": "server.ui.itemcategory.potions",
      "Icon": "Icons/ItemCategories/Items-Potion.png"
    },
    {
      "Id": "Recipes",
      "Name": "server.ui.itemcategory.recipes",
      "Icon": "Icons/ItemCategories/Items-Recipe.png"
    },
    {
      "Id": "Ingredients",
      "Name": "server.ui.itemcategory.ingredients",
      "Icon": "Icons/ItemCategories/Items-Ingredients.png"
    }
  ]
}
```

## Assigning Items to Categories

In an item definition file, set the `Categories` field to a list of `"<LibraryId>.<ChildId>"` strings:

```json
{
  "Categories": [
    "Items.Foods"
  ]
}
```

A single item can belong to multiple categories by adding more entries to the array.

## Related Pages

- [Item Definitions](/hytale-modding-docs/reference/item-system/item-definitions) — Where the `Categories` field is set on items
- [Item Groups](/hytale-modding-docs/reference/item-system/item-groups) — Named block/item sets (distinct from categories)
- [Resource Types](/hytale-modding-docs/reference/item-system/resource-types) — Resource groupings used in recipes
