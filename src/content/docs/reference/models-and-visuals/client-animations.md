---
title: Client Animations
description: Reference for blockyanim animation files in Hytale, the binary animation clip format used by block models and entity models for bone-driven keyframe animation.
---

## Overview

Client animation files (`.blockyanim`) contain bone-driven keyframe animation data for voxel models. They animate the named bones defined in `.blockymodel` files to produce movement such as doors opening, chest lids lifting, candle flames flickering, and fire burning. Like blockymodel files, these are binary assets authored in the Hytale Model Maker tool — not directly human-editable.

Server model definitions reference blockyanim files inside their `AnimationSets`. Block-specific animations live alongside their models in the `Blocks/Animations/` directory tree.

## File Location

```
Assets/Common/Blocks/Animations/
  Candle/
    Candle_Burn.blockyanim
  Chest/
    Chest_Close.blockyanim
    Chest_Open.blockyanim
  Coffin/
    Coffin_Close.blockyanim
    Coffin_Open.blockyanim
  Door/
    Door_Close_In.blockyanim
    Door_Close_Out.blockyanim
    Door_Open_In.blockyanim
    Door_Open_Out.blockyanim
    Door_Open_Slide_In.blockyanim
    Door_Open_Slide_Out.blockyanim
  Fire/
    Fire_Burn.blockyanim
    Fire_Small_Burn.blockyanim
  Light/
    Light_Off.blockyanim
    Light_On.blockyanim
  Trapdoor/
    ...
```

Entity animations live under a separate path:

```
Assets/Common/Characters/Animations/
  Damage/
    Default/
      Hurt.blockyanim
      Hurt2.blockyanim
  ...

Assets/Common/NPC/
  Beast/
    Bear_Grizzly/
      Animations/
        Default/
          Idle.blockyanim
          Run.blockyanim
        Damage/
          Death.blockyanim
  ...
```

## Naming Conventions

| Pattern | Example | Description |
|---------|---------|-------------|
| `{Object}_{Action}.blockyanim` | `Chest_Open.blockyanim` | Primary action animation for an object. |
| `{Object}_{Action}_{Direction}.blockyanim` | `Door_Open_In.blockyanim` | Directional variant of an action. |
| `{Action}.blockyanim` | `Idle.blockyanim` | Entity animation named by state. |
| `{Action}{N}.blockyanim` | `Hurt2.blockyanim` | Numbered variant for random selection. |

## Animation Pairing

Each blockyanim file targets bones defined in a specific blockymodel. The animation system matches by bone name, so:

- Bone names in the animation **must** match those in the target model exactly.
- A single animation can be shared across multiple models if they define the same bone names.
- Missing bones are silently ignored; extra bones in the model remain static.

## How Animations Are Referenced

### In Server Model AnimationSets

```json
{
  "AnimationSets": {
    "Idle": {
      "Animations": [
        {
          "Animation": "NPC/Beast/Bear_Grizzly/Animations/Default/Idle.blockyanim",
          "Speed": 0.6
        }
      ]
    }
  }
}
```

### In Block Type Definitions

Block types with interactive states reference animations for their state transitions (e.g. open/close):

```json
{
  "OpenAnimation": "Blocks/Animations/Chest/Chest_Open.blockyanim",
  "CloseAnimation": "Blocks/Animations/Chest/Chest_Close.blockyanim"
}
```

## Common Block Animation Categories

| Category | Animations | Description |
|----------|-----------|-------------|
| Chest | `Chest_Open`, `Chest_Close` | Lid hinge animation for all chest types |
| Coffin | `Coffin_Open`, `Coffin_Close` | Lid slide animation for coffin blocks |
| Door | `Door_Open_In/Out`, `Door_Close_In/Out`, `Door_Open_Slide_In/Out` | Swing and slide variants for doors |
| Candle | `Candle_Burn` | Looping flame flicker |
| Fire | `Fire_Burn`, `Fire_Small_Burn` | Looping fire animations at two scales |
| Light | `Light_On`, `Light_Off` | Toggle animations for light-emitting blocks |

## Related Pages

- [Client Models](/hytale-modding-docs/reference/models-and-visuals/client-models) — `.blockymodel` mesh files that define the bones animated by these clips
- [Animation Sets](/hytale-modding-docs/reference/models-and-visuals/animation-sets) — how animation clips are grouped into named sets
- [Server Models](/hytale-modding-docs/reference/models-and-visuals/server-models) — server model definitions that wire animations to entity states
