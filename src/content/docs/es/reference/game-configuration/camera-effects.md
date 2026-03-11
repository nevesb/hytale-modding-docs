---
title: Efectos de Camara
description: Referencia de las definiciones de efectos de camara, sacudida de camara y balanceo de vision en Hytale, que controlan la sacudida de pantalla en ataques, el balanceo de vision impulsado por movimiento y transiciones de entrada/salida suave.
---

## Descripcion General

Los archivos de efectos de camara controlan como la camara responde a los eventos del juego. El sistema tiene tres capas: los archivos **CameraEffect** activan una sacudida de camara nombrada con un valor de intensidad, los archivos **CameraShake** definen las curvas de oscilacion reales para las vistas en primera y tercera persona, y los archivos **ViewBobbing** producen movimiento ritmico de la camara durante los estados de movimiento. Juntos agregan retroalimentacion visceral a golpes de combate, pisadas y desplazamiento.

## Ubicacion de Archivos

```
Assets/Server/Camera/
  CameraEffect/
    Battleaxe/
      Battleaxe_Bash.json
      Battleaxe_Sweep.json
      Battleaxe_Swing_Horizontal.json
      ...
    Block/
    Crossbow/
    Daggers/
    Greatsword/
    Longsword/
    Spear/
    Warhammer/
  CameraShake/
    Battleaxe/
      Battleaxe_Bash.json
      Battleaxe_Sweep.json
      ...
    Daggers/
    Greatsword/
    Longsword/
    Spear/
    Warhammer/
  ViewBobbing/
    Climbing.json
    Crouching.json
    Flying.json
    Idle.json
    Mounting.json
    None.json
    Running.json
    Sliding.json
    Sprinting.json
    SprintMounting.json
    Swimming.json
    Walking.json
```

## Esquema

### CameraEffect

| Campo | Tipo | Requerido | Por defecto | Descripcion |
|-------|------|-----------|-------------|-------------|
| `Type` | `string` | Si | — | Tipo de efecto. Actualmente `"CameraShake"` es el unico tipo soportado. |
| `CameraShake` | `string` | Si | — | ID de la definicion de sacudida de camara a reproducir. Se resuelve a un archivo en `CameraShake/`. |
| `Intensity` | `IntensityConfig` | Si | — | Controla la fuerza del efecto. |

### IntensityConfig

| Campo | Tipo | Requerido | Por defecto | Descripcion |
|-------|------|-----------|-------------|-------------|
| `Value` | `number` | Si | — | Multiplicador de intensidad aplicado a la sacudida. Los valores tipicos van de `0.01` a `0.1`. |

### CameraShake

Los archivos de sacudida de camara definen el comportamiento de oscilacion por separado para las perspectivas de primera y tercera persona.

| Campo | Tipo | Requerido | Por defecto | Descripcion |
|-------|------|-----------|-------------|-------------|
| `FirstPerson` | `ShakeView` | No | — | Configuracion de sacudida para la camara en primera persona. |
| `ThirdPerson` | `ShakeView` | No | — | Configuracion de sacudida para la camara en tercera persona. |

### ShakeView

| Campo | Tipo | Requerido | Por defecto | Descripcion |
|-------|------|-----------|-------------|-------------|
| `Duration` | `number` | No | `0` | Duracion total en segundos. `0` significa que la sacudida se reproduce una vez a traves de sus ciclos de oscilacion. |
| `EaseIn` | `Ease` | No | — | Transicion de entrada suave al inicio de la sacudida. |
| `EaseOut` | `Ease` | No | — | Transicion de salida suave al final de la sacudida. |
| `Offset` | `AxisOscillations` | No | — | Oscilaciones de desplazamiento posicional en los ejes X, Y, Z. |
| `Rotation` | `RotationOscillations` | No | — | Oscilaciones rotacionales en los ejes Pitch, Yaw, Roll. |

### Ease

| Campo | Tipo | Requerido | Por defecto | Descripcion |
|-------|------|-----------|-------------|-------------|
| `Time` | `number` | Si | — | Duracion de la transicion suave en segundos. |
| `Type` | `string` | Si | — | Funcion de suavizado: `"Linear"`, `"QuadInOut"`, `"QuadIn"`, `"QuadOut"`. |

### Oscillation

Cada eje en `Offset` (X, Y, Z) o `Rotation` (Pitch, Yaw, Roll) contiene un array de entradas de oscilacion:

| Campo | Tipo | Requerido | Por defecto | Descripcion |
|-------|------|-----------|-------------|-------------|
| `Frequency` | `number` | Si | — | Frecuencia de oscilacion en Hz. Valores mas altos producen sacudidas mas rapidas. |
| `Amplitude` | `number` | Si | — | Desplazamiento maximo o rotacion en unidades/grados. |
| `Type` | `string` | Si | — | Funcion de onda: `"Sin"`, `"Cos"`, `"Perlin_Hermite"`. |
| `Clamp` | `ClampConfig` | No | — | Limita la salida de la oscilacion a un rango. |

### ClampConfig

| Campo | Tipo | Requerido | Por defecto | Descripcion |
|-------|------|-----------|-------------|-------------|
| `Min` | `number` | No | — | Valor minimo de limitacion. |
| `Max` | `number` | No | — | Valor maximo de limitacion. |

### ViewBobbing

Los archivos de balanceo de vision definen el movimiento ritmico de la camara vinculado a estados de movimiento.

| Campo | Tipo | Requerido | Por defecto | Descripcion |
|-------|------|-----------|-------------|-------------|
| `FirstPerson` | `BobView` | No | — | Configuracion de balanceo de vision en primera persona. |

### BobView

| Campo | Tipo | Requerido | Por defecto | Descripcion |
|-------|------|-----------|-------------|-------------|
| `EaseIn` | `Ease` | No | — | Transicion hacia este estado de balanceo. |
| `Offset` | `AxisOscillations` | No | — | Oscilaciones posicionales (balanceo de cabeza). |
| `Rotation` | `RotationOscillations` | No | — | Oscilaciones rotacionales (inclinacion de cabeza). |

## Ejemplos

**Efecto de camara** (`Assets/Server/Camera/CameraEffect/Battleaxe/Battleaxe_Sweep.json`):

```json
{
  "Type": "CameraShake",
  "CameraShake": "Battleaxe_Sweep",
  "Intensity": {
    "Value": 0.05
  }
}
```

**Sacudida de camara** (`Assets/Server/Camera/CameraShake/Battleaxe/Battleaxe_Sweep.json`, condensado):

```json
{
  "FirstPerson": {
    "Duration": 0.0,
    "EaseIn":  { "Time": 0.25, "Type": "QuadInOut" },
    "EaseOut": { "Time": 0.5,  "Type": "QuadInOut" },
    "Offset": { "X": [], "Y": [], "Z": [] },
    "Rotation": {
      "Pitch": [],
      "Yaw": [
        { "Frequency": 30.0, "Amplitude": 0.4, "Type": "Sin" }
      ],
      "Roll": []
    }
  },
  "ThirdPerson": {
    "Duration": 0.0,
    "EaseIn":  { "Time": 0.25, "Type": "QuadInOut" },
    "EaseOut": { "Time": 0.5,  "Type": "QuadInOut" },
    "Rotation": {
      "Yaw": [
        { "Frequency": 30.0, "Amplitude": 0.2, "Type": "Sin" }
      ]
    }
  }
}
```

**Balanceo de vision** (`Assets/Server/Camera/ViewBobbing/Running.json`):

```json
{
  "FirstPerson": {
    "EaseIn": { "Time": 0.5, "Type": "Linear" },
    "Offset": {
      "X": [
        { "Type": "Sin", "Frequency": 11.0, "Amplitude": 0.02 }
      ],
      "Y": [
        { "Type": "Cos", "Frequency": 22.0, "Amplitude": 0.024, "Clamp": { "Min": -0.5 } },
        { "Type": "Perlin_Hermite", "Frequency": 22.0, "Amplitude": 0.005, "Clamp": { "Min": -0.5 } }
      ],
      "Z": []
    },
    "Rotation": {
      "Pitch": [
        { "Type": "Cos", "Frequency": 22.0, "Amplitude": 0.001 }
      ],
      "Roll": []
    }
  }
}
```

## Paginas Relacionadas

- [Configuraciones de Jugabilidad](/es/hytale-modding-docs/reference/game-configuration/gameplay-configs) — el campo `CameraEffects` referencia configuraciones de efectos de camara
- [Modelos del Servidor](/es/hytale-modding-docs/reference/models-and-visuals/server-models) — configuracion de seguimiento de camara de entidades
- [Particulas](/es/hytale-modding-docs/reference/models-and-visuals/particles) — efectos visuales de particulas activados junto con sacudidas de camara
