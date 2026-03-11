---
title: NPC Spawn Rules
description: Configuration files that control where, when, and how NPCs spawn into the world via beacons, markers, and world spawn tables.
---

## Overview

Spawn rule files link NPC roles to world locations and conditions. The system has three spawn mechanisms: **Beacon spawns** manage dynamic spawn points tied to environment tags with lifecycle controls; **World spawns** are simpler tables tied to environment tags and optional day-time windows; **Marker spawns** are placed directly in the world and reference specific NPC names with respawn timers.

## File Location

- `Assets/Server/NPC/Spawn/Beacons/**/*.json` — Beacon-driven spawners
- `Assets/Server/NPC/Spawn/World/**/*.json` — World environment spawners
- `Assets/Server/NPC/Spawn/Markers/**/*.json` — Placed marker spawners
- `Assets/Server/NPC/Spawn/Suppression/**/*.json` — Spawn suppression volumes

## How NPC Spawning Works

```mermaid
flowchart TD;
    A[World Loads Chunk] --> B{Check Spawn Sources};

    B --> C[Beacon Spawns];
    B --> D[World Spawns];
    B --> E[Marker Spawns];

    C --> F["Environment<br>Matches?"];
    F -->|"Yes"| G["Player in<br>Range?"];
    F -->|"No"| Z[Skip];
    G -->|"Yes"| H["Light Level<br>OK?"];
    G -->|"No"| Z;
    H -->|"Yes"| I[Select NPC by Weight];
    H -->|"No"| Z;

    D --> J["Environment<br>Matches?"];
    J -->|"Yes"| K["DayTimeRange<br>OK?"];
    J -->|"No"| Z;
    K -->|"Yes"| L[Select NPC by Weight];
    K -->|"No"| Z;

    E --> M["Player Near<br>Marker?"];
    M -->|"Yes"| N["Respawn Timer<br>Ready?"];
    M -->|"No"| Z;
    N -->|"Yes"| O[Spawn Specific NPC];
    N -->|"No"| Z;

    I --> P["MaxSpawnedNPCs<br>Reached?"];
    P -->|"No"| Q[Spawn NPC];
    P -->|"Yes"| Z;
    L --> Q;
    O --> Q;

    Q --> R["Flock<br>Defined?"];
    R -->|"Yes"| S["Spawn Group<br>Size: min-max"];
    R -->|"No"| T[Spawn Single NPC];

    style A fill:darkgreen,color:white;
    style Q fill:rebeccapurple,color:white;
    style Z fill:darkred,color:white;```

### Suppression Zones

```mermaid
flowchart LR;
    A["NPC Tries to Spawn"] --> B["Inside Suppression<br>Volume?"];
    B -->|"No"| C[Spawn Allowed];
    B -->|"Yes"| D["NPC Group in<br>SuppressedGroups?"];
    D -->|"No"| C;
    D -->|"Yes"| E[Spawn Blocked];

    style C fill:darkgreen,color:white;
    style E fill:darkred,color:white;```

## Schema

### Beacon Spawn

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Environments` | string[] | Yes | — | Environment tag IDs where this beacon is active. |
| `NPCs` | array | Yes | — | List of NPC entries (see NPC entry table below). |
| `MinDistanceFromPlayer` | number | No | — | Minimum distance from the player to spawn, in blocks. |
| `MaxSpawnedNPCs` | number | No | — | Maximum live NPCs this beacon will maintain. |
| `ConcurrentSpawnsRange` | [number, number] | No | — | Min/max NPCs to spawn in a single spawn event. |
| `SpawnAfterGameTimeRange` | [string, string] | No | — | ISO 8601 duration range before the first spawn (e.g. `["PT20M", "PT40M"]`). |
| `NPCIdleDespawnTime` | number | No | — | Seconds an idle NPC persists before despawning. |
| `BeaconVacantDespawnGameTime` | string | No | — | ISO 8601 duration — how long a vacant beacon waits before despawning. |
| `BeaconRadius` | number | No | — | Radius of the beacon's managed area, in blocks. |
| `SpawnRadius` | number | No | — | Radius within which NPCs are spawned, in blocks. |
| `TargetDistanceFromPlayer` | number | No | — | Ideal spawn distance from the player. |
| `LightRanges` | object | No | — | Block light level constraints, e.g. `{ "Light": [0, 2] }`. |

### World Spawn

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Environments` | string[] | Yes | — | Environment tag IDs where this spawn table is active. |
| `NPCs` | array | Yes | — | List of NPC entries (see NPC entry table below). |
| `DayTimeRange` | [number, number] | No | — | In-game hour range when spawning is allowed, e.g. `[6, 18]` for daytime only. |

