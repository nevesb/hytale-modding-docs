---
title: Modify World Generation
description: How to modify world generation using HytaleGenerator configs, including biome weights, environment assignments, ore distribution, and structure placement.
---

## Goal

Modify Hytale's procedural world generation to create a custom biome region with unique environment settings, adjusted ore distribution, custom structure placement rules, and NPC spawn overrides. By the end you will understand how HytaleGenerator config files control terrain shape, biome selection, and feature placement.

## Prerequisites

- A mod folder with a valid `manifest.json` (see [Setup Your Dev Environment](/hytale-modding-docs/tutorials/beginner/setup-dev-environment))
- Familiarity with JSON template inheritance (see [Inheritance and Templates](/hytale-modding-docs/reference/concepts/inheritance-and-templates))
- Understanding of environment files (see [Environments](/hytale-modding-docs/reference/world-and-environment/environments))
- Understanding of NPC spawn rules (see [NPC Spawn Rules](/hytale-modding-docs/reference/npc-system/npc-spawn-rules))

---

## How World Generation Works

Hytale's world generator uses a layered config system stored in `Assets/Server/HytaleGenerator/`. The generator processes terrain in stages:

1. **Zone selection** — the world is divided into zones (Zone 1 through Zone 4) based on distance from spawn
2. **Biome assignment** — each chunk within a zone is assigned a biome based on weighted selection
3. **Terrain shaping** — noise functions generate elevation, caves, and surface features
4. **Block placement** — surface blocks, subsurface layers, and ore veins are placed
5. **Structure generation** — prefab structures (villages, ruins, dungeons) are placed according to rules
6. **Environment assignment** — each biome receives an environment file controlling weather
7. **NPC spawning** — spawn rules tied to environments populate the world with NPCs

### Generator File Structure

```
Assets/Server/HytaleGenerator/
  WorldGenerator.json          (top-level config: zone boundaries, seed settings)
  Zones/
    Zone1/
      Zone1_Config.json        (biome list, structure rules for Zone 1)
      Biomes/
        Forest.json            (terrain shape, block palette, ore distribution)
        Mountains.json
        Plains.json
      Structures/
        Village.json           (structure placement rules)
        Ruins.json
    Zone2/
      ...
  OreDistribution/
    Default.json               (global ore vein settings)
  StructureRules/
    Placement.json             (spacing and density constraints)
```

---

## Step 1: Understand the Zone Config

Zone configs define the biomes available in a zone and their relative weights. The generator picks a biome for each chunk based on these weights.

Here is the structure of a zone config:

```json
{
  "Biomes": [
    {
      "Id": "Forest",
      "Weight": 40,
      "Environment": "Env_Zone1_Forests",
      "MinDistanceFromSpawn": 0,
      "MaxDistanceFromSpawn": -1
    },
    {
      "Id": "Mountains",
      "Weight": 20,
      "Environment": "Env_Zone1_Mountains",
      "MinDistanceFromSpawn": 100,
      "MaxDistanceFromSpawn": -1
    },
    {
      "Id": "Plains",
      "Weight": 30,
      "Environment": "Env_Zone1",
      "MinDistanceFromSpawn": 0,
      "MaxDistanceFromSpawn": -1
    }
  ],
  "Structures": [
    {
      "Id": "Village_Small",
      "Weight": 5,
      "BiomeFilter": ["Forest", "Plains"],
      "MinSpacing": 500,
      "MaxPerZone": 10
    }
  ]
}
```

### Biome entry fields

| Field | Type | Description |
|-------|------|-------------|
| `Id` | string | Unique biome identifier, references a biome definition file |
| `Weight` | number | Relative probability of this biome being selected. Higher = more common |
| `Environment` | string | Environment file ID controlling weather in this biome |
| `MinDistanceFromSpawn` | number | Minimum block distance from world spawn before this biome can appear. `0` = no minimum |
| `MaxDistanceFromSpawn` | number | Maximum distance. `-1` = no limit |

### Structure entry fields

