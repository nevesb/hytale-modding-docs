---
title: Crear un Sistema de Combate Personalizado
description: Construye una pelea de jefe multifase con mecánicas de escudo, cambios de apariencia, invocación de esbirros, animaciones de ataque personalizadas y apariciones en el mundo.
---

import { Aside } from '@astrojs/starlight/components';

## Lo que aprenderás

Construye un encuentro completo con un **Slime Jefe** que incluye:
- Un jefe multifase que cambia de apariencia a medida que pierde HP
- Entity effects de escudo con resistencia al daño
- Animaciones de ataque personalizadas usando `ItemPlayerAnimations`
- Movimiento de combate con desplazamiento lateral (`MaintainDistance`)
- Invocación de esbirros durante las transiciones de fase
- Configuración de apariciones en el mundo para generación natural
- Botín con un objeto trofeo

<Aside type="tip">
El mod completo está disponible en GitHub: [hytale-mod-custom-combat-system](https://github.com/nevesb/hytale-mod-custom-combat-system)
</Aside>

## Requisitos previos

- Un mod funcional con un NPC personalizado (ver [Crear un NPC](/hytale-modding-docs/es/tutorials/beginner/create-an-npc))
- Comprensión de la aparición de NPCs (ver [Aparición Personalizada de NPCs](/hytale-modding-docs/es/tutorials/intermediate/custom-npc-spawning))
- Familiaridad con cadenas de interacción (ver [Árboles de Comportamiento de IA para NPCs](/hytale-modding-docs/es/tutorials/advanced/npc-ai-behavior-trees))

---

## Arquitectura del sistema

El sistema de jefe conecta varios tipos de archivos:

```
ModelAsset (BossSlime_Giant)     ─── define hitbox, animaciones de estado, apariencia
    │
ItemPlayerAnimations             ─── mapea IDs de animación de ataque a archivos .blockyanim
    │
Interaction (Boss_Slime_Attack)  ─── activa la animación de ataque + cadena de daño
    │
NPC Role (Boss_Slime_Giant)      ─── define fases, movimiento, estados de combate
    │
Entity Effect (Shield_Crystal)   ─── escudo con resistencia al daño + partículas
    │
World Spawn                      ─── generación natural en bosques de la Zona 1
```

---

## Paso 1: Crear el Model Asset del jefe

El jefe necesita una definición de modelo que mapee animaciones de estado (Idle, Walk, Death, etc.) pero **no** animaciones de ataque. Las animaciones de ataque se manejan por separado a través de `ItemPlayerAnimations`.

Crea `Server/Models/Beast/BossSlime_Giant.json`:

```json
{
  "Model": "NPC/Beast/BossSlime/Model/Model_Giant.blockymodel",
  "Texture": "NPC/Beast/BossSlime/Model/Texture_Giant.png",
  "EyeHeight": 1.5,
  "CrouchOffset": -0.5,
  "HitBox": {
    "Max": { "X": 1.5, "Y": 1.5, "Z": 1.5 },
    "Min": { "X": -3.0, "Y": 0, "Z": -3.0 }
  },
  "AnimationSets": {
    "Walk": {
      "Animations": [
        { "Animation": "NPC/Beast/BossSlime/Animations/Default/Walk.blockyanim" }
      ]
    },
    "Idle": {
      "Animations": [
        { "Animation": "NPC/Beast/BossSlime/Animations/Default/Idle.blockyanim" }
      ]
    },
    "Death": {
      "Animations": [
        { "Animation": "NPC/Beast/BossSlime/Animations/Default/Death.blockyanim", "Loop": false }
      ]
    },
    "Run": {
      "Animations": [
        { "Animation": "NPC/Beast/BossSlime/Animations/Default/Run.blockyanim" }
      ]
    },
    "Walk_Backward": {
      "Animations": [
        { "Animation": "NPC/Beast/BossSlime/Animations/Default/Walk_Backward.blockyanim" }
      ]
    }
  }
}
```

<Aside type="caution">
**No** añadas animaciones de ataque a `AnimationSets`. Las animaciones de ataque para NPCs deben definirse en un archivo `ItemPlayerAnimations` separado (Paso 2). Mezclarlas provoca que la animación no se reproduzca.
</Aside>

También necesitas model assets `BossSlime_Medium.json` y `BossSlime_Small.json` para las transiciones de fase (mismas animaciones, diferentes modelos/texturas). El `BossSlime.json` base sirve como apariencia predeterminada.

---

## Paso 2: Crear el mapeo de animación de ataque

Las bestias del juego base (Bear, Cactee, etc.) usan archivos `ItemPlayerAnimations` para mapear IDs de animación de combate a archivos `.blockyanim`. Tu jefe necesita lo mismo.

Crea `Server/Item/Animations/NPC/Beast/BossSlime/BossSlime_Default.json`:

```json
{
  "Animations": {
    "Attack": {
      "ThirdPerson": "NPC/Beast/BossSlime/Animations/Default/Attack.blockyanim",
      "Looping": false,
      "Speed": 1
    }
  },
  "Camera": {
    "Pitch": {
      "AngleRange": { "Max": 15, "Min": -15 },
      "TargetNodes": ["Head"]
    },
    "Yaw": {
      "AngleRange": { "Max": 15, "Min": -15 },
      "TargetNodes": ["Head"]
    }
  },
  "WiggleWeights": {
    "Pitch": 2, "PitchDeceleration": 0.1,
    "Roll": 0.1, "RollDeceleration": 0.1,
    "X": 3, "XDeceleration": 0.1,
    "Y": 0.1, "YDeceleration": 0.1,
    "Z": 0.1, "ZDeceleration": 0.1
  }
}
```

### Cómo funciona

| Sección | Propósito |
|---------|-----------|
| `Animations.Attack` | Mapea el ID `"Attack"` al archivo `.blockyanim` |
| `Camera` | Límites del seguimiento de cabeza durante el combate |
| `WiggleWeights` | Balanceo visual cuando el NPC se mueve o ataca |

La clave `"Attack"` es lo que se referencia en el `ItemAnimationId` de la interacción. El nombre del archivo `BossSlime_Default` se convierte en el `ItemPlayerAnimationsId`.

---

## Paso 3: Crear la interacción de ataque

El jefe usa la cadena vanilla `Root_NPC_Attack_Melee`, pero sobrescribe la animación inicial para usar el ataque personalizado del slime.

Crea `Server/Item/Interactions/Boss_Slime_Attack_Start.json`:

```json
{
  "Type": "Simple",
  "Effects": {
    "ItemPlayerAnimationsId": "BossSlime_Default",
    "ItemAnimationId": "Attack",
    "ClearAnimationOnFinish": false,
    "ClearSoundEventOnFinish": false
  },
  "RunTime": 0.1,
  "Next": {
    "Type": "Replace",
    "DefaultValue": {
      "Interactions": ["NPC_Attack_Selector_Left"]
    },
    "Var": "Melee_Selector"
  }
}
```

Esto reemplaza la interacción vanilla `NPC_Attack_Melee_Simple` (que usa la animación humanoide `SwingLeft`) con una interacción que reproduce la animación `Attack` del slime en su lugar.

Crea la interacción de daño en `Server/Item/Interactions/Boss_Slime_Slam_Damage.json`:

```json
{
  "Parent": "DamageEntityParent",
  "DamageCalculator": {
    "BaseDamage": { "Physical": 15 }
  },
  "DamageEffects": {
    "Knockback": { "Force": 3, "VelocityY": 4 },
    "WorldSoundEventId": "SFX_Unarmed_Impact",
    "LocalSoundEventId": "SFX_Unarmed_Impact"
  }
}
```

---

## Paso 4: Crear el Entity Effect de escudo

El escudo proporciona resistencia temporal al daño y un efecto visual de partículas.

Crea `Server/Entity/Effects/Shield_Crystal.json`:

```json
{
  "Duration": 1,
  "DamageResistance": {
    "Physical": [{ "Amount": 1.0, "CalculationType": "Multiplicative" }],
    "Slashing": [{ "Amount": 1.0, "CalculationType": "Multiplicative" }],
    "Bludgeoning": [{ "Amount": 1.0, "CalculationType": "Multiplicative" }],
    "Projectile": [{ "Amount": 1.0, "CalculationType": "Multiplicative" }],
    "Fire": [{ "Amount": 1.0, "CalculationType": "Multiplicative" }],
    "Ice": [{ "Amount": 1.0, "CalculationType": "Multiplicative" }],
    "Poison": [{ "Amount": 1.0, "CalculationType": "Multiplicative" }],
    "Environment": [{ "Amount": 1.0, "CalculationType": "Multiplicative" }]
  },
  "ApplicationEffects": {
    "Particles": [{ "SystemId": "Example_Shield" }]
  },
  "Invulnerable": false
}
```

### Notas de diseño

| Campo | Valor | Propósito |
|-------|-------|-----------|
| `Duration: 1` | 1 segundo | Duración corta, pero se refresca continuamente por los bloques de instrucciones del jefe |
| `Amount: 1.0` + `Multiplicative` | 100% de resistencia | Inmunidad total al daño mientras el escudo está activo |
| `SystemId: "Example_Shield"` | Partícula integrada | Muestra un efecto de burbuja de escudo alrededor del jefe |
| `Invulnerable: false` | No invulnerable | Permite que el escudo se rompa al infligir suficiente daño |

---

## Paso 5: Crear el Role del jefe

Este es el archivo principal. El jefe usa `Type: "Generic"` con una máquina de estados que controla fases, movimiento de combate y ataques.

Crea `Server/NPC/Roles/Boss_Slime_Giant.json`:

```json
{
  "Type": "Generic",
  "Appearance": "BossSlime_Giant",
  "MaxHealth": 450,
  "KnockbackScale": 0.5,
  "DisableDamageGroups": ["Self"],
  "DefaultNPCAttitude": "Ignore",
  "DefaultPlayerAttitude": "Neutral",
  "DropList": "Drop_BossSlime_Crown",
  "IsMemory": true,
  "MemoriesCategory": "Boss",
  "StartState": "Idle",
  "MotionControllerList": [
    {
      "Type": "Walk",
      "MaxWalkSpeed": 6,
      "Gravity": 10,
      "RunThreshold": 0.3,
      "MaxFallSpeed": 15,
      "MaxRotationSpeed": 360,
      "Acceleration": 8
    }
  ],
  "CombatConfig": {
    "EntityEffect": "Shield_Crystal"
  },
  "InteractionVars": {
    "Melee_Start": {
      "Interactions": ["Boss_Slime_Attack_Start"]
    },
    "Melee_Damage": {
      "Interactions": [{ "Parent": "Boss_Slime_Slam_Damage" }]
    }
  }
}
```

### Campos clave explicados

| Campo | Propósito |
|-------|-----------|
| `Type: "Generic"` | Control manual completo mediante bloques de instrucciones (sin IA de plantilla) |
| `InteractionVars.Melee_Start` | Sobrescribe `Root_NPC_Attack_Melee` para usar la animación de ataque del slime |
| `InteractionVars.Melee_Damage` | Sobrescribe la interacción de daño con valores personalizados |
| `CombatConfig.EntityEffect` | Aplica el efecto `Shield_Crystal` durante el combate |
| `DefaultPlayerAttitude: "Neutral"` | El jefe ignora a los jugadores hasta ser atacado |
| `StartState: "Idle"` | El jefe comienza en el estado Idle |

---

## Paso 6: Añadir transiciones de fase

Las transiciones de fase usan sensores `Once` que se activan cuando el HP cae por debajo de ciertos umbrales. Se añaden como `Instructions` con `Continue: true` para que se ejecuten en paralelo con otros bloques.

```json
{
  "$Comment": "Phase 1 end: HP <= 77.8% - spawn 1 slime",
  "Continue": true,
  "Instructions": [{
    "Sensor": {
      "Type": "Self", "Once": true,
      "Filters": [{
        "Type": "Stat", "Stat": "Health", "StatTarget": "Value",
        "RelativeTo": "Health", "RelativeToTarget": "Max",
        "ValueRange": [0, 0.778]
      }]
    },
    "Actions": [{
      "Type": "Spawn", "FanOut": true, "SpawnAngle": 360,
      "DistanceRange": [3, 5], "CountRange": [1, 1],
      "DelayRange": [0, 0], "Kind": "Slime"
    }]
  }]
}
```

El jefe completo tiene cuatro disparadores de fase:

| Fase | Umbral de HP | Acciones |
|------|-------------|----------|
| Fin de fase 1 | 77.8% (350 HP) | Invoca 1 Slime |
| Inicio de fase 2 | 55.6% (250 HP) | Cambia a apariencia Medium, reactiva el escudo, invoca 2 Slimes |
| Fin de fase 2 | 38.9% (175 HP) | Invoca 1 Slime |
| Inicio de fase 3 | 22.2% (100 HP) | Cambia a apariencia Small, invoca 2 Slimes |

El cambio de apariencia usa acciones de tipo `"Type": "Appearance"`:

```json
{ "Type": "Appearance", "Appearance": "BossSlime_Medium" }
```

Los bloques de refresco del escudo usan sensores continuos (sin `Once`) para reaplicar el escudo cada segundo durante las fases protegidas:

```json
{
  "Continue": true,
  "Instructions": [{
    "Sensor": {
      "Type": "Self",
      "Filters": [{
        "Type": "Stat", "Stat": "Health", "StatTarget": "Value",
        "RelativeTo": "Health", "RelativeToTarget": "Max",
        "ValueRange": [0.778, 1.0]
      }]
    },
    "Actions": [{
      "Type": "ApplyEntityEffect", "UseTarget": false,
      "EntityEffect": "Shield_Crystal"
    }]
  }]
}
```

---

## Paso 7: Añadir movimiento de combate

El jefe usa dos modos de movimiento controlados por estado:

**Estado Idle** — Deambula aleatoriamente, observa jugadores cercanos:

```json
{
  "Sensor": { "Type": "State", "State": "Idle" },
  "Instructions": [
    {
      "Sensor": { "Type": "Player", "Range": 20 },
      "HeadMotion": { "Type": "Watch" },
      "BodyMotion": { "Type": "Nothing" }
    },
    {
      "Sensor": { "Type": "Any" },
      "BodyMotion": {
        "Type": "Wander",
        "MaxHeadingChange": 45,
        "RelativeSpeed": 0.3
      }
    }
  ]
}
```

**Estado Combat** — Mantiene distancia y se desplaza lateralmente:

```json
{
  "Sensor": { "Type": "State", "State": "Combat" },
  "Instructions": [{
    "Sensor": { "Type": "Player", "Range": 30 },
    "BodyMotion": {
      "Type": "MaintainDistance",
      "DesiredDistanceRange": [1.5, 3.5],
      "MoveThreshold": 0.5,
      "RelativeForwardsSpeed": 0.6,
      "RelativeBackwardsSpeed": 0.5,
      "StrafingDurationRange": [1, 1],
      "StrafingFrequencyRange": [2, 2]
    }
  }]
}
```

### Parámetros de MaintainDistance

| Campo | Valor | Propósito |
|-------|-------|-----------|
| `DesiredDistanceRange: [1.5, 3.5]` | Mantenerse a 1.5-3.5 bloques del jugador | Lo suficientemente cerca para cuerpo a cuerpo, igual que el Template_Predator vanilla |
| `StrafingDurationRange: [1, 1]` | Desplazarse lateralmente durante 1 segundo | Crea el movimiento de "danza de combate" |
| `StrafingFrequencyRange: [2, 2]` | Desplazarse cada 2 segundos | Reposicionamiento regular durante el combate |
| `RelativeForwardsSpeed: 0.6` | 60% de velocidad al acercarse | Aproximación cautelosa |

<Aside type="caution">
Establecer `DesiredDistanceRange` demasiado alto (por ejemplo, `[3, 5]`) mantendrá al jefe fuera del rango cuerpo a cuerpo. Los depredadores cuerpo a cuerpo vanilla usan `[1.5, 3.5]` calculado a partir de `AttackDistance - 1`.
</Aside>

---

## Paso 8: Añadir acciones de combate

El bloque de combate maneja transiciones de estado y ataques:

```json
{
  "Instructions": [
    {
      "Sensor": { "Type": "State", "State": "Idle" },
      "Instructions": [
        {
          "Sensor": { "Type": "Damage" },
          "Actions": [{ "Type": "State", "State": "Combat" }]
        },
        {
          "Sensor": { "Type": "Any" },
          "Actions": [{ "Type": "Nothing" }]
        }
      ]
    },
    {
      "Sensor": { "Type": "State", "State": "Combat" },
      "Instructions": [
        {
          "Sensor": { "Type": "Player", "Range": 14 },
          "ActionsBlocking": true,
          "Actions": [
            {
              "Type": "Attack",
              "Attack": "Root_NPC_Attack_Melee",
              "AttackPauseRange": [1.0, 2.0]
            },
            { "Type": "Timeout", "Delay": [0.2, 0.2] }
          ],
          "HeadMotion": { "Type": "Aim", "RelativeTurnSpeed": 1.5 }
        },
        {
          "Sensor": { "Type": "Not", "Sensor": { "Type": "Player", "Range": 40 } },
          "Actions": [{ "Type": "State", "State": "Idle" }]
        }
      ]
    }
  ]
}
```

### Cómo InteractionVars sobrescribe la cadena de ataque

La cadena vanilla `Root_NPC_Attack_Melee` funciona a través de Replace Vars:

```
Root_NPC_Attack_Melee
  └─ Replace Var "Melee_Start" (default: NPC_Attack_Melee_Simple → SwingLeft)
       └─ Replace Var "Melee_Selector" (default: NPC_Attack_Selector_Left)
            └─ Replace Var "Melee_Damage" (default: daño genérico)
```

Al definir `InteractionVars` en el role del jefe, sobrescribes enlaces específicos:
- `Melee_Start` → `Boss_Slime_Attack_Start` (reproduce la animación del slime en lugar del golpe humanoide)
- `Melee_Damage` → `Boss_Slime_Slam_Damage` (valores de daño y retroceso personalizados)

---

## Paso 9: Crear el botín

Crea `Server/Drops/Drop_BossSlime_Crown.json`:

```json
{
  "Container": {
    "Type": "Choice",
    "Containers": [
      {
        "Type": "Single",
        "Item": { "ItemId": "Trophy_Slime_Crown", "QuantityMin": 1, "QuantityMax": 1 },
        "Weight": 100
      },
      {
        "Type": "Single",
        "Item": { "ItemId": "Ore_Crystal_Glow", "QuantityMin": 1, "QuantityMax": 3 },
        "Weight": 80
      }
    ]
  }
}
```

Crea el objeto trofeo en `Server/Item/Items/Trophy_Slime_Crown.json`:

```json
{
  "TranslationProperties": {
    "Name": "Slime Crown",
    "Description": "A trophy from the defeated Slime King"
  },
  "Model": "NPC/Beast/BossSlime/Model/Model_Crown.blockymodel",
  "Texture": "NPC/Beast/BossSlime/Model/Texture.png",
  "MaxStack": 1,
  "Scale": 0.5,
  "Icon": "Icons/ItemsGenerated/Trophy_Slime_Crown.png"
}
```

---

## Paso 10: Configurar las apariciones en el mundo

Añade el jefe y los slimes regulares a los bosques de la Zona 1.

Crea `Server/NPC/Spawn/World/Zone1/Spawns_Zone1_Forests_Slime.json`:

```json
{
  "Environments": [
    "Env_Zone1_Forests",
    "Env_Zone1_Autumn",
    "Env_Zone1_Azure"
  ],
  "NPCs": [
    {
      "Weight": 8,
      "SpawnBlockSet": "Soil",
      "Id": "Slime"
    },
    {
      "Weight": 1,
      "SpawnBlockSet": "Soil",
      "Id": "Boss_Slime_Giant"
    }
  ],
  "DayTimeRange": [6, 18]
}
```

### Diseño de aparición

| Campo | Propósito |
|-------|-----------|
| `Environments` | Las tres variantes de bosque de la Zona 1 |
| `Weight: 8` vs `Weight: 1` | Los slimes regulares son 8 veces más comunes que el jefe |
| `SpawnBlockSet: "Soil"` | Aparecen sobre bloques de tierra/pasto |
| `DayTimeRange: [6, 18]` | Solo de día (6 AM a 6 PM) |

---

## Paso 11: Probar el jefe

1. Activa el mod e inicia un servidor en la Zona 1.
2. Explora el Bosque Azure para encontrar slimes generados naturalmente.
3. Encuentra o invoca al Boss Slime Giant con la consola de desarrollador.

| Prueba | Resultado esperado |
|--------|-------------------|
| El jefe deambula en Idle | Se mueve lentamente, cambia de dirección aleatoriamente |
| El jugador se acerca a menos de 20 bloques | El jefe observa al jugador pero no ataca |
| El jugador golpea al jefe | El jefe entra en estado Combat, comienza a desplazarse lateralmente |
| El jefe ataca | Reproduce la animación de ataque del slime, inflige 15 de daño físico con retroceso |
| El HP baja del 77.8% | Invoca 1 Slime cercano |
| El HP baja del 55.6% | Cambia a apariencia Medium, el escudo se reactiva, invoca 2 Slimes |
| El HP baja del 38.9% | Invoca 1 Slime |
| El HP baja del 22.2% | Cambia a apariencia Small, invoca 2 Slimes |
| El jefe muere | Suelta el trofeo Slime Crown o mineral Crystal Glow |

### Solución de problemas

| Problema | Causa | Solución |
|----------|-------|----------|
| No hay animación de ataque | `AnimationSets` contiene `Attack` | Elimina `Attack` de los `AnimationSets` del modelo, defínelo solo en `ItemPlayerAnimations` |
| El jefe se queda demasiado lejos para golpear | `DesiredDistanceRange` demasiado alto | Usa `[1.5, 3.5]` para rango cuerpo a cuerpo |
| El jefe no se mueve en idle | `BodyMotion` establecido en `Nothing` | Añade `"Type": "Wander"` con `RelativeSpeed: 0.3` |
| El servidor no carga | `ItemPlayerAnimationsId` inválido | Asegúrate de que el archivo de animación exista en `Server/Item/Animations/` e incluya las secciones `Camera` + `WiggleWeights` |
| El jefe ataca pero no hace daño | Falta `InteractionVars.Melee_Damage` | Añade la sobrescritura de daño referenciando `Boss_Slime_Slam_Damage` |

---

## Estructura completa de archivos

```
CreateACustomNPC/
  Common/
    NPC/Beast/BossSlime/
      Animations/Default/
        Attack.blockyanim, Idle.blockyanim, Walk.blockyanim,
        Death.blockyanim, Run.blockyanim, Walk_Backward.blockyanim, ...
      Model/
        Model_Giant.blockymodel, Model_Medium.blockymodel,
        Model.blockymodel, Model_Crown.blockymodel,
        Texture_Giant.png, Texture_Medium.png, Texture.png
    Icons/
      ModelsGenerated/  (BossSlime_Giant.png, etc.)
      ItemsGenerated/   (Trophy_Slime_Crown.png)
  Server/
    Models/Beast/
      BossSlime_Giant.json, BossSlime_Medium.json,
      BossSlime_Small.json, BossSlime.json
    Item/
      Animations/NPC/Beast/BossSlime/BossSlime_Default.json
      Interactions/
        Boss_Slime_Attack_Start.json, Boss_Slime_Slam_Damage.json
      Items/Trophy_Slime_Crown.json
    Entity/Effects/Shield_Crystal.json
    Drops/Drop_BossSlime_Crown.json
    NPC/
      Roles/Boss_Slime_Giant.json
      Spawn/World/Zone1/Spawns_Zone1_Forests_Slime.json
  manifest.json
```

---

## Próximos pasos

- [Crear un NPC](/hytale-modding-docs/es/tutorials/beginner/create-an-npc) -- crea el NPC Slime base que el jefe invoca
- [Aparición Personalizada de NPCs](/hytale-modding-docs/es/tutorials/intermediate/custom-npc-spawning) -- aprende más sobre la configuración de apariciones en el mundo
- [Árboles de Comportamiento de IA para NPCs](/hytale-modding-docs/es/tutorials/advanced/npc-ai-behavior-trees) -- patrones avanzados de IA para NPCs
- [Entity Effects](/hytale-modding-docs/es/reference/combat-and-projectiles/entity-effects) -- referencia completa de entity effects
- [NPC Roles](/hytale-modding-docs/es/reference/npc-system/npc-roles) -- esquema completo de NPC roles
