---
title: Item Interactions
description: Reference for item interaction chain JSON files in Hytale, covering interaction types, conditions, damage calculators, and chaining with Next.
---

## Overview

Item interactions define how items behave when used — attacks, block placement, consumption, tool use, dodge rolls, and more. Each interaction is a JSON object with a `Type` and an optional `Next` field that chains to the following step. This creates pipelines that can branch on conditions, deal damage, apply effects, play sounds, and spawn particles. Interaction files are referenced by ID from item definitions via the `Interactions` and `InteractionVars` fields.

## File Location

```
Assets/Server/Item/Interactions/<Category>/<InteractionId>.json
```

Top-level and root interactions:
```
Assets/Server/Item/Interactions/Block_Primary.json
Assets/Server/Item/Interactions/Block_Secondary.json
Assets/Server/Item/Interactions/Dodge.json
Assets/Server/Item/Interactions/Stamina_Bar_Flash.json
Assets/Server/Item/RootInteractions/            — Root interaction entry points
```

Subcategories:
```
Interactions/Consumables/   — Food and potion consume conditions
Interactions/Weapons/       — Weapon attack chains (Axe, Bow, Club, etc.)
Interactions/Weapons/Common/Melee/  — Shared melee damage and selector
Interactions/Tools/         — Tool-specific interactions
Interactions/Block/         — Block break/attack interactions
Interactions/Dodge/         — Dodge roll interactions
Interactions/NPCs/          — NPC-triggered interactions
Interactions/Stat_Check/    — Stat-gating conditions
```

## Schema

### Core Interaction Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Type` | string | No | `"Simple"` | Interaction type. See type list below. |
| `Next` | string or object | No | — | The next interaction to execute on success. Can be an interaction ID string or an inline interaction object. |
| `Failed` | string or object | No | — | The interaction to execute when this one fails (used by `Condition`, `UseBlock`, `PlaceBlock`, etc.). |
| `RunTime` | number | No | — | Duration in seconds this interaction occupies in the chain timeline. |
| `Effects` | object | No | — | Effects applied when this interaction executes successfully. See Effects fields below. |
| `Parent` | string | No | — | Inherits fields from the named interaction (template inheritance). |

### Interaction Types

| Type | Description |
|------|-------------|
| `Simple` | Executes immediately with no logic, then proceeds to `Next`. |
| `Condition` | Checks one or more boolean conditions. Proceeds to `Next` on pass, `Failed` on fail. |
| `MovementCondition` | Branches based on the entity's movement direction (ForwardLeft, ForwardRight, Left, Right, BackLeft, BackRight). |
| `UseBlock` | Attempts to interact with a targeted block. Falls through to `Failed` if no block is hit. |
| `PlaceBlock` | Places the held block item at the target location. |
| `Selector` | Sweeps a hitbox arc or volume to detect entities and blocks. Routes hits to `HitEntity` and `HitBlock` sub-interactions. |
| `Serial` | Executes a list of child interactions in sequence. Uses an `Interactions` array. |
| `ApplyEffect` | Applies a gameplay effect by `EffectId`. |
| `Replace` | Reads a named variable (`Var`) and substitutes its value into the chain. Falls back to `DefaultValue` if the variable is unset and `DefaultOk` is true. |

### Condition Fields (Type: `"Condition"`)

| Field | Type | Description |
|-------|------|-------------|
| `RequiredGameMode` | string | Requires the entity to be in this game mode (e.g. `"Adventure"`). |
| `Crouching` | boolean | If set, requires (`true`) or forbids (`false`) crouching. |
| `Flying` | boolean | If set, requires (`true`) or forbids (`false`) flying. |

### Selector Fields (Type: `"Selector"`)

| Field | Type | Description |
|-------|------|-------------|
| `Selector.Id` | string | Shape type of the sweep (e.g. `"Horizontal"`). |
| `Selector.Direction` | string | Sweep direction (e.g. `"ToLeft"`). |
| `Selector.TestLineOfSight` | boolean | Whether to check line-of-sight before registering hits. |
| `Selector.StartDistance` | number | Near edge of the sweep volume. |
| `Selector.EndDistance` | number | Far edge of the sweep volume. |
| `Selector.Length` | number | Arc length in degrees. |
| `Selector.YawStartOffset` | number | Yaw offset from facing direction to start the sweep. |
| `HitEntity` | object | Interaction chain executed for each entity hit. |
| `HitBlock` | object | Interaction chain executed for each block hit. |

