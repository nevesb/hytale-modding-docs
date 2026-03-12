---
title: Crear Instancias de Mazmorras Personalizadas
description: Cómo crear instancias de mazmorras personalizadas con prefabs, portales, configuraciones de jugabilidad, tablas de botín y encuentros con NPCs.
---

## Objetivo

Construir una instancia de mazmorra personalizada completa llamada **Sunken Vault** (Cripta Sumergida) — un área instanciada autocontenida a la que los jugadores entran a través de un portal, luchan contra encuentros con NPCs, recolectan botín de contenedores y salen al morir o completarla. Crearás una configuración de jugabilidad para la instancia, definirás puntos de entrada y salida del portal, configurarás tablas de botín de la mazmorra y conectarás las apariciones de NPCs dentro de la instancia.

## Prerrequisitos

- Una carpeta de mod con un `manifest.json` válido (ver [Configura tu Entorno de Desarrollo](/hytale-modding-docs/tutorials/beginner/setup-dev-environment))
- Familiaridad con la herencia de plantillas JSON (ver [Inheritance and Templates](/hytale-modding-docs/reference/concepts/inheritance-and-templates))
- Comprensión de los roles y reglas de aparición de NPCs (ver [Create a Custom NPC](/hytale-modding-docs/tutorials/beginner/create-an-npc))
- Comprensión de las tablas de botín (ver [Drop Tables](/hytale-modding-docs/reference/economy-and-progression/drop-tables))

---

## Cómo Funcionan las Instancias

Las instancias de Hytale son zonas de mundo aisladas con sus propias reglas de jugabilidad. Cuando un jugador entra en un portal vinculado a una instancia, el motor crea (o reutiliza) una copia de esa instancia y teletransporta al jugador dentro. Las instancias tienen su propia configuración de jugabilidad que puede sobrescribir las penalizaciones por muerte, la interacción con bloques y el comportamiento de reaparición independientemente del mundo principal.

Componentes clave:

| Componente | Ubicación del Archivo | Propósito |
|------------|----------------------|-----------|
| Gameplay Config | `Server/GameplayConfigs/` | Reglas de muerte, destrucción de bloques y reaparición dentro de la instancia |
| Portal Type | `Server/PortalTypes/` | Define el bloque de portal que transporta jugadores a la instancia |
| Environment | `Server/Environments/` | Clima y atmósfera dentro de la instancia |
| NPC Spawn Rules | `Server/NPC/Spawn/` | Qué NPCs aparecen dentro de la instancia |
| Drop Tables | `Server/Drops/` | Botín de contenedores y NPCs en la instancia |

---

## Paso 1: Crear la Configuración de Jugabilidad de la Instancia

Las configuraciones de jugabilidad de instancias heredan de `Default_Instance`, que deshabilita la destrucción de bloques y previene la pérdida de objetos al morir. El jugador es expulsado de la instancia cuando muere.

Crea `YourMod/Assets/Server/GameplayConfigs/SunkenVault.json`:

```json
{
  "Parent": "Default_Instance",
  "World": {
    "AllowBlockBreaking": false,
    "AllowBlockGathering": false,
    "DaytimeDurationSeconds": 0,
    "NighttimeDurationSeconds": 0
  },
  "Death": {
    "LoseItems": false,
    "RespawnController": {
      "Type": "ExitInstance"
    }
  },
  "Player": {
    "MovementConfig": "Default",
    "HitboxCollisionConfig": "SoftCollision",
    "ArmorVisibilityOption": "All"
  }
}
```

### Explicación de los campos de configuración

| Campo | Propósito |
|-------|-----------|
| `Parent` | Hereda todos los valores predeterminados de `Default_Instance`, que ya deshabilita la interacción con bloques |
| `AllowBlockBreaking` | Previene que los jugadores destruyan la estructura de la mazmorra |
| `AllowBlockGathering` | Previene la recolección de recursos dentro de la mazmorra |
| `DaytimeDurationSeconds: 0` | Congela el ciclo día/noche para que la mazmorra tenga un estado de iluminación fijo |
| `LoseItems: false` | Los jugadores conservan todos los objetos al morir dentro de la instancia |
| `RespawnController.Type: "ExitInstance"` | Morir expulsa al jugador de vuelta a la ubicación del portal en el mundo principal |

