---
title: Crear un Banco de Crafteo Personalizado
description: Tutorial paso a paso para agregar un banco de crafteo personalizado con categorías de recetas, mejoras por niveles y recetas de objetos que lo utilicen.
sidebar:
  order: 4
---

## Objetivo

Construir un **Banco de Runecrafting** personalizado que los jugadores puedan colocar en el mundo y usar para fabricar objetos mágicos. Definirás el objeto del banco con categorías de crafteo, configurarás mejoras basadas en niveles y crearás recetas de objetos que requieran el banco.

## Lo que Aprenderás

- Cómo se definen los bancos de crafteo usando la propiedad `Bench` del tipo de bloque
- Cómo crear categorías que organizan las recetas dentro de la interfaz del banco
- Cómo los niveles de tier desbloquean recetas progresivamente más difíciles
- Cómo las recetas de objetos referencian un banco mediante `BenchRequirement`

## Requisitos Previos

- Una carpeta de mod con un `manifest.json` válido (ver [Configura tu Entorno de Desarrollo](/es/hytale-modding-docs/tutorials/beginner/setup-dev-environment))
- Familiaridad con definiciones de bloques (ver [Crear un Bloque Personalizado](/es/hytale-modding-docs/tutorials/beginner/create-a-block))
- Familiaridad con definiciones de objetos (ver [Crear un Objeto Personalizado](/es/hytale-modding-docs/tutorials/beginner/create-an-item))

---

## Paso 1: Crear la Definición del Objeto del Banco

Los bancos de crafteo en Hytale son objetos con un `BlockType` que contiene un objeto `Bench`. El objeto `Bench` define el tipo del banco, su ID único, categorías y niveles de tier. El Banco de Agricultura vanilla (`Bench_Farming.json`) y el Banco de Armas (`Bench_Weapon.json`) siguen este patrón.

Crea la definición de tu banco en:

```
YourMod/Assets/Server/Item/Items/Bench/Bench_Runecrafting.json
```

```json
{
  "TranslationProperties": {
    "Name": "server.items.Bench_Runecrafting.name",
    "Description": "server.items.Bench_Runecrafting.description"
  },
  "Icon": "Icons/ItemsGenerated/Bench_Runecrafting.png",
  "Categories": [
    "Furniture.Benches"
  ],
  "MaxStack": 1,
  "ItemLevel": 4,
  "BlockType": {
    "Material": "Solid",
    "DrawType": "Model",
    "Opacity": "Transparent",
    "CustomModel": "Blocks/Benches/Runecrafting.blockymodel",
    "CustomModelTexture": [
      {
        "Texture": "Blocks/Benches/Runecrafting_Texture.png",
        "Weight": 1
      }
    ],
    "HitboxType": "Bench_Runecrafting",
    "VariantRotation": "NESW",
    "Bench": {
      "Type": "Crafting",
      "Id": "Runecraftingbench",
      "Categories": [
        {
          "Id": "Runes",
          "Icon": "Icons/CraftingCategories/Runecrafting/Runes.png",
          "Name": "server.benchCategories.runecraftingbench.runes"
        },
        {
          "Id": "Enchantments",
          "Icon": "Icons/CraftingCategories/Runecrafting/Enchantments.png",
          "Name": "server.benchCategories.runecraftingbench.enchantments"
        },
        {
          "Id": "Scrolls",
          "Icon": "Icons/CraftingCategories/Runecrafting/Scrolls.png",
          "Name": "server.benchCategories.runecraftingbench.scrolls"
        }
      ],
      "LocalOpenSoundEventId": "SFX_Bench_Placeholder",
      "LocalCloseSoundEventId": "SFX_Bench_Placeholder",
      "CompletedSoundEventId": "SFX_Bench_Placeholder",
      "BenchUpgradeSoundEventId": "SFX_Workbench_Upgrade_Start_Default",
      "BenchUpgradeCompletedSoundEventId": "SFX_Workbench_Upgrade_Complete_Default",
      "TierLevels": [
        {
          "CraftingTimeReductionModifier": 0.0,
          "UpgradeRequirement": {
            "Material": [
              {
                "ItemId": "Ingredient_Crystal_Cyan",
                "Quantity": 10
              },
              {
                "ItemId": "Ingredient_Bar_Iron",
                "Quantity": 5
              }
            ],
            "TimeSeconds": 3
          }
        },
        {
          "CraftingTimeReductionModifier": 0.15,
          "UpgradeRequirement": {
            "Material": [
              {
                "ItemId": "Ingredient_Crystal_Cyan",
                "Quantity": 25
              },
              {
                "ItemId": "Ingredient_Bar_Thorium",
                "Quantity": 10
              }
            ],
            "TimeSeconds": 3
          }
        },
        {
          "CraftingTimeReductionModifier": 0.3
        }
      ]
    },
    "State": {
      "Id": "crafting",
      "Definitions": {
        "CraftCompleted": {}
      }
    },
    "Gathering": {
      "Breaking": {
        "GatherType": "Benches"
      }
    },
    "BlockParticleSetId": "Stone",
    "ParticleColor": "#4488cc",
    "Support": {
      "Down": [
        {
          "FaceType": "Full"
        }
      ]
    },
    "BlockSoundSetId": "Stone"
  },
  "Recipe": {
    "TimeSeconds": 3,
    "Input": [
      {
        "ResourceTypeId": "Rock",
        "Quantity": 10
      },
      {
        "ItemId": "Ingredient_Crystal_Cyan",
        "Quantity": 5
      }
    ],
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Id": "Workbench",
        "Categories": [
          "Workbench_Crafting"
        ]
      }
    ]
  },
  "PlayerAnimationsId": "Block",
  "Tags": {
    "Type": [
      "Bench"
    ]
  },
  "ItemSoundSetId": "ISS_Blocks_Wood"
}
```

