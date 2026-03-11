---
title: Inheritance and Templates
description: How Hytale uses template inheritance to reduce duplication across JSON configuration files.
---

## Overview

Hytale's configuration system uses a template inheritance model. Instead of defining every field for each entity, you create base templates with shared properties, then extend them with specific overrides. This pattern appears across NPC roles, items, gameplay configs, and damage types.

## How Inheritance Works

```mermaid
flowchart TD;
    A["Base Template<br>Template_Beasts_Passive"] --> B[Chicken Role]
    A --> C[Rabbit Role]
    A --> D[Sheep Role]

    B -->|"Reference + Modify"| E["Chicken<br>HP: 15, Speed: 1.2<br>Drops: Feathers"]
    C -->|"Reference + Modify"| F["Rabbit<br>HP: 10, Speed: 2.0<br>Drops: Rabbit Hide"]
    D -->|"Reference + Modify"| G["Sheep<br>HP: 20, Speed: 1.0<br>Drops: Wool"]

    H[Shared from Template] --> I[AI: Passive Wander]
    H --> J[Flee when attacked]
    H --> K[Sensing range: 10]
    H --> L[Sound reactions]

    style A fill:#4a3d8f,color:#fff
    style E fill:#2d5a27,color:#fff
    style F fill:#2d5a27,color:#fff
    style G fill:#2d5a27,color:#fff
    style H fill:#2d6a8f,color:#fff
```

### Resolution Order

```mermaid
flowchart LR;
    A["Role File<br>Chicken.json"] -->|"1. Read Reference"| B["Template File<br>Template_Beasts_Passive"]
    B -->|"2. Load Base"| C["Full Template<br>All fields defined"]
    C -->|"3. Apply Modify"| D["Override<br>Appearance, Stats,<br>Drops, Speed"]
    D -->|"4. Result"| E["Final NPC Definition<br>Template + Overrides"]

    style A fill:#8b6500,color:#fff
    style E fill:#2d5a27,color:#fff
```

## Inheritance Mechanisms

### Reference + Modify (NPC Roles)

The most common pattern for NPCs. The `Reference` field points to a template, and `Modify` overrides specific fields:

```json
{
  "Reference": "Template_Beasts_Passive_Critter",
  "Modify": {
    "Appearance": "Chicken",
    "MaxHealth": 10,
    "MaxSpeed": 3.0,
    "DropList": "Drop_Chicken",
    "NameTranslationKey": "server.npc.chicken.name"
  }
}
```

The resulting NPC inherits all properties from `Template_Beasts_Passive_Critter` (AI behavior, view range, hearing, flock patterns, etc.) and only overrides the five fields listed in `Modify`.

### Parent (Items, Configs)

Items and gameplay configs use a `Parent` field for single-level inheritance:

```json
{
  "Parent": "Template_Food",
  "TranslationProperties": {
    "Name": "server.items.food_bread.name",
    "Description": "server.items.food_bread.description"
  },
  "Quality": "Uncommon",
  "Recipe": {
    "Input": [{ "ItemId": "Ingredient_Dough", "Quantity": 1 }],
    "Output": [{ "ItemId": "Food_Bread", "Quantity": 1 }],
    "BenchRequirement": { "Type": "Processing", "Id": "Cookingbench" },
    "TimeSeconds": 8
  }
}
```

### Inherits (Damage Types)

Damage types use `Inherits` for classification hierarchies:

```json
{
  "Inherits": "Physical"
}
```

This creates a chain: `Bludgeoning` inherits from `Physical`, which inherits from the base `Damage` type.

### Variant Type

Some NPC files use `"Type": "Variant"` to define multiple variations of the same base entity:

```json
{
  "Type": "Variant",
  "Reference": "Template_Livestock_Cow",
  "Modify": {
    "Appearance": "Cow_Brown"
  }
}
```

## Parameters and Compute

Templates can define parameters with default values, which concrete entities can override:

```json
{
  "Parameters": {
    "BaseHealth": {
      "Value": 100,
      "Description": "Base health for this NPC tier"
    },
    "SpeedMultiplier": {
      "Value": 1.0,
      "Description": "Movement speed modifier"
    }
  },
  "MaxHealth": { "Compute": "BaseHealth" },
  "MaxSpeed": { "Compute": "4.0 * SpeedMultiplier" }
}
```

A child entity overrides parameters to change computed values without redefining the formulas.

## Template Hierarchy

Templates are typically organized in `_Core/Templates/` directories:

```
Server/NPC/Roles/
├── _Core/
│   └── Templates/
│       ├── Template_Beasts_Passive_Critter.json
│       ├── Template_Beasts_Hostile.json
│       ├── Template_Livestock_Cow.json
│       └── Template_Intelligent_Villager.json
├── Critter/
│   ├── Chicken.json          (References Template_Beasts_Passive_Critter)
│   └── Rabbit.json           (References Template_Beasts_Passive_Critter)
└── Beast/
    ├── Bear_Grizzly.json     (References Template_Beasts_Hostile)
    └── Wolf.json             (References Template_Beasts_Hostile)
```

## Best Practices

- **Always reference a template** when creating new entities — don't define every field from scratch
- **Override only what's different** — keep `Modify` blocks small
- **Use Parameters for tuning** — makes balancing easier without touching formulas
- **Check the template first** — read the template file to understand what defaults you inherit

## Related Pages

- [NPC Roles](/hytale-modding-docs/reference/npc-system/npc-roles/) — where Reference/Modify is most used
- [NPC Templates](/hytale-modding-docs/reference/npc-system/npc-templates/) — available base templates
- [Item Definitions](/hytale-modding-docs/reference/item-system/item-definitions/) — Parent inheritance for items
- [Damage Types](/hytale-modding-docs/reference/combat-and-projectiles/damage-types/) — Inherits hierarchy
