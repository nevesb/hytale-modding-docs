---
title: Animation Sets
description: Reference for animation set definitions embedded within server model files in Hytale, covering animation grouping, playback speed, blending, looping, and sound event triggers.
---

## Overview

Animation sets are named groups of animation clips defined inside server model files. The engine uses these named sets to play the correct animation for a given entity state (idle, walk, attack, death, etc.). Each set contains one or more `AnimationEntry` objects; when multiple entries exist the engine selects one randomly, giving visual variety. Animation sets support playback speed scaling, cross-fade blending, loop control, and per-clip sound event triggers.

Animation sets live inside the `AnimationSets` field of a server model definition. This page focuses on the animation set schema itself. For the full model file format, see [Server Models](/hytale-modding-docs/reference/models-and-visuals/server-models).

## File Location

Animation sets are embedded in server model JSON files:

```
Assets/Server/Models/
  Beast/
    Bear_Grizzly.json      (contains AnimationSets)
    Bear_Polar.json
    Cactee.json
  Critter/
  Flying_Beast/
  Human/
    Player.json
    Mannequin.json
  Intelligent/
  Livestock/
  Pets/
  Projectiles/
```

## Schema

### AnimationSet

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Animations` | `AnimationEntry[]` | Yes | — | One or more animation clips in this set. When multiple entries exist, the engine selects one randomly on each play. |

### AnimationEntry

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Animation` | `string` | Yes | — | Path to the `.blockyanim` animation file, relative to the Common assets root. |
| `Speed` | `number` | No | `1` | Playback speed multiplier. Values below `1` slow the animation; values above `1` speed it up. |
| `BlendingDuration` | `number` | No | `0` | Time in seconds to crossfade from the previous animation into this one. Produces smoother transitions at the cost of a brief overlap. |
| `Looping` | `boolean` | No | `true` | Whether the animation loops continuously. Set to `false` for one-shot animations such as death or attack. |
| `SoundEventId` | `string` | No | — | Sound event triggered each time this animation plays or loops (e.g. footstep or roar sounds). |

## Standard Set Names

The engine expects specific named sets for core entity states. Custom sets can be added for scripted or AI-driven behaviour.

| Name | Purpose |
|------|---------|
| `Idle` | Standing still, no input |
| `Walk` / `WalkBackward` | Walking forward or backward |
| `Run` | Running / sprinting |
| `Crouch` / `CrouchWalk` / `CrouchWalkBackward` | Crouched movement states |
| `Jump` / `JumpWalk` / `JumpRun` | Jump variants by movement speed |
| `Fall` | Falling through air |
| `Swim` / `SwimIdle` / `SwimFast` / `SwimBackward` | Swimming states |
| `Fly` / `FlyIdle` / `FlyFast` / `FlyBackward` | Flying states |
| `Hurt` / `Death` | Damage reaction and death |
| `Alerted` | Aggro trigger animation |
| `Sleep` / `Laydown` / `Wake` | Rest cycle |
| `Spawn` | Entity spawn-in animation |
| `Roar` / `Search` / `Eat` | Ambient flavour animations |

## Example

**Multiple animation variants with blending** (from `Assets/Server/Models/Human/Mannequin.json`):

```json
{
  "AnimationSets": {
    "Hurt": {
      "Animations": [
        {
          "Animation": "Characters/Animations/Damage/Default/Hurt.blockyanim",
          "BlendingDuration": 0.1,
          "Looping": false
        },
        {
          "Animation": "Characters/Animations/Damage/Default/Hurt2.blockyanim",
          "BlendingDuration": 0.1,
          "Looping": false
        }
      ]
    }
  }
}
```

**Single clip with sound event** (from `Assets/Server/Models/Beast/Bear_Grizzly.json`):

```json
{
  "AnimationSets": {
    "Run": {
      "Animations": [
        {
          "Animation": "NPC/Beast/Bear_Grizzly/Animations/Default/Run.blockyanim",
          "SoundEventId": "SFX_Bear_Grizzly_Run",
          "Speed": 1
        }
      ]
    },
    "Death": {
      "Animations": [
        {
          "Animation": "NPC/Beast/Bear_Grizzly/Animations/Damage/Death.blockyanim",
          "Looping": false,
          "SoundEventId": "SFX_Bear_Grizzly_Death"
        }
      ]
    }
  }
}
```

## Related Pages

- [Server Models](/hytale-modding-docs/reference/models-and-visuals/server-models) — full model file format that contains animation sets
- [Client Animations](/hytale-modding-docs/reference/models-and-visuals/client-animations) — `.blockyanim` file format referenced by animation entries
- [Client Models](/hytale-modding-docs/reference/models-and-visuals/client-models) — `.blockymodel` visual mesh format
