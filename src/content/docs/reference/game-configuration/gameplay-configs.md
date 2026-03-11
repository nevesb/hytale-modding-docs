---
title: Gameplay Configs
description: Reference for gameplay configuration files in Hytale, which control death penalties, item durability, day/night cycle duration, player settings, stamina, respawn, and more.
---

## Overview

Gameplay config files are the top-level tuning files for a world or instance. They support inheritance via a `Parent` field — child configs override only the fields they declare, inheriting everything else from the parent. The `Default.json` config is the base for all standard worlds; `Default_Instance.json` extends it for instanced content with different death and world-editing rules.

## File Location

```
Assets/Server/GameplayConfigs/
  Default.json
  Default_Instance.json
  CreativeHub.json
  ForgottenTemple.json
  Portal.json
```

## Schema

### Top-level

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Parent` | `string` | No | — | ID of a parent config to inherit from. Only overridden fields need to be specified in the child. |
| `Gathering` | `GatheringConfig` | No | — | Settings for block gathering feedback (unbreakable blocks, incorrect tool responses). |
| `Death` | `DeathConfig` | No | — | Controls what happens to items and respawn on player death. |
| `ItemEntity` | `ItemEntityConfig` | No | — | Settings for dropped item entities in the world. |
| `ItemDurability` | `ItemDurabilityConfig` | No | — | Penalty multipliers applied when equipment durability reaches zero. |
| `Plugin` | `PluginConfig` | No | — | Configuration for gameplay plugins: Stamina, Memories. |
| `Respawn` | `RespawnConfig` | No | — | Respawn point rules. |
| `World` | `WorldConfig` | No | — | Day/night cycle durations and block interaction settings. |
| `Player` | `PlayerConfig` | No | — | Movement, hitbox, and armour visibility settings. |
| `CameraEffects` | `CameraEffectsConfig` | No | — | Visual effects triggered by damage types. |
| `CreativePlaySoundSet` | `string` | No | — | Sound set used during creative mode play. |
| `Spawn` | `SpawnConfig` | No | — | Particle effects shown on first player spawn. |
| `Ping` | `PingConfig` | No | — | World ping settings (duration, cooldown, radius, sound). |

### DeathConfig

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `ItemsLossMode` | `"Configured" \| "None" \| "All"` | No | — | Determines which items are lost on death. `Configured` uses percentage fields; `None` keeps all items; `All` drops everything. |
| `ItemsAmountLossPercentage` | `number` | No | — | Percentage of item stacks lost on death when `ItemsLossMode` is `"Configured"`. |
| `ItemsDurabilityLossPercentage` | `number` | No | — | Percentage of equipment durability lost on death. |
| `LoseItems` | `boolean` | No | — | Shorthand override: `false` prevents any item loss regardless of other settings. |
| `RespawnController` | `object` | No | — | Custom respawn behaviour. `{ "Type": "ExitInstance" }` ejects the player from an instance on death. |

### ItemEntityConfig

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Lifetime` | `number` | No | — | Seconds before a dropped item entity despawns from the world. |

### ItemDurabilityConfig

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `BrokenPenalties` | `object` | No | — | Multipliers applied to the entity's stats when each equipment category is fully broken. |
| `BrokenPenalties.Weapon` | `number` | No | — | Stat multiplier when the equipped weapon has zero durability (e.g. `0.75` = 25% stat reduction). |
| `BrokenPenalties.Armor` | `number` | No | — | Stat multiplier when equipped armour is fully broken. |
| `BrokenPenalties.Tool` | `number` | No | — | Stat multiplier when equipped tool is fully broken. |

