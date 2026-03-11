---
title: Objectives
description: Reference for objective definitions in Hytale, covering task-based quest objectives, objective lines, location markers, and completion rewards.
---

## Overview

The objective system drives quest-like gameplay through four file types: **Objectives** define sequential task sets and completion rewards, **ObjectiveLines** group objectives into a progression chain, **ObjectiveLocationMarkers** place area triggers that activate objectives when players enter, and **ReachLocationMarkers** define named waypoints used by reach-location tasks. Tasks support kill, gather, craft, bounty, treasure map, use-block, use-entity, and reach-location types.

## File Location

```
Assets/Server/Objective/
  Objectives/
    Objective_Bounty.json
    Objective_Craft.json
    Objective_Gather.json
    Objective_Gameplay_Trailer.json
    Objective_Kill.json
    Objective_KillSpawnBeacon.json
    Objective_KillSpawnMarker.json
    Objective_ReachLocation.json
    Objective_TreasureMap.json
    Objective_Tutorial.json
    Objective_UseBlock.json
    Objective_UseEntity.json
  ObjectiveLines/
    ObjectiveLine_Test.json
    ObjectiveLine_Tutorial.json
  ObjectiveLocationMarkers/
    ObjectiveLocationMarker_Gameplay_Trailer.json
    ObjectiveLocationMarker_KillSpawnBeacon.json
    ObjectiveLocationMarker_Test.json
    ObjectiveLocationMarker_Trigger.json
  ReachLocationMarkers/
    ObjectiveReachMarker_Example.json
```

## Schema

### Objective

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `TaskSets` | `TaskSet[]` | Yes | — | Ordered array of task sets. Each set must be completed before the next becomes active. |
| `Completions` | `Completion[]` | No | `[]` | Rewards or actions triggered when all task sets are finished. |
| `RemoveOnItemDrop` | `boolean` | No | `false` | When `true`, the objective is removed if the player drops its associated item. |

### TaskSet

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Tasks` | `Task[]` | Yes | — | Array of tasks within this set. All tasks must be completed to advance to the next set. |

### Task

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Type` | `string` | Yes | — | Task type. See task types below. |
| `Count` | `number` | No | `1` | Number of times the action must be performed. |
| `ItemId` | `string` | No | — | Item ID for craft or item-related tasks. |
| `NPCGroupId` | `string` | No | — | NPC group ID for kill tasks. |
| `NpcId` | `string` | No | — | Specific NPC ID for bounty tasks. |
| `TaskId` | `string` | No | — | Task identifier for use-entity tasks. |
| `AnimationIdToPlay` | `string` | No | — | Animation to play on the target entity during use-entity tasks. |
| `BlockTagOrItemId` | `BlockTagOrItemId` | No | — | Block tag or item ID filter for gather and use-block tasks. |
| `TargetLocation` | `string` | No | — | Reach location marker name for reach-location tasks. |
| `WorldLocationCondition` | `WorldLocationCondition` | No | — | Spatial constraints for bounty and treasure map tasks. |
| `SpawnBeacons` | `SpawnBeacon[]` | No | — | Spawn beacon definitions for kill-spawn-beacon tasks. |
| `Chests` | `TreasureChest[]` | No | — | Chest definitions for treasure map tasks. |
| `TaskConditions` | `TaskCondition[]` | No | `[]` | Additional conditions that must be met for the task to count. |

### Task Types

| Type | Description | Key Fields |
|------|-------------|------------|
| `KillNPC` | Kill a number of NPCs from a group | `NPCGroupId`, `Count` |
| `KillSpawnBeacon` | Kill NPCs spawned by specific beacons | `NPCGroupId`, `Count`, `SpawnBeacons` |
| `Gather` | Collect items or blocks matching a filter | `BlockTagOrItemId`, `Count` |
| `Craft` | Craft a specific item | `ItemId`, `Count` |
| `UseBlock` | Interact with a specific block type | `BlockTagOrItemId`, `Count`, `TaskConditions` |
| `UseEntity` | Interact with an NPC or entity | `TaskId`, `Count`, `AnimationIdToPlay` |
| `ReachLocation` | Travel to a named waypoint | `TargetLocation` |
| `Bounty` | Hunt a specific NPC within a radius | `NpcId`, `WorldLocationCondition` |
| `TreasureMap` | Find and open treasure chests | `Chests` |

### BlockTagOrItemId

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `ItemId` | `string` | No | — | Specific item ID to match. |
| `BlockTag` | `string` | No | — | Block tag to match (matches any block with this tag). |

### WorldLocationCondition

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Type` | `string` | Yes | — | `"LocationRadius"` or `"LookBlocksBelow"`. |
| `MinRadius` | `number` | No | — | Minimum distance from the objective giver. |
| `MaxRadius` | `number` | No | — | Maximum distance from the objective giver. |
| `BlockTags` | `string[]` | No | — | Block tags to check below the target location (for `"LookBlocksBelow"`). |
| `Count` | `number` | No | — | Number of blocks to check below. |
| `MinRange` | `number` | No | — | Minimum depth range for block checking. |
| `MaxRange` | `number` | No | — | Maximum depth range for block checking. |

### TreasureChest

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `MinRadius` | `number` | Yes | — | Minimum placement distance from the player. |
| `MaxRadius` | `number` | Yes | — | Maximum placement distance from the player. |
| `DropList` | `string` | Yes | — | Drop list ID for chest contents. |
| `WorldLocationCondition` | `WorldLocationCondition` | No | — | Terrain constraints for chest placement. |
| `ChestBlockTypeKey` | `string` | Yes | — | Block type used for the treasure chest. |

### TaskCondition

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Type` | `string` | Yes | — | Condition type: `"SoloInventory"`. |
| `BlockTagOrItemId` | `BlockTagOrItemId` | No | — | Item or block the player must possess. |
| `Quantity` | `number` | No | — | Required quantity of the item. |

