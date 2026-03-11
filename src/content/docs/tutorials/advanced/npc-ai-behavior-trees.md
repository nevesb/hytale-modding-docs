---
title: NPC AI Behavior Trees
description: Deep dive into NPC AI configuration using DecisionMaking conditions, Combat Action Evaluators, behavior priorities, combat actions, and flee conditions.
---

## Goal

Build a custom NPC called the **Ironclad Sentinel** with complex AI that switches between melee and ranged combat, heals itself when low on health, calls for help from allies, and flees when critically wounded. You will configure Decision Making conditions, a Combat Action Evaluator (CAE), and wire them into an NPC role with multi-state combat behaviour.

## Prerequisites

- A mod folder with a valid `manifest.json` (see [Setup Your Dev Environment](/hytale-modding-docs/tutorials/beginner/setup-dev-environment))
- Understanding of NPC roles and templates (see [NPC Roles](/hytale-modding-docs/reference/npc-system/npc-roles) and [NPC Templates](/hytale-modding-docs/reference/npc-system/npc-templates))
- Familiarity with the condition system (see [NPC Decision Making](/hytale-modding-docs/reference/npc-system/npc-decision-making))
- Understanding of combat evaluators (see [NPC Combat Balancing](/hytale-modding-docs/reference/npc-system/npc-combat-balancing))

---

## How NPC AI Works

Hytale's NPC AI uses a utility-based decision system. Each tick, the AI evaluates available actions by scoring them through conditions. The action with the highest utility score above a minimum threshold is executed. This creates emergent, context-sensitive behavior without scripted sequences.

### Architecture Overview

```
NPC Role
├── Instructions (behavior tree: Idle, Alert, Combat states)
├── Sensors (sight, hearing, absolute detection)
└── Combat Action Evaluator (CAE)
    ├── RunConditions (should the evaluator run this tick?)
    ├── AvailableActions (scored actions: melee, ranged, heal, flee)
    │   └── Conditions (per-action scoring: distance, health, cooldown)
    └── ActionSets (groups of actions active per sub-state)
```

### Key Concepts

| Concept | Description |
|---------|-------------|
| **Condition** | A scoring function that maps a game stat to a 0-1 utility score using a response curve |
| **Response Curve** | Mathematical function that shapes how raw values map to scores: Linear, Logistic, Switch |
| **Action** | A named combat behaviour with conditions, distance ranges, and ability references |
| **Action Set** | A named group of actions and basic attacks active during a combat sub-state |
| **Sub-State** | A combat mode the NPC can switch between (Default, Ranged, Healing, etc.) |

---

## Step 1: Understanding Condition Types

Conditions are the building blocks of AI decisions. Each condition reads a game value and maps it to a 0-1 score using a curve. Multiple conditions on an action are multiplied together to produce the final utility score.

### Condition types reference

| Type | What it reads | Common use |
|------|--------------|------------|
| `OwnStatPercent` | NPC's own stat as % of max | Heal when health is low |
| `TargetStatPercent` | Target's stat as % of max | Focus weak targets |
| `TargetDistance` | Distance to current target in blocks | Choose melee vs ranged |
| `TimeSinceLastUsed` | Seconds since this action was last used | Cooldown pacing |
| `Randomiser` | Random value between min and max | Add unpredictability |

### Curve types

The curve transforms a raw value into a 0-1 score:

| Curve | Shape | Use case |
|-------|-------|----------|
| `"Linear"` | Straight line, 0 to 1 | Score increases proportionally with the value |
| `"ReverseLinear"` | Straight line, 1 to 0 | Score highest when value is lowest (heal when hurt) |
| `"SimpleLogistic"` | S-curve rising | Score jumps sharply in the middle range (prefer when close) |
| `"SimpleDescendingLogistic"` | S-curve falling | Score drops sharply (avoid when close) |
| `Switch` with `SwitchPoint` | Binary 0/1 flip | Hard gate: only score 1 after threshold |

### How scores combine

When an action has multiple conditions, the engine multiplies all scores together. This means:

- Any condition scoring 0 disables the action entirely
- All conditions must score reasonably high for the action to win
- A `Randomiser` with `MinValue: 0.9, MaxValue: 1.0` adds slight unpredictability without dominating the score

