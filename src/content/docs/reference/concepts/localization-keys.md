---
title: Localization Keys
description: How Hytale handles text translation using key-value language files.
---

## Overview

All player-facing text in Hytale uses translation keys instead of hardcoded strings. This enables multi-language support. Keys are defined in `.lang` files under the `Languages/` directories.

## File Locations

- `Server/Languages/*.lang` — Server-side strings (item names, NPC names, quest text)
- `Common/Languages/*.lang` — Client-side strings (UI labels, tooltips, menus)

## Language File Format

Language files use a simple `key=value` format, one entry per line:

```
server.items.sword_iron.name=Iron Sword
server.items.sword_iron.description=A sturdy blade forged from iron.
server.npc.chicken.name=Chicken
server.npc.bear_grizzly.name=Grizzly Bear
```

## Using Translation Keys

### In Item Definitions

```json
{
  "TranslationProperties": {
    "Name": "server.items.sword_iron.name",
    "Description": "server.items.sword_iron.description"
  }
}
```

### In NPC Roles

```json
{
  "Modify": {
    "NameTranslationKey": "server.npc.chicken.name"
  }
}
```

### In Portal Types

```json
{
  "Description": {
    "DisplayName": "server.portals.dungeon_entrance.name",
    "FlavorText": "server.portals.dungeon_entrance.flavor",
    "Tips": [
      "server.portals.dungeon_entrance.tip1",
      "server.portals.dungeon_entrance.tip2"
    ]
  }
}
```

## Key Naming Conventions

| Pattern | Used For |
|---------|----------|
| `server.items.{id}.name` | Item display names |
| `server.items.{id}.description` | Item descriptions |
| `server.npc.{id}.name` | NPC display names |
| `server.blocks.{id}.name` | Block display names |
| `server.portals.{id}.*` | Portal UI text |
| `server.quests.{id}.*` | Quest text |

## Adding Translations for Mods

Create a language file in your mod's `Server/Languages/` directory:

```
mymod.items.magic_staff.name=Magic Staff
mymod.items.magic_staff.description=A staff imbued with arcane power.
```

Use a unique prefix (your mod name) to avoid conflicts with base game keys.

## Related Pages

- [Item Definitions](/hytale-modding-docs/reference/item-system/item-definitions/) — TranslationProperties usage
- [NPC Roles](/hytale-modding-docs/reference/npc-system/npc-roles/) — NameTranslationKey
