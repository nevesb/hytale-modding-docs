---
title: Reglas de Aparición de NPCs Personalizadas
description: Tutorial paso a paso para crear reglas de aparición de NPCs personalizadas con entornos, rangos de tiempo, fases lunares y condiciones de bioma.
---

## Objetivo

Crear reglas de aparición avanzadas que controlen dónde, cuándo y cómo aparecen tus NPCs en el mundo. Construirás archivos de aparición para criaturas diurnas del bosque, enemigos nocturnos del vacío con modificadores de fase lunar y depredadores específicos de zona con restricciones de nivel de luz.

## Lo que Aprenderás

- Cómo los archivos de reglas de aparición conectan entornos con roles de NPC
- Cómo usar `DayTimeRange` para restricciones de hora del día
- Cómo `Weight` y `Flock` controlan la frecuencia de aparición y el tamaño del grupo
- Cómo `SpawnBlockSet` determina el tipo de superficie para la aparición
- Cómo `MoonPhaseWeightModifiers`, `LightRanges` y `Despawn` crean comportamientos de aparición avanzados

## Requisitos Previos

- Una carpeta de mod con un `manifest.json` válido (ver [Configura tu Entorno de Desarrollo](/es/hytale-modding-docs/tutorials/beginner/setup-dev-environment))
- Al menos un rol de NPC personalizado (ver [Crear un NPC Personalizado](/es/hytale-modding-docs/tutorials/beginner/create-an-npc))

---

## Descripción General del Sistema de Aparición

Las reglas de aparición se encuentran en `Assets/Server/NPC/Spawn/World/` y están organizadas por zona. El motor lee cada archivo JSON en estos directorios y los fusiona. Cada archivo asocia una lista de entornos (biomas) con una lista de NPCs que pueden aparecer allí.

```
Assets/Server/NPC/Spawn/World/
  Zone0/
  Zone1/
    Spawns_Zone1_Forests_Critter.json
    Spawns_Zone1_Forests_Predator.json
    Spawns_Zone1_Mountains_Animal.json
  Zone2/
  Zone3/
  Zone4/
  Void/
  Unique/
```

---

## Paso 1: Crear una Regla de Aparición Diurna Básica

Este ejemplo genera criaturas en los biomas de bosque de la Zona 1 durante el día -- siguiendo el patrón utilizado por archivos vanilla como `Spawns_Zone1_Forests_Critter.json`.

Crea:

```
YourMod/Assets/Server/NPC/Spawn/World/Zone1/Spawns_Zone1_MyMod_Critter.json
```

```json
{
  "Environments": [
    "Env_Zone1_Forests",
    "Env_Zone1_Autumn",
    "Env_Zone1_Azure"
  ],
  "NPCs": [
    {
      "Weight": 4,
      "SpawnBlockSet": "Soil",
      "Id": "Mossbug",
      "Flock": "One_Or_Two"
    },
    {
      "Weight": 2,
      "SpawnBlockSet": "Birds",
      "Id": "Glowfly",
      "Flock": "Group_Small"
    }
  ],
  "DayTimeRange": [
    6,
    18
  ]
}
```

### Referencia de campos

| Campo | Propósito |
|-------|-----------|
| `Environments` | Array de IDs de entorno a los que aplica este archivo de aparición. El motor los compara con el mapa de biomas del generador de mundo |
| `NPCs` | Array de entradas de NPC que pueden aparecer en los entornos listados |
| `NPCs[].Weight` | Probabilidad relativa de aparición. Valores más altos significan más común. Las criaturas vanilla usan típicamente 2-6 |
| `NPCs[].SpawnBlockSet` | Tipo de superficie para la aparición: `"Soil"` (suelo), `"Birds"` (aire), `"Water"` (acuático) |
| `NPCs[].Id` | ID del rol de NPC -- coincide con el nombre del archivo JSON del rol sin `.json` |
| `NPCs[].Flock` | Tamaño del grupo. Valores de cadena: `"One_Or_Two"`, `"Group_Small"`, `"Group_Large"` |
| `DayTimeRange` | Horas `[inicio, fin]` (0-24) durante las cuales la aparición está activa. `[6, 18]` = 6 AM a 6 PM |

---

## Paso 2: Crear una Regla de Aparición Nocturna con Fases Lunares

Las criaturas del vacío en Hytale usan configuraciones de aparición avanzadas que incluyen modificadores de fase lunar y reglas de desaparición. Este patrón proviene de archivos en `Assets/Server/NPC/Spawn/World/Void/`.

Crea:

```
YourMod/Assets/Server/NPC/Spawn/World/Void/Spawns_MyMod_Night_Void.json
```

```json
{
  "Environments": [
    "Env_Zone1_Plains",
    "Env_Zone2_Savanna",
    "Env_Zone3_Tundra"
  ],
  "Despawn": {
    "DayTimeRange": [
      5,
      19
    ]
  },
  "MoonPhaseWeightModifiers": [
    0.5,
    1,
    1.5,
    1.5,
    1
  ],
  "NPCs": [
    {
      "Weight": 20,
      "SpawnBlockSet": "Soil",
      "Id": "Shadow_Crawler",
      "Flock": {
        "Size": [
          2,
          3
        ]
      }
    }
  ],
  "DayTimeRange": [
    19,
    5
  ],
  "LightRanges": {
    "Light": [
      0,
      8
    ]
  }
}
```

### Campos de aparición avanzados