**Example**: An action with conditions `[OwnStatPercent(Health, ReverseLinear), TimeSinceLastUsed(Linear, 0-5)]` scores highest when the NPC is hurt AND the action has not been used recently. If health is at 100%, `ReverseLinear` returns 0, making the action impossible regardless of cooldown.

---

## Step 2: Create Decision Making Condition Files

Standalone condition files in `DecisionMaking/Conditions/` can be referenced by multiple CAEs. Create reusable conditions for common patterns.

Create `YourMod/Assets/Server/NPC/DecisionMaking/Conditions/Condition_LowHealth.json`:

```json
{
  "Type": "OwnStatPercent",
  "Stat": "Health",
  "Curve": "ReverseLinear"
}
```

This condition scores highest (near 1.0) when the NPC has very low health, and lowest (near 0.0) at full health. Any action using this condition will be strongly preferred when the NPC is injured.

Create `YourMod/Assets/Server/NPC/DecisionMaking/Conditions/Condition_TargetClose.json`:

```json
{
  "Type": "TargetDistance",
  "Curve": {
    "ResponseCurve": "SimpleDescendingLogistic",
    "XRange": [0, 12]
  }
}
```

This scores high when the target is close (within ~4 blocks) and drops off rapidly as distance approaches 12 blocks. The logistic curve creates a sharp transition rather than a gradual one.

Create `YourMod/Assets/Server/NPC/DecisionMaking/Conditions/Condition_TargetFar.json`:

```json
{
  "Type": "TargetDistance",
  "Curve": {
    "ResponseCurve": "SimpleLogistic",
    "XRange": [0, 15]
  }
}
```

The opposite of `Condition_TargetClose` — scores high when the target is far away, useful for triggering ranged attacks.

---

## Step 3: Create the Combat Action Evaluator

The CAE is the core of the NPC's combat intelligence. It defines all available combat actions and the conditions under which each is preferred.

Create `YourMod/Assets/Server/NPC/Balancing/Intelligent/CAE_Ironclad_Sentinel.json`:

```json
{
  "Type": "CombatActionEvaluator",
  "TargetMemoryDuration": 8,
  "CombatActionEvaluator": {
    "RunConditions": [
      {
        "Type": "TimeSinceLastUsed",
        "Curve": {
          "ResponseCurve": "Linear",
          "XRange": [0, 3]
        }
      },
      {
        "Type": "Randomiser",
        "MinValue": 0.9,
        "MaxValue": 1
      }
    ],
    "MinRunUtility": 0.5,
    "MinActionUtility": 0.01,
    "AvailableActions": {
      "SelectTarget": {
        "Type": "SelectBasicAttackTarget",
        "Description": "Select the best target for basic attacks",
        "Conditions": [
          {
            "Type": "TargetDistance",
            "Curve": {
              "ResponseCurve": "SimpleDescendingLogistic",
              "XRange": [0, 20]
            }
          }
        ]
      },
      "MeleeSwing": {
        "Type": "Ability",
        "Description": "Heavy melee swing when target is close",
        "WeaponSlot": 0,
        "SubState": "Melee",
        "Ability": "Sentinel_MeleeSwing",
        "Target": "Hostile",
        "AttackDistanceRange": [2.5, 2.5],
        "PostExecuteDistanceRange": [2.5, 2.5],
        "WeightCoefficient": 1.2,
        "Conditions": [
          {
            "Type": "TargetDistance",
            "Curve": {
              "ResponseCurve": "SimpleDescendingLogistic",
              "XRange": [0, 5]
            }
          },
          {
            "Type": "TimeSinceLastUsed",
            "Curve": {
              "ResponseCurve": "Linear",
              "XRange": [0, 1.5]
            }
          }
        ]
      },
      "ShieldBash": {
        "Type": "Ability",
        "Description": "Shield bash to stagger close targets",
        "WeaponSlot": 1,
        "SubState": "Melee",
        "Ability": "Sentinel_ShieldBash",
        "Target": "Hostile",
        "AttackDistanceRange": [2, 2],
        "PostExecuteDistanceRange": [3, 3],
        "WeightCoefficient": 1.0,
        "ChargeFor": 0.5,
        "Conditions": [
          {
            "Type": "TargetDistance",
            "Curve": {
              "ResponseCurve": "SimpleDescendingLogistic",
              "XRange": [0, 4]
            }
          },
          {
            "Type": "TimeSinceLastUsed",
            "Curve": {
              "Type": "Switch",
              "SwitchPoint": 5
            }
          }
        ]
      },
      "RangedThrow": {
        "Type": "Ability",
        "Description": "Throw projectile when target is at range",
        "WeaponSlot": 0,
        "SubState": "Ranged",
        "Ability": "Sentinel_SpearThrow",
        "Target": "Hostile",
        "AttackDistanceRange": [12, 12],
        "PostExecuteDistanceRange": [2.5, 2.5],
        "WeightCoefficient": 0.9,
        "Conditions": [
          {
            "Type": "TargetDistance",
            "Curve": {
              "ResponseCurve": "SimpleLogistic",
              "XRange": [0, 15]
            }
          },
          {
            "Type": "TimeSinceLastUsed",
            "Curve": {
              "ResponseCurve": "Linear",
              "XRange": [0, 3]
            }
          }
        ]
      },
      "HealSelf": {
        "Type": "Ability",
        "Description": "Heal when health is low",
        "Ability": "Sentinel_HealSelf",
        "Target": "Self",
        "WeightCoefficient": 1.5,
        "Conditions": [
          {
            "Type": "OwnStatPercent",
            "Stat": "Health",
            "Curve": "ReverseLinear"
          },
          {
            "Type": "TimeSinceLastUsed",
            "Curve": {
              "Type": "Switch",
              "SwitchPoint": 10
            }
          }
        ]
      },
      "CallForHelp": {
        "Type": "Ability",
        "Description": "Call nearby allies when hurt",
        "Ability": "Sentinel_CallForHelp",
        "Target": "Self",
        "WeightCoefficient": 1.3,
        "Conditions": [
          {
            "Type": "OwnStatPercent",
            "Stat": "Health",
            "Curve": "ReverseLinear"
          },
          {
            "Type": "TimeSinceLastUsed",
            "Curve": {
              "Type": "Switch",
              "SwitchPoint": 15
            }
          },
          {
            "Type": "Randomiser",
            "MinValue": 0.6,
            "MaxValue": 1
          }
        ]
      }
    },
    "ActionSets": {
      "Default": {
        "BasicAttacks": {
          "Attacks": ["Sentinel_MeleeSwing"],
          "Randomise": false,
          "MaxRange": 2.5,
          "Timeout": 0.5,
          "CooldownRange": [0.5, 1.0]
        },
        "Actions": [
          "SelectTarget",
          "MeleeSwing",
          "ShieldBash",
          "RangedThrow",
          "HealSelf",
          "CallForHelp"
        ]
      },
      "Melee": {
        "BasicAttacks": {
          "Attacks": ["Sentinel_MeleeSwing", "Sentinel_ShieldBash"],
          "Randomise": true,
          "MaxRange": 2.5,
          "Timeout": 0.5,
          "CooldownRange": [0.3, 0.8]
        },
        "Actions": [
          "SelectTarget",
          "ShieldBash",
          "RangedThrow",
          "HealSelf",
          "CallForHelp"
        ]
      },
      "Ranged": {
        "BasicAttacks": {
          "Attacks": ["Sentinel_SpearThrow"],
          "Randomise": false,
          "MaxRange": 12,
          "Timeout": 1.0,
          "CooldownRange": [1.5, 3.0]
        },
        "Actions": [
          "SelectTarget",
          "MeleeSwing",
          "HealSelf"
        ]
      }
    }
  }
}
```

### Breaking down the CAE design

**RunConditions** control how often the evaluator fires:
- `TimeSinceLastUsed` with a 3-second Linear curve means the evaluator scores higher the longer it has been since it last ran
- `Randomiser` at 0.9-1.0 adds 10% variance so the NPC does not act on perfectly predictable intervals
- `MinRunUtility: 0.5` means both conditions must score above ~0.7 each (0.7 * 0.7 = 0.49, just below threshold) before the evaluator fires

**WeightCoefficient** multiplies the final utility score:
- `HealSelf` at 1.5 makes it strongly preferred when conditions are met
- `CallForHelp` at 1.3 gives it priority over basic attacks
- `RangedThrow` at 0.9 makes it slightly less preferred than melee when both are viable
- `MeleeSwing` at 1.2 gives melee a slight edge over default

**Sub-state switching**: When `MeleeSwing` fires, it activates the `Melee` sub-state, which has faster cooldowns and randomised basic attacks between swing and bash. When `RangedThrow` fires, it switches to `Ranged`, which has only the spear throw as a basic attack with longer cooldowns.

