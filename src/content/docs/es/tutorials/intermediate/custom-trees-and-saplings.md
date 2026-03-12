---
title: Árboles y Brotes Personalizados
description: Tutorial paso a paso para crear árboles personalizados con mecánicas de crecimiento de brotes, progresión de prefabs multi-etapa e integración con la agricultura.
sidebar:
  order: 1
---

## Objetivo

Crear un árbol **Crystalwood** personalizado que los jugadores puedan cultivar desde un brote. Definirás el objeto brote con etapas de agricultura, configurarás referencias de prefab para cada etapa de crecimiento y configurarás modificadores de crecimiento para que el árbol responda al agua y fertilizante.

## Lo que Aprenderás

- Cómo los objetos brote usan la propiedad `Farming` del tipo de bloque para crecimiento multi-etapa
- Cómo las etapas de crecimiento transicionan de tipos de bloque a prefabs
- Cómo `Duration`, `ReplaceMaskTags` y `ActiveGrowthModifiers` controlan el comportamiento de crecimiento
- Cómo usar la herencia `Parent` para crear variantes de árboles eficientemente

## Requisitos Previos

- Una carpeta de mod con un `manifest.json` válido (ver [Configura tu Entorno de Desarrollo](/es/hytale-modding-docs/tutorials/beginner/setup-dev-environment))
- Familiaridad con definiciones de bloques y objetos (ver [Crear un Bloque Personalizado](/es/hytale-modding-docs/tutorials/beginner/create-a-block))
- Archivos de prefab de árboles creados en el editor de prefabs de Hytale (archivos `.prefab.json`)

---

## Descripción General del Sistema de Crecimiento

Los árboles de Hytale crecen a través de una serie de etapas definidas en la propiedad `BlockType.Farming` del brote. La primera etapa es un bloque (el brote en sí), y las etapas posteriores son prefabs (modelos de árboles cada vez más grandes). Cada etapa tiene un rango de duración, y el motor transiciona automáticamente entre etapas.

```
Bloque Brote → Prefab Árbol Pequeño → Prefab Árbol Mediano → Prefab Árbol Completo
   Etapa 0          Etapa 1              Etapa 2                 Etapa 3
```

El brote de Roble vanilla (`Plant_Sapling_Oak.json`) define 6 etapas de crecimiento, mientras que el brote de Abedul usa herencia `Parent` para reutilizar la mayor parte de la estructura del Roble con diferentes texturas y prefabs.

---

## Paso 1: Crear la Definición del Objeto Brote

El brote es un objeto que coloca un bloque con componentes de agricultura. Crea:

```
YourMod/Assets/Server/Item/Items/Plant/Plant_Sapling_Crystalwood.json
```

