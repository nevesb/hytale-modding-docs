---
title: Árboles de Comportamiento de IA de NPCs
description: Inmersión profunda en la configuración de IA de NPCs usando condiciones de DecisionMaking, Combat Action Evaluators, prioridades de comportamiento, acciones de combate y condiciones de huida.
---

## Objetivo

Construir un NPC personalizado llamado **Ironclad Sentinel** (Centinela Acorazado) con IA compleja que alterna entre combate cuerpo a cuerpo y a distancia, se cura cuando tiene poca salud, pide ayuda a aliados y huye cuando está críticamente herido. Configurarás condiciones de Decision Making, un Combat Action Evaluator (CAE), y los conectarás a un rol de NPC con comportamiento de combate de múltiples estados.

## Prerrequisitos

- Una carpeta de mod con un `manifest.json` válido (ver [Configura tu Entorno de Desarrollo](/hytale-modding-docs/tutorials/beginner/setup-dev-environment))
- Comprensión de los roles y plantillas de NPCs (ver [NPC Roles](/hytale-modding-docs/reference/npc-system/npc-roles) y [NPC Templates](/hytale-modding-docs/reference/npc-system/npc-templates))
- Familiaridad con el sistema de condiciones (ver [NPC Decision Making](/hytale-modding-docs/reference/npc-system/npc-decision-making))
- Comprensión de los evaluadores de combate (ver [NPC Combat Balancing](/hytale-modding-docs/reference/npc-system/npc-combat-balancing))

---

## Cómo Funciona la IA de NPCs

La IA de NPCs de Hytale usa un sistema de decisión basado en utilidad. En cada tick, la IA evalúa las acciones disponibles puntuándolas a través de condiciones. La acción con la puntuación de utilidad más alta por encima de un umbral mínimo se ejecuta. Esto crea comportamiento emergente y sensible al contexto sin secuencias scriptadas.

### Vista General de la Arquitectura

```
NPC Role
├── Instructions (árbol de comportamiento: estados Idle, Alert, Combat)
├── Sensors (vista, oído, detección absoluta)
└── Combat Action Evaluator (CAE)
    ├── RunConditions (¿debería el evaluador ejecutarse este tick?)
    ├── AvailableActions (acciones puntuadas: cuerpo a cuerpo, distancia, curación, huida)
    │   └── Conditions (puntuación por acción: distancia, salud, enfriamiento)
    └── ActionSets (grupos de acciones activas por sub-estado)
```

### Conceptos Clave

| Concepto | Descripción |
|----------|-------------|
| **Condition** | Una función de puntuación que mapea una estadística del juego a una puntuación de utilidad 0-1 usando una curva de respuesta |
| **Response Curve** | Función matemática que determina cómo los valores crudos se mapean a puntuaciones: Linear, Logistic, Switch |
| **Action** | Un comportamiento de combate con nombre con condiciones, rangos de distancia y referencias a habilidades |
| **Action Set** | Un grupo con nombre de acciones y ataques básicos activos durante un sub-estado de combate |
| **Sub-State** | Un modo de combate entre el que el NPC puede alternar (Default, Ranged, Healing, etc.) |

---

## Paso 1: Comprender los Tipos de Condiciones

Las condiciones son los bloques de construcción de las decisiones de IA. Cada condición lee un valor del juego y lo mapea a una puntuación de 0-1 usando una curva. Múltiples condiciones en una acción se multiplican entre sí para producir la puntuación de utilidad final.

### Referencia de tipos de condiciones

| Tipo | Qué lee | Uso común |
|------|---------|-----------|
| `OwnStatPercent` | Estadística propia del NPC como % del máximo | Curar cuando la salud es baja |
| `TargetStatPercent` | Estadística del objetivo como % del máximo | Enfocarse en objetivos débiles |
| `TargetDistance` | Distancia al objetivo actual en bloques | Elegir entre cuerpo a cuerpo y distancia |
| `TimeSinceLastUsed` | Segundos desde que esta acción fue usada por última vez | Ritmo de enfriamiento |
| `Randomiser` | Valor aleatorio entre mínimo y máximo | Agregar imprevisibilidad |