| Campo | Propósito |
|-------|-----------|
| `Despawn.DayTimeRange` | Horas `[inicio, fin]` durante las cuales los NPCs generados son forzados a desaparecer. Se usa para eliminar criaturas nocturnas al amanecer |
| `MoonPhaseWeightModifiers` | Array de multiplicadores aplicados a todos los valores de `Weight` según la fase lunar actual. Índice 0 = luna nueva, índices más altos = lunas más llenas. Valores por encima de 1.0 aumentan las apariciones; por debajo de 1.0 las disminuyen |
| `LightRanges.Light` | Rango de nivel de luz `[min, max]` (0-15) requerido en la ubicación de aparición. `[0, 8]` significa que el NPC solo aparece en áreas oscuras |
| `Flock.Size` | Alternativa a los nombres de rebaño de cadena. Array `[min, max]` para tamaños de grupo personalizados |

### DayTimeRange nocturno

Cuando `inicio > fin` (ej., `[19, 5]`), el rango se extiende pasada la medianoche. Esto significa que la aparición está activa desde las 7 PM hasta las 5 AM.

---

## Paso 3: Crear una Aparición de Depredador Específica de Zona

Los depredadores usan pesos más altos y típicamente aparecen solos. Este patrón coincide con `Spawns_Zone1_Forests_Predator.json`.

Crea:

```
YourMod/Assets/Server/NPC/Spawn/World/Zone1/Spawns_Zone1_MyMod_Predator.json
```

```json
{
  "Environments": [
    "Env_Zone1_Forests",
    "Env_Zone1_Autumn"
  ],
  "NPCs": [
    {
      "Weight": 5,
      "SpawnBlockSet": "Soil",
      "Id": "Thornbeast"
    },
    {
      "Weight": 3,
      "SpawnBlockSet": "Soil",
      "Id": "Venomfang",
      "Flock": "One_Or_Two"
    }
  ],
  "DayTimeRange": [
    6,
    18
  ]
}
```

Cuando no se especifica `Flock` (como con Thornbeast arriba), el NPC aparece individualmente.

---

## Paso 4: Crear una Regla de Aparición Acuática

Para criaturas acuáticas, usa el set de bloques de aparición `Water` y el campo `SpawnFluidTag`:

```
YourMod/Assets/Server/NPC/Spawn/World/Zone1/Spawns_Zone1_MyMod_Aquatic.json
```

```json
{
  "Environments": [
    "Env_Zone1_Forests",
    "Env_Zone1_Autumn"
  ],
  "NPCs": [
    {
      "Weight": 10,
      "SpawnBlockSet": "Water",
      "SpawnFluidTag": "Water",
      "Id": "Glowfish",
      "Flock": "Group_Small"
    }
  ],
  "DayTimeRange": [
    6,
    18
  ]
}
```

### SpawnFluidTag

El campo `SpawnFluidTag` restringe la aparición a casillas que contienen un fluido específico. Usa `"Water"` para apariciones en agua dulce. Este campo se usa en archivos vanilla como `Spawns_Portals_Oasis_Animal.json` para flamingos cerca del agua.

---

## IDs de Entorno Disponibles

Aquí están los IDs de entorno comunes por zona:

| Zona | IDs de Entorno |
|------|----------------|
| Zona 1 | `Env_Zone1_Plains`, `Env_Zone1_Forests`, `Env_Zone1_Autumn`, `Env_Zone1_Azure`, `Env_Zone1_Mountains_Critter` |
| Zona 2 | `Env_Zone2_Savanna`, `Env_Zone2_Desert` |
| Zona 3 | `Env_Zone3_Tundra` |
| Único | `Env_Portals_Oasis` |

Consulta el campo `Environments` en los archivos de aparición vanilla bajo cada directorio de zona para la lista completa.

---

## Paso 5: Probar en el Juego

1. Coloca la carpeta de tu mod en el directorio de mods del servidor.
2. Inicia el servidor y observa si hay errores sobre IDs de NPC desconocidos o nombres de entorno inválidos.
3. Usa el spawner de NPCs del desarrollador para verificar que tus roles de NPC funcionen independientemente.
4. Viaja al bioma apropiado durante la hora correcta del día.
5. Para apariciones nocturnas, espera hasta el anochecer y aléjate de fuentes de luz.
6. Verifica que los tamaños de rebaño coincidan con tu configuración.
7. Para probar fases lunares, avanza el reloj del juego a través de múltiples días.

**Errores comunes y soluciones:**

| Error | Causa | Solución |
|-------|-------|----------|
| El NPC nunca aparece naturalmente | ID de entorno incorrecto | Compara los nombres de entorno con los archivos de aparición vanilla en la misma zona |
| El NPC aparece a la hora incorrecta | `DayTimeRange` invertido | Para nocturno, usa `[19, 5]` no `[5, 19]` |
| Demasiadas o muy pocas apariciones | `Weight` desbalanceado | Compara con pesos vanilla: criaturas usan 2-6, depredadores usan 3-5 |
| El NPC aparece en el aire | `SpawnBlockSet` incorrecto | Usa `"Soil"` para criaturas terrestres, `"Birds"` solo para NPCs voladores |
| Las criaturas del vacío persisten al amanecer | Falta `Despawn` | Agrega `"Despawn": { "DayTimeRange": [5, 19] }` |

---

## Próximos Pasos

- [Crear un NPC Personalizado](/es/hytale-modding-docs/tutorials/beginner/create-an-npc) -- define el rol de NPC que tus reglas de aparición referencian
- [Tablas de Botín Personalizadas](/es/hytale-modding-docs/tutorials/intermediate/custom-loot-tables) -- configura lo que tus NPCs generados dropean al ser derrotados
- [Armas de Proyectil](/es/hytale-modding-docs/tutorials/intermediate/projectile-weapons) -- crea armas para luchar contra tus depredadores generados
