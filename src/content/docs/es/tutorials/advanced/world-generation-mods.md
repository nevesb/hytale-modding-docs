---
title: Modificar la Generación de Mundo
description: Cómo modificar la generación de mundo usando configuraciones de HytaleGenerator, incluyendo pesos de biomas, asignaciones de entorno, distribución de minerales y colocación de estructuras.
---

## Objetivo

Modificar la generación procedural de mundo de Hytale para crear una región de bioma personalizada con configuraciones de entorno únicas, distribución de minerales ajustada, reglas de colocación de estructuras personalizadas y sobrecargas de aparición de NPCs. Al final comprenderás cómo los archivos de configuración de HytaleGenerator controlan la forma del terreno, la selección de biomas y la colocación de características.

## Prerrequisitos

- Una carpeta de mod con un `manifest.json` válido (ver [Configura tu Entorno de Desarrollo](/hytale-modding-docs/tutorials/beginner/setup-dev-environment))
- Familiaridad con la herencia de plantillas JSON (ver [Inheritance and Templates](/hytale-modding-docs/reference/concepts/inheritance-and-templates))
- Comprensión de los archivos de entorno (ver [Environments](/hytale-modding-docs/reference/world-and-environment/environments))
- Comprensión de las reglas de aparición de NPCs (ver [NPC Spawn Rules](/hytale-modding-docs/reference/npc-system/npc-spawn-rules))

---

## Cómo Funciona la Generación de Mundo

El generador de mundo de Hytale usa un sistema de configuración por capas almacenado en `Assets/Server/HytaleGenerator/`. El generador procesa el terreno en etapas:

1. **Selección de zona** — el mundo se divide en zonas (Zona 1 a Zona 4) basándose en la distancia desde el punto de aparición
2. **Asignación de bioma** — a cada chunk dentro de una zona se le asigna un bioma basándose en selección ponderada
3. **Modelado del terreno** — funciones de ruido generan elevación, cuevas y características de superficie
4. **Colocación de bloques** — se colocan bloques de superficie, capas subsuperficiales y vetas de mineral
5. **Generación de estructuras** — las estructuras prefabricadas (aldeas, ruinas, mazmorras) se colocan según las reglas
6. **Asignación de entorno** — cada bioma recibe un archivo de entorno que controla el clima
7. **Aparición de NPCs** — las reglas de aparición vinculadas a entornos pueblan el mundo con NPCs

### Estructura de Archivos del Generador

```
Assets/Server/HytaleGenerator/
  WorldGenerator.json          (configuración de nivel superior: límites de zona, ajustes de semilla)
  Zones/
    Zone1/
      Zone1_Config.json        (lista de biomas, reglas de estructuras para la Zona 1)
      Biomes/
        Forest.json            (forma del terreno, paleta de bloques, distribución de minerales)
        Mountains.json
        Plains.json
      Structures/
        Village.json           (reglas de colocación de estructuras)
        Ruins.json
    Zone2/
      ...
  OreDistribution/
    Default.json               (configuración global de vetas de mineral)
  StructureRules/
    Placement.json             (restricciones de espaciado y densidad)
```

---

## Paso 1: Comprender la Configuración de Zona

Las configuraciones de zona definen los biomas disponibles en una zona y sus pesos relativos. El generador selecciona un bioma para cada chunk basándose en estos pesos.

Aquí está la estructura de una configuración de zona:

```json
{
  "Biomes": [
    {
      "Id": "Forest",
      "Weight": 40,
      "Environment": "Env_Zone1_Forests",
      "MinDistanceFromSpawn": 0,
      "MaxDistanceFromSpawn": -1
    },
    {
      "Id": "Mountains",
      "Weight": 20,
      "Environment": "Env_Zone1_Mountains",
      "MinDistanceFromSpawn": 100,
      "MaxDistanceFromSpawn": -1
    },
    {
      "Id": "Plains",
      "Weight": 30,
      "Environment": "Env_Zone1",
      "MinDistanceFromSpawn": 0,
      "MaxDistanceFromSpawn": -1
    }
  ],
  "Structures": [
    {
      "Id": "Village_Small",
      "Weight": 5,
      "BiomeFilter": ["Forest", "Plains"],
      "MinSpacing": 500,
      "MaxPerZone": 10
    }
  ]
}
```

### Campos de entrada de bioma

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `Id` | string | Identificador único del bioma, referencia un archivo de definición de bioma |
| `Weight` | number | Probabilidad relativa de que este bioma sea seleccionado. Mayor = más común |
| `Environment` | string | ID del archivo de entorno que controla el clima en este bioma |
| `MinDistanceFromSpawn` | number | Distancia mínima en bloques desde el punto de aparición del mundo antes de que este bioma pueda aparecer. `0` = sin mínimo |
| `MaxDistanceFromSpawn` | number | Distancia máxima. `-1` = sin límite |

