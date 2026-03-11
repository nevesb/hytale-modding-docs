---
title: Modelos de Servidor
description: Referência para definições de modelos do lado do servidor no Hytale, cobrindo hitboxes, altura dos olhos, faixas de escala, conjuntos de animação, configuração de câmera e propriedades de ícone para NPCs e entidades.
---

## Visão Geral

Arquivos de modelo de servidor definem as propriedades físicas e comportamentais da representação visual de uma entidade no servidor: dimensões da hitbox, altura dos olhos, variação de escala, rastreamento de câmera direcionado a bones, e a biblioteca completa de conjuntos de animação nomeados usados pelos sistemas de IA e física. Eles são separados dos assets visuais exclusivos do cliente — o servidor precisa dos metadados de hitbox e animação para executar lógica de colisão, IA e som. Modelos suportam herança via campo `Parent`.

## Localização dos Arquivos

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

## Schema

### Nível superior

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Model` | `string` | Sim | — | Caminho para o arquivo `.blockymodel` que define a malha visual. |
| `Texture` | `string` | Não | — | Caminho para a textura padrão aplicada ao modelo. |
| `Parent` | `string` | Não | — | ID de uma definição de modelo pai para herdar campos não definidos. |
| `EyeHeight` | `number` | Sim | — | Altura em unidades dos pés da entidade até a posição dos olhos. Usado para posicionamento de câmera e linha de visão. |
| `CrouchOffset` | `number` | Não | `0` | Deslocamento vertical aplicado à posição dos olhos quando a entidade está agachada. |
| `HitBox` | `HitBox` | Sim | — | Caixa delimitadora alinhada aos eixos usada para colisão e detecção de acertos. |
| `MinScale` | `number` | Não | `1` | Escala aleatória mínima aplicada a esta entidade ao nascer. |
| `MaxScale` | `number` | Não | `1` | Escala aleatória máxima aplicada a esta entidade ao nascer. A escala é escolhida uniformemente entre min e max. |
| `DefaultAttachments` | `object[]` | Não | `[]` | Lista de anexos de itens presentes na entidade por padrão (ex: armas empunhadas). |
| `Camera` | `CameraConfig` | Não | — | Configuração de rastreamento de câmera direcionado a bones. |
| `AnimationSets` | `object` | Sim | — | Mapa de nome do conjunto de animação → `AnimationSet`. Veja abaixo. |
| `IconProperties` | `IconProperties` | Não | — | Parâmetros de câmera usados ao renderizar o ícone de inventário da entidade. |

### HitBox

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Min` | `Vector3` | Sim | — | Canto mínimo da AABB relativo à origem da entidade (pés). |
| `Max` | `Vector3` | Sim | — | Canto máximo da AABB relativo à origem da entidade. |

### Vector3

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `X` | `number` | Sim | — | Componente X. |
| `Y` | `number` | Sim | — | Componente Y (vertical). |
| `Z` | `number` | Sim | — | Componente Z. |

### CameraConfig

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Pitch` | `CameraAxis` | Não | — | Configuração de rastreamento de pitch. |
| `Yaw` | `CameraAxis` | Não | — | Configuração de rastreamento de yaw. |

### CameraAxis

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `AngleRange.Min` | `number` | Sim | — | Ângulo mínimo em graus que a câmera pode rastrear neste eixo. |
| `AngleRange.Max` | `number` | Sim | — | Ângulo máximo em graus que a câmera pode rastrear neste eixo. |
| `TargetNodes` | `string[]` | Sim | — | Nomes dos bones que a câmera mira ao rastrear. |

### AnimationSet

Um conjunto de animação é um grupo nomeado de um ou mais clipes de animação. O motor reproduz um clipe do grupo (aleatoriamente ou em sequência dependendo do contexto).

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Animations` | `AnimationEntry[]` | Sim | — | Um ou mais clipes de animação neste conjunto. |

### AnimationEntry

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Animation` | `string` | Sim | — | Caminho para o arquivo de animação `.blockyanim`. |
| `Speed` | `number` | Não | `1` | Multiplicador de velocidade de reprodução. |
| `BlendingDuration` | `number` | Não | `0` | Tempo em segundos para fazer blend da animação anterior para esta. |
| `Looping` | `boolean` | Não | `true` | Se a animação entra em loop. Defina como `false` para animações de disparo único. |
| `SoundEventId` | `string` | Não | — | Evento de som acionado quando esta animação é reproduzida (ex: sons de passos). |

### IconProperties

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Scale` | `number` | Não | — | Nível de zoom usado ao renderizar o ícone. |
| `Rotation` | `[number, number, number]` | Não | — | Rotação Euler `[X, Y, Z]` em graus aplicada ao modelo para renderização do ícone. |
| `Translation` | `[number, number]` | Não | — | Deslocamento 2D `[X, Y]` em pixels aplicado para centralizar o modelo no quadro do ícone. |

## Nomes Padrão de Conjuntos de Animação

O motor espera conjuntos nomeados específicos. Conjuntos personalizados podem ser adicionados para uso via script.

| Name | Purpose |
|------|---------|
| `Idle` | Parado |
| `Walk` / `WalkBackward` | Andando para frente/trás |
| `Run` | Correndo |
| `Crouch` / `CrouchWalk` / `CrouchWalkBackward` | Estados agachados |
| `Jump` / `JumpWalk` / `JumpRun` | Variantes de pulo |
| `Fall` | Caindo |
| `Swim` / `SwimIdle` / `SwimFast` / `SwimBackward` | Estados de natação |
| `Fly` / `FlyIdle` / `FlyFast` / `FlyBackward` | Estados de voo |
| `Hurt` / `Death` | Reações de dano |
| `Alerted` | Gatilho de aggro |
| `Sleep` / `Laydown` / `Wake` | Ciclo de descanso |
| `Spawn` | Animação de surgimento |
| `Roar` / `Search` / `Eat` | Animações ambientais |

## Exemplo

**Urso Pardo** (`Assets/Server/Models/Beast/Bear_Grizzly.json`, condensado):

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

**Manequim** (`Assets/Server/Models/Human/Mannequin.json`) — usa herança com `Parent`:

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

## Páginas Relacionadas

- [Sistema de NPCs](/hytale-modding-docs/reference/npc-system/) — definições de NPCs que referenciam IDs de modelos
- [Configs de Projéteis](/hytale-modding-docs/reference/combat-and-projectiles/projectile-configs) — campo `Model` referenciando IDs de modelos de projéteis
