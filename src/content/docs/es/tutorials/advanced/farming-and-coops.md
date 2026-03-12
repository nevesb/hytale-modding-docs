---
title: Sistema Completo de Granja
description: Construye un sistema de granja completo con corrales personalizados, modificadores de crecimiento, gestión de animales, tablas de botín de producción e integración de cultivos.
---

## Objetivo

Construir un sistema de granja completo para un animal personalizado llamado el **Silkworm** (Gusano de Seda). Crearás un corral que aloja Silkworms, configurarás tablas de botín de producción, establecerás modificadores de crecimiento para condiciones ambientales, crearás el rol de NPC del Silkworm con soporte de domesticación e integrarás con el sistema de fabricación. Al final tendrás un ciclo de granja autocontenido: atrapar Silkworms salvajes, colocarlos en un corral y recolectar fibra de seda para fabricación.

## Prerrequisitos

- Una carpeta de mod con un `manifest.json` válido (ver [Configura tu Entorno de Desarrollo](/hytale-modding-docs/tutorials/beginner/setup-dev-environment))
- Comprensión de los roles de NPC (ver [NPC Roles](/hytale-modding-docs/reference/npc-system/npc-roles) y [Create a Custom NPC](/hytale-modding-docs/tutorials/beginner/create-an-npc))
- Comprensión de las tablas de botín (ver [Drop Tables](/hytale-modding-docs/reference/economy-and-progression/drop-tables))
- Familiaridad con el sistema de granja (ver [Farming & Coops](/hytale-modding-docs/reference/economy-and-progression/farming-coops))

---

## Cómo Funciona el Sistema de Granja

El sistema de granja tiene dos componentes principales:

### Corrales

Los corrales son estructuras que alojan NPCs animales y producen botín con un temporizador. Cada corral define:
- Qué grupos de NPCs pueden colocarse dentro
- Número máximo de residentes
- Qué produce cada especie (mediante referencias a tablas de botín)
- Cuándo los residentes deambulan libremente vs permanecen dentro

### Modificadores

Los modificadores de crecimiento son condiciones ambientales que aceleran o ralentizan los ciclos de producción. Existen cuatro tipos de modificadores:

| Modificador | Fuente | Efecto |
|-------------|--------|--------|
| `Water` | Bloques de agua cercanos o clima de lluvia | Multiplica la tasa de crecimiento (vanilla: 2.5x) |
| `Fertilizer` | Objeto de fertilizante aplicado al corral o suelo | Multiplica la tasa de crecimiento (vanilla: 2x) |
| `LightLevel` | Luz artificial o luz solar | Multiplica la tasa de crecimiento cuando hay suficiente luz presente |
| `Darkness` | Ausencia de luz | Multiplica la tasa de crecimiento en condiciones oscuras (para especies de cavernas) |

### Ciclo de Producción

```
Animal colocado en el corral
    → El temporizador comienza (basado en el rango ProduceTimeout)
    → Los modificadores se aplican (Water, Light, Fertilizer lo aceleran)
    → El temporizador se completa
    → Se ejecuta la tabla de botín de producción
    → Los objetos aparecen en la salida del corral
    → El temporizador se reinicia
```

---

## Paso 1: Crear el Rol de NPC del Silkworm

El Silkworm es una criatura pasiva que puede ser domesticada y colocada en corrales. Usa la base `Template_Beasts_Passive_Critter` para comportamiento simple de deambulación y huida.

Crea `YourMod/Assets/Server/NPC/Roles/MyMod/Silkworm.json`:

```json
{
  "Type": "Variant",
  "Reference": "Template_Beasts_Passive_Critter",
  "Modify": {
    "Appearance": "Gecko",
    "DropList": "Drop_Silkworm",
    "MaxHealth": 8,
    "MaxSpeed": 3,
    "ViewRange": 6,
    "HearingRange": 4,
    "IsTameable": true,
    "TameRoleChange": "Tamed_Silkworm",
    "AttractiveItemSet": ["Plant_Crop_Cotton_Item"],
    "AttractiveItemSetParticles": "Want_Food_Plant",
    "ProduceItem": "Ingredient_Silk_Fibre",
    "ProduceTimeout": ["PT12H", "PT36H"],
    "IsMemory": true,
    "MemoriesCategory": "Critter",
    "MemoriesNameOverride": "Silkworm",
    "NameTranslationKey": {
      "Compute": "NameTranslationKey"
    }
  },
  "Parameters": {
    "NameTranslationKey": {
      "Value": "server.npcRoles.Silkworm.name",
      "Description": "Translation key for NPC name display"
    }
  }
}
```

