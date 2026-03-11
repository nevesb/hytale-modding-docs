---
title: Grupos de Objetos
description: Referencia de los archivos JSON de grupos de objetos en Hytale, que definen conjuntos nombrados de IDs de bloque usados por recetas, sistemas de crafteo y generación de mundo.
---

## Descripción General

Los grupos de objetos definen colecciones nombradas de IDs de bloque. Un grupo agrupa variantes de bloque relacionadas — por ejemplo, todos los tipos de bloque de piedra aqua — bajo un solo ID de grupo. Otros sistemas referencian IDs de grupo para operar sobre todos los bloques miembros sin listar cada uno individualmente.

## Ubicación del Archivo

```
Assets/Server/Item/Groups/<GroupId>.json
```

Ejemplos:
```
Assets/Server/Item/Groups/FullBlocks_Aqua.json
Assets/Server/Item/Groups/FullBlocks_Basalt.json
Assets/Server/Item/Groups/FullBlocks_Blackwood.json
Assets/Server/Item/Groups/Foods.json
Assets/Server/Item/Groups/Metal_Bars.json
Assets/Server/Item/Groups/Rock.json
Assets/Server/Item/Groups/Soils.json
Assets/Server/Item/Groups/Wood_All.json
```

## Esquema

| Campo | Tipo | Requerido | Por Defecto | Descripción |
|-------|------|-----------|-------------|-------------|
| `Blocks` | string[] | Sí | — | Arreglo de IDs de bloque/objeto que pertenecen a este grupo. Cada entrada es el ID exacto del objeto tal como se usa en las definiciones de objetos (ej. `"Rock_Aqua"`, `"Rock_Aqua_Cobble"`). |

## Ejemplos

`Assets/Server/Item/Groups/FullBlocks_Aqua.json`:

```json
{
  "Blocks": [
    "Rock_Aqua",
    "Rock_Aqua_Cobble"
  ]
}
```

`Assets/Server/Item/Groups/FullBlocks_Basalt.json`:

```json
{
  "Blocks": [
    "Rock_Basalt",
    "Rock_Basalt_Cobble"
  ]
}
```

`Assets/Server/Item/Groups/FullBlocks_Blackwood.json`:

```json
{
  "Blocks": [
    "Wood_Blackwood_Planks",
    "Wood_Blackwood_Decorative",
    "Wood_Blackwood_Ornate"
  ]
}
```

## Grupos Disponibles (Lista Parcial)

Los grupos cubren todas las familias principales de bloques. La convención de nomenclatura es `FullBlocks_<Material>` para conjuntos de bloques colocables y nombres simples para categorías de objetos/ingredientes:

| ID de Grupo | Descripción |
|-------------|-------------|
| `FullBlocks_Aqua` | Variantes de piedra aqua |
| `FullBlocks_Basalt` | Variantes de piedra basalto |
| `FullBlocks_Blackwood` | Variantes de tablones y decorativas de madera negra |
| `FullBlocks_Calcite` | Variantes de piedra calcita |
| `FullBlocks_Limestone` | Variantes de piedra caliza |
| `FullBlocks_Marble` | Variantes de mármol |
| `FullBlocks_Stone` | Variantes de piedra estándar |
| `FullBlocks_Softwood` | Variantes de tablones de madera blanda |
| `FullBlocks_Volcanic` | Variantes de piedra volcánica |
| `Foods` | Todos los objetos de comida |
| `Metal_Bars` | Todos los objetos de lingotes/barras de metal |
| `Rock` | Todos los tipos de bloque de roca |
| `Soils` | Todos los tipos de bloque de tierra |
| `Wood_All` | Todos los tipos de tablones de madera |
| `Wood_Trunk` | Todos los tipos de tronco de madera |
| `Bone` | Variantes de objetos de hueso |
| `Flowers` | Tipos de bloque de flores |
| `Mushrooms` | Tipos de bloque de hongos |
| `Meats` | Objetos de ingrediente de carne |
| `Fish` | Todos los objetos de pescado |
| `Fuel` | Objetos que pueden usarse como combustible |
| `Rubble` | Tipos de bloque de escombros |
| `Sands` | Tipos de arena y grava |

## Páginas Relacionadas

- [Definiciones de Objetos](/hytale-modding-docs/reference/item-system/item-definitions) — Definiciones de bloques y objetos que los grupos referencian
- [Definiciones de Bloques](/hytale-modding-docs/reference/item-system/block-definitions) — Propiedades de textura y material de bloques
- [Tipos de Recurso](/hytale-modding-docs/reference/item-system/resource-types) — Mecanismo alternativo de agrupación usado en entradas de recetas
