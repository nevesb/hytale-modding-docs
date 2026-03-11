---
title: Crear un NPC personalizado
description: Tutorial paso a paso para agregar un NPC tipo criatura personalizado a Hytale, incluyendo definición de rol, tabla de botín y reglas de aparición.
---

## Objetivo

Agregar una criatura pasiva llamada **Mossbug** al mundo del juego. Crearás un JSON de rol de NPC que referencia un modelo, escribirás una tabla de botín para que suelte ingredientes al morir, y configurarás reglas de aparición para que aparezca en entornos de bosque.

## Requisitos previos

- Una carpeta de mod con un `manifest.json` válido (consulta [Configura tu entorno de desarrollo](/hytale-modding-docs/tutorials/beginner/setup-dev-environment))
- Familiaridad con la herencia de plantillas JSON (consulta [Conceptos básicos de JSON](/hytale-modding-docs/getting-started/json-basics))

---

## Resumen de tipos de NPC

Hytale organiza los NPCs en tipos definidos por la plantilla de la que heredan. Comprender las plantillas disponibles te ayuda a elegir la base correcta para tu NPC.

| Plantilla | Carpeta | Comportamiento |
|-----------|---------|---------------|
| `Template_Beasts_Passive_Critter` | `Creature/Critter/` | Animal pasivo pequeño — huye cuando se siente amenazado, deambula, puede ser atraído por comida |
| `Template_Animal_Neutral` | `Creature/Mammal/` | Bestia neutral más grande — ataca cuando es provocada |
| `Template_Predator` | `Creature/` | Caza activamente a jugadores dentro de su rango de visión |
| `Template_Livestock` | `Creature/Livestock/` | Animal de granja — puede mantenerse en corrales o establos |
| `Template_Birds_Passive` | `Avian/` | Ave pasiva voladora |
| `Template_Intelligent` | `Intelligent/` | NPC humanoide con capacidad de diálogo y misiones |
| `Template_Spirit` | `Elemental/` | Criatura elemental o mágica |

Para una criatura pasiva pequeña como el Mossbug, `Template_Beasts_Passive_Critter` es la base correcta. Proporciona comportamientos de deambulación, huida y curiosidad opcional — similar a cómo funcionan las ardillas y las ranas del juego base.

---

## Paso 1: Crear o referenciar un modelo

El campo `Appearance` de tu NPC nombra el conjunto de modelo que el motor usa para renderizar. Los nombres de apariencia del juego base como `Squirrel`, `Frog_Green` y `Mouse` se mapean a conjuntos de rig y animación preconstruidos.

Para una forma de criatura completamente nueva, necesitas un asset de apariencia personalizado (un modelo completo, rig y conjunto de animaciones en Blockbench). Para este tutorial, referenciamos una apariencia del juego base para hacer funcionar el NPC inmediatamente, y luego puedes reemplazarla con un modelo personalizado.

Usaremos `"Appearance": "Gecko"` como sustituto. Todos los nombres de apariencia disponibles del juego base se pueden encontrar revisando el campo `Appearance` en los archivos bajo `Assets/Server/NPC/Roles/`.

---

## Paso 2: Crear el JSON de rol del NPC

Los roles de NPC se encuentran en `Assets/Server/NPC/Roles/`. Organiza los NPCs de tu mod en una subcarpeta.

Crea:

```
YourMod/Assets/Server/NPC/Roles/MyMod/Mossbug.json
```

El patrón `Type: "Variant"` — usado por cada criatura del juego base incluyendo la ardilla y la rana — hereda toda la lógica de IA de la plantilla y sobrescribe solo los campos que difieren:

```json
{
  "Type": "Variant",
  "Reference": "Template_Beasts_Passive_Critter",
  "Modify": {
    "Appearance": "Gecko",
    "DropList": "Drop_Mossbug",
    "MaxHealth": 12,
    "IsMemory": true,
    "MemoriesCategory": "Critter",
    "MemoriesNameOverride": "Mossbug",
    "NameTranslationKey": {
      "Compute": "NameTranslationKey"
    }
  },
  "Parameters": {
    "NameTranslationKey": {
      "Value": "server.npcRoles.Mossbug.name",
      "Description": "Translation key for NPC name display"
    }
  }
}
```

### Campos de Modify explicados

| Campo | Propósito |
|-------|-----------|
| `Appearance` | El conjunto de modelo y animaciones a renderizar. Debe coincidir con un nombre de apariencia conocido |
| `DropList` | ID del archivo de tabla de botín (sin `.json`). Se resuelve desde `Assets/Server/Drops/` |
| `MaxHealth` | Puntos de vida. Las criaturas del juego base usan entre 10 y 20. La ardilla y la rana usan 15 |
| `IsMemory` | Si el jugador puede desbloquear esta criatura en su bestiario de Memorias |
| `MemoriesCategory` | Pestaña de categoría del bestiario: `Critter`, `Beast`, `Livestock`, `Other` |
| `MemoriesNameOverride` | El nombre mostrado en la pantalla de Memorias |
| `NameTranslationKey` | Clave de traducción para el nombre que aparece sobre la cabeza del NPC |

