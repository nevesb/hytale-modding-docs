---
title: Projectiles
description: Reference for server-side projectile definitions in Hytale, covering physics parameters, damage, sound events, and hit/miss particles.
---

## Overview

Projectile files define the physics behaviour and damage properties of individual projectile instances — arrows, spells, and other fired objects. They are the data-layer counterpart to [Projectile Configs](/hytale-modding-docs/reference/combat-and-projectiles/projectile-configs), which define launch parameters and interaction chains. Each projectile file is referenced by an `Appearance` string that links it to client-side visuals.

## File Location

```
Assets/Server/Projectiles/
```

Subdirectories group projectiles by category:

```
Assets/Server/Projectiles/
  Arrow_FullCharge.json
  Arrow_HalfCharge.json
  Arrow_NoCharge.json
  Ice_Ball.json
  Ice_Bolt.json
  Roots.json
  NPCs/
  Player/
  Spells/
    Fireball.json
```

## Schema

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Appearance` | `string` | Yes | — | Client-side appearance ID used to look up the projectile's visual model and texture. |
| `MuzzleVelocity` | `number` | Yes | — | Initial launch speed in units/second at the moment of firing. |
| `TerminalVelocity` | `number` | Yes | — | Maximum speed the projectile can reach in flight. |
| `Gravity` | `number` | Yes | — | Downward gravitational acceleration applied each second. `0` for perfectly straight shots. |
| `Bounciness` | `number` | No | `0` | Fraction of velocity retained after bouncing off a surface. `0` = no bounce. |
| `ImpactSlowdown` | `number` | No | `0` | Velocity reduction applied on impact. |
| `TimeToLive` | `number` | No | `0` | Seconds before the projectile is automatically destroyed. `0` = no timeout. |
| `Damage` | `number` | Yes | — | Base damage dealt on a successful hit. |
| `DeadTime` | `number` | No | `0` | Seconds the projectile lingers after hitting a target before being removed. |
| `DeadTimeMiss` | `number` | No | — | Seconds the projectile lingers after missing (hitting terrain). |
| `SticksVertically` | `boolean` | No | `false` | If `true`, the projectile embeds upright in surfaces rather than lying flat. |
| `PitchAdjustShot` | `boolean` | No | `false` | If `true`, the projectile's pitch is corrected based on arc trajectory. |
| `HorizontalCenterShot` | `number` | No | `0` | Horizontal accuracy offset from crosshair centre. |
| `VerticalCenterShot` | `number` | No | `0` | Vertical accuracy offset from crosshair centre. |
| `DepthShot` | `number` | No | `1` | Depth multiplier for hit detection. |
| `Radius` | `number` | No | — | Collision sphere radius. If omitted, a default capsule hitbox is used. |
| `Height` | `number` | No | — | Collision capsule height. |
| `HitSoundEventId` | `string` | No | — | Sound event played on entity hit. |
| `MissSoundEventId` | `string` | No | — | Sound event played on terrain miss. |
| `BounceSoundEventId` | `string` | No | — | Sound event played on each bounce. |
| `DeathSoundEventId` | `string` | No | — | Sound event played when the projectile expires naturally. |
| `HitParticles` | `ParticleRef` | No | — | Particle system spawned on entity hit. |
| `MissParticles` | `ParticleRef` | No | — | Particle system spawned on terrain miss. |
| `BounceParticles` | `ParticleRef` | No | — | Particle system spawned on each bounce. |
| `DeathParticles` | `ParticleRef` | No | — | Particle system spawned when the projectile expires. |
| `DeathEffectsOnHit` | `boolean` | No | `false` | If `true`, death particles and sounds also trigger on a successful entity hit. |
| `ExplosionConfig` | `object` | No | — | Configures area-of-effect explosion on impact (see below). |

### ParticleRef

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `SystemId` | `string` | Yes | — | Particle system ID to spawn. |

### ExplosionConfig

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `DamageEntities` | `boolean` | No | `false` | Whether the explosion damages nearby entities. |
| `DamageBlocks` | `boolean` | No | `false` | Whether the explosion damages nearby blocks. |
| `EntityDamageRadius` | `number` | No | — | Radius in units within which entities take damage. |
| `EntityDamageFalloff` | `number` | No | `1.0` | Damage reduction multiplier applied at the edge of the radius. |
| `BlockDamageRadius` | `number` | No | — | Radius in units within which blocks are damaged. |
| `Knockback` | `object` | No | — | Knockback applied to entities in the explosion radius. |

## Examples

**Full-charge arrow** (`Assets/Server/Projectiles/Arrow_FullCharge.json`):

```json
{
  "Appearance": "Arrow_Crude",
  "SticksVertically": true,
  "MuzzleVelocity": 50,
  "TerminalVelocity": 50,
  "Gravity": 10,
  "Bounciness": 0,
  "ImpactSlowdown": 0,
  "TimeToLive": 20,
  "Damage": 20,
  "DeadTime": 0.1,
  "HorizontalCenterShot": 0.1,
  "VerticalCenterShot": 0.1,
  "DepthShot": 1,
  "PitchAdjustShot": true,
  "HitSoundEventId": "SFX_Arrow_FullCharge_Hit",
  "MissSoundEventId": "SFX_Arrow_FullCharge_Miss",
  "HitParticles": {
    "SystemId": "Impact_Blade_01"
  }
}
```

**Fireball spell** (`Assets/Server/Projectiles/Spells/Fireball.json`):

```json
{
  "Appearance": "Fireball",
  "Radius": 0.1,
  "Height": 0.2,
  "MuzzleVelocity": 40,
  "TerminalVelocity": 100,
  "Gravity": 4,
  "Bounciness": 0,
  "TimeToLive": 0,
  "Damage": 60,
  "DeadTime": 0,
  "DeathEffectsOnHit": true,
  "MissParticles": { "SystemId": "Explosion_Medium" },
  "BounceParticles": { "SystemId": "Impact_Fire" },
  "DeathParticles": { "SystemId": "Explosion_Medium" },
  "MissSoundEventId": "SFX_Fireball_Miss",
  "DeathSoundEventId": "SFX_Fireball_Death",
  "ExplosionConfig": {
    "DamageEntities": true,
    "DamageBlocks": false,
    "EntityDamageRadius": 5,
    "EntityDamageFalloff": 1.0
  }
}
```

## Related Pages

- [Projectile Configs](/hytale-modding-docs/reference/combat-and-projectiles/projectile-configs) — launch parameters and interaction chains
- [Damage Types](/hytale-modding-docs/reference/combat-and-projectiles/damage-types) — damage type hierarchy
