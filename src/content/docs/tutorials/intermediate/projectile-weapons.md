---
title: Create a Projectile Weapon
description: Step-by-step tutorial for creating a projectile weapon with projectile definitions, projectile configs, and interaction chains.
sidebar:
  order: 5
---

## Goal

Create a custom **Frost Staff** that fires ice bolt projectiles. You will define the projectile entity, create a projectile config that controls launch physics and hit interactions, and wire it all together through the weapon's interaction chain.

## What You'll Learn

- How projectile definitions control appearance, physics, and damage
- How projectile configs connect weapons to projectiles with launch settings
- How the interaction chain fires projectiles on weapon use
- How hit and miss interactions handle impact effects

## Prerequisites

- A mod folder with a valid `manifest.json` (see [Setup Your Dev Environment](/hytale-modding-docs/tutorials/beginner/setup-dev-environment))
- Familiarity with item definitions (see [Create a Custom Item](/hytale-modding-docs/tutorials/beginner/create-an-item))

---

## Projectile System Overview

Hytale's projectile system has three layers:

1. **Projectile Definition** (`Assets/Server/Projectiles/`) -- defines the projectile entity itself: appearance, physics, damage, and effects
2. **Projectile Config** (`Assets/Server/ProjectileConfigs/`) -- connects a weapon to a projectile with launch force, sounds, and interaction chains for hit/miss
3. **Weapon Item** -- references the projectile config through its interaction chain

```
Weapon Item
  └─ references → Projectile Config
                     └─ references → Projectile Definition
```

---

## Step 1: Create the Projectile Definition

Projectile definitions describe the physical projectile that travels through the world. The vanilla `Ice_Bolt.json` and `Arrow_FullCharge.json` are good reference points.

Create:

```
YourMod/Assets/Server/Projectiles/Frost_Bolt.json
```

```json
{
  "Appearance": "Ice_Bolt",
  "Radius": 0.2,
  "Height": 0.2,
  "SticksVertically": true,
  "MuzzleVelocity": 45,
  "TerminalVelocity": 50,
  "Gravity": 5,
  "Bounciness": 0,
  "ImpactSlowdown": 0,
  "TimeToLive": 15,
  "Damage": 18,
  "DeadTimeMiss": 0,
  "DeathEffectsOnHit": true,
  "HorizontalCenterShot": 0.15,
  "VerticalCenterShot": 0.1,
  "DepthShot": 1.5,
  "PitchAdjustShot": true,
  "HitParticles": {
    "SystemId": "Impact_Ice"
  },
  "DeathParticles": {
    "SystemId": "Impact_Ice"
  },
  "HitSoundEventId": "SFX_Ice_Break",
  "MissSoundEventId": "SFX_Ice_Break",
  "DeathSoundEventId": "SFX_Ice_Break"
}
```

### Projectile fields explained

| Field | Purpose |
|-------|---------|
| `Appearance` | The visual model for the projectile. Must match a known projectile appearance name |
| `Radius` / `Height` | Collision hitbox dimensions of the projectile |
| `MuzzleVelocity` | Initial launch speed (units per second) |
| `TerminalVelocity` | Maximum speed the projectile can reach |
| `Gravity` | Downward acceleration. Lower values = flatter trajectory. Arrows use 10, ice bolts use 3-5 |
| `Bounciness` | How much the projectile bounces on impact. `0` = no bounce |
| `ImpactSlowdown` | Speed reduction on hit. `0` = projectile stops |
| `TimeToLive` | Seconds before the projectile despawns if it hits nothing |
| `Damage` | Base damage dealt on hit |
| `SticksVertically` | If `true`, the projectile embeds in surfaces on miss |
| `DeadTimeMiss` | Seconds the projectile lingers after missing. `0` = disappears immediately |
| `DeathEffectsOnHit` | If `true`, death particles play on hit as well as on natural expiry |
| `HorizontalCenterShot` / `VerticalCenterShot` | Accuracy spread. Lower values = more accurate. `0` = perfectly centred |
| `DepthShot` | Forward offset from the character when the projectile spawns |
| `PitchAdjustShot` | If `true`, the projectile's initial angle matches the player's aim pitch |
| `HitParticles` / `DeathParticles` | Particle effect system IDs played on hit or death |
| `HitSoundEventId` / `MissSoundEventId` | Sound events for impact and miss |

---

## Step 2: Create the Projectile Config

The projectile config connects a weapon to a projectile. It specifies launch force, physics overrides, sounds, and the interaction chain that runs on hit or miss. Configs live in `Assets/Server/ProjectileConfigs/`.

Create:

```
YourMod/Assets/Server/ProjectileConfigs/Weapons/Staff/Projectile_Config_Frost_Staff.json
```

```json
{
  "Model": "Ice_Bolt",
  "LaunchForce": 20,
  "Physics": {
    "Type": "Standard",
    "Gravity": 5,
    "TerminalVelocityAir": 50,
    "TerminalVelocityWater": 15,
    "RotationMode": "VelocityDamped",
    "Bounciness": 0.0,
    "SticksVertically": true
  },
  "LaunchLocalSoundEventId": "SFX_Staff_Shoot_Local",
  "LaunchWorldSoundEventId": "SFX_Staff_Shoot",
  "Interactions": {
    "ProjectileHit": {
      "Interactions": [
        {
          "Type": "Replace",
          "Var": "Primary_Shoot_Damage",
          "DefaultValue": {
            "Interactions": [
              "Weapon_Staff_Frost_Damage"
            ]
          }
        },
        {
          "Type": "Replace",
          "Var": "Primary_Shoot_Impact",
          "DefaultValue": {
            "Interactions": [
              "Common_Projectile_Impact_Effects"
            ]
          }
        },
        "Common_Projectile_Despawn"
      ]
    },
    "ProjectileMiss": {
      "Interactions": [
        {
          "Type": "Replace",
          "Var": "Primary_Shoot_Miss",
          "DefaultValue": {
            "Interactions": [
              "Common_Projectile_Miss"
            ]
          }
        },
        "Common_Projectile_Despawn"
      ]
    }
  }
}
```