### Tipos de curvas

La curva transforma un valor crudo en una puntuación de 0-1:

| Curva | Forma | Caso de uso |
|-------|-------|-------------|
| `"Linear"` | Línea recta, 0 a 1 | La puntuación aumenta proporcionalmente con el valor |
| `"ReverseLinear"` | Línea recta, 1 a 0 | Puntuación más alta cuando el valor es más bajo (curar cuando está herido) |
| `"SimpleLogistic"` | Curva S ascendente | La puntuación salta bruscamente en el rango medio (preferir cuando está cerca) |
| `"SimpleDescendingLogistic"` | Curva S descendente | La puntuación cae bruscamente (evitar cuando está cerca) |
| `Switch` con `SwitchPoint` | Cambio binario 0/1 | Compuerta dura: solo puntúa 1 después del umbral |

### Cómo se combinan las puntuaciones

Cuando una acción tiene múltiples condiciones, el motor multiplica todas las puntuaciones entre sí. Esto significa:

- Cualquier condición que puntúe 0 deshabilita la acción por completo
- Todas las condiciones deben puntuar razonablemente alto para que la acción gane
- Un `Randomiser` con `MinValue: 0.9, MaxValue: 1.0` agrega ligera imprevisibilidad sin dominar la puntuación

**Ejemplo**: Una acción con condiciones `[OwnStatPercent(Health, ReverseLinear), TimeSinceLastUsed(Linear, 0-5)]` puntúa más alto cuando el NPC está herido Y la acción no se ha usado recientemente. Si la salud está al 100%, `ReverseLinear` devuelve 0, haciendo imposible la acción independientemente del enfriamiento.

---

## Paso 2: Crear Archivos de Condiciones de Decision Making

Los archivos de condiciones independientes en `DecisionMaking/Conditions/` pueden ser referenciados por múltiples CAEs. Crea condiciones reutilizables para patrones comunes.

Crea `YourMod/Assets/Server/NPC/DecisionMaking/Conditions/Condition_LowHealth.json`:

```json
{
  "Type": "OwnStatPercent",
  "Stat": "Health",
  "Curve": "ReverseLinear"
}
```

Esta condición puntúa más alto (cerca de 1.0) cuando el NPC tiene muy poca salud, y más bajo (cerca de 0.0) con salud completa. Cualquier acción que use esta condición será fuertemente preferida cuando el NPC esté herido.

Crea `YourMod/Assets/Server/NPC/DecisionMaking/Conditions/Condition_TargetClose.json`:

```json
{
  "Type": "TargetDistance",
  "Curve": {
    "ResponseCurve": "SimpleDescendingLogistic",
    "XRange": [0, 12]
  }
}
```

Esto puntúa alto cuando el objetivo está cerca (dentro de ~4 bloques) y cae rápidamente a medida que la distancia se acerca a 12 bloques. La curva logística crea una transición brusca en lugar de gradual.

Crea `YourMod/Assets/Server/NPC/DecisionMaking/Conditions/Condition_TargetFar.json`:

```json
{
  "Type": "TargetDistance",
  "Curve": {
    "ResponseCurve": "SimpleLogistic",
    "XRange": [0, 15]
  }
}
```

Lo opuesto a `Condition_TargetClose` — puntúa alto cuando el objetivo está lejos, útil para activar ataques a distancia.

---

## Paso 3: Crear el Combat Action Evaluator

El CAE es el núcleo de la inteligencia de combate del NPC. Define todas las acciones de combate disponibles y las condiciones bajo las cuales cada una es preferida.

Crea `YourMod/Assets/Server/NPC/Balancing/Intelligent/CAE_Ironclad_Sentinel.json`:

