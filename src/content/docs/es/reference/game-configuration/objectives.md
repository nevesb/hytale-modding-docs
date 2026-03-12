---
title: Objetivos
description: Referencia de las definiciones de objetivos en Hytale, que cubren objetivos de misiones basados en tareas, líneas de objetivos, marcadores de ubicación y recompensas por completar.
---

## Descripción General

El sistema de objetivos impulsa la jugabilidad tipo misiones a través de cuatro tipos de archivo: **Objectives** definen conjuntos de tareas secuenciales y recompensas por completar, **ObjectiveLines** agrupan objetivos en una cadena de progresión, **ObjectiveLocationMarkers** colocan disparadores de área que activan objetivos cuando los jugadores entran, y **ReachLocationMarkers** definen puntos de referencia con nombre utilizados por las tareas de llegar a una ubicación. Las tareas soportan los tipos matar, recolectar, fabricar, recompensa, mapa del tesoro, usar bloque, usar entidad y llegar a ubicación.

## Ubicación de Archivos

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

## Esquema

### Objective

| Campo | Tipo | Requerido | Predeterminado | Descripción |
|-------|------|-----------|----------------|-------------|
| `TaskSets` | `TaskSet[]` | Sí | — | Array ordenado de conjuntos de tareas. Cada conjunto debe completarse antes de que el siguiente se active. |
| `Completions` | `Completion[]` | No | `[]` | Recompensas o acciones que se activan cuando todos los conjuntos de tareas están terminados. |
| `RemoveOnItemDrop` | `boolean` | No | `false` | Cuando es `true`, el objetivo se elimina si el jugador suelta su objeto asociado. |

### TaskSet

| Campo | Tipo | Requerido | Predeterminado | Descripción |
|-------|------|-----------|----------------|-------------|
| `Tasks` | `Task[]` | Sí | — | Array de tareas dentro de este conjunto. Todas las tareas deben completarse para avanzar al siguiente conjunto. |

### Task

| Campo | Tipo | Requerido | Predeterminado | Descripción |
|-------|------|-----------|----------------|-------------|
| `Type` | `string` | Sí | — | Tipo de tarea. Ver tipos de tarea a continuación. |
| `Count` | `number` | No | `1` | Número de veces que la acción debe realizarse. |
| `ItemId` | `string` | No | — | ID del objeto para tareas de fabricación o relacionadas con objetos. |
| `NPCGroupId` | `string` | No | — | ID del grupo de NPCs para tareas de matar. |
| `NpcId` | `string` | No | — | ID específico del NPC para tareas de recompensa. |
| `TaskId` | `string` | No | — | Identificador de la tarea para tareas de usar entidad. |
| `AnimationIdToPlay` | `string` | No | — | Animación a reproducir en la entidad objetivo durante tareas de usar entidad. |
| `BlockTagOrItemId` | `BlockTagOrItemId` | No | — | Filtro de etiqueta de bloque o ID de objeto para tareas de recolección y uso de bloque. |
| `TargetLocation` | `string` | No | — | Nombre del marcador de ubicación para tareas de llegar a ubicación. |
| `WorldLocationCondition` | `WorldLocationCondition` | No | — | Restricciones espaciales para tareas de recompensa y mapa del tesoro. |
| `SpawnBeacons` | `SpawnBeacon[]` | No | — | Definiciones de balizas de aparición para tareas de matar-baliza-de-aparición. |
| `Chests` | `TreasureChest[]` | No | — | Definiciones de cofres para tareas de mapa del tesoro. |
| `TaskConditions` | `TaskCondition[]` | No | `[]` | Condiciones adicionales que deben cumplirse para que la tarea cuente. |

### Tipos de Tarea

| Tipo | Descripción | Campos Clave |
|------|-------------|--------------|
| `KillNPC` | Matar una cantidad de NPCs de un grupo | `NPCGroupId`, `Count` |
| `KillSpawnBeacon` | Matar NPCs generados por balizas específicas | `NPCGroupId`, `Count`, `SpawnBeacons` |
| `Gather` | Recolectar objetos o bloques que coincidan con un filtro | `BlockTagOrItemId`, `Count` |
| `Craft` | Fabricar un objeto específico | `ItemId`, `Count` |
| `UseBlock` | Interactuar con un tipo de bloque específico | `BlockTagOrItemId`, `Count`, `TaskConditions` |
| `UseEntity` | Interactuar con un NPC o entidad | `TaskId`, `Count`, `AnimationIdToPlay` |
| `ReachLocation` | Viajar a un punto de referencia con nombre | `TargetLocation` |
| `Bounty` | Cazar un NPC específico dentro de un radio | `NpcId`, `WorldLocationCondition` |
| `TreasureMap` | Encontrar y abrir cofres del tesoro | `Chests` |

### BlockTagOrItemId

| Campo | Tipo | Requerido | Predeterminado | Descripción |
|-------|------|-----------|----------------|-------------|
| `ItemId` | `string` | No | — | ID específico del objeto a coincidir. |
| `BlockTag` | `string` | No | — | Etiqueta de bloque a coincidir (coincide con cualquier bloque que tenga esta etiqueta). |

### WorldLocationCondition

| Campo | Tipo | Requerido | Predeterminado | Descripción |
|-------|------|-----------|----------------|-------------|
| `Type` | `string` | Sí | — | `"LocationRadius"` o `"LookBlocksBelow"`. |
| `MinRadius` | `number` | No | — | Distancia mínima desde el dador del objetivo. |
| `MaxRadius` | `number` | No | — | Distancia máxima desde el dador del objetivo. |
| `BlockTags` | `string[]` | No | — | Etiquetas de bloque a verificar debajo de la ubicación objetivo (para `"LookBlocksBelow"`). |
| `Count` | `number` | No | — | Número de bloques a verificar debajo. |
| `MinRange` | `number` | No | — | Rango mínimo de profundidad para la verificación de bloques. |
| `MaxRange` | `number` | No | — | Rango máximo de profundidad para la verificación de bloques. |

