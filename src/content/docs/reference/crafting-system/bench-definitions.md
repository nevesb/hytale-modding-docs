---
title: Bench Definitions
description: Reference for crafting and processing bench item definitions in Hytale, including BlockType.Bench configuration, tier levels, and upgrade requirements.
---

## Overview

Benches are placeable block-items that enable recipes requiring a specific bench ID. Each bench is defined as a standard item file under `Assets/Server/Item/Items/Bench/`, with a `BlockType.Bench` section describing the bench's operational type, categories, sound events, tier system, and UI behaviour. The same item file also embeds the recipe used to craft the bench itself.

## File Location

```
Assets/Server/Item/Items/Bench/
```

One JSON file per bench, e.g. `Bench_WorkBench.json`, `Bench_Campfire.json`, `Bench_Furnace.json`.

## Schema

### Item-level fields (bench-relevant subset)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `TranslationProperties.Name` | `string` | Yes | — | Localisation key for the bench display name. |
| `BlockType` | `object` | Yes | — | Block behaviour definition. See below. |
| `Recipe` | `object` | No | — | Inline recipe to craft this bench. Uses the standard recipe schema. |
| `Tags.Type` | `string[]` | No | — | Should include `"Bench"` for all bench items. |
| `MaxStack` | `number` | No | — | Almost always `1` for benches. |

### BlockType fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Material` | `string` | Yes | — | Physical material class (e.g. `"Solid"`). |
| `DrawType` | `string` | Yes | — | Render type (e.g. `"Model"`). |
| `CustomModel` | `string` | Yes | — | Path to the `.blockymodel` file. |
| `Bench` | `BenchConfig` | Yes | — | Core bench configuration. See below. |
| `State` | `object` | No | — | Visual state definitions (idle, crafting, processing states). |
| `Gathering.Breaking.GatherType` | `string` | No | — | Gather type on block break (e.g. `"Benches"`). |
| `VariantRotation` | `string` | No | — | Rotation variants (e.g. `"NESW"`). |

### BenchConfig

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Type` | `"Crafting" \| "Processing"` | Yes | — | Determines whether the bench shows a crafting queue or a processing pipeline. |
| `Id` | `string` | Yes | — | Unique bench identifier referenced in `BenchRequirement.Id` on recipes. |
| `Categories` | `CategoryEntry[]` | No | — | Crafting benches only. Named category tabs shown in the UI. |
| `TierLevels` | `TierLevel[]` | No | — | Upgrade tier definitions. Each entry describes upgrade costs and bonuses. |
| `LocalOpenSoundEventId` | `string` | No | — | Sound played locally when the bench UI opens. |
| `LocalCloseSoundEventId` | `string` | No | — | Sound played locally when the bench UI closes. |
| `CompletedSoundEventId` | `string` | No | — | Sound played when a craft completes. |
| `FailedSoundEventId` | `string` | No | — | Sound played when a craft fails. |
| `AllowNoInputProcessing` | `boolean` | No | `false` | Processing benches only. Allows processing to start without a full input set. |
| `Fuel` | `FuelSlot[]` | No | — | Processing benches only. Defines fuel input slots. |
| `OutputSlotsCount` | `number` | No | — | Processing benches only. Number of output slots. |

### TierLevel

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `UpgradeRequirement` | `object` | No | — | Materials and time needed to reach this tier. |
| `UpgradeRequirement.Material` | `OutputEntry[]` | No | — | Items consumed on upgrade. |
| `UpgradeRequirement.TimeSeconds` | `number` | No | — | Time in seconds to complete the upgrade. |
| `CraftingTimeReductionModifier` | `number` | No | `0` | Fractional reduction applied to all recipe `TimeSeconds` at this tier (e.g. `0.15` = 15% faster). |

## Example

**Crafting bench** (`Assets/Server/Item/Items/Bench/Bench_WorkBench.json`, condensed):

```json
{
  "TranslationProperties": {
    "Name": "server.items.Bench_WorkBench.name"
  },
  "Recipe": {
    "Input": [
      { "Quantity": 4, "ResourceTypeId": "Wood_Trunk" },
      { "Quantity": 3, "ResourceTypeId": "Rock" }
    ],
    "BenchRequirement": [
      { "Type": "Crafting", "Categories": ["Tools"], "Id": "Fieldcraft" }
    ]
  },
  "BlockType": {
    "Bench": {
      "Type": "Crafting",
      "Id": "Workbench",
      "Categories": [
        { "Id": "Workbench_Survival", "Icon": "Icons/CraftingCategories/Workbench/WeaponsCrude.png", "Name": "server.benchCategories.workbench.survival" },
        { "Id": "Workbench_Tools",    "Icon": "Icons/CraftingCategories/Workbench/Tools.png",       "Name": "server.benchCategories.workbench.tools" }
      ],
      "TierLevels": [
        {
          "CraftingTimeReductionModifier": 0.0,
          "UpgradeRequirement": {
            "Material": [
              { "ItemId": "Ingredient_Bar_Copper", "Quantity": 30 },
              { "ItemId": "Ingredient_Bar_Iron",   "Quantity": 20 }
            ],
            "TimeSeconds": 5.0
          }
        },
        {
          "CraftingTimeReductionModifier": 0.15,
          "UpgradeRequirement": {
            "Material": [
              { "ItemId": "Ingredient_Bar_Thorium", "Quantity": 30 }
            ],
            "TimeSeconds": 10.0
          }
        },
        { "CraftingTimeReductionModifier": 0.3 }
      ],
      "LocalOpenSoundEventId": "SFX_Workbench_Open",
      "CompletedSoundEventId": "SFX_Workbench_Craft"
    }
  },
  "Tags": { "Type": ["Bench"] },
  "MaxStack": 1
}
```

**Processing bench** (`Assets/Server/Item/Items/Bench/Bench_Campfire.json`, condensed):

```json
{
  "BlockType": {
    "Bench": {
      "Type": "Processing",
      "Id": "Campfire",
      "AllowNoInputProcessing": true,
      "Fuel": [
        { "ResourceTypeId": "Fuel", "Icon": "Icons/Processing/FuelSlotIcon.png" }
      ],
      "OutputSlotsCount": 4
    }
  }
}
```

## Related Pages

- [Recipes](/hytale-modding-docs/reference/crafting-system/recipes) — recipe format and bench requirement field
- [Salvage](/hytale-modding-docs/reference/crafting-system/salvage) — the Salvage bench and its recipe format