```json
{
  "TranslationProperties": {
    "Name": "server.items.Plant_Sapling_Crystalwood.name",
    "Description": "server.items.Plant_Sapling_Crystalwood.description"
  },
  "Icon": "Icons/MyMod/Plant_Crystalwood_Sapling.png",
  "Categories": [
    "Blocks.Plants"
  ],
  "Interactions": {
    "Primary": "Block_Primary",
    "Secondary": "Block_Secondary"
  },
  "ItemLevel": 5,
  "Recipe": {
    "TimeSeconds": 0,
    "Input": [
      {
        "ItemId": "Ingredient_Life_Essence",
        "Quantity": 12
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
        "Id": "Farmingbench",
        "Categories": [
          "Saplings"
        ],
        "RequiredTierLevel": 3
      }
    ]
  },
  "BlockType": {
    "DrawType": "Model",
    "CustomModel": "Blocks/Foliage/Tree/Sapling.blockymodel",
    "CustomModelTexture": [
      {
        "Texture": "Blocks/Foliage/Tree/Sapling_Textures/Crystalwood.png",
        "Weight": 1
      }
    ],
    "Group": "Wood",
    "HitboxType": "Plant_Large",
    "Flags": {},
    "RandomRotation": "YawStep1",
    "BlockEntity": {
      "Components": {
        "FarmingBlock": {}
      }
    },
    "Farming": {
      "Stages": {
        "Default": [
          {
            "Block": "Plant_Sapling_Crystalwood",
            "Duration": {
              "Min": 30000,
              "Max": 50000
            },
            "Type": "BlockType"
          },
          {
            "Prefabs": [
              {
                "Path": "Trees/Crystalwood/Stage_0/Crystalwood_Stage0_001.prefab.json",
                "Weight": 1
              }
            ],
            "Duration": {
              "Min": 40000,
              "Max": 60000
            },
            "Type": "Prefab",
            "ReplaceMaskTags": [
              "Soil"
            ],
            "SoundEventId": "SFX_Crops_Grow"
          },
          {
            "Prefabs": [
              {
                "Path": "Trees/Crystalwood/Stage_1/Crystalwood_Stage1_001.prefab.json",
                "Weight": 1
              }
            ],
            "Duration": {
              "Min": 40000,
              "Max": 60000
            },
            "Type": "Prefab",
            "ReplaceMaskTags": [
              "Soil"
            ],
            "SoundEventId": "SFX_Crops_Grow"
          },
          {
            "Prefabs": [
              {
                "Path": "Trees/Crystalwood/Stage_2/Crystalwood_Stage2_001.prefab.json",
                "Weight": 1
              },
              {
                "Path": "Trees/Crystalwood/Stage_2/Crystalwood_Stage2_002.prefab.json",
                "Weight": 1
              }
            ],
            "Duration": {
              "Min": 60000,
              "Max": 80000
            },
            "Type": "Prefab",
            "ReplaceMaskTags": [
              "Soil"
            ],
            "SoundEventId": "SFX_Crops_Grow"
          },
          {
            "Prefabs": [
              {
                "Path": "Trees/Crystalwood/Stage_3/Crystalwood_Stage3_001.prefab.json",
                "Weight": 1
              },
              {
                "Path": "Trees/Crystalwood/Stage_3/Crystalwood_Stage3_002.prefab.json",
                "Weight": 1
              }
            ],
            "Type": "Prefab",
            "ReplaceMaskTags": [
              "Soil"
            ],
            "SoundEventId": "SFX_Crops_Grow"
          }
        ]
      },
      "StartingStageSet": "Default",
      "ActiveGrowthModifiers": [
        "Fertilizer",
        "Water",
        "LightLevel"
      ]
    },
    "Gathering": {
      "Soft": {
        "ItemId": "Plant_Sapling_Crystalwood"
      }
    },
    "Support": {
      "Down": [
        {
          "TagId": "Type=Soil"
        }
      ]
    },
    "BlockParticleSetId": "Flower",
    "BlockSoundSetId": "Bush",
    "ParticleColor": "#44aacc"
  },
  "PlayerAnimationsId": "Item",
  "Tags": {
    "Type": [
      "Plant"
    ],
    "Family": [
      "Sapling"
    ]
  },
  "ItemSoundSetId": "ISS_Items_Foliage"
}
```

### Etapas de agricultura explicadas

El array `Farming.Stages.Default` define cada etapa de crecimiento en orden:

| Etapa | Tipo | Propósito |
|-------|------|-----------|
| 0 | `BlockType` | El bloque brote en sí. `Block` referencia el ID de bloque propio de este objeto |
| 1-2 | `Prefab` | Prefabs de árbol pequeño y mediano colocados a medida que el árbol crece |
| 3-4 | `Prefab` | Prefabs de árbol más grandes. La etapa final no tiene `Duration` (permanece para siempre) |

### Campos clave de agricultura

| Campo | Propósito |
|-------|-----------|
| `Stages.Default[].Type` | `"BlockType"` para el bloque brote inicial, `"Prefab"` para etapas de modelo de árbol |
| `Stages.Default[].Block` | Para etapas `BlockType`: el ID de bloque a colocar (generalmente el brote en sí) |
| `Stages.Default[].Prefabs` | Para etapas `Prefab`: array de rutas de prefab con pesos para selección aleatoria |
| `Stages.Default[].Duration.Min` / `Max` | Rango de tiempo en ticks del juego antes de avanzar a la siguiente etapa. El motor elige un valor aleatorio dentro del rango |
| `Stages.Default[].ReplaceMaskTags` | Etiquetas de bloque que el prefab puede reemplazar al crecer. `"Soil"` permite que las raíces penetren la tierra |
| `Stages.Default[].SoundEventId` | Sonido reproducido cuando ocurre la transición de etapa |
| `StartingStageSet` | Qué conjunto de etapas usar al inicio. `"Default"` es estándar |
| `ActiveGrowthModifiers` | Array de modificadores que afectan la velocidad de crecimiento: `"Fertilizer"` (compost), `"Water"` (lluvia/irrigación), `"LightLevel"` (luz solar) |

