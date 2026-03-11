---
title: Weather System
description: Reference for weather definition files in Hytale, covering sky colours, cloud layers, fog, sun and moon visuals, and ambient particles.
---

## Overview

Weather files define the complete visual state of the sky for a named weather condition. All colour and scale properties use an array of time-keyed entries — the engine interpolates between keyframes as the in-game hour progresses. Cloud layers, fog density, sun/moon colours, and ambient particles are all controlled here. Weather IDs defined in these files are referenced by [environment forecast schedules](/hytale-modding-docs/reference/world-and-environment/environments).

## File Location

```
Assets/Server/Weathers/
  Blood_Moon.json
  Creative_Hub.json
  Forgotten_Temple.json
  Void.json
  Unique/
  Zone1/
    Cave_Deep.json
    Cave_Fog.json
    Cave_Goblin.json
    (Zone1_Sunny.json, Zone1_Rain.json, etc.)
  Zone2/
  Zone3/
  Zone4/
  Skylands/
  Minigames/
```

## Schema

### Top-level

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Stars` | `string` | No | — | Path to the star field texture rendered at night. |
| `Moons` | `MoonEntry[]` | No | — | Moon phase textures, one per day in the moon cycle. |
| `Clouds` | `CloudLayer[]` | No | — | Ordered list of cloud texture layers composited over the sky. |
| `SkyTopColors` | `HourColor[]` | No | — | Zenith sky colour keyframes. |
| `SkyBottomColors` | `HourColor[]` | No | — | Horizon sky colour keyframes. |
| `SkySunsetColors` | `HourColor[]` | No | — | Sunset/sunrise tint colour keyframes. |
| `FogColors` | `HourColor[]` | No | — | Fog colour keyframes. |
| `FogDensities` | `HourValue[]` | No | — | Fog density keyframes (0–1). |
| `FogHeightFalloffs` | `HourValue[]` | No | — | Fog height falloff keyframes. |
| `FogDistance` | `[number, number]` | No | — | `[near, far]` fog distance range in units. |
| `FogOptions` | `FogOptions` | No | — | Additional fog rendering options. |
| `SunColors` | `HourColor[]` | No | — | Sun disc colour keyframes. |
| `SunGlowColors` | `HourColor[]` | No | — | Sun glow halo colour keyframes. |
| `SunScales` | `HourValue[]` | No | — | Sun disc scale keyframes. |
| `MoonColors` | `HourColor[]` | No | — | Moon disc colour keyframes. |
| `MoonGlowColors` | `HourColor[]` | No | — | Moon glow halo colour keyframes. |
| `MoonScales` | `HourValue[]` | No | — | Moon disc scale keyframes. |
| `Particle` | `WeatherParticle` | No | — | Ambient particle system played during this weather (e.g. rain, snow, fireflies). |

### MoonEntry

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Day` | `number` | Yes | — | Day index in the moon cycle (0-based). |
| `Texture` | `string` | Yes | — | Path to the moon phase texture for this cycle day. |

### CloudLayer

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Texture` | `string` | Yes | — | Path to the cloud texture for this layer. |
| `Colors` | `HourColor[]` | Yes | — | RGBA colour keyframes controlling cloud visibility and tint over the day. |
| `Speeds` | `HourValue[]` | Yes | — | Scroll speed keyframes for this cloud layer. |

### HourColor

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Hour` | `number` | Yes | — | In-game hour (0–23) at which this colour applies. The engine interpolates between keyframes. |
| `Color` | `string` | Yes | — | Hex colour string, optionally with alpha (e.g. `"#ffffffe6"`, `"rgba(#2c6788, 1)"`). |

### HourValue

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Hour` | `number` | Yes | — | In-game hour (0–23). |
| `Value` | `number` | Yes | — | Numeric value at this hour (scale, density, speed, etc.). |

### FogOptions

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `FogHeightCameraFixed` | `number` | No | — | Locks the fog height plane relative to the camera rather than the world. |
| `EffectiveViewDistanceMultiplier` | `number` | No | `1.0` | Scales the effective view distance during this weather. |

### WeatherParticle

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `SystemId` | `string` | Yes | — | Particle system ID to play as ambient weather effect. |
| `OvergroundOnly` | `boolean` | No | `false` | If `true`, particles only spawn in above-ground areas. |
| `Color` | `string` | No | — | Hex tint colour applied to the particle system. |

## Example

**Zone 1 sunny weather** (`Assets/Server/Weathers/Zone1/Cave_Deep.json` — note this shows a cave weather variant; Zone1 main weathers follow the same schema):

```json
{
  "Stars": "Sky/Stars.png",
  "Moons": [
    { "Day": 0, "Texture": "Sky/MoonCycle/Moon_Full.png"     },
    { "Day": 1, "Texture": "Sky/MoonCycle/Moon_Gibbous.png"  },
    { "Day": 2, "Texture": "Sky/MoonCycle/Moon_Half.png"     },
    { "Day": 3, "Texture": "Sky/MoonCycle/Moon_Crescent.png" },
    { "Day": 4, "Texture": "Sky/MoonCycle/Moon_New.png"      }
  ],
  "Clouds": [
    {
      "Texture": "Sky/Clouds/Light_Base.png",
      "Colors": [
        { "Hour": 3,  "Color": "#1a1a1bc7" },
        { "Hour": 5,  "Color": "#ff5e4366" },
        { "Hour": 7,  "Color": "#ffffffe6" },
        { "Hour": 17, "Color": "#ffffffe6" },
        { "Hour": 19, "Color": "#ff5e4347" },
        { "Hour": 21, "Color": "#1a1a1bc7" }
      ],
      "Speeds": [
        { "Hour": 0, "Value": 0 }
      ]
    }
  ],
  "SkyTopColors": [
    { "Hour": 7,  "Color": "rgba(#2c6788, 1)" },
    { "Hour": 19, "Color": "rgba(#2c6788, 1)" },
    { "Hour": 5,  "Color": "rgba(#000000, 1)" },
    { "Hour": 21, "Color": "rgba(#030000, 1)" }
  ],
  "FogColors": [
    { "Hour": 7, "Color": "#14212e" }
  ],
  "SunColors": [
    { "Hour": 7,  "Color": "#ffffff"  },
    { "Hour": 17, "Color": "#ffffff"  },
    { "Hour": 18, "Color": "#fff7e3"  },
    { "Hour": 19, "Color": "#fec9ae"  },
    { "Hour": 5,  "Color": "#fec9ae"  }
  ],
  "MoonColors": [
    { "Hour": 3,  "Color": "#98aff2ff" },
    { "Hour": 5,  "Color": "#e5c0bcff" },
    { "Hour": 17, "Color": "#e5c0bcff" },
    { "Hour": 19, "Color": "#2241a16e" },
    { "Hour": 21, "Color": "#6e7aaac4" }
  ],
  "FogDistance": [-192, 128]
}
```

**Void weather with ambient particles** (`Assets/Server/Weathers/Void.json`, condensed):

```json
{
  "FogDistance": [-128.0, 512.0],
  "FogOptions": {
    "FogHeightCameraFixed": 0.5,
    "EffectiveViewDistanceMultiplier": 1.0
  },
  "Particle": {
    "SystemId": "Magic_Sparks_Heavy_GS",
    "OvergroundOnly": true,
    "Color": "#fd69a4"
  }
}
```

## Related Pages

- [Environments](/hytale-modding-docs/reference/world-and-environment/environments) — hourly weather forecast schedules that reference weather IDs
- [Farming & Coops](/hytale-modding-docs/reference/economy-and-progression/farming-coops) — weather IDs used in Water modifier conditions
