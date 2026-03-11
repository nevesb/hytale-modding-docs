---
title: Templates de NPC
description: Arquivos de template base que definem comportamento compartilhado de NPCs e o sistema de heranca de parametros Reference/Modify.
---

## Visao Geral

Templates de NPC sao arquivos de role `Abstract` que definem comportamento, atributos e logica de IA comuns compartilhados por uma familia de NPCs. Roles concretos referenciam um template pelo campo `Reference` e sobrescrevem valores seletivamente via `Modify`. O sistema de `Parameters` permite que templates declarem padroes nomeados com documentacao que roles concretos podem sobrescrever sem alterar o template em si.

## Localizacao dos Arquivos

`Assets/Server/NPC/Roles/_Core/Templates/*.json`

## O Padrao Reference / Modify

Um arquivo de role `Variant` vincula-se a um template e sobrescreve campos especificos:

```json
{
  "Type": "Variant",
  "Reference": "Template_Predator",
  "Modify": {
    "Appearance": "Fox",
    "MaxHealth": 38
  }
}
```

O engine faz o merge da definicao completa do template com o bloco `Modify`. Campos nao listados em `Modify` mantem o valor do template. O valor de `Reference` e o nome do arquivo sem a extensao `.json`.

## O Sistema Parameter / Compute

Templates declaram `Parameters` — valores nomeados com um padrao e uma descricao:

```json
{
  "Parameters": {
    "MaxHealth": {
      "Value": 100,
      "Description": "Max health for the NPC"
    },
    "Appearance": {
      "Value": "Bear_Grizzly",
      "Description": "Model to be used"
    }
  }
}
```

Campos de nivel superior no template leem desses parametros usando o atalho `Compute`:

```json
{
  "MaxHealth": { "Compute": "MaxHealth" },
  "Appearance": { "Compute": "Appearance" }
}
```

Um role `Variant` concreto sobrescreve um parametro fornecendo um novo valor no seu proprio bloco `Parameters` dentro de `Modify`:

```json
{
  "Type": "Variant",
  "Reference": "Template_Predator",
  "Modify": {
    "MaxHealth": 38,
    "Appearance": "Fox"
  },
  "Parameters": {
    "NameTranslationKey": {
      "Value": "server.npcRoles.Fox.name",
      "Description": "Translation key for NPC name display"
    }
  }
}
```

## Schema — Campos do Template (Abstract)

| Field | Type | Descricao |
|-------|------|-----------|
| `Type` | `"Abstract"` | Marca este arquivo como template base nao spawnavel. |
| `StartState` | string | Estado inicial de IA, ex: `"Idle"`. |
| `Parameters` | object | Definicoes de parametros nomeados. Cada entrada tem `Value`, `TypeHint` opcional e `Description`. |
| `Appearance` | Compute | Resolvido a partir de `Parameters.Appearance`. |
| `MaxHealth` | Compute | Resolvido a partir de `Parameters.MaxHealth`. |
| `DropList` | Compute | Resolvido a partir de `Parameters.DropList`. |
| `NameTranslationKey` | Compute | Resolvido a partir de `Parameters.NameTranslationKey`. |
| `MotionControllerList` | array | Controladores de locomocao (Walk, Fly, Swim). |
| `Instructions` | array | Arvore de comportamento de IA completa compartilhada por todas as variantes. |
| `KnockbackScale` | number | Multiplicador de knockback padrao. |
| `DisableDamageGroups` | string[] | Grupos de dano bloqueados por padrao. |

## Templates Base Disponiveis

| Template | Familia de Comportamento | Padroes Principais |
|----------|--------------------------|---------------------|
| `Template_Predator` | Cacador agressivo, ataca e foge se ameacado | `ViewRange: 24`, `AlertedRange: 28`, `FleeIfNotThreatened: true` |
| `Template_Animal_Neutral` | Animal presa passivo, foge quando ameacado | `ViewRange: 16`, `AlertedRange: 18`, `StartState: Idle` |
| `Template_Livestock` | Animal de fazenda domesticavel com pastejo e producao | `AlertedActionRange: 6`, `GrazingBlockSet: Grass` |
| `Template_Birds_Passive` | Passaro passivo voador com comportamento de bando | `FlockArray: ["Template_Birds_Passive"]`, `MotionControllerList: [Fly]` |
| `Template_Intelligent` | NPC de faccao com IA de combate e pedido de ajuda | `AlertedRange: 45`, `ChanceToBeAlertedWhenReceivingCallForHelp: 70` |
| `Template_Beasts_Passive_Critter` | Pequena criatura passiva | Atributos minimos, comportamento de bando em escala de criatura |
| `Template_Edible_Critter` | Criatura passiva que pode ser comida | Estende criatura com interacao de comida |
| `Template_Spirit` | Entidade espiritual com movimento especial | Locomocao de espirito, padroes de particulas |
| `Template_Summoned_Ally` | Invocacao aliada do jogador | Atitude amigavel ao jogador por padrao |
| `Template_Swimming_Aggressive` | NPC aquatico agressivo | Locomocao de natacao, IA hostil |
| `Template_Swimming_Passive` | NPC aquatico passivo | Locomocao de natacao, comportamento de fuga |
| `Template_Temple` | NPC guardiao de templo | IA de guardiao, vida alta |

## Exemplo — Template_Animal_Neutral (abreviado)

Este e o template que `Chicken`, `Deer`, `Moose` e outros animais neutros herdam:

```json
{
  "Type": "Abstract",
  "StartState": "Idle",
  "Parameters": {
    "Appearance": {
      "Value": "Deer_Stag",
      "Description": "The NPC's model."
    },
    "ViewRange": {
      "Value": 16,
      "Description": "The view distance of the NPC, in blocks."
    },
    "ViewSector": {
      "Value": 180,
      "Description": "The view sector of the NPC, in degrees."
    },
    "HearingRange": {
      "Value": 8,
      "Description": "The hearing distance of the NPC, in blocks."
    },
    "AbsoluteDetectionRange": {
      "Value": 4,
      "Description": "The range at which a target is guaranteed to be detected, in blocks."
    },
    "AlertedRange": {
      "Value": 18,
      "Description": "The range within which the target can be seen when alerted, in blocks."
    },
    "AlertedActionRange": {
      "Value": 8,
      "Description": "The range at which an NPC will react to players, in blocks."
    },
    "DropList": {
      "Value": "Empty",
      "Description": "The NPC's drop list."
    },
    "AttractiveItemSet": {
      "Value": [],
      "TypeHint": "String",
      "Description": "Items that are deemed attractive when held nearby."
    },
    "MaxHealth": {
      "Value": 100,
      "Description": "Max health for the NPC"
    },
    "NameTranslationKey": {
      "Value": "server.npcRoles.Template.name",
      "Description": "Translation key for NPC name display"
    }
  }
}
```

## Paginas Relacionadas

- [NPC Roles](/hytale-modding-docs/reference/npc-system/npc-roles) — Schema completo de arquivos de role e exemplos concretos de NPCs
- [NPC Decision Making](/hytale-modding-docs/reference/npc-system/npc-decision-making) — Tipos de condicao de IA usados dentro dos templates
- [Inheritance and Templates](/hytale-modding-docs/reference/concepts/inheritance-and-templates) — Heranca geral de templates em todos os tipos de configuracao
