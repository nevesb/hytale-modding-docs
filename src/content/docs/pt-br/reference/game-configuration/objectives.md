---
title: Objetivos
description: Referência para definições de objetivos no Hytale, abrangendo objetivos de missão baseados em tarefas, linhas de objetivos, marcadores de localização e recompensas de conclusão.
---

## Visão Geral

O sistema de objetivos impulsiona jogabilidade similar a quests através de quatro tipos de arquivo: **Objectives** definem conjuntos sequenciais de tarefas e recompensas de conclusão, **ObjectiveLines** agrupam objetivos em uma cadeia de progressão, **ObjectiveLocationMarkers** posicionam gatilhos de área que ativam objetivos quando jogadores entram, e **ReachLocationMarkers** definem pontos de passagem nomeados usados por tarefas de alcançar-localização. As tarefas suportam tipos de matar, coletar, fabricar, recompensa, mapa do tesouro, usar-bloco, usar-entidade e alcançar-localização.

## Localização dos Arquivos

```
Assets/Server/Objective/
  Objectives/
    Objective_Bounty.json
    Objective_Craft.json
    Objective_Gather.json
    Objective_Gameplay_Trailer.json
    Objective_Kill.json
    Objective_KillSpawnBeacon.json
    Objective_KillSpawnMarker.json
    Objective_ReachLocation.json
    Objective_TreasureMap.json
    Objective_Tutorial.json
    Objective_UseBlock.json
    Objective_UseEntity.json
  ObjectiveLines/
    ObjectiveLine_Test.json
    ObjectiveLine_Tutorial.json
  ObjectiveLocationMarkers/
    ObjectiveLocationMarker_Gameplay_Trailer.json
    ObjectiveLocationMarker_KillSpawnBeacon.json
    ObjectiveLocationMarker_Test.json
    ObjectiveLocationMarker_Trigger.json
  ReachLocationMarkers/
    ObjectiveReachMarker_Example.json
```

## Schema

### Objective

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `TaskSets` | `TaskSet[]` | Sim | — | Array ordenado de conjuntos de tarefas. Cada conjunto deve ser completado antes que o próximo se torne ativo. |
| `Completions` | `Completion[]` | Não | `[]` | Recompensas ou ações disparadas quando todos os conjuntos de tarefas são finalizados. |
| `RemoveOnItemDrop` | `boolean` | Não | `false` | Quando `true`, o objetivo é removido se o jogador dropar o item associado. |

### TaskSet

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `Tasks` | `Task[]` | Sim | — | Array de tarefas dentro deste conjunto. Todas as tarefas devem ser completadas para avançar ao próximo conjunto. |

### Task

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `Type` | `string` | Sim | — | Tipo da tarefa. Veja os tipos de tarefa abaixo. |
| `Count` | `number` | Não | `1` | Número de vezes que a ação deve ser realizada. |
| `ItemId` | `string` | Não | — | ID do item para tarefas de fabricação ou relacionadas a itens. |
| `NPCGroupId` | `string` | Não | — | ID do grupo de NPC para tarefas de matar. |
| `NpcId` | `string` | Não | — | ID específico do NPC para tarefas de recompensa. |
| `TaskId` | `string` | Não | — | Identificador da tarefa para tarefas de usar-entidade. |
| `AnimationIdToPlay` | `string` | Não | — | Animação a reproduzir na entidade alvo durante tarefas de usar-entidade. |
| `BlockTagOrItemId` | `BlockTagOrItemId` | Não | — | Filtro de tag de bloco ou ID de item para tarefas de coletar e usar-bloco. |
| `TargetLocation` | `string` | Não | — | Nome do marcador de localização para tarefas de alcançar-localização. |
| `WorldLocationCondition` | `WorldLocationCondition` | Não | — | Restrições espaciais para tarefas de recompensa e mapa do tesouro. |
| `SpawnBeacons` | `SpawnBeacon[]` | Não | — | Definições de beacons de spawn para tarefas de kill-spawn-beacon. |
| `Chests` | `TreasureChest[]` | Não | — | Definições de baús para tarefas de mapa do tesouro. |
| `TaskConditions` | `TaskCondition[]` | Não | `[]` | Condições adicionais que devem ser atendidas para a tarefa contar. |

