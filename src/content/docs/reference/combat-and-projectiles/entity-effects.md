---
title: Entity Effects
description: Reference for server-side entity effect definitions in Hytale, covering duration, visual tints, stat modifiers, damage-over-time, and overlap behaviour.
---

## Overview

Entity effects are temporary or permanent modifiers applied to entities at runtime. They drive a wide range of systems: visual tints and screen overlays on damage, food buffs that boost max health, damage-over-time from burns and poison, crowd-control effects like root and stun, and cosmetic particle trails on weapon abilities. Each effect file defines its duration, overlap rules, stat modifications, and visual/audio feedback.

## File Location

```
Assets/Server/Entity/Effects/
```

Subdirectories group effects by category:

```
Assets/Server/Entity/Effects/
  BlockPlacement/     (block place success/fail feedback)
  Damage/             (hit flash effects)
  Deployables/        (totem heal/slow auras)
  Drop/               (item rarity glow effects)
  Food/
    Boost/            (max-stat increases from food)
    Buff/             (instant heals and timed buffs)
  GameMode/           (creative mode visual)
  Immunity/           (dodge invulnerability, fire/env immunity)
  Mana/               (mana regen and drain effects)
  Movement/           (dodge directional effects)
  Npc/                (NPC death, heal, return-home)
  Portals/            (teleport visual)
  Projectiles/        (arrow, bomb, rubble sub-effects)
  Stamina/            (stamina broken, error, regen delay)
  Status/             (burn, freeze, poison, root, slow, stun)
  Weapons/            (weapon signature and ability effects)
```

## Schema

### Top-level fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Duration` | `number` | Yes | — | Length of the effect in seconds. `0` or `0.0` means the effect fires once instantly. |
| `Infinite` | `boolean` | No | `false` | If `true`, the effect persists indefinitely until explicitly removed. Overrides `Duration`. |
| `OverlapBehavior` | `"Overwrite" \| "Extend"` | No | — | How to handle re-application while already active. `Overwrite` replaces the timer; `Extend` adds to remaining duration. |
| `RemovalBehavior` | `string` | No | — | How the effect is removed. Known value: `"Duration"` (removed when timer expires). |
| `Debuff` | `boolean` | No | `false` | If `true`, the effect is classified as a debuff and can be cleansed by antidote-type interactions. |
| `Invulnerable` | `boolean` | No | `false` | If `true`, the entity cannot take damage while the effect is active. |
| `StatusEffectIcon` | `string` | No | — | Path to the UI icon displayed in the status effect bar. |
| `DeathMessageKey` | `string` | No | — | Localisation key for the death message when this effect kills an entity. |
| `ApplicationEffects` | `ApplicationEffects` | No | — | Visual, audio, and movement modifications applied while the effect is active. |
| `StatModifiers` | `object` | No | — | Map of stat ID to flat value added per tick (e.g. `{"Health": 2}`). |
| `ValueType` | `string` | No | — | How `StatModifiers` values are interpreted. Known value: `"Percent"`. |
| `RawStatModifiers` | `object` | No | — | Map of stat ID to an array of raw modifier objects for advanced stat manipulation. |
| `DamageCalculator` | `DamageCalculator` | No | — | Periodic damage applied while the effect is active. |
| `DamageCalculatorCooldown` | `number` | No | — | Seconds between each damage tick from the `DamageCalculator`. |
| `DamageEffects` | `object` | No | — | Sound events triggered on each damage tick. |
| `ModelOverride` | `ModelOverride` | No | — | Replaces the entity's visual model for the effect duration (e.g. root vines). |

### ApplicationEffects

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `EntityTopTint` | `string` | No | — | Hex colour applied to the upper portion of the entity model. |
| `EntityBottomTint` | `string` | No | — | Hex colour applied to the lower portion of the entity model. |
| `ScreenEffect` | `string` | No | — | Path to a screen overlay texture (e.g. `"ScreenEffects/Fire.png"`). |
| `HorizontalSpeedMultiplier` | `number` | No | — | Multiplier applied to horizontal movement speed. `0.5` = 50% speed. |
| `KnockbackMultiplier` | `number` | No | — | Multiplier for incoming knockback. `0` = immune to knockback. |
| `ModelVFXId` | `string` | No | — | ID of a model-level VFX to attach to the entity. |
| `Particles` | `ParticleRef[]` | No | — | List of particle systems to spawn on the entity. |
| `MovementEffects` | `object` | No | — | Movement overrides. Contains `DisableAll: true` to fully immobilise the entity. |
| `WorldSoundEventId` | `string` | No | — | Sound event audible to all nearby players. |
| `LocalSoundEventId` | `string` | No | — | Sound event audible only to the affected player. |

