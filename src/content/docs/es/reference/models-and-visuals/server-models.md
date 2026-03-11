---
title: Modelos del servidor
description: Referencia para las definiciones de modelos del lado del servidor en Hytale, cubriendo hitboxes, altura de ojos, rangos de escala, conjuntos de animacion, configuracion de camara y propiedades de iconos para NPCs y entidades.
---

## Descripcion general

Los archivos de modelos del servidor definen las propiedades fisicas y de comportamiento de la representacion visual de una entidad en el servidor: dimensiones del hitbox, altura de ojos, variacion de escala, seguimiento de camara dirigido a huesos, y la biblioteca completa de conjuntos de animacion nombrados utilizados por los sistemas de IA y fisica. Son separados de los assets visuales solo del cliente — el servidor necesita metadatos de hitbox y animacion para ejecutar colision, IA y logica de sonido. Los modelos soportan herencia mediante un campo `Parent`.

## Ubicacion de archivos

```
Assets/Server/Models/
  Beast/
    Bear_Grizzly.json
    Bear_Polar.json
    Cactee.json
  Boss/
  Critter/
  Deployables/
  Elemental/
  Flying_Beast/
  Flying_Critter/
  Flying_Wildlife/
  Human/
    Mannequin.json
    Player.json
  Intelligent/
  Instances/
  Livestock/
  Pets/
  Projectiles/
```

## Esquema

### Nivel superior

| Campo | Tipo | Requerido | Predeterminado | Descripcion |
|-------|------|-----------|----------------|-------------|
| `Model` | `string` | Si | — | Ruta al archivo `.blockymodel` que define la malla visual. |
| `Texture` | `string` | No | — | Ruta a la textura predeterminada aplicada al modelo. |
| `Parent` | `string` | No | — | ID de una definicion de modelo padre de la cual heredar campos no establecidos. |
| `EyeHeight` | `number` | Si | — | Altura en unidades desde los pies de la entidad hasta la posicion de sus ojos. Utilizada para colocacion de camara y linea de vision. |
| `CrouchOffset` | `number` | No | `0` | Desplazamiento vertical aplicado a la posicion de los ojos cuando la entidad esta agachada. |
| `HitBox` | `HitBox` | Si | — | Caja delimitadora alineada con los ejes utilizada para colision y deteccion de impactos. |
| `MinScale` | `number` | No | `1` | Escala aleatoria minima aplicada a esta entidad al aparecer. |
| `MaxScale` | `number` | No | `1` | Escala aleatoria maxima aplicada a esta entidad al aparecer. La escala se elige uniformemente entre min y max. |
| `DefaultAttachments` | `object[]` | No | `[]` | Lista de accesorios de items presentes en la entidad por defecto (por ejemplo, armas sostenidas). |
| `Camera` | `CameraConfig` | No | — | Configuracion de seguimiento de camara dirigido a huesos. |
| `AnimationSets` | `object` | Si | — | Mapa de nombre de conjunto de animacion a `AnimationSet`. Ver abajo. |
| `IconProperties` | `IconProperties` | No | — | Parametros de camara utilizados al renderizar el icono de inventario de la entidad. |

### HitBox

| Campo | Tipo | Requerido | Predeterminado | Descripcion |
|-------|------|-----------|----------------|-------------|
| `Min` | `Vector3` | Si | — | Esquina minima del AABB relativa al origen de la entidad (pies). |
| `Max` | `Vector3` | Si | — | Esquina maxima del AABB relativa al origen de la entidad. |

### Vector3

| Campo | Tipo | Requerido | Predeterminado | Descripcion |
|-------|------|-----------|----------------|-------------|
| `X` | `number` | Si | — | Componente X. |
| `Y` | `number` | Si | — | Componente Y (vertical). |
| `Z` | `number` | Si | — | Componente Z. |

### CameraConfig

| Campo | Tipo | Requerido | Predeterminado | Descripcion |
|-------|------|-----------|----------------|-------------|
| `Pitch` | `CameraAxis` | No | — | Configuracion de seguimiento de cabeceo. |
| `Yaw` | `CameraAxis` | No | — | Configuracion de seguimiento de guiñada. |

### CameraAxis

| Campo | Tipo | Requerido | Predeterminado | Descripcion |
|-------|------|-----------|----------------|-------------|
| `AngleRange.Min` | `number` | Si | — | Angulo minimo en grados que la camara puede seguir en este eje. |
| `AngleRange.Max` | `number` | Si | — | Angulo maximo en grados que la camara puede seguir en este eje. |
| `TargetNodes` | `string[]` | Si | — | Nombres de huesos a los que apunta la camara al hacer seguimiento. |

### AnimationSet

Un conjunto de animacion es un grupo nombrado de uno o mas clips de animacion. El motor reproduce un clip del grupo (aleatoriamente o en secuencia dependiendo del contexto).

| Campo | Tipo | Requerido | Predeterminado | Descripcion |
|-------|------|-----------|----------------|-------------|
| `Animations` | `AnimationEntry[]` | Si | — | Uno o mas clips de animacion en este conjunto. |

### AnimationEntry

