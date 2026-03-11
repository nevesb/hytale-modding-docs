---
title: Tabelas de Drop
description: Referência para definições de tabelas de drop no Hytale, cobrindo tipos de contêiner, entradas de itens, pesos e estruturas de contêineres aninhados.
---

## Visão Geral

As tabelas de drop definem quais itens são produzidos quando um contêiner é aberto, um NPC é eliminado ou um nó de recurso é coletado. O sistema usa uma estrutura recursiva de `Container` que suporta três modos de seleção: `Single` (sempre produz um item), `Choice` (escolhe aleatoriamente um filho por peso) e `Multiple` (avalia todos os filhos). Aninhar esses tipos permite criar tabelas de loot ponderadas complexas com drops garantidos e opcionais.

## Como as Tabelas de Drop Funcionam

```mermaid
flowchart TD
    A[NPC Dies / Block Breaks] --> B[Lookup Drop Table]
    B --> C{Container Type?}

    C -->|"Multiple"| D[Evaluate ALL Children]
    C -->|"Choice"| E[Pick ONE by Weight]
    C -->|"Single"| F[Always Drop This Item]

    D --> G["Child 1: Guaranteed<br/>Single → 3x Bone"]
    D --> H["Child 2: Random Loot<br/>Choice → Weighted Pool"]

    H --> I{Roll Weights}
    I -->|"Weight: 60"| J["Common:<br/>5x Stone"]
    I -->|"Weight: 30"| K["Uncommon:<br/>1x Iron"]
    I -->|"Weight: 10"| L["Rare:<br/>1x Diamond"]

    G --> M[Final Drops]
    J --> M
    K --> M
    L --> M

    style A fill:#8b2500,color:#fff
    style M fill:#2d5a27,color:#fff
    style L fill:#8b6500,color:#fff
```

### Exemplo de Aninhamento de Contêineres

```mermaid
flowchart TD
    A[Root: Multiple] --> B["Single<br/>1x XP Orb<br/>Guaranteed"]
    A --> C["Choice<br/>Weighted random"]
    A --> D["Choice<br/>Weighted random"]

    C -->|"70%"| E[Nothing]
    C -->|"30%"| F[1x Feather]

    D -->|"90%"| G[Nothing]
    D -->|"10%"| H[1x Rare Egg]

    style B fill:#2d5a27,color:#fff
    style F fill:#2d6a8f,color:#fff
    style H fill:#8b6500,color:#fff
```

## Localização dos Arquivos

```
Assets/Server/Drops/
  Items/          (contêineres do mundo: barris, potes, caixões)
  NPCs/
    Beast/
    Boss/
    Critter/
    Elemental/
    Flying_Beast/
    Flying_Critter/
    Flying_Wildlife/
    Intelligent/
    Inventory/
  Objectives/
  Plant/
  Rock/
  Wood/
```

## Schema

### Nível superior

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Container` | `Container` | Sim | — | Nó contêiner raiz que define a lógica de loot. |

### Container

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Type` | `"Single" \| "Multiple" \| "Choice" \| "Empty"` | Sim | — | Modo de seleção para este nó contêiner. |
| `Item` | `ItemEntry` | Não | — | O item a ser produzido. Válido apenas quando `Type` é `"Single"`. |
| `Containers` | `Container[]` | Não | — | Contêineres filhos. Usado pelos tipos `Multiple` e `Choice`. |
| `Weight` | `number` | Não | — | Peso de probabilidade relativa. Usado por contêineres pai `Choice` ao selecionar entre irmãos. |

### Tipos de Container

| Type | Comportamento |
|------|---------------|
| `Single` | Sempre produz exatamente o item definido em `Item`. |
| `Multiple` | Avalia cada contêiner filho independentemente e combina todos os resultados. |
| `Choice` | Seleciona aleatoriamente um contêiner filho ponderado pelo campo `Weight` de cada filho. |
| `Empty` | Não produz nada. Usado como opção ponderada de "sem drop" dentro de nós `Choice`. |

### ItemEntry

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `ItemId` | `string` | Sim | — | ID do item a ser produzido. |
| `QuantityMin` | `number` | Sim | — | Tamanho mínimo da pilha produzida. |
| `QuantityMax` | `number` | Sim | — | Tamanho máximo da pilha produzida. A quantidade real é escolhida uniformemente entre min e max. |

## Exemplos

**Contêiner do mundo com drops de escolha ponderada** (`Assets/Server/Drops/Items/Barrels.json`):

```json
{
  "Container": {
    "Type": "Choice",
    "Containers": [
      {
        "Type": "Choice",
        "Weight": 100,
        "Containers": [
          {
            "Type": "Single",
            "Item": {
              "ItemId": "Plant_Fruit_Apple",
              "QuantityMin": 1,
              "QuantityMax": 1
            }
          }
        ]
      },
      {
        "Type": "Choice",
        "Weight": 25,
        "Containers": [
          {
            "Type": "Single",
            "Item": {
              "ItemId": "Weapon_Arrow_Crude",
              "QuantityMin": 1,
              "QuantityMax": 5
            }
          }
        ]
      },
      {
        "Type": "Empty",
        "Weight": 800
      }
    ]
  }
}
```

**Drop de NPC com múltiplos drops garantidos** (`Assets/Server/Drops/NPCs/Beast/Drop_Bear_Grizzly.json`):

```json
{
  "Container": {
    "Type": "Multiple",
    "Containers": [
      {
        "Type": "Choice",
        "Weight": 100,
        "Containers": [
          {
            "Type": "Single",
            "Item": {
              "ItemId": "Ingredient_Hide_Heavy",
              "QuantityMin": 1,
              "QuantityMax": 2
            }
          }
        ]
      },
      {
        "Type": "Choice",
        "Weight": 100,
        "Containers": [
          {
            "Type": "Single",
            "Item": {
              "ItemId": "Food_Wildmeat_Raw",
              "QuantityMin": 2,
              "QuantityMax": 3
            }
          }
        ]
      }
    ]
  }
}
```

O `Multiple` raiz garante que o urso sempre dropa tanto couro quanto carne. Cada filho usa um `Choice` com peso 100 (a única opção não vazia), tornando cada drop individual garantido.

## Páginas Relacionadas

- [Lojas de Troca](/hytale-modding-docs/reference/economy-and-progression/barter-shops) — slots de troca de mercadores
- [Fazendas e Galinheiros](/hytale-modding-docs/reference/economy-and-progression/farming-coops) — o campo `ProduceDrops` referencia IDs de tabelas de drop
- [Receitas](/hytale-modding-docs/reference/crafting-system/recipes) — crafting como alternativa aos drops
