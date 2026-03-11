---
title: Instances
description: Reference for instance configuration files in Hytale, which define self-contained world instances with spawn points, world generation, game modes, NPC behaviour, chunk storage, and discovery UI.
---

## Overview

Instance configuration files define self-contained worlds that players can enter — the overworld zones, dungeon instances, creative hubs, and portal destinations. Each instance has a `config.json` that specifies the world seed, spawn point, world generation type, game mode, and a wide range of gameplay toggles (PvP, fall damage, NPC spawning, block ticking, etc.). Instances also configure their chunk storage backend, plugin settings, and an optional discovery UI that displays a title card when players enter.

Instance directories also contain a `resources/` folder with runtime state files (e.g. `InstanceData.json`, `Time.json`) that track persistent world state.

## File Location

```
Assets/Server/Instances/
  Basic/
  Challenge_Combat_1/
  CreativeHub/
    config.json
    resources/
  Default/
  Default_Flat/
  Default_Void/
  Dungeon_1/
  Dungeon_Goblin/
  Dungeon_Outlander/
  Forgotten_Temple/
    config.json
    resources/
  Movement_Gym/
    config.json
    resources/
  NPC_Faction_Gym/
  NPC_Gym/
  Persistent/
  Portals_Hedera/
  Portals_Henges/
  Portals_Jungles/
  Portals_Oasis/
  Portals_Taiga/
  ShortLived/
  TimeOut/
  Zone1_Plains1/
  Zone2_Desert1/
  Zone3_Taiga1/
  Zone4_Volcanic1/
```

## Schema

### config.json

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Version` | `number` | Yes | — | Config format version (currently `4`). |
| `UUID` | `object` | Yes | — | Binary UUID identifying this instance. Contains `$binary` and `$type` fields. |
| `DisplayName` | `string` | No | — | Human-readable name for the instance (e.g. `"the Crossroads"`). |
| `Seed` | `number` | Yes | — | World generation seed. |
| `SpawnProvider` | `SpawnProvider` | Yes | — | Spawn point configuration. |
| `WorldGen` | `WorldGen` | Yes | — | World generation settings. |
| `WorldMap` | `WorldMap` | No | — | World map display configuration. |
| `ChunkStorage` | `ChunkStorage` | Yes | — | Backend for chunk data persistence. |
| `ChunkConfig` | `object` | No | `{}` | Additional chunk-level configuration overrides. |
| `IsTicking` | `boolean` | No | `false` | Whether entity tick updates run in this instance. |
| `IsBlockTicking` | `boolean` | No | `false` | Whether block tick updates run (e.g. crop growth, fire spread). |
| `IsPvpEnabled` | `boolean` | No | `false` | Whether player-versus-player damage is enabled. |
| `IsFallDamageEnabled` | `boolean` | No | `true` | Whether fall damage is applied. |
| `IsGameTimePaused` | `boolean` | No | `false` | Whether the in-game day/night clock is frozen. |
| `GameTime` | `string` | No | — | Initial game time as an ISO 8601 timestamp. |
| `ClientEffects` | `ClientEffects` | No | — | Visual overrides for sun, bloom, and sunshaft rendering. |
| `RequiredPlugins` | `object` | No | `{}` | Map of plugin IDs required for this instance. |
| `GameMode` | `string` | No | — | Game mode: `"Creative"`, `"Adventure"`, `"Survival"`. |
| `IsSpawningNPC` | `boolean` | No | `true` | Whether NPCs spawn naturally in this instance. |
| `IsSpawnMarkersEnabled` | `boolean` | No | `true` | Whether spawn markers in prefabs are active. |
| `IsAllNPCFrozen` | `boolean` | No | `false` | When `true`, all NPCs are frozen and do not move or act. |
| `GameplayConfig` | `string` | No | `"Default"` | ID of the gameplay config to use. References a file in `GameplayConfigs/`. |
| `IsCompassUpdating` | `boolean` | No | `true` | Whether the compass UI updates in this instance. |
| `IsSavingPlayers` | `boolean` | No | `true` | Whether player state is saved when they leave. |
| `IsSavingChunks` | `boolean` | No | `true` | Whether modified chunks are saved to storage. |
| `SaveNewChunks` | `boolean` | No | `true` | Whether newly generated chunks are saved. |
| `IsUnloadingChunks` | `boolean` | No | `true` | Whether chunks unload when no players are nearby. |
| `IsObjectiveMarkersEnabled` | `boolean` | No | `true` | Whether objective markers are visible. |
| `DeleteOnUniverseStart` | `boolean` | No | `false` | Whether this instance is deleted when the universe restarts. |
| `DeleteOnRemove` | `boolean` | No | `false` | Whether the instance data is deleted when the instance is removed. |
| `ResourceStorage` | `ResourceStorage` | No | — | Backend for resource data persistence. |
| `Plugin` | `PluginConfig` | No | — | Plugin-specific settings, including instance discovery UI. |

### SpawnProvider

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Id` | `string` | Yes | — | Spawn provider type: `"Global"` for a fixed world spawn. |
| `SpawnPoint` | `SpawnPoint` | Yes | — | World coordinates and rotation for the spawn position. |