Compara con el `Default_Instance.json` vanilla que usa el mismo patrón. Tu configuración agrega el ciclo de tiempo congelado y ajustes explícitos del jugador.

---

## Paso 2: Crear el Entorno de la Instancia

El entorno de la instancia controla el clima y la atmósfera. Para una mazmorra, normalmente querrás un clima estático único sin variación.

Crea `YourMod/Assets/Server/Environments/SunkenVault.json`:

```json
{
  "WaterTint": "#0a3d6b",
  "SpawnDensity": 0.8,
  "Tags": {
    "Dungeon": [],
    "SunkenVault": []
  },
  "WeatherForecasts": {
    "0":  [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "1":  [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "2":  [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "3":  [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "4":  [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "5":  [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "6":  [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "7":  [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "8":  [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "9":  [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "10": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "11": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "12": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "13": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "14": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "15": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "16": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "17": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "18": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "19": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "20": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "21": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "22": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "23": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }]
  }
}
```

Usar un único ID de clima con peso 100 para cada hora crea una atmósfera constante. El `WaterTint` le da al agua subterránea un tinte azul-verde oscuro apropiado para una mazmorra sumergida. `SpawnDensity` en `0.8` reduce ligeramente las apariciones ambientales de NPCs comparado con el valor predeterminado del mundo principal de `0.5` (valores más altos significan más apariciones en contenido instanciado donde los encuentros están controlados).

---

## Paso 3: Definir el Tipo de Portal

Los tipos de portal definen el bloque con el que los jugadores interactúan para entrar en la instancia. El portal referencia la configuración de jugabilidad y el entorno que creaste.

Crea `YourMod/Assets/Server/PortalTypes/Portal_SunkenVault.json`:

```json
{
  "InstanceType": "SunkenVault",
  "GameplayConfig": "SunkenVault",
  "Environment": "SunkenVault",
  "MaxPlayers": 4,
  "PortalAppearance": "Portal_Dungeon",
  "SpawnOffset": {
    "X": 0,
    "Y": 1,
    "Z": 3
  },
  "ExitOffset": {
    "X": 0,
    "Y": 1,
    "Z": -3
  },
  "CooldownSeconds": 30,
  "RequiredItemToEnter": "Key_SunkenVault",
  "ConsumeRequiredItem": true
}
```

### Explicación de los campos del portal

| Campo | Propósito |
|-------|-----------|
| `InstanceType` | Identificador único para este tipo de instancia. Debe coincidir en todos los archivos de configuración relacionados |
| `GameplayConfig` | Referencia el ID del archivo de configuración de jugabilidad (nombre del archivo sin `.json`) |
| `Environment` | Referencia el ID del archivo de entorno |
| `MaxPlayers` | Máximo de jugadores concurrentes permitidos en una copia de la instancia |
| `PortalAppearance` | Visual del lado del cliente para el bloque de portal |
| `SpawnOffset` | Donde aparecen los jugadores relativo al origen de la instancia al entrar |
| `ExitOffset` | Donde aparecen los jugadores relativo al portal del mundo principal al salir |
| `CooldownSeconds` | Segundos mínimos antes de que un jugador pueda reentrar después de salir |
| `RequiredItemToEnter` | ID del objeto que el jugador debe tener en el inventario para usar el portal |
| `ConsumeRequiredItem` | Si el objeto requerido se consume al entrar |

Para crear un portal sin requisito de llave, omite tanto `RequiredItemToEnter` como `ConsumeRequiredItem`.

---

## Paso 4: Crear Tablas de Botín de la Mazmorra

Las mazmorras necesitan tablas de botín para los contenedores de tesoro colocados dentro de la instancia. Usa los tipos de contenedor `Multiple` y `Choice` para crear pools de botín variados.

Crea `YourMod/Assets/Server/Drops/Items/SunkenVault_Chest.json`:

