---
title: Máscaras de mundo
description: Referencia para las definiciones de máscaras de mundo en Hytale, que controlan la forma de continentes, gradientes de temperatura, zonas climáticas y el mapeo de bioma a color para la generación procedural del mundo.
---

## Descripción general

Los archivos de máscaras de mundo definen la estructura a gran escala del mundo procedural. El archivo principal `Mask.json` vincula la forma del continente, temperatura, intensidad y sub-máscaras de clima, y declara zonas únicas (puntos de aparición, templos). Los archivos de sub-máscaras usan generadores de ruido y caídas basadas en distancia para producir campos escalares que el generador del mundo muestrea para decidir qué bioma ocupa una coordenada dada. Un archivo complementario `Zones.json` mapea colores de máscara a listas de zonas nombradas.

## Ubicación de archivos

```
Assets/Server/World/
  Default/
    Mask.json
    World.json
    Zones.json
    Mask/
      Blend_Inner.json
      Blend_Outer.json
      Continent.json
      Intensity.json
      Temperature.json
      Climate/
        Cold.json
        Hot.json
        Temperate.json
        Island/
          Tier1.json
          Tier2.json
          Tier3.json
      Continent/
        Blend_Inner.json
        Blend_Outer.json
        Continent_Inner.json
        Continent_Outer.json
      Temperature/
        Temperature_Inner.json
        Temperature_Outer.json
  Flat/
  Void/
  Instance_Creative_Hub/
  Instance_Dungeon_Goblin/
  Instance_Forgotten_Temple/
```

## Esquema

### Mask.json (nivel superior)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Randomizer` | `Randomizer` | No | — | Aleatorizador de ruido global aplicado a todo el muestreo de máscaras. |
| `Noise` | `NoiseConfig` | Sí | — | Referencias a las sub-máscaras de continente, temperatura e intensidad, más umbrales de tierra/océano. |
| `Climate` | `ClimateConfig` | Sí | — | Definiciones de zonas climáticas y parámetros de mezcla. |
| `UniqueZones` | `UniqueZone[]` | No | `[]` | Zonas nombradas colocadas en ubicaciones específicas del mundo (ej. aparición, templos). |

### Randomizer

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Generators` | `Generator[]` | Sí | — | Arreglo de generadores de ruido que contribuyen a la aleatorización. |

### Generator

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Seed` | `string` | No | — | Cadena de semilla determinista. |
| `NoiseType` | `string` | Sí | — | Algoritmo de ruido: `"SIMPLEX"`, `"OLD_SIMPLEX"`, `"POINT"`. |
| `Scale` | `number` | Sí | — | Escala espacial del ruido. |
| `Amplitude` | `number` | No | `1` | Multiplicador de amplitud de salida. |
| `Octaves` | `number` | No | `1` | Número de octavas fractales. |
| `Persistence` | `number` | No | `0.5` | Decaimiento de amplitud por octava. |
| `Lacunarity` | `number` | No | `2.0` | Multiplicador de frecuencia por octava. |

### NoiseConfig

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Thresholds` | `Thresholds` | Sí | — | Umbrales escalares que separan tierra, isla, playa y océano poco profundo. |
| `Continent` | `FileRef` | Sí | — | Referencia a la sub-máscara de forma de continente. |
| `Temperature` | `FileRef` | Sí | — | Referencia a la sub-máscara de gradiente de temperatura. |
| `Intensity` | `FileRef` | Sí | — | Referencia a la sub-máscara de intensidad. |

### Thresholds

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Land` | `number` | Sí | — | Valor de ruido por encima del cual el terreno se considera tierra. |
| `Island` | `number` | Sí | — | Valor de ruido por encima del cual el terreno se considera una isla. |
| `BeachSize` | `number` | Sí | — | Ancho de la banda de transición de playa. |
| `ShallowOceanSize` | `number` | Sí | — | Ancho de la banda de océano poco profundo alrededor de la tierra. |

