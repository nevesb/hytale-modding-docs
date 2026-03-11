---
title: Requisitos de Banco
description: Referencia del campo BenchRequirement en las recetas de Hytale, que vincula recetas de crafteo a bancos, categorías y niveles de tier específicos.
---

## Descripción General

El campo `BenchRequirement` en una receta determina con qué banco de crafteo el jugador debe interactuar para craftear ese objeto. Conecta el sistema de recetas al sistema de bancos especificando un ID de banco, tipo de banco, uno o más filtros de categoría y un nivel de tier opcional. Una receta puede listar múltiples requisitos de banco, permitiéndole aparecer en más de un banco. Las recetas sin `BenchRequirement` (o con un requisito de `Fieldcraft`) pueden craftearse desde el inventario del jugador sin un banco colocado.

## Ubicación del Archivo

Los requisitos de banco aparecen en línea dentro de las definiciones de recetas:

```
Assets/Server/Item/Items/Bench/*.json     (integrados en Recipe.BenchRequirement)
Assets/Server/Item/Items/**/*.json        (cualquier objeto con una Recipe en línea)
Assets/Server/Item/Recipes/**/*.json      (archivos de receta independientes)
```

Los objetos de banco en sí se encuentran en:

```
Assets/Server/Item/Items/Bench/
  Bench_Alchemy.json
  Bench_Arcane.json
  Bench_Armory.json
  Bench_Armour.json
  Bench_Builders.json
  Bench_Campfire.json
  Bench_Cooking.json
  Bench_Farming.json
  Bench_Furnace.json
  Bench_Furniture.json
  Bench_Loom.json
  Bench_Lumbermill.json
  Bench_Memories.json
  Bench_Salvage.json
  Bench_Tannery.json
  Bench_Trough.json
  Bench_Weapon.json
  Bench_WorkBench.json
```

## Esquema

### BenchRequirement (elemento del arreglo)

| Campo | Tipo | Requerido | Por Defecto | Descripción |
|-------|------|-----------|-------------|-------------|
| `Id` | `string` | Sí | — | Identificador del banco que debe coincidir con el `BlockType.Bench.Id` de un banco colocado. Valores conocidos incluyen `"Workbench"`, `"Cookingbench"`, `"Furnace"`, `"Campfire"`, `"Alchemybench"`, `"Loombench"`, `"Fieldcraft"`. |
| `Type` | `string` | Sí | — | Tipo operacional del banco. Valores conocidos: `"Crafting"` (selección manual de recetas), `"Processing"` (basado en entrada con combustible). |
| `Categories` | `string[]` | No | — | Lista de IDs de categoría del banco a los que pertenece la receta. Estos corresponden a las pestañas `BlockType.Bench.Categories[].Id` mostradas en la interfaz del banco (ej. `"Workbench_Crafting"`, `"Prepared"`, `"Baked"`, `"Tools"`). |
| `RequiredTierLevel` | `number` | No | — | Nivel mínimo de tier del banco requerido para desbloquear esta receta. Los tiers comienzan en `1` (banco base); valores más altos requieren mejoras del banco. |

### Cómo los IDs se conectan a las definiciones de banco

Cada objeto de banco define un objeto `BlockType.Bench` con un campo `Id` y un arreglo `Categories`. Cuando una receta especifica `BenchRequirement[].Id = "Workbench"`, el motor lo empareja con cualquier banco colocado cuyo `BlockType.Bench.Id` sea igual a `"Workbench"`. El arreglo `Categories` en el requisito determina bajo qué pestaña de la interfaz de ese banco aparece la receta.

```
Recipe.BenchRequirement[].Id  ──coincide con──>  BlockType.Bench.Id
Recipe.BenchRequirement[].Categories  ──filtra──>  BlockType.Bench.Categories[].Id
```

## Ejemplos

**Requisito básico de banco de trabajo** (de `Bench_Cooking.json`):

```json
{
  "BenchRequirement": [
    {
      "Type": "Crafting",
      "Id": "Workbench",
      "Categories": [
        "Workbench_Crafting"
      ]
    }
  ]
}
```

El banco de cocina debe craftearse en un banco de trabajo, bajo la pestaña de categoría "Crafting".

**Requisito con compuerta de tier** (de `Bench_Alchemy.json`):

```json
{
  "BenchRequirement": [
    {
      "Id": "Workbench",
      "Type": "Crafting",
      "Categories": [
        "Workbench_Crafting"
      ],
      "RequiredTierLevel": 2
    }
  ]
}
```

El banco de alquimia requiere un banco de trabajo de tier 2 (mejorado) para craftearse.

**Múltiples requisitos de banco** (de `Bench_Campfire.json`):

```json
{
  "BenchRequirement": [
    {
      "Type": "Crafting",
      "Categories": [
        "Tools"
      ],
      "Id": "Fieldcraft"
    },
    {
      "Id": "Workbench",
      "Type": "Crafting",
      "Categories": [
        "Workbench_Survival"
      ]
    }
  ]
}
```

La receta de fogata aparece en dos ubicaciones: el menú de crafteo de campo del jugador (bajo "Tools") y la interfaz del banco de trabajo (bajo "Survival"). Esto permite al jugador craftearla en cualquiera de las dos estaciones.

**Receta sin requisito de banco** (de `Bench_Loom.json`):

```json
{
  "Recipe": {
    "Input": [
      { "Quantity": 5, "ResourceTypeId": "Wood_Trunk" },
      { "ItemId": "Ingredient_Fabric_Scrap_Cotton", "Quantity": 3 }
    ]
  }
}
```

Cuando `BenchRequirement` se omite por completo, la receta puede craftearse sin ningún banco.

## Páginas Relacionadas

- [Definiciones de Bancos](/hytale-modding-docs/reference/crafting-system/bench-definitions) — Esquema completo del objeto de banco incluyendo configuración de `BlockType.Bench` y mejoras de tier
- [Recetas](/hytale-modding-docs/reference/crafting-system/recipes) — Esquema de entrada/salida de recetas donde se integra `BenchRequirement`
- [Desguace](/hytale-modding-docs/reference/crafting-system/salvage) — Recetas de procesamiento del banco de desguace
