---
title: JSON Basics
description: How Hytale uses JSON for game configuration and modding.
---

## JSON in Hytale

Every piece of game content in Hytale — from NPCs to items to world generation — is defined in JSON files. Understanding the common patterns will help you create mods efficiently.

## Common Patterns

### Template Inheritance

Most JSON files support inheriting from a template using `Parent` or `Reference`:

```json
{
  "Reference": "Template_Beasts_Passive_Critter",
  "Modify": {
    "Appearance": "Chicken",
    "MaxHealth": 10,
    "DropList": "Drop_Chicken"
  }
}
```

The `Reference` points to a template file, and `Modify` overrides specific fields. This avoids duplicating common configuration across similar entities.

### Computed Values

Some fields support computed values that reference parameters:

```json
{
  "Parameters": {
    "BaseHealth": {
      "Value": 100,
      "Description": "Base health for this NPC"
    }
  },
  "MaxHealth": {
    "Compute": "BaseHealth * 1.5"
  }
}
```

### Weight-Based Selection

Drops, spawns, and shops use a weight system for random selection:

```json
{
  "Container": {
    "Type": "Choice",
    "Containers": [
      { "Weight": 70, "Item": { "ItemId": "Coin_Gold" } },
      { "Weight": 25, "Item": { "ItemId": "Gem_Ruby" } },
      { "Weight": 5, "Item": { "ItemId": "Sword_Legendary" } }
    ]
  }
}
```

Higher weight = higher probability. The total doesn't need to equal 100 — weights are relative.

### Interaction Chaining

Complex behaviors are built by chaining interactions with the `Next` field:

```json
{
  "Type": "Condition",
  "RequiredGameMode": "Adventure",
  "Next": {
    "Type": "ApplyEffect",
    "EffectId": "Poison",
    "Next": {
      "Type": "Damage",
      "DamageCalculator": {
        "BaseDamage": { "Poison": 5 }
      }
    }
  }
}
```

Each interaction triggers the next one in sequence, creating complex gameplay behaviors.

### Translation Keys

Player-visible text uses localization keys:

```json
{
  "TranslationProperties": {
    "Name": "server.items.sword_iron.name",
    "Description": "server.items.sword_iron.description"
  }
}
```

The actual text is defined in language files (`Languages/en-US.lang`):
```
server.items.sword_iron.name=Iron Sword
server.items.sword_iron.description=A sturdy blade forged from iron.
```

## File Validation

Hytale validates JSON files on server startup. Common errors:
- **Trailing commas** — JSON doesn't allow commas after the last element
- **Missing references** — `Parent` or `Reference` pointing to non-existent templates
- **Invalid field types** — String where number expected, or vice versa
- **Missing required fields** — Some fields are mandatory depending on the entity type
