---
title: Reglas de Aparición de NPCs Personalizados
description: Tutorial paso a paso para crear reglas de aparición que hagan que los Slimes aparezcan en bosques Azure y un mercader Feran aparezca en biomas Feran.
sidebar:
  order: 6
---

## Objetivo

Crear **reglas de aparición** que hagan que tus NPCs personalizados aparezcan naturalmente en el mundo. Harás que el **Slime** del tutorial [Crear un NPC Personalizado](/hytale-modding-docs/tutorials/beginner/create-an-npc/) aparezca en bosques Azure, y que el **Mercader Encantado Feran** del tutorial [Tiendas de NPCs y Comercio](/hytale-modding-docs/tutorials/intermediate/npc-shops-and-trading/) aparezca en biomas Feran.

![Slime apareciendo naturalmente en un bioma de bosque Azure](/hytale-modding-docs/images/tutorials/custom-npc-spawning/slime-azure-forest.png)

## Lo Que Aprenderás

- Cómo los archivos de aparición del mundo controlan dónde y cuándo aparecen los NPCs en los biomas
- Cómo `Environments` conecta las reglas de aparición a biomas específicos
- Cómo `Weight`, `Flock` y `DayTimeRange` controlan la frecuencia de aparición, el tamaño del grupo y el horario
- Cómo `SpawnBlockSet` restringe a los NPCs a tipos de superficie específicos

## Requisitos Previos

- El mod del Slime NPC de [Crear un NPC Personalizado](/hytale-modding-docs/tutorials/beginner/create-an-npc/)
- El mod del Mercader Encantado Feran de [Tiendas de NPCs y Comercio](/hytale-modding-docs/tutorials/intermediate/npc-shops-and-trading/)

