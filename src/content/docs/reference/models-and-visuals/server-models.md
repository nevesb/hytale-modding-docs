---
title: Server Models
description: Reference for server-side model definitions in Hytale, covering hitboxes, eye height, scale ranges, animation sets, camera configuration, and icon properties for NPCs and entities.
---

## Overview

Server model files define the physical and behavioural properties of an entity's visual representation on the server: hitbox dimensions, eye height, scale variation, bone-targeted camera tracking, and the full library of named animation sets used by the AI and physics systems. They are separate from client-only visual assets — the server needs hitbox and animation metadata to run collision, AI, and sound logic. Models support inheritance via a `Parent` field.

## File Location

```
Assets/Server/Models/
  Beast/
    Bear_Grizzly.json
    Bear_Polar.json
    Cactee.json
  Boss/
  Critter/
  Deployables/
  Elemental/
  Flying_Beast/
  Flying_Critter/
  Flying_Wildlife/
  Human/
    Mannequin.json
    Player.json
  Intelligent/
  Instances/
  Livestock/
  Pets/
  Projectiles/
```

## Schema

### Top-level

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Model` | `string` | Yes | — | Path to the `.blockymodel` file defining the visual mesh. |
| `Texture` | `string` | No | — | Path to the default texture applied to the model. |
| `Parent` | `string` | No | — | ID of a parent model definition to inherit unset fields from. |
| `EyeHeight` | `number` | Yes | — | Height in units from the entity's feet to its eye position. Used for camera placement and line-of-sight. |
| `CrouchOffset` | `number` | No | `0` | Vertical offset applied to the eye position when the entity is crouching. |
| `HitBox` | `HitBox` | Yes | — | Axis-aligned bounding box used for collision and hit detection. |
| `MinScale` | `number` | No | `1` | Minimum random scale applied to this entity on spawn. |
| `MaxScale` | `number` | No | `1` | Maximum random scale applied to this entity on spawn. Scale is chosen uniformly between min and max. |
| `DefaultAttachments` | `object[]` | No | `[]` | List of item attachments present on the entity by default (e.g. held weapons). |
| `Camera` | `CameraConfig` | No | — | Bone-targeted camera tracking configuration. |
| `AnimationSets` | `object` | Yes | — | Map of animation set name → `AnimationSet`. See below. |
| `IconProperties` | `IconProperties` | No | — | Camera parameters used when rendering the entity's inventory icon. |

### HitBox

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Min` | `Vector3` | Yes | — | Minimum corner of the AABB relative to the entity's origin (feet). |
| `Max` | `Vector3` | Yes | — | Maximum corner of the AABB relative to the entity's origin. |

### Vector3

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `X` | `number` | Yes | — | X component. |
| `Y` | `number` | Yes | — | Y component (vertical). |
| `Z` | `number` | Yes | — | Z component. |

### CameraConfig

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Pitch` | `CameraAxis` | No | — | Pitch tracking configuration. |
| `Yaw` | `CameraAxis` | No | — | Yaw tracking configuration. |

### CameraAxis

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `AngleRange.Min` | `number` | Yes | — | Minimum angle in degrees the camera can track on this axis. |
| `AngleRange.Max` | `number` | Yes | — | Maximum angle in degrees the camera can track on this axis. |
| `TargetNodes` | `string[]` | Yes | — | Bone names the camera aims at when tracking. |

### AnimationSet

An animation set is a named group of one or more animation clips. The engine plays one clip from the group (randomly or in sequence depending on context).

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Animations` | `AnimationEntry[]` | Yes | — | One or more animation clips in this set. |

### AnimationEntry

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Animation` | `string` | Yes | — | Path to the `.blockyanim` animation file. |
| `Speed` | `number` | No | `1` | Playback speed multiplier. |
| `BlendingDuration` | `number` | No | `0` | Time in seconds to blend from the previous animation into this one. |
| `Looping` | `boolean` | No | `true` | Whether the animation loops. Set to `false` for one-shot animations. |
| `SoundEventId` | `string` | No | — | Sound event triggered when this animation plays (e.g. footstep sounds). |

### IconProperties

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Scale` | `number` | No | — | Zoom level used when rendering the icon. |
| `Rotation` | `[number, number, number]` | No | — | Euler rotation `[X, Y, Z]` in degrees applied to the model for icon rendering. |
| `Translation` | `[number, number]` | No | — | 2D `[X, Y]` offset in pixels applied to centre the model in the icon frame. |

