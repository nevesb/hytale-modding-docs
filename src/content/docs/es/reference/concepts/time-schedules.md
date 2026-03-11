---
title: Horarios temporales
description: Cómo Hytale utiliza horarios por hora para el clima, apariciones y cambios visuales.
---

## Descripción general

Varios sistemas de Hytale usan horarios por hora — arreglos indexados por hora (0-23) — para variar el comportamiento a lo largo del ciclo día/noche. Los pronósticos del clima, colores del cielo, densidad de niebla y ventanas de aparición de NPCs usan este patrón.

## Formato del horario

Los horarios usan claves de texto `"0"` a `"23"` representando las horas:

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

Las reglas de aparición usan un formato más simple `[inicio, fin]`:

```json
{
  "DayTimeRange": [6, 18]
}
```

Esto restringe la aparición a las horas 6:00 a 18:00 (solo durante el día).

## Arreglos de colores por hora

Los visuales del clima usan arreglos de 24 elementos para transiciones suaves:

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

Cada elemento corresponde a una hora. El juego interpola entre valores para transiciones suaves.

## Sistemas que usan horarios temporales

| Sistema | Formato | Ubicación |
|---------|---------|-----------|
| Pronósticos del clima | Arreglos ponderados por hora | `Server/Environments/` |
| Colores de cielo/niebla/sol | Arreglos de colores de 24 elementos | `Server/Weathers/` |
| Velocidades de nubes | Arreglos de flotantes de 24 elementos | `Server/Weathers/` |
| Aparición de NPCs | `DayTimeRange` [inicio, fin] | `Server/NPC/Spawn/` |
| Producción agrícola | `ResidentRoamTime` [inicio, fin] | `Server/Farming/Coops/` |

## Páginas relacionadas

- [Sistema de clima](/hytale-modding-docs/reference/world-and-environment/weather-system/) — propiedades visuales por hora
- [Entornos](/hytale-modding-docs/reference/world-and-environment/environments/) — horarios de pronósticos del clima
- [Reglas de aparición de NPCs](/hytale-modding-docs/reference/npc-system/npc-spawn-rules/) — DayTimeRange
