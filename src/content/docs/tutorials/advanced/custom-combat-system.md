---
title: Create a Custom Combat System
description: Build a multi-phase boss fight with shield mechanics, appearance changes, minion spawning, custom attack animations, and world spawns.
---

import { Aside } from '@astrojs/starlight/components';

## What You'll Learn

Build a complete **Boss Slime** encounter with:
- A multi-phase boss that changes appearance as it loses HP
- Shield entity effects with damage resistance
- Custom attack animations using `ItemPlayerAnimations`
- Combat movement with `MaintainDistance` strafing
- Minion spawning during phase transitions
- World spawn configuration for natural generation
- Loot drops with a trophy item

<Aside type="tip">
The complete mod is available on GitHub: [hytale-mod-custom-combat-system](https://github.com/nevesb/hytale-mod-custom-combat-system)
</Aside>

## Prerequisites

- A working mod with a custom NPC (see [Create an NPC](/hytale-modding-docs/tutorials/beginner/create-an-npc))
- Understanding of NPC spawning (see [Custom NPC Spawning](/hytale-modding-docs/tutorials/intermediate/custom-npc-spawning))
- Familiarity with interaction chains (see [NPC AI Behavior Trees](/hytale-modding-docs/tutorials/advanced/npc-ai-behavior-trees))

---

## System Architecture

The boss system connects several file types:

```
ModelAsset (BossSlime_Giant)     ─── defines hitbox, state animations, appearance
    │
ItemPlayerAnimations             ─── maps attack animation IDs to .blockyanim files
    │
Interaction (Boss_Slime_Attack)  ─── triggers the attack animation + damage chain
    │
NPC Role (Boss_Slime_Giant)      ─── defines phases, movement, combat states
    │
Entity Effect (Shield_Crystal)   ─── shield with damage resistance + particles
    │
World Spawn                      ─── natural generation in Zone 1 forests
```

---

## Step 1: Create the Boss Model Asset

The boss needs a model definition that maps state animations (Idle, Walk, Death, etc.) but **not** attack animations. Attack animations are handled separately via `ItemPlayerAnimations`.

Create `Server/Models/Beast/BossSlime_Giant.json`:

```json
{
  "Model": "NPC/Beast/BossSlime/Model/Model_Giant.blockymodel",
  "Texture": "NPC/Beast/BossSlime/Model/Texture_Giant.png",
  "EyeHeight": 1.5,
  "CrouchOffset": -0.5,
  "HitBox": {
    "Max": { "X": 1.5, "Y": 1.5, "Z": 1.5 },
    "Min": { "X": -3.0, "Y": 0, "Z": -3.0 }
  },
  "AnimationSets": {
    "Walk": {
      "Animations": [
        { "Animation": "NPC/Beast/BossSlime/Animations/Default/Walk.blockyanim" }
      ]
    },
    "Idle": {
      "Animations": [
        { "Animation": "NPC/Beast/BossSlime/Animations/Default/Idle.blockyanim" }
      ]
    },
    "Death": {
      "Animations": [
        { "Animation": "NPC/Beast/BossSlime/Animations/Default/Death.blockyanim", "Loop": false }
      ]
    },
    "Run": {
      "Animations": [
        { "Animation": "NPC/Beast/BossSlime/Animations/Default/Run.blockyanim" }
      ]
    },
    "Walk_Backward": {
      "Animations": [
        { "Animation": "NPC/Beast/BossSlime/Animations/Default/Walk_Backward.blockyanim" }
      ]
    }
  }
}
```

<Aside type="caution">
Do **not** add attack animations to `AnimationSets`. Attack animations for NPCs must be defined in a separate `ItemPlayerAnimations` file (Step 2). Mixing them causes the animation to not play.
</Aside>

You also need `BossSlime_Medium.json` and `BossSlime_Small.json` model assets for phase transitions (same animations, different models/textures). The base `BossSlime.json` serves as the default appearance.

---

## Step 2: Create the Attack Animation Mapping

Vanilla beasts (Bear, Cactee, etc.) use `ItemPlayerAnimations` files to map combat animation IDs to `.blockyanim` files. Your boss needs the same.

Create `Server/Item/Animations/NPC/Beast/BossSlime/BossSlime_Default.json`:

```json
{
  "Animations": {
    "Attack": {
      "ThirdPerson": "NPC/Beast/BossSlime/Animations/Default/Attack.blockyanim",
      "Looping": false,
      "Speed": 1
    }
  },
  "Camera": {
    "Pitch": {
      "AngleRange": { "Max": 15, "Min": -15 },
      "TargetNodes": ["Head"]
    },
    "Yaw": {
      "AngleRange": { "Max": 15, "Min": -15 },
      "TargetNodes": ["Head"]
    }
  },
  "WiggleWeights": {
    "Pitch": 2, "PitchDeceleration": 0.1,
    "Roll": 0.1, "RollDeceleration": 0.1,
    "X": 3, "XDeceleration": 0.1,
    "Y": 0.1, "YDeceleration": 0.1,
    "Z": 0.1, "ZDeceleration": 0.1
  }
}
```

### How it works

| Section | Purpose |
|---------|---------|
| `Animations.Attack` | Maps the ID `"Attack"` to the `.blockyanim` file |
| `Camera` | Head tracking limits during combat |
| `WiggleWeights` | Visual wobble when the NPC moves/attacks |

The `"Attack"` key is what you reference in the interaction's `ItemAnimationId`. The filename `BossSlime_Default` becomes the `ItemPlayerAnimationsId`.

---

## Step 3: Create the Attack Interaction

The boss uses the vanilla `Root_NPC_Attack_Melee` chain, but overrides the start animation to use the slime's custom attack.

Create `Server/Item/Interactions/Boss_Slime_Attack_Start.json`:

```json
{
  "Type": "Simple",
  "Effects": {
    "ItemPlayerAnimationsId": "BossSlime_Default",
    "ItemAnimationId": "Attack",
    "ClearAnimationOnFinish": false,
    "ClearSoundEventOnFinish": false
  },
  "RunTime": 0.1,
  "Next": {
    "Type": "Replace",
    "DefaultValue": {
      "Interactions": ["NPC_Attack_Selector_Left"]
    },
    "Var": "Melee_Selector"
  }
}
```

This replaces the vanilla `NPC_Attack_Melee_Simple` (which uses humanoid `SwingLeft` animation) with an interaction that plays the slime's `Attack` animation instead.

Create the damage interaction at `Server/Item/Interactions/Boss_Slime_Slam_Damage.json`:

```json
{
  "Parent": "DamageEntityParent",
  "DamageCalculator": {
    "BaseDamage": { "Physical": 15 }
  },
  "DamageEffects": {
    "Knockback": { "Force": 3, "VelocityY": 4 },
    "WorldSoundEventId": "SFX_Unarmed_Impact",
    "LocalSoundEventId": "SFX_Unarmed_Impact"
  }
}
```

---

## Step 4: Create the Shield Entity Effect

The shield provides temporary damage resistance and a visual particle effect.

Create `Server/Entity/Effects/Shield_Crystal.json`:

```json
{
  "Duration": 1,
  "DamageResistance": {
    "Physical": [{ "Amount": 1.0, "CalculationType": "Multiplicative" }],
    "Slashing": [{ "Amount": 1.0, "CalculationType": "Multiplicative" }],
    "Bludgeoning": [{ "Amount": 1.0, "CalculationType": "Multiplicative" }],
    "Projectile": [{ "Amount": 1.0, "CalculationType": "Multiplicative" }],
    "Fire": [{ "Amount": 1.0, "CalculationType": "Multiplicative" }],
    "Ice": [{ "Amount": 1.0, "CalculationType": "Multiplicative" }],
    "Poison": [{ "Amount": 1.0, "CalculationType": "Multiplicative" }],
    "Environment": [{ "Amount": 1.0, "CalculationType": "Multiplicative" }]
  },
  "ApplicationEffects": {
    "Particles": [{ "SystemId": "Example_Shield" }]
  },
  "Invulnerable": false
}
```

### Design notes

| Field | Value | Purpose |
|-------|-------|---------|
| `Duration: 1` | 1 second | Short duration, but continuously refreshed by the boss's instruction blocks |
| `Amount: 1.0` + `Multiplicative` | 100% resistance | Full damage immunity while shield is active |
| `SystemId: "Example_Shield"` | Built-in particle | Displays a bubble shield effect around the boss |
| `Invulnerable: false` | Not invulnerable | Allows the shield to be broken by dealing enough damage |

---

## Step 5: Create the Boss Role

This is the core file. The boss uses `Type: "Generic"` with a state machine controlling phases, combat movement, and attacks.

Create `Server/NPC/Roles/Boss_Slime_Giant.json`:

```json
{
  "Type": "Generic",
  "Appearance": "BossSlime_Giant",
  "MaxHealth": 450,
  "KnockbackScale": 0.5,
  "DisableDamageGroups": ["Self"],
  "DefaultNPCAttitude": "Ignore",
  "DefaultPlayerAttitude": "Neutral",
  "DropList": "Drop_BossSlime_Crown",
  "IsMemory": true,
  "MemoriesCategory": "Boss",
  "StartState": "Idle",
  "MotionControllerList": [
    {
      "Type": "Walk",
      "MaxWalkSpeed": 6,
      "Gravity": 10,
      "RunThreshold": 0.3,
      "MaxFallSpeed": 15,
      "MaxRotationSpeed": 360,
      "Acceleration": 8
    }
  ],
  "CombatConfig": {
    "EntityEffect": "Shield_Crystal"
  },
  "InteractionVars": {
    "Melee_Start": {
      "Interactions": ["Boss_Slime_Attack_Start"]
    },
    "Melee_Damage": {
      "Interactions": [{ "Parent": "Boss_Slime_Slam_Damage" }]
    }
  }
}
```

### Key fields explained

| Field | Purpose |
|-------|---------|
| `Type: "Generic"` | Full manual control via instruction blocks (no template AI) |
| `InteractionVars.Melee_Start` | Overrides `Root_NPC_Attack_Melee` to use the slime's attack animation |
| `InteractionVars.Melee_Damage` | Overrides the damage interaction with custom values |
| `CombatConfig.EntityEffect` | Applies `Shield_Crystal` effect during combat |
| `DefaultPlayerAttitude: "Neutral"` | Boss ignores players until attacked |
| `StartState: "Idle"` | Boss starts in the Idle state |

---

## Step 6: Add Phase Transitions

Phase transitions use `Once` sensors that fire when HP drops below thresholds. Add these as `Instructions` with `Continue: true` so they run alongside other blocks.

```json
{
  "$Comment": "Phase 1 end: HP <= 77.8% - spawn 1 slime",
  "Continue": true,
  "Instructions": [{
    "Sensor": {
      "Type": "Self", "Once": true,
      "Filters": [{
        "Type": "Stat", "Stat": "Health", "StatTarget": "Value",
        "RelativeTo": "Health", "RelativeToTarget": "Max",
        "ValueRange": [0, 0.778]
      }]
    },
    "Actions": [{
      "Type": "Spawn", "FanOut": true, "SpawnAngle": 360,
      "DistanceRange": [3, 5], "CountRange": [1, 1],
      "DelayRange": [0, 0], "Kind": "Slime"
    }]
  }]
}
```

The full boss has four phase triggers:

| Phase | HP Threshold | Actions |
|-------|-------------|---------|
| Phase 1 end | 77.8% (350 HP) | Spawn 1 Slime |
| Phase 2 start | 55.6% (250 HP) | Change to Medium appearance, re-apply shield, spawn 2 Slimes |
| Phase 2 end | 38.9% (175 HP) | Spawn 1 Slime |
| Phase 3 start | 22.2% (100 HP) | Change to Small appearance, spawn 2 Slimes |

The appearance change uses `"Type": "Appearance"` actions:

```json
{ "Type": "Appearance", "Appearance": "BossSlime_Medium" }
```

Shield refresh blocks use continuous sensors (without `Once`) to re-apply the shield every second during protected phases:

```json
{
  "Continue": true,
  "Instructions": [{
    "Sensor": {
      "Type": "Self",
      "Filters": [{
        "Type": "Stat", "Stat": "Health", "StatTarget": "Value",
        "RelativeTo": "Health", "RelativeToTarget": "Max",
        "ValueRange": [0.778, 1.0]
      }]
    },
    "Actions": [{
      "Type": "ApplyEntityEffect", "UseTarget": false,
      "EntityEffect": "Shield_Crystal"
    }]
  }]
}
```

---

## Step 7: Add Combat Movement

The boss uses two movement modes controlled by state:

**Idle state** — Wanders randomly, watches nearby players:

```json
{
  "Sensor": { "Type": "State", "State": "Idle" },
  "Instructions": [
    {
      "Sensor": { "Type": "Player", "Range": 20 },
      "HeadMotion": { "Type": "Watch" },
      "BodyMotion": { "Type": "Nothing" }
    },
    {
      "Sensor": { "Type": "Any" },
      "BodyMotion": {
        "Type": "Wander",
        "MaxHeadingChange": 45,
        "RelativeSpeed": 0.3
      }
    }
  ]
}
```

**Combat state** — Maintains distance and strafes:

```json
{
  "Sensor": { "Type": "State", "State": "Combat" },
  "Instructions": [{
    "Sensor": { "Type": "Player", "Range": 30 },
    "BodyMotion": {
      "Type": "MaintainDistance",
      "DesiredDistanceRange": [1.5, 3.5],
      "MoveThreshold": 0.5,
      "RelativeForwardsSpeed": 0.6,
      "RelativeBackwardsSpeed": 0.5,
      "StrafingDurationRange": [1, 1],
      "StrafingFrequencyRange": [2, 2]
    }
  }]
}
```

### MaintainDistance parameters

| Field | Value | Purpose |
|-------|-------|---------|
| `DesiredDistanceRange: [1.5, 3.5]` | Stay 1.5-3.5 blocks from player | Close enough for melee, matching vanilla Template_Predator |
| `StrafingDurationRange: [1, 1]` | Strafe for 1 second | Creates the "combat dance" movement |
| `StrafingFrequencyRange: [2, 2]` | Strafe every 2 seconds | Regular repositioning during combat |
| `RelativeForwardsSpeed: 0.6` | 60% speed approaching | Approach cautiously |

<Aside type="caution">
Setting `DesiredDistanceRange` too high (e.g., `[3, 5]`) will keep the boss out of melee range. Vanilla melee predators use `[1.5, 3.5]` calculated from `AttackDistance - 1`.
</Aside>

---

## Step 8: Add Combat Actions

The combat block handles state transitions and attacks:

```json
{
  "Instructions": [
    {
      "Sensor": { "Type": "State", "State": "Idle" },
      "Instructions": [
        {
          "Sensor": { "Type": "Damage" },
          "Actions": [{ "Type": "State", "State": "Combat" }]
        },
        {
          "Sensor": { "Type": "Any" },
          "Actions": [{ "Type": "Nothing" }]
        }
      ]
    },
    {
      "Sensor": { "Type": "State", "State": "Combat" },
      "Instructions": [
        {
          "Sensor": { "Type": "Player", "Range": 14 },
          "ActionsBlocking": true,
          "Actions": [
            {
              "Type": "Attack",
              "Attack": "Root_NPC_Attack_Melee",
              "AttackPauseRange": [1.0, 2.0]
            },
            { "Type": "Timeout", "Delay": [0.2, 0.2] }
          ],
          "HeadMotion": { "Type": "Aim", "RelativeTurnSpeed": 1.5 }
        },
        {
          "Sensor": { "Type": "Not", "Sensor": { "Type": "Player", "Range": 40 } },
          "Actions": [{ "Type": "State", "State": "Idle" }]
        }
      ]
    }
  ]
}
```

### How InteractionVars override the attack chain

The vanilla `Root_NPC_Attack_Melee` chain works through Replace Vars:

```
Root_NPC_Attack_Melee
  └─ Replace Var "Melee_Start" (default: NPC_Attack_Melee_Simple → SwingLeft)
       └─ Replace Var "Melee_Selector" (default: NPC_Attack_Selector_Left)
            └─ Replace Var "Melee_Damage" (default: generic damage)
```

By defining `InteractionVars` on the boss role, you override specific links:
- `Melee_Start` → `Boss_Slime_Attack_Start` (plays slime animation instead of humanoid swing)
- `Melee_Damage` → `Boss_Slime_Slam_Damage` (custom damage values and knockback)

---

## Step 9: Create Loot Drops

Create `Server/Drops/Drop_BossSlime_Crown.json`:

```json
{
  "Container": {
    "Type": "Choice",
    "Containers": [
      {
        "Type": "Single",
        "Item": { "ItemId": "Trophy_Slime_Crown", "QuantityMin": 1, "QuantityMax": 1 },
        "Weight": 100
      },
      {
        "Type": "Single",
        "Item": { "ItemId": "Ore_Crystal_Glow", "QuantityMin": 1, "QuantityMax": 3 },
        "Weight": 80
      }
    ]
  }
}
```

Create the trophy item at `Server/Item/Items/Trophy_Slime_Crown.json`:

```json
{
  "TranslationProperties": {
    "Name": "Slime Crown",
    "Description": "A trophy from the defeated Slime King"
  },
  "Model": "NPC/Beast/BossSlime/Model/Model_Crown.blockymodel",
  "Texture": "NPC/Beast/BossSlime/Model/Texture.png",
  "MaxStack": 1,
  "Scale": 0.5,
  "Icon": "Icons/ItemsGenerated/Trophy_Slime_Crown.png"
}
```

---

## Step 10: Configure World Spawns

Add the boss and regular slimes to Zone 1 forests.

Create `Server/NPC/Spawn/World/Zone1/Spawns_Zone1_Forests_Slime.json`:

```json
{
  "Environments": [
    "Env_Zone1_Forests",
    "Env_Zone1_Autumn",
    "Env_Zone1_Azure"
  ],
  "NPCs": [
    {
      "Weight": 8,
      "SpawnBlockSet": "Soil",
      "Id": "Slime"
    },
    {
      "Weight": 1,
      "SpawnBlockSet": "Soil",
      "Id": "Boss_Slime_Giant"
    }
  ],
  "DayTimeRange": [6, 18]
}
```

### Spawn design

| Field | Purpose |
|-------|---------|
| `Environments` | All three Zone 1 forest variants |
| `Weight: 8` vs `Weight: 1` | Regular slimes are 8x more common than the boss |
| `SpawnBlockSet: "Soil"` | Spawns on grass/dirt blocks |
| `DayTimeRange: [6, 18]` | Daytime only (6 AM to 6 PM) |

---

## Step 11: Test the Boss

1. Enable the mod and start a server in Zone 1.
2. Explore Azure Forest to find naturally spawned slimes.
3. Find or spawn the Boss Slime Giant with the developer console.

| Test | Expected Result |
|------|----------------|
| Boss wanders in Idle | Moves slowly, changes direction randomly |
| Player approaches within 20 blocks | Boss watches player but doesn't attack |
| Player hits boss | Boss enters Combat state, starts strafing |
| Boss attacks | Plays slime attack animation, deals 15 physical damage with knockback |
| HP drops below 77.8% | Spawns 1 Slime nearby |
| HP drops below 55.6% | Changes to Medium appearance, shield reactivates, spawns 2 Slimes |
| HP drops below 38.9% | Spawns 1 Slime |
| HP drops below 22.2% | Changes to Small appearance, spawns 2 Slimes |
| Boss dies | Drops Slime Crown trophy or Crystal Glow ore |

### Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| No attack animation | `AnimationSets` contains `Attack` | Remove `Attack` from model's `AnimationSets`, define it only in `ItemPlayerAnimations` |
| Boss stays too far to hit | `DesiredDistanceRange` too high | Use `[1.5, 3.5]` for melee range |
| Boss doesn't move in idle | `BodyMotion` set to `Nothing` | Add `"Type": "Wander"` with `RelativeSpeed: 0.3` |
| Server fails to load | Invalid `ItemPlayerAnimationsId` | Ensure the animation file exists at `Server/Item/Animations/` and includes `Camera` + `WiggleWeights` sections |
| Boss attacks but no damage | Missing `InteractionVars.Melee_Damage` | Add damage override referencing `Boss_Slime_Slam_Damage` |

---

## Complete File Structure

```
CreateACustomNPC/
  Common/
    NPC/Beast/BossSlime/
      Animations/Default/
        Attack.blockyanim, Idle.blockyanim, Walk.blockyanim,
        Death.blockyanim, Run.blockyanim, Walk_Backward.blockyanim, ...
      Model/
        Model_Giant.blockymodel, Model_Medium.blockymodel,
        Model.blockymodel, Model_Crown.blockymodel,
        Texture_Giant.png, Texture_Medium.png, Texture.png
    Icons/
      ModelsGenerated/  (BossSlime_Giant.png, etc.)
      ItemsGenerated/   (Trophy_Slime_Crown.png)
  Server/
    Models/Beast/
      BossSlime_Giant.json, BossSlime_Medium.json,
      BossSlime_Small.json, BossSlime.json
    Item/
      Animations/NPC/Beast/BossSlime/BossSlime_Default.json
      Interactions/
        Boss_Slime_Attack_Start.json, Boss_Slime_Slam_Damage.json
      Items/Trophy_Slime_Crown.json
    Entity/Effects/Shield_Crystal.json
    Drops/Drop_BossSlime_Crown.json
    NPC/
      Roles/Boss_Slime_Giant.json
      Spawn/World/Zone1/Spawns_Zone1_Forests_Slime.json
  manifest.json
```

---

## Next Steps

- [Create an NPC](/hytale-modding-docs/tutorials/beginner/create-an-npc) -- create the base Slime NPC that the boss spawns
- [Custom NPC Spawning](/hytale-modding-docs/tutorials/intermediate/custom-npc-spawning) -- learn more about world spawn configuration
- [NPC AI Behavior Trees](/hytale-modding-docs/tutorials/advanced/npc-ai-behavior-trees) -- advanced AI patterns for NPCs
- [Entity Effects](/hytale-modding-docs/reference/combat-and-projectiles/entity-effects) -- full entity effects reference
- [NPC Roles](/hytale-modding-docs/reference/npc-system/npc-roles) -- complete NPC role schema
