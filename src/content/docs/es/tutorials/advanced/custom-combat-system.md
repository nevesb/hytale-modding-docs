---
title: Crear un Sistema de Combate Personalizado
description: Creación de un sistema de combate personalizado con nuevos tipos de daño, efectos de entidad, interacciones de proyectiles, estadísticas de armas y balanceo de combate de NPCs.
---

## Objetivo

Construir un sistema de combate personalizado completo basado en un nuevo tipo de daño **Lightning** (Rayo). Crearás la definición del tipo de daño, un bastón de rayos como arma con configuraciones de proyectiles, efectos de entidad que se aplican al impactar, y un NPC que usa ataques de rayo con un Combat Action Evaluator ajustado. Este tutorial demuestra cómo se conectan los componentes de combate de Hytale: tipos de daño, proyectiles, interacciones, objetos e IA de NPCs.

## Prerrequisitos

- Una carpeta de mod con un `manifest.json` válido (ver [Configura tu Entorno de Desarrollo](/hytale-modding-docs/tutorials/beginner/setup-dev-environment))
- Comprensión de los tipos de daño (ver [Damage Types](/hytale-modding-docs/reference/combat-and-projectiles/damage-types))
- Comprensión de los proyectiles (ver [Projectiles](/hytale-modding-docs/reference/combat-and-projectiles/projectiles) y [Projectile Configs](/hytale-modding-docs/reference/combat-and-projectiles/projectile-configs))
- Familiaridad con las definiciones de objetos (ver [Item Definitions](/hytale-modding-docs/reference/item-system/item-definitions))
- Comprensión de la IA de combate de NPCs (ver [NPC Combat Balancing](/hytale-modding-docs/reference/npc-system/npc-combat-balancing))

---

## Arquitectura del Sistema

El sistema de combate involucra cinco tipos de archivo interconectados:

```
Damage Type  ─── define las propiedades del daño (pérdida de durabilidad, pérdida de resistencia, color)
    │
Projectile   ─── define la física y los valores base de daño
    │
Projectile Config ─── define los parámetros de lanzamiento y las cadenas de interacción
    │
Item Definition ─── define el arma que lanza el proyectil
    │
NPC CAE      ─── define la IA que usa las habilidades del arma
```

Cada componente referencia a los demás por ID. Construirlos en orden asegura que cada capa tenga sus dependencias en su lugar.

---

## Paso 1: Crear un Tipo de Daño Personalizado

Los tipos de daño definen cómo el daño interactúa con el objetivo: si causa pérdida de durabilidad, drenaje de resistencia, si evita las resistencias y qué color muestran los números de daño flotantes.

Crea `YourMod/Assets/Server/Entity/Damage/Lightning.json`:

```json
{
  "Parent": "Elemental",
  "Inherits": "Elemental",
  "DurabilityLoss": false,
  "StaminaLoss": true,
  "BypassResistances": false,
  "DamageTextColor": "#7DF9FF"
}
```

### Decisiones de diseño

