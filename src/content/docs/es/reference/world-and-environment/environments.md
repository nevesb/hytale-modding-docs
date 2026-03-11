---
title: Ambientes
description: Referencia para las definiciones de ambientes en Hytale, que programan pronósticos de clima ponderados para cada hora del juego en una zona o región.
---

## Descripción general

Los archivos de ambiente definen el horario de clima para una región del mundo del juego. Cada archivo contiene un mapa `WeatherForecasts` con 24 entradas — una por hora del juego (0–23). En cada hora el motor muestrea de la lista ponderada de IDs de clima para determinar qué clima se reproduce. Pueden existir múltiples archivos de ambiente para la misma zona, representando variantes estacionales o temáticas.

## Ubicación de archivos

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

## Esquema

### Nivel superior

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `WeatherForecasts` | `object` | Sí | — | Mapa de cadenas de hora (`"0"`–`"23"`) a arreglos de `WeatherForecastEntry`. |
| `WaterTint` | `string` | No | — | Color hexadecimal aplicado a las superficies de agua en este ambiente. |
| `SpawnDensity` | `number` | No | — | Multiplicador para la densidad de aparición de NPCs en este ambiente. |
| `Tags` | `object` | No | — | Mapa arbitrario de etiquetas clave-valor usado por otros sistemas para identificar este ambiente. |

### WeatherForecastEntry

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `WeatherId` | `string` | Sí | — | ID de la definición de clima a reproducir potencialmente en esta hora. Referencia un archivo en `Assets/Server/Weathers/`. |
| `Weight` | `number` | Sí | — | Probabilidad relativa de que este clima sea seleccionado. Un peso de `0` deshabilita el clima para esa hora sin eliminar la entrada. |

## Cómo funciona el muestreo

Cada hora del juego, el motor busca el arreglo en la clave de esa hora y realiza una selección aleatoria ponderada. Las entradas con `Weight: 0` nunca son elegidas. La suma de todos los pesos en el arreglo de una hora no necesita ser igual a 100 — la selección es proporcional.

## Ejemplos

**Ambiente predeterminado de Zona 1** (`Assets/Server/Environments/Zone1/Env_Zone1.json`, condensado a las horas 0, 4, 18–19):

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

Observa que `Zone1_Foggy_Light` tiene `Weight: 0` durante el día (horas 0–2) pero gana peso al amanecer (horas 3–7), haciendo que la niebla sea un fenómeno exclusivo de la mañana. `Zone1_Sunny_Fireflies` solo aparece en las horas de la tarde 18–21.

**Ambiente simple de clima único** (`Assets/Server/Environments/Default.json`, condensado):

```json
{
  "WeatherForecasts": {
    "0":  [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "1":  [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "23": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }]
  }
}
```

## Páginas relacionadas

- [Sistema de clima](/hytale-modding-docs/reference/world-and-environment/weather-system) — formato de archivo de clima con parámetros de cielo, nubes y niebla
- [Granjas y corrales](/hytale-modding-docs/reference/economy-and-progression/farming-coops) — IDs de clima usados en condiciones del modificador de agua
- [Configuraciones de juego](/hytale-modding-docs/reference/game-configuration/gameplay-configs) — duración del día/noche que impulsa la progresión de horas
