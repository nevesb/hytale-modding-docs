---
title: Generación de mundos
description: Referencia para los archivos de generación de mundos en Hytale, cubriendo el pipeline HytaleGenerator incluyendo biomas, mapas de densidad, asignaciones, máscaras de bloques y configuraciones de estructura del mundo.
---

## Descripción general

La generación de mundos en Hytale es impulsada por un pipeline basado en grafos de nodos llamado **HytaleGenerator**. Produce terreno a través de funciones de ruido por capas, mapas de densidad, definiciones de biomas y asignaciones de prefabs ponderadas. Cada componente se define en un archivo JSON separado y se conecta mediante referencias de importación/exportación. El sistema soporta formas de continentes procedurales, zonas climáticas, redes de cuevas, tallado de ríos y colocación de dispersión por bioma.

## Ubicación de archivos

```
Assets/Server/HytaleGenerator/
  Assignments/
    Boreal1/
      Boreal1_Hedera_Trees.json
      Boreal1_Hedera_Mushrooms.json
      ...
    Desert1/
    Plains1/
    Volcanic1/
  Biomes/
    Basic.json
    Boreal1/
      Boreal1_Hedera.json
      Boreal1_Henges.json
    Desert1/
    Plains1/
    Volcanic1/
    Default_Flat/
    Default_Void/
  BlockMasks/
  Density/
    Map_Default.json
    Map_Portals.json
    Map_Tiles.json
    Plains1_Caves_Terrain.json
    ...
  Graphs/
  Settings/
    Settings.json
  WorldStructures/
```

## Esquema

### Settings (Settings.json)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `StatsCheckpoints` | `number[]` | No | — | Umbrales de conteo de chunks en los que se registran estadísticas de generación. |
| `CustomConcurrency` | `number` | No | `-1` | Conteo de hilos para la generación. `-1` usa el valor predeterminado del motor. |
| `BufferCapacityFactor` | `number` | No | `0.1` | Fracción de memoria total asignada a los búferes de generación. |
| `TargetViewDistance` | `number` | No | `512` | Distancia de visión objetivo en bloques usada para pre-calcular la prioridad de generación. |
| `TargetPlayerCount` | `number` | No | `3` | Conteo esperado de jugadores usado para dimensionar las colas de generación. |

### Nodo de densidad (archivos de grafo de nodos)

Los archivos de densidad definen un árbol de nodos de procesamiento que producen un campo escalar usado para la forma del terreno, tallado de ríos o mapeo de biomas. Cada nodo tiene como mínimo:

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `$NodeId` | `string` | Sí | — | Identificador único para este nodo en el grafo. |
| `Type` | `string` | Sí | — | Tipo de nodo. Ver tipos de nodo abajo. |
| `Skip` | `boolean` | No | `false` | Cuando es `true`, el nodo se omite durante la generación. |
| `ExportAs` | `string` | No | — | Nombre bajo el cual se publica la salida de este nodo para importación por otros grafos. |
| `SingleInstance` | `boolean` | No | `false` | Cuando es `true`, el nodo se evalúa una vez y se cachea globalmente. |
| `Inputs` | `DensityNode[]` | No | `[]` | Nodos hijos cuyas salidas alimentan este nodo. |

#### Tipos comunes de nodos de densidad

| Type | Description | Key Fields |
|------|-------------|------------|
| `SimplexNoise2D` | Generador de ruido simplex 2D | `Lacunarity`, `Persistence`, `Octaves`, `Scale`, `Seed` |
| `Constant` | Produce un valor fijo | `Value` |
| `Sum` | Suma todos los valores de entrada | — |
| `Min` / `Max` | Retorna el mínimo o máximo de las entradas | — |
| `Clamp` | Limita la entrada entre dos paredes | `WallA`, `WallB` |
| `Normalizer` | Remapea un rango de valores | `FromMin`, `FromMax`, `ToMin`, `ToMax` |
| `Inverter` | Niega la entrada | — |
| `Abs` | Valor absoluto | — |
| `Mix` | Mezcla dos entradas usando una tercera como alfa | — |
| `Scale` | Multiplica las coordenadas de entrada | `ScaleX`, `ScaleY`, `ScaleZ` |
| `Cache` | Cachea el resultado de los nodos hijos | `Capacity` |
| `YOverride` | Fuerza una coordenada Y fija para evaluación 2D | `Value` |
| `Distance` | Distancia desde el origen con una curva de caída | `Curve` |
| `Exported` | Marca la salida de un nodo para importación entre grafos | `ExportAs`, `SingleInstance` |
| `Imported` | Referencia un nodo exportado por nombre | `Name` |