### PluginConfig

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Stamina` | `StaminaPlugin` | No | — | Stamina system settings. |
| `Memories` | `MemoriesPlugin` | No | — | Memories (XP) system settings. |
| `Weathers` | `object` | No | — | Weather plugin overrides. |

### StaminaPlugin

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `SprintRegenDelay` | `object` | No | — | Configures how sprinting delays stamina regeneration. |
| `SprintRegenDelay.EntityStatId` | `string` | No | — | The entity stat ID to modify (e.g. `"StaminaRegenDelay"`). |
| `SprintRegenDelay.Value` | `number` | No | — | Value applied to the stat (negative values reduce regen delay). |

### MemoriesPlugin

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `MemoriesAmountPerLevel` | `number[]` | No | — | Array of memory costs per level-up, indexed by level (0-based). |
| `MemoriesRecordParticles` | `string` | No | — | Particle system played when a memory is recorded at a statue. |
| `MemoriesCatchItemId` | `string` | No | — | Item ID of the collectible memory particle in the world. |
| `MemoriesCatchEntityParticle` | `object` | No | — | Particle attached to the entity when catching a memory. |
| `MemoriesCatchParticleViewDistance` | `number` | No | — | View distance in units at which catch particles are visible. |

### RespawnConfig

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `RadiusLimitRespawnPoint` | `number` | No | — | Maximum distance in units from the player's death location where a respawn point can be used. |
| `MaxRespawnPointsPerPlayer` | `number` | No | — | Maximum number of active respawn points a player can have simultaneously. |

### WorldConfig

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `DaytimeDurationSeconds` | `number` | No | — | Real-world seconds for a full daytime period. |
| `NighttimeDurationSeconds` | `number` | No | — | Real-world seconds for a full nighttime period. |
| `BlockPlacementFragilityTimer` | `number` | No | — | Seconds after placement during which a block can be instantly broken by the placer. `0` disables. |
| `AllowBlockBreaking` | `boolean` | No | — | Whether players can break blocks in this world. |
| `AllowBlockGathering` | `boolean` | No | — | Whether players can gather resources from blocks. |
| `Sleep` | `SleepConfig` | No | — | Sleep system configuration. |

### SleepConfig

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `WakeUpHour` | `number` | No | — | In-game hour at which sleeping players wake up. |
| `AllowedSleepHoursRange` | `[number, number]` | No | — | `[start, end]` hour range during which players can go to sleep. Wraps across midnight. |

### PlayerConfig

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `MovementConfig` | `string` | No | — | ID of the movement configuration preset for players. |
| `HitboxCollisionConfig` | `string` | No | — | ID of the hitbox collision preset (e.g. `"SoftCollision"`). |
| `ArmorVisibilityOption` | `"All" \| "None" \| "Cosmetic"` | No | — | Controls which armour layers are visible on the player model. |

### SpawnConfig

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `FirstSpawnParticles` | `ParticleEntry[]` | No | — | Particle systems spawned at the player's location on first spawn. |

### PingConfig

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `PingDuration` | `number` | No | — | Seconds a ping marker remains visible. |
| `PingCooldown` | `number` | No | — | Seconds between allowed pings for a player. |
| `PingBroadcastRadius` | `number` | No | — | Radius in units within which other players see the ping. |
| `PingSound` | `string` | No | — | Sound event played when a ping is placed. |

## Examples

**Default world config** (`Assets/Server/GameplayConfigs/Default.json`):

```json
{
  "Death": {
    "ItemsLossMode": "Configured",
    "ItemsAmountLossPercentage": 50.0,
    "ItemsDurabilityLossPercentage": 10.0
  },
  "ItemEntity": {
    "Lifetime": 600.0
  },
  "ItemDurability": {
    "BrokenPenalties": {
      "Weapon": 0.75,
      "Armor": 0.75,
      "Tool": 0.75
    }
  },
  "Plugin": {
    "Stamina": {
      "SprintRegenDelay": {
        "EntityStatId": "StaminaRegenDelay",
        "Value": -0.75
      }
    },
    "Memories": {
      "MemoriesAmountPerLevel": [10, 25, 50, 100, 200],
      "MemoriesRecordParticles": "MemoryRecordedStatue",
      "MemoriesCatchItemId": "Memory_Particle",
      "MemoriesCatchParticleViewDistance": 64
    }
  },
  "Respawn": {
    "RadiusLimitRespawnPoint": 500,
    "MaxRespawnPointsPerPlayer": 3
  },
  "World": {
    "DaytimeDurationSeconds": 1728,
    "NighttimeDurationSeconds": 1152,
    "BlockPlacementFragilityTimer": 0,
    "Sleep": {
      "WakeUpHour": 4.79,
      "AllowedSleepHoursRange": [19.5, 4.79]
    }
  },
  "Player": {
    "MovementConfig": "Default",
    "HitboxCollisionConfig": "SoftCollision",
    "ArmorVisibilityOption": "All"
  },
  "Ping": {
    "PingDuration": 5.0,
    "PingCooldown": 1.0,
    "PingBroadcastRadius": 100.0,
    "PingSound": "SFX_Ping"
  }
}
```

**Instance config** (`Assets/Server/GameplayConfigs/Default_Instance.json`) — inherits from Default and overrides:

```json
{
  "Parent": "Default",
  "World": {
    "AllowBlockBreaking": false,
    "AllowBlockGathering": false
  },
  "Death": {
    "LoseItems": false,
    "RespawnController": {
      "Type": "ExitInstance"
    }
  }
}
```

## Related Pages

- [Environments](/hytale-modding-docs/reference/world-and-environment/environments) — day/night hour progression driven by `DaytimeDurationSeconds`
- [Drop Tables](/hytale-modding-docs/reference/economy-and-progression/drop-tables) — items dropped on death subject to `ItemsLossMode`
- [Weather System](/hytale-modding-docs/reference/world-and-environment/weather-system) — weather controlled by `Plugin.Weathers`
