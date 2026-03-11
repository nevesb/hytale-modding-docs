---
title: Block Definitions
description: Reference for block definition JSON files in Hytale, covering textures, materials, light, and draw types for world blocks.
---

## Overview

Block definitions describe the visual and physical properties of blocks placed in the world. Most block data lives inside the `BlockType` object of an item definition file, but standalone block files exist for fluids, fluid effects, and breaking decals. Textures can be specified per-face or as a single `All` shorthand, with optional `Weight` values for randomized variants.

## File Location

Block data is stored in two places:

- **Item-embedded blocks** (rocks, wood, soil, etc.): `BlockType` object inside `Assets/Server/Item/Items/<Category>/<ItemId>.json`
- **Standalone block files** (fluids, decals, fluid effects): `Assets/Server/Item/Block/<Subcategory>/<BlockId>.json`

Subcategories under `Assets/Server/Item/Block/`:
```
Block/Fluids/          — Fluid blocks (Lava, Water, Slime, Poison, Fire)
Block/BreakingDecals/  — Break-animation crack overlays
Block/FluidFX/         — Fluid visual effect configs
Block/Hitboxes/        — Custom hitbox shape definitions
Block/Blocks/_Debug/   — Debug-only test blocks
```

## Schema

### Texture Object Fields

Each entry in the `Textures` array defines one texture variant. Multiple entries with `Weight` values enable random texture selection.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `All` | string | No | — | Texture path applied to all six faces of the block. |
| `Sides` | string | No | — | Texture applied to the four side faces (North, South, East, West). |
| `UpDown` | string | No | — | Texture applied to top and bottom faces. |
| `Top` | string | No | — | Texture applied to the top face only. |
| `Bottom` | string | No | — | Texture applied to the bottom face only. |
| `North` | string | No | — | Texture applied to the north face only. |
| `South` | string | No | — | Texture applied to the south face only. |
| `East` | string | No | — | Texture applied to the east face only. |
| `West` | string | No | — | Texture applied to the west face only. |
| `Weight` | number | No | `1` | Relative probability weight for this variant when multiple texture entries are present. |

### BlockType / Block-Level Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Textures` | object[] | No | — | Array of texture variant objects (see above). |
| `Material` | string | No | — | Physical material category. Values: `Solid`, `Fluid`, `Empty`, `Plant`. Controls collision and interaction behavior. |
| `DrawType` | string | No | — | Rendering mode. Common values: `Model` (custom mesh), `Block` (standard cube), `Plant` (billboard foliage). |
| `Opacity` | string | No | — | Transparency level. Values: `Opaque`, `Semitransparent`, `Transparent`. |
| `Light` | object | No | — | Light emission config. Contains `Color` (hex string, e.g. `"#e90"`) and optionally `Level` (number). |
| `ParticleColor` | string | No | — | Hex color for block-break particle effects (e.g. `"#58ad9b"`). |
| `CustomModel` | string | No | — | Path to a `.blockymodel` file used instead of a standard cube mesh. |
| `CustomModelTexture` | object[] | No | — | Array of `{ "Texture": "<path>", "Weight": <number> }` for custom model texture variants. |
| `CustomModelScale` | number | No | `1.0` | Scale multiplier for the custom model. |
| `HitboxType` | string | No | — | ID of a hitbox definition from `Block/Hitboxes/`. |
| `RandomRotation` | string | No | — | Rotation randomization when placed. Example: `"YawStep1"`. |
| `BlockParticleSetId` | string | No | — | Particle set used for ambient block particles (e.g. `"Lava"`, `"Dust"`). |
| `BlockSoundSetId` | string | No | — | Sound set ID for block interaction sounds. |
| `Gathering` | object | No | — | Harvesting configuration. Child objects `Harvest`, `Soft`, and `Breaking` each accept a `GatherType` string. |
| `Aliases` | string[] | No | — | Alternative string IDs for this block, used by commands and world generation. |

### Fluid-Specific Fields

These fields appear in standalone fluid block files under `Block/Fluids/`.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `MaxFluidLevel` | number | No | — | Maximum fluid level integer. Source blocks typically use `1`; flowing fluids use `8`. |
| `Effect` | string[] | No | — | List of effect IDs applied when an entity enters this fluid (e.g. `["Lava"]`). |
| `FluidFXId` | string | No | — | References a fluid visual effect config from `Block/FluidFX/`. |
| `Ticker` | object | No | — | Fluid flow behavior. Contains `CanDemote` (boolean), `SpreadFluid` (string), `FlowRate` (number), `SupportedBy` (string), and `Collisions` (object mapping block IDs to placement results). |
| `Interactions` | object | No | — | Block-level interaction chains (e.g. collision effects). Uses the same chain format as item interactions. |
| `Parent` | string | No | — | ID of a parent block to inherit fields from. |

## Example

`Assets/Server/Item/Items/Rock/Rock_Aqua.json` (BlockType section):

```json
{
  "TranslationProperties": {
    "Name": "server.items.Rock_Aqua.name"
  },
  "Icon": "Icons/ItemsGenerated/Rock_Aqua.png",
  "Parent": "Rock_Stone",
  "BlockType": {
    "Textures": [
      {
        "All": "BlockTextures/Rock_Aqua.png",
        "Weight": 1
      }
    ],
    "ParticleColor": "#58ad9b",
    "Gathering": {
      "Breaking": {
        "GatherType": "Rocks"
      }
    },
    "Aliases": [
      "aqua",
      "aqua00"
    ]
  }
}
```

`Assets/Server/Item/Block/Blocks/_Debug/Debug_Test_Block.json` (standalone block with light):

```json
{
  "Textures": [
    {
      "All": "Blocks/_Debug/Texture.png"
    }
  ],
  "Material": "Solid",
  "Light": {
    "Color": "#f0f"
  }
}
```

`Assets/Server/Item/Block/Fluids/Lava_Source.json` (fluid block):

```json
{
  "MaxFluidLevel": 1,
  "Effect": ["Lava"],
  "Opacity": "Transparent",
  "Textures": [
    {
      "Weight": 1,
      "All": "BlockTextures/Fluid_Lava.png"
    }
  ],
  "Light": {
    "Color": "#e90"
  },
  "Ticker": {
    "CanDemote": false,
    "SpreadFluid": "Lava",
    "FlowRate": 2.0,
    "Collisions": {
      "Water": {
        "BlockToPlace": "Rock_Stone_Cobble",
        "SoundEvent": "SFX_Flame_Break"
      }
    }
  }
}
```

## Related Pages

- [Item Definitions](/hytale-modding-docs/reference/item-system/item-definitions) — Full item definition schema including BlockType
- [Item Groups](/hytale-modding-docs/reference/item-system/item-groups) — Named sets of block IDs used by recipes and systems
- [Item Interactions](/hytale-modding-docs/reference/item-system/item-interactions) — Interaction chains used in fluid collision triggers
