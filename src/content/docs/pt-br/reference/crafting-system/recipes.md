---
title: Receitas
description: Referencia para definicoes de receitas de fabricacao no Hytale, incluindo entradas, saidas, requisitos de bancada e tempo de processamento.
---

## Visao Geral

Receitas de fabricacao definem a transformacao de itens ou recursos de entrada em itens de saida. Cada receita especifica quais materiais sao consumidos, o que e produzido, qual bancada (se alguma) deve estar presente e quanto tempo a fabricacao leva. As receitas ficam em `Assets/Server/Item/Recipes/` e sao carregadas pelo sistema de itens em tempo de execucao.

## Como a Fabricacao Funciona

```mermaid
flowchart TD;
    A["Jogador Abre<br>Bancada de Fabricacao"] --> B[Mostrar Receitas Disponiveis];
    B --> C["Possui Materiais<br>Necessarios?"];
    C -->|"Nao"| D[Receita Indisponivel];
    C -->|"Sim"| E[Jogador Clica em Fabricar];

    E --> F["Bancada Corresponde<br>ao Requisito da Receita?"];
    F -->|"Nao"| D;
    F -->|"Sim"| G[Consumir Entradas];

    G --> H["ProcessingTime > 0?"];
    H -->|"Sim"| I["Aguardar Temporizador<br>ex: 5 segundos"];
    H -->|"Nao"| J[Fabricacao Instantanea];

    I --> K[Produzir Itens de Saida];
    J --> K;

    K --> L["Adicionar ao Inventario<br>ou Derrubar"];

    style A fill:darkgreen,color:white;
    style D fill:darkred,color:white;
    style K fill:rebeccapurple,color:white;```

### Resolucao de Receitas com Grupos

```mermaid
flowchart LR;
    A["Entrada da Receita:<br>Grupo 'AnyWood' x4"] --> B{Jogador Possui?};
    B -->|"Madeira de Carvalho x4"| C[Valido];
    B -->|"Madeira de Betula x2<br>+ Madeira de Pinho x2"| D["Valido<br>Itens mistos do grupo"];
    B -->|"Pedra x4"| E["Invalido<br>Nao esta no grupo"];

    style C fill:darkgreen,color:white;
    style D fill:darkgreen,color:white;
    style E fill:darkred,color:white;```

## Localizacao dos Arquivos

```
Assets/Server/Item/Recipes/
```

Receitas de reciclagem estao no subdiretorio:

```
Assets/Server/Item/Recipes/Salvage/
```

Alguns itens incorporam sua propria receita diretamente no arquivo de definicao do item em `Assets/Server/Item/Items/` usando o mesmo schema.

## Schema

### Campos de nivel superior

| Campo | Tipo | Obrigatorio | Padrao | Descricao |
|-------|------|-------------|--------|-----------|
| `Input` | `InputEntry[]` | Sim | — | Lista de itens ou tipos de recurso consumidos pela receita. |
| `Output` | `OutputEntry[]` | Nao | — | Lista completa de todos os itens produzidos. Quando omitido, o item que carrega a receita e a unica saida. |
| `PrimaryOutput` | `OutputEntry` | Nao | — | A saida "principal" mostrada na UI de fabricacao quando existem multiplas saidas. |
| `BenchRequirement` | `BenchRequirement[]` | Nao | `[]` | Bancadas (ou fabricacao de campo) necessarias para realizar a fabricacao. |
| `TimeSeconds` | `number` | Nao | `0` | Quantos segundos do mundo real a fabricacao leva. |

### InputEntry

| Campo | Tipo | Obrigatorio | Padrao | Descricao |
|-------|------|-------------|--------|-----------|
| `ItemId` | `string` | Nao¹ | — | ID especifico do item a consumir. Mutuamente exclusivo com `ResourceTypeId`. |
| `ResourceTypeId` | `string` | Nao¹ | — | Tag de recurso a consumir (ex: `"Wood_Trunk"`, `"Rock"`). Qualquer item marcado com este tipo de recurso satisfaz o slot. |
| `Quantity` | `number` | Sim | — | Numero de itens ou unidades de recurso consumidos. |

¹ Exatamente um entre `ItemId` ou `ResourceTypeId` deve estar presente por entrada.

### OutputEntry

| Campo | Tipo | Obrigatorio | Padrao | Descricao |
|-------|------|-------------|--------|-----------|
| `ItemId` | `string` | Sim | — | ID do item produzido. |
| `Quantity` | `number` | Nao | `1` | Tamanho da pilha do item produzido. |

### BenchRequirement

| Campo | Tipo | Obrigatorio | Padrao | Descricao |
|-------|------|-------------|--------|-----------|
| `Type` | `"Crafting" \| "Processing"` | Sim | — | Se a bancada e uma estacao de fabricacao ou processamento. |
| `Id` | `string` | Sim | — | O ID da bancada (ex: `"Workbench"`, `"Campfire"`, `"Fieldcraft"`). |
| `Categories` | `string[]` | Nao | — | Lista opcional de slots de categoria na bancada que devem estar ativos para esta receita aparecer. |

## Exemplo

**Receita de reciclagem** (`Assets/Server/Item/Recipes/Salvage/Salvage_Armor_Adamantite_Chest.json`):

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

**Receita inline em um arquivo de item** (de `Assets/Server/Item/Items/Bench/Bench_Campfire.json`):

```json
{
  "Recipe": {
    "TimeSeconds": 1,
    "Input": [
      { "ItemId": "Ingredient_Stick", "Quantity": 4 },
      { "ResourceTypeId": "Rubble", "Quantity": 2 }
    ],
    "BenchRequirement": [
      { "Type": "Crafting", "Categories": ["Tools"], "Id": "Fieldcraft" },
      { "Id": "Workbench", "Type": "Crafting", "Categories": ["Workbench_Survival"] }
    ]
  }
}
```

## Paginas Relacionadas

- [Definicoes de Bancadas](/pt-br/hytale-modding-docs/reference/crafting-system/bench-definitions) — como bancadas sao definidas e configuradas
- [Reciclagem](/pt-br/hytale-modding-docs/reference/crafting-system/salvage) — formato de receita especifico de reciclagem
- [Tabelas de Loot](/pt-br/hytale-modding-docs/reference/economy-and-progression/drop-tables) — loot de conteineres do mundo