### Campos de entrada de estructura

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `Id` | string | Identificador del prefab de la estructura |
| `Weight` | number | Frecuencia relativa de colocación |
| `BiomeFilter` | string[] | En qué biomas puede aparecer esta estructura |
| `MinSpacing` | number | Distancia mínima en bloques entre instancias de esta estructura |
| `MaxPerZone` | number | Número máximo de esta estructura en toda la zona |

---

## Paso 2: Crear un Bioma Personalizado

Define un nuevo bioma con propiedades únicas de terreno y bloques. Los archivos de bioma controlan los parámetros de ruido que dan forma al terreno, la paleta de bloques de superficie y las vetas de mineral generadas bajo tierra.

Crea `YourMod/Assets/Server/HytaleGenerator/Zones/Zone1/Biomes/CrystalGrove.json`:

```json
{
  "Id": "CrystalGrove",
  "TerrainShape": {
    "BaseHeight": 72,
    "HeightVariation": 18,
    "NoiseScale": 0.02,
    "NoiseOctaves": 4,
    "Roughness": 0.45
  },
  "SurfaceBlocks": {
    "TopBlock": "Block_Grass_Azure",
    "FillerBlock": "Block_Dirt",
    "FillerDepth": 4,
    "StoneBlock": "Block_Stone"
  },
  "Features": {
    "Trees": {
      "Density": 0.15,
      "Types": [
        { "Id": "Tree_Azure_Medium", "Weight": 60 },
        { "Id": "Tree_Azure_Large", "Weight": 25 },
        { "Id": "Tree_Azure_Small", "Weight": 15 }
      ]
    },
    "Vegetation": {
      "Density": 0.3,
      "Types": [
        { "Id": "Plant_Fern_Azure", "Weight": 40 },
        { "Id": "Plant_Flower_Crystal", "Weight": 30 },
        { "Id": "Plant_Mushroom_Glow", "Weight": 30 }
      ]
    }
  },
  "OreOverrides": [
    {
      "OreId": "Ore_Crystal",
      "VeinSize": [3, 8],
      "HeightRange": [20, 60],
      "Frequency": 12
    },
    {
      "OreId": "Ore_Copper",
      "VeinSize": [2, 6],
      "HeightRange": [10, 50],
      "Frequency": 8
    }
  ],
  "CaveSettings": {
    "Frequency": 0.6,
    "MinHeight": 5,
    "MaxHeight": 55,
    "CaveWidth": [3, 7]
  }
}
```

### Campos de forma del terreno

| Campo | Propósito |
|-------|-----------|
| `BaseHeight` | Elevación promedio del terreno en bloques. Los bosques vanilla usan ~64-72 |
| `HeightVariation` | Desviación máxima de la altura base. Mayor = terreno más montañoso |
| `NoiseScale` | Controla la frecuencia de las características del terreno. Menor = características más suaves y grandes |
| `NoiseOctaves` | Número de capas de ruido combinadas. Más octavas = más detalle |
| `Roughness` | Multiplicador de rugosidad superficial. 0 = perfectamente suave, 1 = muy rugoso |

### Campos de sobrecarga de minerales

| Campo | Propósito |
|-------|-----------|
| `OreId` | ID de bloque del mineral a generar |
| `VeinSize` | `[min, max]` número de bloques por veta de mineral |
| `HeightRange` | `[min, max]` rango de nivel Y donde las vetas pueden aparecer |
| `Frequency` | Número de intentos de veta por chunk. Mayor = más mineral |

---

## Paso 3: Crear el Entorno del Bioma

Crea un archivo de entorno para el Crystal Grove con una atmósfera mística que presenta niebla frecuente y clima ocasional con tinte azur.

Crea `YourMod/Assets/Server/Environments/Zone1/Env_Zone1_CrystalGrove.json`:

