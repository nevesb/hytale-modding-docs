---
title: Conjuntos de Animação
description: Referência para definições de conjuntos de animação incorporados em arquivos de modelo de servidor no Hytale, cobrindo agrupamento de animações, velocidade de reprodução, mesclagem, loop e gatilhos de eventos sonoros.
---

## Visão Geral

Conjuntos de animação são grupos nomeados de clipes de animação definidos dentro de arquivos de modelo de servidor. O motor utiliza esses conjuntos nomeados para reproduzir a animação correta para um determinado estado da entidade (parado, andando, atacando, morrendo, etc.). Cada conjunto contém um ou mais objetos `AnimationEntry`; quando existem múltiplas entradas, o motor seleciona uma aleatoriamente, proporcionando variedade visual. Conjuntos de animação suportam escalonamento de velocidade de reprodução, mesclagem por crossfade, controle de loop e gatilhos de eventos sonoros por clipe.

Os conjuntos de animação ficam dentro do campo `AnimationSets` de uma definição de modelo de servidor. Esta página foca no esquema do conjunto de animação em si. Para o formato completo do arquivo de modelo, veja [Modelos de Servidor](/hytale-modding-docs/pt-br/reference/models-and-visuals/server-models).

## Localização dos Arquivos

Os conjuntos de animação são incorporados em arquivos JSON de modelo de servidor:

```
Assets/Server/Models/
  Beast/
    Bear_Grizzly.json      (contém AnimationSets)
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

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `Animations` | `AnimationEntry[]` | Sim | — | Um ou mais clipes de animação neste conjunto. Quando existem múltiplas entradas, o motor seleciona uma aleatoriamente a cada reprodução. |

### AnimationEntry

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `Animation` | `string` | Sim | — | Caminho para o arquivo de animação `.blockyanim`, relativo à raiz dos assets Common. |
| `Speed` | `number` | Não | `1` | Multiplicador de velocidade de reprodução. Valores abaixo de `1` desaceleram a animação; valores acima de `1` a aceleram. |
| `BlendingDuration` | `number` | Não | `0` | Tempo em segundos para fazer crossfade da animação anterior para esta. Produz transições mais suaves ao custo de uma breve sobreposição. |
| `Looping` | `boolean` | Não | `true` | Se a animação repete continuamente. Defina como `false` para animações de disparo único, como morte ou ataque. |
| `SoundEventId` | `string` | Não | — | Evento sonoro disparado cada vez que esta animação é reproduzida ou entra em loop (ex.: sons de passos ou rugidos). |

## Nomes Padrão de Conjuntos

O motor espera conjuntos nomeados específicos para os estados principais da entidade. Conjuntos personalizados podem ser adicionados para comportamentos controlados por script ou IA.

| Nome | Propósito |
|------|-----------|
| `Idle` | Parado, sem entrada |
| `Walk` / `WalkBackward` | Andando para frente ou para trás |
| `Run` | Correndo / sprintando |
| `Crouch` / `CrouchWalk` / `CrouchWalkBackward` | Estados de movimento agachado |
| `Jump` / `JumpWalk` / `JumpRun` | Variantes de pulo por velocidade de movimento |
| `Fall` | Caindo pelo ar |
| `Swim` / `SwimIdle` / `SwimFast` / `SwimBackward` | Estados de natação |
| `Fly` / `FlyIdle` / `FlyFast` / `FlyBackward` | Estados de voo |
| `Hurt` / `Death` | Reação a dano e morte |
| `Alerted` | Animação de alerta de agressão |
| `Sleep` / `Laydown` / `Wake` | Ciclo de descanso |
| `Spawn` | Animação de surgimento da entidade |
| `Roar` / `Search` / `Eat` | Animações ambientais de comportamento |

## Exemplo

**Múltiplas variantes de animação com mesclagem** (de `Assets/Server/Models/Human/Mannequin.json`):

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

**Clipe único com evento sonoro** (de `Assets/Server/Models/Beast/Bear_Grizzly.json`):

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

## Páginas Relacionadas

- [Modelos de Servidor](/hytale-modding-docs/pt-br/reference/models-and-visuals/server-models) — formato completo do arquivo de modelo que contém conjuntos de animação
- [Animações de Cliente](/hytale-modding-docs/pt-br/reference/models-and-visuals/client-animations) — formato de arquivo `.blockyanim` referenciado pelas entradas de animação
- [Modelos de Cliente](/hytale-modding-docs/pt-br/reference/models-and-visuals/client-models) — formato de malha visual `.blockymodel`
