---
title: Configuraciones de Jugabilidad
description: Referencia de los archivos de configuracion de jugabilidad en Hytale, que controlan penalizaciones por muerte, durabilidad de objetos, duracion del ciclo dia/noche, configuracion del jugador, resistencia, reaparicion y mas.
---

## Descripcion General

Los archivos de configuracion de jugabilidad son los archivos de ajuste de nivel superior para un mundo o instancia. Soportan herencia a traves de un campo `Parent` — las configuraciones hijas solo anulan los campos que declaran, heredando todo lo demas del padre. La configuracion `Default.json` es la base para todos los mundos estandar; `Default_Instance.json` la extiende para contenido instanciado con diferentes reglas de muerte y edicion de mundo.

## Ubicacion de Archivos

```
Assets/Server/GameplayConfigs/
  Default.json
  Default_Instance.json
  CreativeHub.json
  ForgottenTemple.json
  Portal.json
```

## Esquema

### Nivel superior

| Campo | Tipo | Requerido | Por defecto | Descripcion |
|-------|------|-----------|-------------|-------------|
| `Parent` | `string` | No | — | ID de una configuracion padre de la cual heredar. Solo los campos anulados necesitan especificarse en el hijo. |
| `Gathering` | `GatheringConfig` | No | — | Ajustes para la retroalimentacion de recoleccion de bloques (bloques irrompibles, respuestas de herramienta incorrecta). |
| `Death` | `DeathConfig` | No | — | Controla lo que sucede con los objetos y la reaparicion al morir el jugador. |
| `ItemEntity` | `ItemEntityConfig` | No | — | Ajustes para entidades de objetos tirados en el mundo. |
| `ItemDurability` | `ItemDurabilityConfig` | No | — | Multiplicadores de penalizacion aplicados cuando la durabilidad del equipo llega a cero. |
| `Plugin` | `PluginConfig` | No | — | Configuracion de plugins de jugabilidad: Resistencia, Memorias. |
| `Respawn` | `RespawnConfig` | No | — | Reglas de punto de reaparicion. |
| `World` | `WorldConfig` | No | — | Duraciones del ciclo dia/noche y ajustes de interaccion con bloques. |
| `Player` | `PlayerConfig` | No | — | Ajustes de movimiento, hitbox y visibilidad de armadura. |
| `CameraEffects` | `CameraEffectsConfig` | No | — | Efectos visuales activados por tipos de dano. |
| `CreativePlaySoundSet` | `string` | No | — | Conjunto de sonidos usado durante la reproduccion en modo creativo. |
| `Spawn` | `SpawnConfig` | No | — | Efectos de particulas mostrados en la primera aparicion del jugador. |
| `Ping` | `PingConfig` | No | — | Ajustes de ping del mundo (duracion, enfriamiento, radio, sonido). |

### DeathConfig

| Campo | Tipo | Requerido | Por defecto | Descripcion |
|-------|------|-----------|-------------|-------------|
| `ItemsLossMode` | `"Configured" \| "None" \| "All"` | No | — | Determina que objetos se pierden al morir. `Configured` usa campos de porcentaje; `None` mantiene todos los objetos; `All` suelta todo. |
| `ItemsAmountLossPercentage` | `number` | No | — | Porcentaje de pilas de objetos perdidas al morir cuando `ItemsLossMode` es `"Configured"`. |
| `ItemsDurabilityLossPercentage` | `number` | No | — | Porcentaje de durabilidad del equipo perdida al morir. |
| `LoseItems` | `boolean` | No | — | Anulacion abreviada: `false` previene cualquier perdida de objetos independientemente de otros ajustes. |
| `RespawnController` | `object` | No | — | Comportamiento de reaparicion personalizado. `{ "Type": "ExitInstance" }` expulsa al jugador de una instancia al morir. |

### ItemEntityConfig

| Campo | Tipo | Requerido | Por defecto | Descripcion |
|-------|------|-----------|-------------|-------------|
| `Lifetime` | `number` | No | — | Segundos antes de que una entidad de objeto tirada desaparezca del mundo. |

### ItemDurabilityConfig