### DamageCalculator Fields

Used inside interaction objects to define damage output.

| Field | Type | Description |
|-------|------|-------------|
| `Type` | string | Calculation method. `"Absolute"` uses a fixed base damage value. |
| `BaseDamage` | object | Map of damage type to amount (e.g. `{ "Physical": 12 }`). |
| `RandomPercentageModifier` | number | Fraction of base damage added as random variance (e.g. `0.2` = ±20%). |

### Effects Fields

| Field | Type | Description |
|-------|------|-------------|
| `WorldSoundEventId` | string | Sound event ID played at world position. |
| `LocalSoundEventId` | string | Sound event ID played locally (heard only by the acting player). |
| `WorldParticles` | object[] | Array of `{ "SystemId": "<id>" }` particle systems spawned at world position. |
| `Particles` | object[] | Particle configs with `SystemId`, `Color`, `TargetNodeName`, `TargetEntityPart`. |
| `Trails` | object[] | Weapon trail effect configs with `TrailId`, `TargetNodeName`, `PositionOffset`, `RotationOffset`. |
| `CameraEffect` | string | Camera shake/effect ID applied to the acting player (e.g. `"Impact"`, `"Sword_Swing_Diagonal_Right"`). |
| `ItemAnimationId` | string | Animation played on the held item (e.g. `"Consume"`, `"Build"`). |
| `WaitForAnimationToFinish` | boolean | Whether the chain waits for the item animation to complete before continuing. |
| `Knockback` | object | Knockback config with `Type`, `Force`, `Direction` (X/Y/Z), `VelocityType`, and `VelocityConfig`. |

## Examples

`Assets/Server/Item/Interactions/Block_Primary.json`:

```json
{
  "Type": "Simple",
  "Next": {
    "Type": "UseBlock",
    "Failed": "Block_Attack"
  }
}
```

`Assets/Server/Item/Interactions/Block_Secondary.json`:

```json
{
  "Type": "UseBlock",
  "Failed": {
    "Type": "PlaceBlock",
    "RunTime": 0.125,
    "Effects": {
      "WaitForAnimationToFinish": false,
      "ItemAnimationId": "Build"
    }
  }
}
```

`Assets/Server/Item/Interactions/Consumables/Condition_Consume_Food.json`:

```json
{
  "Type": "Condition",
  "RequiredGameMode": "Adventure",
  "Crouching": false,
  "Next": "Consume_Charge",
  "Failed": "Block_Secondary"
}
```

`Assets/Server/Item/Interactions/Dodge.json`:

```json
{
  "Type": "Condition",
  "Flying": false,
  "Next": {
    "Type": "MovementCondition",
    "ForwardLeft": { "Type": "Simple" },
    "ForwardRight": { "Type": "Simple" },
    "Left": "Dodge_Left",
    "Right": "Dodge_Right",
    "BackLeft": { "Type": "Simple" },
    "BackRight": { "Type": "Simple" }
  }
}
```

`Assets/Server/Item/Interactions/Weapons/Common/Melee/Common_Melee_Damage.json`:

```json
{
  "Parent": "DamageEntityParent",
  "DamageCalculator": {
    "BaseDamage": {
      "Physical": 6
    }
  },
  "Effects": {
    "CameraEffect": "Impact"
  },
  "DamageEffects": {
    "Knockback": {
      "Type": "Force",
      "Force": 6.5,
      "Direction": { "X": 0.0, "Y": 1.0, "Z": -1.5 },
      "VelocityType": "Set"
    },
    "WorldSoundEventId": "SFX_Sword_T2_Impact",
    "LocalSoundEventId": "SFX_Sword_T2_Impact"
  }
}
```

## Related Pages

- [Item Definitions](/hytale-modding-docs/reference/item-system/item-definitions) — Where `Interactions` and `InteractionVars` are set on items
- [Interaction Chaining](/hytale-modding-docs/reference/concepts/interaction-chaining) — Conceptual guide to building interaction pipelines