### Asignación (colocación de dispersión/prefabs)

Los archivos de asignación controlan qué decoraciones, vegetación o estructuras se colocan en una región de bioma. Usan un enfoque de función de campo con delimitadores.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Type` | `string` | Sí | — | Tipo de nivel superior, típicamente `"FieldFunction"`. |
| `ExportAs` | `string` | No | — | Nombre de exportación para esta asignación. |
| `FieldFunction` | `FieldFunction` | Sí | — | Función de ruido que produce el campo de densidad de colocación. |
| `Delimiters` | `Delimiter[]` | Sí | — | Rangos dentro de la salida de la función de campo que activan la colocación. |

#### FieldFunction

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Type` | `string` | Sí | — | Tipo de ruido, ej. `"SimplexNoise2D"`. |
| `Skip` | `boolean` | No | `false` | Omitir esta función. |
| `Lacunarity` | `number` | No | `2` | Multiplicador de frecuencia por octava. |
| `Persistence` | `number` | No | `0.5` | Multiplicador de amplitud por octava. |
| `Octaves` | `number` | No | `1` | Número de octavas de ruido. |
| `Scale` | `number` | Sí | — | Escala espacial del ruido. |
| `Seed` | `string` | Sí | — | Cadena de semilla para generación determinista. |

#### Delimiter

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Min` | `number` | Sí | — | Valor mínimo de campo para este rango. |
| `Max` | `number` | Sí | — | Valor máximo de campo para este rango. |
| `Assignments` | `AssignmentNode` | Sí | — | Qué colocar cuando el valor del campo cae en este rango. |

#### AssignmentNode

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Type` | `string` | Sí | — | `"Weighted"`, `"Constant"` o `"Cluster"`. |
| `SkipChance` | `number` | No | `0` | Probabilidad (0–1) de omitir la colocación por completo. |
| `Seed` | `string` | No | — | Semilla para selección aleatoria ponderada. |
| `WeightedAssignments` | `WeightedEntry[]` | No | — | Arreglo de opciones ponderadas (cuando `Type` es `"Weighted"`). |
| `Prop` | `PropConfig` | No | — | Prefab/prop a colocar (cuando `Type` es `"Constant"` o dentro de una entrada ponderada). |

## Ejemplo

**Mapa de densidad** (`Assets/Server/HytaleGenerator/Density/Map_Default.json`, condensado para mostrar la estructura):

```json
{
  "$NodeId": "Exported.Density-ed27c3c9",
  "Type": "Exported",
  "ExportAs": "Biome-Map",
  "SingleInstance": true,
  "Inputs": [
    {
      "Type": "YOverride",
      "Value": 0,
      "Inputs": [
        {
          "Type": "Cache",
          "Capacity": 1,
          "Inputs": [
            {
              "Type": "Mix",
              "Inputs": [
                { "Type": "Imported", "Name": "Biome-Map-Tiles" },
                { "Type": "Constant", "Value": -0.3 },
                {
                  "Type": "Clamp",
                  "WallA": 0,
                  "WallB": 1,
                  "Inputs": [
                    {
                      "Type": "Normalizer",
                      "FromMin": 0.62,
                      "FromMax": 0.62,
                      "ToMin": 0,
                      "ToMax": 1,
                      "Inputs": [
                        { "Type": "Exported", "ExportAs": "World-River-Map" }
                      ]
                    }
                  ]
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

**Configuración del generador** (`Assets/Server/HytaleGenerator/Settings/Settings.json`):

```json
{
  "StatsCheckpoints": [1, 100, 500, 1000],
  "CustomConcurrency": -1,
  "BufferCapacityFactor": 0.1,
  "TargetViewDistance": 512,
  "TargetPlayerCount": 3
}
```

## Páginas relacionadas

- [Máscaras de mundo](/hytale-modding-docs/reference/world-and-environment/world-masks) — máscaras de ruido para forma de continente, temperatura y clima
- [Ambientes](/hytale-modding-docs/reference/world-and-environment/environments) — definiciones de ambiente asignadas por zona
- [Instancias](/hytale-modding-docs/reference/game-configuration/instances) — configuraciones de instancia que seleccionan un perfil de generación de mundo
