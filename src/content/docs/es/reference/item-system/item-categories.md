---
title: Categorías de Objetos
description: Referencia de los archivos JSON de categorías de objetos en Hytale, definiendo el árbol jerárquico de categorías usado en menús de crafteo y la biblioteca creativa.
---

## Descripción General

Las categorías de objetos definen la estructura de árbol que organiza los objetos en los menús de crafteo y la biblioteca creativa. Cada archivo JSON representa un nodo de categoría de nivel superior y contiene una lista ordenada de entradas de categoría hijas. Los objetos se asignan a categorías a través del arreglo `Categories` en su definición de objeto.

## Ubicación del Archivo

```
Assets/Server/Item/Category/<LibraryId>/<CategoryId>.json
```

Las dos raíces de biblioteca son:
- `Assets/Server/Item/Category/CreativeLibrary/` — Navegador de objetos del modo creativo (Blocks, Furniture, Items, Tool)
- `Assets/Server/Item/Category/Fieldcraft/` — Menús de crafteo de supervivencia (Tools)

## Esquema

### Campos del Archivo de Categoría

| Campo | Tipo | Requerido | Por Defecto | Descripción |
|-------|------|-----------|-------------|-------------|
| `Icon` | string | Sí | — | Ruta a la imagen del icono para esta categoría de nivel superior (ej. `"Icons/ItemCategories/Natural.png"`). |
| `Order` | number | No | `0` | Orden de clasificación de esta categoría relativo a sus hermanos. Valores más bajos aparecen primero. |
| `Name` | string | No | — | Clave de localización para el nombre de visualización de la categoría (usado en nodos hoja/subcategoría). |
| `Children` | object[] | No | — | Arreglo ordenado de entradas de categoría hijas. |

### Campos de Entrada de Children

| Campo | Tipo | Requerido | Por Defecto | Descripción |
|-------|------|-----------|-------------|-------------|
| `Id` | string | Sí | — | Identificador único para esta categoría hija. Usado como el segundo segmento en los valores de `Categories` del objeto (ej. `"Foods"` se mapea a `"Items.Foods"`). |
| `Name` | string | Sí | — | Clave de localización para la etiqueta de visualización de la categoría hija (ej. `"server.ui.itemcategory.foods"`). |
| `Icon` | string | Sí | — | Ruta a la imagen del icono para esta categoría hija. |

## Ejemplo

`Assets/Server/Item/Category/CreativeLibrary/Blocks.json`:

```json
{
  "Icon": "Icons/ItemCategories/Natural.png",
  "Order": 0,
  "Children": [
    {
      "Id": "Rocks",
      "Name": "server.ui.itemcategory.rocks",
      "Icon": "Icons/ItemCategories/Blocks.png"
    },
    {
      "Id": "Structural",
      "Name": "server.ui.itemcategory.structural",
      "Icon": "Icons/ItemCategories/Build-Roofs.png"
    },
    {
      "Id": "Soils",
      "Name": "server.ui.itemcategory.soils",
      "Icon": "Icons/ItemCategories/Soil.png"
    },
    {
      "Id": "Ores",
      "Name": "server.ui.itemcategory.ores",
      "Icon": "Icons/ItemCategories/Natural-Ore.png"
    },
    {
      "Id": "Plants",
      "Name": "server.ui.itemcategory.plants",
      "Icon": "Icons/ItemCategories/Natural-Vegetal.png"
    },
    {
      "Id": "Fluids",
      "Name": "server.ui.itemcategory.fluids",
      "Icon": "Icons/ItemCategories/Natural-Fluid.png"
    },
    {
      "Id": "Portals",
      "Name": "server.ui.itemcategory.portals",
      "Icon": "Icons/ItemCategories/Portal.png"
    },
    {
      "Id": "Deco",
      "Name": "server.ui.itemcategory.deco",
      "Icon": "Icons/ItemCategories/Natural-Fire.png"
    }
  ]
}
```

`Assets/Server/Item/Category/CreativeLibrary/Items.json`:

```json
{
  "Icon": "Icons/ItemCategories/Items.png",
  "Order": 2,
  "Children": [
    {
      "Id": "Tools",
      "Name": "server.ui.itemcategory.tools",
      "Icon": "Icons/ItemCategories/Items-Tools.png"
    },
    {
      "Id": "Weapons",
      "Name": "server.ui.itemcategory.weapons",
      "Icon": "Icons/ItemCategories/Items-Weapons.png"
    },
    {
      "Id": "Armors",
      "Name": "server.ui.itemcategory.armors",
      "Icon": "Icons/ItemCategories/Items-Armor.png"
    },
    {
      "Id": "Foods",
      "Name": "server.ui.itemcategory.foods",
      "Icon": "Icons/ItemCategories/Items-Food.png"
    },
    {
      "Id": "Potions",
      "Name": "server.ui.itemcategory.potions",
      "Icon": "Icons/ItemCategories/Items-Potion.png"
    },
    {
      "Id": "Recipes",
      "Name": "server.ui.itemcategory.recipes",
      "Icon": "Icons/ItemCategories/Items-Recipe.png"
    },
    {
      "Id": "Ingredients",
      "Name": "server.ui.itemcategory.ingredients",
      "Icon": "Icons/ItemCategories/Items-Ingredients.png"
    }
  ]
}
```

## Asignación de Objetos a Categorías

En un archivo de definición de objeto, establece el campo `Categories` como una lista de cadenas `"<LibraryId>.<ChildId>"`:

```json
{
  "Categories": [
    "Items.Foods"
  ]
}
```

Un solo objeto puede pertenecer a múltiples categorías agregando más entradas al arreglo.

## Páginas Relacionadas

- [Definiciones de Objetos](/hytale-modding-docs/reference/item-system/item-definitions) — Donde se establece el campo `Categories` en los objetos
- [Grupos de Objetos](/hytale-modding-docs/reference/item-system/item-groups) — Conjuntos nombrados de bloques/objetos (distintos de las categorías)
- [Tipos de Recurso](/hytale-modding-docs/reference/item-system/resource-types) — Agrupaciones de recursos usadas en recetas
