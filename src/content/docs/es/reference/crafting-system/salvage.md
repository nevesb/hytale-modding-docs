---
title: Desguace
description: Referencia de las definiciones de recetas de desguace en Hytale, que descomponen objetos en sus materiales constituyentes en un Banco de Desguace.
---

## Descripción General

Las recetas de desguace definen cómo los objetos existentes se descomponen en materias primas en el Banco de Desguace. Usan el mismo esquema base de recetas que las recetas de crafteo pero siempre tienen exactamente un objeto de entrada, múltiples salidas y un `BenchRequirement` que apunta al banco de procesamiento `"Salvagebench"`. El campo `PrimaryOutput` identifica el material recuperado más valioso mostrado en la interfaz.

## Ubicación del Archivo

```
Assets/Server/Item/Recipes/Salvage/
```

Un archivo JSON por objeto desguazable, nombrado `Salvage_<ItemId>.json`, ej. `Salvage_Armor_Adamantite_Chest.json`.

## Esquema

Las recetas de desguace comparten el [esquema completo de recetas](/hytale-modding-docs/reference/crafting-system/recipes). Los campos usados en la práctica son:

| Campo | Tipo | Requerido | Por Defecto | Descripción |
|-------|------|-----------|-------------|-------------|
| `Input` | `InputEntry[]` | Sí | — | Arreglo de un solo elemento que identifica el objeto a desguazar. Siempre usa `ItemId`. |
| `Input[].ItemId` | `string` | Sí | — | El ID del objeto que se está desguazando. |
| `Input[].Quantity` | `number` | Sí | — | Siempre `1` para desguace. |
| `PrimaryOutput` | `OutputEntry` | Sí | — | El material recuperado principal mostrado como resultado destacado en la interfaz. |
| `PrimaryOutput.ItemId` | `string` | Sí | — | ID del objeto del material recuperado principal. |
| `PrimaryOutput.Quantity` | `number` | Sí | — | Cantidad del material principal recuperado. |
| `Output` | `OutputEntry[]` | Sí | — | Lista completa de todos los materiales recuperados, incluyendo la salida principal y cualquier material secundario. |
| `Output[].ItemId` | `string` | Sí | — | ID del objeto del material recuperado. |
| `Output[].Quantity` | `number` | Sí | — | Cantidad recuperada. |
| `BenchRequirement` | `BenchRequirement[]` | Sí | — | Siempre `[{ "Type": "Processing", "Id": "Salvagebench" }]`. |
| `TimeSeconds` | `number` | Sí | — | Tiempo de procesamiento en segundos en el Banco de Desguace. |

## Ejemplos

**Pechera de adamantita** (`Salvage_Armor_Adamantite_Chest.json`):

```json
{
  "Input": [
    {
      "ItemId": "Armor_Adamantite_Chest",
      "Quantity": 1
    }
  ],
  "PrimaryOutput": {
    "ItemId": "Ore_Adamantite",
    "Quantity": 6
  },
  "Output": [
    {
      "ItemId": "Ore_Adamantite",
      "Quantity": 6
    },
    {
      "ItemId": "Ingredient_Hide_Heavy",
      "Quantity": 2
    },
    {
      "ItemId": "Ingredient_Fabric_Scrap_Cindercloth",
      "Quantity": 2
    }
  ],
  "BenchRequirement": [
    {
      "Type": "Processing",
      "Id": "Salvagebench"
    }
  ],
  "TimeSeconds": 4
}
```

**Pechera de tela de algodón** (`Salvage_Armor_Cloth_Cotton_Chest.json`):

```json
{
  "Input": [
    {
      "ItemId": "Armor_Cloth_Cotton_Chest",
      "Quantity": 1
    }
  ],
  "PrimaryOutput": {
    "ItemId": "Ingredient_Fabric_Scrap_Cotton",
    "Quantity": 4
  },
  "Output": [
    {
      "ItemId": "Ingredient_Fabric_Scrap_Cotton",
      "Quantity": 4
    }
  ],
  "BenchRequirement": [
    {
      "Type": "Processing",
      "Id": "Salvagebench"
    }
  ],
  "TimeSeconds": 2
}
```

## Páginas Relacionadas

- [Recetas](/hytale-modding-docs/reference/crafting-system/recipes) — Esquema base de recetas
- [Definiciones de Bancos](/hytale-modding-docs/reference/crafting-system/bench-definitions) — Definición del objeto Banco de Desguace
