---
title: Create a Custom Combat System
description: Creating a custom combat system with new damage types, entity effects, projectile interactions, weapon stats, and NPC combat balancing.
---

## Goal

Build a complete custom combat system around a new **Lightning** damage type. You will create the damage type definition, a lightning staff weapon with projectile configs, entity effects that apply on hit, and an NPC that uses lightning attacks with a tuned Combat Action Evaluator. This tutorial demonstrates how Hytale's combat components connect: damage types, projectiles, interactions, items, and NPC AI.

## Prerequisites

- A mod folder with a valid `manifest.json` (see [Setup Your Dev Environment](/hytale-modding-docs/tutorials/beginner/setup-dev-environment))
- Understanding of damage types (see [Damage Types](/hytale-modding-docs/reference/combat-and-projectiles/damage-types))
- Understanding of projectiles (see [Projectiles](/hytale-modding-docs/reference/combat-and-projectiles/projectiles) and [Projectile Configs](/hytale-modding-docs/reference/combat-and-projectiles/projectile-configs))
- Familiarity with item definitions (see [Item Definitions](/hytale-modding-docs/reference/item-system/item-definitions))
- Understanding of NPC combat AI (see [NPC Combat Balancing](/hytale-modding-docs/reference/npc-system/npc-combat-balancing))

---

## System Architecture

The combat system involves five interconnected file types:

```
Damage Type  ─── defines damage properties (durability loss, stamina loss, color)
    │
Projectile   ─── defines physics and base damage values
    │
Projectile Config ─── defines launch parameters and interaction chains
    │
Item Definition ─── defines the weapon that launches the projectile
    │
NPC CAE      ─── defines AI that uses the weapon abilities
```

Each component references the others by ID. Building them in order ensures each layer has its dependencies in place.

---

## Step 1: Create a Custom Damage Type

Damage types define how damage interacts with the target: whether it causes durability loss, stamina drain, bypasses resistances, and what color floating damage numbers display.

Create `YourMod/Assets/Server/Entity/Damage/Lightning.json`:

```json
{
  "Parent": "Elemental",
  "Inherits": "Elemental",
  "DurabilityLoss": false,
  "StaminaLoss": true,
  "BypassResistances": false,
  "DamageTextColor": "#7DF9FF"
}
```

### Design decisions