### SpawnPoint

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `X` | `number` | Yes | — | X coordinate in blocks. |
| `Y` | `number` | Yes | — | Y coordinate (vertical) in blocks. |
| `Z` | `number` | Yes | — | Z coordinate in blocks. |
| `Pitch` | `number` | No | `0` | Camera pitch angle in degrees. |
| `Yaw` | `number` | No | `0` | Camera yaw angle in degrees. |
| `Roll` | `number` | No | `0` | Camera roll angle in degrees. |

### WorldGen

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Type` | `string` | Yes | — | Generator type: `"Hytale"` (legacy), `"HytaleGenerator"` (node-graph). |
| `Name` | `string` | No | — | World generation profile name (used with `"Hytale"` type). |
| `Environment` | `string` | No | — | Environment ID for this world (used with `"Hytale"` type). |
| `WorldStructure` | `string` | No | — | World structure name (used with `"HytaleGenerator"` type). |

### WorldMap

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Type` | `string` | Yes | — | `"WorldGen"` (shows biome map), `"Disabled"` (no map). |

### ClientEffects

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `SunHeightPercent` | `number` | No | — | Sun height override as a percentage. |
| `SunAngleDegrees` | `number` | No | — | Sun angle override in degrees. |
| `BloomIntensity` | `number` | No | — | Post-process bloom intensity. |
| `BloomPower` | `number` | No | — | Bloom power exponent. |
| `SunIntensity` | `number` | No | — | Sun light intensity multiplier. |
| `SunshaftIntensity` | `number` | No | — | God-ray intensity. |
| `SunshaftScaleFactor` | `number` | No | — | God-ray scale factor. |

### Discovery (Plugin.Instance.Discovery)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `TitleKey` | `string` | Yes | — | Localisation key for the title shown when entering. |
| `SubtitleKey` | `string` | No | — | Localisation key for the subtitle. |
| `Display` | `boolean` | No | `true` | Whether the discovery card is shown. |
| `AlwaysDisplay` | `boolean` | No | `false` | Show the card every time, not just on first entry. |
| `Icon` | `string` | No | — | Icon image filename for the discovery card. |
| `Major` | `boolean` | No | `false` | Whether this is a major discovery (larger UI treatment). |
| `Duration` | `number` | No | — | Seconds the discovery card is displayed. |
| `FadeInDuration` | `number` | No | — | Seconds for the card fade-in transition. |
| `FadeOutDuration` | `number` | No | — | Seconds for the card fade-out transition. |

### Instance Plugin Config

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `RemovalConditions` | `array` | No | `[]` | Conditions under which this instance is automatically removed. |
| `PreventReconnection` | `boolean` | No | `false` | When `true`, players cannot reconnect to this instance after disconnecting. |
| `Discovery` | `Discovery` | No | — | Discovery UI configuration. |

## Examples

**Creative Hub** (`Assets/Server/Instances/CreativeHub/config.json`, condensed):

```json
{
  "Version": 4,
  "DisplayName": "the Crossroads",
  "Seed": 1618917989368,
  "SpawnProvider": {
    "Id": "Global",
    "SpawnPoint": { "X": 5103.5, "Y": 168.0, "Z": 4982.5, "Yaw": 90.0 }
  },
  "WorldGen": {
    "Type": "Hytale",
    "Name": "Instance_Creative_Hub",
    "Environment": "Env_Creative_Hub"
  },
  "WorldMap": { "Type": "Disabled" },
  "GameMode": "Creative",
  "IsSpawningNPC": false,
  "IsAllNPCFrozen": true,
  "IsGameTimePaused": true,
  "GameplayConfig": "CreativeHub",
  "IsSavingPlayers": false,
  "Plugin": {
    "Instance": {
      "PreventReconnection": true,
      "Discovery": {
        "TitleKey": "server.instances.creative_hub.title",
        "SubtitleKey": "server.instances.creative_hub.subtitle",
        "Display": true,
        "Icon": "Forgotten_Temple.png",
        "Major": true,
        "Duration": 4.0,
        "FadeInDuration": 1.5,
        "FadeOutDuration": 1.5
      }
    }
  }
}
```

**Movement Gym with visual overrides** (`Assets/Server/Instances/Movement_Gym/config.json`, condensed):

```json
{
  "Version": 4,
  "WorldGen": {
    "Type": "HytaleGenerator",
    "WorldStructure": "Default_Flat"
  },
  "WorldMap": { "Type": "WorldGen" },
  "ClientEffects": {
    "SunHeightPercent": 100.0,
    "BloomIntensity": 0.3,
    "BloomPower": 8.0,
    "SunIntensity": 0.25,
    "SunshaftIntensity": 0.3,
    "SunshaftScaleFactor": 4.0
  },
  "GameMode": "Creative",
  "IsGameTimePaused": true,
  "IsObjectiveMarkersEnabled": true
}
```

## Related Pages

- [Gameplay Configs](/hytale-modding-docs/reference/game-configuration/gameplay-configs) — gameplay rules applied within instances
- [Portal Types](/hytale-modding-docs/reference/world-and-environment/portal-types) — portal definitions that connect to instance IDs
- [World Generation](/hytale-modding-docs/reference/world-and-environment/world-generation) — generator pipeline selected by `WorldGen.Type`
- [Environments](/hytale-modding-docs/reference/world-and-environment/environments) — environment files referenced by `WorldGen.Environment`