**Repositorio del mod complementario:** [hytale-mods-custom-npc-spawns](https://github.com/nevesb/hytale-mods-custom-npc-spawns)

---

## Visión General del Sistema de Aparición

Hytale usa **apariciones del mundo** para hacer que los NPCs aparezcan naturalmente mientras los jugadores exploran. Los archivos de aparición se encuentran en `Server/NPC/Spawn/World/` y están organizados por zona. El motor lee cada archivo JSON en cada directorio de zona y los fusiona. Cada archivo asocia una lista de entornos (biomas) con NPCs que pueden aparecer allí.

```
Server/NPC/Spawn/
  World/
    Zone0/          (Océano)
    Zone1/          (Bosque Azure, Llanuras, Montañas)
    Zone2/          (Feran, Sabana, Desierto)
    Zone3/          (Tundra)
    Void/           (Criaturas nocturnas)
```

### IDs de Entorno

Los entornos representan biomas. Cada zona tiene varias variantes de entorno:

| Zona | Entornos Comunes |
|------|-----------------|
| Zone 1 | `Env_Zone1_Forests`, `Env_Zone1_Azure`, `Env_Zone1_Autumn`, `Env_Zone1_Plains`, `Env_Zone1_Mountains_Critter` |
| Zone 2 | `Env_Zone2_Feran`, `Env_Zone2_Savanna`, `Env_Zone2_Desert`, `Env_Zone2_Oasis`, `Env_Zone2_Plateau` |
| Zone 3 | `Env_Zone3_Tundra` |

---

## Paso 1: Crear la Aparición del Slime en el Mundo

Las apariciones del mundo hacen que los NPCs aparezcan naturalmente mientras el jugador explora. Los depredadores vanilla como los Osos y las Arañas usan este sistema para poblar los bosques.

Aquí está la aparición de depredadores del bosque vanilla como referencia:

```json
// Vanilla: Spawns_Zone1_Forests_Predator.json
{
  "Environments": [
    "Env_Zone1_Forests",
    "Env_Zone1_Autumn",
    "Env_Zone1_Azure"
  ],
  "NPCs": [
    {
      "Weight": 5,
      "SpawnBlockSet": "Soil",
      "Id": "Bear_Grizzly"
    },
    {
      "Weight": 5,
      "SpawnBlockSet": "Soil",
      "Id": "Spider"
    }
  ],
  "DayTimeRange": [6, 18]
}
```

Ahora crea un archivo de aparición para los Slimes en bosques Azure y estándar:

```
NPCSpawning/Server/NPC/Spawn/World/Zone1/Spawns_Zone1_Azure_Slime.json
```

```json
{
  "Environments": [
    "Env_Zone1_Azure",
    "Env_Zone1_Forests"
  ],
  "NPCs": [
    {
      "Weight": 15,
      "SpawnBlockSet": "Soil",
      "Id": "Slime",
      "Flock": "One_Or_Two"
    }
  ],
  "DayTimeRange": [
    6,
    18
  ]
}
```

### Desglose de Campos

| Campo | Valor | Propósito |
|-------|-------|-----------|
| `Environments` | `["Env_Zone1_Azure", "Env_Zone1_Forests"]` | Los Slimes aparecen en biomas de bosque Azure y estándar |
| `Weight` | `15` | Frecuencia de aparición relativa a otros NPCs. Comparación: los depredadores vanilla usan 5 |
| `SpawnBlockSet` | `"Soil"` | Aparecen solo en bloques de suelo. Otras opciones: `"Birds"` (aire), `"Water"` (acuático), `"Volcanic"` (cueva) |
| `Id` | `"Slime"` | Coincide con el nombre del archivo de rol del NPC (`Slime.json`) sin `.json` |
| `Flock` | `"One_Or_Two"` | Aparecen 1-2 Slimes juntos. Otras opciones: `"Group_Small"`, `"Group_Medium"`, `"Group_Large"` |
| `DayTimeRange` | `[6, 18]` | Activo de 6 AM a 6 PM (solo durante el día) |

:::tip[Apariciones Nocturnas]
Para NPCs nocturnos, establece `DayTimeRange` en `[19, 5]` (se extiende pasada la medianoche — 7 PM a 5 AM). Agrega `"Despawn": { "DayTimeRange": [5, 19] }` para que desaparezcan al amanecer, como las criaturas Void vanilla.
:::

### Opciones de Flock

| Valor de Flock | Tamaño del Grupo | Caso de Uso |
|----------------|-------------------|-------------|
| *(omitido)* | 1 | Depredadores solitarios (Osos, Arañas) |
| `"One_Or_Two"` | 1-2 | Grupos ligeros |
| `"Group_Small"` | 2-4 | Manadas de criaturas |
| `"Group_Medium"` | 3-6 | Manadas de animales |
| `"Group_Large"` | 5-10 | Bandadas grandes |
| `{"Size": [2, 3]}` | 2-3 | Rango personalizado |

---

## Paso 2: Crear la Aparición del Mercader en el Mundo

El Mercader Encantado Feran aparece naturalmente en biomas Feran. Esto hace que el mercader aparezca en y alrededor de las ciudades Feran:

```
NPCSpawning/Server/NPC/Spawn/World/Zone2/Spawns_Zone2_Feran_Merchant.json
```

```json
{
  "Environments": [
    "Env_Zone2_Feran"
  ],
  "NPCs": [
    {
      "Weight": 100,
      "SpawnBlockSet": "Soil",
      "Id": "Feran_Enchanted_Merchant",
      "Flock": "One_Or_Two"
    }
  ],
  "DayTimeRange": [
    6,
    18
  ]
}
```

![Mercader Encantado Feran aparecido en una ciudad Feran — "Presiona F para comerciar"](/hytale-modding-docs/images/tutorials/custom-npc-spawning/feran-merchant-city.png)

| Campo | Valor | Propósito |
|-------|-------|-----------|
| `Environments` | `["Env_Zone2_Feran"]` | Aparece solo en biomas Feran (Zone 2) |
| `Weight` | `100` | Un peso alto asegura apariciones frecuentes. Comparación: las criaturas vanilla usan 5-20 |
| `Id` | `"Feran_Enchanted_Merchant"` | Coincide con el nombre del archivo de rol del NPC del mod NPCShopsAndTrading |
| `Flock` | `"One_Or_Two"` | Aparecen 1-2 mercaderes juntos |

:::tip[Múltiples Entornos]
Para que el mercader aparezca en todos los biomas de Zone 2, agrega más entornos al array: `["Env_Zone2_Feran", "Env_Zone2_Savanna", "Env_Zone2_Desert", "Env_Zone2_Oasis", "Env_Zone2_Plateau"]`.
:::

---

## Paso 3: Crear el Manifiesto

El mod de aparición depende tanto del mod del Slime NPC como del mod del NPC de Comercio:

```
NPCSpawning/manifest.json
```

```json
{
  "Group": "HytaleModdingManual",
  "Name": "NPCSpawning",
  "Version": "1.0.0",
  "Description": "Custom NPC spawn rules for Slime in Azure forests and Feran Enchanted Merchant in Feran cities",
  "Authors": [
    {
      "Name": "HytaleModdingManual"
    }
  ],
  "Dependencies": {
    "HytaleModdingManual:CreateACustomNPC": "1.0.0",
    "HytaleModdingManual:NPCShopsAndTrading": "1.0.0"
  },
  "OptionalDependencies": {},
  "IncludesAssetPack": false
}
```

Ten en cuenta que `IncludesAssetPack` es `false` — las reglas de aparición son archivos solo del servidor sin recursos del lado del cliente (sin modelos, texturas ni íconos).

---

## Paso 4: Opciones Avanzadas de Aparición

### Apariciones Nocturnas con Fases Lunares

Las criaturas Void usan apariciones solo nocturnas con modificadores de fase lunar. Este patrón hace que los NPCs sean más comunes durante la luna llena:

```json
{
  "Environments": [
    "Env_Zone1_Plains",
    "Env_Zone1_Forests"
  ],
  "NPCs": [
    {
      "Weight": 20,
      "SpawnBlockSet": "Soil",
      "Id": "Slime",
      "Flock": {
        "Size": [2, 4]
      }
    }
  ],
  "DayTimeRange": [19, 5],
  "MoonPhaseWeightModifiers": [0.5, 1, 1.5, 1.5, 1],
  "LightRanges": {
    "Light": [0, 8]
  },
  "Despawn": {
    "DayTimeRange": [5, 19]
  }
}
```

| Campo | Propósito |
|-------|-----------|
| `MoonPhaseWeightModifiers` | Array de multiplicadores por fase lunar (índice 0 = luna nueva). `1.5` duplica las apariciones en luna llena, `0.5` las reduce a la mitad en luna nueva |
| `LightRanges.Light` | `[min, max]` nivel de luz (0-15). `[0, 8]` restringe a áreas oscuras |
| `Despawn.DayTimeRange` | Los NPCs desaparecen forzosamente durante estas horas (limpieza al amanecer) |

### Apariciones Acuáticas

Para NPCs acuáticos, usa el conjunto de bloques `Water` con `SpawnFluidTag`:

```json
{
  "Environments": ["Env_Zone1_Forests"],
  "NPCs": [
    {
      "Weight": 10,
      "SpawnBlockSet": "Water",
      "SpawnFluidTag": "Water",
      "Id": "Glowfish",
      "Flock": "Group_Small"
    }
  ]
}
```

---

## Paso 5: Probar en el Juego

1. Copia la carpeta `NPCSpawning/` a `%APPDATA%/Hytale/UserData/Mods/`

2. Asegúrate de que los mods **CreateACustomNPC** y **NPCShopsAndTrading** también estén instalados (dependencias requeridas)

3. Inicia Hytale y prueba la aparición del Slime:
   - Viaja a un bioma de **Bosque Azure** o **Bosque estándar** en Zone 1
   - Explora durante el día (6 AM - 6 PM)
   - Los Slimes deberían aparecer naturalmente en grupos de 1-2

4. Prueba la aparición del Mercader:
   - Viaja a un **bioma Feran** en Zone 2
   - El Mercader Encantado debería aparecer naturalmente cerca de las ciudades Feran
   - Haz clic derecho para abrir la interfaz de comercio

**Errores comunes y soluciones:**

| Error | Causa | Solución |
|-------|-------|----------|
| El NPC nunca aparece | ID de entorno incorrecto | Verifica que `Environments` coincida con los nombres de bioma de los archivos de aparición vanilla en la misma zona |
| `Unknown NPC role` | Rol del NPC no encontrado | Verifica que el mod de dependencia esté instalado y que `Id` coincida con el nombre del archivo de rol |
| El NPC aparece a la hora incorrecta | `DayTimeRange` invertido | Día: `[6, 18]`. Noche: `[19, 5]` (inicio > fin se extiende pasada la medianoche) |
| Demasiadas apariciones | `Weight` demasiado alto | Compara con vanilla: criaturas usan 2-6, depredadores usan 3-5 |
| El NPC flota en el aire | `SpawnBlockSet` incorrecto | Usa `"Soil"` para criaturas terrestres, `"Birds"` solo para NPCs voladores |

---

## Resumen de la Estructura de Archivos

```
NPCSpawning/
  manifest.json
  Server/
    NPC/
      Spawn/
        World/
          Zone1/
            Spawns_Zone1_Azure_Slime.json
          Zone2/
            Spawns_Zone2_Feran_Merchant.json
```

---

## Referencia de Apariciones Vanilla

| Archivo Vanilla | Patrón | Caso de Uso |
|----------------|--------|-------------|
| `Spawns_Zone1_Forests_Predator.json` | Aparición del mundo, diurna, pesos iguales | Depredadores del bosque (Osos, Arañas) |
| `Spawns_Zone1_Forests_Critter.json` | Aparición del mundo, diurna, pesos variados + manadas | Criaturas del bosque (Jabalíes, Conejos) |
| `Spawns_Void_Zone1.json` | Aparición nocturna, fases lunares, rangos de luz | Criaturas Void |
| `Kweebec_Merchant.json` | Marcador dedicado de mercader | Mercader individual en aldeas Kweebec |

---

## Próximos Pasos

- [Crear un NPC Personalizado](/hytale-modding-docs/tutorials/beginner/create-an-npc/) — define los roles de NPC que tus reglas de aparición referencian
- [Tiendas de NPCs y Comercio](/hytale-modding-docs/tutorials/intermediate/npc-shops-and-trading/) — crea el NPC mercader Feran que aparece en asentamientos
- [Tablas de Botín Personalizadas](/hytale-modding-docs/tutorials/intermediate/custom-loot-tables/) — configura lo que sueltan tus NPCs al ser derrotados