| Campo | Tipo | Requerido | Por defecto | Descripcion |
|-------|------|-----------|-------------|-------------|
| `BrokenPenalties` | `object` | No | — | Multiplicadores aplicados a las estadisticas de la entidad cuando cada categoria de equipo esta completamente rota. |
| `BrokenPenalties.Weapon` | `number` | No | — | Multiplicador de estadisticas cuando el arma equipada tiene cero durabilidad (por ejemplo, `0.75` = 25% de reduccion de estadisticas). |
| `BrokenPenalties.Armor` | `number` | No | — | Multiplicador de estadisticas cuando la armadura equipada esta completamente rota. |
| `BrokenPenalties.Tool` | `number` | No | — | Multiplicador de estadisticas cuando la herramienta equipada esta completamente rota. |

### PluginConfig

| Campo | Tipo | Requerido | Por defecto | Descripcion |
|-------|------|-----------|-------------|-------------|
| `Stamina` | `StaminaPlugin` | No | — | Ajustes del sistema de resistencia. |
| `Memories` | `MemoriesPlugin` | No | — | Ajustes del sistema de Memorias (XP). |
| `Weathers` | `object` | No | — | Anulaciones del plugin de clima. |

### StaminaPlugin

| Campo | Tipo | Requerido | Por defecto | Descripcion |
|-------|------|-----------|-------------|-------------|
| `SprintRegenDelay` | `object` | No | — | Configura como el sprint retrasa la regeneracion de resistencia. |
| `SprintRegenDelay.EntityStatId` | `string` | No | — | El ID de estadistica de entidad a modificar (por ejemplo, `"StaminaRegenDelay"`). |
| `SprintRegenDelay.Value` | `number` | No | — | Valor aplicado a la estadistica (valores negativos reducen el retraso de regeneracion). |

### MemoriesPlugin

| Campo | Tipo | Requerido | Por defecto | Descripcion |
|-------|------|-----------|-------------|-------------|
| `MemoriesAmountPerLevel` | `number[]` | No | — | Array de costos de memoria por subida de nivel, indexado por nivel (base 0). |
| `MemoriesRecordParticles` | `string` | No | — | Sistema de particulas reproducido cuando se registra una memoria en una estatua. |
| `MemoriesCatchItemId` | `string` | No | — | ID del objeto de la particula de memoria coleccionable en el mundo. |
| `MemoriesCatchEntityParticle` | `object` | No | — | Particula adjunta a la entidad al atrapar una memoria. |
| `MemoriesCatchParticleViewDistance` | `number` | No | — | Distancia de vision en unidades a la que las particulas de captura son visibles. |

### RespawnConfig

| Campo | Tipo | Requerido | Por defecto | Descripcion |
|-------|------|-----------|-------------|-------------|
| `RadiusLimitRespawnPoint` | `number` | No | — | Distancia maxima en unidades desde la ubicacion de muerte del jugador donde se puede usar un punto de reaparicion. |
| `MaxRespawnPointsPerPlayer` | `number` | No | — | Numero maximo de puntos de reaparicion activos que un jugador puede tener simultaneamente. |

### WorldConfig

| Campo | Tipo | Requerido | Por defecto | Descripcion |
|-------|------|-----------|-------------|-------------|
| `DaytimeDurationSeconds` | `number` | No | — | Segundos del mundo real para un periodo completo de dia. |
| `NighttimeDurationSeconds` | `number` | No | — | Segundos del mundo real para un periodo completo de noche. |
| `BlockPlacementFragilityTimer` | `number` | No | — | Segundos despues de la colocacion durante los cuales un bloque puede ser roto instantaneamente por quien lo coloco. `0` desactiva. |
| `AllowBlockBreaking` | `boolean` | No | — | Si los jugadores pueden romper bloques en este mundo. |
| `AllowBlockGathering` | `boolean` | No | — | Si los jugadores pueden recolectar recursos de bloques. |
| `Sleep` | `SleepConfig` | No | — | Configuracion del sistema de sueno. |

### SleepConfig

| Campo | Tipo | Requerido | Por defecto | Descripcion |
|-------|------|-----------|-------------|-------------|
| `WakeUpHour` | `number` | No | — | Hora del juego a la que los jugadores dormidos se despiertan. |
| `AllowedSleepHoursRange` | `[number, number]` | No | — | Rango de horas `[inicio, fin]` durante el cual los jugadores pueden irse a dormir. Se ajusta a traves de medianoche. |