### Campos clave de granja

| Campo | Valor | Propósito |
|-------|-------|-----------|
| `IsTameable: true` | Habilita la interacción de domesticación | Los jugadores pueden domesticar Silkworms salvajes alimentándolos con objetos atractivos |
| `TameRoleChange` | `"Tamed_Silkworm"` | Cuando se domestica, el NPC cambia a una variante domesticada con comportamiento diferente |
| `AttractiveItemSet` | `["Plant_Crop_Cotton_Item"]` | Los Silkworms son atraídos por el algodón — sostener algodón cerca de uno inicia el proceso de domesticación |
| `ProduceItem` | `"Ingredient_Silk_Fibre"` | Los Silkworms en libertad periódicamente sueltan fibra de seda en el suelo |
| `ProduceTimeout` | `["PT12H", "PT36H"]` | Duración ISO 8601: produce cada 12-36 horas del juego cuando deambula libremente |

Compara con la Gallina vanilla que usa `"ProduceItem": "Food_Egg"` y `"ProduceTimeout": ["PT18H", "PT48H"]`.

Crea la variante domesticada en `YourMod/Assets/Server/NPC/Roles/MyMod/Tamed_Silkworm.json`:

```json
{
  "Type": "Variant",
  "Reference": "Template_Beasts_Passive_Critter",
  "Modify": {
    "Appearance": "Gecko",
    "DropList": "Drop_Silkworm",
    "MaxHealth": 8,
    "MaxSpeed": 2,
    "ViewRange": 4,
    "HearingRange": 3,
    "DefaultPlayerAttitude": "Neutral",
    "ProduceItem": "Ingredient_Silk_Fibre",
    "ProduceTimeout": ["PT8H", "PT24H"],
    "IsMemory": false,
    "NameTranslationKey": {
      "Compute": "NameTranslationKey"
    }
  },
  "Parameters": {
    "NameTranslationKey": {
      "Value": "server.npcRoles.Tamed_Silkworm.name",
      "Description": "Translation key for NPC name display"
    }
  }
}
```

La variante domesticada tiene un tiempo de producción más corto (8-24 horas vs 12-36), velocidad más lenta (menos probable que deambule lejos) y una actitud neutral hacia los jugadores (no huirá cuando se le acerquen).

---

## Paso 2: Crear Grupos de NPCs

Los grupos de NPCs definen qué animales acepta un corral. Los corrales referencian grupos, no roles individuales.

Crea `YourMod/Assets/Server/NPC/Groups/Silkworm.json`:

```json
{
  "Id": "Silkworm",
  "Members": [
    "Silkworm",
    "Tamed_Silkworm"
  ]
}
```

Tanto las variantes salvajes como domesticadas pertenecen al mismo grupo. Esto significa que el corral acepta ambas — un Silkworm salvaje colocado en un corral se trata igual que uno domesticado para propósitos de producción.

---

## Paso 3: Crear el Corral del Silkworm

La definición del corral especifica la capacidad, grupos de NPCs aceptados, tablas de botín de producción y horarios de deambulación.

Crea `YourMod/Assets/Server/Farming/Coops/Coop_Silkworm.json`:

```json
{
  "MaxResidents": 8,
  "ProduceDrops": {
    "Silkworm": "Drop_Silkworm_Produce",
    "Tamed_Silkworm": "Drop_Silkworm_Produce"
  },
  "ResidentRoamTime": [8, 16],
  "ResidentSpawnOffset": {
    "X": 0,
    "Y": 0,
    "Z": 2
  },
  "AcceptedNpcGroups": [
    "Silkworm"
  ],
  "CaptureWildNPCsInRange": true,
  "WildCaptureRadius": 8
}
```

### Decisiones de diseño del corral