### Tipos de Tarefa

| Tipo | Descrição | Campos Principais |
|------|-----------|-------------------|
| `KillNPC` | Matar um número de NPCs de um grupo | `NPCGroupId`, `Count` |
| `KillSpawnBeacon` | Matar NPCs gerados por beacons específicos | `NPCGroupId`, `Count`, `SpawnBeacons` |
| `Gather` | Coletar itens ou blocos correspondentes a um filtro | `BlockTagOrItemId`, `Count` |
| `Craft` | Fabricar um item específico | `ItemId`, `Count` |
| `UseBlock` | Interagir com um tipo de bloco específico | `BlockTagOrItemId`, `Count`, `TaskConditions` |
| `UseEntity` | Interagir com um NPC ou entidade | `TaskId`, `Count`, `AnimationIdToPlay` |
| `ReachLocation` | Viajar até um ponto de passagem nomeado | `TargetLocation` |
| `Bounty` | Caçar um NPC específico dentro de um raio | `NpcId`, `WorldLocationCondition` |
| `TreasureMap` | Encontrar e abrir baús do tesouro | `Chests` |

### BlockTagOrItemId

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `ItemId` | `string` | Não | — | ID específico do item para corresponder. |
| `BlockTag` | `string` | Não | — | Tag de bloco para corresponder (corresponde a qualquer bloco com esta tag). |

### WorldLocationCondition

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `Type` | `string` | Sim | — | `"LocationRadius"` ou `"LookBlocksBelow"`. |
| `MinRadius` | `number` | Não | — | Distância mínima do provedor do objetivo. |
| `MaxRadius` | `number` | Não | — | Distância máxima do provedor do objetivo. |
| `BlockTags` | `string[]` | Não | — | Tags de blocos para verificar abaixo da localização alvo (para `"LookBlocksBelow"`). |
| `Count` | `number` | Não | — | Número de blocos para verificar abaixo. |
| `MinRange` | `number` | Não | — | Intervalo mínimo de profundidade para verificação de blocos. |
| `MaxRange` | `number` | Não | — | Intervalo máximo de profundidade para verificação de blocos. |

### TreasureChest

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `MinRadius` | `number` | Sim | — | Distância mínima de posicionamento do jogador. |
| `MaxRadius` | `number` | Sim | — | Distância máxima de posicionamento do jogador. |
| `DropList` | `string` | Sim | — | ID da lista de drops para o conteúdo do baú. |
| `WorldLocationCondition` | `WorldLocationCondition` | Não | — | Restrições de terreno para posicionamento do baú. |
| `ChestBlockTypeKey` | `string` | Sim | — | Tipo de bloco usado para o baú do tesouro. |

### TaskCondition

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `Type` | `string` | Sim | — | Tipo de condição: `"SoloInventory"`. |
| `BlockTagOrItemId` | `BlockTagOrItemId` | Não | — | Item ou bloco que o jogador deve possuir. |
| `Quantity` | `number` | Não | — | Quantidade necessária do item. |

### Completion

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `Type` | `string` | Sim | — | Ação de conclusão: `"GiveItems"` ou `"ClearObjectiveItems"`. |
| `DropList` | `string` | Não | — | ID da lista de drops para recompensas de itens (quando `Type` é `"GiveItems"`). |

### ObjectiveLine

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `ObjectiveIds` | `string[]` | Sim | — | Array ordenado de IDs de objetivos a apresentar em sequência. |

### ObjectiveLocationMarker

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `Setup` | `MarkerSetup` | Sim | — | O que acontece quando um jogador entra na área do marcador. |
| `Area` | `MarkerArea` | Sim | — | Definição espacial da zona de gatilho. |
| `TriggerConditions` | `TriggerCondition[]` | Não | `[]` | Condições adicionais que devem ser atendidas para o marcador ser ativado. |

