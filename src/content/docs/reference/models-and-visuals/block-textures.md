---
title: Block Textures
description: Reference for block texture conventions in Hytale, covering the naming patterns, directory layout, and face-specific texture system used by standard cube blocks.
---

## Overview

Block textures are PNG images that define the visual appearance of standard cube blocks. Unlike blockymodel-based blocks that have full 3D voxel geometry, standard blocks use a set of face textures applied to a unit cube. The engine resolves textures by naming convention — a block named `Calcite` looks for `Calcite.png`, `Calcite_Top.png`, `Calcite_Side.png`, etc. in the `BlockTextures` directory. All textures use a consistent pixel resolution and are packed into a texture atlas at load time.

## File Location

```
Assets/Common/BlockTextures/
  Bone_Side.png
  Bone_Top.png
  Calcite.png
  Calcite_Brick_Decorative.png
  Calcite_Brick_Decorative_Top.png
  Calcite_Brick_Ornate.png
  Calcite_Brick_Side.png
  Calcite_Brick_Smooth.png
  Calcite_Brick_Top.png
  Calcite_Cobble.png
  Calcite_Cobble_Top.png
  Calcite_Top.png
  Chalk.png
  Clay_Black.png
  Clay_Blue.png
  Clay_Smooth_Black.png
  ...
```

## Naming Conventions

### Face-specific Textures

The engine uses a suffix-based system to assign textures to specific cube faces. If a face-specific texture is not found, the engine falls back to the base texture.

| Suffix | Faces Applied | Description |
|--------|--------------|-------------|
| _(none)_ | All faces (fallback) | Base texture used for any face without a specific override. |
| `_Top` | Top (+Y) | Top face texture. Common for blocks with different top/side appearance (e.g. grass, ore). |
| `_Side` | North, South, East, West | Side face texture, used when sides differ from top and bottom. |
| `_Bottom` | Bottom (-Y) | Bottom face texture. Rarely needed; falls back to base if absent. |

### Resolution Order

For a block named `Calcite_Brick`:

1. **Top face**: `Calcite_Brick_Top.png` -> `Calcite_Brick.png`
2. **Side faces**: `Calcite_Brick_Side.png` -> `Calcite_Brick.png`
3. **Bottom face**: `Calcite_Brick_Bottom.png` -> `Calcite_Brick.png`

### Material and Variant Patterns

| Pattern | Example | Description |
|---------|---------|-------------|
| `{Material}.png` | `Chalk.png` | Simple uniform block — same texture on all faces. |
| `{Material}_{Finish}.png` | `Calcite_Brick_Smooth.png` | Processed variant of a base material. |
| `{Material}_{Finish}_{Face}.png` | `Calcite_Brick_Decorative_Top.png` | Face-specific texture for a processed variant. |
| `{Category}_{Colour}.png` | `Clay_Blue.png` | Colour variant within a material category. |
| `{Category}_{Finish}_{Colour}.png` | `Clay_Smooth_Blue.png` | Colour variant of a processed finish. |

## Texture Specifications

| Property | Value | Description |
|----------|-------|-------------|
| Format | PNG | Standard RGBA PNG images. |
| Resolution | 16x16 pixels (standard) | All block textures use the same resolution for atlas packing. |
| Transparency | Supported | Alpha channel enables partially transparent blocks (glass, leaves). |
| Colour Space | sRGB | Standard colour space; the engine handles linear conversion. |

## Common Material Categories

| Category | Examples | Description |
|----------|----------|-------------|
| Soil | `Soil_Grass.png`, `Soil_Dirt.png` | Natural terrain surface blocks. |
| Stone | `Stone.png`, `Stone_Mossy.png` | Underground and surface rock. |
| Calcite | `Calcite.png`, `Calcite_Brick_Ornate.png` | Light-coloured building stone with many decorative variants. |
| Clay | `Clay_Black.png` through `Clay_Purple.png` | Coloured clay blocks for building. |
| Ore | Various per-zone ores | Mineral deposits with distinct face textures. |
| Wood | Various tree species | Bark (side) and ring (top) textures. |

## Related Pages

- [Client Models](/hytale-modding-docs/reference/models-and-visuals/client-models) — `.blockymodel` files for blocks with non-cube geometry
- [Block Type Lists](/hytale-modding-docs/reference/game-configuration/block-type-lists) — named lists that group block types by category
