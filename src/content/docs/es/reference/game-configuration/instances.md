---
title: Instancias
description: Referencia de los archivos de configuración de instancias en Hytale, que definen mundos autocontenidos con puntos de aparición, generación de mundo, modos de juego, comportamiento de NPCs, almacenamiento de chunks y UI de descubrimiento.
---

## Descripción General

Los archivos de configuración de instancias definen mundos autocontenidos en los que los jugadores pueden entrar — las zonas del mundo principal, instancias de mazmorras, hubs creativos y destinos de portales. Cada instancia tiene un `config.json` que especifica la semilla del mundo, el punto de aparición, el tipo de generación de mundo, el modo de juego y una amplia variedad de opciones de jugabilidad (PvP, daño por caída, aparición de NPCs, tick de bloques, etc.). Las instancias también configuran su backend de almacenamiento de chunks, ajustes de plugins y una UI de descubrimiento opcional que muestra una tarjeta de título cuando los jugadores entran.

Los directorios de instancias también contienen una carpeta `resources/` con archivos de estado en tiempo de ejecución (por ejemplo, `InstanceData.json`, `Time.json`) que rastrean el estado persistente del mundo.

## Ubicación de Archivos

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

## Esquema

### config.json

| Campo | Tipo | Requerido | Predeterminado | Descripción |
|-------|------|-----------|----------------|-------------|
| `Version` | `number` | Sí | — | Versión del formato de configuración (actualmente `4`). |
| `UUID` | `object` | Sí | — | UUID binario que identifica esta instancia. Contiene los campos `$binary` y `$type`. |
| `DisplayName` | `string` | No | — | Nombre legible para la instancia (por ejemplo, `"the Crossroads"`). |
| `Seed` | `number` | Sí | — | Semilla de generación del mundo. |
| `SpawnProvider` | `SpawnProvider` | Sí | — | Configuración del punto de aparición. |
| `WorldGen` | `WorldGen` | Sí | — | Configuración de generación del mundo. |
| `WorldMap` | `WorldMap` | No | — | Configuración de visualización del mapa del mundo. |
| `ChunkStorage` | `ChunkStorage` | Sí | — | Backend para la persistencia de datos de chunks. |
| `ChunkConfig` | `object` | No | `{}` | Sobrecargas de configuración adicionales a nivel de chunk. |
| `IsTicking` | `boolean` | No | `false` | Si las actualizaciones de tick de entidades se ejecutan en esta instancia. |
| `IsBlockTicking` | `boolean` | No | `false` | Si las actualizaciones de tick de bloques se ejecutan (por ejemplo, crecimiento de cultivos, propagación del fuego). |
| `IsPvpEnabled` | `boolean` | No | `false` | Si el daño jugador contra jugador está habilitado. |
| `IsFallDamageEnabled` | `boolean` | No | `true` | Si se aplica daño por caída. |
| `IsGameTimePaused` | `boolean` | No | `false` | Si el reloj de día/noche del juego está congelado. |
| `GameTime` | `string` | No | — | Hora inicial del juego como marca de tiempo ISO 8601. |
| `ClientEffects` | `ClientEffects` | No | — | Sobrecargas visuales para el renderizado del sol, bloom y rayos de sol. |
| `RequiredPlugins` | `object` | No | `{}` | Mapa de IDs de plugins requeridos para esta instancia. |
| `GameMode` | `string` | No | — | Modo de juego: `"Creative"`, `"Adventure"`, `"Survival"`. |
| `IsSpawningNPC` | `boolean` | No | `true` | Si los NPCs aparecen naturalmente en esta instancia. |
| `IsSpawnMarkersEnabled` | `boolean` | No | `true` | Si los marcadores de aparición en prefabs están activos. |
| `IsAllNPCFrozen` | `boolean` | No | `false` | Cuando es `true`, todos los NPCs están congelados y no se mueven ni actúan. |
| `GameplayConfig` | `string` | No | `"Default"` | ID de la configuración de jugabilidad a utilizar. Hace referencia a un archivo en `GameplayConfigs/`. |
| `IsCompassUpdating` | `boolean` | No | `true` | Si la UI de la brújula se actualiza en esta instancia. |
| `IsSavingPlayers` | `boolean` | No | `true` | Si el estado del jugador se guarda cuando sale. |
| `IsSavingChunks` | `boolean` | No | `true` | Si los chunks modificados se guardan en el almacenamiento. |
| `SaveNewChunks` | `boolean` | No | `true` | Si los chunks recién generados se guardan. |
| `IsUnloadingChunks` | `boolean` | No | `true` | Si los chunks se descargan cuando no hay jugadores cerca. |
| `IsObjectiveMarkersEnabled` | `boolean` | No | `true` | Si los marcadores de objetivos son visibles. |
| `DeleteOnUniverseStart` | `boolean` | No | `false` | Si esta instancia se elimina cuando el universo se reinicia. |
| `DeleteOnRemove` | `boolean` | No | `false` | Si los datos de la instancia se eliminan cuando se retira la instancia. |
| `ResourceStorage` | `ResourceStorage` | No | — | Backend para la persistencia de datos de recursos. |
| `Plugin` | `PluginConfig` | No | — | Ajustes específicos de plugins, incluyendo la UI de descubrimiento de la instancia. |

### SpawnProvider

