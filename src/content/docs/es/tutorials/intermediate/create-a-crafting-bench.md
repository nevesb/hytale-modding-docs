---
title: Crear una Mesa de Crafteo Personalizada
description: Tutorial paso a paso para añadir un Yunque de Cristal con modelo personalizado, categorías de recetas e interfaz de crafteo.
sidebar:
  order: 4
---

## Objetivo

Construye un **Yunque de Cristal** — una mesa de crafteo personalizada que los jugadores pueden colocar en el mundo y usar para forjar armas de cristal. Definirás el ítem de la mesa con un `BlockType` en línea, configurarás las categorías de crafteo, el `State` requerido para la interfaz de crafteo y las claves de traducción.

## Lo que Aprenderás

- Cómo se definen las mesas de crafteo usando la propiedad de bloque `Bench`
- Por qué `State` con `Id: "crafting"` es **obligatorio** para que se abra la interfaz de la mesa
- Cómo crear categorías que organizan las recetas dentro de la interfaz de la mesa
- Cómo los niveles de tier y `CraftingTimeReductionModifier` controlan la velocidad de crafteo
- Cómo las recetas de ítems referencian una mesa mediante `BenchRequirement`

## Requisitos Previos

- Una carpeta de mod con un `manifest.json` válido (ver [Configura tu Entorno de Desarrollo](/hytale-modding-docs/es/tutorials/beginner/setup-dev-environment))
- Familiaridad con definiciones de bloques (ver [Crear un Bloque Personalizado](/hytale-modding-docs/es/tutorials/beginner/create-a-block))
- Familiaridad con definiciones de ítems (ver [Crear un Ítem Personalizado](/hytale-modding-docs/es/tutorials/beginner/create-an-item))