### Projectile config fields

| Field | Purpose |
|-------|---------|
| `Model` | The projectile appearance model to use |
| `LaunchForce` | Force applied when firing. Higher = faster initial speed |
| `Physics.Type` | Physics simulation type. `"Standard"` is the default |
| `Physics.Gravity` | Gravity override for the config (overrides the projectile definition's value) |
| `Physics.TerminalVelocityAir` / `TerminalVelocityWater` | Max speed in air and water |
| `Physics.RotationMode` | How the projectile rotates in flight. `"VelocityDamped"` makes it face the direction of travel |
| `Interactions.ProjectileHit` | Interaction chain executed when the projectile hits an entity |
| `Interactions.ProjectileMiss` | Interaction chain executed when the projectile hits terrain or expires |

### Interaction chain structure

The `Interactions` object uses a replace-variable pattern. Each entry with `"Type": "Replace"` defines a named variable (`Var`) with a `DefaultValue` containing interaction references. This allows templates to override specific parts of the chain. The string entries (like `"Common_Projectile_Despawn"`) reference shared interaction files.

---

## Step 3: Create the Weapon Item

The weapon item references the projectile config through its interaction setup. Create the staff item definition:

```
YourMod/Assets/Server/Item/Items/Weapon/Weapon_Staff_Frost.json
```

```json
{
  "TranslationProperties": {
    "Name": "server.items.Weapon_Staff_Frost.name",
    "Description": "server.items.Weapon_Staff_Frost.description"
  },
  "Icon": "Icons/MyMod/Weapon_Staff_Frost.png",
  "Quality": "Rare",
  "MaxStack": 1,
  "ItemLevel": 5,
  "Interactions": {
    "Primary": "Staff_Frost_Primary_Shoot",
    "Secondary": "Staff_Frost_Secondary_Block"
  },
  "ProjectileConfig": "Projectile_Config_Frost_Staff",
  "Recipe": {
    "TimeSeconds": 8,
    "Input": [
      {
        "ItemId": "Ingredient_Bar_Iron",
        "Quantity": 5
      },
      {
        "ItemId": "Ingredient_Ice_Essence",
        "Quantity": 10
      },
      {
        "ItemId": "Ingredient_Crystal_Cyan",
        "Quantity": 3
      }
    ],
    "OutputQuantity": 1,
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Id": "Weapon_Bench",
        "Categories": [
          "Weapon_Bow"
        ]
      }
    ]
  },
  "PlayerAnimationsId": "Staff",
  "Tags": {
    "Type": [
      "Weapon"
    ],
    "Family": [
      "Staff"
    ]
  },
  "ItemSoundSetId": "ISS_Weapons_Staff"
}
```

### Key weapon fields

| Field | Purpose |
|-------|---------|
| `Interactions.Primary` | The interaction file triggered on primary attack (left click). This interaction chain ultimately fires the projectile |
| `Interactions.Secondary` | The interaction file triggered on secondary action (right click) |
| `ProjectileConfig` | References the projectile config file by name (without `.json`). This is what connects the weapon to its projectile |

---

## Step 4: Add Translation Keys

```
YourMod/Assets/Languages/en-US.lang
```

```
server.items.Weapon_Staff_Frost.name=Frost Staff
server.items.Weapon_Staff_Frost.description=A staff that fires bolts of freezing ice.
```

---

## Step 5: Test In-Game

1. Place your mod folder in the server mods directory.
2. Start the server and watch for errors about unknown projectile configs or missing interaction files.
3. Use the developer item spawner to give yourself `Weapon_Staff_Frost`.
4. Equip the staff and use primary attack (left click) to fire the projectile.
5. Verify the projectile travels with the correct arc (gravity), speed, and appearance.
6. Hit an NPC and confirm damage is applied and hit particles play.
7. Fire at terrain and confirm miss sound and particles play.
8. Check that the projectile despawns after `TimeToLive` seconds if it hits nothing.

**Common errors and fixes:**

| Error | Cause | Fix |
|-------|-------|-----|
| `Unknown projectile config` | Config file not found | Verify file path under `ProjectileConfigs/` and filename matches `ProjectileConfig` value |
| Projectile flies straight up | `PitchAdjustShot` is false | Set `"PitchAdjustShot": true` |
| Projectile drops too fast | `Gravity` too high | Reduce gravity. Arrows use 10, magic bolts use 3-5 |
| No visual on projectile | Wrong `Appearance` | Check `Assets/Server/Models/Projectiles/` for valid appearance names |
| No damage on hit | `Damage` is 0 or interactions missing | Set `Damage` > 0 and verify `ProjectileHit` interaction chain |

---

## Next Steps

- [Create a Custom Item](/hytale-modding-docs/tutorials/beginner/create-an-item) -- understand the full item definition structure
- [Create a Crafting Bench](/hytale-modding-docs/tutorials/intermediate/create-a-crafting-bench) -- build the bench where players craft your weapon
- [Custom Loot Tables](/hytale-modding-docs/tutorials/intermediate/custom-loot-tables) -- make your weapon drop from enemies
