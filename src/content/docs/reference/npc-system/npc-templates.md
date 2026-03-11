---
title: NPC Templates
description: Base template files that define shared NPC behavior, and the Reference/Modify parameter inheritance system.
---

## Overview

NPC templates are `Abstract` role files that define common behavior, stats, and AI logic shared by a family of NPCs. Concrete roles reference a template via the `Reference` field and selectively override values via `Modify`. The `Parameters` system lets templates declare named defaults with documentation that concrete roles can override without changing the template itself.

## File Location

`Assets/Server/NPC/Roles/_Core/Templates/*.json`

## The Reference / Modify Pattern

A `Variant` role file links to a template and overrides specific fields:

```json
{
  "Type": "Variant",
  "Reference": "Template_Predator",
  "Modify": {
    "Appearance": "Fox",
    "MaxHealth": 38
  }
}
```

The engine merges the template's full definition with the `Modify` block. Fields not listed in `Modify` keep the template's value. The `Reference` value is the filename without the `.json` extension.

## The Parameter / Compute System

Templates declare `Parameters` — named values with a default and a description:

```json
{
  "Parameters": {
    "MaxHealth": {
      "Value": 100,
      "Description": "Max health for the NPC"
    },
    "Appearance": {
      "Value": "Bear_Grizzly",
      "Description": "Model to be used"
    }
  }
}
```

Top-level fields in the template read from these parameters using the `Compute` shorthand:

```json
{
  "MaxHealth": { "Compute": "MaxHealth" },
  "Appearance": { "Compute": "Appearance" }
}
```

A concrete `Variant` role overrides a parameter by supplying a new value in its own `Parameters` block inside `Modify`:

```json
{
  "Type": "Variant",
  "Reference": "Template_Predator",
  "Modify": {
    "MaxHealth": 38,
    "Appearance": "Fox"
  },
  "Parameters": {
    "NameTranslationKey": {
      "Value": "server.npcRoles.Fox.name",
      "Description": "Translation key for NPC name display"
    }
  }
}
```

## Schema — Template (Abstract) fields

| Field | Type | Description |
|-------|------|-------------|
| `Type` | `"Abstract"` | Marks this file as a non-spawnable base template. |
| `StartState` | string | Initial AI state, e.g. `"Idle"`. |
| `Parameters` | object | Named parameter definitions. Each entry has `Value`, optional `TypeHint`, and `Description`. |
| `Appearance` | Compute | Resolved from `Parameters.Appearance`. |
| `MaxHealth` | Compute | Resolved from `Parameters.MaxHealth`. |
| `DropList` | Compute | Resolved from `Parameters.DropList`. |
| `NameTranslationKey` | Compute | Resolved from `Parameters.NameTranslationKey`. |
| `MotionControllerList` | array | Locomotion controllers (Walk, Fly, Swim). |
| `Instructions` | array | Full AI behavior tree shared by all variants. |
| `KnockbackScale` | number | Default knockback multiplier. |
| `DisableDamageGroups` | string[] | Damage groups blocked by default. |

## Available Base Templates

| Template | Behavior Family | Key Defaults |
|----------|----------------|--------------|
| `Template_Predator` | Aggressive hunter, will attack then flee if threatened | `ViewRange: 24`, `AlertedRange: 28`, `FleeIfNotThreatened: true` |
| `Template_Animal_Neutral` | Passive prey animal, flees when threatened | `ViewRange: 16`, `AlertedRange: 18`, `StartState: Idle` |
| `Template_Livestock` | Tameable farm animal with grazing and produce | `AlertedActionRange: 6`, `GrazingBlockSet: Grass` |
| `Template_Birds_Passive` | Flying passive bird with flock behavior | `FlockArray: ["Template_Birds_Passive"]`, `MotionControllerList: [Fly]` |
| `Template_Intelligent` | Faction NPC with combat AI and call-for-help | `AlertedRange: 45`, `ChanceToBeAlertedWhenReceivingCallForHelp: 70` |
| `Template_Beasts_Passive_Critter` | Small passive critter | Minimal stats, critter-scale flock behavior |
| `Template_Edible_Critter` | Passive critter that can be eaten | Extends critter with food interaction |
| `Template_Spirit` | Spirit entity with special movement | Spirit locomotion, particle defaults |
| `Template_Summoned_Ally` | Player-allied summon | Friendly attitude to player by default |
| `Template_Swimming_Aggressive` | Aggressive aquatic NPC | Swim locomotion, hostile AI |
| `Template_Swimming_Passive` | Passive aquatic NPC | Swim locomotion, flee behavior |
| `Template_Temple` | Temple guardian NPC | Guardian AI, high health |

## Example — Template_Animal_Neutral (abbreviated)

This is the template that `Chicken`, `Deer`, `Moose`, and other neutral animals inherit from:

```json
{
  "Type": "Abstract",
  "StartState": "Idle",
  "Parameters": {
    "Appearance": {
      "Value": "Deer_Stag",
      "Description": "The NPC's model."
    },
    "ViewRange": {
      "Value": 16,
      "Description": "The view distance of the NPC, in blocks."
    },
    "ViewSector": {
      "Value": 180,
      "Description": "The view sector of the NPC, in degrees."
    },
    "HearingRange": {
      "Value": 8,
      "Description": "The hearing distance of the NPC, in blocks."
    },
    "AbsoluteDetectionRange": {
      "Value": 4,
      "Description": "The range at which a target is guaranteed to be detected, in blocks."
    },
    "AlertedRange": {
      "Value": 18,
      "Description": "The range within which the target can be seen when alerted, in blocks."
    },
    "AlertedActionRange": {
      "Value": 8,
      "Description": "The range at which an NPC will react to players, in blocks."
    },
    "DropList": {
      "Value": "Empty",
      "Description": "The NPC's drop list."
    },
    "AttractiveItemSet": {
      "Value": [],
      "TypeHint": "String",
      "Description": "Items that are deemed attractive when held nearby."
    },
    "MaxHealth": {
      "Value": 100,
      "Description": "Max health for the NPC"
    },
    "NameTranslationKey": {
      "Value": "server.npcRoles.Template.name",
      "Description": "Translation key for NPC name display"
    }
  }
}
```

## Related Pages

- [NPC Roles](/hytale-modding-docs/reference/npc-system/npc-roles) — Full role file schema and concrete NPC examples
- [NPC Decision Making](/hytale-modding-docs/reference/npc-system/npc-decision-making) — AI condition types used inside templates
- [Inheritance and Templates](/hytale-modding-docs/reference/concepts/inheritance-and-templates) — General template inheritance across all config types
