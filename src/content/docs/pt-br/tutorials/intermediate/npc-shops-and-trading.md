---
title: Lojas de NPCs e Comércio
description: Tutorial passo a passo para configurar lojas de troca de NPCs com slots de comércio fixos e baseados em pool, limites de estoque e intervalos de reabastecimento.
sidebar:
  order: 3
---

## Objetivo

Criar um NPC mercador personalizado com uma **loja de troca** que oferece tanto trocas fixas (sempre disponíveis) quanto trocas aleatórias de pool (estoque rotativo). Você construirá a definição da loja, configurará limites de estoque e intervalos de reabastecimento, e conectará a loja a uma função de NPC.

## O Que Você Vai Aprender

- Como definições de lojas de troca controlam inventários de comércio de NPCs
- Como slots de comércio `Fixed` oferecem trocas consistentes e sempre disponíveis
- Como slots de comércio `Pool` criam seleções aleatórias rotativas com pesos
- Como `Stock`, `RefreshInterval` e `RestockHour` gerenciam inventário e resets
- Como conectar uma loja a uma função de NPC

## Pré-requisitos

- Uma pasta de mod com um `manifest.json` válido (veja [Configurar Seu Ambiente de Desenvolvimento](/hytale-modding-docs/pt-br/tutorials/beginner/setup-dev-environment))
- Uma função de NPC personalizada (veja [Criar um NPC Personalizado](/hytale-modding-docs/pt-br/tutorials/beginner/create-an-npc))

---

## Visão Geral da Loja de Troca

Lojas de troca ficam em `Assets/Server/BarterShops/`. Cada loja é um arquivo JSON que define o que um NPC mercador vende e compra. O jogo vanilla inclui lojas como `Kweebec_Merchant.json` (com trocas fixas e baseadas em pool) e `Klops_Merchant.json` (com uma única troca fixa).

O Hytale usa um sistema de **troca** em vez de um sistema de moeda -- jogadores trocam itens diretamente por outros itens. Cada troca tem um `Input` (o que o jogador paga) e um `Output` (o que o jogador recebe).

---

## Passo 1: Criar a Definição da Loja

Crie seu arquivo de loja em:

```
YourMod/Assets/Server/BarterShops/Crystal_Merchant.json
```

```json
{
  "DisplayNameKey": "server.barter.crystal_merchant.title",
  "RefreshInterval": {
    "Days": 2
  },
  "RestockHour": 6,
  "TradeSlots": [
    {
      "Type": "Fixed",
      "Trade": {
        "Output": { "ItemId": "Ingredient_Crystal_Cyan", "Quantity": 5 },
        "Input": [{ "ItemId": "Ingredient_Life_Essence", "Quantity": 25 }],
        "Stock": 20
      }
    },
    {
      "Type": "Fixed",
      "Trade": {
        "Output": { "ItemId": "Ingredient_Bar_Iron", "Quantity": 2 },
        "Input": [{ "ItemId": "Ingredient_Crystal_Cyan", "Quantity": 10 }],
        "Stock": 10
      }
    },
    {
      "Type": "Pool",
      "SlotCount": 3,
      "Trades": [
        {
          "Weight": 40,
          "Output": { "ItemId": "Food_Kebab_Meat", "Quantity": 1 },
          "Input": [{ "ItemId": "Ingredient_Crystal_Cyan", "Quantity": 3 }],
          "Stock": [4, 8]
        },
        {
          "Weight": 30,
          "Output": { "ItemId": "Food_Pie_Apple", "Quantity": 1 },
          "Input": [{ "ItemId": "Ingredient_Crystal_Cyan", "Quantity": 5 }],
          "Stock": [3, 6]
        },
        {
          "Weight": 20,
          "Output": { "ItemId": "Weapon_Sword_Crystal", "Quantity": 1 },
          "Input": [{ "ItemId": "Ingredient_Crystal_Cyan", "Quantity": 30 }],
          "Stock": [1, 2]
        },
        {
          "Weight": 20,
          "Output": { "ItemId": "Armor_Crystal_Chest", "Quantity": 1 },
          "Input": [{ "ItemId": "Ingredient_Crystal_Cyan", "Quantity": 40 }],
          "Stock": [1, 2]
        },
        {
          "Weight": 10,
          "Output": { "ItemId": "Rune_Fire", "Quantity": 1 },
          "Input": [{ "ItemId": "Ingredient_Crystal_Cyan", "Quantity": 50 }],
          "Stock": [1]
        }
      ]
    },
    {
      "Type": "Pool",
      "SlotCount": 2,
      "Trades": [
        {
          "Weight": 30,
          "Output": { "ItemId": "Recipe_Food_Pie_Apple", "Quantity": 1 },
          "Input": [{ "ItemId": "Ingredient_Life_Essence_Concentrated", "Quantity": 2 }],
          "Stock": [1]
        },
        {
          "Weight": 30,
          "Output": { "ItemId": "Recipe_Food_Pie_Pumpkin", "Quantity": 1 },
          "Input": [{ "ItemId": "Ingredient_Life_Essence_Concentrated", "Quantity": 2 }],
          "Stock": [1]
        },
        {
          "Weight": 20,
          "Output": { "ItemId": "Recipe_Food_Pie_Meat", "Quantity": 1 },
          "Input": [{ "ItemId": "Ingredient_Life_Essence_Concentrated", "Quantity": 3 }],
          "Stock": [1]
        }
      ]
    }
  ]
}
```