### Múltiples variantes de prefab

Cuando una etapa tiene múltiples entradas en su array `Prefabs`, el motor elige una aleatoriamente basándose en `Weight`. Esto crea variedad natural:

```json
"Prefabs": [
  {
    "Path": "Trees/Crystalwood/Stage_2/Crystalwood_Stage2_001.prefab.json",
    "Weight": 1
  },
  {
    "Path": "Trees/Crystalwood/Stage_2/Crystalwood_Stage2_002.prefab.json",
    "Weight": 1
  }
]
```

Pesos iguales dan una probabilidad 50/50. Usa pesos diferentes para hacer algunas variantes más raras.

---

## Paso 2: Crear el Componente de Entidad de Bloque

El objeto `BlockEntity.Components.FarmingBlock` le indica al motor que este bloque usa el sistema de agricultura. El objeto vacío `{}` hereda el comportamiento de agricultura predeterminado. La propiedad `Farming` en el mismo `BlockType` proporciona la configuración real de etapas.

```json
"BlockEntity": {
  "Components": {
    "FarmingBlock": {}
  }
}
```

Este componente es obligatorio. Sin él, las etapas de `Farming` serán ignoradas.

---

## Paso 3: Configurar Soporte de Bloque y Recolección

Dos propiedades adicionales de `BlockType` aseguran que el brote se comporte correctamente:

### Soporte

```json
"Support": {
  "Down": [
    {
      "TagId": "Type=Soil"
    }
  ]
}
```

El brote requiere un bloque con la etiqueta `Type=Soil` directamente debajo. Si el suelo se elimina, el brote se rompe y se dropea a sí mismo.

### Recolección

```json
"Gathering": {
  "Soft": {
    "ItemId": "Plant_Sapling_Crystalwood"
  }
}
```

El tipo de recolección `Soft` significa que los jugadores pueden romper el brote con cualquier herramienta (o a mano) y recibir el objeto brote de vuelta.

---

## Paso 4: Crear una Variante Usando Herencia Parent

Para crear una variante de color de tu árbol sin duplicar todo el archivo, usa la herencia `Parent`. El brote de Abedul en vanilla usa exactamente este patrón:

```
YourMod/Assets/Server/Item/Items/Plant/Plant_Sapling_Crystalwood_Red.json
```

```json
{
  "TranslationProperties": {
    "Name": "server.items.Plant_Sapling_Crystalwood_Red.name",
    "Description": "server.items.Plant_Sapling_Crystalwood_Red.description"
  },
  "Parent": "Plant_Sapling_Crystalwood",
  "Icon": "Icons/MyMod/Plant_Crystalwood_Red_Sapling.png",
  "ItemLevel": 6,
  "Recipe": {
    "TimeSeconds": 0,
    "Input": [
      {
        "ItemId": "Ingredient_Life_Essence",
        "Quantity": 18
      },
      {
        "ItemId": "Ingredient_Crystal_Cyan",
        "Quantity": 4
      }
    ],
    "OutputQuantity": 1,
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Id": "Farmingbench",
        "Categories": [
          "Saplings"
        ],
        "RequiredTierLevel": 4
      }
    ]
  },
  "BlockType": {
    "CustomModelTexture": [
      {
        "Texture": "Blocks/Foliage/Tree/Sapling_Textures/Crystalwood_Red.png",
        "Weight": 1
      }
    ],
    "Farming": {
      "Stages": {
        "Default": [
          {
            "Block": "Plant_Sapling_Crystalwood_Red",
            "Duration": {
              "Min": 30000,
              "Max": 50000
            },
            "Type": "BlockType"
          },
          {
            "Prefabs": [
              {
                "Path": "Trees/Crystalwood_Red/Stage_0/Crystalwood_Red_Stage0_001.prefab.json",
                "Weight": 1
              }
            ],
            "Duration": {
              "Min": 40000,
              "Max": 60000
            },
            "Type": "Prefab",
            "ReplaceMaskTags": [
              "Soil"
            ],
            "SoundEventId": "SFX_Crops_Grow"
          },
          {
            "Prefabs": [
              {
                "Path": "Trees/Crystalwood_Red/Stage_1/Crystalwood_Red_Stage1_001.prefab.json",
                "Weight": 1
              }
            ],
            "Type": "Prefab",
            "ReplaceMaskTags": [
              "Soil"
            ],
            "SoundEventId": "SFX_Crops_Grow"
          }
        ]
      },
      "StartingStageSet": "Default",
      "ActiveGrowthModifiers": [
        "Fertilizer",
        "Water",
        "LightLevel"
      ]
    },
    "Gathering": {
      "Soft": {
        "ItemId": "Plant_Sapling_Crystalwood_Red"
      }
    },
    "ParticleColor": "#cc4444"
  }
}
```