**HealSelf logic breakdown**:
- `OwnStatPercent(Health, ReverseLinear)`: At 50% HP scores 0.5, at 20% HP scores 0.8
- `TimeSinceLastUsed(Switch, 10)`: Hard gate — cannot heal more often than every 10 seconds
- `WeightCoefficient: 1.5`: Multiplied by the condition scores, this outweighs most combat actions when health is below ~40%

---

## Step 4: Create the NPC Role

Wire the CAE into an NPC role that uses the `Template_Intelligent` base, which provides faction-aware combat AI with call-for-help support.

Create `YourMod/Assets/Server/NPC/Roles/MyMod/Ironclad_Sentinel.json`:

```json
{
  "Type": "Variant",
  "Reference": "Template_Intelligent",
  "Modify": {
    "Appearance": "Skeleton_Warrior",
    "DropList": "Drop_Ironclad_Sentinel",
    "MaxHealth": 180,
    "MaxSpeed": 5,
    "ViewRange": 20,
    "ViewSector": 220,
    "HearingRange": 16,
    "AlertedRange": 28,
    "DefaultPlayerAttitude": "Hostile",
    "DefaultNPCAttitude": "Neutral",
    "KnockbackScale": 0.6,
    "FlockArray": ["Ironclad_Sentinel"],
    "IsMemory": true,
    "MemoriesCategory": "Undead",
    "MemoriesNameOverride": "Ironclad Sentinel",
    "NameTranslationKey": {
      "Compute": "NameTranslationKey"
    }
  },
  "Parameters": {
    "NameTranslationKey": {
      "Value": "server.npcRoles.Ironclad_Sentinel.name",
      "Description": "Translation key for NPC name display"
    }
  }
}
```

### Role design notes

| Field | Value | Rationale |
|-------|-------|-----------|
| `MaxHealth: 180` | Higher than vanilla Goblin Scrapper (~80) | Boss-tier durability for a dungeon guardian |
| `ViewRange: 20` | Extended sight range | Detects intruders from further away |
| `ViewSector: 220` | Wide field of view | Harder to sneak behind |
| `AlertedRange: 28` | Very long alert range | Once alerted, tracks players across large rooms |
| `KnockbackScale: 0.6` | Reduced knockback | Heavy armoured NPC resists being pushed around |
| `FlockArray` | Self-referencing | Sentinels coordinate as a group |

The `Template_Intelligent` base provides:
- `ChanceToBeAlertedWhenReceivingCallForHelp: 70` — 70% chance nearby Sentinels join combat when one calls for help
- Full combat AI state machine: Idle, Alert, Combat, Flee
- Faction-aware attitudes for NPC-to-NPC interactions

---

## Step 5: Configure Flee Behaviour

The Sentinel should retreat when critically wounded. Flee behaviour is controlled by fields on the NPC role that the template reads from.

Add flee parameters to your role's `Modify` block:

```json
{
  "Type": "Variant",
  "Reference": "Template_Intelligent",
  "Modify": {
    "Appearance": "Skeleton_Warrior",
    "DropList": "Drop_Ironclad_Sentinel",
    "MaxHealth": 180,
    "MaxSpeed": 5,
    "ViewRange": 20,
    "ViewSector": 220,
    "HearingRange": 16,
    "AlertedRange": 28,
    "DefaultPlayerAttitude": "Hostile",
    "DefaultNPCAttitude": "Neutral",
    "KnockbackScale": 0.6,
    "FlockArray": ["Ironclad_Sentinel"],
    "FleeRange": 20,
    "FleeHealthThreshold": 0.15,
    "FleeSpeed": 7,
    "FleeIfNotThreatened": false,
    "IsMemory": true,
    "MemoriesCategory": "Undead",
    "MemoriesNameOverride": "Ironclad Sentinel",
    "NameTranslationKey": {
      "Compute": "NameTranslationKey"
    }
  },
  "Parameters": {
    "NameTranslationKey": {
      "Value": "server.npcRoles.Ironclad_Sentinel.name",
      "Description": "Translation key for NPC name display"
    }
  }
}
```

### Flee fields explained

