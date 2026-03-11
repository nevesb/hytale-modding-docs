---
title: Tipos de Recurso
description: Referencia de los archivos JSON de tipos de recurso en Hytale, que definen categorías de ingredientes nombradas usadas como entradas flexibles de recetas.
---

## Descripción General

Los tipos de recurso son categorías de ingredientes nombradas que permiten a las recetas de crafteo aceptar cualquier objeto perteneciente a un grupo en lugar de requerir un ID de objeto específico. Por ejemplo, una receta con `ResourceTypeId: "Meats"` aceptará cualquier objeto etiquetado con el tipo de recurso `Meats`. Los objetos declaran su membresía de tipo de recurso a través del arreglo `ResourceTypes` en su definición de objeto.

## Ubicación del Archivo

```
Assets/Server/Item/ResourceTypes/<ResourceTypeId>.json
```

## Esquema

Los archivos de tipo de recurso son mínimos. La mayoría contiene solo una ruta de icono; la lista de membresía se define del lado del objeto a través de `ResourceTypes` en cada definición de objeto.

| Campo | Tipo | Requerido | Por Defecto | Descripción |
|-------|------|-----------|-------------|-------------|
| `Icon` | string | No | — | Ruta a la imagen del icono mostrada en la interfaz de recetas para representar este tipo de recurso (ej. `"Icons/ResourceTypes/Any_Meat.png"`). |

## Tipos de Recurso Disponibles (Lista Parcial)

| ID de Tipo de Recurso | Icono |
|-----------------------|-------|
| `Bone` | `Icons/ResourceTypes/Any_Bone.png` |
| `Books` | — |
| `Bricks` | — |
| `Charcoal` | — |
| `Clays` | — |
| `Copper_Iron_Bar` | — |
| `Fish` | — |
| `Fish_Common` | — |
| `Fish_Epic` | — |
| `Fish_Legendary` | — |
| `Fish_Rare` | — |
| `Fish_Uncommon` | — |
| `Flowers` | — |
| `Foods` | — |
| `Fruits` | — |
| `Fuel` | `Icons/ResourceTypes/Fuel.png` |
| `Ice` | — |
| `Meats` | `Icons/ResourceTypes/Any_Meat.png` |
| `Metal_Bars` | `Icons/ResourceTypes/Rock.png` |
| `Milk_Bucket` | — |
| `Moss` | — |
| `Mushrooms` | — |
| `Rock` | — |
| `Rubble` | — |
| `Salvage_*` | — |
| `Sands` | — |
| `Soils` | — |
| `Vegetables` | — |
| `Wood_All` | — |
| `Wood_Trunk` | — |

## Ejemplos

`Assets/Server/Item/ResourceTypes/Meats.json`:

```json
{
  "Icon": "Icons/ResourceTypes/Any_Meat.png"
}
```

`Assets/Server/Item/ResourceTypes/Fuel.json`:

```json
{
  "Icon": "Icons/ResourceTypes/Fuel.png"
}
```

`Assets/Server/Item/ResourceTypes/Foods.json`:

```json
{}
```

## Cómo los Objetos Declaran Membresía de Tipo de Recurso

En una definición de objeto, agrega un arreglo `ResourceTypes` con una entrada por cada tipo al que pertenece el objeto:

```json
{
  "ResourceTypes": [
    { "Id": "Meats" }
  ]
}
```

Un objeto puede pertenecer a múltiples tipos de recurso. Por ejemplo, `Food_Fish_Raw` pertenece tanto a `Fish` como a los tipos de comida de la plantilla padre.

## Cómo las Recetas Referencian Tipos de Recurso

En una entrada `Input` de receta, usa `ResourceTypeId` en lugar de `ItemId`:

```json
{
  "Recipe": {
    "Input": [
      {
        "ResourceTypeId": "Fuel",
        "Quantity": 3
      },
      {
        "ResourceTypeId": "Fish",
        "Quantity": 1
      }
    ]
  }
}
```

Esto permite que la receta acepte cualquier objeto etiquetado con el tipo de recurso correspondiente, en lugar de requerir un objeto específico.

## Páginas Relacionadas

- [Definiciones de Objetos](/hytale-modding-docs/reference/item-system/item-definitions) — Donde se declara la membresía de `ResourceTypes` en los objetos
- [Grupos de Objetos](/hytale-modding-docs/reference/item-system/item-groups) — Conjuntos nombrados de bloques (sistema de agrupación complementario)
- [Categorías de Objetos](/hytale-modding-docs/reference/item-system/item-categories) — Jerarquía de categorías de interfaz para menús