| Campo | Valor | Justificación |
|-------|-------|---------------|
| `MaxResidents: 8` | Mayor que el corral de Gallinas (6) | Los Silkworms son pequeños, pueden caber más |
| `ProduceDrops` | Mapea ambas variantes a la misma tabla de botín | Salvajes y domesticados producen los mismos objetos |
| `ResidentRoamTime: [8, 16]` | Solo deambulación diurna | Los Silkworms deambulan de 8 AM a 4 PM, permanecen dentro el resto del tiempo |
| `CaptureWildNPCsInRange: true` | Captura automáticamente Silkworms salvajes cercanos | Función de conveniencia: los Silkworms salvajes que deambulan cerca del corral son capturados automáticamente |
| `WildCaptureRadius: 8` | Rango de captura de 8 bloques | Rango moderado — los jugadores necesitan atraer a los Silkworms relativamente cerca |

Compara con el corral de Gallinas vanilla:
- El corral de Gallinas tiene `MaxResidents: 6`, `WildCaptureRadius: 10`
- El corral de Gallinas acepta 3 grupos de NPCs: `Chicken`, `Chicken_Desert`, `Skrill`
- El corral del Silkworm es más simple con un grupo pero mayor capacidad

---

## Paso 4: Crear Tablas de Botín de Producción

La tabla de botín de producción define qué objetos genera un residente del corral en cada ciclo de producción.

Crea `YourMod/Assets/Server/Drops/NPCs/Critter/Drop_Silkworm_Produce.json`:

```json
{
  "Container": {
    "Type": "Multiple",
    "Containers": [
      {
        "Type": "Choice",
        "Weight": 100,
        "Containers": [
          {
            "Type": "Single",
            "Item": {
              "ItemId": "Ingredient_Silk_Fibre",
              "QuantityMin": 1,
              "QuantityMax": 3
            }
          }
        ]
      },
      {
        "Type": "Choice",
        "Containers": [
          {
            "Type": "Single",
            "Weight": 15,
            "Item": {
              "ItemId": "Ingredient_Silk_Thread",
              "QuantityMin": 1,
              "QuantityMax": 1
            }
          },
          {
            "Type": "Empty",
            "Weight": 85
          }
        ]
      }
    ]
  }
}
```

En cada ciclo de producción, un Silkworm siempre suelta 1-3 Fibra de Seda y tiene un 15% de probabilidad de soltar también 1 Hilo de Seda (un material de fabricación de nivel superior).

También crea la tabla de botín de matar NPC en `YourMod/Assets/Server/Drops/NPCs/Critter/Drop_Silkworm.json`:

```json
{
  "Container": {
    "Type": "Choice",
    "Containers": [
      {
        "Type": "Single",
        "Weight": 80,
        "Item": {
          "ItemId": "Ingredient_Silk_Fibre",
          "QuantityMin": 1,
          "QuantityMax": 1
        }
      },
      {
        "Type": "Empty",
        "Weight": 20
      }
    ]
  }
}
```

Matar a un Silkworm tiene un 80% de probabilidad de soltar 1 Fibra de Seda — mucho menos eficiente que criarlos en un corral (1-3 fibras por ciclo más probabilidad de hilo). Esto incentiva el ciclo de granja sobre la caza.

---

## Paso 5: Crear Modificadores de Crecimiento

Los modificadores de crecimiento aceleran los ciclos de producción cuando se cumplen las condiciones ambientales. Crea modificadores que afecten la producción de Silkworms.

Los modificadores vanilla en `Assets/Server/Farming/Modifiers/` ya se aplican globalmente. Puedes crear modificadores adicionales para tu sistema de granja o depender de los vanilla.

Para los Silkworms, crea un modificador de oscuridad ya que prefieren ambientes sombreados:

Crea `YourMod/Assets/Server/Farming/Modifiers/Darkness_Silkworm.json`:

```json
{
  "Type": "Darkness",
  "Modifier": 1.8
}
```

Esto les da a los Silkworms un multiplicador de tasa de crecimiento de 1.8x cuando su corral está en un área oscura (subterráneo o en una estructura con techo). Compara con el modificador de Luz vanilla que da 2x para áreas bien iluminadas — los Silkworms son lo opuesto, prefiriendo la oscuridad.

El modificador de Agua vanilla (`Modifier: 2.5`) y el modificador de Fertilizante (`Modifier: 2`) también se aplican a los corrales. Un corral de Silkworms cerca de agua en una cueva oscura se beneficiaría de ambos:

