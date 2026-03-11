---
title: Interações de Itens
description: Referência para arquivos JSON de cadeias de interação de itens no Hytale, cobrindo tipos de interação, condições, calculadores de dano e encadeamento com Next.
---

## Visão Geral

Interações de itens definem como os itens se comportam quando usados — ataques, colocação de blocos, consumo, uso de ferramentas, esquivas e mais. Cada interação é um objeto JSON com um `Type` e um campo opcional `Next` que encadeia para a próxima etapa. Isso cria pipelines que podem ramificar em condições, causar dano, aplicar efeitos, reproduzir sons e gerar partículas. Arquivos de interação são referenciados por ID a partir das definições de itens pelos campos `Interactions` e `InteractionVars`.

## Localização dos Arquivos

```
Assets/Server/Item/Interactions/<Category>/<InteractionId>.json
```

Interações de nível superior e raiz:
```
Assets/Server/Item/Interactions/Block_Primary.json
Assets/Server/Item/Interactions/Block_Secondary.json
Assets/Server/Item/Interactions/Dodge.json
Assets/Server/Item/Interactions/Stamina_Bar_Flash.json
Assets/Server/Item/RootInteractions/            — Pontos de entrada de interação raiz
```

Subcategorias:
```
Interactions/Consumables/   — Condições de consumo de comida e poção
Interactions/Weapons/       — Cadeias de ataque de armas (Machado, Arco, Clava, etc.)
Interactions/Weapons/Common/Melee/  — Dano e seletor de melee compartilhados
Interactions/Tools/         — Interações específicas de ferramentas
Interactions/Block/         — Interações de quebra/ataque de blocos
Interactions/Dodge/         — Interações de esquiva
Interactions/NPCs/          — Interações acionadas por NPCs
Interactions/Stat_Check/    — Condições de verificação de stats
```

## Schema

### Campos Principais de Interação

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `Type` | string | Não | `"Simple"` | Tipo de interação. Veja a lista de tipos abaixo. |
| `Next` | string ou object | Não | — | A próxima interação a executar em caso de sucesso. Pode ser um ID de interação (string) ou um objeto de interação inline. |
| `Failed` | string ou object | Não | — | A interação a executar quando esta falha (usado por `Condition`, `UseBlock`, `PlaceBlock`, etc.). |
| `RunTime` | number | Não | — | Duração em segundos que esta interação ocupa na linha do tempo da cadeia. |
| `Effects` | object | Não | — | Efeitos aplicados quando esta interação é executada com sucesso. Veja os campos de Effects abaixo. |
| `Parent` | string | Não | — | Herda campos da interação nomeada (herança de template). |

### Tipos de Interação

| Tipo | Descrição |
|------|-----------|
| `Simple` | Executa imediatamente sem lógica, depois prossegue para `Next`. |
| `Condition` | Verifica uma ou mais condições booleanas. Prossegue para `Next` se passar, `Failed` se falhar. |
| `MovementCondition` | Ramifica com base na direção de movimento da entidade (ForwardLeft, ForwardRight, Left, Right, BackLeft, BackRight). |
| `UseBlock` | Tenta interagir com um bloco alvo. Vai para `Failed` se nenhum bloco for atingido. |
| `PlaceBlock` | Coloca o item de bloco segurado na localização alvo. |
| `Selector` | Varre um arco ou volume de hitbox para detectar entidades e blocos. Encaminha acertos para sub-interações `HitEntity` e `HitBlock`. |
| `Serial` | Executa uma lista de interações filhas em sequência. Usa um array `Interactions`. |
| `ApplyEffect` | Aplica um efeito de gameplay por `EffectId`. |
| `Replace` | Lê uma variável nomeada (`Var`) e substitui seu valor na cadeia. Volta para `DefaultValue` se a variável não estiver definida e `DefaultOk` for true. |

### Campos de Condition (Type: `"Condition"`)

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `RequiredGameMode` | string | Requer que a entidade esteja neste modo de jogo (ex.: `"Adventure"`). |
| `Crouching` | boolean | Se definido, requer (`true`) ou proíbe (`false`) agachamento. |
| `Flying` | boolean | Se definido, requer (`true`) ou proíbe (`false`) voo. |