### MarkerSetup

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `Type` | `string` | Sim | — | Tipo de configuração: `"Objective"`. |
| `ObjectiveId` | `string` | Sim | — | ID do objetivo a ser ativado. |

### MarkerArea

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `Type` | `string` | Sim | — | Tipo de área: `"Radius"`. |
| `EntryRadius` | `number` | Sim | — | Distância em blocos na qual o marcador é ativado. |
| `ExitRadius` | `number` | Sim | — | Distância em blocos na qual o marcador é desativado. Deve ser maior que `EntryRadius` para prevenir oscilação. |

### TriggerCondition

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `Type` | `string` | Sim | — | Tipo de condição: `"HourRange"` ou `"Weather"`. |
| `MinHour` | `number` | Não | — | Hora de início para condições de intervalo de horas. |
| `MaxHour` | `number` | Não | — | Hora de fim para condições de intervalo de horas. Funciona através da meia-noite. |
| `WeatherIds` | `string[]` | Não | — | IDs de clima necessários para condições de clima. |

### ReachLocationMarker

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `Radius` | `number` | Sim | — | Distância em blocos dentro da qual o jogador é considerado ter alcançado a localização. |
| `Name` | `string` | Sim | — | Nome de exibição para o marcador do ponto de passagem. |

## Exemplos

**Objetivo de matar** (`Assets/Server/Objective/Objectives/Objective_Kill.json`):

```json
{
  "TaskSets": [
    {
      "Tasks": [
        {
          "Type": "KillNPC",
          "Count": 3,
          "NPCGroupId": "Trork_Warrior"
        }
      ]
    }
  ],
  "Completions": [
    {
      "Type": "GiveItems",
      "DropList": "Trork_Camp_Inventory"
    }
  ]
}
```

**Linha de objetivo do tutorial** (`Assets/Server/Objective/ObjectiveLines/ObjectiveLine_Tutorial.json`):

```json
{
  "ObjectiveIds": [
    "Objective_Tutorial"
  ]
}
```

**Marcador de localização com condições de gatilho** (`Assets/Server/Objective/ObjectiveLocationMarkers/ObjectiveLocationMarker_Trigger.json`):

```json
{
  "Setup": {
    "Type": "Objective",
    "ObjectiveId": "Objective_Kill"
  },
  "Area": {
    "Type": "Radius",
    "EntryRadius": 25,
    "ExitRadius": 35
  },
  "TriggerConditions": [
    { "Type": "HourRange", "MinHour": 17, "MaxHour": 2 },
    { "Type": "Weather", "WeatherIds": ["Zone1_Cloudy_Medium"] }
  ]
}
```

**Objetivo de mapa do tesouro** (`Assets/Server/Objective/Objectives/Objective_TreasureMap.json`):

```json
{
  "TaskSets": [
    {
      "Tasks": [
        {
          "Type": "TreasureMap",
          "Chests": [
            {
              "MinRadius": 10,
              "MaxRadius": 20,
              "DropList": "Zone1_Encounters_Tier3",
              "WorldLocationCondition": {
                "Type": "LookBlocksBelow",
                "BlockTags": ["Stone", "Soil"],
                "Count": 3,
                "MinRange": 0,
                "MaxRange": 5
              },
              "ChestBlockTypeKey": "Furniture_Ancient_Chest_Large"
            }
          ]
        }
      ]
    }
  ],
  "Completions": [
    { "Type": "ClearObjectiveItems" }
  ],
  "RemoveOnItemDrop": true
}
```

## Páginas Relacionadas

- [Configurações de Jogabilidade](/hytale-modding-docs/reference/game-configuration/gameplay-configs) — configuração `IsObjectiveMarkersEnabled`
- [Instâncias](/hytale-modding-docs/reference/game-configuration/instances) — configuração de marcadores de objetivo a nível de instância
- [Tabelas de Drop](/hytale-modding-docs/reference/economy-and-progression/drop-tables) — listas de drops referenciadas por recompensas de conclusão
- [Listas de Tipos de Blocos](/hytale-modding-docs/reference/game-configuration/block-type-lists) — tags de blocos usadas em tarefas de coletar e usar-bloco