- Tasa base de producción: 1x
- Bonus de oscuridad: 1.8x
- Bonus de agua: 2.5x
- Combinado: producción aproximadamente 4.5x más rápida

### Comprensión del apilamiento de modificadores

Los modificadores se aplican multiplicativamente al temporizador base de producción. Si el `ProduceTimeout` de un Silkworm es de 24 horas del juego con la tasa base:

| Modificadores activos | Tiempo efectivo de producción |
|----------------------|------------------------------|
| Ninguno | 24 horas |
| Oscuridad (1.8x) | ~13.3 horas |
| Agua (2.5x) | ~9.6 horas |
| Oscuridad + Agua | ~5.3 horas |
| Oscuridad + Agua + Fertilizante (2x) | ~2.7 horas |

---

## Paso 6: Crear Reglas de Aparición para Silkworms Salvajes

Los Silkworms salvajes necesitan reglas de aparición para que los jugadores puedan encontrarlos y atraparlos. Colócalos en entornos de bosque donde aparezcan en grupos pequeños.

Crea `YourMod/Assets/Server/NPC/Spawn/World/Zone1/Spawns_Zone1_Silkworm.json`:

```json
{
  "Environments": [
    "Env_Zone1_Forests",
    "Env_Zone1_Autumn",
    "Env_Zone1_Azure"
  ],
  "NPCs": [
    {
      "Weight": 2,
      "SpawnBlockSet": "Soil",
      "Id": "Silkworm",
      "Flock": "One_Or_Two"
    }
  ],
  "DayTimeRange": [6, 14]
}
```

El peso 2 hace que los Silkworms sean poco comunes (la Ardilla vanilla usa peso 6). Solo aparecen durante las horas de la mañana y primera tarde, y aparecen en parejas como máximo — haciéndolos un recurso que vale la pena buscar.

---

## Paso 7: Crear Integración de Fabricación

Conecta la salida de la granja con el sistema de fabricación. Crea objetos que usen Fibra de Seda e Hilo de Seda.

Crea `YourMod/Assets/Server/Item/Items/MyMod/Ingredient_Silk_Fibre.json`:

```json
{
  "TranslationProperties": {
    "Name": "server.items.Ingredient_Silk_Fibre.name",
    "Description": "server.items.Ingredient_Silk_Fibre.description"
  },
  "Quality": "Common",
  "Icon": "Icons/ItemsGenerated/Ingredient_Silk_Fibre.png",
  "Categories": ["Items.Ingredients"],
  "MaxStack": 50,
  "DropOnDeath": true,
  "ResourceTypes": [
    { "Id": "Fibre" }
  ]
}
```

Crea `YourMod/Assets/Server/Item/Items/MyMod/Ingredient_Silk_Thread.json`:

```json
{
  "TranslationProperties": {
    "Name": "server.items.Ingredient_Silk_Thread.name",
    "Description": "server.items.Ingredient_Silk_Thread.description"
  },
  "Quality": "Uncommon",
  "Icon": "Icons/ItemsGenerated/Ingredient_Silk_Thread.png",
  "Categories": ["Items.Ingredients"],
  "MaxStack": 25,
  "DropOnDeath": true,
  "ResourceTypes": [
    { "Id": "Thread" }
  ],
  "Recipe": {
    "Input": [
      { "ItemId": "Ingredient_Silk_Fibre", "Quantity": 3 }
    ],
    "OutputQuantity": 1,
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Id": "Loom",
        "Categories": ["Textiles"]
      }
    ],
    "TimeSeconds": 4
  }
}
```

El Hilo de Seda puede fabricarse a partir de 3 Fibras de Seda en un Telar, u obtenerse raramente de la producción del corral. Esto crea dos caminos: los jugadores pueden esperar por botines afortunados o fabricar hilo activamente a partir de fibra.

---

## Paso 8: Agregar Claves de Traducción

Agrega a `YourMod/Assets/Languages/en-US.lang`:

```
server.npcRoles.Silkworm.name=Silkworm
server.npcRoles.Tamed_Silkworm.name=Silkworm
server.items.Ingredient_Silk_Fibre.name=Silk Fibre
server.items.Ingredient_Silk_Fibre.description=Fine fibre produced by silkworms. Used in textile crafting.
server.items.Ingredient_Silk_Thread.name=Silk Thread
server.items.Ingredient_Silk_Thread.description=Woven silk thread. A premium crafting material for light armour and decoration.
```