### ClimateConfig

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `FadeMode` | `string` | No | `"CHILDREN"` | Cómo se desvanecen los límites climáticos: `"CHILDREN"` usa configuraciones por hijo. |
| `FadeRadius` | `number` | No | — | Radio de la zona de transición climática. |
| `FadeDistance` | `number` | No | — | Distancia sobre la cual ocurre el desvanecimiento. |
| `Climates` | `FileRef[]` | Sí | — | Referencias a archivos individuales de definición climática. |

### Definición de clima (ej. Cold.json)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Name` | `string` | Sí | — | Nombre visible para este clima (ej. `"Zone 3"`). |
| `Color` | `string` | Sí | — | Color hexadecimal usado para representar este clima en mapas de depuración. |
| `Points` | `ClimatePoint[]` | Sí | — | Coordenadas de temperatura/intensidad que definen dónde aparece este clima. |
| `Children` | `ClimateTier[]` | No | `[]` | Sub-niveles dentro de este clima con colores de bioma distintos y configuraciones de isla. |

### ClimateTier

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Name` | `string` | Sí | — | Nombre visible del nivel (ej. `"Tier 1"`). |
| `Color` | `string` | Sí | — | Color hexadecimal para el bioma terrestre de este nivel. |
| `Shore` | `string` | No | — | Color hexadecimal para áreas costeras en este nivel. |
| `Ocean` | `string` | No | — | Color hexadecimal para océano profundo en este nivel. |
| `ShallowOcean` | `string` | No | — | Color hexadecimal para océano poco profundo en este nivel. |
| `Island` | `FileRef` | No | — | Referencia a un archivo de máscara de isla para este nivel. |
| `Points` | `ClimatePoint[]` | Sí | — | Coordenadas climáticas con `Modifier` opcional. |

### ClimatePoint

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Temperature` | `number` | Sí | — | Valor del eje de temperatura (0–1). |
| `Intensity` | `number` | Sí | — | Valor del eje de intensidad (0–1). |
| `Modifier` | `number` | No | `1` | Modificador de mezcla para transiciones entre niveles. |

### UniqueZone

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Name` | `string` | Sí | — | Identificador de zona referenciado por el bioma y el mapeo de colores de Zones.json. |
| `Parent` | `string` | No | — | Nombre de una zona única padre para colocación relativa. |
| `Color` | `string` | Sí | — | Color hexadecimal para renderizado en mapa de depuración. |
| `Radius` | `number` | Sí | — | Radio de la zona en chunks. |
| `OriginX` | `number` | Sí | — | Origen X para cálculos de distancia. |
| `OriginY` | `number` | Sí | — | Origen Y para cálculos de distancia. |
| `Distance` | `number` | Sí | — | Distancia máxima desde el origen para buscar colocación. |
| `MinDistance` | `number` | No | `0` | Distancia mínima desde el origen (crea un área de búsqueda anular). |
| `Rule` | `PlacementRule` | Sí | — | Restricciones sobre valores de continente, temperatura, intensidad y desvanecimiento. |

### PlacementRule

Cada clave (`Continent`, `Temperature`, `Intensity`, `Fade`) contiene:

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Target` | `number` | Sí | — | Valor ideal de máscara para colocación. |
| `Radius` | `number` | Sí | — | Desviación aceptable del objetivo. |
| `Weight` | `number` | Sí | — | Importancia de esta restricción relativa a las demás. |

### Tipos de sub-máscara

Los archivos de sub-máscara usan un campo `Type` para definir su comportamiento:

| Type | Description | Key Fields |
|------|-------------|------------|
| `DISTORTED` | Máscara basada en puntos con distorsión de ruido | `Noise` (con `NoiseType`, `X`, `Y`, `InnerRadius`, `OuterRadius`), `Randomizer` |
| `BLEND` | Mezcla dos máscaras hijas usando una máscara alfa | `Alpha` (FileRef), `Noise` (FileRef[]), `Thresholds`, `Normalize` |

### Zones.json

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `GridGenerator` | `GridGenerator` | Sí | — | Controla la cuadrícula estilo Voronoi usada para asignar zonas. |
| `MaskMapping` | `object` | Sí | — | Mapa de cadenas de color hexadecimal a arreglos de cadenas de nombres de zona. |

