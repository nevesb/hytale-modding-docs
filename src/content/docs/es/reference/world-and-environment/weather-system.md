---
title: Sistema de clima
description: Referencia para los archivos de definición de clima en Hytale, cubriendo colores del cielo, capas de nubes, niebla, visuales del sol y la luna, y partículas ambientales.
---

## Descripción general

Los archivos de clima definen el estado visual completo del cielo para una condición climática nombrada. Todas las propiedades de color y escala usan un arreglo de entradas con clave temporal — el motor interpola entre keyframes a medida que avanza la hora del juego. Las capas de nubes, densidad de niebla, colores del sol/luna y partículas ambientales se controlan aquí. Los IDs de clima definidos en estos archivos son referenciados por los [horarios de pronóstico de ambiente](/hytale-modding-docs/reference/world-and-environment/environments).

## Ubicación de archivos

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

## Esquema

### Nivel superior

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Stars` | `string` | No | — | Ruta a la textura del campo de estrellas renderizado por la noche. |
| `Moons` | `MoonEntry[]` | No | — | Texturas de fases lunares, una por día en el ciclo lunar. |
| `Clouds` | `CloudLayer[]` | No | — | Lista ordenada de capas de textura de nubes compuestas sobre el cielo. |
| `SkyTopColors` | `HourColor[]` | No | — | Keyframes de color del cénit del cielo. |
| `SkyBottomColors` | `HourColor[]` | No | — | Keyframes de color del horizonte del cielo. |
| `SkySunsetColors` | `HourColor[]` | No | — | Keyframes de color del tinte del atardecer/amanecer. |
| `FogColors` | `HourColor[]` | No | — | Keyframes de color de la niebla. |
| `FogDensities` | `HourValue[]` | No | — | Keyframes de densidad de niebla (0–1). |
| `FogHeightFalloffs` | `HourValue[]` | No | — | Keyframes de caída de altura de niebla. |
| `FogDistance` | `[number, number]` | No | — | Rango de distancia de niebla `[cerca, lejos]` en unidades. |
| `FogOptions` | `FogOptions` | No | — | Opciones adicionales de renderizado de niebla. |
| `SunColors` | `HourColor[]` | No | — | Keyframes de color del disco solar. |
| `SunGlowColors` | `HourColor[]` | No | — | Keyframes de color del halo del resplandor solar. |
| `SunScales` | `HourValue[]` | No | — | Keyframes de escala del disco solar. |
| `MoonColors` | `HourColor[]` | No | — | Keyframes de color del disco lunar. |
| `MoonGlowColors` | `HourColor[]` | No | — | Keyframes de color del halo del resplandor lunar. |
| `MoonScales` | `HourValue[]` | No | — | Keyframes de escala del disco lunar. |
| `Particle` | `WeatherParticle` | No | — | Sistema de partículas ambientales reproducido durante este clima (ej. lluvia, nieve, luciérnagas). |

### MoonEntry

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Day` | `number` | Sí | — | Índice del día en el ciclo lunar (base 0). |
| `Texture` | `string` | Sí | — | Ruta a la textura de fase lunar para este día del ciclo. |

### CloudLayer

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Texture` | `string` | Sí | — | Ruta a la textura de nube para esta capa. |
| `Colors` | `HourColor[]` | Sí | — | Keyframes de color RGBA que controlan la visibilidad y el tinte de la nube a lo largo del día. |
| `Speeds` | `HourValue[]` | Sí | — | Keyframes de velocidad de desplazamiento para esta capa de nubes. |

### HourColor

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Hour` | `number` | Sí | — | Hora del juego (0–23) en la que se aplica este color. El motor interpola entre keyframes. |
| `Color` | `string` | Sí | — | Cadena de color hexadecimal, opcionalmente con alfa (ej. `"#ffffffe6"`, `"rgba(#2c6788, 1)"`). |

### HourValue

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Hour` | `number` | Sí | — | Hora del juego (0–23). |
| `Value` | `number` | Sí | — | Valor numérico en esta hora (escala, densidad, velocidad, etc.). |

### FogOptions

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `FogHeightCameraFixed` | `number` | No | — | Fija el plano de altura de la niebla relativo a la cámara en lugar del mundo. |
| `EffectiveViewDistanceMultiplier` | `number` | No | `1.0` | Escala la distancia de visión efectiva durante este clima. |

### WeatherParticle

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `SystemId` | `string` | Sí | — | ID del sistema de partículas a reproducir como efecto climático ambiental. |
| `OvergroundOnly` | `boolean` | No | `false` | Si es `true`, las partículas solo aparecen en áreas sobre el suelo. |
| `Color` | `string` | No | — | Color de tinte hexadecimal aplicado al sistema de partículas. |

## Ejemplo

**Clima soleado de Zona 1** (`Assets/Server/Weathers/Zone1/Cave_Deep.json` — nota: esto muestra una variante de clima de cueva; los climas principales de Zone1 siguen el mismo esquema):

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

**Clima del vacío con partículas ambientales** (`Assets/Server/Weathers/Void.json`, condensado):

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

## Páginas relacionadas

- [Ambientes](/hytale-modding-docs/reference/world-and-environment/environments) — horarios de pronóstico de clima por hora que referencian IDs de clima
- [Granjas y corrales](/hytale-modding-docs/reference/economy-and-progression/farming-coops) — IDs de clima usados en condiciones del modificador de agua
