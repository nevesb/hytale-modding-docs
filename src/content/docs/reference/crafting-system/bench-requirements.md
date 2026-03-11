---
title: Bench Requirements
description: Reference for the BenchRequirement field in Hytale recipes, which links crafting recipes to specific benches, categories, and tier levels.
---

## Overview

The `BenchRequirement` field on a recipe determines which crafting bench the player must interact with to craft that item. It connects the recipe system to the bench system by specifying a bench ID, bench type, one or more category filters, and an optional tier level. A recipe can list multiple bench requirements, allowing it to appear on more than one bench. Recipes without a `BenchRequirement` (or with a `Fieldcraft` requirement) can be crafted from the player's inventory without a placed bench.

## File Location

Bench requirements appear inline within recipe definitions:

```
Assets/Server/Item/Items/Bench/*.json     (embedded in Recipe.BenchRequirement)
Assets/Server/Item/Items/**/*.json        (any item with an inline Recipe)
Assets/Server/Item/Recipes/**/*.json      (standalone recipe files)
```

The bench items themselves live at:

```
Assets/Server/Item/Items/Bench/
  Bench_Alchemy.json
  Bench_Arcane.json
  Bench_Armory.json
  Bench_Armour.json
  Bench_Builders.json
  Bench_Campfire.json
  Bench_Cooking.json
  Bench_Farming.json
  Bench_Furnace.json
  Bench_Furniture.json
  Bench_Loom.json
  Bench_Lumbermill.json
  Bench_Memories.json
  Bench_Salvage.json
  Bench_Tannery.json
  Bench_Trough.json
  Bench_Weapon.json
  Bench_WorkBench.json
```

## Schema

### BenchRequirement (array element)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Id` | `string` | Yes | — | Bench identifier that must match the `BlockType.Bench.Id` of a placed bench. Known values include `"Workbench"`, `"Cookingbench"`, `"Furnace"`, `"Campfire"`, `"Alchemybench"`, `"Loombench"`, `"Fieldcraft"`. |
| `Type` | `string` | Yes | — | Bench operational type. Known values: `"Crafting"` (manual recipe selection), `"Processing"` (input-driven with fuel). |
| `Categories` | `string[]` | No | — | List of bench category IDs the recipe belongs to. These correspond to the `BlockType.Bench.Categories[].Id` tabs shown in the bench UI (e.g. `"Workbench_Crafting"`, `"Prepared"`, `"Baked"`, `"Tools"`). |
| `RequiredTierLevel` | `number` | No | — | Minimum bench tier level required to unlock this recipe. Tiers start at `1` (base bench); higher values require bench upgrades. |

### How IDs connect to bench definitions

Each bench item defines a `BlockType.Bench` object with an `Id` field and a `Categories` array. When a recipe specifies `BenchRequirement[].Id = "Workbench"`, the engine matches it to any placed bench whose `BlockType.Bench.Id` equals `"Workbench"`. The `Categories` array on the requirement determines which tab within that bench's UI the recipe appears under.

```
Recipe.BenchRequirement[].Id  ──matches──>  BlockType.Bench.Id
Recipe.BenchRequirement[].Categories  ──filters──>  BlockType.Bench.Categories[].Id
```

## Examples

**Basic workbench requirement** (from `Bench_Cooking.json`):

```json
{
  "BenchRequirement": [
    {
      "Type": "Crafting",
      "Id": "Workbench",
      "Categories": [
        "Workbench_Crafting"
      ]
    }
  ]
}
```

The cooking bench itself must be crafted at a workbench, under the "Crafting" category tab.

**Tier-gated requirement** (from `Bench_Alchemy.json`):

```json
{
  "BenchRequirement": [
    {
      "Id": "Workbench",
      "Type": "Crafting",
      "Categories": [
        "Workbench_Crafting"
      ],
      "RequiredTierLevel": 2
    }
  ]
}
```

The alchemy bench requires a tier-2 (upgraded) workbench to craft.

**Multiple bench requirements** (from `Bench_Campfire.json`):

```json
{
  "BenchRequirement": [
    {
      "Type": "Crafting",
      "Categories": [
        "Tools"
      ],
      "Id": "Fieldcraft"
    },
    {
      "Id": "Workbench",
      "Type": "Crafting",
      "Categories": [
        "Workbench_Survival"
      ]
    }
  ]
}
```

The campfire recipe appears in two locations: the player's fieldcraft menu (under "Tools") and the workbench UI (under "Survival"). This allows the player to craft it at either station.

**Recipe with no bench requirement** (from `Bench_Loom.json`):

```json
{
  "Recipe": {
    "Input": [
      { "Quantity": 5, "ResourceTypeId": "Wood_Trunk" },
      { "ItemId": "Ingredient_Fabric_Scrap_Cotton", "Quantity": 3 }
    ]
  }
}
```

When `BenchRequirement` is omitted entirely, the recipe can be crafted without any bench.

## Related Pages

- [Bench Definitions](/hytale-modding-docs/reference/crafting-system/bench-definitions) — full bench item schema including `BlockType.Bench` configuration and tier upgrades
- [Recipes](/hytale-modding-docs/reference/crafting-system/recipes) — recipe input/output schema where `BenchRequirement` is embedded
- [Salvage](/hytale-modding-docs/reference/crafting-system/salvage) — salvage bench processing recipes