```json
{
  "Type": "CombatActionEvaluator",
  "TargetMemoryDuration": 8,
  "CombatActionEvaluator": {
    "RunConditions": [
      {
        "Type": "TimeSinceLastUsed",
        "Curve": {
          "ResponseCurve": "Linear",
          "XRange": [0, 3]
        }
      },
      {
        "Type": "Randomiser",
        "MinValue": 0.9,
        "MaxValue": 1
      }
    ],
    "MinRunUtility": 0.5,
    "MinActionUtility": 0.01,
    "AvailableActions": {
      "SelectTarget": {
        "Type": "SelectBasicAttackTarget",
        "Description": "Select the best target for basic attacks",
        "Conditions": [
          {
            "Type": "TargetDistance",
            "Curve": {
              "ResponseCurve": "SimpleDescendingLogistic",
              "XRange": [0, 20]
            }
          }
        ]
      },
      "MeleeSwing": {
        "Type": "Ability",
        "Description": "Heavy melee swing when target is close",
        "WeaponSlot": 0,
        "SubState": "Melee",
        "Ability": "Sentinel_MeleeSwing",
        "Target": "Hostile",
        "AttackDistanceRange": [2.5, 2.5],
        "PostExecuteDistanceRange": [2.5, 2.5],
        "WeightCoefficient": 1.2,
        "Conditions": [
          {
            "Type": "TargetDistance",
            "Curve": {
              "ResponseCurve": "SimpleDescendingLogistic",
              "XRange": [0, 5]
            }
          },
          {
            "Type": "TimeSinceLastUsed",
            "Curve": {
              "ResponseCurve": "Linear",
              "XRange": [0, 1.5]
            }
          }
        ]
      },
      "ShieldBash": {
        "Type": "Ability",
        "Description": "Shield bash to stagger close targets",
        "WeaponSlot": 1,
        "SubState": "Melee",
        "Ability": "Sentinel_ShieldBash",
        "Target": "Hostile",
        "AttackDistanceRange": [2, 2],
        "PostExecuteDistanceRange": [3, 3],
        "WeightCoefficient": 1.0,
        "ChargeFor": 0.5,
        "Conditions": [
          {
            "Type": "TargetDistance",
            "Curve": {
              "ResponseCurve": "SimpleDescendingLogistic",
              "XRange": [0, 4]
            }
          },
          {
            "Type": "TimeSinceLastUsed",
            "Curve": {
              "Type": "Switch",
              "SwitchPoint": 5
            }
          }
        ]
      },
      "RangedThrow": {
        "Type": "Ability",
        "Description": "Throw projectile when target is at range",
        "WeaponSlot": 0,
        "SubState": "Ranged",
        "Ability": "Sentinel_SpearThrow",
        "Target": "Hostile",
        "AttackDistanceRange": [12, 12],
        "PostExecuteDistanceRange": [2.5, 2.5],
        "WeightCoefficient": 0.9,
        "Conditions": [
          {
            "Type": "TargetDistance",
            "Curve": {
              "ResponseCurve": "SimpleLogistic",
              "XRange": [0, 15]
            }
          },
          {
            "Type": "TimeSinceLastUsed",
            "Curve": {
              "ResponseCurve": "Linear",
              "XRange": [0, 3]
            }
          }
        ]
      },
      "HealSelf": {
        "Type": "Ability",
        "Description": "Heal when health is low",
        "Ability": "Sentinel_HealSelf",
        "Target": "Self",
        "WeightCoefficient": 1.5,
        "Conditions": [
          {
            "Type": "OwnStatPercent",
            "Stat": "Health",
            "Curve": "ReverseLinear"
          },
          {
            "Type": "TimeSinceLastUsed",
            "Curve": {
              "Type": "Switch",
              "SwitchPoint": 10
            }
          }
        ]
      },
      "CallForHelp": {
        "Type": "Ability",
        "Description": "Call nearby allies when hurt",
        "Ability": "Sentinel_CallForHelp",
        "Target": "Self",
        "WeightCoefficient": 1.3,
        "Conditions": [
          {
            "Type": "OwnStatPercent",
            "Stat": "Health",
            "Curve": "ReverseLinear"
          },
          {
            "Type": "TimeSinceLastUsed",
            "Curve": {
              "Type": "Switch",
              "SwitchPoint": 15
            }
          },
          {
            "Type": "Randomiser",
            "MinValue": 0.6,
            "MaxValue": 1
          }
        ]
      }
    },
    "ActionSets": {
      "Default": {
        "BasicAttacks": {
          "Attacks": ["Sentinel_MeleeSwing"],
          "Randomise": false,
          "MaxRange": 2.5,
          "Timeout": 0.5,
          "CooldownRange": [0.5, 1.0]
        },
        "Actions": [
          "SelectTarget",
          "MeleeSwing",
          "ShieldBash",
          "RangedThrow",
          "HealSelf",
          "CallForHelp"
        ]
      },
      "Melee": {
        "BasicAttacks": {
          "Attacks": ["Sentinel_MeleeSwing", "Sentinel_ShieldBash"],
          "Randomise": true,
          "MaxRange": 2.5,
          "Timeout": 0.5,
          "CooldownRange": [0.3, 0.8]
        },
        "Actions": [
          "SelectTarget",
          "ShieldBash",
          "RangedThrow",
          "HealSelf",
          "CallForHelp"
        ]
      },
      "Ranged": {
        "BasicAttacks": {
          "Attacks": ["Sentinel_SpearThrow"],
          "Randomise": false,
          "MaxRange": 12,
          "Timeout": 1.0,
          "CooldownRange": [1.5, 3.0]
        },
        "Actions": [
          "SelectTarget",
          "MeleeSwing",
          "HealSelf"
        ]
      }
    }
  }
}
```