### Campos clave del banco explicados

| Campo | Propósito |
|-------|-----------|
| `Bench.Type` | Debe ser `"Crafting"` para bancos basados en recetas |
| `Bench.Id` | Identificador único que las recetas referencian en su `BenchRequirement`. Es la cadena que conecta las recetas a este banco |
| `Bench.Categories` | Array de pestañas de categorías mostradas en la interfaz del banco. Cada una tiene un `Id`, `Icon` y un `Name` de traducción |
| `Bench.TierLevels` | Array de niveles de mejora. Cada nivel puede tener un `CraftingTimeReductionModifier` (porcentaje más rápido) y un `UpgradeRequirement` con materiales y tiempo |
| `VariantRotation` | `"NESW"` permite que el banco mire en cuatro direcciones al colocarlo |
| `State` | Define estados visuales como `CraftCompleted` para animaciones durante el crafteo |

### Estructura de categorías

Cada categoría en el array `Categories` es un objeto con tres campos:

```json
{
  "Id": "Runes",
  "Icon": "Icons/CraftingCategories/Runecrafting/Runes.png",
  "Name": "server.benchCategories.runecraftingbench.runes"
}
```

- **`Id`** -- El identificador de categoría que las recetas referencian para aparecer bajo esta pestaña
- **`Icon`** -- Ruta al PNG del icono mostrado en la pestaña de categoría
- **`Name`** -- Clave de traducción para el texto de la etiqueta de categoría

---

## Paso 2: Crear Recetas que Usen el Banco

Cualquier definición de objeto con un bloque `Recipe` puede referenciar tu banco. La conexión se realiza a través del array `BenchRequirement`, donde `Id` coincide con el `Bench.Id` de tu banco y `Categories` lista bajo qué pestañas de categoría aparece la receta.

Crea un objeto que se fabrique en el Banco de Runecrafting:

```
YourMod/Assets/Server/Item/Items/Rune/Rune_Fire.json
```

```json
{
  "TranslationProperties": {
    "Name": "server.items.Rune_Fire.name",
    "Description": "server.items.Rune_Fire.description"
  },
  "Icon": "Icons/MyMod/Rune_Fire.png",
  "Quality": "Rare",
  "MaxStack": 16,
  "ItemLevel": 3,
  "Recipe": {
    "TimeSeconds": 5,
    "Input": [
      {
        "ItemId": "Ingredient_Fire_Essence",
        "Quantity": 3
      },
      {
        "ItemId": "Ingredient_Crystal_Cyan",
        "Quantity": 2
      }
    ],
    "OutputQuantity": 1,
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Id": "Runecraftingbench",
        "Categories": [
          "Runes"
        ],
        "RequiredTierLevel": 1
      }
    ]
  }
}
```

### Campos de BenchRequirement

