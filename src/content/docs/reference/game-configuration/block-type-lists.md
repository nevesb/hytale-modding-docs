---
title: Block Type Lists
description: Reference for block type list definitions in Hytale, which group block type IDs into named categories used by world generation, game rules, and filtering systems.
---

## Overview

Block type list files define named groups of block type IDs. These lists are referenced by other systems — world generation uses them to determine which blocks can be scattered, replaced, or gathered, and game rules use them to filter block interactions. Each list is simply a JSON object with a `Blocks` array containing string IDs that correspond to registered block types.

## File Location

```
Assets/Server/BlockTypeList/
  AllScatter.json
  Empty.json
  Gravel.json
  Ores.json
  PlantScatter.json
  PlantsAndTrees.json
  Rock.json
  Snow.json
  Soils.json
  TreeLeaves.json
  TreeWood.json
  TreeWoodAndLeaves.json
```

## Schema

### Top-level

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Blocks` | `string[]` | Yes | — | Array of block type ID strings. Each ID must match a registered block type name. |

## List Descriptions

| List | Approximate Size | Description |
|------|-----------------|-------------|
| `AllScatter` | ~160 entries | All decorative scatter blocks: grasses, flowers, ferns, rubble, bones, coral, and nest decorations. |
| `Empty` | 0 entries | Empty list used as a "none" placeholder. |
| `Gravel` | Small | Gravel block variants. |
| `Ores` | Small | Mineable ore blocks across all zones. |
| `PlantScatter` | Medium | Subset of scatter limited to plants and flowers. |
| `PlantsAndTrees` | Medium | Plants, flowers, and tree-related blocks. |
| `Rock` | Small | Natural rock and stone blocks. |
| `Snow` | Small | Snow-covered block variants. |
| `Soils` | ~13 entries | Soil and grass terrain blocks across biome types. |
| `TreeLeaves` | Small | Leaf blocks from all tree species. |
| `TreeWood` | Small | Trunk/wood blocks from all tree species. |
| `TreeWoodAndLeaves` | Medium | Combined tree wood and leaf blocks. |

## Examples

**Soils list** (`Assets/Server/BlockTypeList/Soils.json`):

```json
{
  "Blocks": [
    "Soil_Dirt",
    "Soil_Dirt_Burnt",
    "Soil_Dirt_Cold",
    "Soil_Dirt_Dry",
    "Soil_Dirt_Poisoned",
    "Soil_Grass",
    "Soil_Grass_Burnt",
    "Soil_Grass_Cold",
    "Soil_Grass_Deep",
    "Soil_Grass_Dry",
    "Soil_Grass_Full",
    "Soil_Grass_Sunny",
    "Soil_Grass_Wet"
  ]
}
```

**AllScatter list** (`Assets/Server/BlockTypeList/AllScatter.json`, condensed):

```json
{
  "Blocks": [
    "Wood_Sticks",
    "Plant_Bush_Green",
    "Plant_Grass_Arid",
    "Plant_Grass_Arid_Short",
    "Plant_Grass_Lush",
    "Plant_Flower_Bushy_Blue",
    "Plant_Flower_Common_Red",
    "Plant_Fern",
    "Rubble_Stone",
    "Rubble_Sandstone",
    "Deco_Bone_Skulls_Feran",
    "Deco_Coral_Shell",
    "Deco_Trash"
  ]
}
```

## Related Pages

- [World Generation](/hytale-modding-docs/reference/world-and-environment/world-generation) — assignments that reference block type lists for scatter placement
- [Block Textures](/hytale-modding-docs/reference/models-and-visuals/block-textures) — texture files for the blocks referenced in these lists
- [Objectives](/hytale-modding-docs/reference/game-configuration/objectives) — task conditions that filter by block tags matching these lists