### Campos de nível superior da loja

| Campo | Finalidade |
|-------|-----------|
| `DisplayNameKey` | Chave de tradução para o título da loja mostrado na interface de comércio |
| `RefreshInterval.Days` | Número de dias no jogo entre reabastecimentos de estoque. O Mercador Kweebec usa 3 dias, Klops usa 1 dia |
| `RestockHour` | Hora do dia (0-24) quando o reabastecimento acontece. `6` = 6h |
| `TradeSlots` | Array de definições de slots de comércio. Cada slot é `Fixed` ou `Pool` |

---

## Passo 2: Entendendo Slots de Comércio Fixos

Slots fixos sempre aparecem na interface da loja e oferecem a mesma troca a cada ciclo de reabastecimento.

```json
{
  "Type": "Fixed",
  "Trade": {
    "Output": { "ItemId": "Ingredient_Crystal_Cyan", "Quantity": 5 },
    "Input": [{ "ItemId": "Ingredient_Life_Essence", "Quantity": 25 }],
    "Stock": 20
  }
}
```

### Campos de troca fixa

| Campo | Finalidade |
|-------|-----------|
| `Type` | Deve ser `"Fixed"` |
| `Trade.Output` | O item e quantidade que o jogador recebe |
| `Trade.Input` | Array de itens que o jogador deve pagar. Múltiplas entradas requerem todos os itens |
| `Trade.Stock` | Número de vezes que esta troca pode ser completada antes do slot ficar vazio. Reabastecido no intervalo de atualização |

### Múltiplos itens de entrada

Uma troca pode requerer múltiplos itens diferentes como pagamento:

```json
"Input": [
  { "ItemId": "Ingredient_Crystal_Cyan", "Quantity": 10 },
  { "ItemId": "Ingredient_Life_Essence", "Quantity": 5 }
]
```

O jogador deve fornecer ambos os itens para completar a troca.

---

## Passo 3: Entendendo Slots de Comércio Pool

Slots pool selecionam aleatoriamente um subconjunto de trocas de um pool maior em cada reabastecimento. Isso cria um inventário rotativo que incentiva os jogadores a voltar regularmente.

```json
{
  "Type": "Pool",
  "SlotCount": 3,
  "Trades": [
    {
      "Weight": 40,
      "Output": { "ItemId": "Food_Kebab_Meat", "Quantity": 1 },
      "Input": [{ "ItemId": "Ingredient_Crystal_Cyan", "Quantity": 3 }],
      "Stock": [4, 8]
    },
    {
      "Weight": 10,
      "Output": { "ItemId": "Rune_Fire", "Quantity": 1 },
      "Input": [{ "ItemId": "Ingredient_Crystal_Cyan", "Quantity": 50 }],
      "Stock": [1]
    }
  ]
}
```

### Campos de troca pool

| Campo | Finalidade |
|-------|-----------|
| `Type` | Deve ser `"Pool"` |
| `SlotCount` | Número de trocas selecionadas aleatoriamente do pool em cada reabastecimento. Deve ser menor ou igual ao número total de trocas no pool |
| `Trades` | Array de trocas possíveis para escolher |
| `Trades[].Weight` | Probabilidade relativa desta troca ser selecionada. Peso maior = mais provável de aparecer. O Mercador Kweebec usa pesos de 20 a 50 |
| `Trades[].Stock` | Para trocas pool, este é um array: `[fixo]` para estoque exato ou `[mín, máx]` para quantidade de estoque aleatória |

### Estoque como array

Em trocas pool, `Stock` usa formato de array:

| Formato | Significado |
|---------|------------|
| `[1]` | Exatamente 1 em estoque por reabastecimento |
| `[4, 8]` | Estoque aleatório entre 4 e 8 por reabastecimento |
| `[10, 20]` | Estoque aleatório entre 10 e 20 por reabastecimento |

Compare com trocas fixas onde `Stock` é um inteiro simples.

---

## Passo 4: Conectar a Loja a uma Função de NPC

A loja de troca é conectada a uma definição de função de NPC. A função de NPC deve referenciar o arquivo da loja. Na sua função de NPC:

```
YourMod/Assets/Server/NPC/Roles/MyMod/Crystal_Merchant.json
```

```json
{
  "Type": "Variant",
  "Reference": "Template_Intelligent",
  "Modify": {
    "Appearance": "Kweebec_Elder",
    "MaxHealth": 100,
    "BarterShop": "Crystal_Merchant",
    "NameTranslationKey": {
      "Compute": "NameTranslationKey"
    }
  },
  "Parameters": {
    "NameTranslationKey": {
      "Value": "server.npcRoles.Crystal_Merchant.name",
      "Description": "Translation key for NPC name"
    }
  }
}
```

O campo `BarterShop` referencia o arquivo da loja pelo nome (sem `.json`). O engine resolve isto de `Assets/Server/BarterShops/`.

---

## Passo 5: Adicionar Chaves de Tradução

```
YourMod/Assets/Languages/en-US.lang
```

```
server.barter.crystal_merchant.title=Crystal Merchant
server.npcRoles.Crystal_Merchant.name=Crystal Merchant
```

---

## Passo 6: Testar No Jogo

1. Coloque sua pasta de mod no diretório de mods do servidor.
2. Inicie o servidor e observe erros sobre IDs de loja de troca desconhecidos ou referências de itens inválidas.
3. Gere o NPC Mercador de Cristal usando o gerador de desenvolvedor.
4. Clique com o botão direito no NPC para abrir a interface de comércio.
5. Verifique que slots de comércio fixos aparecem com os itens, quantidades e estoque corretos.
6. Verifique que slots de comércio pool mostram `SlotCount` trocas selecionadas aleatoriamente.
7. Compre itens até o estoque acabar e confirme que o slot aparece como vazio.
8. Avance o tempo além do `RefreshInterval` e `RestockHour`, depois reabra a loja.
9. Confirme que slots fixos foram reabastecidos e slots pool foram re-randomizados.

**Erros comuns e correções:**

| Erro | Causa | Correção |
|------|-------|----------|
| `Unknown barter shop` | Valor de `BarterShop` não corresponde ao nome do arquivo | Certifique-se de que o valor corresponda exatamente ao nome do arquivo JSON sem `.json` |
| Interface da loja está vazia | Array `TradeSlots` está vazio ou malformado | Verifique a estrutura JSON com pelo menos um slot de comércio |
| Pool mostra menos trocas que o esperado | `SlotCount` excede as trocas disponíveis | Certifique-se de que `SlotCount` é menor ou igual ao número de entradas em `Trades` |
| Troca não pode ser completada | IDs de item em `Input` estão errados | Verifique se todos os valores de `ItemId` correspondem a definições reais de itens |
| Loja nunca reabastece | `RefreshInterval` não definido | Adicione `"RefreshInterval": { "Days": 1 }` |

---

## Dicas de Design

- **Slots fixos** funcionam bem para itens básicos que jogadores sempre precisam (materiais básicos, comida)
- **Slots pool** funcionam bem para itens raros, equipamentos e receitas que criam empolgação quando aparecem
- Use múltiplos grupos pool para criar diferentes níveis de raridade (pool de comida comum vs pool de receitas raras)
- Mantenha valores de `Stock` baixos para itens poderosos para impedir jogadores de comprar quantidades ilimitadas
- Defina valores de `Weight` proporcionais à frequência que deseja que cada troca apareça. O Mercador Kweebec usa pesos de 20 (receitas raras) a 50 (cultivos comuns)

---

## Próximos Passos

- [Criar um NPC Personalizado](/hytale-modding-docs/pt-br/tutorials/beginner/create-an-npc) -- construa a função de NPC que hospeda sua loja
- [Tabelas de Loot Personalizadas](/hytale-modding-docs/pt-br/tutorials/intermediate/custom-loot-tables) -- configure drops para itens que sua loja vende
- [Criar uma Bancada de Trabalho](/hytale-modding-docs/pt-br/tutorials/intermediate/create-a-crafting-bench) -- permita que jogadores fabriquem os itens que seu mercador troca