```json
{
  "WaterTint": "#2a7bc4",
  "SpawnDensity": 0.6,
  "Tags": {
    "Zone1": [],
    "CrystalGrove": []
  },
  "WeatherForecasts": {
    "0":  [
      { "WeatherId": "Zone1_Sunny",       "Weight": 30 },
      { "WeatherId": "Zone1_Foggy_Light", "Weight": 40 },
      { "WeatherId": "Zone1_Cloudy_Medium", "Weight": 30 }
    ],
    "4":  [
      { "WeatherId": "Zone1_Foggy_Light", "Weight": 60 },
      { "WeatherId": "Zone1_Sunny",       "Weight": 30 },
      { "WeatherId": "Zone1_Rain_Light",  "Weight": 10 }
    ],
    "8":  [
      { "WeatherId": "Zone1_Sunny",       "Weight": 50 },
      { "WeatherId": "Zone1_Foggy_Light", "Weight": 30 },
      { "WeatherId": "Zone1_Rain_Light",  "Weight": 20 }
    ],
    "12": [
      { "WeatherId": "Zone1_Sunny",         "Weight": 60 },
      { "WeatherId": "Zone1_Cloudy_Medium",  "Weight": 30 },
      { "WeatherId": "Zone1_Rain_Light",    "Weight": 10 }
    ],
    "16": [
      { "WeatherId": "Zone1_Sunny",       "Weight": 40 },
      { "WeatherId": "Zone1_Foggy_Light", "Weight": 40 },
      { "WeatherId": "Zone1_Rain_Light",  "Weight": 20 }
    ],
    "18": [
      { "WeatherId": "Zone1_Sunny_Fireflies", "Weight": 50 },
      { "WeatherId": "Zone1_Foggy_Light",     "Weight": 40 },
      { "WeatherId": "Zone1_Sunny",           "Weight": 10 }
    ],
    "20": [
      { "WeatherId": "Zone1_Sunny_Fireflies", "Weight": 60 },
      { "WeatherId": "Zone1_Foggy_Light",     "Weight": 30 },
      { "WeatherId": "Zone1_Sunny",           "Weight": 10 }
    ],
    "22": [
      { "WeatherId": "Zone1_Foggy_Light",   "Weight": 50 },
      { "WeatherId": "Zone1_Sunny",         "Weight": 30 },
      { "WeatherId": "Zone1_Cloudy_Medium", "Weight": 20 }
    ]
  }
}
```

Observa la alta ponderación de niebla — esto crea una atmósfera mística donde la niebla aparece aproximadamente el 40-60% del tiempo, especialmente al amanecer y al atardecer. El clima `Sunny_Fireflies` aparece solo en horas de la tarde (18-21), coincidiendo con el patrón vanilla de la Zona 1.

---

## Paso 4: Registrar el Bioma en la Configuración de Zona

Para agregar tu bioma a la generación de la Zona 1, crea una configuración de zona de sobrecarga que añada el Crystal Grove a la lista de biomas.

Crea `YourMod/Assets/Server/HytaleGenerator/Zones/Zone1/Zone1_Config.json`:

```json
{
  "Biomes": [
    {
      "Id": "CrystalGrove",
      "Weight": 15,
      "Environment": "Env_Zone1_CrystalGrove",
      "MinDistanceFromSpawn": 200,
      "MaxDistanceFromSpawn": -1
    }
  ],
  "Structures": [
    {
      "Id": "Ruins_CrystalShrine",
      "Weight": 3,
      "BiomeFilter": ["CrystalGrove"],
      "MinSpacing": 800,
      "MaxPerZone": 3
    }
  ]
}
```

Un peso de 15 hace que el Crystal Grove sea relativamente poco común (compara con Forest en 40). Establecer `MinDistanceFromSpawn: 200` evita que aparezca justo en el punto de aparición del mundo, creando una sensación de descubrimiento.

---

## Paso 5: Crear Apariciones de NPCs Específicas del Bioma

Agrega apariciones de NPCs únicas vinculadas al entorno del Crystal Grove. Esto sigue el mismo patrón de reglas de aparición usado en el mundo principal pero referencia tu entorno personalizado.

Crea `YourMod/Assets/Server/NPC/Spawn/World/Zone1/Spawns_Zone1_CrystalGrove.json`:

```json
{
  "Environments": [
    "Env_Zone1_CrystalGrove"
  ],
  "NPCs": [
    {
      "Weight": 5,
      "SpawnBlockSet": "Soil",
      "Id": "Gecko",
      "Flock": "One_Or_Two"
    },
    {
      "Weight": 3,
      "SpawnBlockSet": "Soil",
      "Id": "Frog_Green",
      "Flock": "Group_Small"
    }
  ],
  "DayTimeRange": [6, 18]
}
```

Agrega un archivo de aparición nocturna separado para criaturas nocturnas:

Crea `YourMod/Assets/Server/NPC/Spawn/World/Zone1/Spawns_Zone1_CrystalGrove_Night.json`:

```json
{
  "Environments": [
    "Env_Zone1_CrystalGrove"
  ],
  "NPCs": [
    {
      "Weight": 4,
      "SpawnBlockSet": "Soil",
      "Id": "Bat",
      "Flock": "Group_Small"
    }
  ],
  "DayTimeRange": [20, 6]
}
```