### TreasureChest

| Campo | Tipo | Requerido | Predeterminado | Descripción |
|-------|------|-----------|----------------|-------------|
| `MinRadius` | `number` | Sí | — | Distancia mínima de colocación desde el jugador. |
| `MaxRadius` | `number` | Sí | — | Distancia máxima de colocación desde el jugador. |
| `DropList` | `string` | Sí | — | ID de la lista de botín para el contenido del cofre. |
| `WorldLocationCondition` | `WorldLocationCondition` | No | — | Restricciones de terreno para la colocación del cofre. |
| `ChestBlockTypeKey` | `string` | Sí | — | Tipo de bloque utilizado para el cofre del tesoro. |

### TaskCondition

| Campo | Tipo | Requerido | Predeterminado | Descripción |
|-------|------|-----------|----------------|-------------|
| `Type` | `string` | Sí | — | Tipo de condición: `"SoloInventory"`. |
| `BlockTagOrItemId` | `BlockTagOrItemId` | No | — | Objeto o bloque que el jugador debe poseer. |
| `Quantity` | `number` | No | — | Cantidad requerida del objeto. |

### Completion

| Campo | Tipo | Requerido | Predeterminado | Descripción |
|-------|------|-----------|----------------|-------------|
| `Type` | `string` | Sí | — | Acción de completar: `"GiveItems"` o `"ClearObjectiveItems"`. |
| `DropList` | `string` | No | — | ID de la lista de botín para recompensas de objetos (cuando `Type` es `"GiveItems"`). |

### ObjectiveLine

| Campo | Tipo | Requerido | Predeterminado | Descripción |
|-------|------|-----------|----------------|-------------|
| `ObjectiveIds` | `string[]` | Sí | — | Array ordenado de IDs de objetivos a presentar en secuencia. |

### ObjectiveLocationMarker

| Campo | Tipo | Requerido | Predeterminado | Descripción |
|-------|------|-----------|----------------|-------------|
| `Setup` | `MarkerSetup` | Sí | — | Qué sucede cuando un jugador entra en el área del marcador. |
| `Area` | `MarkerArea` | Sí | — | Definición espacial de la zona de activación. |
| `TriggerConditions` | `TriggerCondition[]` | No | `[]` | Condiciones adicionales que deben cumplirse para que el marcador se active. |

### MarkerSetup

| Campo | Tipo | Requerido | Predeterminado | Descripción |
|-------|------|-----------|----------------|-------------|
| `Type` | `string` | Sí | — | Tipo de configuración: `"Objective"`. |
| `ObjectiveId` | `string` | Sí | — | ID del objetivo a activar. |

### MarkerArea

| Campo | Tipo | Requerido | Predeterminado | Descripción |
|-------|------|-----------|----------------|-------------|
| `Type` | `string` | Sí | — | Tipo de área: `"Radius"`. |
| `EntryRadius` | `number` | Sí | — | Distancia en bloques a la que el marcador se activa. |
| `ExitRadius` | `number` | Sí | — | Distancia en bloques a la que el marcador se desactiva. Debe ser mayor que `EntryRadius` para evitar parpadeo. |

### TriggerCondition

| Campo | Tipo | Requerido | Predeterminado | Descripción |
|-------|------|-----------|----------------|-------------|
| `Type` | `string` | Sí | — | Tipo de condición: `"HourRange"` o `"Weather"`. |
| `MinHour` | `number` | No | — | Hora de inicio para condiciones de rango horario. |
| `MaxHour` | `number` | No | — | Hora de fin para condiciones de rango horario. Se envuelve a medianoche. |
| `WeatherIds` | `string[]` | No | — | IDs de clima requeridos para condiciones de clima. |

### ReachLocationMarker

| Campo | Tipo | Requerido | Predeterminado | Descripción |
|-------|------|-----------|----------------|-------------|
| `Radius` | `number` | Sí | — | Distancia en bloques dentro de la cual se considera que el jugador ha llegado a la ubicación. |
| `Name` | `string` | Sí | — | Nombre de visualización para el marcador de punto de referencia. |

## Ejemplos

**Objetivo de matar** (`Assets/Server/Objective/Objectives/Objective_Kill.json`):

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

**Línea de objetivo del tutorial** (`Assets/Server/Objective/ObjectiveLines/ObjectiveLine_Tutorial.json`):

```json
{
  "ObjectiveIds": [
    "Objective_Tutorial"
  ]
}
```

**Marcador de ubicación con condiciones de activación** (`Assets/Server/Objective/ObjectiveLocationMarkers/ObjectiveLocationMarker_Trigger.json`):

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

**Objetivo de mapa del tesoro** (`Assets/Server/Objective/Objectives/Objective_TreasureMap.json`):

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

## Páginas Relacionadas

- [Gameplay Configs](/hytale-modding-docs/reference/game-configuration/gameplay-configs) — opción `IsObjectiveMarkersEnabled`
- [Instances](/hytale-modding-docs/reference/game-configuration/instances) — opción de marcadores de objetivos a nivel de instancia
- [Drop Tables](/hytale-modding-docs/reference/economy-and-progression/drop-tables) — listas de botín referenciadas por las recompensas de completar
- [Block Type Lists](/hytale-modding-docs/reference/game-configuration/block-type-lists) — etiquetas de bloque usadas en tareas de recolección y uso de bloque
