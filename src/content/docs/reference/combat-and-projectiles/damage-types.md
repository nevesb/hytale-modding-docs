---
title: Damage Types
description: Reference for the damage type hierarchy in Hytale, including Physical, Elemental, and Environmental subtypes, and their effect on durability and stamina.
---

## Overview

Damage types form an inheritance hierarchy used by the combat system to determine resistances, effects, and penalties. Each damage type file can declare a `Parent` and `Inherits` field to extend another type's properties. Leaf types (e.g. `Fire`, `Slashing`) are what weapons and abilities actually deal; the root types (`Physical`, `Elemental`, `Environment`) exist solely to define shared sub-type behaviour.

## File Location

```
Assets/Server/Entity/Damage/
```

One JSON file per damage type:

```
Assets/Server/Entity/Damage/
  Physical.json
  Elemental.json
  Environment.json
  Environmental.json
  Bludgeoning.json   (implicit — no standalone file; defined inline)
  Slashing.json
  Fire.json
  Ice.json
  Poison.json
  Projectile.json
  Fall.json
  Drowning.json
  Suffocation.json
  OutOfWorld.json
  Command.json
```

## Schema

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Parent` | `string` | No | — | The ID of the parent damage type this type inherits from. |
| `Inherits` | `string` | No | — | Additional inheritance declaration (typically mirrors `Parent`). |
| `DurabilityLoss` | `boolean` | No | `false` | Whether hits of this type cause equipment durability loss. |
| `StaminaLoss` | `boolean` | No | `false` | Whether hits of this type deplete the target's stamina. |
| `BypassResistances` | `boolean` | No | `false` | If `true`, this damage type ignores all resistance calculations. |
| `DamageTextColor` | `string` | No | — | Hex colour used for floating damage numbers (e.g. `"#00FF00"` for poison). |
| `$Comment` | `string` | No | — | Internal comment string, not used at runtime. |

## Hierarchy

```
(root)
├── Physical                    DurabilityLoss: true, StaminaLoss: true
│   ├── Slashing                Parent: Physical
│   ├── Bludgeoning             (inherited from Physical)
│   └── Piercing                (inherited from Physical)
│
├── Elemental                   (base type for elemental sub-types)
│   ├── Fire                    Parent: Elemental
│   ├── Ice                     Parent: Elemental
│   └── Poison                  DamageTextColor: #00FF00
│
├── Projectile                  DurabilityLoss: true, StaminaLoss: false
│
├── Environment                 (base type)
│   ├── Fall                    Parent: Environment
│   └── Drowning                Parent: Environment
│
├── Environmental               DurabilityLoss: true, StaminaLoss: true, BypassResistances: false
│                               (environmental hazards: thorns, cactus, etc.)
│
├── Suffocation
├── OutOfWorld
└── Command                     DurabilityLoss: false, StaminaLoss: false, BypassResistances: true
```

## Type Descriptions

| Type | Parent | DurabilityLoss | StaminaLoss | BypassResistances | Notes |
|------|--------|---------------|-------------|-------------------|-------|
| `Physical` | — | `true` | `true` | `false` | Root physical type; facilitates sub-types. |
| `Slashing` | `Physical` | `true` | `true` | `false` | Sword, axe damage. |
| `Elemental` | — | `false` | `false` | `false` | Root elemental type; facilitates sub-types. |
| `Fire` | `Elemental` | `false` | `false` | `false` | Fire spell and ignition damage. |
| `Ice` | `Elemental` | `false` | `false` | `false` | Ice spell damage. |
| `Poison` | — | `false` | `false` | `false` | Green damage text (`#00FF00`). |
| `Projectile` | — | `true` | `false` | `false` | Arrow and thrown projectile hits. |
| `Environment` | — | — | — | — | Root type for environmental damage. |
| `Fall` | `Environment` | — | — | — | Fall damage. |
| `Drowning` | `Environment` | — | — | — | Suffocation in water. |
| `Environmental` | — | `true` | `true` | `false` | Plant hazards (thorns, cactus). |
| `Command` | — | `false` | `false` | `true` | Admin/script-applied damage; bypasses all resistances. |

## Examples

**Physical** (`Assets/Server/Entity/Damage/Physical.json`):

```json
{
  "$Comment": "This damage type exists to facilitate sub types",
  "DurabilityLoss": true,
  "StaminaLoss": true
}
```

**Slashing** (`Assets/Server/Entity/Damage/Slashing.json`):

```json
{
  "Parent": "Physical",
  "Inherits": "Physical"
}
```

**Poison** (`Assets/Server/Entity/Damage/Poison.json`):

```json
{
  "DamageTextColor": "#00FF00"
}
```

**Command** (`Assets/Server/Entity/Damage/Command.json`):

```json
{
  "DurabilityLoss": false,
  "StaminaLoss": false,
  "BypassResistances": true
}
```

**Environmental** (`Assets/Server/Entity/Damage/Environmental.json`):

```json
{
  "$Comment": "Damage type for environmental hazards like plants (bushes, cactus, etc.)",
  "DurabilityLoss": true,
  "StaminaLoss": true,
  "BypassResistances": false
}
```

## Related Pages

- [Projectiles](/hytale-modding-docs/reference/combat-and-projectiles/projectiles) — `Damage` field on projectile definitions
- [Projectile Configs](/hytale-modding-docs/reference/combat-and-projectiles/projectile-configs) — `BaseDamage` map in interaction damage calculators
