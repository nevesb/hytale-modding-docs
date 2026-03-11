---
title: "Showcase: Dude VS Dungeon Mod"
description: A complete mod walkthrough — custom NPCs, items, dungeon instances, crafting, and loot tables working together.
---

## Overview

This showcase walks through the structure of a complete Hytale mod called **Dude VS Dungeon**. It demonstrates how multiple systems connect: custom NPCs with AI behaviors, unique weapons and armor, crafting recipes, dungeon instances with portals, and loot tables that tie everything together.

This is not a step-by-step tutorial — it's a guided tour of a finished mod to show how the pieces fit.

## Mod Structure

```
dude_vs_dungeon/
├── manifest.json
├── Server/
│   ├── NPC/
│   │   ├── Roles/
│   │   │   ├── DungeonGuard.json
│   │   │   ├── DungeonBoss.json
│   │   │   └── DungeonMinion.json
│   │   ├── Spawn/
│   │   │   └── Markers/
│   │   │       └── Dungeon_Spawns.json
│   │   └── Balancing/
│   │       ├── CAE_DungeonGuard.json
│   │       └── CAE_DungeonBoss.json
│   ├── Item/
│   │   ├── Items/
│   │   │   ├── Weapon/
│   │   │   │   └── DungeonBlade.json
│   │   │   └── Armor/
│   │   │       └── DungeonArmor_Chest.json
│   │   └── Recipes/
│   │       └── DungeonBlade_Recipe.json
│   ├── Drops/
│   │   ├── Drop_DungeonGuard.json
│   │   ├── Drop_DungeonBoss.json
│   │   └── Drop_DungeonChest.json
│   ├── Instances/
│   │   └── DungeonInstance.json
│   ├── PortalTypes/
│   │   └── DungeonPortal.json
│   └── Models/
│       ├── DungeonGuard.json
│       ├── DungeonBoss.json
│       └── DungeonMinion.json
└── Common/
    └── NPC/
        ├── DungeonGuard/
        ├── DungeonBoss/
        └── DungeonMinion/
```

## System Interactions

```mermaid
flowchart TD;
    A["Player Finds<br/>Dungeon Portal"] --> B[Enter Instance];
    B --> C["Dungeon Instance<br/>Loads Prefab];

    C --> D["Marker Spawns<br/>Activate"];
    D --> E[DungeonMinion x3];
    D --> F[DungeonGuard x2];
    D --> G[DungeonBoss x1];

    E -->|"Kill"| H["Drop Table:<br/>Common Loot"];
    F -->|"Kill"| I["Drop Table:<br/>Uncommon Loot"];
    G -->|"Kill"| J["Drop Table:<br/>Boss Loot"];

    H --> K["Materials for<br/>DungeonBlade Recipe"];
    I --> K;
    J --> L["Unique DungeonArmor<br/>Guaranteed Drop"];

    K --> M["Player Crafts<br/>DungeonBlade at Bench"];

    style A fill:darkgreen,color:white;
    style G fill:darkred,color:white;
    style L fill:rebeccapurple,color:white;
    style M fill:steelblue,color:white;```

## Key Files Explained

### 1. The Boss NPC Role

The DungeonBoss inherits from the monster template and overrides combat stats:

```json
{
  "Reference": "Template_Beasts_Aggressive_Monster",
  "Modify": {
    "Appearance": "dude_vs_dungeon:DungeonBoss",
    "Health": {
      "Parameter": "BossHealth",
      "Compute": { "Base": 500 }
    },
    "MovementSpeed": {
      "Parameter": "BossSpeed",
      "Compute": { "Base": 1.8 }
    },
    "Drops": {
      "Reference": "dude_vs_dungeon:Drop_DungeonBoss"
    },
    "CombatActionEvaluator": "dude_vs_dungeon:CAE_DungeonBoss"
  }
}
```

### 2. Boss Combat AI

The boss has multiple combat phases driven by health thresholds:

```json
{
  "EvaluationInterval": 0.5,
  "AvailableActions": {
    "SlashAttack": {
      "ActionId": "MeleeAttack_Heavy",
      "Conditions": [
        { "Type": "TargetDistance", "Curve": { "ResponseCurve": "SimpleDescendingLogistic", "XRange": [0, 5] } },
        { "Type": "TimeSinceLastUsed", "Curve": { "ResponseCurve": "Linear", "XRange": [0, 3] } }
      ]
    },
    "Enrage": {
      "ActionId": "Buff_Enrage",
      "RunConditions": [
        { "Type": "OwnStatPercent", "Stat": "Health", "Curve": "ReverseLinear" }
      ],
      "Conditions": [
        { "Type": "OwnStatPercent", "Stat": "Health", "Curve": { "Type": "Switch", "SwitchPoint": 0.3 } }
      ]
    }
  },
  "ActionSets": {
    "Default": {
      "Actions": ["SlashAttack"],
      "BasicAttackType": "MeleeAttack_Light"
    },
    "Enraged": {
      "Actions": ["SlashAttack", "Enrage"],
      "BasicAttackType": "MeleeAttack_Heavy"
    }
  }
}
```