| Campo | Propósito |
|-------|-----------|
| `Type` | Debe ser `"Crafting"` para coincidir con un banco de crafteo |
| `Id` | Debe coincidir exactamente con el `Bench.Id` de tu definición de banco (sensible a mayúsculas) |
| `Categories` | Array de IDs de categoría bajo las cuales aparece esta receta. Debe coincidir con un `Id` de categoría del banco |
| `RequiredTierLevel` | Nivel de tier mínimo del banco requerido. Los niveles de tier se indexan desde 1 a partir del array `TierLevels`. Omitir para tier 0 (sin mejora necesaria) |

---

## Paso 3: Agregar una Receta Bloqueada por Tier

Para crear una receta que solo se desbloquee después de que el jugador mejore su banco, establece `RequiredTierLevel` a un valor más alto:

```
YourMod/Assets/Server/Item/Items/Rune/Rune_Void.json
```

```json
{
  "TranslationProperties": {
    "Name": "server.items.Rune_Void.name",
    "Description": "server.items.Rune_Void.description"
  },
  "Icon": "Icons/MyMod/Rune_Void.png",
  "Quality": "Epic",
  "MaxStack": 8,
  "ItemLevel": 6,
  "Recipe": {
    "TimeSeconds": 10,
    "Input": [
      {
        "ItemId": "Ingredient_Void_Essence",
        "Quantity": 5
      },
      {
        "ItemId": "Ingredient_Crystal_Cyan",
        "Quantity": 8
      }
    ],
    "OutputQuantity": 1,
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Id": "Runecraftingbench",
        "Categories": [
          "Runes"
        ],
        "RequiredTierLevel": 2
      }
    ]
  }
}
```

Esta receta aparece en gris hasta que el jugador mejore el Banco de Runecrafting al tier 2.

---

## Paso 4: Agregar Claves de Traducción

Agrega todas las claves de traducción a tu archivo de idioma:

```
YourMod/Assets/Languages/en-US.lang
```

```
server.items.Bench_Runecrafting.name=Runecrafting Bench
server.items.Bench_Runecrafting.description=A bench for crafting runes and enchantments.
server.benchCategories.runecraftingbench.runes=Runes
server.benchCategories.runecraftingbench.enchantments=Enchantments
server.benchCategories.runecraftingbench.scrolls=Scrolls
server.items.Rune_Fire.name=Fire Rune
server.items.Rune_Fire.description=A rune imbued with the essence of fire.
server.items.Rune_Void.name=Void Rune
server.items.Rune_Void.description=A rune channelling void energy.
```

---

## Paso 5: Probar en el Juego

1. Coloca la carpeta de tu mod en el directorio de mods del servidor.
2. Inicia el servidor y observa si hay errores de validación JSON.
3. Usa el spawner de objetos del desarrollador para darte `Bench_Runecrafting`.
4. Coloca el banco y haz clic derecho para abrir la interfaz de crafteo.
5. Confirma que las tres pestañas de categoría (Runes, Enchantments, Scrolls) aparezcan.
6. Verifica que `Rune_Fire` aparezca bajo la pestaña Runes y pueda fabricarse.
7. Confirma que `Rune_Void` aparezca en gris hasta que mejores el banco al tier 2.
8. Mejora el banco proporcionando los materiales requeridos y verifica que la receta de tier 2 se desbloquee.

**Errores comunes y soluciones:**

| Error | Causa | Solución |
|-------|-------|----------|
| La receta no aparece en el banco | Discrepancia en `BenchRequirement.Id` | Asegúrate de que `Id` coincida exactamente con `Bench.Id` (sensible a mayúsculas) |
| Pestaña de categoría faltante | El `Id` de categoría no está en la definición del banco | Agrega la categoría al array `Categories` del banco |
| La receta siempre aparece en gris | `RequiredTierLevel` demasiado alto | Verifica que el nivel de tier exista en el array `TierLevels` del banco |
| El banco no se puede colocar | Falta el bloque `Support` | Agrega `"Support": { "Down": [{ "FaceType": "Full" }] }` |

---

## Próximos Pasos

- [Crear un Bloque Personalizado](/es/hytale-modding-docs/tutorials/beginner/create-a-block) -- aprende cómo se conectan los bloques y los objetos
- [Tablas de Botín Personalizadas](/es/hytale-modding-docs/tutorials/intermediate/custom-loot-tables) -- configura drops que incluyan tus objetos fabricados
- [Tiendas de NPCs y Comercio](/es/hytale-modding-docs/tutorials/intermediate/npc-shops-and-trading) -- vende objetos fabricados en el banco a través de mercaderes NPC
