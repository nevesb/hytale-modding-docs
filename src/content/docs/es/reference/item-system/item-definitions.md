---
title: Definiciones de Objetos
description: Referencia de los archivos JSON de definición de objetos en Hytale, cubriendo campos para comida, armas, herramientas y todos los objetos colocables.
---

## Descripción General

Las definiciones de objetos son archivos JSON que describen cada objeto en Hytale — comida, armas, herramientas, bloques y más. Cada archivo se encuentra en una subcarpeta de categoría bajo `Assets/Server/Item/Items/` y puede extender una plantilla padre para heredar campos compartidos. El subobjeto `BlockType` controla cómo se ve el objeto cuando se coloca en el mundo.

## Ubicación del Archivo

```
Assets/Server/Item/Items/<Category>/<ItemId>.json
```

Ejemplos:
- `Assets/Server/Item/Items/Food/Food_Bread.json`
- `Assets/Server/Item/Items/Weapon/Axe/Weapon_Axe_Copper.json`
- `Assets/Server/Item/Items/Tool/Pickaxe/Tool_Pickaxe_Copper.json`

## Esquema

### Campos de Nivel Superior

| Campo | Tipo | Requerido | Por Defecto | Descripción |
|-------|------|-----------|-------------|-------------|
| `Parent` | string | No | — | ID de un objeto plantilla del cual heredar campos (ej. `"Template_Food"`). |
| `TranslationProperties` | object | Sí | — | Claves de localización para el texto de visualización del objeto. |
| `TranslationProperties.Name` | string | Sí | — | Clave de localización para el nombre del objeto (ej. `"server.items.Food_Bread.name"`). |
| `TranslationProperties.Description` | string | No | — | Clave de localización para la descripción del objeto. |
| `Quality` | string | No | — | ID del nivel de calidad. Uno de `Junk`, `Common`, `Uncommon`, `Rare`, `Epic`, `Legendary`, `Tool`, `Developer`, `Template`. |
| `Icon` | string | No | — | Ruta a la imagen del icono del objeto (ej. `"Icons/ItemsGenerated/Food_Bread.png"`). |
| `Categories` | string[] | No | — | Lista de IDs de categoría en las que aparece este objeto (ej. `["Items.Foods"]`). |
| `ItemLevel` | number | No | — | Nivel de poder del objeto usado por los sistemas de progresión y desbloqueo de crafteo. |
| `MaxStack` | number | No | — | Número máximo de este objeto que puede apilarse en una ranura de inventario. |
| `DropOnDeath` | boolean | No | `false` | Si este objeto se suelta cuando el jugador que lo lleva muere. |
| `Scale` | number | No | `1.0` | Escala visual de la entidad del objeto cuando se suelta en el mundo. |
| `Interactions` | object | No | — | Mapea nombres de ranuras de interacción (ej. `Primary`, `Secondary`) a IDs de cadenas de interacción. |
| `InteractionVars` | object | No | — | Sobrecargas de variables de interacción con nombre. Cada clave es un nombre de variable; cada valor tiene un arreglo `Interactions` de cadenas en línea o referenciadas por padre. |
| `Recipe` | object | No | — | Receta de crafteo para este objeto. Ver campos de Receta abajo. |
| `BlockType` | object | No | — | Controla cómo aparece el objeto cuando se coloca como bloque en el mundo. Ver campos de BlockType abajo. |
| `ResourceTypes` | object[] | No | — | Lista de objetos `{ "Id": "<ResourceTypeId>" }`. Marca este objeto como perteneciente a grupos de recursos usados en recetas. |
| `Tags` | object | No | — | Grupos de etiquetas clave-valor (ej. `{ "Type": ["Food"], "Family": ["Axe"] }`). Usados para filtrado e interacciones. |
| `MaxDurability` | number | No | — | Durabilidad máxima para herramientas y armas. |
| `DurabilityLossOnHit` | number | No | — | Durabilidad perdida por golpe para armas. |
| `Weapon` | object | No | — | Marca este objeto como un arma. Generalmente un objeto vacío `{}` que activa el comportamiento de arma. |
| `Tool` | object | No | — | Configuración de herramienta incluyendo `Specs` (poder de recolección por tipo de bloque) y `DurabilityLossBlockTypes`. |
| `Consumable` | boolean | No | — | Marca este objeto como consumible. |
| `PlayerAnimationsId` | string | No | — | ID del conjunto de animaciones usado cuando el jugador sostiene este objeto (ej. `"Axe"`, `"Item"`). |
| `Model` | string | No | — | Ruta al archivo `.blockymodel` para el modelo sostenido de arma/herramienta (ej. `"Items/Weapons/Axe/Copper.blockymodel"`). |
| `Texture` | string | No | — | Ruta a la textura usada con `Model`. |

### Campos de BlockType

