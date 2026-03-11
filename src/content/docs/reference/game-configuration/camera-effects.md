---
title: Camera Effects
description: Reference for camera effect, camera shake, and view bobbing definitions in Hytale, which control screen shake on attacks, movement-driven view bob, and ease-in/out transitions.
---

## Overview

Camera effect files control how the camera responds to gameplay events. The system has three layers: **CameraEffect** files trigger a named camera shake with an intensity value, **CameraShake** files define the actual oscillation curves for first-person and third-person views, and **ViewBobbing** files produce rhythmic camera motion during movement states. Together they add visceral feedback to combat strikes, footsteps, and traversal.

## File Location

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

## Schema

### CameraEffect

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Type` | `string` | Yes | — | Effect type. Currently `"CameraShake"` is the only supported type. |
| `CameraShake` | `string` | Yes | — | ID of the camera shake definition to play. Resolves to a file in `CameraShake/`. |
| `Intensity` | `IntensityConfig` | Yes | — | Controls the strength of the effect. |

### IntensityConfig

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Value` | `number` | Yes | — | Intensity multiplier applied to the shake. Typical values range from `0.01` to `0.1`. |

### CameraShake

Camera shake files define oscillation behaviour separately for first-person and third-person perspectives.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `FirstPerson` | `ShakeView` | No | — | Shake configuration for first-person camera. |
| `ThirdPerson` | `ShakeView` | No | — | Shake configuration for third-person camera. |

### ShakeView

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Duration` | `number` | No | `0` | Total duration in seconds. `0` means the shake plays once through its oscillation cycles. |
| `EaseIn` | `Ease` | No | — | Fade-in transition at the start of the shake. |
| `EaseOut` | `Ease` | No | — | Fade-out transition at the end of the shake. |
| `Offset` | `AxisOscillations` | No | — | Positional offset oscillations on X, Y, Z axes. |
| `Rotation` | `RotationOscillations` | No | — | Rotational oscillations on Pitch, Yaw, Roll axes. |

### Ease

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Time` | `number` | Yes | — | Duration of the ease transition in seconds. |
| `Type` | `string` | Yes | — | Easing function: `"Linear"`, `"QuadInOut"`, `"QuadIn"`, `"QuadOut"`. |

### Oscillation

Each axis in `Offset` (X, Y, Z) or `Rotation` (Pitch, Yaw, Roll) contains an array of oscillation entries:

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Frequency` | `number` | Yes | — | Oscillation frequency in Hz. Higher values produce faster shaking. |
| `Amplitude` | `number` | Yes | — | Maximum displacement or rotation in units/degrees. |
| `Type` | `string` | Yes | — | Wave function: `"Sin"`, `"Cos"`, `"Perlin_Hermite"`. |
| `Clamp` | `ClampConfig` | No | — | Clamps the oscillation output to a range. |

### ClampConfig

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Min` | `number` | No | — | Minimum clamp value. |
| `Max` | `number` | No | — | Maximum clamp value. |

### ViewBobbing

View bobbing files define rhythmic camera motion tied to movement states.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `FirstPerson` | `BobView` | No | — | First-person view bobbing configuration. |

### BobView

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `EaseIn` | `Ease` | No | — | Transition into this bobbing state. |
| `Offset` | `AxisOscillations` | No | — | Positional oscillations (head bob). |
| `Rotation` | `RotationOscillations` | No | — | Rotational oscillations (head tilt). |

## Examples

**Camera effect** (`Assets/Server/Camera/CameraEffect/Battleaxe/Battleaxe_Sweep.json`):

```json
{
  "Type": "CameraShake",
  "CameraShake": "Battleaxe_Sweep",
  "Intensity": {
    "Value": 0.05
  }
}
```

**Camera shake** (`Assets/Server/Camera/CameraShake/Battleaxe/Battleaxe_Sweep.json`, condensed):

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

**View bobbing** (`Assets/Server/Camera/ViewBobbing/Running.json`):

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

## Related Pages

- [Gameplay Configs](/hytale-modding-docs/reference/game-configuration/gameplay-configs) — `CameraEffects` field references camera effect configurations
- [Server Models](/hytale-modding-docs/reference/models-and-visuals/server-models) — entity camera tracking configuration
- [Particles](/hytale-modding-docs/reference/models-and-visuals/particles) — visual particle effects triggered alongside camera shakes
