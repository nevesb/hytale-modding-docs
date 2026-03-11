---
title: Tipos de Recurso
description: Referência para arquivos JSON de tipos de recurso no Hytale, que definem categorias nomeadas de ingredientes usados como entradas flexíveis de receitas.
---

## Visão Geral

Tipos de recurso são categorias nomeadas de ingredientes que permitem que receitas de fabricação aceitem qualquer item pertencente a um grupo em vez de exigir um ID de item específico. Por exemplo, uma receita com `ResourceTypeId: "Meats"` vai aceitar qualquer item marcado com o tipo de recurso `Meats`. Itens declaram sua participação em tipos de recurso pelo array `ResourceTypes` em sua definição de item.

## Localização dos Arquivos

```
Assets/Server/Item/ResourceTypes/<ResourceTypeId>.json
```

## Schema

Arquivos de tipo de recurso são mínimos. A maioria contém apenas um caminho de ícone; a lista de membros é definida no lado do item via `ResourceTypes` em cada definição de item.

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `Icon` | string | Não | — | Caminho para a imagem do ícone exibida na UI de receita para representar este tipo de recurso (ex.: `"Icons/ResourceTypes/Any_Meat.png"`). |

## Tipos de Recurso Disponíveis (Lista Parcial)

| ID do Tipo de Recurso | Ícone |
|-----------------------|-------|
| `Bone` | `Icons/ResourceTypes/Any_Bone.png` |
| `Books` | — |
| `Bricks` | — |
| `Charcoal` | — |
| `Clays` | — |
| `Copper_Iron_Bar` | — |
| `Fish` | — |
| `Fish_Common` | — |
| `Fish_Epic` | — |
| `Fish_Legendary` | — |
| `Fish_Rare` | — |
| `Fish_Uncommon` | — |
| `Flowers` | — |
| `Foods` | — |
| `Fruits` | — |
| `Fuel` | `Icons/ResourceTypes/Fuel.png` |
| `Ice` | — |
| `Meats` | `Icons/ResourceTypes/Any_Meat.png` |
| `Metal_Bars` | `Icons/ResourceTypes/Rock.png` |
| `Milk_Bucket` | — |
| `Moss` | — |
| `Mushrooms` | — |
| `Rock` | — |
| `Rubble` | — |
| `Salvage_*` | — |
| `Sands` | — |
| `Soils` | — |
| `Vegetables` | — |
| `Wood_All` | — |
| `Wood_Trunk` | — |

## Exemplos

`Assets/Server/Item/ResourceTypes/Meats.json`:

```json
{
  "Icon": "Icons/ResourceTypes/Any_Meat.png"
}
```

`Assets/Server/Item/ResourceTypes/Fuel.json`:

```json
{
  "Icon": "Icons/ResourceTypes/Fuel.png"
}
```

`Assets/Server/Item/ResourceTypes/Foods.json`:

```json
{}
```

## Como Itens Declaram Participação em Tipos de Recurso

Na definição de um item, adicione um array `ResourceTypes` com uma entrada por tipo ao qual o item pertence:

```json
{
  "ResourceTypes": [
    { "Id": "Meats" }
  ]
}
```

Um item pode pertencer a múltiplos tipos de recurso. Por exemplo, `Food_Fish_Raw` pertence tanto a `Fish` quanto aos tipos de comida do template pai.

## Como Receitas Referenciam Tipos de Recurso

Em uma entrada `Input` de receita, use `ResourceTypeId` em vez de `ItemId`:

```json
{
  "Recipe": {
    "Input": [
      {
        "ResourceTypeId": "Fuel",
        "Quantity": 3
      },
      {
        "ResourceTypeId": "Fish",
        "Quantity": 1
      }
    ]
  }
}
```

Isso permite que a receita aceite qualquer item marcado com o tipo de recurso correspondente, em vez de exigir um item específico.

## Páginas Relacionadas

- [Definições de Itens](/hytale-modding-docs/reference/item-system/item-definitions) — Onde a participação em `ResourceTypes` é declarada nos itens
- [Grupos de Itens](/hytale-modding-docs/reference/item-system/item-groups) — Conjuntos nomeados de blocos (sistema de agrupamento complementar)
- [Categorias de Itens](/hytale-modding-docs/reference/item-system/item-categories) — Hierarquia de categorias de UI para menus