```json
{
  "Container": {
    "Type": "Multiple",
    "Containers": [
      {
        "Type": "Choice",
        "Containers": [
          {
            "Type": "Single",
            "Weight": 60,
            "Item": {
              "ItemId": "Weapon_Sword_Copper",
              "QuantityMin": 1,
              "QuantityMax": 1
            }
          },
          {
            "Type": "Single",
            "Weight": 30,
            "Item": {
              "ItemId": "Weapon_Sword_Iron",
              "QuantityMin": 1,
              "QuantityMax": 1
            }
          },
          {
            "Type": "Single",
            "Weight": 10,
            "Item": {
              "ItemId": "Weapon_Sword_Gold",
              "QuantityMin": 1,
              "QuantityMax": 1
            }
          }
        ]
      },
      {
        "Type": "Choice",
        "Containers": [
          {
            "Type": "Single",
            "Weight": 70,
            "Item": {
              "ItemId": "Food_Bread",
              "QuantityMin": 2,
              "QuantityMax": 5
            }
          },
          {
            "Type": "Empty",
            "Weight": 30
          }
        ]
      },
      {
        "Type": "Choice",
        "Containers": [
          {
            "Type": "Single",
            "Weight": 50,
            "Item": {
              "ItemId": "Weapon_Arrow_Crude",
              "QuantityMin": 5,
              "QuantityMax": 15
            }
          },
          {
            "Type": "Empty",
            "Weight": 50
          }
        ]
      }
    ]
  }
}
```

Esta tabla de botín usa una raíz `Multiple` para evaluar tres pools independientes:

1. **Pool de armas** (garantizado) — siempre suelta un arma, ponderado hacia niveles inferiores
2. **Pool de comida** (70% de probabilidad) — a veces incluye pan para curación
3. **Pool de munición** (50% de probabilidad) — a veces incluye flechas

El tipo `Empty` con su propio peso crea la posibilidad de no obtener botín de ese pool. Compara este patrón con el `Barrels.json` vanilla que usa `Empty` con peso 800 para hacer que los botines sean raros.

Crea una tabla de botín de nivel jefe para la sala final:

