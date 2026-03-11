---
title: Projectile Configs
description: Reference for projectile configuration files in Hytale, defining launch physics, spawn offsets, and interaction chains for weapon-fired projectiles.
---

## Overview

Projectile config files define how a weapon launches a projectile: the model used, physics parameters, spawn position, and what happens when the projectile hits, misses, or bounces. They act as the bridge between a weapon's attack action and the runtime projectile entity. Configs support inheritance via a `Parent` field, allowing shared base configs to be overridden per-weapon.

## File Location

```
Assets/Server/ProjectileConfigs/
  Weapons/
    Arrows/
    Bows/
    Crossbow/
    Shortbow/
    Staff/
    Throwables/
    ...
  NPCs/
  _Debug/
```

## Schema

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Parent` | `string` | No | — | ID of another projectile config to inherit fields from. Child fields override parent fields. |
| `Model` | `string` | No | — | Visual model ID used for the projectile (e.g. `"Arrow_Crude"`, `"Ice_Ball"`). |
| `Physics` | `PhysicsConfig` | No | — | Physics simulation parameters. See below. |
| `LaunchForce` | `number` | No | — | Scalar force applied at launch, scaled by charge level where applicable. |
| `LaunchLocalSoundEventId` | `string` | No | — | Sound event played locally for the shooter on launch. |
| `LaunchWorldSoundEventId` | `string` | No | — | Sound event played in the world (audible to nearby players) on launch. |
| `SpawnOffset` | `Vector3` | No | — | Local-space offset (X/Y/Z) from the weapon's origin where the projectile spawns. |
| `SpawnRotationOffset` | `RotationOffset` | No | — | Additional rotation applied to the projectile at spawn. |
| `Interactions` | `InteractionMap` | No | — | Named interaction events and their chained action lists. See below. |

### PhysicsConfig

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Type` | `"Standard"` | No | `"Standard"` | Physics simulation model. Currently only `"Standard"` is used. |
| `Gravity` | `number` | No | — | Gravitational acceleration applied per second. |
| `TerminalVelocityAir` | `number` | No | — | Maximum speed in air. |
| `TerminalVelocityWater` | `number` | No | — | Maximum speed in water. |
| `RotationMode` | `"VelocityDamped" \| "Fixed"` | No | — | Controls how the projectile's orientation tracks its velocity vector. |
| `Bounciness` | `number` | No | `0` | Fraction of speed retained after a surface bounce. |
| `BounceCount` | `number` | No | — | Number of times the projectile can bounce before stopping. |
| `BounceLimit` | `number` | No | — | Maximum number of bounces allowed. |
| `AllowRolling` | `boolean` | No | `false` | Whether the projectile can roll along surfaces after bouncing. |
| `SticksVertically` | `boolean` | No | `false` | Whether the projectile embeds vertically in surfaces on impact. |

### Vector3

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `X` | `number` | Yes | — | Lateral offset. |
| `Y` | `number` | Yes | — | Vertical offset. |
| `Z` | `number` | Yes | — | Forward offset. |

### RotationOffset

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Pitch` | `number` | No | `0` | Pitch offset in degrees. |
| `Yaw` | `number` | No | `0` | Yaw offset in degrees. |
| `Roll` | `number` | No | `0` | Roll offset in degrees. |

### InteractionMap

The `Interactions` object maps event names to `InteractionHandler` objects. Supported event keys:

| Key | When it fires |
|-----|---------------|
| `ProjectileSpawn` | Immediately when the projectile is created. |
| `ProjectileHit` | When the projectile hits an entity. |
| `ProjectileMiss` | When the projectile hits terrain or expires. |
| `ProjectileBounce` | When the projectile bounces off a surface. |

### InteractionHandler

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Cooldown` | `object` | No | — | Optional cooldown gating on this handler. |
| `Interactions` | `string[] \| object[]` | Yes | — | Ordered list of named interaction IDs or inline interaction definitions to execute. |

## Examples

**Base arrow config** (`Assets/Server/ProjectileConfigs/Weapons/Arrows/Projectile_Config_Arrow_Base.json`):

```json
{
  "Model": "Arrow_Crude",
  "SpawnRotationOffset": {
    "Pitch": 2,
    "Yaw": 0.25,
    "Roll": 0
  },
  "Physics": {
    "Type": "Standard",
    "Gravity": 15,
    "TerminalVelocityAir": 50,
    "TerminalVelocityWater": 15,
    "RotationMode": "VelocityDamped",
    "Bounciness": 0.0,
    "SticksVertically": true
  },
  "LaunchForce": 30,
  "SpawnOffset": {
    "X": 0.15,
    "Y": -0.25,
    "Z": 0
  }
}
```

**Two-handed bow arrow** (`Projectile_Config_Arrow_Two_Handed_Bow.json`) — inherits from base and adds interactions:

```json
{
  "Parent": "Projectile_Config_Arrow_Base",
  "LaunchLocalSoundEventId": "SFX_Bow_T2_Shoot",
  "LaunchWorldSoundEventId": "SFX_Bow_T2_Shoot",
  "LaunchForce": 5,
  "Interactions": {
    "ProjectileHit": {
      "Interactions": [
        "Bow_Two_Handed_Projectile_Damage",
        "Bow_Two_Handed_Projectile_Damage_End"
      ]
    },
    "ProjectileMiss": {
      "Interactions": [
        "Bow_Two_Handed_Projectile_Miss",
        "Bow_Two_Handed_Projectile_Miss_End"
      ]
    }
  }
}
```

**Ice ball staff config** (`Assets/Server/ProjectileConfigs/Weapons/Staff/Ice/Projectile_Config_Ice_Ball.json`):

```json
{
  "Model": "Ice_Ball",
  "LaunchForce": 30,
  "Physics": {
    "Type": "Standard",
    "Gravity": 4.4,
    "TerminalVelocityAir": 42.5,
    "TerminalVelocityWater": 15,
    "RotationMode": "VelocityDamped",
    "Bounciness": 0.0,
    "SticksVertically": true
  },
  "LaunchWorldSoundEventId": "SFX_Staff_Ice_Shoot",
  "Interactions": {
    "ProjectileHit": {
      "Interactions": [
        {
          "Parent": "DamageEntityParent",
          "DamageCalculator": {
            "Class": "Charged",
            "BaseDamage": { "Ice": 20 }
          },
          "DamageEffects": {
            "Knockback": {
              "Type": "Force",
              "Force": 20,
              "VelocityType": "Set"
            },
            "WorldParticles": [
              { "SystemId": "Impact_Ice" },
              { "SystemId": "IceBall_Explosion" }
            ],
            "WorldSoundEventId": "SFX_Ice_Ball_Death"
          }
        },
        { "Type": "RemoveEntity", "Entity": "User" }
      ]
    },
    "ProjectileMiss": {
      "Interactions": [
        {
          "Type": "Simple",
          "Effects": {
            "WorldSoundEventId": "SFX_Ice_Ball_Death",
            "WorldParticles": [
              { "SystemId": "IceBall_Explosion" }
            ]
          }
        },
        { "Type": "RemoveEntity", "Entity": "User" }
      ]
    }
  }
}
```

## Related Pages

- [Projectiles](/hytale-modding-docs/reference/combat-and-projectiles/projectiles) — projectile physics and damage values
- [Damage Types](/hytale-modding-docs/reference/combat-and-projectiles/damage-types) — damage type hierarchy used in `BaseDamage`
