---
title: Item Groups
description: Reference for item group JSON files in Hytale, which define named sets of block IDs used by recipes, crafting systems, and world generation.
---

## Overview

Item groups define named collections of block IDs. A group bundles related block variants — for example, all aqua stone block types — under a single group ID. Other systems reference group IDs to operate on all member blocks without listing each one individually.

## File Location

```
Assets/Server/Item/Groups/<GroupId>.json
```

Examples:
```
Assets/Server/Item/Groups/FullBlocks_Aqua.json
Assets/Server/Item/Groups/FullBlocks_Basalt.json
Assets/Server/Item/Groups/FullBlocks_Blackwood.json
Assets/Server/Item/Groups/Foods.json
Assets/Server/Item/Groups/Metal_Bars.json
Assets/Server/Item/Groups/Rock.json
Assets/Server/Item/Groups/Soils.json
Assets/Server/Item/Groups/Wood_All.json
```

## Schema

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Blocks` | string[] | Yes | — | Array of block/item IDs that belong to this group. Each entry is the exact item ID as used in item definitions (e.g. `"Rock_Aqua"`, `"Rock_Aqua_Cobble"`). |

## Examples

`Assets/Server/Item/Groups/FullBlocks_Aqua.json`:

```json
{
  "Blocks": [
    "Rock_Aqua",
    "Rock_Aqua_Cobble"
  ]
}
```

`Assets/Server/Item/Groups/FullBlocks_Basalt.json`:

```json
{
  "Blocks": [
    "Rock_Basalt",
    "Rock_Basalt_Cobble"
  ]
}
```

`Assets/Server/Item/Groups/FullBlocks_Blackwood.json`:

```json
{
  "Blocks": [
    "Wood_Blackwood_Planks",
    "Wood_Blackwood_Decorative",
    "Wood_Blackwood_Ornate"
  ]
}
```

## Available Groups (Partial List)

Groups cover all major block families. The naming convention is `FullBlocks_<Material>` for placeable block sets and plain names for item/ingredient categories:

| Group ID | Description |
|----------|-------------|
| `FullBlocks_Aqua` | Aqua stone variants |
| `FullBlocks_Basalt` | Basalt stone variants |
| `FullBlocks_Blackwood` | Blackwood plank and decorative variants |
| `FullBlocks_Calcite` | Calcite stone variants |
| `FullBlocks_Limestone` | Limestone variants |
| `FullBlocks_Marble` | Marble variants |
| `FullBlocks_Stone` | Standard stone variants |
| `FullBlocks_Softwood` | Softwood plank variants |
| `FullBlocks_Volcanic` | Volcanic stone variants |
| `Foods` | All food items |
| `Metal_Bars` | All metal ingot/bar items |
| `Rock` | All rock block types |
| `Soils` | All soil block types |
| `Wood_All` | All wood plank types |
| `Wood_Trunk` | All wood trunk types |
| `Bone` | Bone item variants |
| `Flowers` | Flower block types |
| `Mushrooms` | Mushroom block types |
| `Meats` | Meat ingredient items |
| `Fish` | All fish items |
| `Fuel` | Items that can be used as fuel |
| `Rubble` | Rubble block types |
| `Sands` | Sand and gravel types |

## Related Pages

- [Item Definitions](/hytale-modding-docs/reference/item-system/item-definitions) — Block and item definitions that groups reference
- [Block Definitions](/hytale-modding-docs/reference/item-system/block-definitions) — Block texture and material properties
- [Resource Types](/hytale-modding-docs/reference/item-system/resource-types) — Alternative grouping mechanism used in recipe inputs