### PlayerConfig

| Campo | Tipo | Requerido | Por defecto | Descripcion |
|-------|------|-----------|-------------|-------------|
| `MovementConfig` | `string` | No | — | ID de la configuracion de movimiento preestablecida para jugadores. |
| `HitboxCollisionConfig` | `string` | No | — | ID de la configuracion de colision de hitbox preestablecida (por ejemplo, `"SoftCollision"`). |
| `ArmorVisibilityOption` | `"All" \| "None" \| "Cosmetic"` | No | — | Controla que capas de armadura son visibles en el modelo del jugador. |

### SpawnConfig

| Campo | Tipo | Requerido | Por defecto | Descripcion |
|-------|------|-----------|-------------|-------------|
| `FirstSpawnParticles` | `ParticleEntry[]` | No | — | Sistemas de particulas generados en la ubicacion del jugador en la primera aparicion. |

### PingConfig

| Campo | Tipo | Requerido | Por defecto | Descripcion |
|-------|------|-----------|-------------|-------------|
| `PingDuration` | `number` | No | — | Segundos que un marcador de ping permanece visible. |
| `PingCooldown` | `number` | No | — | Segundos entre pings permitidos para un jugador. |
| `PingBroadcastRadius` | `number` | No | — | Radio en unidades dentro del cual otros jugadores ven el ping. |
| `PingSound` | `string` | No | — | Evento de sonido reproducido cuando se coloca un ping. |

## Ejemplos

**Configuracion de mundo por defecto** (`Assets/Server/GameplayConfigs/Default.json`):

```json
{
  "Death": {
    "ItemsLossMode": "Configured",
    "ItemsAmountLossPercentage": 50.0,
    "ItemsDurabilityLossPercentage": 10.0
  },
  "ItemEntity": {
    "Lifetime": 600.0
  },
  "ItemDurability": {
    "BrokenPenalties": {
      "Weapon": 0.75,
      "Armor": 0.75,
      "Tool": 0.75
    }
  },
  "Plugin": {
    "Stamina": {
      "SprintRegenDelay": {
        "EntityStatId": "StaminaRegenDelay",
        "Value": -0.75
      }
    },
    "Memories": {
      "MemoriesAmountPerLevel": [10, 25, 50, 100, 200],
      "MemoriesRecordParticles": "MemoryRecordedStatue",
      "MemoriesCatchItemId": "Memory_Particle",
      "MemoriesCatchParticleViewDistance": 64
    }
  },
  "Respawn": {
    "RadiusLimitRespawnPoint": 500,
    "MaxRespawnPointsPerPlayer": 3
  },
  "World": {
    "DaytimeDurationSeconds": 1728,
    "NighttimeDurationSeconds": 1152,
    "BlockPlacementFragilityTimer": 0,
    "Sleep": {
      "WakeUpHour": 4.79,
      "AllowedSleepHoursRange": [19.5, 4.79]
    }
  },
  "Player": {
    "MovementConfig": "Default",
    "HitboxCollisionConfig": "SoftCollision",
    "ArmorVisibilityOption": "All"
  },
  "Ping": {
    "PingDuration": 5.0,
    "PingCooldown": 1.0,
    "PingBroadcastRadius": 100.0,
    "PingSound": "SFX_Ping"
  }
}
```

**Configuracion de instancia** (`Assets/Server/GameplayConfigs/Default_Instance.json`) — hereda de Default y anula:

```json
{
  "Parent": "Default",
  "World": {
    "AllowBlockBreaking": false,
    "AllowBlockGathering": false
  },
  "Death": {
    "LoseItems": false,
    "RespawnController": {
      "Type": "ExitInstance"
    }
  }
}
```

## Paginas Relacionadas

- [Entornos](/es/hytale-modding-docs/reference/world-and-environment/environments) — progresion de horas dia/noche impulsada por `DaytimeDurationSeconds`
- [Tablas de Botin](/es/hytale-modding-docs/reference/economy-and-progression/drop-tables) — objetos soltados al morir sujetos a `ItemsLossMode`
- [Sistema de Clima](/es/hytale-modding-docs/reference/world-and-environment/weather-system) — clima controlado por `Plugin.Weathers`
