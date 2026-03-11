---
title: Time Schedules
description: How Hytale uses hourly time schedules for weather, spawning, and visual changes.
---

## Overview

Several Hytale systems use hourly schedules — arrays indexed by hour (0-23) — to vary behavior throughout the day/night cycle. Weather forecasts, sky colors, fog density, and NPC spawn windows all use this pattern.

## Schedule Format

Schedules use string keys `"0"` through `"23"` representing hours:

```json
{
  "WeatherForecasts": {
    "0": [{ "WeatherId": "Zone1_Clear_Night", "Weight": 100 }],
    "6": [{ "WeatherId": "Zone1_Sunny", "Weight": 70 }, { "WeatherId": "Zone1_Cloudy", "Weight": 30 }],
    "12": [{ "WeatherId": "Zone1_Sunny", "Weight": 50 }, { "WeatherId": "Zone1_Rain", "Weight": 50 }],
    "18": [{ "WeatherId": "Zone1_Cloudy", "Weight": 100 }]
  }
}
```

## DayTimeRange

Spawn rules use a simpler `[start, end]` format:

```json
{
  "DayTimeRange": [6, 18]
}
```

This restricts spawning to hours 6:00 through 18:00 (daytime only).

## Hourly Color Arrays

Weather visuals use 24-element arrays for smooth transitions:

```json
{
  "SkyTopColors": [
    "#0a0a2e", "#0a0a2e", "#0a0a2e", "#0a0a2e", "#0a0a2e", "#1a1a4e",
    "#4a6ea0", "#6a9ec0", "#7ab0d0", "#7ab0d0", "#7ab0d0", "#7ab0d0",
    "#7ab0d0", "#7ab0d0", "#7ab0d0", "#7ab0d0", "#6a9ec0", "#4a6ea0",
    "#2a3e6e", "#1a1a4e", "#0a0a2e", "#0a0a2e", "#0a0a2e", "#0a0a2e"
  ]
}
```

Each element corresponds to one hour. The game interpolates between values for smooth transitions.

## Systems Using Time Schedules

| System | Format | Location |
|--------|--------|----------|
| Weather forecasts | Hourly weighted arrays | `Server/Environments/` |
| Sky/fog/sun colors | 24-element color arrays | `Server/Weathers/` |
| Cloud speeds | 24-element float arrays | `Server/Weathers/` |
| NPC spawning | `DayTimeRange` [start, end] | `Server/NPC/Spawn/` |
| Farm production | `ResidentRoamTime` [start, end] | `Server/Farming/Coops/` |

## Related Pages

- [Weather System](/hytale-modding-docs/reference/world-and-environment/weather-system/) — hourly visual properties
- [Environments](/hytale-modding-docs/reference/world-and-environment/environments/) — weather forecast schedules
- [NPC Spawn Rules](/hytale-modding-docs/reference/npc-system/npc-spawn-rules/) — DayTimeRange