---

## Paso 6: Definir Reglas de Colocación de Estructuras

Las estructuras son edificios o ruinas prefabricados colocados durante la generación del mundo. Define una estructura de Santuario de Cristal que solo aparece en tu bioma.

Crea `YourMod/Assets/Server/HytaleGenerator/StructureRules/Ruins_CrystalShrine.json`:

```json
{
  "Id": "Ruins_CrystalShrine",
  "PrefabId": "Prefab_CrystalShrine",
  "Placement": {
    "SurfaceSnap": true,
    "MinTerrainFlatness": 0.7,
    "ClearAbove": 10,
    "RotationMode": "Random90"
  },
  "LootContainers": [
    {
      "ContainerId": "Chest_CrystalShrine",
      "DropTable": "SunkenVault_Chest",
      "MaxPerStructure": 2
    }
  ],
  "NPCSpawners": [
    {
      "RoleId": "SunkenVault_Guardian",
      "Count": [1, 3],
      "SpawnRadius": 8
    }
  ]
}
```

### Campos de colocación

| Campo | Propósito |
|-------|-----------|
| `SurfaceSnap` | Alinea la estructura a la altura de la superficie del terreno |
| `MinTerrainFlatness` | Puntuación mínima de planitud (0-1) requerida en el sitio de colocación. Mayor = terreno más plano necesario |
| `ClearAbove` | Bloques mínimos de espacio libre por encima de la huella de la estructura |
| `RotationMode` | Cómo se rota la estructura: `Random90` selecciona 0/90/180/270 grados aleatoriamente |

---

## Paso 7: Probar tu Generación de Mundo

1. Coloca tu carpeta de mod en el directorio de mods del servidor.
2. Inicia el servidor con una **nueva semilla de mundo** — los mundos existentes no regenerarán chunks que ya hayan sido cargados.
3. Viaja al menos 200 bloques desde el punto de aparición (tu configuración de `MinDistanceFromSpawn`).
4. Busca el bioma Crystal Grove — hierba azur y vegetación de cristal.
5. Verifica que las apariciones de NPCs coincidan con tus reglas de aparición (gecos y ranas durante el día, murciélagos de noche).
6. Busca estructuras de Santuario de Cristal dentro del bioma.

### Solución de Problemas

| Problema | Causa | Solución |
|----------|-------|----------|
| El bioma nunca aparece | Peso demasiado bajo o requisito de distancia demasiado alto | Aumenta `Weight` a 25+ para pruebas, o reduce `MinDistanceFromSpawn` a 0 |
| Clima incorrecto en el bioma | ID de entorno no coincide | Verifica que el campo `Environment` de la configuración de zona coincida con el nombre de tu archivo de entorno |
| Sin minerales personalizados bajo tierra | Sobrecarga de minerales no aplicada | Confirma que `OreOverrides` usa IDs de bloques válidos que existen en el registro de bloques |
| Estructura flotando sobre el terreno | `SurfaceSnap` no establecido | Establece `"SurfaceSnap": true` en las reglas de colocación |
| Estructura apareciendo en el agua | Sin verificación de agua | Agrega `"AvoidWater": true` a las reglas de colocación |
| Mundo existente sin cambios | Los chunks ya fueron generados | Crea un nuevo mundo — el generador solo se ejecuta para chunks no visitados |

---

## Listado Completo de Archivos

```
YourMod/
  Assets/
    Server/
      HytaleGenerator/
        Zones/
          Zone1/
            Zone1_Config.json
            Biomes/
              CrystalGrove.json
        StructureRules/
          Ruins_CrystalShrine.json
      Environments/
        Zone1/
          Env_Zone1_CrystalGrove.json
      NPC/
        Spawn/
          World/
            Zone1/
              Spawns_Zone1_CrystalGrove.json
              Spawns_Zone1_CrystalGrove_Night.json
```

---

## Próximos Pasos

- [Custom Dungeons](/hytale-modding-docs/tutorials/advanced/custom-dungeons) — coloca portales de mazmorras dentro de estructuras generadas
- [NPC AI Behavior Trees](/hytale-modding-docs/tutorials/advanced/npc-ai-behavior-trees) — crea IA única para NPCs específicos del bioma
- [Environments](/hytale-modding-docs/reference/world-and-environment/environments) — referencia completa de horarios de clima
- [NPC Spawn Rules](/hytale-modding-docs/reference/npc-system/npc-spawn-rules) — detalles del formato de reglas de aparición
- [Weather System](/hytale-modding-docs/reference/world-and-environment/weather-system) — parámetros de definición de clima