### GridGenerator

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Scale` | `number` | Sí | — | Tamaño de celda de la cuadrícula. |
| `Jitter` | `number` | No | `0` | Desplazamiento aleatorio aplicado a los puntos de la cuadrícula (0–1). |
| `Randomizer` | `Randomizer` | No | — | Generadores de ruido para la variación de la cuadrícula. |

### World.json

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Masks` | `string[]` | Sí | — | Arreglo de referencias a archivos de máscara (ej. `["Mask.json"]`). |
| `PrefabStore` | `string` | No | `"ASSETS"` | Fuente de datos de prefabs: `"ASSETS"` o `"DISK"`. |
| `Height` | `number` | Sí | — | Altura del mundo en regiones. |
| `Width` | `number` | Sí | — | Ancho del mundo en regiones. |
| `OffsetX` | `number` | No | `0` | Desplazamiento horizontal del origen. |
| `OffsetY` | `number` | No | `0` | Desplazamiento vertical del origen. |
| `Randomizer` | `Randomizer` | No | — | Aleatorizador adicional para ruido a nivel del mundo. |

## Ejemplos

**Máscara de nivel superior** (`Assets/Server/World/Default/Mask.json`, condensado):

```json
{
  "Randomizer": {
    "Generators": [
      { "Seed": "RANDOMIZER", "NoiseType": "SIMPLEX", "Scale": 0.01, "Amplitude": 16.0 }
    ]
  },
  "Noise": {
    "Thresholds": {
      "Land": 0.5,
      "Island": 0.75,
      "BeachSize": 0.02,
      "ShallowOceanSize": 0.08
    },
    "Continent": { "File": "Mask.Continent" },
    "Temperature": { "File": "Mask.Temperature" },
    "Intensity": { "File": "Mask.Intensity" }
  },
  "Climate": {
    "FadeMode": "CHILDREN",
    "FadeRadius": 50.0,
    "FadeDistance": 100.0,
    "Climates": [
      { "File": "Mask.Climate.Temperate" },
      { "File": "Mask.Climate.Cold" },
      { "File": "Mask.Climate.Hot" }
    ]
  },
  "UniqueZones": [
    {
      "Name": "Zone1_Spawn",
      "Color": "#ff0000",
      "Radius": 35,
      "OriginX": 0,
      "OriginY": 0,
      "Distance": 3000,
      "Rule": {
        "Continent":   { "Target": 0.0, "Radius": 0.3, "Weight": 1.0 },
        "Temperature": { "Target": 0.5, "Radius": 0.2, "Weight": 1.0 },
        "Intensity":   { "Target": 0.1, "Radius": 0.3, "Weight": 1.0 },
        "Fade":        { "Target": 1.0, "Radius": 0.5, "Weight": 0.5 }
      }
    }
  ]
}
```

**Sub-máscara de mezcla de continente** (`Assets/Server/World/Default/Mask/Blend_Inner.json`):

```json
{
  "Type": "DISTORTED",
  "Noise": {
    "NoiseType": "POINT",
    "X": 0.0,
    "Y": 0.0,
    "InnerRadius": 1700.0,
    "OuterRadius": 2500.0
  },
  "Randomizer": {
    "Generators": [
      {
        "Seed": "CONTINENT-INNER-WARP-1",
        "NoiseType": "SIMPLEX",
        "Scale": 0.00085,
        "Octaves": 1,
        "Persistence": 0.5,
        "Lacunarity": 2.5,
        "Amplitude": 450
      }
    ]
  }
}
```

## Páginas relacionadas

- [Generación de mundos](/hytale-modding-docs/reference/world-and-environment/world-generation) — el pipeline HytaleGenerator que consume estas máscaras
- [Ambientes](/hytale-modding-docs/reference/world-and-environment/environments) — archivos de ambiente asignados a zonas definidas por máscaras
- [Instancias](/hytale-modding-docs/reference/game-configuration/instances) — configuraciones de instancia que seleccionan una definición de mundo
