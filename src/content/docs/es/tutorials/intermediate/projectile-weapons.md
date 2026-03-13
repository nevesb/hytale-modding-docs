---
title: Armas de Proyectil
description: Tutorial paso a paso para agregar ataques de proyectil cargados a una espada usando elementos de daño personalizados, configs de proyectiles, consumo de munición y cadenas de interacción.
sidebar:
  order: 5
---

## Objetivo

Agregar **ataques de proyectil** a la Espada de Cristal del tutorial [Crear un Banco de Crafteo](/hytale-modding-docs/es/tutorials/intermediate/create-a-crafting-bench/). Crearás un elemento de daño personalizado, munición crafteable y dos ataques de proyectil: un **rayo cargado** que consume munición al embestir, y un **orbe especial** que se dispara cuando la SignatureEnergy está llena.

![Rayo de cristal disparándose desde la Espada de Cristal durante un ataque de embestida cargado](/hytale-modding-docs/images/tutorials/projectile-weapons/crystal-bolt-firing.png)

## Lo que Aprenderás

- Cómo las definiciones de `Projectile` y los archivos `ProjectileConfig` trabajan juntos
- Cómo las interacciones `Type: "Projectile"` disparan proyectiles desde armas
- Cómo `Type: "Charging"` crea ataques de mantener-para-cargar con una barra de progreso
- Cómo `Type: "ModifyInventory"` consume munición con un respaldo en caso de fallo
- Cómo `EntityStatsOnHit` genera SignatureEnergy a partir de impactos de proyectil
- Cómo `InteractionVars` sobrescribe el comportamiento vanilla de la espada sin reemplazar la cadena completa

## Requisitos Previos

- El mod del Yunque de Cristal de [Crear un Banco de Crafteo](/hytale-modding-docs/es/tutorials/intermediate/create-a-crafting-bench/)
- El mod del bloque Brillo de Cristal de [Crear un Bloque Personalizado](/hytale-modding-docs/es/tutorials/beginner/create-a-block/)
- El mod del Árbol Encantado de [Árboles y Semillas Personalizados](/hytale-modding-docs/es/tutorials/intermediate/custom-trees-and-saplings/)