| Campo | Tipo | Requerido | Predeterminado | Descripción |
|-------|------|-----------|----------------|-------------|
| `Id` | `string` | Sí | — | Tipo de proveedor de aparición: `"Global"` para un punto de aparición fijo en el mundo. |
| `SpawnPoint` | `SpawnPoint` | Sí | — | Coordenadas del mundo y rotación para la posición de aparición. |

### SpawnPoint

| Campo | Tipo | Requerido | Predeterminado | Descripción |
|-------|------|-----------|----------------|-------------|
| `X` | `number` | Sí | — | Coordenada X en bloques. |
| `Y` | `number` | Sí | — | Coordenada Y (vertical) en bloques. |
| `Z` | `number` | Sí | — | Coordenada Z en bloques. |
| `Pitch` | `number` | No | `0` | Ángulo de inclinación de la cámara en grados. |
| `Yaw` | `number` | No | `0` | Ángulo de guiñada de la cámara en grados. |
| `Roll` | `number` | No | `0` | Ángulo de alabeo de la cámara en grados. |

### WorldGen

| Campo | Tipo | Requerido | Predeterminado | Descripción |
|-------|------|-----------|----------------|-------------|
| `Type` | `string` | Sí | — | Tipo de generador: `"Hytale"` (heredado), `"HytaleGenerator"` (grafo de nodos). |
| `Name` | `string` | No | — | Nombre del perfil de generación de mundo (usado con el tipo `"Hytale"`). |
| `Environment` | `string` | No | — | ID de entorno para este mundo (usado con el tipo `"Hytale"`). |
| `WorldStructure` | `string` | No | — | Nombre de la estructura del mundo (usado con el tipo `"HytaleGenerator"`). |

### WorldMap

| Campo | Tipo | Requerido | Predeterminado | Descripción |
|-------|------|-----------|----------------|-------------|
| `Type` | `string` | Sí | — | `"WorldGen"` (muestra mapa de biomas), `"Disabled"` (sin mapa). |

### ClientEffects

| Campo | Tipo | Requerido | Predeterminado | Descripción |
|-------|------|-----------|----------------|-------------|
| `SunHeightPercent` | `number` | No | — | Sobrecarga de la altura del sol como porcentaje. |
| `SunAngleDegrees` | `number` | No | — | Sobrecarga del ángulo del sol en grados. |
| `BloomIntensity` | `number` | No | — | Intensidad del bloom de post-procesado. |
| `BloomPower` | `number` | No | — | Exponente de potencia del bloom. |
| `SunIntensity` | `number` | No | — | Multiplicador de intensidad de la luz solar. |
| `SunshaftIntensity` | `number` | No | — | Intensidad de los rayos de sol. |
| `SunshaftScaleFactor` | `number` | No | — | Factor de escala de los rayos de sol. |

### Discovery (Plugin.Instance.Discovery)

| Campo | Tipo | Requerido | Predeterminado | Descripción |
|-------|------|-----------|----------------|-------------|
| `TitleKey` | `string` | Sí | — | Clave de localización para el título mostrado al entrar. |
| `SubtitleKey` | `string` | No | — | Clave de localización para el subtítulo. |
| `Display` | `boolean` | No | `true` | Si la tarjeta de descubrimiento se muestra. |
| `AlwaysDisplay` | `boolean` | No | `false` | Mostrar la tarjeta cada vez, no solo en la primera entrada. |
| `Icon` | `string` | No | — | Nombre del archivo de imagen del icono para la tarjeta de descubrimiento. |
| `Major` | `boolean` | No | `false` | Si es un descubrimiento mayor (tratamiento de UI más grande). |
| `Duration` | `number` | No | — | Segundos que se muestra la tarjeta de descubrimiento. |
| `FadeInDuration` | `number` | No | — | Segundos de la transición de aparición de la tarjeta. |
| `FadeOutDuration` | `number` | No | — | Segundos de la transición de desaparición de la tarjeta. |

### Instance Plugin Config

| Campo | Tipo | Requerido | Predeterminado | Descripción |
|-------|------|-----------|----------------|-------------|
| `RemovalConditions` | `array` | No | `[]` | Condiciones bajo las cuales esta instancia se elimina automáticamente. |
| `PreventReconnection` | `boolean` | No | `false` | Cuando es `true`, los jugadores no pueden reconectarse a esta instancia después de desconectarse. |
| `Discovery` | `Discovery` | No | — | Configuración de la UI de descubrimiento. |

## Ejemplos

**Creative Hub** (`Assets/Server/Instances/CreativeHub/config.json`, condensado):

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

**Movement Gym con sobrecargas visuales** (`Assets/Server/Instances/Movement_Gym/config.json`, condensado):

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

## Páginas Relacionadas

- [Gameplay Configs](/hytale-modding-docs/reference/game-configuration/gameplay-configs) — reglas de jugabilidad aplicadas dentro de las instancias
- [Portal Types](/hytale-modding-docs/reference/world-and-environment/portal-types) — definiciones de portales que conectan con IDs de instancias
- [World Generation](/hytale-modding-docs/reference/world-and-environment/world-generation) — pipeline del generador seleccionado por `WorldGen.Type`
- [Environments](/hytale-modding-docs/reference/world-and-environment/environments) — archivos de entorno referenciados por `WorldGen.Environment`
