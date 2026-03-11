---
title: Portal Types
description: Reference for portal type definitions in Hytale, which configure the destination instance, UI description, loading screen, and gameplay rules for world portals.
---

## Overview

Portal type files define the configuration for portals that transport players between the overworld and instanced content. Each file specifies which instance the portal leads to, the display name and flavour text shown on the loading screen, a theme colour, splash artwork, and gameplay tips. An optional `VoidInvasionEnabled` flag controls whether void invasion events can occur inside the portal's destination.

## File Location

```
Assets/Server/PortalTypes/
  Hederas_Lair.json
  Henges.json
  Jungles.json
  Taiga.json
  Windsurf_Valley.json
```

## Schema

### Top-level

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `InstanceId` | `string` | Yes | — | ID of the destination instance. Must match an instance directory name under `Assets/Server/Instances/`. |
| `Description` | `Description` | Yes | — | UI metadata displayed on the loading screen and portal tooltip. |
| `VoidInvasionEnabled` | `boolean` | No | `false` | Whether void invasion events can trigger inside this portal's destination instance. |

### Description

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `DisplayName` | `string` | Yes | — | Localisation key for the portal's display name (e.g. `"server.portals.hederas_lair"`). |
| `FlavorText` | `string` | Yes | — | Localisation key for the descriptive flavour text shown below the title. |
| `ThemeColor` | `string` | Yes | — | Hex colour (with optional alpha) used for the loading screen accent and UI elements. |
| `SplashImage` | `string` | No | `"DefaultArtwork.png"` | Filename of the splash artwork displayed during loading. |
| `Tips` | `string[]` | No | `[]` | Array of localisation keys for gameplay tips shown on the loading screen. |

## Examples

**Hedera's Lair** (`Assets/Server/PortalTypes/Hederas_Lair.json`):

```json
{
  "InstanceId": "Portals_Hedera",
  "Description": {
    "DisplayName": "server.portals.hederas_lair",
    "FlavorText": "server.portals.hederas_lair.description",
    "ThemeColor": "#23970cec",
    "SplashImage": "DefaultArtwork.png",
    "Tips": [
      "server.portals.hederas_lair.tip1",
      "server.portals.hederas_lair.tip2"
    ]
  },
  "VoidInvasionEnabled": true
}
```

**Windsurf Valley** (`Assets/Server/PortalTypes/Windsurf_Valley.json`):

```json
{
  "InstanceId": "Portals_Oasis",
  "Description": {
    "DisplayName": "server.portals.oasis",
    "FlavorText": "server.portals.oasis.description",
    "ThemeColor": "#f3b33cec",
    "SplashImage": "DefaultArtwork.png",
    "Tips": [
      "server.portals.windsurf_valley.tip1"
    ]
  }
}
```

## Related Pages

- [Instances](/hytale-modding-docs/reference/game-configuration/instances) — instance definitions that portals connect to
- [Gameplay Configs](/hytale-modding-docs/reference/game-configuration/gameplay-configs) — gameplay rules applied inside portal destinations
- [Environments](/hytale-modding-docs/reference/world-and-environment/environments) — environment files used within portal instances
