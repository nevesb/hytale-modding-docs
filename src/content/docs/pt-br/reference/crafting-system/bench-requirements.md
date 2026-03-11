---
title: Requisitos de Bancada
description: Referencia para o campo BenchRequirement em receitas do Hytale, que vincula receitas de fabricacao a bancadas, categorias e niveis de tier especificos.
---

## Visao Geral

O campo `BenchRequirement` em uma receita determina com qual bancada de fabricacao o jogador deve interagir para fabricar aquele item. Ele conecta o sistema de receitas ao sistema de bancadas especificando um ID de bancada, tipo de bancada, um ou mais filtros de categoria e um nivel de tier opcional. Uma receita pode listar varios requisitos de bancada, permitindo que apareca em mais de uma bancada. Receitas sem `BenchRequirement` (ou com requisito `Fieldcraft`) podem ser fabricadas a partir do inventario do jogador sem uma bancada colocada.

## Localizacao dos Arquivos

Os requisitos de bancada aparecem inline dentro das definicoes de receitas:

```
Assets/Server/Item/Items/Bench/*.json     (incorporado em Recipe.BenchRequirement)
Assets/Server/Item/Items/**/*.json        (qualquer item com uma Recipe inline)
Assets/Server/Item/Recipes/**/*.json      (arquivos de receita independentes)
```

Os proprios itens de bancada estao em:

```
Assets/Server/Item/Items/Bench/
  Bench_Alchemy.json
  Bench_Arcane.json
  Bench_Armory.json
  Bench_Armour.json
  Bench_Builders.json
  Bench_Campfire.json
  Bench_Cooking.json
  Bench_Farming.json
  Bench_Furnace.json
  Bench_Furniture.json
  Bench_Loom.json
  Bench_Lumbermill.json
  Bench_Memories.json
  Bench_Salvage.json
  Bench_Tannery.json
  Bench_Trough.json
  Bench_Weapon.json
  Bench_WorkBench.json
```

## Schema

### BenchRequirement (elemento do array)

| Campo | Tipo | Obrigatorio | Padrao | Descricao |
|-------|------|-------------|--------|-----------|
| `Id` | `string` | Sim | — | Identificador da bancada que deve corresponder ao `BlockType.Bench.Id` de uma bancada colocada. Valores conhecidos incluem `"Workbench"`, `"Cookingbench"`, `"Furnace"`, `"Campfire"`, `"Alchemybench"`, `"Loombench"`, `"Fieldcraft"`. |
| `Type` | `string` | Sim | — | Tipo operacional da bancada. Valores conhecidos: `"Crafting"` (selecao manual de receita), `"Processing"` (baseado em entrada com combustivel). |
| `Categories` | `string[]` | Nao | — | Lista de IDs de categorias da bancada a qual a receita pertence. Correspondem as abas `BlockType.Bench.Categories[].Id` mostradas na UI da bancada (ex: `"Workbench_Crafting"`, `"Prepared"`, `"Baked"`, `"Tools"`). |
| `RequiredTierLevel` | `number` | Nao | — | Nivel minimo de tier da bancada necessario para desbloquear esta receita. Os tiers comecam em `1` (bancada base); valores maiores requerem melhorias na bancada. |

### Como os IDs se conectam as definicoes de bancada

Cada item de bancada define um objeto `BlockType.Bench` com um campo `Id` e um array `Categories`. Quando uma receita especifica `BenchRequirement[].Id = "Workbench"`, o motor a associa a qualquer bancada colocada cujo `BlockType.Bench.Id` seja igual a `"Workbench"`. O array `Categories` no requisito determina em qual aba da UI da bancada a receita aparece.

```
Recipe.BenchRequirement[].Id  ──corresponde a──>  BlockType.Bench.Id
Recipe.BenchRequirement[].Categories  ──filtra──>  BlockType.Bench.Categories[].Id
```

## Exemplos

**Requisito basico de bancada de trabalho** (de `Bench_Cooking.json`):

```json
{
  "BenchRequirement": [
    {
      "Type": "Crafting",
      "Id": "Workbench",
      "Categories": [
        "Workbench_Crafting"
      ]
    }
  ]
}
```

A propria bancada de culinaria deve ser fabricada em uma bancada de trabalho, na aba de categoria "Crafting".

**Requisito com restricao de tier** (de `Bench_Alchemy.json`):

```json
{
  "BenchRequirement": [
    {
      "Id": "Workbench",
      "Type": "Crafting",
      "Categories": [
        "Workbench_Crafting"
      ],
      "RequiredTierLevel": 2
    }
  ]
}
```

A bancada de alquimia requer uma bancada de trabalho de tier 2 (melhorada) para ser fabricada.

**Requisitos multiplos de bancada** (de `Bench_Campfire.json`):

```json
{
  "BenchRequirement": [
    {
      "Type": "Crafting",
      "Categories": [
        "Tools"
      ],
      "Id": "Fieldcraft"
    },
    {
      "Id": "Workbench",
      "Type": "Crafting",
      "Categories": [
        "Workbench_Survival"
      ]
    }
  ]
}
```

A receita de fogueira aparece em dois locais: o menu de fabricacao de campo do jogador (em "Tools") e a UI da bancada de trabalho (em "Survival"). Isso permite ao jogador fabrica-la em qualquer estacao.

**Receita sem requisito de bancada** (de `Bench_Loom.json`):

```json
{
  "Recipe": {
    "Input": [
      { "Quantity": 5, "ResourceTypeId": "Wood_Trunk" },
      { "ItemId": "Ingredient_Fabric_Scrap_Cotton", "Quantity": 3 }
    ]
  }
}
```

Quando `BenchRequirement` e totalmente omitido, a receita pode ser fabricada sem qualquer bancada.

## Paginas Relacionadas

- [Definicoes de Bancadas](/pt-br/hytale-modding-docs/reference/crafting-system/bench-definitions) — schema completo do item de bancada incluindo configuracao `BlockType.Bench` e melhorias de tier
- [Receitas](/pt-br/hytale-modding-docs/reference/crafting-system/recipes) — schema de entrada/saida de receitas onde `BenchRequirement` e incorporado
- [Reciclagem](/pt-br/hytale-modding-docs/reference/crafting-system/salvage) — receitas de processamento da bancada de reciclagem