### Campos de Selector (Type: `"Selector"`)

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `Selector.Id` | string | Tipo de forma da varredura (ex.: `"Horizontal"`). |
| `Selector.Direction` | string | Direção da varredura (ex.: `"ToLeft"`). |
| `Selector.TestLineOfSight` | boolean | Se verifica linha de visão antes de registrar acertos. |
| `Selector.StartDistance` | number | Borda próxima do volume de varredura. |
| `Selector.EndDistance` | number | Borda distante do volume de varredura. |
| `Selector.Length` | number | Comprimento do arco em graus. |
| `Selector.YawStartOffset` | number | Offset de yaw da direção que está encarando para iniciar a varredura. |
| `HitEntity` | object | Cadeia de interação executada para cada entidade atingida. |
| `HitBlock` | object | Cadeia de interação executada para cada bloco atingido. |

### Campos de DamageCalculator

Usado dentro de objetos de interação para definir a saída de dano.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `Type` | string | Método de cálculo. `"Absolute"` usa um valor de dano base fixo. |
| `BaseDamage` | object | Mapa de tipo de dano para quantidade (ex.: `{ "Physical": 12 }`). |
| `RandomPercentageModifier` | number | Fração do dano base adicionada como variância aleatória (ex.: `0.2` = +/-20%). |

### Campos de Effects

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `WorldSoundEventId` | string | ID de evento de som reproduzido na posição no mundo. |
| `LocalSoundEventId` | string | ID de evento de som reproduzido localmente (ouvido apenas pelo jogador que age). |
| `WorldParticles` | object[] | Array de sistemas de partículas `{ "SystemId": "<id>" }` gerados na posição no mundo. |
| `Particles` | object[] | Configs de partículas com `SystemId`, `Color`, `TargetNodeName`, `TargetEntityPart`. |
| `Trails` | object[] | Configs de efeito de rastro de arma com `TrailId`, `TargetNodeName`, `PositionOffset`, `RotationOffset`. |
| `CameraEffect` | string | ID de tremor/efeito de câmera aplicado ao jogador que age (ex.: `"Impact"`, `"Sword_Swing_Diagonal_Right"`). |
| `ItemAnimationId` | string | Animação reproduzida no item segurado (ex.: `"Consume"`, `"Build"`). |
| `WaitForAnimationToFinish` | boolean | Se a cadeia espera a animação do item terminar antes de continuar. |
| `Knockback` | object | Config de knockback com `Type`, `Force`, `Direction` (X/Y/Z), `VelocityType` e `VelocityConfig`. |

## Exemplos

`Assets/Server/Item/Interactions/Block_Primary.json`:

```json
{
  "Type": "Simple",
  "Next": {
    "Type": "UseBlock",
    "Failed": "Block_Attack"
  }
}
```

`Assets/Server/Item/Interactions/Block_Secondary.json`:

```json
{
  "Type": "UseBlock",
  "Failed": {
    "Type": "PlaceBlock",
    "RunTime": 0.125,
    "Effects": {
      "WaitForAnimationToFinish": false,
      "ItemAnimationId": "Build"
    }
  }
}
```

`Assets/Server/Item/Interactions/Consumables/Condition_Consume_Food.json`:

```json
{
  "Type": "Condition",
  "RequiredGameMode": "Adventure",
  "Crouching": false,
  "Next": "Consume_Charge",
  "Failed": "Block_Secondary"
}
```

`Assets/Server/Item/Interactions/Dodge.json`:

```json
{
  "Type": "Condition",
  "Flying": false,
  "Next": {
    "Type": "MovementCondition",
    "ForwardLeft": { "Type": "Simple" },
    "ForwardRight": { "Type": "Simple" },
    "Left": "Dodge_Left",
    "Right": "Dodge_Right",
    "BackLeft": { "Type": "Simple" },
    "BackRight": { "Type": "Simple" }
  }
}
```

`Assets/Server/Item/Interactions/Weapons/Common/Melee/Common_Melee_Damage.json`:

```json
{
  "Parent": "DamageEntityParent",
  "DamageCalculator": {
    "BaseDamage": {
      "Physical": 6
    }
  },
  "Effects": {
    "CameraEffect": "Impact"
  },
  "DamageEffects": {
    "Knockback": {
      "Type": "Force",
      "Force": 6.5,
      "Direction": { "X": 0.0, "Y": 1.0, "Z": -1.5 },
      "VelocityType": "Set"
    },
    "WorldSoundEventId": "SFX_Sword_T2_Impact",
    "LocalSoundEventId": "SFX_Sword_T2_Impact"
  }
}
```

## Páginas Relacionadas

- [Definições de Itens](/hytale-modding-docs/reference/item-system/item-definitions) — Onde `Interactions` e `InteractionVars` são definidos nos itens
- [Encadeamento de Interações](/hytale-modding-docs/reference/concepts/interaction-chaining) — Guia conceitual para construir pipelines de interação