---

## Paso 9: Probar el Sistema de Granja

1. Coloca tu carpeta de mod en el directorio de mods del servidor e inicia el servidor.
2. Viaja a un bioma de bosque de la Zona 1 y busca Silkworms salvajes durante la mañana.
3. Sostén objetos de algodón cerca de un Silkworm para probar la mecánica de atracción y domesticación.
4. Construye o coloca una estructura de corral y prueba estas interacciones:

| Prueba | Resultado esperado |
|--------|-------------------|
| Colocar Silkworm domesticado en el corral | El Silkworm aparece dentro, el conteo de residentes aumenta |
| Colocar el 9no Silkworm (sobre capacidad) | El corral rechaza — MaxResidents es 8 |
| Esperar el ciclo de producción | Fibra de Seda (1-3) aparece en la salida del corral. 15% de probabilidad de Hilo de Seda |
| Verificar horas de deambulación | Los Silkworms deambulan libremente de 8 AM a 4 PM, regresan al refugio el resto del tiempo |
| Colocar corral cerca del agua | El temporizador de producción debería acelerarse (modificador de Agua 2.5x) |
| Colocar corral bajo tierra | El modificador de Oscuridad se aplica (1.8x) |
| Silkworm salvaje deambula dentro de 8 bloques | Capturado automáticamente en el corral (CaptureWildNPCsInRange) |
| Matar un Silkworm salvaje | 80% de probabilidad de 1 Fibra de Seda |
| Fabricar Hilo de Seda en el Telar | 3 Fibras de Seda = 1 Hilo de Seda |

### Solución de Problemas

| Problema | Causa | Solución |
|----------|-------|----------|
| El corral no acepta al Silkworm | Grupo de NPC no coincide | Asegúrate de que `AcceptedNpcGroups` coincida con el ID del grupo en `Groups/Silkworm.json` |
| Sin salida de producción | ID de tabla de botín no coincide | Verifica que las claves de `ProduceDrops` coincidan con los nombres de archivo de los roles de NPC |
| Producción muy lenta | Sin modificadores activos | Coloca el corral cerca del agua o en oscuridad para activar modificadores |
| La captura salvaje no funciona | Radio muy pequeño | Aumenta `WildCaptureRadius` o atrae a los Silkworms más cerca |
| La domesticación falla | Objeto atractivo incorrecto | Confirma que `AttractiveItemSet` contiene un ID de objeto válido |
| Los Silkworms no aparecen | Entorno no coincide | Verifica que el array `Environments` del archivo de aparición contenga IDs de entorno válidos |

---

## Listado Completo de Archivos

```
YourMod/
  Assets/
    Server/
      NPC/
        Roles/
          MyMod/
            Silkworm.json
            Tamed_Silkworm.json
        Groups/
          Silkworm.json
        Spawn/
          World/
            Zone1/
              Spawns_Zone1_Silkworm.json
      Farming/
        Coops/
          Coop_Silkworm.json
        Modifiers/
          Darkness_Silkworm.json
      Drops/
        NPCs/
          Critter/
            Drop_Silkworm.json
            Drop_Silkworm_Produce.json
      Item/
        Items/
          MyMod/
            Ingredient_Silk_Fibre.json
            Ingredient_Silk_Thread.json
    Languages/
      en-US.lang
```

---

## Próximos Pasos

- [Create a Custom Item](/hytale-modding-docs/tutorials/beginner/create-an-item) — crea armaduras y herramientas con Hilo de Seda
- [Recipes](/hytale-modding-docs/reference/crafting-system/recipes) — referencia completa de recetas de fabricación
- [Farming & Coops](/hytale-modding-docs/reference/economy-and-progression/farming-coops) — referencia completa del esquema de corrales
- [Drop Tables](/hytale-modding-docs/reference/economy-and-progression/drop-tables) — patrones avanzados de tablas de botín
- [NPC Groups](/hytale-modding-docs/reference/npc-system/npc-groups) — definiciones de grupos de NPCs
- [Weather System](/hytale-modding-docs/reference/world-and-environment/weather-system) — IDs de clima usados en condiciones del modificador de Agua