| Campo | Valor | Justificación |
|-------|-------|---------------|
| `Parent: "Elemental"` | Hereda de la raíz Elemental | El rayo es un subtipo elemental, como Fuego y Hielo |
| `DurabilityLoss: false` | No daña el equipamiento | El daño elemental tradicionalmente no desgasta el equipo |
| `StaminaLoss: true` | Drena resistencia al impactar | El rayo electrocuta al objetivo, agotando su resistencia |
| `BypassResistances: false` | Sujeto a verificaciones de resistencia | Permite que la armadura y los buffs reduzcan el daño de rayo |
| `DamageTextColor: "#7DF9FF"` | Azul eléctrico | Distinto del Fuego (predeterminado) y el Veneno (#00FF00) |

La jerarquía de tipos de daño ahora se ve así:

```
Elemental
├── Fire
├── Ice
├── Poison
└── Lightning  (tu nuevo tipo)
```

---

## Paso 2: Crear el Proyectil de Rayo

Define la entidad de proyectil que vuela a través del mundo cuando el arma dispara.

Crea `YourMod/Assets/Server/Projectiles/Spells/LightningBolt.json`:

```json
{
  "Appearance": "LightningBolt",
  "Radius": 0.15,
  "Height": 0.3,
  "MuzzleVelocity": 55,
  "TerminalVelocity": 120,
  "Gravity": 2,
  "Bounciness": 0,
  "TimeToLive": 5,
  "Damage": 45,
  "DeadTime": 0,
  "DeathEffectsOnHit": true,
  "HitSoundEventId": "SFX_Lightning_Hit",
  "MissSoundEventId": "SFX_Lightning_Miss",
  "DeathSoundEventId": "SFX_Lightning_Death",
  "HitParticles": {
    "SystemId": "Impact_Lightning"
  },
  "MissParticles": {
    "SystemId": "Lightning_Sparks"
  },
  "DeathParticles": {
    "SystemId": "Lightning_Dissipate"
  },
  "ExplosionConfig": {
    "DamageEntities": true,
    "DamageBlocks": false,
    "EntityDamageRadius": 3,
    "EntityDamageFalloff": 0.5
  }
}
```

### Notas de diseño del proyectil

| Campo | Valor | Comparación |
|-------|-------|-------------|
| `MuzzleVelocity: 55` | Más rápido que la Bola de Fuego (40) | El rayo debería sentirse más rápido que el fuego |
| `Gravity: 2` | Gravedad baja | Trayectoria casi recta, a diferencia de las flechas (gravedad 10-15) |
| `Damage: 45` | Entre la Bola de Hielo (20) y la Bola de Fuego (60) | Equilibrado para un elemental de rango medio |
| `TimeToLive: 5` | 5 segundos de vida | Desaparece si no impacta nada |
| `EntityDamageRadius: 3` | AoE pequeño | Efecto de rayo encadenado en entidades cercanas, más pequeño que la Bola de Fuego (5) |
| `EntityDamageFalloff: 0.5` | 50% de daño en el borde | Las entidades en el borde del AoE reciben la mitad del daño |

Compara con la Bola de Fuego vanilla que tiene `MuzzleVelocity: 40`, `Gravity: 4`, `Damage: 60` y `EntityDamageRadius: 5`. El rayo intercambia daño bruto por velocidad y precisión.

---

## Paso 3: Crear la Configuración del Proyectil

La configuración del proyectil conecta el arma con el proyectil, definiendo los parámetros de lanzamiento y las cadenas de interacción para eventos de impacto/fallo.

Crea `YourMod/Assets/Server/ProjectileConfigs/Weapons/Staff/Lightning/Projectile_Config_LightningBolt.json`:

```json
{
  "Model": "LightningBolt",
  "LaunchForce": 35,
  "Physics": {
    "Type": "Standard",
    "Gravity": 2,
    "TerminalVelocityAir": 55,
    "TerminalVelocityWater": 10,
    "RotationMode": "VelocityDamped",
    "Bounciness": 0.0,
    "SticksVertically": false
  },
  "LaunchWorldSoundEventId": "SFX_Staff_Lightning_Shoot",
  "SpawnOffset": {
    "X": 0.1,
    "Y": -0.2,
    "Z": 0.5
  },
  "Interactions": {
    "ProjectileHit": {
      "Interactions": [
        {
          "Parent": "DamageEntityParent",
          "DamageCalculator": {
            "Class": "Charged",
            "BaseDamage": {
              "Lightning": 45
            }
          },
          "DamageEffects": {
            "Knockback": {
              "Type": "Force",
              "Force": 15,
              "VelocityType": "Set"
            },
            "WorldParticles": [
              { "SystemId": "Impact_Lightning" },
              { "SystemId": "Lightning_Sparks" }
            ],
            "WorldSoundEventId": "SFX_Lightning_Hit"
          }
        },
        {
          "Type": "ApplyEffect",
          "EffectId": "Effect_Lightning_Stun",
          "Duration": 1.5
        },
        {
          "Type": "RemoveEntity",
          "Entity": "User"
        }
      ]
    },
    "ProjectileMiss": {
      "Interactions": [
        {
          "Type": "Simple",
          "Effects": {
            "WorldSoundEventId": "SFX_Lightning_Miss",
            "WorldParticles": [
              { "SystemId": "Lightning_Sparks" }
            ]
          }
        },
        {
          "Type": "RemoveEntity",
          "Entity": "User"
        }
      ]
    },
    "ProjectileSpawn": {
      "Interactions": [
        {
          "Type": "Simple",
          "Effects": {
            "WorldParticles": [
              { "SystemId": "Lightning_Charge" }
            ]
          }
        }
      ]
    }
  }
}
```

### Desglose de la cadena de interacción

La cadena `ProjectileHit` ejecuta tres interacciones en secuencia:

1. **DamageEntityParent** — calcula y aplica daño usando el tipo de daño `Lightning` con 45 de daño base, con fuerza de retroceso de 15 y efectos de partículas/sonido
2. **ApplyEffect** — aplica un efecto de aturdimiento (`Effect_Lightning_Stun`) durante 1.5 segundos, impidiendo que el objetivo actúe
3. **RemoveEntity** — destruye el proyectil después de impactar

El campo `BaseDamage` usa un mapa de tipo de daño a valor: `{ "Lightning": 45 }`. Esto referencia tu tipo de daño personalizado por su ID de nombre de archivo. Compara con la configuración de la Bola de Hielo vanilla que usa `{ "Ice": 20 }`.

---

## Paso 4: Crear el Arma Bastón de Rayo

Define el objeto de arma que lanza rayos.

Crea `YourMod/Assets/Server/Item/Items/Weapon/Staff/Weapon_Staff_Lightning.json`:

```json
{
  "Parent": "Template_Weapon",
  "TranslationProperties": {
    "Name": "server.items.Weapon_Staff_Lightning.name",
    "Description": "server.items.Weapon_Staff_Lightning.description"
  },
  "Quality": "Rare",
  "Icon": "Icons/ItemsGenerated/Weapon_Staff_Lightning.png",
  "Categories": ["Items.Weapons.Staves"],
  "ItemLevel": 15,
  "MaxStack": 1,
  "MaxDurability": 250,
  "DurabilityLossOnHit": 2,
  "DropOnDeath": true,
  "PlayerAnimationsId": "Staff",
  "Model": "Items/Weapons/Staff/Lightning.blockymodel",
  "Texture": "Items/Weapons/Staff/Lightning_Texture.png",
  "Weapon": {},
  "Tags": {
    "Type": ["Weapon"],
    "Family": ["Staff"],
    "Element": ["Lightning"]
  },
  "Interactions": {
    "Primary": "Root_Primary_Staff_Lightning"
  },
  "InteractionVars": {
    "ProjectileConfig": {
      "Interactions": [
        {
          "Type": "SpawnProjectile",
          "ProjectileConfigId": "Projectile_Config_LightningBolt"
        }
      ]
    }
  },
  "Recipe": {
    "Input": [
      { "ItemId": "Ingredient_Crystal", "Quantity": 5 },
      { "ItemId": "Ingredient_Wood_Stick", "Quantity": 2 },
      { "ResourceTypeId": "Metal_Ingot", "Quantity": 3 }
    ],
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Id": "MagicBench",
        "Categories": ["Staves"]
      }
    ],
    "TimeSeconds": 10
  }
}
```

### Campos clave del arma

| Campo | Propósito |
|-------|-----------|
| `Weapon: {}` | Objeto vacío que activa el comportamiento de arma en el objeto |
| `PlayerAnimationsId: "Staff"` | Usa el conjunto de animaciones de bastón para el personaje del jugador |
| `MaxDurability: 250` | El bastón tiene 250 usos antes de romperse |
| `DurabilityLossOnHit: 2` | Cada disparo cuesta 2 de durabilidad (125 disparos en total) |
| `ProjectileConfigId` | Referencia la configuración del proyectil que define el comportamiento de lanzamiento |
| `Tags.Element: ["Lightning"]` | Etiqueta usada para filtrado y consultas de resistencia |

---

## Paso 5: Crear Efectos de Entidad

Los efectos de entidad son condiciones de estado aplicadas a los objetivos. Crea un efecto de aturdimiento que el rayo aplica al impactar.

Crea `YourMod/Assets/Server/Entity/Effects/Effect_Lightning_Stun.json`:

```json
{
  "Id": "Effect_Lightning_Stun",
  "Duration": 1.5,
  "Stackable": false,
  "MaxStacks": 1,
  "StatModifiers": {
    "MaxSpeed": {
      "Type": "Multiply",
      "Value": 0
    },
    "AttackSpeed": {
      "Type": "Multiply",
      "Value": 0
    }
  },
  "Particles": {
    "SystemId": "Lightning_Stun_Loop",
    "AttachToEntity": true
  },
  "Icon": "Icons/Effects/Lightning_Stun.png",
  "TranslationKey": "server.effects.Lightning_Stun.name"
}
```

### Diseño del efecto

| Campo | Propósito |
|-------|-----------|
| `Duration: 1.5` | El efecto dura 1.5 segundos |
| `Stackable: false` | Golpear a un objetivo aturdido no extiende el aturdimiento |
| `StatModifiers.MaxSpeed` | Multiplicar por 0 = el objetivo no puede moverse |
| `StatModifiers.AttackSpeed` | Multiplicar por 0 = el objetivo no puede atacar |
| `Particles` | Indicador visual adjunto a la entidad aturdida |

Crea un segundo efecto para un debuff de daño con el tiempo de rayo:

Crea `YourMod/Assets/Server/Entity/Effects/Effect_Lightning_Shock.json`:

```json
{
  "Id": "Effect_Lightning_Shock",
  "Duration": 5,
  "Stackable": true,
  "MaxStacks": 3,
  "TickInterval": 1.0,
  "TickDamage": {
    "DamageType": "Lightning",
    "Amount": 8
  },
  "StatModifiers": {
    "MaxSpeed": {
      "Type": "Multiply",
      "Value": 0.7
    }
  },
  "Particles": {
    "SystemId": "Lightning_Shock_Loop",
    "AttachToEntity": true
  },
  "Icon": "Icons/Effects/Lightning_Shock.png",
  "TranslationKey": "server.effects.Lightning_Shock.name"
}
```

Este se acumula hasta 3 veces, infligiendo 8 de daño Lightning por segundo por acumulación (máximo 24/segundo) mientras ralentiza al objetivo al 70% de velocidad. Cada acumulación tiene su propia duración de 5 segundos.

---

## Paso 6: Crear un NPC que Use Rayos

Construye un NPC **Storm Mage** (Mago de Tormenta) que usa ataques de rayo en combate, demostrando cómo la IA de NPCs se integra con el sistema de combate personalizado.

Crea `YourMod/Assets/Server/NPC/Roles/MyMod/Storm_Mage.json`:

```json
{
  "Type": "Variant",
  "Reference": "Template_Intelligent",
  "Modify": {
    "Appearance": "Mage_Storm",
    "DropList": "Drop_Storm_Mage",
    "MaxHealth": 95,
    "MaxSpeed": 5,
    "ViewRange": 22,
    "ViewSector": 180,
    "HearingRange": 14,
    "AlertedRange": 30,
    "DefaultPlayerAttitude": "Hostile",
    "FleeRange": 18,
    "FleeHealthThreshold": 0.2,
    "FleeSpeed": 7,
    "IsMemory": true,
    "MemoriesCategory": "Other",
    "MemoriesNameOverride": "Storm Mage",
    "NameTranslationKey": {
      "Compute": "NameTranslationKey"
    }
  },
  "Parameters": {
    "NameTranslationKey": {
      "Value": "server.npcRoles.Storm_Mage.name",
      "Description": "Translation key for NPC name display"
    }
  }
}
```

Crea el CAE del Storm Mage en `YourMod/Assets/Server/NPC/Balancing/Intelligent/CAE_Storm_Mage.json`:

```json
{
  "Type": "CombatActionEvaluator",
  "TargetMemoryDuration": 6,
  "CombatActionEvaluator": {
    "RunConditions": [
      {
        "Type": "TimeSinceLastUsed",
        "Curve": { "ResponseCurve": "Linear", "XRange": [0, 4] }
      },
      { "Type": "Randomiser", "MinValue": 0.9, "MaxValue": 1 }
    ],
    "MinRunUtility": 0.5,
    "MinActionUtility": 0.01,
    "AvailableActions": {
      "SelectTarget": {
        "Type": "SelectBasicAttackTarget",
        "Description": "Select target for ranged lightning attacks",
        "Conditions": [
          {
            "Type": "TargetDistance",
            "Curve": { "ResponseCurve": "SimpleDescendingLogistic", "XRange": [0, 25] }
          }
        ]
      },
      "LightningBolt": {
        "Type": "Ability",
        "Description": "Fire a lightning bolt at the target",
        "Ability": "Storm_Mage_LightningBolt",
        "Target": "Hostile",
        "AttackDistanceRange": [15, 15],
        "PostExecuteDistanceRange": [10, 12],
        "WeightCoefficient": 1.0,
        "Conditions": [
          {
            "Type": "TargetDistance",
            "Curve": { "ResponseCurve": "SimpleLogistic", "XRange": [0, 18] }
          },
          {
            "Type": "TimeSinceLastUsed",
            "Curve": { "ResponseCurve": "Linear", "XRange": [0, 2] }
          }
        ]
      },
      "LightningBarrage": {
        "Type": "Ability",
        "Description": "Rapid fire three lightning bolts",
        "Ability": "Storm_Mage_LightningBarrage",
        "Target": "Hostile",
        "AttackDistanceRange": [12, 12],
        "PostExecuteDistanceRange": [8, 10],
        "ChargeFor": 1.0,
        "WeightCoefficient": 1.3,
        "Conditions": [
          {
            "Type": "TargetDistance",
            "Curve": { "ResponseCurve": "SimpleLogistic", "XRange": [0, 15] }
          },
          {
            "Type": "TimeSinceLastUsed",
            "Curve": { "Type": "Switch", "SwitchPoint": 8 }
          },
          {
            "Type": "TargetStatPercent",
            "Stat": "Health",
            "Curve": "Linear"
          }
        ]
      },
      "Retreat": {
        "Type": "Ability",
        "Description": "Teleport away when target gets too close",
        "Ability": "Storm_Mage_Retreat",
        "Target": "Self",
        "WeightCoefficient": 1.4,
        "Conditions": [
          {
            "Type": "TargetDistance",
            "Curve": { "ResponseCurve": "SimpleDescendingLogistic", "XRange": [0, 6] }
          },
          {
            "Type": "TimeSinceLastUsed",
            "Curve": { "Type": "Switch", "SwitchPoint": 5 }
          }
        ]
      }
    },
    "ActionSets": {
      "Default": {
        "BasicAttacks": {
          "Attacks": ["Storm_Mage_LightningBolt"],
          "Randomise": false,
          "MaxRange": 15,
          "Timeout": 1.0,
          "CooldownRange": [1.5, 2.5]
        },
        "Actions": [
          "SelectTarget",
          "LightningBolt",
          "LightningBarrage",
          "Retreat"
        ]
      }
    }
  }
}
```

### Diseño de IA del Storm Mage

El Storm Mage es un lanzador a distancia que:
- **Prefiere el rango** — `PostExecuteDistanceRange` lo mantiene a 10-12 bloques de distancia después de atacar
- **Usa LightningBarrage** contra objetivos con alta salud (la condición `TargetStatPercent(Health, Linear)` puntúa más alto cuando el objetivo tiene mucha salud)
- **Se retira** cuando los jugadores se acercan a menos de 6 bloques (la logística descendente puntúa alto a corta distancia)
- **Huye** al 20% de salud (definido en el archivo de rol)

---

## Paso 7: Agregar Claves de Traducción

Agrega a `YourMod/Assets/Languages/en-US.lang`:

```
server.items.Weapon_Staff_Lightning.name=Lightning Staff
server.items.Weapon_Staff_Lightning.description=A crackling staff that channels lightning energy.
server.npcRoles.Storm_Mage.name=Storm Mage
server.effects.Lightning_Stun.name=Stunned
server.effects.Lightning_Shock.name=Shocked
```

---

## Paso 8: Probar el Sistema de Combate

1. Coloca tu carpeta de mod en el directorio de mods del servidor e inicia el servidor.
2. Obtén el Bastón de Rayo usando el generador de objetos de desarrollador.
3. Prueba el arma:

| Prueba | Resultado esperado |
|--------|-------------------|
| Disparar al terreno | El rayo impacta el terreno, se reproducen partículas de chispas y el sonido de fallo |
| Disparar a un NPC | El NPC recibe 45 de daño Lightning (números azules), se aturde durante 1.5s, se aplica retroceso |
| Verificar la resistencia del NPC | Resistencia del NPC agotada (StaminaLoss: true) |
| Verificar la durabilidad del equipamiento | El equipamiento del objetivo NO se daña (DurabilityLoss: false) |
| Disparar a un grupo de NPCs | El AoE daña entidades dentro de 3 bloques con 50% de reducción |

4. Genera un Storm Mage y prueba el combate con NPCs:

| Prueba | Resultado esperado |
|--------|-------------------|
| Acercarse al Storm Mage | Comienza a disparar rayos a 15 bloques de distancia |
| Correr al cuerpo a cuerpo | El Storm Mage usa la habilidad Retreat para teletransportarse lejos |
| Esperar la barrera | El Storm Mage carga durante 1s y luego dispara rayos rápidos |
| Dañar hasta el 20% de HP | El Storm Mage huye a velocidad 7 |

### Solución de Problemas

| Problema | Causa | Solución |
|----------|-------|----------|
| Los números de daño aparecen blancos | Tipo de daño no encontrado | Verifica que `Lightning.json` existe en `Entity/Damage/` y tiene `DamageTextColor` |
| El proyectil no hace daño | Clave de `BaseDamage` no coincide | Asegúrate de que la clave `BaseDamage` coincida con el nombre de archivo del tipo de daño: `"Lightning"` |
| El efecto de aturdimiento no se aplica | ID de efecto no coincide | Verifica que `EffectId` en la interacción coincida con el campo `Id` del archivo de efecto |
| Sin retroceso al impactar | Falta configuración de retroceso | Verifica que `DamageEffects.Knockback` tiene `Force` > 0 |
| El arma no es fabricable | ID del banco incorrecto | Verifica que `BenchRequirement.Id` coincida con un banco de fabricación existente |
| El NPC no usa rayos | CAE no referenciado | Asegúrate de que el rol del NPC referencia el archivo CAE en su cableado de plantilla |

---

## Listado Completo de Archivos

```
YourMod/
  Assets/
    Server/
      Entity/
        Damage/
          Lightning.json
        Effects/
          Effect_Lightning_Stun.json
          Effect_Lightning_Shock.json
      Projectiles/
        Spells/
          LightningBolt.json
      ProjectileConfigs/
        Weapons/
          Staff/
            Lightning/
              Projectile_Config_LightningBolt.json
      Item/
        Items/
          Weapon/
            Staff/
              Weapon_Staff_Lightning.json
      NPC/
        Roles/
          MyMod/
            Storm_Mage.json
        Balancing/
          Intelligent/
            CAE_Storm_Mage.json
    Languages/
      en-US.lang
```

---

## Próximos Pasos

- [NPC AI Behavior Trees](/hytale-modding-docs/tutorials/advanced/npc-ai-behavior-trees) — agrega IA compleja de múltiples estados al Storm Mage
- [Custom Dungeons](/hytale-modding-docs/tutorials/advanced/custom-dungeons) — usa el sistema de Rayos en encuentros de mazmorras
- [Damage Types](/hytale-modding-docs/reference/combat-and-projectiles/damage-types) — referencia completa de tipos de daño
- [Projectile Configs](/hytale-modding-docs/reference/combat-and-projectiles/projectile-configs) — esquema completo de configuración de proyectiles
- [Item Definitions](/hytale-modding-docs/reference/item-system/item-definitions) — referencia completa del esquema de objetos