El campo `Parent` hereda todas las propiedades de `Plant_Sapling_Crystalwood`. Solo los campos que especifiques se sobrescriben -- el modelo, hitbox, set de sonidos, reglas de soporte y otras propiedades se heredan automáticamente.

---

## Paso 5: Agregar Claves de Traducción

```
YourMod/Assets/Languages/en-US.lang
```

```
server.items.Plant_Sapling_Crystalwood.name=Crystalwood Sapling
server.items.Plant_Sapling_Crystalwood.description=A sapling that grows into a tree with crystalline bark.
server.items.Plant_Sapling_Crystalwood_Red.name=Red Crystalwood Sapling
server.items.Plant_Sapling_Crystalwood_Red.description=A variant crystalwood sapling with crimson foliage.
```

---

## Paso 6: Probar en el Juego

1. Coloca la carpeta de tu mod en el directorio de mods del servidor.
2. Inicia el servidor y observa si hay errores sobre rutas de prefab faltantes o IDs de bloque desconocidos.
3. Usa el spawner de objetos del desarrollador para darte `Plant_Sapling_Crystalwood`.
4. Coloca el brote en un bloque de tierra/suelo y confirma que se renderiza correctamente.
5. Espera a la primera etapa de crecimiento (o usa comandos de aceleración de tiempo) y verifica que el brote transicione al primer prefab de árbol.
6. Confirma que cada etapa posterior cargue el modelo de prefab correcto.
7. Verifica que la etapa final permanezca permanentemente (sin `Duration` establecida).
8. Rompe el brote antes de que crezca y confirma que recibes el objeto brote de vuelta.
9. Prueba que remover el bloque de suelo debajo del brote cause que se rompa.

**Errores comunes y soluciones:**

| Error | Causa | Solución |
|-------|-------|----------|
| El brote se coloca pero nunca crece | Falta el componente `FarmingBlock` | Agrega `"BlockEntity": { "Components": { "FarmingBlock": {} } }` |
| `Unknown prefab path` | Archivo de prefab faltante o ruta incorrecta | Verifica que los archivos `.prefab.json` existan en las rutas referenciadas |
| El brote flota en el aire | Falta la configuración de `Support` | Agrega `"Support": { "Down": [{ "TagId": "Type=Soil" }] }` |
| Crecimiento demasiado rápido o lento | Los valores de `Duration` necesitan ajuste | Vanilla usa 40000-60000 para la mayoría de etapas, 80000-100000 para etapas tardías |
| La variante hereda etapas incorrectas | `Parent` no sobrescribe `Farming` | La variante debe proporcionar el objeto completo `Farming.Stages` para sobrescribir las etapas |

---

## Próximos Pasos

- [Crear un Bloque Personalizado](/es/hytale-modding-docs/tutorials/beginner/create-a-block) -- entiende las definiciones de bloques que contienen tus prefabs de árboles
- [Tablas de Botín Personalizadas](/es/hytale-modding-docs/tutorials/intermediate/custom-loot-tables) -- configura drops cuando los jugadores talen tus árboles personalizados
- [Crear un Banco de Crafteo](/es/hytale-modding-docs/tutorials/intermediate/create-a-crafting-bench) -- construye el Banco de Agricultura donde se fabrican los brotes
