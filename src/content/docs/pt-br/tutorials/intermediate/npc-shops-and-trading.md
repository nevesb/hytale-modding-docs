---
title: Lojas de NPCs e Comércio
description: Tutorial passo a passo para configurar um NPC mercador Feran com uma loja de troca que troca Frutas Encantadas por Mudas Encantadas.
sidebar:
  order: 3
---

## Objetivo

Criar um **Mercador Feran Longtooth** — um NPC passivo que oferece trocas de itens, trocando Frutas Encantadas por Mudas Encantadas e blocos Crystal Glow. Você vai construir a definição da loja, configurar a função do NPC com lógica de interação e conectar tudo para que os jogadores possam clicar com o botão direito no NPC para negociar.

## O Que Você Vai Aprender

- Como definições de lojas de troca controlam inventários de comércio de NPCs
- Como slots de comércio `Fixed` oferecem trocas sempre disponíveis
- Como slots de comércio `Pool` criam estoque rotativo aleatório
- Como `InteractionInstruction` com `OpenBarterShop` conecta a loja a um NPC
- Como `Stock`, `RefreshInterval` e `RestockHour` gerenciam resets de inventário

## Pré-requisitos

- Um ambiente de mod funcional (veja [Configurar Seu Ambiente de Desenvolvimento](/hytale-modding-docs/pt-br/tutorials/beginner/setup-dev-environment/))
- O mod Árvore Encantada instalado (veja [Árvores e Mudas Personalizadas](/hytale-modding-docs/pt-br/tutorials/intermediate/custom-trees-and-saplings/)) — fornece `Plant_Fruit_Enchanted` e `Plant_Sapling_Enchanted`
- O NPC Slime com tabela de loot (veja [Tabelas de Loot Personalizadas](/hytale-modding-docs/pt-br/tutorials/intermediate/custom-loot-tables/)) — o Slime dropa Frutas Encantadas