**Repositorio del mod complementario:** [hytale-mods-custom-projectile](https://github.com/nevesb/hytale-mods-custom-projectile) (v2.0.0)

:::note[Este Tutorial Reemplaza Mods Anteriores]
El mod complementario de este tutorial incluye todo de los tutoriales [Crear un Objeto Personalizado](/hytale-modding-docs/es/tutorials/beginner/create-an-item/) y [Crear un Banco de Crafteo](/hytale-modding-docs/es/tutorials/intermediate/create-a-crafting-bench/). Solo necesitas instalar `hytale-mods-custom-projectile` — reemplaza tanto `CreateACustomWeapon` como `CreateACraftingBench`.
:::

---

## Descripción General del Sistema de Proyectiles

El sistema de proyectiles de Hytale tiene tres capas:

| Capa | Ubicación | Propósito |
|------|-----------|-----------|
| **Definición de Proyectil** | `Server/Projectiles/` | La entidad del proyectil: apariencia, física, hitbox, daño base |
| **Config de Proyectil** | `Server/ProjectileConfigs/` | Configuración de lanzamiento: fuerza, desplazamiento de aparición, sonidos y cadenas de interacción de impacto/fallo |
| **Interacción del Arma** | `Server/Item/Interactions/` | `Type: "Projectile"` con una referencia `Config` que dispara el proyectil |

El flujo es:

```
Jugador mantiene ataque → Interacción de carga (1s) → ModifyInventory (consumir munición)
  → Éxito: Animación de embestida + Proyectil se dispara desde la punta de la espada
  → Fallo (sin munición): Ataque de embestida normal
```

---

## Paso 1: Crear un Elemento de Daño Personalizado

Crea un nuevo tipo de daño para que los proyectiles de cristal inflijan su propio elemento de daño con un color distintivo.

```
Server/Entity/Damage/Crystal_Light.json
```

```json
{
  "Parent": "Elemental",
  "Inherits": "Elemental",
  "DamageTextColor": "#88ccff"
}
```

Los campos `Parent` e `Inherits` hacen que Crystal Light se comporte como otros daños elementales (afectado por resistencia elemental). El `DamageTextColor` controla el color del número de daño flotante — azul claro para coincidir con el tema de cristal.

Los elementos de daño vanilla como `Fire`, `Ice` y `Nature` siguen el mismo patrón. Puedes referenciar tu elemento personalizado por nombre (`"Crystal_Light"`) en cualquier objeto `BaseDamage`.

---

## Paso 2: Crear Definiciones de Proyectil

Las definiciones de proyectil describen la entidad física que viaja por el mundo. Crea dos: un rayo rápido para el ataque cargado y un orbe grande para el ataque especial.

### Rayo de Luz de Cristal

```
Server/Projectiles/Crystal_Light_Bolt.json
```

```json
{
  "Appearance": "Ice_Bolt",
  "Radius": 0.2,
  "Height": 0.2,
  "HorizontalCenterShot": 0.2,
  "VerticalCenterShot": 0.1,
  "DepthShot": 1.5,
  "PitchAdjustShot": true,
  "SticksVertically": false,
  "MuzzleVelocity": 55,
  "TerminalVelocity": 60,
  "Gravity": 2,
  "ImpactSlowdown": 0,
  "TimeToLive": 10,
  "Damage": 18,
  "DeadTimeMiss": 0,
  "DeathEffectsOnHit": true,
  "HitParticles": {
    "SystemId": "Impact_Ice"
  },
  "DeathParticles": {
    "SystemId": "Impact_Ice"
  },
  "HitSoundEventId": "SFX_Ice_Break",
  "DeathSoundEventId": "SFX_Ice_Break"
}
```

### Orbe de Luz de Cristal

```
Server/Projectiles/Crystal_Light_Orb.json
```

```json
{
  "Appearance": "Ice_Ball",
  "Radius": 2.5,
  "Height": 0.3,
  "HorizontalCenterShot": 0.2,
  "DepthShot": 1,
  "PitchAdjustShot": false,
  "SticksVertically": false,
  "MuzzleVelocity": 35,
  "TerminalVelocity": 45,
  "Gravity": 3,
  "Damage": 36,
  "DeathEffectsOnHit": true,
  "TimeToLive": 5,
  "DeadTimeMiss": 0,
  "ImpactSlowdown": 0,
  "VerticalCenterShot": 0,
  "HitParticles": {
    "SystemId": "Impact_Ice"
  },
  "DeathParticles": {
    "SystemId": "IceBall_Explosion"
  },
  "MissParticles": {
    "SystemId": "IceBall_Explosion"
  },
  "DeathSoundEventId": "SFX_Ice_Ball_Death"
}
```

### Diferencias Clave

| Propiedad | Rayo | Orbe |
|-----------|------|------|
| `Appearance` | `Ice_Bolt` (pequeño, tipo flecha) | `Ice_Ball` (esfera grande) |
| `MuzzleVelocity` | 55 (rápido) | 35 (más lento) |
| `Gravity` | 2 (trayectoria plana) | 3 (arco leve) |
| `Radius` | 0.2 (estrecho) | 2.5 (amplio con salpicadura) |
| `Damage` | 18 | 36 (doble) |

:::tip[Apariencias Vanilla]
Los valores de `Appearance` de proyectiles referencian modelos visuales integrados. Las opciones comunes incluyen `Ice_Bolt`, `Ice_Ball`, `Arrow_Crude`, `Arrow_FullCharge` y `Bomb`. Puedes encontrarlos navegando `Assets/Server/Projectiles/`.
:::

---

## Paso 3: Crear Configs de Proyectil

Los Configs de Proyectil conectan la interacción del arma con el proyectil. Definen la fuerza de lanzamiento, posición de aparición, sonidos y qué sucede al impactar o fallar.

### Config del Rayo

```
Server/ProjectileConfigs/HytaleModdingManual/Projectile_Config_Crystal_Light_Bolt.json
```

```json
{
  "Parent": "Projectile_Config_Arrow_Base",
  "Model": "Ice_Bolt",
  "Physics": {
    "Type": "Standard",
    "Gravity": 2,
    "TerminalVelocityAir": 60,
    "TerminalVelocityWater": 15,
    "RotationMode": "VelocityDamped",
    "Bounciness": 0.0,
    "SticksVertically": false
  },
  "LaunchForce": 55,
  "SpawnOffset": {
    "X": 0.3,
    "Y": -0.3,
    "Z": 1.5
  },
  "LaunchLocalSoundEventId": "SFX_Ice_Break",
  "LaunchWorldSoundEventId": "SFX_Ice_Break",
  "Interactions": {
    "ProjectileHit": {
      "Interactions": [
        "Crystal_Light_Bolt_Damage",
        "Common_Projectile_Despawn"
      ]
    },
    "ProjectileMiss": {
      "Interactions": [
        "Common_Projectile_Miss",
        "Common_Projectile_Despawn"
      ]
    }
  }
}
```

El `SpawnOffset` controla dónde aparece el proyectil relativo al jugador. `Z: 1.5` lo empuja hacia adelante hasta la punta de la espada. `Y: -0.3` lo baja desde la altura de la cabeza.

`Parent: "Projectile_Config_Arrow_Base"` hereda la física y rotación de aparición predeterminadas de flechas. Sobrescribimos `Physics`, `LaunchForce` y `SpawnOffset` para el comportamiento de nuestro rayo de cristal.

### Config del Orbe

```
Server/ProjectileConfigs/HytaleModdingManual/Projectile_Config_Crystal_Light_Orb.json
```

```json
{
  "Parent": "Projectile_Config_Arrow_Base",
  "Model": "Ice_Ball",
  "Physics": {
    "Type": "Standard",
    "Gravity": 3,
    "TerminalVelocityAir": 45,
    "TerminalVelocityWater": 10,
    "RotationMode": "VelocityDamped",
    "Bounciness": 0.0,
    "SticksVertically": false
  },
  "LaunchForce": 35,
  "LaunchLocalSoundEventId": "SFX_Ice_Ball_Death",
  "LaunchWorldSoundEventId": "SFX_Ice_Ball_Death",
  "Interactions": {
    "ProjectileHit": {
      "Interactions": [
        "Crystal_Light_Orb_Damage",
        "Common_Projectile_Despawn"
      ]
    },
    "ProjectileMiss": {
      "Interactions": [
        "Common_Projectile_Miss",
        "Common_Projectile_Despawn"
      ]
    }
  }
}
```

---

## Paso 4: Crear Interacciones de Daño

Las interacciones de daño definen qué sucede cuando un proyectil impacta una entidad. Especifican cantidades de daño, retroceso, partículas, sonidos y generación de estadísticas.

### Daño del Rayo

```
Server/Item/Interactions/HytaleModdingManual/Crystal_Light_Bolt_Damage.json
```

```json
{
  "Parent": "DamageEntityParent",
  "DamageCalculator": {
    "BaseDamage": {
      "Crystal_Light": 18
    }
  },
  "DamageEffects": {
    "Knockback": {
      "Type": "Force",
      "VelocityConfig": {
        "AirResistance": 0.97,
        "AirResistanceMax": 0.96,
        "GroundResistance": 0.94,
        "GroundResistanceMax": 0.3,
        "Threshold": 3.0,
        "Style": "Exp"
      },
      "Direction": {
        "X": 0.0,
        "Y": 1,
        "Z": -3
      },
      "Force": 8,
      "VelocityType": "Add"
    },
    "WorldParticles": [
      {
        "SystemId": "Impact_Ice",
        "Scale": 1
      }
    ],
    "WorldSoundEventId": "SFX_Ice_Break",
    "EntityStatsOnHit": [
      {
        "EntityStatId": "SignatureEnergy",
        "Amount": 5
      }
    ]
  }
}
```

### Daño del Orbe

```
Server/Item/Interactions/HytaleModdingManual/Crystal_Light_Orb_Damage.json
```

```json
{
  "Parent": "DamageEntityParent",
  "DamageCalculator": {
    "BaseDamage": {
      "Crystal_Light": 36
    }
  },
  "DamageEffects": {
    "Knockback": {
      "Type": "Force",
      "VelocityConfig": {
        "AirResistance": 0.97,
        "AirResistanceMax": 0.96,
        "GroundResistance": 0.94,
        "GroundResistanceMax": 0.3,
        "Threshold": 3.0,
        "Style": "Exp"
      },
      "Direction": {
        "X": 0.0,
        "Y": 3,
        "Z": -1
      },
      "Force": 20,
      "VelocityType": "Set"
    },
    "WorldParticles": [
      {
        "SystemId": "Impact_Ice",
        "Scale": 1
      },
      {
        "SystemId": "IceBall_Explosion",
        "Scale": 1
      }
    ],
    "WorldSoundEventId": "SFX_Ice_Ball_Death",
    "EntityStatsOnHit": [
      {
        "EntityStatId": "SignatureEnergy",
        "Amount": 10
      }
    ]
  }
}
```

### Generación de SignatureEnergy

El array `EntityStatsOnHit` es clave para el ciclo de progresión de la espada. Cada impacto de rayo otorga **+5** de SignatureEnergy, y cada impacto de orbe otorga **+10**. Cuando la SignatureEnergy alcanza el 100%, el ataque especial queda disponible. Esto crea un ciclo de juego: usa ataques cargados para acumular energía, y luego desata el poderoso orbe.

---

## Paso 5: Crear el Objeto de Munición

Las Cargas de Luz son la munición consumida por el ataque cargado. Se craftean en el Yunque de Cristal en lotes de 50.

```
Server/Item/Items/HytaleModdingManual/Weapon_Arrow_Crystal_Glow.json
```

```json
{
  "TranslationProperties": {
    "Name": "server.items.Weapon_Arrow_Crystal_Glow.name",
    "Description": "server.items.Weapon_Arrow_Crystal_Glow.description"
  },
  "Categories": [
    "Items.Weapons"
  ],
  "Quality": "Uncommon",
  "ItemLevel": 25,
  "PlayerAnimationsId": "Dagger",
  "Recipe": {
    "TimeSeconds": 5.0,
    "KnowledgeRequired": false,
    "Input": [
      {
        "ItemId": "Plant_Fruit_Enchanted",
        "Quantity": 1
      },
      {
        "ItemId": "Ore_Crystal_Glow",
        "Quantity": 1
      },
      {
        "ItemId": "Weapon_Arrow_Crude",
        "Quantity": 10
      }
    ],
    "OutputQuantity": 50,
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Categories": [
          "Crystal_Glow"
        ],
        "Id": "Armory_Crystal_Glow"
      }
    ]
  },
  "Model": "Items/Weapons/Arrow/Arrow.blockymodel",
  "Texture": "Items/Weapons/Arrow/Crude_Texture.png",
  "Icon": "Icons/ItemsGenerated/Weapon_Arrow_Crude.png",
  "MaxStack": 100,
  "Tags": {
    "Type": [
      "Weapon"
    ],
    "Family": [
      "Arrow"
    ]
  },
  "Weapon": {},
  "Light": {
    "Radius": 1,
    "Color": "#88ccff"
  },
  "ItemSoundSetId": "ISS_Weapons_Arrows"
}
```

![Interfaz del banco Yunque de Cristal mostrando la receta de Carga de Luz — 1 Fruta Encantada + 1 Brillo de Cristal + 10 Flechas Toscas = 50 Cargas de Luz](/hytale-modding-docs/images/tutorials/projectile-weapons/crystal-anvil-bench.png)

Puntos clave:
- `OutputQuantity: 50` produce 50 cargas por crafteo — importante para objetos de munición que se consumen rápidamente
- Sin `Interactions` ni `InteractionVars` — este objeto es solo munición, no un arma que puedas blandir
- El objeto vacío `Weapon: {}` es necesario para que el objeto aparezca en las categorías de armas
- `MaxStack: 100` permite llevar una cantidad razonable

---

## Paso 6: Crear las Interacciones de Disparo

Estas son interacciones simples de `Type: "Projectile"` que disparan cada proyectil. Deben ser **archivos nombrados**, no en línea — Hytale valida las interacciones por ID de asset y las interacciones de proyectil en línea pueden fallar la validación.

### Disparo del Rayo

```
Server/Item/Interactions/HytaleModdingManual/Crystal_Sword_Shoot_Bolt.json
```

```json
{
  "Type": "Projectile",
  "Config": "Projectile_Config_Crystal_Light_Bolt",
  "Next": {
    "Type": "Simple",
    "RunTime": 0.2
  }
}
```

### Disparo del Orbe

```
Server/Item/Interactions/HytaleModdingManual/Crystal_Sword_Shoot_Orb.json
```

```json
{
  "Type": "Projectile",
  "Config": "Projectile_Config_Crystal_Light_Orb",
  "Next": {
    "Type": "Simple",
    "RunTime": 0.2
  }
}
```

El campo `Config` referencia el ProjectileConfig por nombre de archivo (sin `.json`). El bloque `Next` agrega un breve tiempo de espera después de disparar.

:::caution[Se Requieren Archivos Nombrados]
Siempre crea las interacciones de proyectil como archivos nombrados separados. Poner en línea `Type: "Projectile"` dentro de un bloque Serial o Parallel puede causar errores de validación de assets como `Failed to validate asset: **TuInteraccion_Next_Interactions_0`.
:::

---

## Paso 7: Crear la Interacción de Carga

La interacción de carga requiere que el jugador mantenga presionado el botón de ataque durante 1 segundo antes de que se active el ataque cargado.

```
Server/Item/Interactions/HytaleModdingManual/Crystal_Sword_Charge.json
```

```json
{
  "Type": "Charging",
  "AllowIndefiniteHold": false,
  "DisplayProgress": true,
  "HorizontalSpeedMultiplier": 0.5,
  "Next": {
    "0": "Weapon_Sword_Primary_Thrust",
    "1.0": "Crystal_Sword_Charged_Entry"
  }
}
```

| Campo | Propósito |
|-------|-----------|
| `AllowIndefiniteHold` | `false` significa que se dispara automáticamente cuando se alcanza el umbral más alto |
| `DisplayProgress` | Muestra la barra de carga sobre la barra de acceso rápido |
| `HorizontalSpeedMultiplier` | Reduce la velocidad de movimiento mientras se carga (0.5 = mitad de velocidad) |
| `Next` | Mapea umbrales de carga (en segundos) a interacciones |

Los umbrales funcionan como "el más alto alcanzado":
- **Soltar antes de 1.0s** → ejecuta `"0"` → embestida vanilla normal (no se consume munición)
- **Mantener por 1.0s** → se dispara automáticamente `"1.0"` → entrada cargada con proyectil

---

## Paso 8: Crear la Entrada Cargada

Este es el núcleo del ataque cargado. Verifica la munición, la consume, reproduce la animación de embestida y dispara el rayo.

```
Server/Item/Interactions/HytaleModdingManual/Crystal_Sword_Charged_Entry.json
```

```json
{
  "Type": "ModifyInventory",
  "ItemToRemove": {
    "Id": "Weapon_Arrow_Crystal_Glow",
    "Quantity": 1
  },
  "AdjustHeldItemDurability": -0.3,
  "Next": {
    "Type": "Parallel",
    "Interactions": [
      {
        "Interactions": [
          "Weapon_Sword_Primary_Thrust"
        ]
      },
      {
        "Interactions": [
          {
            "Type": "Simple",
            "RunTime": 0.6
          },
          "Crystal_Sword_Shoot_Bolt"
        ]
      }
    ]
  },
  "Failed": "Weapon_Sword_Primary_Thrust"
}
```

### Cómo funciona

1. `ModifyInventory` verifica si el jugador tiene 1 `Weapon_Arrow_Crystal_Glow` en el inventario
2. **Si tiene** (`Next`): remueve la munición, reduce la durabilidad en 0.3, luego ejecuta un `Parallel`:
   - **Rama 1**: Reproduce la animación de embestida vanilla (`Weapon_Sword_Primary_Thrust`)
   - **Rama 2**: Espera 0.6 segundos (sincronizando el proyectil con el final de la animación de embestida), luego dispara el rayo
3. **Si no tiene munición** (`Failed`): realiza una embestida normal sin proyectil

El `Parallel` es esencial para la sincronización — permite que el proyectil se dispare en el momento exacto en que la animación de embestida alcanza la extensión completa (0.6s), en lugar de esperar a que toda la animación termine.

:::danger[Evitar Recursión de Replace Var]
Nunca uses `"Type": "Replace", "Var": "X"` dentro de una interacción que es en sí misma la sobrescritura para la variable X. Esto crea un bucle de recursión infinita donde la interacción sigue buscando su propia sobrescritura. Siempre referencia interacciones concretas directamente.
:::

---

## Paso 9: Crear el Ataque Especial

El ataque especial dispara un poderoso Orbe de Luz de Cristal cuando la SignatureEnergy alcanza el 100%.

### Interacción Raíz

```
Server/Item/RootInteractions/HytaleModdingManual/Crystal_Sword_Special.json
```

```json
{
  "Interactions": [
    "Crystal_Sword_Special"
  ]
}
```

### Interacción Especial

```
Server/Item/Interactions/HytaleModdingManual/Crystal_Sword_Special.json
```

```json
{
  "Type": "StatsCondition",
  "Costs": {
    "SignatureEnergy": 100
  },
  "ValueType": "Percent",
  "Next": {
    "Type": "Serial",
    "Interactions": [
      {
        "Type": "Parallel",
        "Interactions": [
          {
            "Interactions": [
              {
                "Type": "Simple",
                "RunTime": 0.4,
                "Effects": {
                  "ItemPlayerAnimationsId": "Sword",
                  "ItemAnimationId": "Thrust",
                  "ClearAnimationOnFinish": true,
                  "Particles": [
                    {
                      "SystemId": "IceBall",
                      "TargetNodeName": "Handle",
                      "PositionOffset": {
                        "X": 1.0,
                        "Y": 0,
                        "Z": 0
                      }
                    }
                  ]
                }
              }
            ]
          },
          {
            "Interactions": [
              "Crystal_Sword_Shoot_Orb"
            ]
          }
        ]
      },
      {
        "Type": "ChangeStat",
        "StatModifiers": {
          "SignatureEnergy": -100
        },
        "ValueType": "Percent"
      }
    ]
  }
}
```

El flujo:
1. `StatsCondition` verifica si la SignatureEnergy está al 100% — si no, no pasa nada
2. `Parallel` ejecuta la animación de embestida (con partículas de IceBall en la hoja) junto con el proyectil del orbe
3. `ChangeStat` drena toda la SignatureEnergy después del ataque

---

## Paso 10: Conectar Todo a la Espada

Actualiza `Weapon_Sword_Crystal_Glow.json` para conectar todos los nuevos sistemas. Los cambios clave están en `Interactions`, `InteractionVars` y `Weapon`:

```json {33-36,74-91,128-140}
{
  "Parent": "Template_Weapon_Sword",
  "Interactions": {
    "Primary": "Root_Weapon_Sword_Primary",
    "Secondary": "Root_Weapon_Sword_Secondary_Guard",
    "Ability1": "Crystal_Sword_Special"
  },
  "InteractionVars": {
    "Thrust_Damage": {
      "Interactions": [
        {
          "Parent": "Weapon_Sword_Primary_Thrust_Damage",
          "DamageCalculator": {
            "BaseDamage": {
              "Physical": 20,
              "Crystal_Light": 12
            }
          }
        }
      ]
    },
    "Thrust_Stamina": {
      "Interactions": [
        "Crystal_Sword_Charge"
      ]
    }
  },
  "Weapon": {
    "EntityStatsToClear": [
      "SignatureEnergy"
    ],
    "StatModifiers": {
      "SignatureEnergy": [
        {
          "Amount": 20,
          "CalculationType": "Additive"
        }
      ]
    }
  },
  "ItemAppearanceConditions": {
    "SignatureEnergy": [
      {
        "Condition": [100, 100],
        "ConditionValueType": "Percent",
        "Particles": [
          {
            "SystemId": "Sword_Signature_Ready",
            "TargetNodeName": "Handle",
            "PositionOffset": { "X": 0.8 },
            "TargetEntityPart": "PrimaryItem"
          }
        ]
      }
    ]
  }
}
```

### Qué hace cada sección

**`Interactions`** — Vincula los botones de ataque a cadenas de interacción:
- `Primary` usa el ataque primario vanilla de espada (`Root_Weapon_Sword_Primary`) — esto preserva el combo completo de golpes
- `Ability1` se vincula a nuestro ataque especial personalizado

**`InteractionVars`** — Sobrescribe partes específicas de la cadena vanilla sin reemplazarla:
- `Thrust_Damage` agrega daño Crystal_Light a la embestida
- `Thrust_Stamina` reemplaza la verificación de estamina con nuestra interacción de carga — así es como el ataque de proyectil cargado se integra en el combo existente de la espada

**`Weapon`** — Configura la SignatureEnergy:
- `StatModifiers` agrega 20 de SignatureEnergy máxima cuando está equipada
- `EntityStatsToClear` reinicia la energía cuando se desequipa el arma

**`ItemAppearanceConditions`** — Muestra partículas brillantes en la espada cuando la SignatureEnergy alcanza el 100%, señalando que el ataque especial está listo.

---

## Paso 11: Probar en el Juego

1. Copia la carpeta `CreateACraftingBench/` a `%APPDATA%/Hytale/UserData/Mods/`

2. Asegúrate de que los mods **CreateACustomBlock** y **CustomTreesAndSaplings** también estén instalados (dependencias requeridas)

3. Inicia Hytale y craftea Cargas de Luz en el Yunque de Cristal

4. Prueba el ataque cargado:
   - Equipa la Espada de Cristal con Cargas de Luz en tu inventario
   - Mantén presionado el ataque primario — la barra de carga debería aparecer
   - Suelta antes de 1s → embestida normal (no se consume munición)
   - Mantén por 1s → animación de embestida + rayo de cristal se dispara desde la punta de la espada

5. Prueba el ataque especial:
   - Golpea enemigos con rayos cargados para acumular SignatureEnergy (+5 por impacto de rayo)
   - Cuando la espada brille (100% de energía), presiona Habilidad1
   - Un gran Orbe de Luz de Cristal debería dispararse con un efecto de explosión

**Errores comunes y soluciones:**

| Error | Causa | Solución |
|-------|-------|----------|
| `Failed to validate asset` | Interacción `Type: "Projectile"` en línea | Extraer a un archivo nombrado |
| El proyectil sale de la cabeza | `SpawnOffset` no configurado | Agregar `SpawnOffset` con `Z: 1.5` para moverlo hacia adelante |
| Munición consumida sin proyectil | `RunTime` en un `Type: "Projectile"` | Usar `Next: { "Type": "Simple", "RunTime": 0.2 }` en su lugar |
| Disparo rápido infinito | `Replace Var` apuntando a su propia sobrescritura | Referenciar interacciones directamente, nunca auto-referenciar |
| Barra de carga no visible | `DisplayProgress` faltante | Establecer `"DisplayProgress": true` en la interacción Charging |
| El especial nunca se activa | Sin `EntityStatsOnHit` en el daño | Agregar `EntityStatsOnHit` con cantidad de `SignatureEnergy` a las interacciones de daño |

---

## Resumen de Estructura de Archivos

```
CreateACraftingBench/
  Server/
    Entity/Damage/
      Crystal_Light.json
    Projectiles/
      Crystal_Light_Bolt.json
      Crystal_Light_Orb.json
    ProjectileConfigs/HytaleModdingManual/
      Projectile_Config_Crystal_Light_Bolt.json
      Projectile_Config_Crystal_Light_Orb.json
    Item/
      Interactions/HytaleModdingManual/
        Crystal_Light_Bolt_Damage.json
        Crystal_Light_Orb_Damage.json
        Crystal_Sword_Charge.json
        Crystal_Sword_Charged_Entry.json
        Crystal_Sword_Shoot_Bolt.json
        Crystal_Sword_Shoot_Orb.json
        Crystal_Sword_Special.json
      RootInteractions/HytaleModdingManual/
        Crystal_Sword_Special.json
      Items/HytaleModdingManual/
        Weapon_Arrow_Crystal_Glow.json
        Weapon_Sword_Crystal_Glow.json (actualizado)
```

---

## Próximos Pasos

- [Tiendas de NPC y Comercio](/hytale-modding-docs/es/tutorials/intermediate/npc-shops-and-trading/) — vende Cargas de Luz en una tienda de mercader
- [Tablas de Botín Personalizadas](/hytale-modding-docs/es/tutorials/intermediate/custom-loot-tables/) — haz que los enemigos suelten Cargas de Luz
- [Referencia de Config de Proyectil](/hytale-modding-docs/es/reference/combat/projectile-configs/) — referencia completa del esquema para todos los campos de config de proyectil