### Completion

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Type` | `string` | Yes | — | Completion action: `"GiveItems"` or `"ClearObjectiveItems"`. |
| `DropList` | `string` | No | — | Drop list ID for item rewards (when `Type` is `"GiveItems"`). |

### ObjectiveLine

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `ObjectiveIds` | `string[]` | Yes | — | Ordered array of objective IDs to present in sequence. |

### ObjectiveLocationMarker

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Setup` | `MarkerSetup` | Yes | — | What happens when a player enters the marker area. |
| `Area` | `MarkerArea` | Yes | — | Spatial definition of the trigger zone. |
| `TriggerConditions` | `TriggerCondition[]` | No | `[]` | Additional conditions that must be met for the marker to activate. |

### MarkerSetup

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Type` | `string` | Yes | — | Setup type: `"Objective"`. |
| `ObjectiveId` | `string` | Yes | — | ID of the objective to activate. |

### MarkerArea

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Type` | `string` | Yes | — | Area type: `"Radius"`. |
| `EntryRadius` | `number` | Yes | — | Distance in blocks at which the marker activates. |
| `ExitRadius` | `number` | Yes | — | Distance in blocks at which the marker deactivates. Must be greater than `EntryRadius` to prevent flicker. |

### TriggerCondition

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Type` | `string` | Yes | — | Condition type: `"HourRange"` or `"Weather"`. |
| `MinHour` | `number` | No | — | Start hour for hour-range conditions. |
| `MaxHour` | `number` | No | — | End hour for hour-range conditions. Wraps across midnight. |
| `WeatherIds` | `string[]` | No | — | Required weather IDs for weather conditions. |

### ReachLocationMarker

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Radius` | `number` | Yes | — | Distance in blocks within which the player is considered to have reached the location. |
| `Name` | `string` | Yes | — | Display name for the waypoint marker. |

## Examples

**Kill objective** (`Assets/Server/Objective/Objectives/Objective_Kill.json`):

```json
{
  "TaskSets": [
    {
      "Tasks": [
        {
          "Type": "KillNPC",
          "Count": 3,
          "NPCGroupId": "Trork_Warrior"
        }
      ]
    }
  ],
  "Completions": [
    {
      "Type": "GiveItems",
      "DropList": "Trork_Camp_Inventory"
    }
  ]
}
```

**Tutorial objective line** (`Assets/Server/Objective/ObjectiveLines/ObjectiveLine_Tutorial.json`):

```json
{
  "ObjectiveIds": [
    "Objective_Tutorial"
  ]
}
```

**Location marker with trigger conditions** (`Assets/Server/Objective/ObjectiveLocationMarkers/ObjectiveLocationMarker_Trigger.json`):

```json
{
  "Setup": {
    "Type": "Objective",
    "ObjectiveId": "Objective_Kill"
  },
  "Area": {
    "Type": "Radius",
    "EntryRadius": 25,
    "ExitRadius": 35
  },
  "TriggerConditions": [
    { "Type": "HourRange", "MinHour": 17, "MaxHour": 2 },
    { "Type": "Weather", "WeatherIds": ["Zone1_Cloudy_Medium"] }
  ]
}
```

**Treasure map objective** (`Assets/Server/Objective/Objectives/Objective_TreasureMap.json`):

```json
{
  "TaskSets": [
    {
      "Tasks": [
        {
          "Type": "TreasureMap",
          "Chests": [
            {
              "MinRadius": 10,
              "MaxRadius": 20,
              "DropList": "Zone1_Encounters_Tier3",
              "WorldLocationCondition": {
                "Type": "LookBlocksBelow",
                "BlockTags": ["Stone", "Soil"],
                "Count": 3,
                "MinRange": 0,
                "MaxRange": 5
              },
              "ChestBlockTypeKey": "Furniture_Ancient_Chest_Large"
            }
          ]
        }
      ]
    }
  ],
  "Completions": [
    { "Type": "ClearObjectiveItems" }
  ],
  "RemoveOnItemDrop": true
}
```

## Related Pages

- [Gameplay Configs](/hytale-modding-docs/reference/game-configuration/gameplay-configs) — `IsObjectiveMarkersEnabled` toggle
- [Instances](/hytale-modding-docs/reference/game-configuration/instances) — instance-level objective marker toggle
- [Drop Tables](/hytale-modding-docs/reference/economy-and-progression/drop-tables) — drop lists referenced by completion rewards
- [Block Type Lists](/hytale-modding-docs/reference/game-configuration/block-type-lists) — block tags used in gather and use-block tasks