**Repositorio del mod de ejemplo:** [hytale-mods-custom-bench](https://github.com/nevesb/hytale-mods-custom-bench)

---

## Descripción General de la Mesa de Crafteo

Las mesas de crafteo en Hytale son **ítems** que contienen un `BlockType` en línea con una configuración `Bench`. A diferencia de los bloques puros que necesitan un JSON de Bloque separado y una entrada en `BlockTypeList`, las mesas definen todo en un único archivo JSON de ítem — el mismo patrón que usan las mesas del juego base como `Bench_Weapon` y `Bench_Armory`.

Diferencias clave respecto a los bloques normales:
- **Sin JSON de Bloque separado** en `Server/Item/Block/Blocks/`
- **Sin entrada en `BlockTypeList`** necesaria
- El bloque `State` con `Id: "crafting"` es **obligatorio** para que funcione la interfaz de crafteo
- El objeto `Bench` define el tipo de crafteo, las categorías y los niveles de tier

---

## Paso 1: Configurar la Estructura de Archivos del Mod

```text
CreateACraftingBench/
├── manifest.json
├── Common/
│   ├── Blocks/
│   │   └── HytaleModdingManual/
│   │       └── Armory_Crystal_Glow.blockymodel
│   └── BlockTextures/
│       └── HytaleModdingManual/
│           └── Armory_Crystal_Glow.png
└── Server/
    ├── Item/
    │   └── Items/
    │       └── HytaleModdingManual/
    │           └── Bench_Armory_Crystal_Glow.json
    └── Languages/
        ├── en-US/
        │   └── server.lang
        ├── es/
        │   └── server.lang
        └── pt-BR/
            └── server.lang
```

### manifest.json

```json
{
  "Group": "HytaleModdingManual",
  "Name": "CreateACraftingBench",
  "Version": "1.0.0",
  "Description": "Crystal Anvil crafting bench for forging crystal weapons",
  "Authors": [
    {
      "Name": "HytaleModdingManual"
    }
  ],
  "Dependencies": {},
  "OptionalDependencies": {},
  "IncludesAssetPack": true
}
```

Ten en cuenta que `IncludesAssetPack` es `true` porque tenemos recursos Common (modelo y textura).

---

## Paso 2: Crear la Definición del Ítem de la Mesa

Crea la mesa en `Server/Item/Items/HytaleModdingManual/Bench_Armory_Crystal_Glow.json`:

```json
{
  "TranslationProperties": {
    "Name": "server.items.Bench_Armory_Crystal_Glow.name",
    "Description": "server.items.Bench_Armory_Crystal_Glow.description"
  },
  "Quality": "Rare",
  "Icon": "Icons/ItemsGenerated/Bench_Armory_Crystal_Glow.png",
  "Categories": [
    "Furniture.Benches"
  ],
  "Recipe": {
    "TimeSeconds": 10.0,
    "KnowledgeRequired": false,
    "Input": [
      {
        "ItemId": "Ore_Crystal_Glow",
        "Quantity": 3
      },
      {
        "ItemId": "Wood_Enchanted_Trunk",
        "Quantity": 10
      },
      {
        "ItemId": "Ingredient_Bar_Gold",
        "Quantity": 5
      }
    ],
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Categories": [
          "Workbench_Crafting"
        ],
        "Id": "Workbench",
        "RequiredTierLevel": 2
      }
    ]
  },
  "BlockType": {
    "Material": "Solid",
    "DrawType": "Model",
    "Opacity": "Transparent",
    "CustomModel": "Blocks/HytaleModdingManual/Armory_Crystal_Glow.blockymodel",
    "CustomModelTexture": [
      {
        "Texture": "BlockTextures/HytaleModdingManual/Armory_Crystal_Glow.png",
        "Weight": 1
      }
    ],
    "VariantRotation": "NESW",
    "HitboxType": "Bench_Weapon",
    "State": {
      "Id": "crafting",
      "Definitions": {
        "CraftCompleted": {
          "Looping": true
        },
        "CraftCompletedInstant": {}
      }
    },
    "Gathering": {
      "Breaking": {
        "GatherType": "Benches",
        "ItemId": "Bench_Armory_Crystal_Glow"
      }
    },
    "Light": {
      "Color": "#88ccff"
    },
    "Bench": {
      "Type": "Crafting",
      "LocalOpenSoundEventId": "SFX_Weapon_Bench_Open",
      "LocalCloseSoundEventId": "SFX_Weapon_Bench_Close",
      "CompletedSoundEventId": "SFX_Weapon_Bench_Craft",
      "Id": "Armory_Crystal_Glow",
      "Categories": [
        {
          "Id": "Crystal_Glow_Sword",
          "Name": "server.benchCategories.crystal_glow_sword",
          "Icon": "Icons/CraftingCategories/Armory/Sword.png"
        }
      ],
      "TierLevels": [
        {
          "CraftingTimeReductionModifier": 0.0
        }
      ]
    },
    "BlockSoundSetId": "Crystal",
    "ParticleColor": "#88ccff",
    "Support": {
      "Down": [
        {
          "FaceType": "Full"
        }
      ]
    },
    "BlockParticleSetId": "Crystal"
  },
  "PlayerAnimationsId": "Block",
  "IconProperties": {
    "Scale": 0.5,
    "Rotation": [
      22.5,
      45,
      22.5
    ],
    "Translation": [
      13,
      -14
    ]
  },
  "Tags": {
    "Type": [
      "Bench"
    ]
  },
  "MaxStack": 1,
  "ItemSoundSetId": "ISS_Items_Gems"
}
```

### Explicación de los campos clave de la mesa

| Campo | Propósito |
|-------|-----------|
| `Bench.Type` | Debe ser `"Crafting"` para mesas basadas en recetas |
| `Bench.Id` | Identificador único que las recetas referencian en su `BenchRequirement` |
| `Bench.Categories` | Array de pestañas de categoría que se muestran en la interfaz de la mesa. Cada una tiene un `Id`, `Icon` y `Name` de traducción |
| `Bench.TierLevels` | Array de niveles de mejora. Cada uno puede tener `CraftingTimeReductionModifier` (porcentaje más rápido) y `UpgradeRequirement` |
| `State` | **Obligatorio.** Debe tener `"Id": "crafting"` para que la interfaz de la mesa se abra al interactuar |
| `VariantRotation` | `"NESW"` permite que la mesa mire en cuatro direcciones al colocarse |
| `HitboxType` | Reutiliza el hitbox `"Bench_Weapon"` para el área de interacción |
| `Light.Color` | Emite un suave brillo azul (`#88ccff`) |
| `Support.Down` | Requiere una cara de bloque completa debajo para colocarse |

:::caution[State es obligatorio]
Sin el bloque `State`, la mesa se colocará en el mundo pero **la interfaz de crafteo no se abrirá** al interactuar con ella. No aparece ningún error en los registros — falla silenciosamente. Todas las mesas del juego base (`Bench_Weapon`, `Bench_Armory`, `Bench_Campfire`) incluyen esta configuración de `State`.
:::

### Estructura de categorías

Cada categoría en el array `Categories` define una pestaña en la interfaz de crafteo:

```json
{
  "Id": "Crystal_Glow_Sword",
  "Name": "server.benchCategories.crystal_glow_sword",
  "Icon": "Icons/CraftingCategories/Armory/Sword.png"
}
```

- **`Id`** — El identificador de categoría que las recetas referencian para aparecer bajo esta pestaña
- **`Icon`** — Ruta al PNG del ícono que se muestra en la pestaña de categoría (reutilizamos el ícono de Espada del juego base)
- **`Name`** — Clave de traducción para el texto de la etiqueta de la categoría

---

## Paso 3: Crear una Receta que Use la Mesa

Cualquier ítem con una `Recipe` puede referenciar tu mesa a través de `BenchRequirement`. La conexión se establece haciendo coincidir `BenchRequirement.Id` con el `Bench.Id` de tu mesa, y `Categories` con las pestañas de categoría bajo las que aparece la receta.

Por ejemplo, la receta de la Espada de Cristal Brillante referencia nuestra mesa:

```json
{
  "Recipe": {
    "TimeSeconds": 8.0,
    "Input": [
      {
        "ItemId": "Ore_Crystal_Glow",
        "Quantity": 10
      },
      {
        "ItemId": "Wood_Enchanted_Trunk",
        "Quantity": 50
      },
      {
        "ItemId": "Ingredient_Leather_Heavy",
        "Quantity": 10
      }
    ],
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Id": "Armory_Crystal_Glow",
        "Categories": [
          "Crystal_Glow_Sword"
        ]
      }
    ]
  }
}
```

### Campos de BenchRequirement

| Campo | Propósito |
|-------|-----------|
| `Type` | Debe ser `"Crafting"` para coincidir con una mesa de crafteo |
| `Id` | Debe coincidir exactamente con el `Bench.Id` de tu definición de mesa (sensible a mayúsculas) |
| `Categories` | Array de IDs de categoría bajo los que aparece esta receta. Debe coincidir con un `Id` de categoría de la mesa |
| `RequiredTierLevel` | Nivel mínimo de tier de mesa requerido. Omitir para tier 0 (sin mejora necesaria) |

---

## Paso 4: Añadir las Claves de Traducción

Crea los archivos de idioma en `Server/Languages/<locale>/server.lang`:

### Inglés (`en-US/server.lang`)

```
items.Bench_Armory_Crystal_Glow.name = Crystal Anvil
items.Bench_Armory_Crystal_Glow.description = A crystal anvil for forging crystal weapons.
benchCategories.crystal_glow_sword = Crystal Sword
```

### Español (`es/server.lang`)

```
items.Bench_Armory_Crystal_Glow.name = Yunque de Cristal
items.Bench_Armory_Crystal_Glow.description = Un yunque de cristal para forjar armas de cristal.
benchCategories.crystal_glow_sword = Espada de Cristal
```

### Portugués BR (`pt-BR/server.lang`)

```
items.Bench_Armory_Crystal_Glow.name = Bigorna de Cristal
items.Bench_Armory_Crystal_Glow.description = Uma bigorna de cristal para forjar armas de cristal.
benchCategories.crystal_glow_sword = Espada de Cristal
```

Ten en cuenta el formato de la clave de traducción: `items.<ItemId>.name` y `benchCategories.<category_id>`. El prefijo `server.` en el JSON (`"Name": "server.items.Bench_Armory_Crystal_Glow.name"`) se corresponde con la clave del archivo lang sin el prefijo `server.`.

---

## Paso 5: Añadir el Modelo Personalizado

La mesa usa un `.blockymodel` y una textura personalizados. Colócalos en la carpeta `Common/`:

- **Modelo:** `Common/Blocks/HytaleModdingManual/Armory_Crystal_Glow.blockymodel`
- **Textura:** `Common/BlockTextures/HytaleModdingManual/Armory_Crystal_Glow.png`

Puedes crear el modelo usando [Blockbench](https://www.blockbench.net/) con el formato **Hytale Block**. El modelo debe caber dentro del límite del bloque (32 unidades = 1 bloque). Para una mesa de 2 bloques de ancho, usa el hitbox `"HitboxType": "Bench_Weapon"` que cubre el área más amplia.

:::tip[Rutas de recursos Common]
Los recursos Common deben estar dentro de uno de estos directorios raíz: `Blocks/`, `BlockTextures/`, `Items/`, `Resources/`, `NPC/`, `VFX/` o `Consumable/`. Colocar archivos fuera de estas carpetas causa un error de carga.
:::

---

## Paso 6: Probar en el Juego

1. Coloca la carpeta del mod en tu directorio de mods (`%APPDATA%/Hytale/UserData/Mods/`).
2. Inicia el servidor y revisa los registros en busca de errores de validación.
3. Usa el comando `/spawnitem Bench_Armory_Crystal_Glow` para darte la mesa.
4. Coloca la mesa y haz clic derecho para abrir la interfaz de crafteo.
5. Confirma que aparece la pestaña de categoría Espada de Cristal.

![Yunque de Cristal colocado en el mundo](/hytale-modding-docs/images/tutorials/create-a-crafting-bench/crystal-anvil-ingame.png)

![Interfaz de crafteo del Yunque de Cristal mostrando la receta de la Espada de Cristal](/hytale-modding-docs/images/tutorials/create-a-crafting-bench/crystal-anvil-crafting-ui.png)

**Errores comunes y soluciones:**

| Error | Causa | Solución |
|-------|-------|----------|
| La mesa se coloca pero la interfaz no se abre | Falta el bloque `State` | Añade `"State": { "Id": "crafting", "Definitions": { "CraftCompleted": { "Looping": true }, "CraftCompletedInstant": {} } }` |
| La receta no aparece en la mesa | `BenchRequirement.Id` no coincide | Asegúrate de que `Id` coincide exactamente con `Bench.Id` (sensible a mayúsculas) |
| Falta la pestaña de categoría | El `Id` de categoría no está en la definición de la mesa | Añade la categoría al array `Categories` de la mesa |
| `StackOverflowError` al cargar | Uso de herencia con `Parent` junto con `State` | Haz la mesa independiente — copia todos los campos en lugar de heredar de `Bench_Weapon` |
| La mesa no se puede colocar | Falta el bloque `Support` | Añade `"Support": { "Down": [{ "FaceType": "Full" }] }` |
| Error de carga de recurso Common | Ruta de recurso incorrecta | Asegúrate de que los recursos están dentro de `Blocks/`, `BlockTextures/`, etc. — no en `Animations/` ni carpetas personalizadas |

---

## Referencia de Mesas del Juego Base

Para referencia, aquí están los tipos de mesas que se usan en el juego base:

| Mesa | `Bench.Type` | `Bench.Id` | Categorías |
|------|-------------|------------|------------|
| Mesa de Armas | `Crafting` | `Weapon_Bench` | Sword, Mace, Battleaxe, Daggers, Bow |
| Armería | `DiagramCrafting` | `Armory` | Weapons (Sword, Club, Axe, etc.), Armor (Head, Chest, etc.) |
| Hoguera | `Crafting` | `Campfire` | Cooking |
| Banco de Trabajo | `Crafting` | `Workbench` | Workbench_Crafting |

---

## Próximos Pasos

- [Crear un Bloque Personalizado](/hytale-modding-docs/es/tutorials/beginner/create-a-block) — aprende cómo se conectan bloques e ítems
- [Tablas de Botín Personalizadas](/hytale-modding-docs/es/tutorials/intermediate/custom-loot-tables) — configura drops que incluyan tus ítems crafteados
- [Tiendas y Comercio con NPCs](/hytale-modding-docs/es/tutorials/intermediate/npc-shops-and-trading) — vende ítems crafteados en la mesa a través de mercaderes NPC