| Field | Value | Rationale |
|-------|-------|-----------|
| `Parent: "Elemental"` | Inherits from Elemental root | Lightning is an elemental sub-type, like Fire and Ice |
| `DurabilityLoss: false` | Does not damage equipment | Elemental damage traditionally does not wear gear |
| `StaminaLoss: true` | Drains stamina on hit | Lightning shocks the target, depleting stamina |
| `BypassResistances: false` | Subject to resistance checks | Allows armour and buffs to reduce lightning damage |
| `DamageTextColor: "#7DF9FF"` | Electric blue | Distinct from Fire (default) and Poison (#00FF00) |

The damage type hierarchy now looks like:

```
Elemental
├── Fire
├── Ice
├── Poison
└── Lightning  (your new type)
```

---

## Step 2: Create the Lightning Projectile

Define the projectile entity that flies through the world when the weapon fires.

Create `YourMod/Assets/Server/Projectiles/Spells/LightningBolt.json`:

```json
{
  "Appearance": "LightningBolt",
  "Radius": 0.15,
  "Height": 0.3,
  "MuzzleVelocity": 55,
  "TerminalVelocity": 120,
  "Gravity": 2,
  "Bounciness": 0,
  "TimeToLive": 5,
  "Damage": 45,
  "DeadTime": 0,
  "DeathEffectsOnHit": true,
  "HitSoundEventId": "SFX_Lightning_Hit",
  "MissSoundEventId": "SFX_Lightning_Miss",
  "DeathSoundEventId": "SFX_Lightning_Death",
  "HitParticles": {
    "SystemId": "Impact_Lightning"
  },
  "MissParticles": {
    "SystemId": "Lightning_Sparks"
  },
  "DeathParticles": {
    "SystemId": "Lightning_Dissipate"
  },
  "ExplosionConfig": {
    "DamageEntities": true,
    "DamageBlocks": false,
    "EntityDamageRadius": 3,
    "EntityDamageFalloff": 0.5
  }
}
```

### Projectile design notes

| Field | Value | Comparison |
|-------|-------|------------|
| `MuzzleVelocity: 55` | Faster than Fireball (40) | Lightning should feel faster than fire |
| `Gravity: 2` | Low gravity | Near-straight trajectory, unlike arrows (gravity 10-15) |
| `Damage: 45` | Between Ice Ball (20) and Fireball (60) | Balanced for a midrange elemental |
| `TimeToLive: 5` | 5-second lifetime | Disappears if it misses everything |
| `EntityDamageRadius: 3` | Small AoE | Chain lightning effect on nearby entities, smaller than Fireball (5) |
| `EntityDamageFalloff: 0.5` | 50% damage at edge | Entities at the edge of the AoE take half damage |

Compare to the vanilla Fireball which has `MuzzleVelocity: 40`, `Gravity: 4`, `Damage: 60`, and `EntityDamageRadius: 5`. Lightning trades raw damage for speed and precision.

---

## Step 3: Create the Projectile Config

The projectile config bridges the weapon and the projectile, defining launch parameters and interaction chains for hit/miss events.

Create `YourMod/Assets/Server/ProjectileConfigs/Weapons/Staff/Lightning/Projectile_Config_LightningBolt.json`:

```json
{
  "Model": "LightningBolt",
  "LaunchForce": 35,
  "Physics": {
    "Type": "Standard",
    "Gravity": 2,
    "TerminalVelocityAir": 55,
    "TerminalVelocityWater": 10,
    "RotationMode": "VelocityDamped",
    "Bounciness": 0.0,
    "SticksVertically": false
  },
  "LaunchWorldSoundEventId": "SFX_Staff_Lightning_Shoot",
  "SpawnOffset": {
    "X": 0.1,
    "Y": -0.2,
    "Z": 0.5
  },
  "Interactions": {
    "ProjectileHit": {
      "Interactions": [
        {
          "Parent": "DamageEntityParent",
          "DamageCalculator": {
            "Class": "Charged",
            "BaseDamage": {
              "Lightning": 45
            }
          },
          "DamageEffects": {
            "Knockback": {
              "Type": "Force",
              "Force": 15,
              "VelocityType": "Set"
            },
            "WorldParticles": [
              { "SystemId": "Impact_Lightning" },
              { "SystemId": "Lightning_Sparks" }
            ],
            "WorldSoundEventId": "SFX_Lightning_Hit"
          }
        },
        {
          "Type": "ApplyEffect",
          "EffectId": "Effect_Lightning_Stun",
          "Duration": 1.5
        },
        {
          "Type": "RemoveEntity",
          "Entity": "User"
        }
      ]
    },
    "ProjectileMiss": {
      "Interactions": [
        {
          "Type": "Simple",
          "Effects": {
            "WorldSoundEventId": "SFX_Lightning_Miss",
            "WorldParticles": [
              { "SystemId": "Lightning_Sparks" }
            ]
          }
        },
        {
          "Type": "RemoveEntity",
          "Entity": "User"
        }
      ]
    },
    "ProjectileSpawn": {
      "Interactions": [
        {
          "Type": "Simple",
          "Effects": {
            "WorldParticles": [
              { "SystemId": "Lightning_Charge" }
            ]
          }
        }
      ]
    }
  }
}
```

### Interaction chain breakdown

The `ProjectileHit` chain runs three interactions in sequence:

1. **DamageEntityParent** — calculates and applies damage using the `Lightning` damage type at 45 base damage, with knockback force 15 and particle/sound effects
2. **ApplyEffect** — applies a stun effect (`Effect_Lightning_Stun`) for 1.5 seconds, preventing the target from acting
3. **RemoveEntity** — destroys the projectile after hitting

The `BaseDamage` field uses a map of damage type to value: `{ "Lightning": 45 }`. This references your custom damage type by its filename ID. Compare to the vanilla Ice Ball config which uses `{ "Ice": 20 }`.

---

## Step 4: Create the Lightning Staff Weapon

Define the weapon item that launches lightning bolts.

Create `YourMod/Assets/Server/Item/Items/Weapon/Staff/Weapon_Staff_Lightning.json`:

```json
{
  "Parent": "Template_Weapon",
  "TranslationProperties": {
    "Name": "server.items.Weapon_Staff_Lightning.name",
    "Description": "server.items.Weapon_Staff_Lightning.description"
  },
  "Quality": "Rare",
  "Icon": "Icons/ItemsGenerated/Weapon_Staff_Lightning.png",
  "Categories": ["Items.Weapons.Staves"],
  "ItemLevel": 15,
  "MaxStack": 1,
  "MaxDurability": 250,
  "DurabilityLossOnHit": 2,
  "DropOnDeath": true,
  "PlayerAnimationsId": "Staff",
  "Model": "Items/Weapons/Staff/Lightning.blockymodel",
  "Texture": "Items/Weapons/Staff/Lightning_Texture.png",
  "Weapon": {},
  "Tags": {
    "Type": ["Weapon"],
    "Family": ["Staff"],
    "Element": ["Lightning"]
  },
  "Interactions": {
    "Primary": "Root_Primary_Staff_Lightning"
  },
  "InteractionVars": {
    "ProjectileConfig": {
      "Interactions": [
        {
          "Type": "SpawnProjectile",
          "ProjectileConfigId": "Projectile_Config_LightningBolt"
        }
      ]
    }
  },
  "Recipe": {
    "Input": [
      { "ItemId": "Ingredient_Crystal", "Quantity": 5 },
      { "ItemId": "Ingredient_Wood_Stick", "Quantity": 2 },
      { "ResourceTypeId": "Metal_Ingot", "Quantity": 3 }
    ],
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Id": "MagicBench",
        "Categories": ["Staves"]
      }
    ],
    "TimeSeconds": 10
  }
}
```

### Key weapon fields

| Field | Purpose |
|-------|---------|
| `Weapon: {}` | Empty object that activates weapon behaviour on the item |
| `PlayerAnimationsId: "Staff"` | Uses the staff animation set for the player character |
| `MaxDurability: 250` | Staff has 250 uses before breaking |
| `DurabilityLossOnHit: 2` | Each shot costs 2 durability (125 total shots) |
| `ProjectileConfigId` | References the projectile config that defines launch behaviour |
| `Tags.Element: ["Lightning"]` | Tag used for filtering and resistance lookups |

---

## Step 5: Create Entity Effects

Entity effects are status conditions applied to targets. Create a stun effect that the lightning bolt applies on hit.

Create `YourMod/Assets/Server/Entity/Effects/Effect_Lightning_Stun.json`:

```json
{
  "Id": "Effect_Lightning_Stun",
  "Duration": 1.5,
  "Stackable": false,
  "MaxStacks": 1,
  "StatModifiers": {
    "MaxSpeed": {
      "Type": "Multiply",
      "Value": 0
    },
    "AttackSpeed": {
      "Type": "Multiply",
      "Value": 0
    }
  },
  "Particles": {
    "SystemId": "Lightning_Stun_Loop",
    "AttachToEntity": true
  },
  "Icon": "Icons/Effects/Lightning_Stun.png",
  "TranslationKey": "server.effects.Lightning_Stun.name"
}
```

### Effect design

| Field | Purpose |
|-------|---------|
| `Duration: 1.5` | Effect lasts 1.5 seconds |
| `Stackable: false` | Hitting a stunned target does not extend the stun |
| `StatModifiers.MaxSpeed` | Multiply by 0 = target cannot move |
| `StatModifiers.AttackSpeed` | Multiply by 0 = target cannot attack |
| `Particles` | Visual indicator attached to the stunned entity |

Create a second effect for a damage-over-time lightning debuff:

Create `YourMod/Assets/Server/Entity/Effects/Effect_Lightning_Shock.json`:

```json
{
  "Id": "Effect_Lightning_Shock",
  "Duration": 5,
  "Stackable": true,
  "MaxStacks": 3,
  "TickInterval": 1.0,
  "TickDamage": {
    "DamageType": "Lightning",
    "Amount": 8
  },
  "StatModifiers": {
    "MaxSpeed": {
      "Type": "Multiply",
      "Value": 0.7
    }
  },
  "Particles": {
    "SystemId": "Lightning_Shock_Loop",
    "AttachToEntity": true
  },
  "Icon": "Icons/Effects/Lightning_Shock.png",
  "TranslationKey": "server.effects.Lightning_Shock.name"
}
```

This stacks up to 3 times, dealing 8 Lightning damage per second per stack (max 24/second) while slowing the target to 70% speed. Each stack has its own 5-second duration.

---

## Step 6: Create an NPC That Uses Lightning

Build a **Storm Mage** NPC that uses lightning attacks in combat, demonstrating how NPC AI integrates with the custom combat system.

Create `YourMod/Assets/Server/NPC/Roles/MyMod/Storm_Mage.json`:

```json
{
  "Type": "Variant",
  "Reference": "Template_Intelligent",
  "Modify": {
    "Appearance": "Mage_Storm",
    "DropList": "Drop_Storm_Mage",
    "MaxHealth": 95,
    "MaxSpeed": 5,
    "ViewRange": 22,
    "ViewSector": 180,
    "HearingRange": 14,
    "AlertedRange": 30,
    "DefaultPlayerAttitude": "Hostile",
    "FleeRange": 18,
    "FleeHealthThreshold": 0.2,
    "FleeSpeed": 7,
    "IsMemory": true,
    "MemoriesCategory": "Other",
    "MemoriesNameOverride": "Storm Mage",
    "NameTranslationKey": {
      "Compute": "NameTranslationKey"
    }
  },
  "Parameters": {
    "NameTranslationKey": {
      "Value": "server.npcRoles.Storm_Mage.name",
      "Description": "Translation key for NPC name display"
    }
  }
}
```

Create the Storm Mage's CAE at `YourMod/Assets/Server/NPC/Balancing/Intelligent/CAE_Storm_Mage.json`:

```json
{
  "Type": "CombatActionEvaluator",
  "TargetMemoryDuration": 6,
  "CombatActionEvaluator": {
    "RunConditions": [
      {
        "Type": "TimeSinceLastUsed",
        "Curve": { "ResponseCurve": "Linear", "XRange": [0, 4] }
      },
      { "Type": "Randomiser", "MinValue": 0.9, "MaxValue": 1 }
    ],
    "MinRunUtility": 0.5,
    "MinActionUtility": 0.01,
    "AvailableActions": {
      "SelectTarget": {
        "Type": "SelectBasicAttackTarget",
        "Description": "Select target for ranged lightning attacks",
        "Conditions": [
          {
            "Type": "TargetDistance",
            "Curve": { "ResponseCurve": "SimpleDescendingLogistic", "XRange": [0, 25] }
          }
        ]
      },
      "LightningBolt": {
        "Type": "Ability",
        "Description": "Fire a lightning bolt at the target",
        "Ability": "Storm_Mage_LightningBolt",
        "Target": "Hostile",
        "AttackDistanceRange": [15, 15],
        "PostExecuteDistanceRange": [10, 12],
        "WeightCoefficient": 1.0,
        "Conditions": [
          {
            "Type": "TargetDistance",
            "Curve": { "ResponseCurve": "SimpleLogistic", "XRange": [0, 18] }
          },
          {
            "Type": "TimeSinceLastUsed",
            "Curve": { "ResponseCurve": "Linear", "XRange": [0, 2] }
          }
        ]
      },
      "LightningBarrage": {
        "Type": "Ability",
        "Description": "Rapid fire three lightning bolts",
        "Ability": "Storm_Mage_LightningBarrage",
        "Target": "Hostile",
        "AttackDistanceRange": [12, 12],
        "PostExecuteDistanceRange": [8, 10],
        "ChargeFor": 1.0,
        "WeightCoefficient": 1.3,
        "Conditions": [
          {
            "Type": "TargetDistance",
            "Curve": { "ResponseCurve": "SimpleLogistic", "XRange": [0, 15] }
          },
          {
            "Type": "TimeSinceLastUsed",
            "Curve": { "Type": "Switch", "SwitchPoint": 8 }
          },
          {
            "Type": "TargetStatPercent",
            "Stat": "Health",
            "Curve": "Linear"
          }
        ]
      },
      "Retreat": {
        "Type": "Ability",
        "Description": "Teleport away when target gets too close",
        "Ability": "Storm_Mage_Retreat",
        "Target": "Self",
        "WeightCoefficient": 1.4,
        "Conditions": [
          {
            "Type": "TargetDistance",
            "Curve": { "ResponseCurve": "SimpleDescendingLogistic", "XRange": [0, 6] }
          },
          {
            "Type": "TimeSinceLastUsed",
            "Curve": { "Type": "Switch", "SwitchPoint": 5 }
          }
        ]
      }
    },
    "ActionSets": {
      "Default": {
        "BasicAttacks": {
          "Attacks": ["Storm_Mage_LightningBolt"],
          "Randomise": false,
          "MaxRange": 15,
          "Timeout": 1.0,
          "CooldownRange": [1.5, 2.5]
        },
        "Actions": [
          "SelectTarget",
          "LightningBolt",
          "LightningBarrage",
          "Retreat"
        ]
      }
    }
  }
}
```

### Storm Mage AI design

The Storm Mage is a ranged caster that:
- **Prefers range** — `PostExecuteDistanceRange` keeps it 10-12 blocks away after attacking
- **Uses LightningBarrage** on high-health targets (the `TargetStatPercent(Health, Linear)` condition scores highest when the target has lots of health)
- **Retreats** when players close to within 6 blocks (descending logistic scores high at close range)
- **Flees** at 20% health (defined in the role file)

---

## Step 7: Add Translation Keys

Add to `YourMod/Assets/Languages/en-US.lang`:

```
server.items.Weapon_Staff_Lightning.name=Lightning Staff
server.items.Weapon_Staff_Lightning.description=A crackling staff that channels lightning energy.
server.npcRoles.Storm_Mage.name=Storm Mage
server.effects.Lightning_Stun.name=Stunned
server.effects.Lightning_Shock.name=Shocked
```

---

## Step 8: Test the Combat System

1. Place your mod folder in the server mods directory and start the server.
2. Give yourself the Lightning Staff using the developer item spawner.
3. Test the weapon:

| Test | Expected result |
|------|----------------|
| Fire at terrain | Lightning bolt hits terrain, sparks particle plays, miss sound plays |
| Fire at NPC | NPC takes 45 Lightning damage (blue numbers), gets stunned for 1.5s, knockback applied |
| Check NPC stamina | NPC stamina depleted (StaminaLoss: true) |
| Check equipment durability | Target's equipment NOT damaged (DurabilityLoss: false) |
| Fire at group of NPCs | AoE damages entities within 3 blocks at 50% falloff |

4. Spawn a Storm Mage and test NPC combat:

| Test | Expected result |
|------|----------------|
| Approach Storm Mage | Starts firing lightning bolts at 15-block range |
| Rush into melee | Storm Mage uses Retreat ability to teleport away |
| Wait for barrage | Storm Mage charges for 1s then fires rapid bolts |
| Damage to 20% HP | Storm Mage flees at speed 7 |

### Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| Damage numbers appear white | Damage type not found | Verify `Lightning.json` exists in `Entity/Damage/` and has `DamageTextColor` |
| Projectile does no damage | `BaseDamage` key mismatch | Ensure `BaseDamage` key matches damage type filename: `"Lightning"` |
| Stun effect does not apply | Effect ID mismatch | Verify `EffectId` in interaction matches the effect file's `Id` field |
| No knockback on hit | Missing knockback config | Check `DamageEffects.Knockback` has `Force` > 0 |
| Weapon not craftable | Bench ID wrong | Verify `BenchRequirement.Id` matches an existing crafting bench |
| NPC does not use lightning | CAE not referenced | Ensure the NPC role references the CAE file in its template wiring |

---

## Complete File Listing

```
YourMod/
  Assets/
    Server/
      Entity/
        Damage/
          Lightning.json
        Effects/
          Effect_Lightning_Stun.json
          Effect_Lightning_Shock.json
      Projectiles/
        Spells/
          LightningBolt.json
      ProjectileConfigs/
        Weapons/
          Staff/
            Lightning/
              Projectile_Config_LightningBolt.json
      Item/
        Items/
          Weapon/
            Staff/
              Weapon_Staff_Lightning.json
      NPC/
        Roles/
          MyMod/
            Storm_Mage.json
        Balancing/
          Intelligent/
            CAE_Storm_Mage.json
    Languages/
      en-US.lang
```

---

## Next Steps

- [NPC AI Behavior Trees](/hytale-modding-docs/tutorials/advanced/npc-ai-behavior-trees) — add complex multi-state AI to the Storm Mage
- [Custom Dungeons](/hytale-modding-docs/tutorials/advanced/custom-dungeons) — use the Lightning system in dungeon encounters
- [Damage Types](/hytale-modding-docs/reference/combat-and-projectiles/damage-types) — full damage type reference
- [Projectile Configs](/hytale-modding-docs/reference/combat-and-projectiles/projectile-configs) — complete projectile config schema
- [Item Definitions](/hytale-modding-docs/reference/item-system/item-definitions) — full item schema reference