### Desglose del diseño del CAE

**RunConditions** controlan con qué frecuencia se activa el evaluador:
- `TimeSinceLastUsed` con una curva Linear de 3 segundos significa que el evaluador puntúa más alto cuanto más tiempo ha pasado desde que se ejecutó por última vez
- `Randomiser` en 0.9-1.0 agrega un 10% de varianza para que el NPC no actúe en intervalos perfectamente predecibles
- `MinRunUtility: 0.5` significa que ambas condiciones deben puntuar por encima de ~0.7 cada una (0.7 * 0.7 = 0.49, justo por debajo del umbral) antes de que el evaluador se active

**WeightCoefficient** multiplica la puntuación de utilidad final:
- `HealSelf` en 1.5 lo hace fuertemente preferido cuando se cumplen las condiciones
- `CallForHelp` en 1.3 le da prioridad sobre los ataques básicos
- `RangedThrow` en 0.9 lo hace ligeramente menos preferido que el cuerpo a cuerpo cuando ambos son viables
- `MeleeSwing` en 1.2 le da al cuerpo a cuerpo una ligera ventaja sobre el valor predeterminado

**Cambio de sub-estado**: Cuando `MeleeSwing` se activa, activa el sub-estado `Melee`, que tiene enfriamientos más rápidos y ataques básicos aleatorizados entre golpe y golpe de escudo. Cuando `RangedThrow` se activa, cambia a `Ranged`, que solo tiene el lanzamiento de lanza como ataque básico con enfriamientos más largos.

**Desglose de la lógica de HealSelf**:
- `OwnStatPercent(Health, ReverseLinear)`: Al 50% de HP puntúa 0.5, al 20% de HP puntúa 0.8
- `TimeSinceLastUsed(Switch, 10)`: Compuerta dura — no puede curarse más a menudo que cada 10 segundos
- `WeightCoefficient: 1.5`: Multiplicado por las puntuaciones de las condiciones, esto supera la mayoría de las acciones de combate cuando la salud está por debajo de ~40%

---

## Paso 4: Crear el Rol del NPC

Conecta el CAE a un rol de NPC que use la base `Template_Intelligent`, que proporciona IA de combate con reconocimiento de facción y soporte para pedir ayuda.

Crea `YourMod/Assets/Server/NPC/Roles/MyMod/Ironclad_Sentinel.json`:

