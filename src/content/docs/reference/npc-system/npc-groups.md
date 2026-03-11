---
title: NPC Groups
description: Group definition files that collect NPC role IDs into named sets used by spawn tables, attitude lookups, and suppression volumes.
---

## Overview

NPC Group files define named collections of role IDs. A group gives a single name to a set of roles so that spawn rules, attitude tables, and suppression volumes can refer to the whole set without listing every individual role. Role IDs support a `*` wildcard suffix to match all roles whose name starts with a given prefix.

## File Location

`Assets/Server/NPC/Groups/**/*.json`

Groups are organized in subdirectories that mirror the `Roles/` tree (e.g. `Groups/Creature/Livestock/Chicken.json` for the Chicken flock group, `Groups/Birds.json` for all birds).

## Schema

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `IncludeRoles` | string[] | Yes | — | List of role IDs to include in this group. Supports a `*` wildcard suffix (e.g. `"Trilobite*"` matches all roles whose ID starts with `"Trilobite"`). |

## Wildcard Matching

A trailing `*` in a role ID matches all roles with that prefix. This is useful for variant families:

```json
{ "IncludeRoles": ["Trilobite*", "Jellyfish*", "Tang*"] }
```

This matches `Trilobite`, `Trilobite_Small`, `Jellyfish_Blue`, etc. without listing each variant explicitly.

## Examples

### Birds group

```json
{
  "IncludeRoles": [
    "Bluebird",
    "Crow",
    "Finch_Green",
    "Owl_Brown",
    "Owl_Snow",
    "Parrot",
    "Pigeon",
    "Raven",
    "Sparrow",
    "Woodpecker",
    "Duck",
    "Archaeopteryx",
    "Hawk",
    "Pterodactyl",
    "Vulture"
  ]
}
```

### Aquatic group (with wildcards)

```json
{
  "IncludeRoles": [
    "Eel_Moray",
    "Shark_Hammerhead",
    "Shellfish_Lava",
    "Trilobite*",
    "Whale_Humpback",
    "Bluegill",
    "Frostgill",
    "Minnow",
    "Pike",
    "Piranha_Black",
    "Piranha",
    "Salmon",
    "Snapjaw",
    "Trout_Rainbow",
    "Clownfish",
    "Jellyfish*",
    "Pufferfish",
    "Tang*"
  ]
}
```

### Single-species group (Chicken flock)

```json
{
  "IncludeRoles": [
    "Chicken",
    "Chicken_Chick"
  ]
}
```

## How Groups Are Used

- **Spawn rules** reference group IDs in the `Flock` field of an NPC spawn entry to define which roles can appear together.
- **Attitude files** reference group IDs in the `Groups` object to define how one NPC type feels about a whole category (e.g. all `"Predators"` are `"Hostile"` to prey animals).
- **Suppression volumes** reference group IDs in `SuppressedGroups` to prevent a category of NPCs from spawning in an area.

## Related Pages

- [NPC Roles](/hytale-modding-docs/reference/npc-system/npc-roles) — Individual role files listed inside groups
- [NPC Spawn Rules](/hytale-modding-docs/reference/npc-system/npc-spawn-rules) — Spawn files that reference group IDs via `Flock` and `SuppressedGroups`
- [NPC Attitudes](/hytale-modding-docs/reference/npc-system/npc-attitudes) — Attitude files that reference group IDs for relationship definitions
