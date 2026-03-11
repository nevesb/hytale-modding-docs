---
title: Configuraciones de Proyectiles
description: Referencia de los archivos de configuracion de proyectiles en Hytale, definiendo fisica de lanzamiento, desplazamientos de generacion y cadenas de interaccion para proyectiles disparados por armas.
---

## Descripcion General

Los archivos de configuracion de proyectiles definen como un arma lanza un proyectil: el modelo utilizado, los parametros de fisica, la posicion de generacion y lo que sucede cuando el proyectil impacta, falla o rebota. Actuan como puente entre la accion de ataque de un arma y la entidad de proyectil en tiempo de ejecucion. Las configuraciones soportan herencia a traves de un campo `Parent`, permitiendo que las configuraciones base compartidas sean anuladas por arma.

## Ubicacion de Archivos

```
Assets/Server/ProjectileConfigs/
  Weapons/
    Arrows/
    Bows/
    Crossbow/
    Shortbow/
    Staff/
    Throwables/
    ...
  NPCs/
  _Debug/
```

## Esquema

| Campo | Tipo | Requerido | Por defecto | Descripcion |
|-------|------|-----------|-------------|-------------|
| `Parent` | `string` | No | — | ID de otra configuracion de proyectil de la cual heredar campos. Los campos hijos anulan los campos del padre. |
| `Model` | `string` | No | — | ID del modelo visual usado para el proyectil (por ejemplo, `"Arrow_Crude"`, `"Ice_Ball"`). |
| `Physics` | `PhysicsConfig` | No | — | Parametros de simulacion de fisica. Ver abajo. |
| `LaunchForce` | `number` | No | — | Fuerza escalar aplicada al lanzamiento, escalada por el nivel de carga cuando aplique. |
| `LaunchLocalSoundEventId` | `string` | No | — | Evento de sonido reproducido localmente para el tirador al lanzar. |
| `LaunchWorldSoundEventId` | `string` | No | — | Evento de sonido reproducido en el mundo (audible para jugadores cercanos) al lanzar. |
| `SpawnOffset` | `Vector3` | No | — | Desplazamiento en espacio local (X/Y/Z) desde el origen del arma donde se genera el proyectil. |
| `SpawnRotationOffset` | `RotationOffset` | No | — | Rotacion adicional aplicada al proyectil al generarse. |
| `Interactions` | `InteractionMap` | No | — | Eventos de interaccion nombrados y sus listas de acciones encadenadas. Ver abajo. |

### PhysicsConfig

| Campo | Tipo | Requerido | Por defecto | Descripcion |
|-------|------|-----------|-------------|-------------|
| `Type` | `"Standard"` | No | `"Standard"` | Modelo de simulacion de fisica. Actualmente solo se usa `"Standard"`. |
| `Gravity` | `number` | No | — | Aceleracion gravitacional aplicada por segundo. |
| `TerminalVelocityAir` | `number` | No | — | Velocidad maxima en el aire. |
| `TerminalVelocityWater` | `number` | No | — | Velocidad maxima en el agua. |
| `RotationMode` | `"VelocityDamped" \| "Fixed"` | No | — | Controla como la orientacion del proyectil sigue su vector de velocidad. |
| `Bounciness` | `number` | No | `0` | Fraccion de velocidad retenida despues de un rebote en superficie. |
| `BounceCount` | `number` | No | — | Numero de veces que el proyectil puede rebotar antes de detenerse. |
| `BounceLimit` | `number` | No | — | Numero maximo de rebotes permitidos. |
| `AllowRolling` | `boolean` | No | `false` | Si el proyectil puede rodar sobre superficies despues de rebotar. |
| `SticksVertically` | `boolean` | No | `false` | Si el proyectil se incrusta verticalmente en superficies al impactar. |

### Vector3

| Campo | Tipo | Requerido | Por defecto | Descripcion |
|-------|------|-----------|-------------|-------------|
| `X` | `number` | Si | — | Desplazamiento lateral. |
| `Y` | `number` | Si | — | Desplazamiento vertical. |
| `Z` | `number` | Si | — | Desplazamiento frontal. |

### RotationOffset

| Campo | Tipo | Requerido | Por defecto | Descripcion |
|-------|------|-----------|-------------|-------------|
| `Pitch` | `number` | No | `0` | Desplazamiento de inclinacion en grados. |
| `Yaw` | `number` | No | `0` | Desplazamiento de giro en grados. |
| `Roll` | `number` | No | `0` | Desplazamiento de alabeo en grados. |

### InteractionMap