`YourMod/Assets/Server/Drops/Items/SunkenVault_BossChest.json`:

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
              "ItemId": "Weapon_Sword_Gold",
              "QuantityMin": 1,
              "QuantityMax": 1
            }
          }
        ]
      },
      {
        "Type": "Choice",
        "Weight": 100,
        "Containers": [
          {
            "Type": "Single",
            "Item": {
              "ItemId": "Ingredient_Crystal",
              "QuantityMin": 3,
              "QuantityMax": 8
            }
          }
        ]
      },
      {
        "Type": "Choice",
        "Weight": 100,
        "Containers": [
          {
            "Type": "Single",
            "Item": {
              "ItemId": "Food_Bread",
              "QuantityMin": 5,
              "QuantityMax": 10
            }
          }
        ]
      }
    ]
  }
}
```

---

## Paso 5: Crear Encuentros con NPCs de la Mazmorra

Define NPCs que aparezcan dentro de la mazmorra. Los NPCs de instancias típicamente usan plantillas agresivas con más salud que sus contrapartes del mundo principal.

Crea `YourMod/Assets/Server/NPC/Roles/MyMod/SunkenVault_Guardian.json`:

```json
{
  "Type": "Variant",
  "Reference": "Template_Intelligent",
  "Modify": {
    "Appearance": "Skeleton_Warrior",
    "DropList": "Drop_SunkenVault_Guardian",
    "MaxHealth": 120,
    "MaxSpeed": 6,
    "ViewRange": 18,
    "HearingRange": 14,
    "AlertedRange": 24,
    "DefaultPlayerAttitude": "Hostile",
    "IsMemory": true,
    "MemoriesCategory": "Undead",
    "MemoriesNameOverride": "Vault Guardian",
    "NameTranslationKey": {
      "Compute": "NameTranslationKey"
    }
  },
  "Parameters": {
    "NameTranslationKey": {
      "Value": "server.npcRoles.SunkenVault_Guardian.name",
      "Description": "Translation key for NPC name display"
    }
  }
}
```

Crea la tabla de botín del guardián en `YourMod/Assets/Server/Drops/NPCs/Intelligent/Drop_SunkenVault_Guardian.json`:

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
              "ItemId": "Ingredient_Bone",
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
              "ItemId": "Ingredient_Crystal",
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

---

## Paso 6: Crear Reglas de Aparición de la Instancia

Las reglas de aparición de instancias funcionan como las del mundo principal pero referencian el entorno de la instancia. Crea reglas de aparición para los NPCs guardianes de la Sunken Vault.

Crea `YourMod/Assets/Server/NPC/Spawn/Instance/Spawns_SunkenVault.json`:

```json
{
  "Environments": [
    "SunkenVault"
  ],
  "NPCs": [
    {
      "Weight": 8,
      "SpawnBlockSet": "Soil",
      "Id": "SunkenVault_Guardian",
      "Flock": "Group_Small"
    }
  ],
  "DayTimeRange": [0, 24]
}
```

Establecer `DayTimeRange` en `[0, 24]` asegura que los guardianes aparezcan independientemente de la hora, lo cual es importante porque la instancia tiene un ciclo de tiempo congelado. El `Flock: "Group_Small"` genera guardianes en pequeños grupos de 2-4, creando encuentros significativos.

---

## Paso 7: Agregar Claves de Traducción

Crea `YourMod/Assets/Languages/en-US.lang` (o agrega a tu archivo existente):

```
server.npcRoles.SunkenVault_Guardian.name=Vault Guardian
```

---

## Paso 8: Probar la Mazmorra

1. Coloca tu carpeta de mod en el directorio de mods del servidor.
2. Inicia el servidor y verifica la consola en busca de errores sobre referencias faltantes.
3. Coloca el bloque de portal en el mundo principal usando las herramientas de desarrollador.
4. Entra en el portal y verifica que seas transportado a la instancia.
5. Confirma que los NPCs aparecen y tienen comportamiento hostil.
6. Abre un contenedor de botín y verifica que los objetos coincidan con tu tabla de botín.
7. Muere dentro de la instancia y confirma que eres expulsado al mundo principal sin perder objetos.

### Errores comunes y soluciones

| Error | Causa | Solución |
|-------|-------|----------|
| `Unknown gameplay config: SunkenVault` | Archivo de configuración no encontrado | Verifica que el archivo esté en `GameplayConfigs/SunkenVault.json` |
| `Unknown environment: SunkenVault` | ID de entorno no coincide | Asegúrate de que el nombre del archivo de entorno coincida con el campo `Environment` del portal |
| `Unknown portal type` | Tipo de portal no registrado | Verifica que `PortalTypes/Portal_SunkenVault.json` existe y tiene JSON válido |
| Los jugadores no son expulsados al morir | `RespawnController` incorrecto | Confirma que `"Type": "ExitInstance"` está configurado en la configuración de muerte |
| Los NPCs no aparecen | Etiqueta de entorno no coincide | Verifica que el array `Environments` del archivo de aparición coincida con el nombre del archivo de entorno de la instancia |
| Tabla de botín vacía | Ruta de tabla de botín incorrecta | Confirma que la ruta del archivo coincida con el patrón del ID de `DropList` |

---

## Listado Completo de Archivos

```
YourMod/
  Assets/
    Server/
      GameplayConfigs/
        SunkenVault.json
      Environments/
        SunkenVault.json
      PortalTypes/
        Portal_SunkenVault.json
      Drops/
        Items/
          SunkenVault_Chest.json
          SunkenVault_BossChest.json
        NPCs/
          Intelligent/
            Drop_SunkenVault_Guardian.json
      NPC/
        Roles/
          MyMod/
            SunkenVault_Guardian.json
        Spawn/
          Instance/
            Spawns_SunkenVault.json
    Languages/
      en-US.lang
```

---

## Próximos Pasos

- [NPC AI Behavior Trees](/hytale-modding-docs/tutorials/advanced/npc-ai-behavior-trees) — crea IA compleja para jefes de mazmorras
- [Custom Combat System](/hytale-modding-docs/tutorials/advanced/custom-combat-system) — agrega tipos de daño personalizados para peligros de mazmorras
- [World Generation Mods](/hytale-modding-docs/tutorials/advanced/world-generation-mods) — genera entradas de mazmorras en el mundo principal
- [Gameplay Configs](/hytale-modding-docs/reference/game-configuration/gameplay-configs) — referencia completa de campos de configuración de instancias
- [Drop Tables](/hytale-modding-docs/reference/economy-and-progression/drop-tables) — patrones avanzados de tablas de botín
