---
title: Definiciones de Bancos
description: Referencia de las definiciones de objetos de bancos de crafteo y procesamiento en Hytale, incluyendo configuración de BlockType.Bench, niveles de tier y requisitos de mejora.
---

## Descripción General

Los bancos son objetos de bloque colocables que habilitan recetas que requieren un ID de banco específico. Cada banco se define como un archivo de objeto estándar bajo `Assets/Server/Item/Items/Bench/`, con una sección `BlockType.Bench` que describe el tipo operacional del banco, categorías, eventos de sonido, sistema de tiers e interfaz. El mismo archivo de objeto también integra la receta usada para craftear el banco en sí.

## Ubicación del Archivo

```
Assets/Server/Item/Items/Bench/
```

Un archivo JSON por banco, ej. `Bench_WorkBench.json`, `Bench_Campfire.json`, `Bench_Furnace.json`.

## Esquema

### Campos a nivel de objeto (subconjunto relevante para bancos)

| Campo | Tipo | Requerido | Por Defecto | Descripción |
|-------|------|-----------|-------------|-------------|
| `TranslationProperties.Name` | `string` | Sí | — | Clave de localización para el nombre de visualización del banco. |
| `BlockType` | `object` | Sí | — | Definición de comportamiento de bloque. Ver abajo. |
| `Recipe` | `object` | No | — | Receta en línea para craftear este banco. Usa el esquema estándar de recetas. |
| `Tags.Type` | `string[]` | No | — | Debe incluir `"Bench"` para todos los objetos de banco. |
| `MaxStack` | `number` | No | — | Casi siempre `1` para bancos. |

### Campos de BlockType

| Campo | Tipo | Requerido | Por Defecto | Descripción |
|-------|------|-----------|-------------|-------------|
| `Material` | `string` | Sí | — | Clase de material físico (ej. `"Solid"`). |
| `DrawType` | `string` | Sí | — | Tipo de renderizado (ej. `"Model"`). |
| `CustomModel` | `string` | Sí | — | Ruta al archivo `.blockymodel`. |
| `Bench` | `BenchConfig` | Sí | — | Configuración principal del banco. Ver abajo. |
| `State` | `object` | No | — | Definiciones de estado visual (estados inactivo, crafteando, procesando). |
| `Gathering.Breaking.GatherType` | `string` | No | — | Tipo de recolección al romper el bloque (ej. `"Benches"`). |
| `VariantRotation` | `string` | No | — | Variantes de rotación (ej. `"NESW"`). |

### BenchConfig

| Campo | Tipo | Requerido | Por Defecto | Descripción |
|-------|------|-----------|-------------|-------------|
| `Type` | `"Crafting" \| "Processing"` | Sí | — | Determina si el banco muestra una cola de crafteo o una tubería de procesamiento. |
| `Id` | `string` | Sí | — | Identificador único del banco referenciado en `BenchRequirement.Id` de las recetas. |
| `Categories` | `CategoryEntry[]` | No | — | Solo bancos de crafteo. Pestañas de categoría nombradas mostradas en la interfaz. |
| `TierLevels` | `TierLevel[]` | No | — | Definiciones de tier de mejora. Cada entrada describe costos de mejora y bonificaciones. |
| `LocalOpenSoundEventId` | `string` | No | — | Sonido reproducido localmente cuando se abre la interfaz del banco. |
| `LocalCloseSoundEventId` | `string` | No | — | Sonido reproducido localmente cuando se cierra la interfaz del banco. |
| `CompletedSoundEventId` | `string` | No | — | Sonido reproducido cuando se completa un crafteo. |
| `FailedSoundEventId` | `string` | No | — | Sonido reproducido cuando falla un crafteo. |
| `AllowNoInputProcessing` | `boolean` | No | `false` | Solo bancos de procesamiento. Permite iniciar el procesamiento sin un conjunto completo de entradas. |
| `Fuel` | `FuelSlot[]` | No | — | Solo bancos de procesamiento. Define las ranuras de entrada de combustible. |
| `OutputSlotsCount` | `number` | No | — | Solo bancos de procesamiento. Número de ranuras de salida. |

### TierLevel

| Campo | Tipo | Requerido | Por Defecto | Descripción |
|-------|------|-----------|-------------|-------------|
| `UpgradeRequirement` | `object` | No | — | Materiales y tiempo necesarios para alcanzar este tier. |
| `UpgradeRequirement.Material` | `OutputEntry[]` | No | — | Objetos consumidos en la mejora. |
| `UpgradeRequirement.TimeSeconds` | `number` | No | — | Tiempo en segundos para completar la mejora. |
| `CraftingTimeReductionModifier` | `number` | No | `0` | Reducción fraccional aplicada a todos los `TimeSeconds` de recetas en este tier (ej. `0.15` = 15% más rápido). |

## Ejemplo

**Banco de crafteo** (`Assets/Server/Item/Items/Bench/Bench_WorkBench.json`, condensado):

```json
{
  "TranslationProperties": {
    "Name": "server.items.Bench_WorkBench.name"
  },
  "Recipe": {
    "Input": [
      { "Quantity": 4, "ResourceTypeId": "Wood_Trunk" },
      { "Quantity": 3, "ResourceTypeId": "Rock" }
    ],
    "BenchRequirement": [
      { "Type": "Crafting", "Categories": ["Tools"], "Id": "Fieldcraft" }
    ]
  },
  "BlockType": {
    "Bench": {
      "Type": "Crafting",
      "Id": "Workbench",
      "Categories": [
        { "Id": "Workbench_Survival", "Icon": "Icons/CraftingCategories/Workbench/WeaponsCrude.png", "Name": "server.benchCategories.workbench.survival" },
        { "Id": "Workbench_Tools",    "Icon": "Icons/CraftingCategories/Workbench/Tools.png",       "Name": "server.benchCategories.workbench.tools" }
      ],
      "TierLevels": [
        {
          "CraftingTimeReductionModifier": 0.0,
          "UpgradeRequirement": {
            "Material": [
              { "ItemId": "Ingredient_Bar_Copper", "Quantity": 30 },
              { "ItemId": "Ingredient_Bar_Iron",   "Quantity": 20 }
            ],
            "TimeSeconds": 5.0
          }
        },
        {
          "CraftingTimeReductionModifier": 0.15,
          "UpgradeRequirement": {
            "Material": [
              { "ItemId": "Ingredient_Bar_Thorium", "Quantity": 30 }
            ],
            "TimeSeconds": 10.0
          }
        },
        { "CraftingTimeReductionModifier": 0.3 }
      ],
      "LocalOpenSoundEventId": "SFX_Workbench_Open",
      "CompletedSoundEventId": "SFX_Workbench_Craft"
    }
  },
  "Tags": { "Type": ["Bench"] },
  "MaxStack": 1
}
```

**Banco de procesamiento** (`Assets/Server/Item/Items/Bench/Bench_Campfire.json`, condensado):

```json
{
  "BlockType": {
    "Bench": {
      "Type": "Processing",
      "Id": "Campfire",
      "AllowNoInputProcessing": true,
      "Fuel": [
        { "ResourceTypeId": "Fuel", "Icon": "Icons/Processing/FuelSlotIcon.png" }
      ],
      "OutputSlotsCount": 4
    }
  }
}
```

## Páginas Relacionadas

- [Recetas](/hytale-modding-docs/reference/crafting-system/recipes) — Formato de receta y campo de requisito de banco
- [Desguace](/hytale-modding-docs/reference/crafting-system/salvage) — El banco de desguace y su formato de receta
