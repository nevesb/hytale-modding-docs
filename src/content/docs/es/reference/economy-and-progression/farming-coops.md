---
title: Granjas y corrales
description: Referencia para las definiciones de corrales de granja y modificadores de crecimiento en Hytale, incluyendo grupos de NPCs residentes, tablas de drops de producción, horarios de paseo y modificadores ambientales.
---

## Descripción general

El sistema de granja tiene dos tipos de assets: **Corrales** y **Modificadores**. Los corrales definen recintos que albergan animales NPC y producen drops con el tiempo — especifican qué grupos de NPCs pueden vivir en el corral, cuántos residentes se permiten y qué tabla de drops produce cada especie. Los modificadores definen multiplicadores ambientales (agua, luz, fertilizante) que aceleran las tasas de crecimiento de plantas o animales.

## Ubicación de archivos

```
Assets/Server/Farming/
  Coops/
    Coop_Chicken.json
  Modifiers/
    Darkness.json
    Fertilizer.json
    LightLevel.json
    Water.json
```

## Esquema de corrales

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `MaxResidents` | `number` | Sí | — | Número máximo de residentes NPC que el corral puede albergar simultáneamente. |
| `ProduceDrops` | `object` | Sí | — | Mapa de ID de grupo NPC → ID de tabla de drops. Cada especie residente tiene su propia tabla de drops de producción. |
| `ResidentRoamTime` | `[number, number]` | Sí | — | Rango de horas del juego `[inicio, fin]` durante las cuales los residentes pasean libremente dentro del corral. |
| `ResidentSpawnOffset` | `Vector3` | No | — | Desplazamiento local aplicado al generar un residente dentro de la estructura del corral. |
| `AcceptedNpcGroups` | `string[]` | Sí | — | Lista de IDs de grupos NPC que pueden colocarse o capturarse en este tipo de corral. |
| `CaptureWildNPCsInRange` | `boolean` | No | `false` | Si es `true`, los NPCs salvajes de grupos aceptados dentro del rango son capturados automáticamente en el corral. |
| `WildCaptureRadius` | `number` | No | — | Radio en unidades dentro del cual los NPCs salvajes son auto-capturados cuando `CaptureWildNPCsInRange` es `true`. |

### Vector3

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `X` | `number` | Sí | — | Desplazamiento lateral. |
| `Y` | `number` | Sí | — | Desplazamiento vertical. |
| `Z` | `number` | Sí | — | Desplazamiento frontal. |

## Esquema de modificadores

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Type` | `"Water" \| "Fertilizer" \| "LightLevel" \| "Darkness"` | Sí | — | Categoría del modificador, usada para emparejar el modificador con los sistemas de crecimiento aplicables. |
| `Modifier` | `number` | Sí | — | Multiplicador de tasa de crecimiento aplicado cuando se cumplen las condiciones del modificador (ej. `2.5` = 2.5× más rápido). |
| `Fluids` | `string[]` | No | — | Solo tipo `Water`. IDs de bloques de fluido cuya presencia satisface la condición de agua. |
| `Weathers` | `string[]` | No | — | Solo tipo `Water`. IDs de clima que también cuentan como fuente de agua (ej. lluvia). |
| `ArtificialLight` | `LightRange` | No | — | Solo tipo `LightLevel`. Rangos de canales RGB que deben cumplirse por fuentes de luz artificial. |
| `Sunlight` | `SunlightRange` | No | — | Solo tipo `LightLevel`. Rango de nivel de luz solar que debe cumplirse. |
| `RequireBoth` | `boolean` | No | `false` | Solo tipo `LightLevel`. Si es `true`, tanto las condiciones de `ArtificialLight` como de `Sunlight` deben cumplirse simultáneamente. |

### LightRange (por canal RGB)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Min` | `number` | Sí | — | Nivel mínimo de luz (0–255). |
| `Max` | `number` | Sí | — | Nivel máximo de luz (0–255). |

### SunlightRange

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Min` | `number` | Sí | — | Nivel mínimo de luz solar (0–15). |
| `Max` | `number` | Sí | — | Nivel máximo de luz solar (0–15). |

## Ejemplos

**Corral de gallinas** (`Assets/Server/Farming/Coops/Coop_Chicken.json`):

```json
{
  "MaxResidents": 6,
  "ProduceDrops": {
    "Chicken": "Drop_Chicken_Produce",
    "Chicken_Desert": "Drop_Chicken_Produce",
    "Skrill": "Drop_Chicken_Produce"
  },
  "ResidentRoamTime": [6, 18],
  "ResidentSpawnOffset": {
    "X": 0,
    "Y": 0,
    "Z": 3
  },
  "AcceptedNpcGroups": [
    "Chicken",
    "Chicken_Desert",
    "Skrill"
  ],
  "CaptureWildNPCsInRange": true,
  "WildCaptureRadius": 10
}
```

**Modificador de agua** (`Assets/Server/Farming/Modifiers/Water.json`):

```json
{
  "Type": "Water",
  "Modifier": 2.5,
  "Fluids": ["Water_Source", "Water"],
  "Weathers": ["Zone1_Rain", "Zone1_Rain_Light", "Zone1_Storm", "Zone3_Rain"]
}
```

**Modificador de fertilizante** (`Assets/Server/Farming/Modifiers/Fertilizer.json`):

```json
{
  "Type": "Fertilizer",
  "Modifier": 2
}
```

**Modificador de nivel de luz** (`Assets/Server/Farming/Modifiers/LightLevel.json`):

```json
{
  "Type": "LightLevel",
  "Modifier": 2,
  "ArtificialLight": {
    "Red":   { "Min": 5, "Max": 127 },
    "Green": { "Min": 5, "Max": 127 },
    "Blue":  { "Min": 5, "Max": 127 }
  },
  "Sunlight": {
    "Min": 5.0,
    "Max": 15.0
  },
  "RequireBoth": false
}
```

## Páginas relacionadas

- [Tablas de drops](/hytale-modding-docs/reference/economy-and-progression/drop-tables) — formato de tabla de drops usado en `ProduceDrops`
- [Sistema de clima](/hytale-modding-docs/reference/world-and-environment/weather-system) — IDs de clima referenciados en `Water.Weathers`
- [Tiendas de trueque](/hytale-modding-docs/reference/economy-and-progression/barter-shops) — venta de productos de la granja
