---
title: Atributos de Entidade
description: Referencia para definicoes de atributos de entidade no lado do servidor no Hytale, cobrindo valores base, regras de regeneracao, condicoes e efeitos de limiar.
---

## Visao Geral

Os atributos de entidade definem atributos numericos como vida, stamina, mana e oxigenio que sao rastreados por entidade. Cada arquivo de atributo declara a faixa de valores, regras de regeneracao opcionais com logica condicional e efeitos disparados por limiares. Os atributos sao consumidos pelo sistema de combate, sistema de movimento e sistema de efeitos para restringir habilidades, aplicar dano e disparar mudancas de status.

## Localizacao dos Arquivos

```
Assets/Server/Entity/Stats/
```

Um arquivo JSON por atributo:

```
Assets/Server/Entity/Stats/
  Ammo.json
  DeployablePreview.json
  GlidingActive.json
  Health.json
  Immunity.json
  MagicCharges.json
  Mana.json
  Oxygen.json
  SignatureCharges.json
  SignatureEnergy.json
  Stamina.json
  StaminaRegenDelay.json
```

## Schema

### Campos de nivel superior

| Campo | Tipo | Obrigatorio | Padrao | Descricao |
|-------|------|-------------|--------|-----------|
| `InitialValue` | `number` | Sim | — | Valor inicial do atributo quando a entidade surge. |
| `Min` | `number` | Sim | — | Valor minimo que o atributo pode atingir. Pode ser negativo (ex: estado de stamina sobrecarregada). |
| `Max` | `number` | Sim | — | Valor maximo que o atributo pode atingir. `0` significa que o limite e definido dinamicamente (ex: por equipamento). |
| `Shared` | `boolean` | Nao | `false` | Se `true`, o valor do atributo e sincronizado para todos os clientes proximos para exibicao no HUD. |
| `ResetType` | `string` | Nao | — | Como o atributo e redefinido ao renascer. Valor conhecido: `"MaxValue"` (redefine para `Max`). |
| `IgnoreInvulnerability` | `boolean` | Nao | `false` | Se `true`, modificacoes neste atributo ignoram verificacoes de invulnerabilidade. |
| `HideFromTooltip` | `boolean` | Nao | `false` | Se `true`, o atributo e oculto da interface de tooltip do jogador. |
| `Regenerating` | `RegenRule[]` | Nao | — | Lista de regras de regeneracao avaliadas em ordem. Varias regras podem se acumular ou conflitar. |
| `MinValueEffects` | `ThresholdEffects` | Nao | — | Interacoes disparadas quando o atributo atinge seu valor minimo. |
| `MaxValueEffects` | `ThresholdEffects` | Nao | — | Interacoes disparadas quando o atributo atinge seu valor maximo. |

### RegenRule

| Campo | Tipo | Obrigatorio | Padrao | Descricao |
|-------|------|-------------|--------|-----------|
| `$Comment` | `string` | Nao | — | Nota legivel por humanos, ignorada pelo motor. |
| `Interval` | `number` | Sim | — | Segundos entre cada tick de regeneracao. |
| `Amount` | `number` | Sim | — | Valor adicionado (ou subtraido se negativo) por tick. |
| `RegenType` | `"Additive" \| "Percentage"` | Sim | — | `Additive` adiciona um valor fixo; `Percentage` adiciona uma fracao do maximo. |
| `ClampAtZero` | `boolean` | Nao | `false` | Se `true`, o tick de regeneracao nao reduzira o valor abaixo de zero. |
| `Conditions` | `Condition[]` | Nao | — | Todas as condicoes devem ser atendidas para que esta regra esteja ativa. |

### Condition

| Campo | Tipo | Obrigatorio | Padrao | Descricao |
|-------|------|-------------|--------|-----------|
| `Id` | `string` | Sim | — | Identificador do tipo de condicao. Valores conhecidos: `"Alive"`, `"Player"`, `"NoDamageTaken"`, `"Stat"`, `"Wielding"`, `"Sprinting"`, `"Gliding"`, `"Charging"`, `"Suffocating"`, `"RegenHealth"`. |
| `Inverse` | `boolean` | Nao | `false` | Se `true`, a condicao e negada (NAO deve ser atendida). |
| `Delay` | `number` | Nao | — | Segundos que devem passar desde que a condicao foi verdadeira pela ultima vez. Usado com `"NoDamageTaken"` para criar atrasos de regeneracao. |
| `GameMode` | `string` | Nao | — | Modo de jogo necessario. Usado com a condicao `"Player"`, ex: `"Creative"`. |
| `Stat` | `string` | Nao | — | ID do atributo para comparacao. Usado com a condicao `"Stat"`. |
| `Amount` | `number` | Nao | — | Valor limite para comparacao de atributo. Usado com a condicao `"Stat"`. |
| `Comparison` | `string` | Nao | — | Operador de comparacao. Valores conhecidos: `"Gte"` (maior-ou-igual), `"Lt"` (menor-que). |

### ThresholdEffects

| Campo | Tipo | Obrigatorio | Padrao | Descricao |
|-------|------|-------------|--------|-----------|
| `TriggerAtZero` | `boolean` | Nao | `false` | Se `true`, dispara quando o atributo atinge exatamente zero em vez do minimo real. |
| `Interactions` | `object` | Nao | — | Container com um array `Interactions` de objetos de interacao (ex: `ChangeStat`, `ClearEntityEffect`, `ApplyEffect`). |

## Exemplos

**Health** (`Assets/Server/Entity/Stats/Health.json`):

```json
{
  "InitialValue": 100,
  "Min": 0,
  "Max": 100,
  "Shared": true,
  "ResetType": "MaxValue",
  "Regenerating": [
    {
      "$Comment": "NPC",
      "Interval": 0.5,
      "Amount": 0.05,
      "RegenType": "Percentage",
      "Conditions": [
        { "Id": "Alive" },
        { "Id": "Player", "Inverse": true },
        { "Id": "NoDamageTaken", "Delay": 15 },
        { "Id": "RegenHealth" }
      ]
    },
    {
      "$Comment": "Player in creative mode",
      "Interval": 0.5,
      "Amount": 1.0,
      "RegenType": "Percentage",
      "Conditions": [
        { "Id": "Alive" },
        { "Id": "Player", "GameMode": "Creative" }
      ]
    }
  ]
}
```

**Immunity** (`Assets/Server/Entity/Stats/Immunity.json`):

```json
{
  "InitialValue": 0,
  "Min": 0,
  "Max": 100,
  "Shared": true,
  "Regenerating": [
    {
      "Interval": 0.1,
      "Amount": -0.1,
      "RegenType": "Additive"
    }
  ],
  "MaxValueEffects": {
    "Interactions": {
      "Interactions": [
        {
          "Type": "ApplyEffect",
          "EffectId": "Immune"
        }
      ]
    }
  }
}
```

## Paginas Relacionadas

- [Efeitos de Entidade](/pt-br/hytale-modding-docs/reference/combat-and-projectiles/entity-effects) — efeitos disparados por limiares de atributos
- [Tipos de Dano](/pt-br/hytale-modding-docs/reference/combat-and-projectiles/damage-types) — dano que modifica o atributo Health
- [Projeteis](/pt-br/hytale-modding-docs/reference/combat-and-projectiles/projectiles) — dano de projeteis aplicado a atributos