### Marker Spawn

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Model` | string | Yes | — | The marker model ID (typically `"NPC_Spawn_Marker"`). |
| `NPCs` | array | Yes | — | List of NPC entries (see NPC entry table below). |
| `ExclusionRadius` | number | No | — | Other markers within this radius will not also spawn, in blocks. |
| `RealtimeRespawn` | boolean | No | `false` | If `true`, NPCs respawn on a real-time timer. |
| `MaxDropHeight` | number | No | — | Maximum distance above the ground the NPC can be placed. |
| `DeactivationDistance` | number | No | — | Distance from player at which this marker stops simulating, in blocks. |

### Suppression Volume

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `SuppressionRadius` | number | Yes | — | Radius of the suppression zone, in blocks. |
| `SuppressedGroups` | string[] | Yes | — | NPC group IDs suppressed within this zone (e.g. `["Aggressive", "Passive"]`). |
| `SuppressSpawnMarkers` | boolean | No | `false` | If `true`, also suppresses spawn markers within the zone. |

### NPC Entry (used in `NPCs` array)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Id` / `Name` | string | Yes | — | Role ID of the NPC to spawn. Beacons use `Id`; markers use `Name`. |
| `Weight` | number | No | — | Relative spawn weight when selecting from multiple candidates. |
| `Flock` | string \| object | No | — | Flock group ID (string) or inline flock size spec `{ "Size": [min, max] }`. |
| `SpawnBlockSet` | string | No | — | Block set tag the NPC must spawn on (e.g. `"Volcanic"`, `"Portals_Oasis_Soil"`). |
| `SpawnFluidTag` | string | No | — | Fluid tag required near the spawn point (e.g. `"Water"`). |
| `RealtimeRespawnTime` | number | No | — | Seconds before this NPC respawns (marker spawns). |
| `SpawnAfterGameTime` | string | No | — | ISO 8601 duration before this entry becomes eligible (e.g. `"P1D"`). |

## Examples

### Beacon spawn (cave goblins)

```json
{
  "Environments": ["Env_Zone1_Caves_Goblins"],
  "MinDistanceFromPlayer": 15,
  "MaxSpawnedNPCs": 3,
  "ConcurrentSpawnsRange": [1, 2],
  "SpawnAfterGameTimeRange": ["PT20M", "PT40M"],
  "NPCIdleDespawnTime": 60,
  "BeaconVacantDespawnGameTime": "PT15M",
  "BeaconRadius": 50,
  "SpawnRadius": 40,
  "TargetDistanceFromPlayer": 25,
  "NPCs": [
    { "Weight": 60, "SpawnBlockSet": "Volcanic", "Id": "Goblin_Scrapper" },
    { "Weight": 20, "SpawnBlockSet": "Volcanic", "Id": "Goblin_Lobber" },
    { "Weight": 20, "SpawnBlockSet": "Volcanic", "Id": "Goblin_Miner" }
  ],
  "LightRanges": {
    "Light": [0, 2]
  }
}
```

### World spawn (oasis animals, daytime only)

```json
{
  "Environments": ["Env_Portals_Oasis"],
  "NPCs": [
    {
      "Weight": 15,
      "SpawnBlockSet": "Portals_Oasis_Soil",
      "SpawnFluidTag": "Water",
      "Id": "Flamingo",
      "Flock": "Group_Small"
    },
    {
      "Weight": 10,
      "SpawnBlockSet": "Portals_Oasis_Soil",
      "Id": "Tortoise"
    }
  ],
  "DayTimeRange": [6, 18]
}
```

### Marker spawn (bear, real-time respawn)

```json
{
  "Model": "NPC_Spawn_Marker",
  "NPCs": [
    {
      "Name": "Bear_Grizzly",
      "Weight": 100,
      "RealtimeRespawnTime": 420
    }
  ],
  "ExclusionRadius": 20,
  "RealtimeRespawn": true,
  "MaxDropHeight": 4,
  "DeactivationDistance": 150
}
```

### Suppression volume

```json
{
  "SuppressionRadius": 45,
  "SuppressedGroups": ["Aggressive", "Passive", "Neutral"],
  "SuppressSpawnMarkers": true
}
```

## Related Pages

- [NPC Roles](/hytale-modding-docs/reference/npc-system/npc-roles) — Role files referenced by `Id` / `Name` in spawn entries
- [NPC Groups](/hytale-modding-docs/reference/npc-system/npc-groups) — Group IDs used in `Flock` and suppression
- [NPC Attitudes](/hytale-modding-docs/reference/npc-system/npc-attitudes) — How spawned NPCs relate to each other