### Parameters

El bloque `Parameters` define valores a los que la plantilla accede mediante `{ "Compute": "FieldName" }`. Establecer `NameTranslationKey` aquí alimenta la expresión `"NameTranslationKey": { "Compute": "NameTranslationKey" }` de la plantilla.

### Sobrescrituras opcionales

La plantilla `Template_Beasts_Passive_Critter` expone parámetros adicionales que puedes establecer bajo `Modify`:

```json
"Modify": {
  "Appearance": "Gecko",
  "DropList": "Drop_Mossbug",
  "MaxHealth": 12,
  "MaxSpeed": 7,
  "WanderRadius": 8,
  "ViewRange": 12,
  "HearingRange": 12,
  "AttractiveItems": ["Food_Bread", "Ingredient_Fibre"]
}
```

`AttractiveItems` hace que la criatura investigue y recoja objetos tirados de la lista indicada — útil para mecánicas de domesticación o cebo.

---

## Paso 3: Crear una tabla de botín

Las tablas de botín se encuentran en `Assets/Server/Drops/`. Los drops de NPCs del juego base están organizados en `Drops/NPCs/<Category>/`. Crea:

```
YourMod/Assets/Server/Drops/NPCs/Critter/Drop_Mossbug.json
```

La estructura `Container` usa un sistema de selección basado en pesos. `Type: "Multiple"` ejecuta todos los contenedores hijos en orden. `Type: "Choice"` elige un hijo al azar, ponderado por el campo `Weight`.

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
              "ItemId": "Ingredient_Fibre",
              "QuantityMin": 1,
              "QuantityMax": 2
            }
          }
        ]
      },
      {
        "Type": "Choice",
        "Weight": 30,
        "Containers": [
          {
            "Type": "Single",
            "Item": {
              "ItemId": "Ingredient_Crystal",
              "QuantityMin": 1,
              "QuantityMax": 1
            }
          }
        ]
      }
    ]
  }
}
```

Esta tabla siempre suelta 1-2 de Fibra (peso 100 de 100 en ese grupo) y tiene un 30% de probabilidad de soltar también 1 Cristal. Compara con `Drop_Bear_Grizzly.json` que usa dos grupos `Choice` separados, cada uno con `Weight: 100`, para garantizar tanto un drop de piel como de carne.

### Tipos de contenedor de drops

| Tipo | Comportamiento |
|------|---------------|
| `Multiple` | Evalúa todos los contenedores hijos |
| `Choice` | Elige un hijo proporcionalmente al `Weight` |
| `Single` | Produce el `Item` especificado con una cantidad aleatoria entre `QuantityMin` y `QuantityMax` |

Si quieres que una criatura no suelte nada (como la ardilla y la rana del juego base), simplemente crea un objeto vacío:

```json
{}
```

---

## Paso 4: Crear reglas de aparición

Las reglas de aparición le indican al generador de mundo dónde y cuándo colocar tu NPC. Los archivos de aparición se encuentran en `Assets/Server/NPC/Spawn/World/<Zone>/`.

Crea:

```
YourMod/Assets/Server/NPC/Spawn/World/Zone1/Spawns_Zone1_MyMod_Critter.json
```

```json
{
  "Environments": [
    "Env_Zone1_Forests",
    "Env_Zone1_Autumn"
  ],
  "NPCs": [
    {
      "Weight": 3,
      "SpawnBlockSet": "Soil",
      "Id": "Mossbug",
      "Flock": "One_Or_Two"
    }
  ],
  "DayTimeRange": [
    6,
    18
  ]
}
```

### Campos de aparición explicados

| Campo | Propósito |
|-------|-----------|
| `Environments` | En qué biomas de entorno se aplica este archivo. Coincide con los IDs de entorno usados por la generación del mundo |
| `NPCs` | Lista de NPCs que pueden aparecer en estos entornos |
| `Weight` | Probabilidad relativa de que este NPC sea elegido frente a otros en el mismo archivo. Mayor = más común. La ardilla usa `Weight: 6` en los bosques de la Zona 1 |
| `SpawnBlockSet` | Tipo de superficie donde aparece el NPC: `Soil` (suelo), `Birds` (aire, para NPCs voladores), `Water` (acuático) |
| `Id` | El ID del rol del NPC — coincide con el nombre de tu archivo JSON de rol sin `.json` |
| `Flock` | Tamaño del grupo al aparecer. Valores disponibles: `One_Or_Two`, `Group_Small`, `Group_Large` |
| `DayTimeRange` | Rango de horas `[inicio, fin]` durante el cual las apariciones de este archivo están activas. `[6, 18]` = solo de día |

Para una criatura nocturna, usa `"DayTimeRange": [20, 6]` (cruza la medianoche).

### Entornos disponibles (ejemplos de Zona 1)

| ID de entorno | Descripción |
|---------------|-------------|
| `Env_Zone1_Forests` | Bosque templado estándar |
| `Env_Zone1_Autumn` | Bosque de colores otoñales |
| `Env_Zone1_Azure` | Variante de bosque azulado |
| `Env_Zone1_Mountains_Critter` | Terreno montañoso |

---

## Paso 5: Agregar claves de traducción

Agrega el texto del nombre del NPC al archivo de idioma de tu mod:

```
YourMod/Assets/Languages/en-US.lang
```

```
server.npcRoles.Mossbug.name=Mossbug
```

---

## Paso 6: Probar en el juego

1. Coloca la carpeta de tu mod en el directorio de mods del servidor.
2. Inicia el servidor. Observa la consola en busca de errores sobre IDs de rol desconocidos, apariencias faltantes o referencias inválidas de tablas de botín.
3. Usa el generador de NPCs del modo desarrollador para forzar la aparición de `Mossbug` en tu ubicación.
4. Confirma que el modelo se renderiza, el NPC deambula y huye cuando te acercas.
5. Mata al Mossbug y verifica que la tabla de botín suelte Fibra (y ocasionalmente Cristal).
6. Viaja a un bioma de Bosque de la Zona 1 y confirma que los Mossbugs aparezcan naturalmente durante el día.

**Errores comunes y soluciones:**

| Error | Causa | Solución |
|-------|-------|----------|
| `Unknown reference: Template_Beasts_Passive_Critter` | Plantilla no encontrada | Asegúrate de que los assets del juego base se carguen antes de tu mod |
| `Unknown appearance: Gecko` | Error en el nombre de apariencia | Revisa `Assets/Server/NPC/Roles/` para nombres de apariencia válidos |
| `Unknown drop list: Drop_Mossbug` | Ruta del archivo de drops incorrecta | Confirma que el archivo esté en `Drops/NPCs/Critter/Drop_Mossbug.json` |
| El NPC no aparece naturalmente | ID de entorno incorrecto | Verifica los nombres de entorno con los archivos de aparición del juego base |

---

## Archivos completos

### `YourMod/Assets/Server/NPC/Roles/MyMod/Mossbug.json`
```json
{
  "Type": "Variant",
  "Reference": "Template_Beasts_Passive_Critter",
  "Modify": {
    "Appearance": "Gecko",
    "DropList": "Drop_Mossbug",
    "MaxHealth": 12,
    "IsMemory": true,
    "MemoriesCategory": "Critter",
    "MemoriesNameOverride": "Mossbug",
    "NameTranslationKey": {
      "Compute": "NameTranslationKey"
    }
  },
  "Parameters": {
    "NameTranslationKey": {
      "Value": "server.npcRoles.Mossbug.name",
      "Description": "Translation key for NPC name display"
    }
  }
}
```

### `YourMod/Assets/Server/Drops/NPCs/Critter/Drop_Mossbug.json`
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
              "ItemId": "Ingredient_Fibre",
              "QuantityMin": 1,
              "QuantityMax": 2
            }
          }
        ]
      },
      {
        "Type": "Choice",
        "Weight": 30,
        "Containers": [
          {
            "Type": "Single",
            "Item": {
              "ItemId": "Ingredient_Crystal",
              "QuantityMin": 1,
              "QuantityMax": 1
            }
          }
        ]
      }
    ]
  }
}
```

### `YourMod/Assets/Server/NPC/Spawn/World/Zone1/Spawns_Zone1_MyMod_Critter.json`
```json
{
  "Environments": [
    "Env_Zone1_Forests",
    "Env_Zone1_Autumn"
  ],
  "NPCs": [
    {
      "Weight": 3,
      "SpawnBlockSet": "Soil",
      "Id": "Mossbug",
      "Flock": "One_Or_Two"
    }
  ],
  "DayTimeRange": [
    6,
    18
  ]
}
```

### `YourMod/Assets/Languages/en-US.lang`
```
server.npcRoles.Mossbug.name=Mossbug
```

---

## Siguientes pasos

- [Crear un objeto personalizado](/hytale-modding-docs/tutorials/beginner/create-an-item) — agrega un arma que tu NPC podría soltar
- [Crear un bloque personalizado](/hytale-modding-docs/tutorials/beginner/create-a-block) — crea un bloque como drop para la tabla de botín de tu NPC
- [Conceptos básicos de JSON](/hytale-modding-docs/getting-started/json-basics) — referencia sobre selección basada en pesos y valores calculados
