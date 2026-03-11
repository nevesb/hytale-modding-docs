---
title: Listas de Tipos de Bloque
description: Referencia de las definiciones de listas de tipos de bloque en Hytale, que agrupan IDs de tipos de bloque en categorias nombradas usadas por la generacion de mundo, reglas de juego y sistemas de filtrado.
---

## Descripcion General

Los archivos de listas de tipos de bloque definen grupos nombrados de IDs de tipos de bloque. Estas listas son referenciadas por otros sistemas — la generacion de mundo las usa para determinar que bloques pueden dispersarse, reemplazarse o recolectarse, y las reglas de juego las usan para filtrar interacciones de bloques. Cada lista es simplemente un objeto JSON con un array `Blocks` que contiene IDs de cadena que corresponden a tipos de bloque registrados.

## Ubicacion de Archivos

```
Assets/Server/BlockTypeList/
  AllScatter.json
  Empty.json
  Gravel.json
  Ores.json
  PlantScatter.json
  PlantsAndTrees.json
  Rock.json
  Snow.json
  Soils.json
  TreeLeaves.json
  TreeWood.json
  TreeWoodAndLeaves.json
```

## Esquema

### Nivel superior

| Campo | Tipo | Requerido | Por defecto | Descripcion |
|-------|------|-----------|-------------|-------------|
| `Blocks` | `string[]` | Si | — | Array de cadenas de ID de tipo de bloque. Cada ID debe coincidir con un nombre de tipo de bloque registrado. |

## Descripciones de Listas

| Lista | Tamano Aproximado | Descripcion |
|-------|-------------------|-------------|
| `AllScatter` | ~160 entradas | Todos los bloques de dispersion decorativa: hierbas, flores, helechos, escombros, huesos, corales y decoraciones de nidos. |
| `Empty` | 0 entradas | Lista vacia usada como marcador de posicion "ninguno". |
| `Gravel` | Pequeno | Variantes de bloques de grava. |
| `Ores` | Pequeno | Bloques de mineral excavables a traves de todas las zonas. |
| `PlantScatter` | Mediano | Subconjunto de dispersion limitado a plantas y flores. |
| `PlantsAndTrees` | Mediano | Plantas, flores y bloques relacionados con arboles. |
| `Rock` | Pequeno | Bloques de roca y piedra naturales. |
| `Snow` | Pequeno | Variantes de bloques cubiertos de nieve. |
| `Soils` | ~13 entradas | Bloques de terreno de suelo y hierba a traves de tipos de bioma. |
| `TreeLeaves` | Pequeno | Bloques de hojas de todas las especies de arboles. |
| `TreeWood` | Pequeno | Bloques de tronco/madera de todas las especies de arboles. |
| `TreeWoodAndLeaves` | Mediano | Bloques combinados de madera y hojas de arboles. |

## Ejemplos

**Lista de suelos** (`Assets/Server/BlockTypeList/Soils.json`):

```json
{
  "Blocks": [
    "Soil_Dirt",
    "Soil_Dirt_Burnt",
    "Soil_Dirt_Cold",
    "Soil_Dirt_Dry",
    "Soil_Dirt_Poisoned",
    "Soil_Grass",
    "Soil_Grass_Burnt",
    "Soil_Grass_Cold",
    "Soil_Grass_Deep",
    "Soil_Grass_Dry",
    "Soil_Grass_Full",
    "Soil_Grass_Sunny",
    "Soil_Grass_Wet"
  ]
}
```

**Lista AllScatter** (`Assets/Server/BlockTypeList/AllScatter.json`, condensada):

```json
{
  "Blocks": [
    "Wood_Sticks",
    "Plant_Bush_Green",
    "Plant_Grass_Arid",
    "Plant_Grass_Arid_Short",
    "Plant_Grass_Lush",
    "Plant_Flower_Bushy_Blue",
    "Plant_Flower_Common_Red",
    "Plant_Fern",
    "Rubble_Stone",
    "Rubble_Sandstone",
    "Deco_Bone_Skulls_Feran",
    "Deco_Coral_Shell",
    "Deco_Trash"
  ]
}
```

## Paginas Relacionadas

- [Generacion de Mundo](/es/hytale-modding-docs/reference/world-and-environment/world-generation) — asignaciones que referencian listas de tipos de bloque para colocacion de dispersion
- [Texturas de Bloques](/es/hytale-modding-docs/reference/models-and-visuals/block-textures) — archivos de textura para los bloques referenciados en estas listas
- [Objetivos](/es/hytale-modding-docs/reference/game-configuration/objectives) — condiciones de tarea que filtran por etiquetas de bloque que coinciden con estas listas
