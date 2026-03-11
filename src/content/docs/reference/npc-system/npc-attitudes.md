---
title: NPC Attitudes
description: Attitude files that define how an NPC type relates to other NPC groups and to item categories, controlling combat, avoidance, and social behavior.
---

## Overview

Attitude files define the social and combat disposition of an NPC type toward other groups of NPCs and toward item categories. Each file corresponds to a specific NPC role or family and lists named groups mapped to attitude values. The engine reads these files at runtime to determine whether an NPC should attack, flee, ignore, or befriend another entity it detects.

## File Location

- `Assets/Server/NPC/Attitude/Roles/**/*.json` — Attitude toward NPC groups
- `Assets/Server/NPC/Attitude/Items/**/*.json` — Attitude toward item categories

## Schema

### Role Attitude file

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Groups` | object | Yes | — | Map of attitude names to arrays of NPC group IDs. |

The `Groups` object keys are attitude names. The recognized attitude names are:

| Attitude | Meaning |
|----------|---------|
| `Friendly` | This NPC considers those groups as allies — will not attack them and may assist them. |
| `Hostile` | This NPC will attack members of these groups on sight. |
| `Neutral` | Passive awareness — neither attacks nor assists. |
| `Ignore` | Completely disregards members of these groups. |
| `Revered` | Highest positive regard — may follow or protect. |

### Item Attitude file

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Attitudes` | object | Yes | — | Map of attitude names to arrays of item category IDs. |

Item attitude names follow the same vocabulary as role attitudes (`Friendly`, `Hostile`, `Dislike`, `Love`, etc.).

## Examples

### Predator attitude (Critters file)

Critters consider most categories hostile (flee from them) but are friendly toward `Fen_Stalker`.

```json
{
  "Groups": {
    "Friendly": [
      "Fen_Stalker"
    ],
    "Hostile": [
      "Vermin",
      "Birds",
      "Predators",
      "PredatorsBig",
      "Void"
    ]
  }
}
```

### Prey attitude (Predators file)

Predators treat prey as neutral (trackable but not attacked proactively) and ignore other large predators.

```json
{
  "Groups": {
    "Neutral": [
      "Prey"
    ],
    "Ignore": [
      "Predators",
      "PreyBig"
    ]
  }
}
```

### Faction attitude (Trork)

Trorks are friendly to their own kind, hostile to Kweebecs, ignore prisoners, and revere their chieftain.

```json
{
  "Groups": {
    "Friendly": [
      "Trork"
    ],
    "Hostile": [
      "Kweebec"
    ],
    "Ignore": [
      "Kweebec_Prisoner"
    ],
    "Revered": [
      "Trork_Chieftain"
    ]
  }
}
```

### Living world attitudes

The `LivingWorld/` attitudes provide simple relationships for ambient creatures:

**Aggressive** (aggressive creatures treat passive ones as hostile):
```json
{
  "Groups": {
    "Hostile": ["Passive"]
  }
}
```

**Neutral** (neutral creatures treat aggressive ones as hostile):
```json
{
  "Groups": {
    "Hostile": ["Aggressive"]
  }
}
```

### Item attitude

```json
{
  "Attitudes": {
    "Dislike": ["Weapon"],
    "Love": ["Food"]
  }
}
```

### Empty attitude (no relationships defined)

```json
{
  "Groups": {}
}
```

## Relationship to Role Files

The `AttitudeGroup` parameter in a role's template (e.g. `"AttitudeGroup": "Prey"`) declares which group that NPC belongs to. When another NPC detects it, the engine looks up the detecting NPC's attitude file to see how it maps that group.

## Related Pages

- [NPC Roles](/hytale-modding-docs/reference/npc-system/npc-roles) — Role files that declare `DefaultNPCAttitude`, `DefaultPlayerAttitude`, and `AttitudeGroup`
- [NPC Groups](/hytale-modding-docs/reference/npc-system/npc-groups) — Group definitions referenced in `Groups` arrays
- [NPC Templates](/hytale-modding-docs/reference/npc-system/npc-templates) — Templates that set default attitude parameters