## Standard Animation Set Names

The engine expects specific named sets. Custom sets can be added for scripted use.

| Name | Purpose |
|------|---------|
| `Idle` | Standing still |
| `Walk` / `WalkBackward` | Walking forward/backward |
| `Run` | Running |
| `Crouch` / `CrouchWalk` / `CrouchWalkBackward` | Crouched states |
| `Jump` / `JumpWalk` / `JumpRun` | Jump variants |
| `Fall` | Falling |
| `Swim` / `SwimIdle` / `SwimFast` / `SwimBackward` | Swimming states |
| `Fly` / `FlyIdle` / `FlyFast` / `FlyBackward` | Flying states |
| `Hurt` / `Death` | Damage reactions |
| `Alerted` | Aggro trigger |
| `Sleep` / `Laydown` / `Wake` | Rest cycle |
| `Spawn` | Spawn-in animation |
| `Roar` / `Search` / `Eat` | Flavour animations |

## Example

**Grizzly Bear** (`Assets/Server/Models/Beast/Bear_Grizzly.json`, condensed):

```json
{
  "Model": "NPC/Beast/Bear_Grizzly/Models/Model.blockymodel",
  "Texture": "NPC/Beast/Bear_Grizzly/Models/Texture.png",
  "EyeHeight": 1.5,
  "CrouchOffset": -0.3,
  "HitBox": {
    "Max": { "X":  0.8, "Y": 1.8, "Z":  0.8 },
    "Min": { "X": -0.8, "Y": 0.0, "Z": -0.8 }
  },
  "MinScale": 0.9,
  "MaxScale": 1.25,
  "DefaultAttachments": [],
  "Camera": {
    "Pitch": {
      "AngleRange": { "Max": 45, "Min": -45 },
      "TargetNodes": ["Head"]
    },
    "Yaw": {
      "AngleRange": { "Max": 45, "Min": -45 },
      "TargetNodes": ["Head"]
    }
  },
  "AnimationSets": {
    "Idle": {
      "Animations": [
        { "Animation": "NPC/Beast/Bear_Grizzly/Animations/Default/Idle.blockyanim", "Speed": 0.6 }
      ]
    },
    "Run": {
      "Animations": [
        { "Animation": "NPC/Beast/Bear_Grizzly/Animations/Default/Run.blockyanim", "SoundEventId": "SFX_Bear_Grizzly_Run", "Speed": 1 }
      ]
    },
    "Death": {
      "Animations": [
        { "Animation": "NPC/Beast/Bear_Grizzly/Animations/Damage/Death.blockyanim", "Looping": false, "SoundEventId": "SFX_Bear_Grizzly_Death" }
      ]
    }
  }
}
```

**Mannequin** (`Assets/Server/Models/Human/Mannequin.json`) — uses `Parent` inheritance:

```json
{
  "Model": "NPC/MISC/Mannequin/Models/Model.blockymodel",
  "Texture": "NPC/MISC/Mannequin/Models/Model_Default.png",
  "EyeHeight": 1.6,
  "HitBox": {
    "Max": { "X":  0.3, "Y": 1.8, "Z":  0.3 },
    "Min": { "X": -0.3, "Y": 0.0, "Z": -0.3 }
  },
  "MinScale": 1,
  "MaxScale": 1,
  "Parent": "Player",
  "DefaultAttachments": [],
  "AnimationSets": {
    "Hurt": {
      "Animations": [
        { "Animation": "Characters/Animations/Damage/Default/Hurt.blockyanim",  "BlendingDuration": 0.1, "Looping": false },
        { "Animation": "Characters/Animations/Damage/Default/Hurt2.blockyanim", "BlendingDuration": 0.1, "Looping": false }
      ]
    }
  }
}
```

## Related Pages

- [NPC System](/hytale-modding-docs/reference/npc-system/) — NPC definitions that reference model IDs
- [Projectile Configs](/hytale-modding-docs/reference/combat-and-projectiles/projectile-configs) — `Model` field referencing projectile model IDs