```json
{
  "Type": "Variant",
  "Reference": "Template_Intelligent",
  "Modify": {
    "Appearance": "Skeleton_Warrior",
    "DropList": "Drop_Ironclad_Sentinel",
    "MaxHealth": 180,
    "MaxSpeed": 5,
    "ViewRange": 20,
    "ViewSector": 220,
    "HearingRange": 16,
    "AlertedRange": 28,
    "DefaultPlayerAttitude": "Hostile",
    "DefaultNPCAttitude": "Neutral",
    "KnockbackScale": 0.6,
    "FlockArray": ["Ironclad_Sentinel"],
    "IsMemory": true,
    "MemoriesCategory": "Undead",
    "MemoriesNameOverride": "Ironclad Sentinel",
    "NameTranslationKey": {
      "Compute": "NameTranslationKey"
    }
  },
  "Parameters": {
    "NameTranslationKey": {
      "Value": "server.npcRoles.Ironclad_Sentinel.name",
      "Description": "Translation key for NPC name display"
    }
  }
}
```

### Notas de diseño del rol

| Campo | Valor | Justificación |
|-------|-------|---------------|
| `MaxHealth: 180` | Mayor que el Goblin Scrapper vanilla (~80) | Durabilidad de nivel jefe para un guardián de mazmorra |
| `ViewRange: 20` | Rango de visión extendido | Detecta intrusos desde más lejos |
| `ViewSector: 220` | Campo de visión amplio | Más difícil de acechar por detrás |
| `AlertedRange: 28` | Rango de alerta muy largo | Una vez alertado, rastrea jugadores a través de salas grandes |
| `KnockbackScale: 0.6` | Retroceso reducido | NPC con armadura pesada resiste ser empujado |
| `FlockArray` | Auto-referencia | Los Centinelas se coordinan como grupo |

La base `Template_Intelligent` proporciona:
- `ChanceToBeAlertedWhenReceivingCallForHelp: 70` — 70% de probabilidad de que Centinelas cercanos se unan al combate cuando uno pide ayuda
- Máquina de estados de IA de combate completa: Idle, Alert, Combat, Flee
- Actitudes con reconocimiento de facción para interacciones NPC-a-NPC

---

## Paso 5: Configurar el Comportamiento de Huida

El Centinela debería retirarse cuando está críticamente herido. El comportamiento de huida se controla mediante campos en el rol del NPC que la plantilla lee.

Agrega parámetros de huida al bloque `Modify` de tu rol:

```json
{
  "Type": "Variant",
  "Reference": "Template_Intelligent",
  "Modify": {
    "Appearance": "Skeleton_Warrior",
    "DropList": "Drop_Ironclad_Sentinel",
    "MaxHealth": 180,
    "MaxSpeed": 5,
    "ViewRange": 20,
    "ViewSector": 220,
    "HearingRange": 16,
    "AlertedRange": 28,
    "DefaultPlayerAttitude": "Hostile",
    "DefaultNPCAttitude": "Neutral",
    "KnockbackScale": 0.6,
    "FlockArray": ["Ironclad_Sentinel"],
    "FleeRange": 20,
    "FleeHealthThreshold": 0.15,
    "FleeSpeed": 7,
    "FleeIfNotThreatened": false,
    "IsMemory": true,
    "MemoriesCategory": "Undead",
    "MemoriesNameOverride": "Ironclad Sentinel",
    "NameTranslationKey": {
      "Compute": "NameTranslationKey"
    }
  },
  "Parameters": {
    "NameTranslationKey": {
      "Value": "server.npcRoles.Ironclad_Sentinel.name",
      "Description": "Translation key for NPC name display"
    }
  }
}
```

### Explicación de los campos de huida

| Campo | Propósito |
|-------|-----------|
| `FleeRange` | Distancia que el NPC intenta mantener de las amenazas cuando huye |
| `FleeHealthThreshold` | Porcentaje de salud por debajo del cual el NPC comienza a huir (0.15 = 15%) |
| `FleeSpeed` | Velocidad de movimiento mientras huye (más rápida que el `MaxSpeed: 5` normal) |
| `FleeIfNotThreatened` | Si es `true`, el NPC huye incluso de objetivos no amenazantes. `false` significa que solo huye de entidades que considera peligrosas |

Al 15% de salud (27 HP de 180), el Centinela cambia al modo de huida, corriendo a velocidad 7 mientras intenta mantener 20 bloques de distancia. Esto da a los jugadores una ventana para terminar la pelea antes de que el Centinela escape.

---

## Paso 6: Agregar Claves de Traducción y Tabla de Botín