**Repositório do mod complementar:** [hytale-mods-custom-shop](https://github.com/nevesb/hytale-mods-custom-shop)

:::tip[Loop de Jogo]
Este tutorial completa o loop de jogabilidade de todos os tutoriais anteriores: mate Slimes ou colha Árvores Encantadas para coletar Frutas Encantadas, depois troque 3 Frutas no mercador Feran por uma nova Muda Encantada para plantar mais árvores.
:::

---

## Visão Geral da Loja de Troca

Lojas de troca ficam em `Server/BarterShops/` e definem o que um NPC mercador vende. O Hytale usa um sistema de **troca** — jogadores trocam itens diretamente por outros itens, não há moeda.

Cada troca tem um `Input` (o que o jogador paga) e um `Output` (o que o jogador recebe). O jogo vanilla inclui dois mercadores:

- **Mercador Kweebec** — 3 trocas fixas + 2 grupos pool com estoque rotativo, reabastece a cada 3 dias
- **Mercador Klops** — 1 troca fixa, reabastece diariamente

---

## Passo 1: Configurar a Estrutura de Arquivos do Mod

```text
NPCShopsAndTrading/
├── manifest.json
├── Server/
│   ├── BarterShops/
│   │   └── Feran_Enchanted_Merchant.json
│   ├── NPC/
│   │   └── Roles/
│   │       └── Feran_Enchanted_Merchant.json
│   └── Languages/
│       ├── en-US/
│       │   └── server.lang
│       ├── es/
│       │   └── server.lang
│       └── pt-BR/
│           └── server.lang
```

### manifest.json

```json
{
  "Group": "HytaleModdingManual",
  "Name": "NPCShopsAndTrading",
  "Version": "1.0.0",
  "Description": "Feran Longtooth merchant that trades Enchanted Fruit for Enchanted Saplings",
  "Authors": [
    {
      "Name": "HytaleModdingManual"
    }
  ],
  "Dependencies": {},
  "OptionalDependencies": {},
  "IncludesAssetPack": false,
  "TargetServerVersion": "2026.02.19-1a311a592"
}
```

Note que `IncludesAssetPack` é `false` — este mod adiciona apenas arquivos JSON do lado do servidor. O modelo do Feran Longtooth já existe no vanilla, então não precisamos de uma pasta `Common/`.

---

## Passo 2: Criar a Definição da Loja de Troca

A definição da loja controla quais trocas aparecem na interface quando o jogador interage com o mercador.

Crie `Server/BarterShops/Feran_Enchanted_Merchant.json`:

```json
{
  "DisplayNameKey": "server.barter.feran_enchanted_merchant.title",
  "RefreshInterval": {
    "Days": 2
  },
  "RestockHour": 6,
  "TradeSlots": [
    {
      "Type": "Fixed",
      "Trade": {
        "Output": { "ItemId": "Plant_Sapling_Enchanted", "Quantity": 1 },
        "Input": [{ "ItemId": "Plant_Fruit_Enchanted", "Quantity": 3 }],
        "Stock": 5
      }
    },
    {
      "Type": "Fixed",
      "Trade": {
        "Output": { "ItemId": "Ore_Crystal_Glow", "Quantity": 1 },
        "Input": [{ "ItemId": "Plant_Fruit_Enchanted", "Quantity": 10 }],
        "Stock": 3
      }
    }
  ]
}
```

### Campos da Loja

| Campo | Finalidade |
|-------|-----------|
| `DisplayNameKey` | Chave de tradução para o título da loja mostrado na interface de comércio |
| `RefreshInterval.Days` | Número de dias no jogo entre reabastecimentos de estoque |
| `RestockHour` | Hora do dia (0-24) quando o reabastecimento acontece. `6` = 6h |
| `TradeSlots` | Array de definições de slots de comércio (`Fixed` ou `Pool`) |

Esta loja tem duas trocas fixas:

| Troca | Input | Output | Estoque |
|-------|-------|--------|---------|
| Muda | 3 Frutas Encantadas | 1 Muda Encantada | 5 por reabastecimento |
| Cristal | 10 Frutas Encantadas | 1 bloco Crystal Glow | 3 por reabastecimento |

O bloco Crystal Glow é mais caro (10 frutas vs 3) e tem menor estoque, tornando-o uma troca premium.

---

## Passo 3: Entendendo os Tipos de Slots de Comércio

### Slots Fixos

Slots fixos sempre aparecem na loja e oferecem a mesma troca:

```json
{
  "Type": "Fixed",
  "Trade": {
    "Output": { "ItemId": "Plant_Sapling_Enchanted", "Quantity": 1 },
    "Input": [{ "ItemId": "Plant_Fruit_Enchanted", "Quantity": 3 }],
    "Stock": 5
  }
}
```

| Campo | Finalidade |
|-------|-----------|
| `Trade.Output` | O item e quantidade que o jogador recebe |
| `Trade.Input` | Array de itens que o jogador deve pagar. Múltiplas entradas requerem todos os itens |
| `Trade.Stock` | Número de vezes que esta troca pode ser completada antes do reabastecimento |

### Slots Pool

Slots pool selecionam aleatoriamente trocas de um pool maior a cada reabastecimento, criando estoque rotativo. O `Kweebec_Merchant` vanilla usa este padrão:

```json
{
  "Type": "Pool",
  "SlotCount": 3,
  "Trades": [
    {
      "Weight": 50,
      "Output": { "ItemId": "Food_Salad_Fruit", "Quantity": 2 },
      "Input": [{ "ItemId": "Ingredient_Life_Essence", "Quantity": 20 }],
      "Stock": [4, 8]
    },
    {
      "Weight": 20,
      "Output": { "ItemId": "Recipe_Food_Pie_Apple", "Quantity": 1 },
      "Input": [{ "ItemId": "Ingredient_Life_Essence_Concentrated", "Quantity": 2 }],
      "Stock": [1]
    }
  ]
}
```

| Campo | Finalidade |
|-------|-----------|
| `SlotCount` | Número de trocas selecionadas aleatoriamente do pool a cada reabastecimento |
| `Trades[].Weight` | Probabilidade relativa desta troca aparecer. Maior = mais provável |
| `Trades[].Stock` | Formato array: `[fixo]` para estoque exato ou `[mín, máx]` para intervalo aleatório |

A diferença dos slots fixos: o `Stock` de pool usa um **array** (`[4, 8]` significa 4-8 unidades), enquanto o `Stock` fixo usa um **número** (`5` significa exatamente 5).

---

## Passo 4: Criar a Função do NPC Mercador

Este é o passo mais importante. Mercadores vanilla usam um NPC `Type: "Generic"` com `InteractionInstruction` que abre a loja de troca quando o jogador clica com o botão direito. Isso é muito diferente de NPCs de combate que usam `Variant` + `Reference`.

Crie `Server/NPC/Roles/Feran_Enchanted_Merchant.json`:

```json
{
  "Type": "Generic",
  "Parameters": {
    "NameTranslationKey": {
      "Value": "server.npcRoles.Feran_Enchanted_Merchant.name",
      "Description": "Translation key for NPC name display"
    }
  },
  "StartState": "Idle",
  "DefaultNPCAttitude": "Ignore",
  "DefaultPlayerAttitude": "Neutral",
  "Appearance": "Feran_Longtooth",
  "MaxHealth": 100,
  "KnockbackScale": 0.5,
  "IsMemory": true,
  "MemoriesCategory": "Feran",
  "BusyStates": ["$Interaction"],
  "MotionControllerList": [
    {
      "Type": "Walk",
      "MaxWalkSpeed": 3,
      "Gravity": 10,
      "RunThreshold": 0.3,
      "MaxFallSpeed": 15,
      "MaxRotationSpeed": 360,
      "Acceleration": 10
    }
  ],
  "Instructions": [
    {
      "Instructions": [
        {
          "$Comment": "Idle state - no player nearby",
          "Sensor": { "Type": "State", "State": "Idle" },
          "Instructions": [
            {
              "$Comment": "Watch player when they approach",
              "Sensor": { "Type": "Player", "Range": 8 },
              "Actions": [
                { "Type": "State", "State": "Watching" }
              ]
            },
            {
              "Sensor": { "Type": "Any" },
              "BodyMotion": { "Type": "Nothing" }
            }
          ]
        },
        {
          "$Comment": "Watching state - player is nearby",
          "Sensor": { "Type": "State", "State": "Watching" },
          "Instructions": [
            {
              "Continue": true,
              "Sensor": { "Type": "Player", "Range": 12 },
              "HeadMotion": { "Type": "Watch" }
            },
            {
              "$Comment": "Return to Idle when player leaves",
              "Sensor": {
                "Type": "Not",
                "Sensor": { "Type": "Player", "Range": 12 }
              },
              "Actions": [
                { "Type": "State", "State": "Idle" }
              ]
            },
            {
              "Sensor": { "Type": "Any" },
              "BodyMotion": { "Type": "Nothing" }
            }
          ]
        },
        {
          "$Comment": "Interaction state - look at player while shop is open",
          "Sensor": { "Type": "State", "State": "$Interaction" },
          "Instructions": [
            {
              "Continue": true,
              "Sensor": { "Type": "Target", "Range": 10 },
              "HeadMotion": { "Type": "Watch" }
            },
            {
              "Sensor": { "Type": "Any" },
              "Actions": [
                {
                  "Type": "Timeout",
                  "Delay": [1, 1],
                  "Action": {
                    "Type": "Sequence",
                    "Actions": [
                      { "Type": "ReleaseTarget" },
                      { "Type": "State", "State": "Watching" }
                    ]
                  }
                }
              ]
            }
          ]
        }
      ]
    }
  ],
  "InteractionInstruction": {
    "Instructions": [
      {
        "Sensor": {
          "Type": "Not",
          "Sensor": { "Type": "CanInteract", "ViewSector": 180 }
        },
        "Actions": [
          { "Type": "SetInteractable", "Interactable": false }
        ]
      },
      {
        "Continue": true,
        "Sensor": { "Type": "Any" },
        "Actions": [
          {
            "Type": "SetInteractable",
            "Interactable": true,
            "Hint": "server.interactionHints.trade"
          }
        ]
      },
      {
        "Sensor": { "Type": "HasInteracted" },
        "Instructions": [
          {
            "Sensor": {
              "Type": "Not",
              "Sensor": { "Type": "State", "State": "$Interaction" }
            },
            "Actions": [
              { "Type": "LockOnInteractionTarget" },
              { "Type": "OpenBarterShop", "Shop": "Feran_Enchanted_Merchant" },
              { "Type": "State", "State": "$Interaction" }
            ]
          }
        ]
      }
    ]
  },
  "NameTranslationKey": { "Compute": "NameTranslationKey" }
}
```

### Como o NPC Mercador Funciona

Este é um NPC `Type: "Generic"` — diferente de NPCs de combate que herdam de templates, mercadores definem seu comportamento diretamente. Veja o que cada seção faz:

| Seção | Finalidade |
|-------|-----------|
| `DefaultPlayerAttitude: "Neutral"` | O NPC não ataca jogadores |
| `BusyStates: ["$Interaction"]` | Impede o NPC de fazer outras coisas enquanto a loja está aberta |
| `Instructions` | Comportamento de IA: parado, observar jogadores que se aproximam, olhar para o jogador durante a troca |
| `InteractionInstruction` | Lógica de clique direito: mostrar dica de comércio, abrir loja quando clicado |

A parte crítica é a `InteractionInstruction`:

1. **`SetInteractable`** com `Hint: "server.interactionHints.trade"` — mostra a tooltip "Negociar" quando o jogador olha para o NPC
2. **`HasInteracted`** sensor — é acionado quando o jogador clica com o botão direito
3. **`OpenBarterShop`** com `Shop: "Feran_Enchanted_Merchant"` — abre a interface de comércio vinculada à definição da loja
4. **`LockOnInteractionTarget`** — faz o NPC virar para o jogador durante a troca

:::caution[NPCs Generic vs Variant]
NPCs de combate usam `"Type": "Variant"` com `"Reference": "Template_Predator"` para herdar comportamento de IA. NPCs mercadores usam `"Type": "Generic"` e definem suas próprias instruções, porque precisam de lógica de interação personalizada que os templates não fornecem.
:::

---

## Passo 5: Adicionar Chaves de Tradução

Crie um arquivo `server.lang` para cada idioma:

**`Server/Languages/en-US/server.lang`**
```properties
npcRoles.Feran_Enchanted_Merchant.name = Enchanted Merchant
barter.feran_enchanted_merchant.title = Enchanted Merchant
interactionHints.trade = Trade
```

**`Server/Languages/es/server.lang`**
```properties
npcRoles.Feran_Enchanted_Merchant.name = Mercader Encantado
barter.feran_enchanted_merchant.title = Mercader Encantado
interactionHints.trade = Comerciar
```

**`Server/Languages/pt-BR/server.lang`**
```properties
npcRoles.Feran_Enchanted_Merchant.name = Mercador Encantado
barter.feran_enchanted_merchant.title = Mercador Encantado
interactionHints.trade = Negociar
```

As chaves `.lang` omitem o prefixo `server.` — o engine adiciona automaticamente para arquivos de idioma do lado do servidor.

---

## Passo 6: Testar No Jogo

1. Copie a pasta `NPCShopsAndTrading/` para `%APPDATA%/Hytale/UserData/Mods/`

2. Certifique-se de que o mod **CustomTreesAndSaplings** também está instalado — a loja referencia itens dele

3. Inicie o Hytale e entre no **Modo Criativo**

4. Gere o mercador e pegue algumas Frutas Encantadas para negociar:
   ```text
   /op self
   /npc spawn Feran_Enchanted_Merchant
   /spawnitem Plant_Fruit_Enchanted 9
   ```

5. Clique com o botão direito no Feran para abrir a loja de troca

![NPC Mercador Feran Encantado no jogo](/hytale-modding-docs/images/tutorials/npc-shops-and-trading/feran-merchant.png)

![Interface da loja de troca mostrando ambas as trocas](/hytale-modding-docs/images/tutorials/npc-shops-and-trading/barter-shop-ui.png)

6. Verifique:
   - O título da loja mostra "Mercador Encantado"
   - A troca mostra: 3 Frutas Encantadas → 1 Muda Encantada
   - Você pode completar a troca 5 vezes (Stock: 5)
   - Após comprar todas as 5, o slot aparece como esgotado

**Erros comuns e correções:**

| Erro | Causa | Correção |
|------|-------|----------|
| `Unknown barter shop` | O valor de `Shop` em `OpenBarterShop` não corresponde ao nome do arquivo | Certifique-se de que `"Shop": "Feran_Enchanted_Merchant"` corresponda a `Feran_Enchanted_Merchant.json` |
| Sem dica de comércio ao passar o mouse | `InteractionInstruction` ausente ou malformada | Verifique se a ação `SetInteractable` com `Hint` está presente |
| NPC é hostil | Atitude ou template errado | Certifique-se de que `DefaultPlayerAttitude` é `"Neutral"` e `Type` é `"Generic"` |
| Troca mostra itens errados | Erro de digitação em `ItemId` | Verifique se `Plant_Fruit_Enchanted` e `Plant_Sapling_Enchanted` correspondem aos nomes reais dos arquivos de itens |
| Loja nunca reabastece | `RefreshInterval` ausente | Adicione `"RefreshInterval": { "Days": 2 }` à definição da loja |

---

## Referência de Lojas de Troca Vanilla

| Arquivo Vanilla | Padrão | Trocas |
|----------------|--------|--------|
| `Kweebec_Merchant.json` | 3 Fixed + 2 grupos Pool | Especiarias, Sal, Massa (fixo) + comidas e receitas (rotativo) |
| `Klops_Merchant.json` | 1 Fixed | Uma única troca de placa de construção |

---

## Próximos Passos

- [Spawn de NPCs Personalizados](/hytale-modding-docs/pt-br/tutorials/intermediate/custom-npc-spawning/) — posicione seu mercador em locais específicos do mundo
- [Criar uma Bancada de Trabalho](/hytale-modding-docs/pt-br/tutorials/intermediate/create-a-crafting-bench/) — permita que jogadores fabriquem itens para trocar com o mercador
- [Referência de Tabelas de Drop](/hytale-modding-docs/pt-br/reference/economy-and-progression/drop-tables/) — configure quais itens dropam como material de troca
