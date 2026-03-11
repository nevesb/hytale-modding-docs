---
title: Conjuntos de animacion
description: Referencia para las definiciones de conjuntos de animacion incrustados en archivos de modelos del servidor en Hytale, cubriendo agrupacion de animaciones, velocidad de reproduccion, mezcla, bucles y disparadores de eventos de sonido.
---

## Descripcion general

Los conjuntos de animacion son grupos nombrados de clips de animacion definidos dentro de archivos de modelos del servidor. El motor utiliza estos conjuntos nombrados para reproducir la animacion correcta para un estado dado de la entidad (reposo, caminar, atacar, muerte, etc.). Cada conjunto contiene uno o mas objetos `AnimationEntry`; cuando existen multiples entradas, el motor selecciona una aleatoriamente, proporcionando variedad visual. Los conjuntos de animacion soportan escalado de velocidad de reproduccion, mezcla de transicion, control de bucle y disparadores de eventos de sonido por clip.

Los conjuntos de animacion se encuentran dentro del campo `AnimationSets` de una definicion de modelo del servidor. Esta pagina se enfoca en el esquema del conjunto de animacion en si. Para el formato completo del archivo de modelo, consulta [Modelos del servidor](/hytale-modding-docs/reference/models-and-visuals/server-models).

## Ubicacion de archivos

Los conjuntos de animacion estan incrustados en archivos JSON de modelos del servidor:

```
Assets/Server/Models/
  Beast/
    Bear_Grizzly.json      (contains AnimationSets)
    Bear_Polar.json
    Cactee.json
  Critter/
  Flying_Beast/
  Human/
    Player.json
    Mannequin.json
  Intelligent/
  Livestock/
  Pets/
  Projectiles/
```

## Esquema

### AnimationSet

| Campo | Tipo | Requerido | Predeterminado | Descripcion |
|-------|------|-----------|----------------|-------------|
| `Animations` | `AnimationEntry[]` | Si | — | Uno o mas clips de animacion en este conjunto. Cuando existen multiples entradas, el motor selecciona una aleatoriamente en cada reproduccion. |

### AnimationEntry

| Campo | Tipo | Requerido | Predeterminado | Descripcion |
|-------|------|-----------|----------------|-------------|
| `Animation` | `string` | Si | — | Ruta al archivo de animacion `.blockyanim`, relativa a la raiz de assets Common. |
| `Speed` | `number` | No | `1` | Multiplicador de velocidad de reproduccion. Valores menores a `1` ralentizan la animacion; valores mayores a `1` la aceleran. |
| `BlendingDuration` | `number` | No | `0` | Tiempo en segundos para hacer transicion gradual desde la animacion anterior a esta. Produce transiciones mas suaves a costa de una breve superposicion. |
| `Looping` | `boolean` | No | `true` | Si la animacion se repite continuamente. Establece `false` para animaciones de una sola vez como muerte o ataque. |
| `SoundEventId` | `string` | No | — | Evento de sonido disparado cada vez que esta animacion se reproduce o repite (por ejemplo, sonidos de pasos o rugidos). |

## Nombres estandar de conjuntos

El motor espera conjuntos nombrados especificos para los estados principales de la entidad. Se pueden agregar conjuntos personalizados para comportamiento con scripts o controlado por IA.

| Nombre | Proposito |
|--------|-----------|
| `Idle` | De pie, sin movimiento |
| `Walk` / `WalkBackward` | Caminando hacia adelante o hacia atras |
| `Run` | Corriendo / sprinting |
| `Crouch` / `CrouchWalk` / `CrouchWalkBackward` | Estados de movimiento agachado |
| `Jump` / `JumpWalk` / `JumpRun` | Variantes de salto segun velocidad de movimiento |
| `Fall` | Cayendo por el aire |
| `Swim` / `SwimIdle` / `SwimFast` / `SwimBackward` | Estados de natacion |
| `Fly` / `FlyIdle` / `FlyFast` / `FlyBackward` | Estados de vuelo |
| `Hurt` / `Death` | Reaccion al dano y muerte |
| `Alerted` | Animacion de activacion de agresion |
| `Sleep` / `Laydown` / `Wake` | Ciclo de descanso |
| `Spawn` | Animacion de aparicion de la entidad |
| `Roar` / `Search` / `Eat` | Animaciones ambientales decorativas |

## Ejemplo

**Multiples variantes de animacion con mezcla** (de `Assets/Server/Models/Human/Mannequin.json`):

```json
{
  "AnimationSets": {
    "Hurt": {
      "Animations": [
        {
          "Animation": "Characters/Animations/Damage/Default/Hurt.blockyanim",
          "BlendingDuration": 0.1,
          "Looping": false
        },
        {
          "Animation": "Characters/Animations/Damage/Default/Hurt2.blockyanim",
          "BlendingDuration": 0.1,
          "Looping": false
        }
      ]
    }
  }
}
```

**Clip individual con evento de sonido** (de `Assets/Server/Models/Beast/Bear_Grizzly.json`):

```json
{
  "AnimationSets": {
    "Run": {
      "Animations": [
        {
          "Animation": "NPC/Beast/Bear_Grizzly/Animations/Default/Run.blockyanim",
          "SoundEventId": "SFX_Bear_Grizzly_Run",
          "Speed": 1
        }
      ]
    },
    "Death": {
      "Animations": [
        {
          "Animation": "NPC/Beast/Bear_Grizzly/Animations/Damage/Death.blockyanim",
          "Looping": false,
          "SoundEventId": "SFX_Bear_Grizzly_Death"
        }
      ]
    }
  }
}
```

## Paginas relacionadas

- [Modelos del servidor](/hytale-modding-docs/reference/models-and-visuals/server-models) — formato completo del archivo de modelo que contiene conjuntos de animacion
- [Animaciones del cliente](/hytale-modding-docs/reference/models-and-visuals/client-animations) — formato de archivo `.blockyanim` referenciado por las entradas de animacion
- [Modelos del cliente](/hytale-modding-docs/reference/models-and-visuals/client-models) — formato de malla visual `.blockymodel`