| Field | Type | Description |
|-------|------|-------------|
| `Id` | string | Structure prefab identifier |
| `Weight` | number | Relative placement frequency |
| `BiomeFilter` | string[] | Which biomes this structure can appear in |
| `MinSpacing` | number | Minimum block distance between instances of this structure |
| `MaxPerZone` | number | Maximum number of this structure in the entire zone |

---

## Step 2: Create a Custom Biome

Define a new biome with unique terrain and block properties. Biome files control the noise parameters that shape terrain, the surface block palette, and the ore veins generated underground.

Create `YourMod/Assets/Server/HytaleGenerator/Zones/Zone1/Biomes/CrystalGrove.json`:

```json
{
  "Id": "CrystalGrove",
  "TerrainShape": {
    "BaseHeight": 72,
    "HeightVariation": 18,
    "NoiseScale": 0.02,
    "NoiseOctaves": 4,
    "Roughness": 0.45
  },
  "SurfaceBlocks": {
    "TopBlock": "Block_Grass_Azure",
    "FillerBlock": "Block_Dirt",
    "FillerDepth": 4,
    "StoneBlock": "Block_Stone"
  },
  "Features": {
    "Trees": {
      "Density": 0.15,
      "Types": [
        { "Id": "Tree_Azure_Medium", "Weight": 60 },
        { "Id": "Tree_Azure_Large", "Weight": 25 },
        { "Id": "Tree_Azure_Small", "Weight": 15 }
      ]
    },
    "Vegetation": {
      "Density": 0.3,
      "Types": [
        { "Id": "Plant_Fern_Azure", "Weight": 40 },
        { "Id": "Plant_Flower_Crystal", "Weight": 30 },
        { "Id": "Plant_Mushroom_Glow", "Weight": 30 }
      ]
    }
  },
  "OreOverrides": [
    {
      "OreId": "Ore_Crystal",
      "VeinSize": [3, 8],
      "HeightRange": [20, 60],
      "Frequency": 12
    },
    {
      "OreId": "Ore_Copper",
      "VeinSize": [2, 6],
      "HeightRange": [10, 50],
      "Frequency": 8
    }
  ],
  "CaveSettings": {
    "Frequency": 0.6,
    "MinHeight": 5,
    "MaxHeight": 55,
    "CaveWidth": [3, 7]
  }
}
```

### Terrain shape fields

| Field | Purpose |
|-------|---------|
| `BaseHeight` | Average terrain elevation in blocks. Vanilla forests use ~64-72 |
| `HeightVariation` | Maximum deviation from base height. Higher = hillier terrain |
| `NoiseScale` | Controls the frequency of terrain features. Lower = smoother, larger features |
| `NoiseOctaves` | Number of noise layers combined. More octaves = more detail |
| `Roughness` | Surface roughness multiplier. 0 = perfectly smooth, 1 = very rough |

### Ore override fields

| Field | Purpose |
|-------|---------|
| `OreId` | Block ID of the ore to generate |
| `VeinSize` | `[min, max]` number of blocks per ore vein |
| `HeightRange` | `[min, max]` Y-level range where veins can spawn |
| `Frequency` | Number of vein attempts per chunk. Higher = more ore |

---

## Step 3: Create the Biome Environment

Create an environment file for the Crystal Grove with a mystical atmosphere that features frequent fog and occasional azure-tinted weather.

Create `YourMod/Assets/Server/Environments/Zone1/Env_Zone1_CrystalGrove.json`:

```json
{
  "WaterTint": "#2a7bc4",
  "SpawnDensity": 0.6,
  "Tags": {
    "Zone1": [],
    "CrystalGrove": []
  },
  "WeatherForecasts": {
    "0":  [
      { "WeatherId": "Zone1_Sunny",       "Weight": 30 },
      { "WeatherId": "Zone1_Foggy_Light", "Weight": 40 },
      { "WeatherId": "Zone1_Cloudy_Medium", "Weight": 30 }
    ],
    "4":  [
      { "WeatherId": "Zone1_Foggy_Light", "Weight": 60 },
      { "WeatherId": "Zone1_Sunny",       "Weight": 30 },
      { "WeatherId": "Zone1_Rain_Light",  "Weight": 10 }
    ],
    "8":  [
      { "WeatherId": "Zone1_Sunny",       "Weight": 50 },
      { "WeatherId": "Zone1_Foggy_Light", "Weight": 30 },
      { "WeatherId": "Zone1_Rain_Light",  "Weight": 20 }
    ],
    "12": [
      { "WeatherId": "Zone1_Sunny",         "Weight": 60 },
      { "WeatherId": "Zone1_Cloudy_Medium",  "Weight": 30 },
      { "WeatherId": "Zone1_Rain_Light",    "Weight": 10 }
    ],
    "16": [
      { "WeatherId": "Zone1_Sunny",       "Weight": 40 },
      { "WeatherId": "Zone1_Foggy_Light", "Weight": 40 },
      { "WeatherId": "Zone1_Rain_Light",  "Weight": 20 }
    ],
    "18": [
      { "WeatherId": "Zone1_Sunny_Fireflies", "Weight": 50 },
      { "WeatherId": "Zone1_Foggy_Light",     "Weight": 40 },
      { "WeatherId": "Zone1_Sunny",           "Weight": 10 }
    ],
    "20": [
      { "WeatherId": "Zone1_Sunny_Fireflies", "Weight": 60 },
      { "WeatherId": "Zone1_Foggy_Light",     "Weight": 30 },
      { "WeatherId": "Zone1_Sunny",           "Weight": 10 }
    ],
    "22": [
      { "WeatherId": "Zone1_Foggy_Light",   "Weight": 50 },
      { "WeatherId": "Zone1_Sunny",         "Weight": 30 },
      { "WeatherId": "Zone1_Cloudy_Medium", "Weight": 20 }
    ]
  }
}
```

Notice the heavy fog weighting — this creates a mystical atmosphere where fog appears about 40-60% of the time, especially at dawn and dusk. The `Sunny_Fireflies` weather appears only in evening hours (18-21), matching the vanilla Zone 1 pattern.

---

## Step 4: Register the Biome in the Zone Config

To add your biome to Zone 1's generation, create an override zone config that adds the Crystal Grove to the biome list.

Create `YourMod/Assets/Server/HytaleGenerator/Zones/Zone1/Zone1_Config.json`:

```json
{
  "Biomes": [
    {
      "Id": "CrystalGrove",
      "Weight": 15,
      "Environment": "Env_Zone1_CrystalGrove",
      "MinDistanceFromSpawn": 200,
      "MaxDistanceFromSpawn": -1
    }
  ],
  "Structures": [
    {
      "Id": "Ruins_CrystalShrine",
      "Weight": 3,
      "BiomeFilter": ["CrystalGrove"],
      "MinSpacing": 800,
      "MaxPerZone": 3
    }
  ]
}
```

A weight of 15 makes the Crystal Grove relatively uncommon (compare to Forest at 40). Setting `MinDistanceFromSpawn: 200` prevents it from appearing right at the world spawn, creating a sense of discovery.

---

## Step 5: Create Biome-Specific NPC Spawns

Add unique NPC spawns tied to the Crystal Grove environment. This follows the same spawn rule pattern used in the overworld but references your custom environment.

Create `YourMod/Assets/Server/NPC/Spawn/World/Zone1/Spawns_Zone1_CrystalGrove.json`:

```json
{
  "Environments": [
    "Env_Zone1_CrystalGrove"
  ],
  "NPCs": [
    {
      "Weight": 5,
      "SpawnBlockSet": "Soil",
      "Id": "Gecko",
      "Flock": "One_Or_Two"
    },
    {
      "Weight": 3,
      "SpawnBlockSet": "Soil",
      "Id": "Frog_Green",
      "Flock": "Group_Small"
    }
  ],
  "DayTimeRange": [6, 18]
}
```

Add a separate nighttime spawn file for nocturnal creatures:

Create `YourMod/Assets/Server/NPC/Spawn/World/Zone1/Spawns_Zone1_CrystalGrove_Night.json`:

```json
{
  "Environments": [
    "Env_Zone1_CrystalGrove"
  ],
  "NPCs": [
    {
      "Weight": 4,
      "SpawnBlockSet": "Soil",
      "Id": "Bat",
      "Flock": "Group_Small"
    }
  ],
  "DayTimeRange": [20, 6]
}
```

---

## Step 6: Define Structure Placement Rules

Structures are prefab buildings or ruins placed during world generation. Define a Crystal Shrine structure that only appears in your biome.

Create `YourMod/Assets/Server/HytaleGenerator/StructureRules/Ruins_CrystalShrine.json`:

```json
{
  "Id": "Ruins_CrystalShrine",
  "PrefabId": "Prefab_CrystalShrine",
  "Placement": {
    "SurfaceSnap": true,
    "MinTerrainFlatness": 0.7,
    "ClearAbove": 10,
    "RotationMode": "Random90"
  },
  "LootContainers": [
    {
      "ContainerId": "Chest_CrystalShrine",
      "DropTable": "SunkenVault_Chest",
      "MaxPerStructure": 2
    }
  ],
  "NPCSpawners": [
    {
      "RoleId": "SunkenVault_Guardian",
      "Count": [1, 3],
      "SpawnRadius": 8
    }
  ]
}
```

### Placement fields

| Field | Purpose |
|-------|---------|
| `SurfaceSnap` | Aligns the structure to terrain surface height |
| `MinTerrainFlatness` | Minimum flatness score (0-1) required at the placement site. Higher = flatter terrain needed |
| `ClearAbove` | Minimum blocks of clearance above the structure footprint |
| `RotationMode` | How the structure is rotated: `Random90` picks 0/90/180/270 degrees randomly |

---

## Step 7: Test Your World Generation

1. Place your mod folder in the server mods directory.
2. Start the server with a **new world seed** — existing worlds will not regenerate chunks that have already been loaded.
3. Travel at least 200 blocks from spawn (your `MinDistanceFromSpawn` setting).
4. Look for the Crystal Grove biome — azure grass and crystal vegetation.
5. Verify NPC spawns match your spawn rules (geckos and frogs during the day, bats at night).
6. Search for Crystal Shrine structures within the biome.

### Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| Biome never appears | Weight too low or distance requirement too high | Increase `Weight` to 25+ for testing, or lower `MinDistanceFromSpawn` to 0 |
| Wrong weather in biome | Environment ID mismatch | Verify zone config `Environment` field matches your environment filename |
| No custom ores underground | Ore override not applied | Confirm `OreOverrides` uses valid block IDs that exist in the block registry |
| Structure floating above terrain | `SurfaceSnap` not set | Set `"SurfaceSnap": true` in placement rules |
| Structure spawning in water | No water check | Add `"AvoidWater": true` to placement rules |
| Existing world unchanged | Chunks already generated | Create a new world — the generator only runs for unvisited chunks |

---

## Complete File Listing

```
YourMod/
  Assets/
    Server/
      HytaleGenerator/
        Zones/
          Zone1/
            Zone1_Config.json
            Biomes/
              CrystalGrove.json
        StructureRules/
          Ruins_CrystalShrine.json
      Environments/
        Zone1/
          Env_Zone1_CrystalGrove.json
      NPC/
        Spawn/
          World/
            Zone1/
              Spawns_Zone1_CrystalGrove.json
              Spawns_Zone1_CrystalGrove_Night.json
```

---

## Next Steps

- [Custom Dungeons](/hytale-modding-docs/tutorials/advanced/custom-dungeons) — place dungeon portals inside generated structures
- [NPC AI Behavior Trees](/hytale-modding-docs/tutorials/advanced/npc-ai-behavior-trees) — create unique AI for biome-specific NPCs
- [Environments](/hytale-modding-docs/reference/world-and-environment/environments) — full weather schedule reference
- [NPC Spawn Rules](/hytale-modding-docs/reference/npc-system/npc-spawn-rules) — spawn rule format details
- [Weather System](/hytale-modding-docs/reference/world-and-environment/weather-system) — weather definition parameters
