---
title: Efeitos de Câmera
description: Referência para definições de efeitos de câmera, tremor de câmera e balanço de visão no Hytale, que controlam tremores de tela em ataques, balanço de visão baseado em movimento e transições de ease-in/out.
---

## Visão Geral

Arquivos de efeitos de câmera controlam como a câmera responde a eventos de jogabilidade. O sistema possui três camadas: arquivos **CameraEffect** disparam um tremor de câmera nomeado com um valor de intensidade, arquivos **CameraShake** definem as curvas de oscilação reais para visões em primeira e terceira pessoa, e arquivos **ViewBobbing** produzem movimentos rítmicos da câmera durante estados de movimento. Juntos, eles adicionam feedback visceral a golpes de combate, passos e travessias.

## Localização dos Arquivos

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

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `Type` | `string` | Sim | — | Tipo de efeito. Atualmente `"CameraShake"` é o único tipo suportado. |
| `CameraShake` | `string` | Sim | — | ID da definição de tremor de câmera a ser reproduzida. Resolve para um arquivo em `CameraShake/`. |
| `Intensity` | `IntensityConfig` | Sim | — | Controla a intensidade do efeito. |

### IntensityConfig

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `Value` | `number` | Sim | — | Multiplicador de intensidade aplicado ao tremor. Valores típicos variam de `0.01` a `0.1`. |

### CameraShake

Arquivos de tremor de câmera definem o comportamento de oscilação separadamente para perspectivas em primeira e terceira pessoa.

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `FirstPerson` | `ShakeView` | Não | — | Configuração de tremor para câmera em primeira pessoa. |
| `ThirdPerson` | `ShakeView` | Não | — | Configuração de tremor para câmera em terceira pessoa. |

### ShakeView

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `Duration` | `number` | Não | `0` | Duração total em segundos. `0` significa que o tremor reproduz uma vez através de seus ciclos de oscilação. |
| `EaseIn` | `Ease` | Não | — | Transição de fade-in no início do tremor. |
| `EaseOut` | `Ease` | Não | — | Transição de fade-out no final do tremor. |
| `Offset` | `AxisOscillations` | Não | — | Oscilações de deslocamento posicional nos eixos X, Y, Z. |
| `Rotation` | `RotationOscillations` | Não | — | Oscilações rotacionais nos eixos Pitch, Yaw, Roll. |

### Ease

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `Time` | `number` | Sim | — | Duração da transição de ease em segundos. |
| `Type` | `string` | Sim | — | Função de easing: `"Linear"`, `"QuadInOut"`, `"QuadIn"`, `"QuadOut"`. |

### Oscillation

Cada eixo em `Offset` (X, Y, Z) ou `Rotation` (Pitch, Yaw, Roll) contém um array de entradas de oscilação:

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `Frequency` | `number` | Sim | — | Frequência de oscilação em Hz. Valores mais altos produzem tremores mais rápidos. |
| `Amplitude` | `number` | Sim | — | Deslocamento máximo ou rotação em unidades/graus. |
| `Type` | `string` | Sim | — | Função de onda: `"Sin"`, `"Cos"`, `"Perlin_Hermite"`. |
| `Clamp` | `ClampConfig` | Não | — | Limita a saída da oscilação a um intervalo. |

### ClampConfig

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `Min` | `number` | Não | — | Valor mínimo de limitação. |
| `Max` | `number` | Não | — | Valor máximo de limitação. |

### ViewBobbing

Arquivos de balanço de visão definem movimentos rítmicos da câmera vinculados a estados de movimento.

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `FirstPerson` | `BobView` | Não | — | Configuração de balanço de visão em primeira pessoa. |

### BobView

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `EaseIn` | `Ease` | Não | — | Transição para este estado de balanço. |
| `Offset` | `AxisOscillations` | Não | — | Oscilações posicionais (balanço da cabeça). |
| `Rotation` | `RotationOscillations` | Não | — | Oscilações rotacionais (inclinação da cabeça). |

## Exemplos

**Efeito de câmera** (`Assets/Server/Camera/CameraEffect/Battleaxe/Battleaxe_Sweep.json`):

```json
{
  "Type": "CameraShake",
  "CameraShake": "Battleaxe_Sweep",
  "Intensity": {
    "Value": 0.05
  }
}
```

**Tremor de câmera** (`Assets/Server/Camera/CameraShake/Battleaxe/Battleaxe_Sweep.json`, resumido):

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

**Balanço de visão** (`Assets/Server/Camera/ViewBobbing/Running.json`):

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

## Páginas Relacionadas

- [Configurações de Jogabilidade](/hytale-modding-docs/reference/game-configuration/gameplay-configs) — o campo `CameraEffects` referencia configurações de efeitos de câmera
- [Modelos de Servidor](/hytale-modding-docs/reference/models-and-visuals/server-models) — configuração de rastreamento de câmera de entidades
- [Partículas](/hytale-modding-docs/reference/models-and-visuals/particles) — efeitos visuais de partículas disparados junto com tremores de câmera