| Field | Purpose |
|-------|---------|
| `FleeRange` | Distance the NPC tries to maintain from threats when fleeing |
| `FleeHealthThreshold` | Health percentage below which the NPC starts fleeing (0.15 = 15%) |
| `FleeSpeed` | Movement speed while fleeing (faster than normal `MaxSpeed: 5`) |
| `FleeIfNotThreatened` | If `true`, the NPC flees even from non-threatening targets. `false` means it only flees from entities it considers dangerous |

At 15% health (27 HP out of 180), the Sentinel switches to flee mode, running at speed 7 while trying to maintain 20 blocks of distance. This gives players a window to finish the fight before the Sentinel escapes.

---

## Step 6: Add Translation Keys and Drop Table

Add to `YourMod/Assets/Languages/en-US.lang`:

```
server.npcRoles.Ironclad_Sentinel.name=Ironclad Sentinel
```

Create `YourMod/Assets/Server/Drops/NPCs/Intelligent/Drop_Ironclad_Sentinel.json`:

```json
{
  "Container": {
    "Type": "Multiple",
    "Containers": [
      {
        "Type": "Choice",
        "Weight": 100,
        "Containers": [
          {
            "Type": "Single",
            "Item": {
              "ItemId": "Ingredient_Bone",
              "QuantityMin": 2,
              "QuantityMax": 4
            }
          }
        ]
      },
      {
        "Type": "Choice",
        "Containers": [
          {
            "Type": "Single",
            "Weight": 20,
            "Item": {
              "ItemId": "Ingredient_Hide_Heavy",
              "QuantityMin": 1,
              "QuantityMax": 2
            }
          },
          {
            "Type": "Empty",
            "Weight": 80
          }
        ]
      },
      {
        "Type": "Choice",
        "Containers": [
          {
            "Type": "Single",
            "Weight": 5,
            "Item": {
              "ItemId": "Weapon_Sword_Iron",
              "QuantityMin": 1,
              "QuantityMax": 1
            }
          },
          {
            "Type": "Empty",
            "Weight": 95
          }
        ]
      }
    ]
  }
}
```

---

## Step 7: Test the AI

1. Place your mod folder in the server mods directory.
2. Start the server and spawn an Ironclad Sentinel using the developer NPC spawner.
3. Observe idle behaviour — the Sentinel should stand watch and scan its surroundings.
4. Approach within 20 blocks and confirm the Sentinel becomes alert.
5. Enter combat and test the following behaviours:

| Test | Expected behaviour |
|------|-------------------|
| Stand at melee range (< 3 blocks) | Sentinel uses MeleeSwing and ShieldBash |
| Stand at range (8-12 blocks) | Sentinel switches to RangedThrow |
| Damage Sentinel below 50% HP | HealSelf action activates (if 10s cooldown has passed) |
| Damage Sentinel below 15% HP | Sentinel flees at speed 7 |
| Spawn 2 Sentinels, attack one | Attacked Sentinel calls for help, second has 70% chance to join |
| Wait after Sentinel flees | Sentinel maintains 20 blocks of distance |

### Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| NPC never attacks | `MinActionUtility` too high | Lower `MinActionUtility` to `0.001` |
| NPC always uses same attack | `WeightCoefficient` imbalance | Adjust coefficients so they are closer in value |
| Heal never triggers | Switch point too high or health threshold mismatch | Lower `SwitchPoint` on the heal cooldown condition |
| NPC does not flee | `FleeHealthThreshold` too low | Increase to 0.25 for testing |
| Call for help does not work | Nearby NPCs not in same flock | Ensure `FlockArray` includes the helper NPC's role ID |
| AI feels too slow | `RunConditions` scoring too low | Reduce `XRange` on `TimeSinceLastUsed` to make the evaluator fire more frequently |

---

## Next Steps

- [Custom Combat System](/hytale-modding-docs/tutorials/advanced/custom-combat-system) — add custom damage types to the Sentinel's attacks
- [Custom Dungeons](/hytale-modding-docs/tutorials/advanced/custom-dungeons) — spawn Sentinels inside dungeon instances
- [NPC Decision Making](/hytale-modding-docs/reference/npc-system/npc-decision-making) — full condition type reference
- [NPC Combat Balancing](/hytale-modding-docs/reference/npc-system/npc-combat-balancing) — CAE schema reference
- [Response Curves](/hytale-modding-docs/reference/concepts/response-curves) — mathematical details of curve shapes
