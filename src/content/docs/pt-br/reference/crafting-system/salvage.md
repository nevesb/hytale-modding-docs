---
title: Reciclagem
description: Referencia para definicoes de receitas de reciclagem no Hytale, que desmontam itens em seus materiais constituintes em uma Bancada de Reciclagem.
---

## Visao Geral

Receitas de reciclagem definem como itens existentes sao desmontados em materiais brutos na Bancada de Reciclagem. Elas usam o mesmo schema base de receita que receitas de fabricacao, mas sempre tem exatamente um item de entrada, multiplas saidas e um `BenchRequirement` apontando para a bancada de processamento `"Salvagebench"`. O campo `PrimaryOutput` identifica o material recuperado mais valioso mostrado na UI.

## Localizacao dos Arquivos

```
Assets/Server/Item/Recipes/Salvage/
```

Um arquivo JSON por item reciclavel, nomeado `Salvage_<ItemId>.json`, ex: `Salvage_Armor_Adamantite_Chest.json`.

## Schema

Receitas de reciclagem compartilham o [schema completo de receitas](/pt-br/hytale-modding-docs/reference/crafting-system/recipes). Os campos usados na pratica sao:

| Campo | Tipo | Obrigatorio | Padrao | Descricao |
|-------|------|-------------|--------|-----------|
| `Input` | `InputEntry[]` | Sim | — | Array de elemento unico identificando o item a reciclar. Sempre usa `ItemId`. |
| `Input[].ItemId` | `string` | Sim | — | O ID do item sendo reciclado. |
| `Input[].Quantity` | `number` | Sim | — | Sempre `1` para reciclagem. |
| `PrimaryOutput` | `OutputEntry` | Sim | — | O material recuperado principal mostrado como resultado destaque na UI. |
| `PrimaryOutput.ItemId` | `string` | Sim | — | ID do item do material recuperado principal. |
| `PrimaryOutput.Quantity` | `number` | Sim | — | Quantidade do material principal recuperado. |
| `Output` | `OutputEntry[]` | Sim | — | Lista completa de todos os materiais recuperados, incluindo a saida principal e quaisquer materiais secundarios. |
| `Output[].ItemId` | `string` | Sim | — | ID do item do material recuperado. |
| `Output[].Quantity` | `number` | Sim | — | Quantidade recuperada. |
| `BenchRequirement` | `BenchRequirement[]` | Sim | — | Sempre `[{ "Type": "Processing", "Id": "Salvagebench" }]`. |
| `TimeSeconds` | `number` | Sim | — | Tempo de processamento em segundos na Bancada de Reciclagem. |

## Exemplos

**Peitoral de adamantita** (`Salvage_Armor_Adamantite_Chest.json`):

```json
{
  "Input": [
    {
      "ItemId": "Armor_Adamantite_Chest",
      "Quantity": 1
    }
  ],
  "PrimaryOutput": {
    "ItemId": "Ore_Adamantite",
    "Quantity": 6
  },
  "Output": [
    {
      "ItemId": "Ore_Adamantite",
      "Quantity": 6
    },
    {
      "ItemId": "Ingredient_Hide_Heavy",
      "Quantity": 2
    },
    {
      "ItemId": "Ingredient_Fabric_Scrap_Cindercloth",
      "Quantity": 2
    }
  ],
  "BenchRequirement": [
    {
      "Type": "Processing",
      "Id": "Salvagebench"
    }
  ],
  "TimeSeconds": 4
}
```

**Peitoral de tecido de algodao** (`Salvage_Armor_Cloth_Cotton_Chest.json`):

```json
{
  "Input": [
    {
      "ItemId": "Armor_Cloth_Cotton_Chest",
      "Quantity": 1
    }
  ],
  "PrimaryOutput": {
    "ItemId": "Ingredient_Fabric_Scrap_Cotton",
    "Quantity": 4
  },
  "Output": [
    {
      "ItemId": "Ingredient_Fabric_Scrap_Cotton",
      "Quantity": 4
    }
  ],
  "BenchRequirement": [
    {
      "Type": "Processing",
      "Id": "Salvagebench"
    }
  ],
  "TimeSeconds": 2
}
```

## Paginas Relacionadas

- [Receitas](/pt-br/hytale-modding-docs/reference/crafting-system/recipes) — schema base de receitas
- [Definicoes de Bancadas](/pt-br/hytale-modding-docs/reference/crafting-system/bench-definitions) — definicao do item Bancada de Reciclagem
