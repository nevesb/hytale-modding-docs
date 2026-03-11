---
title: Modificadores de granja
description: Referencia para las definiciones de modificadores de crecimiento de granja en Hytale, cubriendo multiplicadores de agua, fertilizante y nivel de luz que aceleran el crecimiento de cultivos.
---

## Descripción general

Los modificadores de granja definen condiciones ambientales que aceleran o habilitan el crecimiento de plantas y animales. Cada modificador especifica un multiplicador de tasa de crecimiento y las condiciones bajo las cuales se aplica. El sistema soporta tres tipos de modificadores: **Water** (proximidad a fluidos o clima de lluvia), **Fertilizer** (aplicado mediante objetos) y **LightLevel** (umbrales de luz ambiental o artificial). Cuando múltiples modificadores están activos simultáneamente, sus multiplicadores se apilan para determinar la tasa de crecimiento final.

## Ubicación de archivos

```
Assets/Server/Farming/Modifiers/
```

Un archivo JSON por modificador:

```
Assets/Server/Farming/Modifiers/
  Darkness.json
  Fertilizer.json
  LightLevel.json
  Water.json
```

## Esquema

### Campos comunes

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Type` | `"Water" \| "LightLevel" \| "Fertilizer"` | Sí | — | Categoría del modificador. Determina qué campos adicionales son relevantes. |
| `Modifier` | `number` | Sí | — | Multiplicador de tasa de crecimiento aplicado cuando se cumplen las condiciones del modificador. Valores mayores a `1` aceleran el crecimiento; un valor de `2` duplica la tasa, `2.5` multiplica por 2.5x, etc. |

### Campos específicos de Water

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Fluids` | `string[]` | No | — | IDs de bloques de fuentes de fluido que satisfacen la condición de agua cuando son adyacentes (ej. `"Water_Source"`, `"Water"`). |
| `Weathers` | `string[]` | No | — | IDs de clima que satisfacen la condición de agua globalmente (ej. `"Zone1_Rain"`, `"Zone1_Storm"`). |

### Campos específicos de LightLevel

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `ArtificialLight` | `LightChannelRange` | No | — | Rango aceptable para fuentes de luz artificial (colocadas), definido por canal RGB. |
| `Sunlight` | `Range` | No | — | Rango aceptable para la intensidad de la luz solar. |
| `RequireBoth` | `boolean` | No | `false` | Si es `true`, tanto las condiciones de `ArtificialLight` como de `Sunlight` deben cumplirse simultáneamente. Si es `false`, cualquiera de las dos es suficiente. |

### LightChannelRange

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Red` | `Range` | Sí | — | Rango aceptable para el canal de luz roja. |
| `Green` | `Range` | Sí | — | Rango aceptable para el canal de luz verde. |
| `Blue` | `Range` | Sí | — | Rango aceptable para el canal de luz azul. |

### Range

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Min` | `number` | Sí | — | Valor mínimo aceptable (inclusivo). |
| `Max` | `number` | Sí | — | Valor máximo aceptable (inclusivo). |

## Ejemplos

**Modificador de agua** (`Assets/Server/Farming/Modifiers/Water.json`):

```json
{
  "Type": "Water",
  "Modifier": 2.5,
  "Fluids": [
    "Water_Source",
    "Water"
  ],
  "Weathers": [
    "Zone1_Rain",
    "Zone1_Rain_Light",
    "Zone1_Storm",
    "Zone3_Rain"
  ]
}
```

Los cultivos adyacentes a bloques de agua o expuestos a clima de lluvia crecen a 2.5x la tasa base.

**Modificador de nivel de luz** (`Assets/Server/Farming/Modifiers/LightLevel.json`):

```json
{
  "Type": "LightLevel",
  "Modifier": 2,
  "ArtificialLight": {
    "Red": { "Min": 5, "Max": 127 },
    "Green": { "Min": 5, "Max": 127 },
    "Blue": { "Min": 5, "Max": 127 }
  },
  "Sunlight": {
    "Min": 5.0,
    "Max": 15.0
  },
  "RequireBoth": false
}
```

Las plantas que reciben suficiente luz solar O luz artificial crecen a 2x la tasa base.

**Modificador de oscuridad** (`Assets/Server/Farming/Modifiers/Darkness.json`):

```json
{
  "Type": "LightLevel",
  "Modifier": 2,
  "ArtificialLight": {
    "Red": { "Min": 0, "Max": 4 },
    "Green": { "Min": 0, "Max": 4 },
    "Blue": { "Min": 0, "Max": 4 }
  },
  "Sunlight": {
    "Min": 0,
    "Max": 5
  },
  "RequireBoth": true
}
```

Ciertas plantas que prefieren la sombra prosperan en la oscuridad. Tanto la luz artificial COMO la luz solar deben estar dentro de los rangos bajos para que este modificador se aplique.

**Modificador de fertilizante** (`Assets/Server/Farming/Modifiers/Fertilizer.json`):

```json
{
  "Type": "Fertilizer",
  "Modifier": 2
}
```

Cuando se aplica fertilizante a una parcela, la tasa de crecimiento se duplica. El tipo fertilizante no tiene condiciones adicionales más allá de ser aplicado.

## Páginas relacionadas

- [Granjas y corrales](/hytale-modding-docs/reference/economy-and-progression/farming-coops) — definiciones de corrales y drops de producción que funcionan junto con los modificadores de crecimiento
- [Tablas de drops](/hytale-modding-docs/reference/economy-and-progression/drop-tables) — tablas de drops de producción referenciadas por los corrales de granja