| Campo | Tipo | Requerido | Predeterminado | Descripcion |
|-------|------|-----------|----------------|-------------|
| `Animation` | `string` | Si | — | Ruta al archivo de animacion `.blockyanim`. |
| `Speed` | `number` | No | `1` | Multiplicador de velocidad de reproduccion. |
| `BlendingDuration` | `number` | No | `0` | Tiempo en segundos para hacer transicion desde la animacion anterior a esta. |
| `Looping` | `boolean` | No | `true` | Si la animacion se repite. Establecer `false` para animaciones de una sola vez. |
| `SoundEventId` | `string` | No | — | Evento de sonido disparado cuando esta animacion se reproduce (por ejemplo, sonidos de pasos). |

### IconProperties

| Campo | Tipo | Requerido | Predeterminado | Descripcion |
|-------|------|-----------|----------------|-------------|
| `Scale` | `number` | No | — | Nivel de zoom utilizado al renderizar el icono. |
| `Rotation` | `[number, number, number]` | No | — | Rotacion Euler `[X, Y, Z]` en grados aplicada al modelo para el renderizado del icono. |
| `Translation` | `[number, number]` | No | — | Desplazamiento 2D `[X, Y]` en pixeles aplicado para centrar el modelo en el marco del icono. |

## Nombres estandar de conjuntos de animacion

El motor espera conjuntos nombrados especificos. Se pueden agregar conjuntos personalizados para uso con scripts.

| Nombre | Proposito |
|--------|-----------|
| `Idle` | De pie |
| `Walk` / `WalkBackward` | Caminando hacia adelante/atras |
| `Run` | Corriendo |
| `Crouch` / `CrouchWalk` / `CrouchWalkBackward` | Estados agachados |
| `Jump` / `JumpWalk` / `JumpRun` | Variantes de salto |
| `Fall` | Cayendo |
| `Swim` / `SwimIdle` / `SwimFast` / `SwimBackward` | Estados de natacion |
| `Fly` / `FlyIdle` / `FlyFast` / `FlyBackward` | Estados de vuelo |
| `Hurt` / `Death` | Reacciones al dano |
| `Alerted` | Activacion de agresion |
| `Sleep` / `Laydown` / `Wake` | Ciclo de descanso |
| `Spawn` | Animacion de aparicion |
| `Roar` / `Search` / `Eat` | Animaciones decorativas |

## Ejemplo

**Oso Grizzly** (`Assets/Server/Models/Beast/Bear_Grizzly.json`, condensado):

```json
{
  "Model": "NPC/Beast/Bear_Grizzly/Models/Model.blockymodel",
  "Texture": "NPC/Beast/Bear_Grizzly/Models/Texture.png",
  "EyeHeight": 1.5,
  "CrouchOffset": -0.3,
  "HitBox": {
    "Max": { "X":  0.8, "Y": 1.8, "Z":  0.8 },
    "Min": { "X": -0.8, "Y": 0.0, "Z": -0.8 }
  },
  "MinScale": 0.9,
  "MaxScale": 1.25,
  "DefaultAttachments": [],
  "Camera": {
    "Pitch": {
      "AngleRange": { "Max": 45, "Min": -45 },
      "TargetNodes": ["Head"]
    },
    "Yaw": {
      "AngleRange": { "Max": 45, "Min": -45 },
      "TargetNodes": ["Head"]
    }
  },
  "AnimationSets": {
    "Idle": {
      "Animations": [
        { "Animation": "NPC/Beast/Bear_Grizzly/Animations/Default/Idle.blockyanim", "Speed": 0.6 }
      ]
    },
    "Run": {
      "Animations": [
        { "Animation": "NPC/Beast/Bear_Grizzly/Animations/Default/Run.blockyanim", "SoundEventId": "SFX_Bear_Grizzly_Run", "Speed": 1 }
      ]
    },
    "Death": {
      "Animations": [
        { "Animation": "NPC/Beast/Bear_Grizzly/Animations/Damage/Death.blockyanim", "Looping": false, "SoundEventId": "SFX_Bear_Grizzly_Death" }
      ]
    }
  }
}
```

**Maniqui** (`Assets/Server/Models/Human/Mannequin.json`) — usa herencia con `Parent`:

```json
{
  "Model": "NPC/MISC/Mannequin/Models/Model.blockymodel",
  "Texture": "NPC/MISC/Mannequin/Models/Model_Default.png",
  "EyeHeight": 1.6,
  "HitBox": {
    "Max": { "X":  0.3, "Y": 1.8, "Z":  0.3 },
    "Min": { "X": -0.3, "Y": 0.0, "Z": -0.3 }
  },
  "MinScale": 1,
  "MaxScale": 1,
  "Parent": "Player",
  "DefaultAttachments": [],
  "AnimationSets": {
    "Hurt": {
      "Animations": [
        { "Animation": "Characters/Animations/Damage/Default/Hurt.blockyanim",  "BlendingDuration": 0.1, "Looping": false },
        { "Animation": "Characters/Animations/Damage/Default/Hurt2.blockyanim", "BlendingDuration": 0.1, "Looping": false }
      ]
    }
  }
}
```

## Paginas relacionadas

- [Sistema de NPC](/hytale-modding-docs/reference/npc-system/) — definiciones de NPC que referencian IDs de modelos
- [Configuraciones de proyectiles](/hytale-modding-docs/reference/combat-and-projectiles/projectile-configs) — campo `Model` que referencia IDs de modelos de proyectiles
