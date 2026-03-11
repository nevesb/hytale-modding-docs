---
title: Environments
description: Reference for environment definitions in Hytale, which schedule weighted weather forecasts for each in-game hour across a zone or region.
---

## Overview

Environment files define the weather schedule for a region of the game world. Each file contains a `WeatherForecasts` map with 24 entries — one per in-game hour (0–23). At each hour the engine samples from the weighted list of weather IDs to determine what weather plays. Multiple environment files can exist for the same zone, representing seasonal or thematic variants.

## File Location

```
Assets/Server/Environments/
  Default.json
  ForgottenTemple.json
  CreativeHub.json
  Portal.json
  Legacy/
  Unique/
  Zone0/
  Zone1/
    Env_Zone1.json
    Env_Zone1_Autumn.json
    Env_Zone1_Azure.json
  Zone2/
  Zone3/
  Zone4/
```

## Schema

### Top-level

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `WeatherForecasts` | `object` | Yes | — | Map of hour strings (`"0"`–`"23"`) to arrays of `WeatherForecastEntry`. |
| `WaterTint` | `string` | No | — | Hex colour applied to water surfaces in this environment. |
| `SpawnDensity` | `number` | No | — | Multiplier for NPC spawn density in this environment. |
| `Tags` | `object` | No | — | Arbitrary key-value tag map used by other systems to identify this environment. |

### WeatherForecastEntry

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `WeatherId` | `string` | Yes | — | ID of the weather definition to potentially play at this hour. References a file in `Assets/Server/Weathers/`. |
| `Weight` | `number` | Yes | — | Relative probability this weather is selected. A weight of `0` disables the weather for that hour without removing the entry. |

## How Sampling Works

Each in-game hour the engine looks up the array at that hour key and performs a weighted random selection. Entries with `Weight: 0` are never chosen. The sum of all weights in an hour's array does not need to equal 100 — selection is proportional.

## Examples

**Zone 1 default environment** (`Assets/Server/Environments/Zone1/Env_Zone1.json`, condensed to hours 0, 4, 18–19):

```json
{
  "WaterTint": "#1983d9",
  "SpawnDensity": 0.5,
  "Tags": {
    "Zone1": []
  },
  "WeatherForecasts": {
    "0": [
      { "WeatherId": "Zone1_Foggy_Light",     "Weight": 0  },
      { "WeatherId": "Zone1_Sunny_Fireflies", "Weight": 0  },
      { "WeatherId": "Zone1_Storm",           "Weight": 1  },
      { "WeatherId": "Zone1_Sunny",           "Weight": 52 },
      { "WeatherId": "Zone1_Cloudy_Medium",   "Weight": 10 },
      { "WeatherId": "Zone1_Rain",            "Weight": 1  },
      { "WeatherId": "Zone1_Rain_Light",      "Weight": 2  }
    ],
    "4": [
      { "WeatherId": "Zone1_Foggy_Light",     "Weight": 30 },
      { "WeatherId": "Zone1_Sunny_Fireflies", "Weight": 0  },
      { "WeatherId": "Zone1_Storm",           "Weight": 1  },
      { "WeatherId": "Zone1_Sunny",           "Weight": 52 },
      { "WeatherId": "Zone1_Cloudy_Medium",   "Weight": 10 },
      { "WeatherId": "Zone1_Rain",            "Weight": 1  },
      { "WeatherId": "Zone1_Rain_Light",      "Weight": 2  }
    ],
    "18": [
      { "WeatherId": "Zone1_Foggy_Light",     "Weight": 0  },
      { "WeatherId": "Zone1_Sunny_Fireflies", "Weight": 20 },
      { "WeatherId": "Zone1_Storm",           "Weight": 1  },
      { "WeatherId": "Zone1_Sunny",           "Weight": 35 },
      { "WeatherId": "Zone1_Cloudy_Medium",   "Weight": 10 },
      { "WeatherId": "Zone1_Rain",            "Weight": 1  },
      { "WeatherId": "Zone1_Rain_Light",      "Weight": 2  }
    ],
    "19": [
      { "WeatherId": "Zone1_Sunny_Fireflies", "Weight": 40 },
      { "WeatherId": "Zone1_Sunny",           "Weight": 35 }
    ]
  }
}
```

Notice that `Zone1_Foggy_Light` has `Weight: 0` during the day (hours 0–2) but gains weight at dawn (hours 3–7), making fog a morning-only phenomenon. `Zone1_Sunny_Fireflies` only appears in the evening hours 18–21.

**Simple single-weather environment** (`Assets/Server/Environments/Default.json`, condensed):

```json
{
  "WeatherForecasts": {
    "0":  [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "1":  [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "23": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }]
  }
}
```

## Related Pages

- [Weather System](/hytale-modding-docs/reference/world-and-environment/weather-system) — weather file format with sky, cloud, and fog parameters
- [Farming & Coops](/hytale-modding-docs/reference/economy-and-progression/farming-coops) — weather IDs used in Water modifier conditions
- [Gameplay Configs](/hytale-modding-docs/reference/game-configuration/gameplay-configs) — day/night duration that drives hour progression