| Campo | Tipo | Requerido | Por Defecto | Descripción |
|-------|------|-----------|-------------|-------------|
| `Material` | string | No | — | Tipo de material físico. Uno de `Solid`, `Fluid`, `Empty`, `Plant`. |
| `DrawType` | string | No | — | Estilo de renderizado. Valores comunes: `Model`, `Block`, `Plant`. |
| `Opacity` | string | No | — | Nivel de transparencia. Uno de `Opaque`, `Semitransparent`, `Transparent`. |
| `CustomModel` | string | No | — | Ruta al archivo `.blockymodel` usado cuando el objeto se coloca como bloque (ej. `"Items/Consumables/Food/Bread.blockymodel"`). |
| `CustomModelTexture` | object[] | No | — | Arreglo de objetos `{ "Texture": "<ruta>", "Weight": <número> }` para variantes de textura aleatorias. |
| `CustomModelScale` | number | No | `1.0` | Multiplicador de escala aplicado al modelo personalizado. |
| `HitboxType` | string | No | — | ID de la forma de hitbox (ej. `"Food_Medium"`, `"Food_Large"`). |
| `RandomRotation` | string | No | — | Modo de aleatorización de rotación aplicado al colocarse (ej. `"YawStep1"`). |
| `ParticleColor` | string | No | — | Color hexadecimal usado para las partículas de rotura de bloque (ej. `"#e4cb69"`). |
| `Textures` | object[] | No | — | Para bloques colocables: arreglo de objetos de textura con claves por cara. Cada entrada puede tener `All`, `Sides`, `UpDown`, `Top`, `Bottom`, `North`, `South`, `East`, `West`, y un `Weight` para variantes aleatorias. |
| `Gathering` | object | No | — | Define qué tipos de recolección aplican cuando este bloque se cosecha o rompe (`Harvest`, `Soft`, `Breaking`). |

### Campos de Receta

| Campo | Tipo | Requerido | Por Defecto | Descripción |
|-------|------|-----------|-------------|-------------|
| `Input` | object[] | Sí | — | Arreglo de objetos de ingredientes. Cada uno tiene `ItemId` o `ResourceTypeId`, más un `Quantity` opcional (por defecto `1`). |
| `Output` | object[] | No | — | Arreglo de objetos de salida con `ItemId` y `Quantity` opcional. Por defecto es el objeto mismo con cantidad 1. |
| `OutputQuantity` | number | No | `1` | Atajo para establecer la cantidad de salida cuando el objeto de salida es el propio objeto de la definición. |
| `BenchRequirement` | object[] | No | — | Arreglo de requisitos de banco. Cada uno tiene `Type` (`"Crafting"`, `"Processing"`, `"StructuralCrafting"`), `Id` (ID del banco) y un arreglo `Categories` opcional. |
| `TimeSeconds` | number | No | `0` | Duración del crafteo en segundos. |
| `KnowledgeRequired` | boolean | No | `true` | Si el jugador debe haber aprendido esta receta antes de craftearla. |

## Ejemplo

`Assets/Server/Item/Items/Food/Food_Bread.json`:

```json
{
  "TranslationProperties": {
    "Name": "server.items.Food_Bread.name",
    "Description": "server.items.Food_Bread.description"
  },
  "Parent": "Template_Food",
  "Interactions": {
    "Secondary": "Root_Secondary_Consume_Food_T2"
  },
  "Quality": "Uncommon",
  "Icon": "Icons/ItemsGenerated/Food_Bread.png",
  "BlockType": {
    "Material": "Empty",
    "DrawType": "Model",
    "Opacity": "Semitransparent",
    "CustomModel": "Items/Consumables/Food/Bread.blockymodel",
    "CustomModelTexture": [
      {
        "Texture": "Items/Consumables/Food/Bread_Texture.png",
        "Weight": 1
      }
    ],
    "HitboxType": "Food_Medium",
    "RandomRotation": "YawStep1",
    "CustomModelScale": 0.5,
    "ParticleColor": "#e4cb69"
  },
  "InteractionVars": {
    "Consume_Charge": {
      "Interactions": [
        {
          "Parent": "Consume_Charge_Food_T1_Inner",
          "Effects": {
            "Particles": [
              {
                "SystemId": "Food_Eat",
                "Color": "#DCC15D",
                "TargetNodeName": "Mouth",
                "TargetEntityPart": "Entity"
              }
            ]
          }
        }
      ]
    },
    "Effect": {
      "Interactions": [
        {
          "Type": "ApplyEffect",
          "EffectId": "Food_Instant_Heal_Bread"
        }
      ]
    }
  },
  "Recipe": {
    "Input": [
      {
        "ItemId": "Ingredient_Dough",
        "Quantity": 1
      },
      {
        "ResourceTypeId": "Fuel",
        "Quantity": 3
      }
    ],
    "Output": [
      {
        "ItemId": "Food_Bread"
      }
    ],
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Id": "Cookingbench",
        "Categories": [
          "Baked"
        ]
      }
    ],
    "TimeSeconds": 5
  },
  "Scale": 1.5,
  "ItemLevel": 7,
  "MaxStack": 25,
  "DropOnDeath": true
}
```

## Páginas Relacionadas

- [Definiciones de Bloques](/hytale-modding-docs/reference/item-system/block-definitions) — Campos de textura y material específicos de bloques
- [Calidades de Objetos](/hytale-modding-docs/reference/item-system/item-qualities) — Definiciones de niveles de calidad
- [Interacciones de Objetos](/hytale-modding-docs/reference/item-system/item-interactions) — Referencia de cadenas de interacción
- [Categorías de Objetos](/hytale-modding-docs/reference/item-system/item-categories) — Jerarquía de categorías
- [Tipos de Recurso](/hytale-modding-docs/reference/item-system/resource-types) — IDs de tipos de recurso usados en recetas