### Combat Flow

```mermaid
flowchart TD;
    A["Boss Spawns<br/>HP: 500/500"] --> B[Default ActionSet];
    B --> C{Player in Range?};
    C -->|"Yes, < 5 blocks"| D["SlashAttack<br/>High score"];
    C -->|"No"| E[Chase Player];

    D --> F{"HP < 30%?"};
    F -->|"No"| C;
    F -->|"Yes"| G["Switch to<br/>Enraged ActionSet"];

    G --> H[Enrage Buff Active];
    H --> I["Heavy attacks only<br/>Faster evaluation"];
    I --> J{Player Dead?};
    J -->|"No"| I;
    J -->|"Yes"| K[Return to Idle];

    style A fill:darkgreen,color:white;
    style G fill:darkred,color:white;
    style H fill:darkgoldenrod,color:white;```

### 3. Boss Loot Table

Guaranteed unique armor drop + random material rewards:

```json
{
  "Container": {
    "Type": "Multiple",
    "Children": [
      {
        "Type": "Single",
        "Item": "dude_vs_dungeon:DungeonArmor_Chest",
        "Count": 1
      },
      {
        "Type": "Choice",
        "Children": [
          { "Weight": 40, "Type": "Single", "Item": "hytale:Diamond", "Count": [2, 5] },
          { "Weight": 35, "Type": "Single", "Item": "hytale:Gold_Ingot", "Count": [3, 8] },
          { "Weight": 25, "Type": "Single", "Item": "dude_vs_dungeon:DungeonShard", "Count": [1, 3] }
        ]
      }
    ]
  }
}
```

### 4. Dungeon Instance

The instance file ties everything together — the prefab, spawn markers, and portal:

```json
{
  "Prefab": "dude_vs_dungeon:Prefab_DungeonArena",
  "SpawnPoint": { "X": 8, "Y": 1, "Z": 8 },
  "Portal": "dude_vs_dungeon:DungeonPortal",
  "MaxPlayers": 4,
  "ResetTime": "PT30M",
  "Objectives": [
    {
      "Type": "KillNPC",
      "Target": "dude_vs_dungeon:DungeonBoss",
      "Count": 1
    }
  ]
}
```

### 5. The Crafted Weapon

A DungeonBlade crafted from materials dropped by dungeon mobs:

```json
{
  "Parent": "Template_Weapon_Sword",
  "Modify": {
    "TranslationKey": "dude_vs_dungeon.item.name.dungeon_blade",
    "BaseDamage": { "Slashing": 25, "Fire": 10 },
    "AttackSpeed": 1.2,
    "Durability": 500,
    "Quality": "Legendary"
  }
}
```

Recipe requiring dungeon drops:

```json
{
  "Inputs": [
    { "Item": "dude_vs_dungeon:DungeonShard", "Count": 5 },
    { "Item": "hytale:Diamond", "Count": 3 },
    { "Item": "hytale:Iron_Ingot", "Count": 10 }
  ],
  "Output": {
    "Item": "dude_vs_dungeon:DungeonBlade",
    "Count": 1
  },
  "BenchRequirement": [
    { "Id": "WorkBench", "RequiredTierLevel": 3 }
  ],
  "ProcessingTime": 10
}
```

## Systems Used

This mod demonstrates the following systems working together:

| System | Pages |
|--------|-------|
| NPC Roles & Templates | [NPC Roles](/hytale-modding-docs/reference/npc-system/npc-roles/), [NPC Templates](/hytale-modding-docs/reference/npc-system/npc-templates/) |
| Combat AI | [NPC Decision Making](/hytale-modding-docs/reference/npc-system/npc-decision-making/), [NPC Combat Balancing](/hytale-modding-docs/reference/npc-system/npc-combat-balancing/) |
| Spawn System | [NPC Spawn Rules](/hytale-modding-docs/reference/npc-system/npc-spawn-rules/) |
| Items & Crafting | [Item Definitions](/hytale-modding-docs/reference/item-system/item-definitions/), [Recipes](/hytale-modding-docs/reference/crafting-system/recipes/) |
| Loot | [Drop Tables](/hytale-modding-docs/reference/economy-and-progression/drop-tables/) |
| Dungeons | [Instances](/hytale-modding-docs/reference/game-configuration/instances/), [Portal Types](/hytale-modding-docs/reference/world-and-environment/portal-types/) |
| Mod Packaging | [Mod Packaging](/hytale-modding-docs/tutorials/advanced/mod-packaging/) |

## Takeaways

1. **Use inheritance** — the boss and weapons extend base templates, not built from scratch
2. **Connect systems** — drops feed into recipes, spawn markers activate in instances, portals gate content
3. **Layer combat complexity** — the boss uses condition-driven action sets for phase transitions
4. **Balance with weights** — loot uses weighted choices for varied but controlled rewards
5. **Namespace everything** — `dude_vs_dungeon:` prefix prevents conflicts with other mods
