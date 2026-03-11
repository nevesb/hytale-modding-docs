---
title: Particles
description: Reference for particle system and particle spawner definitions in Hytale, covering particle effects for blocks, combat, weather, NPCs, and deployables.
---

## Overview

Hytale's particle system uses two file types that work together: **particle systems** (`.particlesystem`) compose one or more spawner references into a complete effect, and **particle spawners** (`.particlespawner`) define the individual emitter behaviour — emission rate, velocity, lifetime, texture, colour animation, attractors, and collision. Particle system JSON files can also use the `.json` extension for complex multi-spawner effects. The engine loads these at runtime to produce visual effects for block interactions, combat hits, weather, NPC abilities, and deployable objects.

## File Location

```
Assets/Server/Particles/
  Block/
    Block_Top_Glow.particlesystem
    Block_Top_Glow_Alpha.particlespawner
    Clay/
      Block_Break_Clay.particlesystem
      Block_Hit_Clay.particlesystem
    Crystal/
    Stone/
    Wood/
  Combat/
  Deployables/
    Healing_Totem/
      Totem_Heal_Simple_Test.json
    Slowness_Totem/
  Drop/
  Dust_Sparkles_Fine.particlesystem
  Dust_Sparkles_Fine.particlespawner
  Explosion/
  Item/
  Memories/
  NPC/
  Projectile/
  Spell/
  Status_Effect/
  Weapon/
  Weather/
  _Example/
```

## Schema

### Particle System (.particlesystem / .json)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Spawners` | `SpawnerRef[]` | Yes | — | Array of spawner references that make up this particle effect. |
| `LifeSpan` | `number` | No | — | Total duration in seconds before the entire system is destroyed. Omit for infinite-duration effects. |
| `CullDistance` | `number` | No | — | Distance in blocks beyond which the particle system is not rendered. |
| `BoundingRadius` | `number` | No | — | Radius used for frustum culling. |
| `IsImportant` | `boolean` | No | `false` | When `true`, the system is never culled by the particle budget. |

### SpawnerRef

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `SpawnerId` | `string` | Yes | — | ID of the particle spawner to use. Resolves to a `.particlespawner` file by name. |
| `PositionOffset` | `Vector3` | No | `{0,0,0}` | Position offset from the system origin. Only specified axes are overridden. |
| `FixedRotation` | `boolean` | No | `true` | When `false`, particles rotate with the emitting entity. |
| `StartDelay` | `number` | No | `0` | Seconds to wait before this spawner begins emitting. |
| `WaveDelay` | `MinMax` | No | — | Random delay range between emission waves. |

### Particle Spawner (.particlespawner)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `RenderMode` | `string` | No | — | Rendering mode: `"Erosion"`, `"Additive"`, `"AlphaBlend"`, etc. |
| `EmitOffset` | `Vector3MinMax` | No | — | Random offset range for particle spawn position on each axis. |
| `ParticleRotationInfluence` | `string` | No | — | How particle rotation is computed: `"Billboard"` (faces camera), `"Velocity"`, etc. |
| `LinearFiltering` | `boolean` | No | `false` | Use bilinear texture filtering instead of nearest-neighbour. |
| `LightInfluence` | `number` | No | `1.0` | How much scene lighting affects particle colour (0 = unlit, 1 = fully lit). |
| `MaxConcurrentParticles` | `number` | No | `0` | Maximum number of live particles. `0` means unlimited. |
| `ParticleLifeSpan` | `MinMax` | No | — | Random range for individual particle lifetime in seconds. |
| `ParticleRotateWithSpawner` | `boolean` | No | `false` | Whether particles inherit the spawner's rotation. |
| `SpawnRate` | `MinMax` | No | — | Milliseconds between particle emissions (randomized within range). |
| `InitialVelocity` | `VelocityConfig` | No | — | Initial velocity in spherical coordinates. |
| `Attractors` | `Attractor[]` | No | `[]` | Point attractors that pull particles. |
| `Particle` | `ParticleConfig` | Yes | — | Texture, animation keyframes, and initial state. |
| `ParticleCollision` | `object` | No | — | Collision settings for particles hitting blocks. |