### ParticleRef

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `SystemId` | `string` | Yes | — | Particle system ID to spawn. |
| `TargetEntityPart` | `string` | No | — | Entity part to attach the particle to (e.g. `"Entity"`). |
| `TargetNodeName` | `string` | No | — | Bone or node name for attachment (e.g. `"Hip"`). |
| `PositionOffset` | `Vector3` | No | — | Local offset from the attachment point. |
| `Color` | `string` | No | — | Hex colour override for the particle system. |

### RawStatModifier

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Amount` | `number` | Yes | — | Modifier value. Interpretation depends on `CalculationType`. |
| `CalculationType` | `"Additive" \| "Multiplicative"` | Yes | — | `Additive` adds a flat value to the target; `Multiplicative` scales the target by the amount. |
| `Target` | `string` | Yes | — | Which aspect of the stat to modify. Known value: `"Max"` (modifies the stat's maximum). |

### DamageCalculator

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `BaseDamage` | `object` | Yes | — | Map of damage type ID to damage value (e.g. `{"Fire": 5}`). |

### ModelOverride

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Model` | `string` | Yes | — | Path to the replacement `.blockymodel` file. |
| `Texture` | `string` | Yes | — | Path to the replacement texture. |
| `AnimationSets` | `object` | No | — | Map of animation state name to animation definitions (e.g. `Spawn`, `Despawn`). |

## Examples

**Burn status effect** (`Assets/Server/Entity/Effects/Status/Burn.json`):

```json
{
  "ApplicationEffects": {
    "EntityBottomTint": "#100600",
    "EntityTopTint": "#cf2302",
    "ScreenEffect": "ScreenEffects/Fire.png",
    "WorldSoundEventId": "SFX_Effect_Burn_World",
    "LocalSoundEventId": "SFX_Effect_Burn_Local",
    "Particles": [{ "SystemId": "Effect_Fire" }],
    "ModelVFXId": "Burn"
  },
  "DamageCalculatorCooldown": 1,
  "DamageCalculator": {
    "BaseDamage": { "Fire": 5 }
  },
  "DamageEffects": {
    "WorldSoundEventId": "SFX_Effect_Burn_World",
    "PlayerSoundEventId": "SFX_Effect_Burn_Local"
  },
  "OverlapBehavior": "Overwrite",
  "Debuff": true,
  "StatusEffectIcon": "UI/StatusEffects/Burn.png",
  "Duration": 3,
  "DeathMessageKey": "server.general.deathCause.burn"
}
```

**Food buff with max-health boost** (`Assets/Server/Entity/Effects/Food/Boost/Food_Health_Boost_Large.json`):

```json
{
  "RawStatModifiers": {
    "Health": [
      {
        "Amount": 30,
        "CalculationType": "Additive",
        "Target": "Max"
      }
    ]
  },
  "Duration": 480,
  "OverlapBehavior": "Overwrite",
  "StatusEffectIcon": "UI/StatusEffects/AddHealth/Large.png"
}
```

**Dagger dash invulnerability** (`Assets/Server/Entity/Effects/Weapons/Dagger_Dash.json`):

```json
{
  "Duration": 0.25,
  "ApplicationEffects": {
    "Particles": [
      {
        "SystemId": "Daggers_Dash_Straight",
        "TargetEntityPart": "Entity",
        "TargetNodeName": "Hip",
        "PositionOffset": { "Y": 1.0 },
        "Color": "#d7e5ec"
      }
    ],
    "ModelVFXId": "Dagger_Dash"
  },
  "OverlapBehavior": "Extend",
  "Invulnerable": true
}
```

## Related Pages

- [Entity Stats](/hytale-modding-docs/reference/combat-and-projectiles/entity-stats) — stats modified by effects
- [Damage Types](/hytale-modding-docs/reference/combat-and-projectiles/damage-types) — damage type IDs used in `DamageCalculator`
- [Projectile Configs](/hytale-modding-docs/reference/combat-and-projectiles/projectile-configs) — projectiles that apply effects on hit
