---
title: Tag Patterns
description: Logical tag matching system used throughout Hytale's configuration.
---

## Overview

Tag patterns provide a boolean logic system for matching tagged content. They use operators like `And`, `Or`, `Not`, and `Equals` to create complex matching rules for environments, blocks, NPCs, and other tagged entities.

## File Location

`Server/TagPatterns/*.json`

## Operators

| Operator | Purpose | Fields |
|----------|---------|--------|
| `Equals` | Match a single tag | `Tag` |
| `Or` | Match any of the patterns | `Patterns` (array) |
| `And` | Match all of the patterns | `Patterns` (array) |
| `Not` | Invert a pattern | `Pattern` (single) |

## Examples

### Simple OR match

```json
{
  "Op": "Or",
  "Patterns": [
    { "Op": "Equals", "Tag": "Bush" },
    { "Op": "Equals", "Tag": "Seed" }
  ]
}
```

Matches any block tagged as either `Bush` or `Seed`.

### Complex AND + NOT

```json
{
  "Op": "And",
  "Patterns": [
    { "Op": "Equals", "Tag": "Caves" },
    {
      "Op": "Not",
      "Pattern": {
        "Op": "Or",
        "Patterns": [
          { "Op": "Equals", "Tag": "Volcanic" },
          { "Op": "Equals", "Tag": "Spiders" },
          { "Op": "Equals", "Tag": "Dungeons" }
        ]
      }
    }
  ]
}
```

Matches environments tagged as `Caves` but NOT `Volcanic`, `Spiders`, or `Dungeons`.

## Where Tags Are Used

- **Environment audio** — select ambient sounds based on environment tags
- **NPC spawning** — restrict spawns to specific tagged biomes
- **Block interactions** — match block types by tag groups

## Related Pages

- [Environments](/hytale-modding-docs/reference/world-and-environment/environments/) — environment tag usage
- [NPC Spawn Rules](/hytale-modding-docs/reference/npc-system/npc-spawn-rules/) — spawn filtering by tags
