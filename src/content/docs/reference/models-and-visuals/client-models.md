---
title: Client Models
description: Reference for client-side blockymodel files in Hytale, the binary voxel mesh format used for blocks, benches, furniture, and other interactive world objects.
---

## Overview

Client model files (`.blockymodel`) define the voxel mesh geometry for blocks, benches, furniture, doors, and other objects that have a non-standard visual shape. Unlike simple cube blocks that use only textures, blockymodel files contain a full 3D voxel model with named bones for animation support. They are referenced by server-side block definitions and by server model files via the `Model` field.

These are binary files — they are not directly human-editable JSON. They are authored in the Hytale Model Maker tool and exported to the `.blockymodel` format. This page documents the file conventions, directory layout, and how they integrate with the broader asset pipeline.

## File Location

```
Assets/Common/Blocks/
  Animations/           (paired .blockyanim files)
  Benches/
    Alchemy.blockymodel
    Anvil.blockymodel
    ArcaneTable.blockymodel
    Armor.blockymodel
    Bedroll.blockymodel
    Builder.blockymodel
    Campfire.blockymodel
    Carpenter.blockymodel
    Cooking.blockymodel
    Farming.blockymodel
    Furnace.blockymodel
    ...
  Chests/
  Coffins/
  Containers/
  Doors/
  Fences/
  Furniture/
  Lights/
  Signs/
  Stairs/
  Trapdoors/
  Walls/
```

## Naming Conventions

| Pattern | Example | Description |
|---------|---------|-------------|
| `{Object}.blockymodel` | `Anvil.blockymodel` | Base model for a single-variant object. |
| `{Object}_{Variant}.blockymodel` | `Campfire_Cooking.blockymodel` | Variant model (e.g. different state of the same block). |
| `{Category}_{Material}.blockymodel` | `Door_Wood.blockymodel` | Material variant within a category. |

## Integration Points

### Referenced by Server Block Definitions

Block type JSON files reference blockymodel paths to override the default cube shape:

```json
{
  "Model": "Blocks/Benches/Anvil.blockymodel"
}
```

### Referenced by Server Model Definitions

Server model files for NPCs and entities use the same format:

```json
{
  "Model": "NPC/Beast/Bear_Grizzly/Models/Model.blockymodel"
}
```

### Paired with Animations

Many blockymodel files have corresponding `.blockyanim` files in the `Animations/` directory. The bone names defined in the model must match those referenced by the animation clips.

## Bone Structure

Blockymodel files contain named bones that serve as articulation points. Common bone names observed across block models:

| Bone | Used In | Purpose |
|------|---------|---------|
| `Lid` | Chests, Coffins | Hinged lid for open/close animation |
| `Door` | Doors | Swinging or sliding door panel |
| `Flame` | Candles, Campfires | Animated flame element |
| `Trapdoor` | Trapdoors | Hinged trapdoor panel |

## Example Workflow

1. Author a voxel model in Model Maker with named bones
2. Export as `.blockymodel` to `Assets/Common/Blocks/{Category}/`
3. Create matching `.blockyanim` files in `Assets/Common/Blocks/Animations/{Category}/`
4. Reference the model path in the server-side block type definition
5. Wire up animation sets if the block has interactive states

## Related Pages

- [Client Animations](/hytale-modding-docs/reference/models-and-visuals/client-animations) — `.blockyanim` animation clips paired with block models
- [Server Models](/hytale-modding-docs/reference/models-and-visuals/server-models) — server-side model definitions that reference `.blockymodel` paths
- [Block Textures](/hytale-modding-docs/reference/models-and-visuals/block-textures) — texture conventions for standard cube blocks
