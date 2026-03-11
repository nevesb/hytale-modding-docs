---
title: Interaction Chaining
description: How Hytale chains interactions using the Next field to create complex behaviors.
---

## Overview

Hytale builds complex gameplay behaviors by chaining simple interactions together. Each interaction has a `Type` and an optional `Next` field pointing to the following action. This creates sequential pipelines that can include conditions, damage, effects, sounds, and more.

## How Interaction Chains Work

```mermaid
flowchart TD;
    A[Player Uses Item] --> B{Condition Check};
    B -->|"Game Mode = Adventure"| C[Apply Effect];
    B -->|"Wrong Game Mode"| X[Chain Stops];
    C -->|"EffectId: Burning"| D[Deal Damage];
    D -->|"BaseDamage: Fire 10"| E[Chain Complete];
    style A fill:darkgreen,color:white;
    style X fill:darkred,color:white;
    style E fill:steelblue,color:white;```

### Projectile Hit Chain

```mermaid
flowchart LR;
    A[Projectile Hits Entity] --> B["DamageEntity<br>Fire: 15"];
    B --> C["RemoveEntity<br>Projectile destroyed"];
    style A fill:darkgoldenrod,color:white;
    style C fill:darkred,color:white;```

### Complex Weapon Chain

```mermaid
flowchart TD;
    A[Player Swings Sword] --> B{Check Durability};
    B -->|"Has durability"| C[Damage Target];
    B -->|"Broken"| X[Play Break Sound];
    C --> D[Apply Knockback];
    D --> E{Critical Hit?};
    E -->|"Yes"| F[Apply Stun Effect];
    E -->|"No"| G[Play Hit Sound];
    F --> G;
    G --> H[Reduce Durability];
    style A fill:darkgreen,color:white;
    style X fill:darkred,color:white;```

## Chain Structure

```json
{
  "Type": "Condition",
  "RequiredGameMode": "Adventure",
  "Next": {
    "Type": "ApplyEffect",
    "EffectId": "Burning",
    "Next": {
      "Type": "Damage",
      "DamageCalculator": {
        "BaseDamage": { "Fire": 10 }
      }
    }
  }
}
```

This chain: checks game mode → applies burning effect → deals fire damage.

## Interaction Types

| Type | Purpose | Key Fields |
|------|---------|------------|
| `Condition` | Gate based on requirements | `RequiredGameMode` |
| `ApplyEffect` | Apply a status effect | `EffectId` |
| `Damage` | Deal damage | `DamageCalculator`, `BaseDamage` |
| `DamageEntity` | Damage on projectile hit | `DamageCalculator` |
| `RemoveEntity` | Destroy the entity | — |
| `Simple` | Basic interaction | Varies |
| `Consume` | Use a consumable item | `Consume_Charge`, effects |

## Where Chains Are Used

- **Item Interactions** (`Server/Item/Interactions/`) — block breaking, tool usage
- **Projectile Configs** (`Server/ProjectileConfigs/`) — on-hit and on-bounce actions
- **NPC Actions** — combat ability sequences

## Projectile Interaction Example

```json
{
  "Interactions": {
    "ProjectileHit": {
      "Cooldown": 0,
      "Interactions": [
        {
          "Type": "DamageEntity",
          "DamageCalculator": { "BaseDamage": { "Fire": 15 } },
          "Next": {
            "Type": "RemoveEntity"
          }
        }
      ]
    }
  }
}
```

## Related Pages

- [Item Interactions](/hytale-modding-docs/reference/item-system/item-interactions/) — block and item interaction chains
- [Projectile Configs](/hytale-modding-docs/reference/combat-and-projectiles/projectile-configs/) — projectile event chains
- [Damage Types](/hytale-modding-docs/reference/combat-and-projectiles/damage-types/) — damage type hierarchy
