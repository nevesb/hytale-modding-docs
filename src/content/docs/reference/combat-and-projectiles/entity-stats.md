---
title: Entity Stats
description: Reference for server-side entity stat definitions in Hytale, covering base values, regeneration rules, conditions, and threshold effects.
---

## Overview

Entity stats define numeric attributes such as health, stamina, mana, and oxygen that are tracked per entity. Each stat file declares the value range, optional regeneration rules with conditional logic, and threshold-triggered effects. Stats are consumed by the combat system, movement system, and effect system to gate abilities, apply damage, and trigger status changes.

## File Location

```
Assets/Server/Entity/Stats/
```

One JSON file per stat:

```
Assets/Server/Entity/Stats/
  Ammo.json
  DeployablePreview.json
  GlidingActive.json
  Health.json
  Immunity.json
  MagicCharges.json
  Mana.json
  Oxygen.json
  SignatureCharges.json
  SignatureEnergy.json
  Stamina.json
  StaminaRegenDelay.json
```

## Schema

### Top-level fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `InitialValue` | `number` | Yes | — | Starting value of the stat when the entity spawns. |
| `Min` | `number` | Yes | — | Minimum value the stat can reach. Can be negative (e.g. stamina overdrawn state). |
| `Max` | `number` | Yes | — | Maximum value the stat can reach. `0` means the cap is set dynamically (e.g. by equipment). |
| `Shared` | `boolean` | No | `false` | If `true`, the stat value is synchronised to all nearby clients for HUD display. |
| `ResetType` | `string` | No | — | How the stat resets on respawn. Known value: `"MaxValue"` (resets to `Max`). |
| `IgnoreInvulnerability` | `boolean` | No | `false` | If `true`, modifications to this stat bypass invulnerability checks. |
| `HideFromTooltip` | `boolean` | No | `false` | If `true`, the stat is hidden from the player-facing tooltip UI. |
| `Regenerating` | `RegenRule[]` | No | — | List of regeneration rules evaluated in order. Multiple rules can stack or conflict. |
| `MinValueEffects` | `ThresholdEffects` | No | — | Interactions triggered when the stat reaches its minimum value. |
| `MaxValueEffects` | `ThresholdEffects` | No | — | Interactions triggered when the stat reaches its maximum value. |

### RegenRule

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `$Comment` | `string` | No | — | Human-readable note ignored by the engine. |
| `Interval` | `number` | Yes | — | Seconds between each regeneration tick. |
| `Amount` | `number` | Yes | — | Value added (or subtracted if negative) per tick. |
| `RegenType` | `"Additive" \| "Percentage"` | Yes | — | `Additive` adds a flat value; `Percentage` adds a fraction of the max. |
| `ClampAtZero` | `boolean` | No | `false` | If `true`, the regen tick will not push the value below zero. |
| `Conditions` | `Condition[]` | No | — | All conditions must be met for this rule to be active. |

### Condition

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Id` | `string` | Yes | — | Condition type identifier. Known values: `"Alive"`, `"Player"`, `"NoDamageTaken"`, `"Stat"`, `"Wielding"`, `"Sprinting"`, `"Gliding"`, `"Charging"`, `"Suffocating"`, `"RegenHealth"`. |
| `Inverse` | `boolean` | No | `false` | If `true`, the condition is negated (must NOT be met). |
| `Delay` | `number` | No | — | Seconds that must elapse since the condition was last true. Used with `"NoDamageTaken"` to create regen delays. |
| `GameMode` | `string` | No | — | Required game mode. Used with `"Player"` condition, e.g. `"Creative"`. |
| `Stat` | `string` | No | — | Stat ID to compare against. Used with `"Stat"` condition. |
| `Amount` | `number` | No | — | Threshold value for stat comparison. Used with `"Stat"` condition. |
| `Comparison` | `string` | No | — | Comparison operator. Known values: `"Gte"` (greater-than-or-equal), `"Lt"` (less-than). |

### ThresholdEffects

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `TriggerAtZero` | `boolean` | No | `false` | If `true`, fires when the stat reaches exactly zero rather than the actual min. |
| `Interactions` | `object` | No | — | Container with an `Interactions` array of interaction objects (e.g. `ChangeStat`, `ClearEntityEffect`, `ApplyEffect`). |

## Examples

**Health** (`Assets/Server/Entity/Stats/Health.json`):

```json
{
  "InitialValue": 100,
  "Min": 0,
  "Max": 100,
  "Shared": true,
  "ResetType": "MaxValue",
  "Regenerating": [
    {
      "$Comment": "NPC",
      "Interval": 0.5,
      "Amount": 0.05,
      "RegenType": "Percentage",
      "Conditions": [
        { "Id": "Alive" },
        { "Id": "Player", "Inverse": true },
        { "Id": "NoDamageTaken", "Delay": 15 },
        { "Id": "RegenHealth" }
      ]
    },
    {
      "$Comment": "Player in creative mode",
      "Interval": 0.5,
      "Amount": 1.0,
      "RegenType": "Percentage",
      "Conditions": [
        { "Id": "Alive" },
        { "Id": "Player", "GameMode": "Creative" }
      ]
    }
  ]
}
```

**Immunity** (`Assets/Server/Entity/Stats/Immunity.json`):

```json
{
  "InitialValue": 0,
  "Min": 0,
  "Max": 100,
  "Shared": true,
  "Regenerating": [
    {
      "Interval": 0.1,
      "Amount": -0.1,
      "RegenType": "Additive"
    }
  ],
  "MaxValueEffects": {
    "Interactions": {
      "Interactions": [
        {
          "Type": "ApplyEffect",
          "EffectId": "Immune"
        }
      ]
    }
  }
}
```

## Related Pages

- [Entity Effects](/hytale-modding-docs/reference/combat-and-projectiles/entity-effects) — effects triggered by stat thresholds
- [Damage Types](/hytale-modding-docs/reference/combat-and-projectiles/damage-types) — damage that modifies the Health stat
- [Projectiles](/hytale-modding-docs/reference/combat-and-projectiles/projectiles) — projectile damage applied to stats