### VelocityConfig

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Yaw` | `MinMax` | No | — | Random yaw angle range in degrees. |
| `Pitch` | `MinMax` | No | — | Random pitch angle range in degrees. |
| `Speed` | `MinMax` | No | — | Random speed range in blocks per second. |

### Attractor

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Position` | `Vector3` | Yes | — | Attractor position relative to the spawner. |
| `RadialAxis` | `Vector3` | No | — | Axis for radial acceleration. |
| `Radius` | `number` | No | `0` | Attractor influence radius. |
| `RadialAcceleration` | `number` | No | `0` | Inward (negative) or outward (positive) radial force. |
| `RadialTangentAcceleration` | `number` | No | `0` | Tangential force perpendicular to the radial direction. |
| `LinearAcceleration` | `Vector3` | No | — | Constant linear acceleration (e.g. gravity). |

### ParticleConfig

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Texture` | `string` | Yes | — | Path to the particle texture image. |
| `FrameSize` | `{ Width, Height }` | No | — | Size of a single frame in a sprite sheet texture. |
| `ScaleRatioConstraint` | `string` | No | — | `"OneToOne"` locks X and Y scale together. |
| `Animation` | `object` | No | — | Keyframe map where keys are lifetime percentages (`"0"`, `"50"`, `"100"`). |
| `InitialAnimationFrame` | `object` | No | — | Starting values for rotation, scale, opacity, and frame index. |

### Animation Keyframe

Each key in the `Animation` object is a lifetime percentage (0–100). Values at each keyframe:

| Field | Type | Description |
|-------|------|-------------|
| `FrameIndex` | `MinMax` | Sprite sheet frame index range. |
| `Scale` | `{ X: MinMax, Y: MinMax }` | Scale at this point in the particle's life. |
| `Rotation` | `{ X: MinMax, Y: MinMax, Z: MinMax }` | Rotation in degrees. |
| `Opacity` | `number` | Opacity from 0 (invisible) to 1 (fully opaque). |
| `Color` | `string` | Hex colour tint at this keyframe. |

### MinMax

| Field | Type | Description |
|-------|------|-------------|
| `Min` | `number` | Minimum value of the random range. |
| `Max` | `number` | Maximum value of the random range. |

## Examples

**Simple particle system** (`Assets/Server/Particles/Dust_Sparkles_Fine.particlesystem`):

```json
{
  "Spawners": [
    {
      "SpawnerId": "Dust_Sparkles_Fine",
      "FixedRotation": true,
      "WaveDelay": { "Min": 4, "Max": 36 }
    },
    { "SpawnerId": "Dust_Sparkles_Fine" },
    { "SpawnerId": "Dust_Sparkles_Fine" }
  ],
  "CullDistance": 30
}
```

**Multi-spawner effect with delays** (`Assets/Server/Particles/Deployables/Healing_Totem/Totem_Heal_Simple_Test.json`):

```json
{
  "Spawners": [
    { "SpawnerId": "Totem_Heal_Ground_Line",      "PositionOffset": { "Z": 0 }, "FixedRotation": false, "StartDelay": 1.2 },
    { "SpawnerId": "Totem_Heal_Uhr",              "PositionOffset": { "Y": 0.1 }, "StartDelay": 0.8 },
    { "SpawnerId": "Totem_Heal_Ground_Constant",   "PositionOffset": { "Z": 0 }, "FixedRotation": false, "StartDelay": 0.5 },
    { "SpawnerId": "Totem_Heal_Sparks_Constant",   "PositionOffset": { "Y": 0.5 }, "StartDelay": 0.5 }
  ],
  "LifeSpan": 9,
  "CullDistance": 100
}
```

## Related Pages

- [Server Models](/hytale-modding-docs/reference/models-and-visuals/server-models) — entity models that can emit particle systems
- [Camera Effects](/hytale-modding-docs/reference/game-configuration/camera-effects) — visual effects triggered alongside particles during combat
- [Weather System](/hytale-modding-docs/reference/world-and-environment/weather-system) — weather particles for rain, snow, and dust