El objeto `Interactions` mapea nombres de eventos a objetos `InteractionHandler`. Claves de evento soportadas:

| Clave | Cuando se dispara |
|-------|-------------------|
| `ProjectileSpawn` | Inmediatamente cuando se crea el proyectil. |
| `ProjectileHit` | Cuando el proyectil impacta a una entidad. |
| `ProjectileMiss` | Cuando el proyectil impacta el terreno o expira. |
| `ProjectileBounce` | Cuando el proyectil rebota en una superficie. |

### InteractionHandler

| Campo | Tipo | Requerido | Por defecto | Descripcion |
|-------|------|-----------|-------------|-------------|
| `Cooldown` | `object` | No | — | Enfriamiento opcional que controla este manejador. |
| `Interactions` | `string[] \| object[]` | Si | — | Lista ordenada de IDs de interaccion nombrados o definiciones de interaccion en linea para ejecutar. |

## Ejemplos

**Configuracion base de flecha** (`Assets/Server/ProjectileConfigs/Weapons/Arrows/Projectile_Config_Arrow_Base.json`):

```json
{
  "Model": "Arrow_Crude",
  "SpawnRotationOffset": {
    "Pitch": 2,
    "Yaw": 0.25,
    "Roll": 0
  },
  "Physics": {
    "Type": "Standard",
    "Gravity": 15,
    "TerminalVelocityAir": 50,
    "TerminalVelocityWater": 15,
    "RotationMode": "VelocityDamped",
    "Bounciness": 0.0,
    "SticksVertically": true
  },
  "LaunchForce": 30,
  "SpawnOffset": {
    "X": 0.15,
    "Y": -0.25,
    "Z": 0
  }
}
```

**Flecha de arco a dos manos** (`Projectile_Config_Arrow_Two_Handed_Bow.json`) — hereda de la base y agrega interacciones:

```json
{
  "Parent": "Projectile_Config_Arrow_Base",
  "LaunchLocalSoundEventId": "SFX_Bow_T2_Shoot",
  "LaunchWorldSoundEventId": "SFX_Bow_T2_Shoot",
  "LaunchForce": 5,
  "Interactions": {
    "ProjectileHit": {
      "Interactions": [
        "Bow_Two_Handed_Projectile_Damage",
        "Bow_Two_Handed_Projectile_Damage_End"
      ]
    },
    "ProjectileMiss": {
      "Interactions": [
        "Bow_Two_Handed_Projectile_Miss",
        "Bow_Two_Handed_Projectile_Miss_End"
      ]
    }
  }
}
```

**Configuracion de bola de hielo de baston** (`Assets/Server/ProjectileConfigs/Weapons/Staff/Ice/Projectile_Config_Ice_Ball.json`):

```json
{
  "Model": "Ice_Ball",
  "LaunchForce": 30,
  "Physics": {
    "Type": "Standard",
    "Gravity": 4.4,
    "TerminalVelocityAir": 42.5,
    "TerminalVelocityWater": 15,
    "RotationMode": "VelocityDamped",
    "Bounciness": 0.0,
    "SticksVertically": true
  },
  "LaunchWorldSoundEventId": "SFX_Staff_Ice_Shoot",
  "Interactions": {
    "ProjectileHit": {
      "Interactions": [
        {
          "Parent": "DamageEntityParent",
          "DamageCalculator": {
            "Class": "Charged",
            "BaseDamage": { "Ice": 20 }
          },
          "DamageEffects": {
            "Knockback": {
              "Type": "Force",
              "Force": 20,
              "VelocityType": "Set"
            },
            "WorldParticles": [
              { "SystemId": "Impact_Ice" },
              { "SystemId": "IceBall_Explosion" }
            ],
            "WorldSoundEventId": "SFX_Ice_Ball_Death"
          }
        },
        { "Type": "RemoveEntity", "Entity": "User" }
      ]
    },
    "ProjectileMiss": {
      "Interactions": [
        {
          "Type": "Simple",
          "Effects": {
            "WorldSoundEventId": "SFX_Ice_Ball_Death",
            "WorldParticles": [
              { "SystemId": "IceBall_Explosion" }
            ]
          }
        },
        { "Type": "RemoveEntity", "Entity": "User" }
      ]
    }
  }
}
```

## Paginas Relacionadas

- [Proyectiles](/es/hytale-modding-docs/reference/combat-and-projectiles/projectiles) — fisica de proyectiles y valores de dano
- [Tipos de Dano](/es/hytale-modding-docs/reference/combat-and-projectiles/damage-types) — jerarquia de tipos de dano usada en `BaseDamage`