Agrega a `YourMod/Assets/Languages/en-US.lang`:

```
server.npcRoles.Ironclad_Sentinel.name=Ironclad Sentinel
```

Crea `YourMod/Assets/Server/Drops/NPCs/Intelligent/Drop_Ironclad_Sentinel.json`:

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
              "QuantityMin": 2,
              "QuantityMax": 4
            }
          }
        ]
      },
      {
        "Type": "Choice",
        "Containers": [
          {
            "Type": "Single",
            "Weight": 20,
            "Item": {
              "ItemId": "Ingredient_Hide_Heavy",
              "QuantityMin": 1,
              "QuantityMax": 2
            }
          },
          {
            "Type": "Empty",
            "Weight": 80
          }
        ]
      },
      {
        "Type": "Choice",
        "Containers": [
          {
            "Type": "Single",
            "Weight": 5,
            "Item": {
              "ItemId": "Weapon_Sword_Iron",
              "QuantityMin": 1,
              "QuantityMax": 1
            }
          },
          {
            "Type": "Empty",
            "Weight": 95
          }
        ]
      }
    ]
  }
}
```

---

## Paso 7: Probar la IA

1. Coloca tu carpeta de mod en el directorio de mods del servidor.
2. Inicia el servidor y genera un Ironclad Sentinel usando el generador de NPCs de desarrollador.
3. Observa el comportamiento inactivo — el Centinela debería estar de guardia y escanear sus alrededores.
4. Acércate a menos de 20 bloques y confirma que el Centinela se pone en alerta.
5. Entra en combate y prueba los siguientes comportamientos:

| Prueba | Comportamiento esperado |
|--------|------------------------|
| Estar en rango cuerpo a cuerpo (< 3 bloques) | El Centinela usa MeleeSwing y ShieldBash |
| Estar a distancia (8-12 bloques) | El Centinela cambia a RangedThrow |
| Dañar al Centinela por debajo del 50% HP | La acción HealSelf se activa (si han pasado 10s de enfriamiento) |
| Dañar al Centinela por debajo del 15% HP | El Centinela huye a velocidad 7 |
| Generar 2 Centinelas, atacar a uno | El Centinela atacado pide ayuda, el segundo tiene 70% de probabilidad de unirse |
| Esperar después de que el Centinela huya | El Centinela mantiene 20 bloques de distancia |

### Solución de Problemas

| Problema | Causa | Solución |
|----------|-------|----------|
| El NPC nunca ataca | `MinActionUtility` demasiado alto | Reduce `MinActionUtility` a `0.001` |
| El NPC siempre usa el mismo ataque | Desequilibrio en `WeightCoefficient` | Ajusta los coeficientes para que sean más cercanos en valor |
| La curación nunca se activa | Switch point demasiado alto o umbral de salud no coincide | Reduce el `SwitchPoint` en la condición de enfriamiento de curación |
| El NPC no huye | `FleeHealthThreshold` demasiado bajo | Aumenta a 0.25 para pruebas |
| Pedir ayuda no funciona | NPCs cercanos no están en la misma manada | Asegúrate de que `FlockArray` incluya el ID del rol del NPC ayudante |
| La IA se siente muy lenta | `RunConditions` puntúan demasiado bajo | Reduce `XRange` en `TimeSinceLastUsed` para que el evaluador se active más frecuentemente |

---

## Próximos Pasos

- [Custom Combat System](/hytale-modding-docs/tutorials/advanced/custom-combat-system) — agrega tipos de daño personalizados a los ataques del Centinela
- [Custom Dungeons](/hytale-modding-docs/tutorials/advanced/custom-dungeons) — genera Centinelas dentro de instancias de mazmorras
- [NPC Decision Making](/hytale-modding-docs/reference/npc-system/npc-decision-making) — referencia completa de tipos de condiciones
- [NPC Combat Balancing](/hytale-modding-docs/reference/npc-system/npc-combat-balancing) — referencia del esquema CAE
- [Response Curves](/hytale-modding-docs/reference/concepts/response-curves) — detalles matemáticos de las formas de curva
