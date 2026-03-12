---
title: Tabelas de Loot Personalizadas
description: Tutorial passo a passo para criar tabelas de loot e drops com entradas ponderadas, contêineres aninhados e drops condicionais.
sidebar:
  order: 2
---

## Objetivo

Criar um conjunto de tabelas de loot personalizadas que demonstram toda a gama do sistema de drops do Hytale. Você construirá um drop garantido, um drop aleatório ponderado, uma tabela aninhada com equipamento raro e uma tabela de drops de colheita de recursos.

## O Que Você Vai Aprender

- Como os tipos de `Container` (`Multiple`, `Choice`, `Single`) funcionam juntos para criar lógica de drops
- Como `Weight` controla a probabilidade de drops aleatórios
- Como aninhar contêineres para tabelas de loot complexas com drops garantidos e raros
- Como `QuantityMin` e `QuantityMax` criam quantidades de drops variáveis
- Como as diferentes categorias de tabelas de drops (NPCs, Wood, Rock, Crop) são organizadas

## Pré-requisitos

- Uma pasta de mod com um `manifest.json` válido (veja [Configurar Seu Ambiente de Desenvolvimento](/hytale-modding-docs/pt-br/tutorials/beginner/setup-dev-environment))
- Pelo menos um item personalizado (veja [Criar um Item Personalizado](/hytale-modding-docs/pt-br/tutorials/beginner/create-an-item))

---

## Visão Geral do Sistema de Drops

As tabelas de drops ficam em `Assets/Server/Drops/` e são organizadas por tipo de origem:

```
Assets/Server/Drops/
  NPCs/
    Beast/
    Boss/
    Critter/
    Elemental/
    Intelligent/
      Feran/
      Goblin/
      Trork/
    Livestock/
    Undead/
    Void/
  Crop/
  Wood/
  Rock/
  Plant/
  Items/
  Prefabs/
  Traps/
```

Toda tabela de drops é um arquivo JSON com um objeto raiz `Container`. O sistema de contêineres usa três tipos que podem ser aninhados para criar qualquer lógica de drop.

### Tipos de contêiner

| Tipo | Comportamento |
|------|--------------|
| `Multiple` | Avalia **todos** os contêineres filhos em ordem. Cada filho é executado independentemente |
| `Choice` | Escolhe **um** filho aleatoriamente, ponderado pelos valores de `Weight` |
| `Single` | Nó terminal. Produz o `Item` especificado com uma quantidade aleatória entre `QuantityMin` e `QuantityMax` |

---

## Passo 1: Criar um Drop Garantido

A tabela de drops mais simples garante um ou mais itens toda vez. Este padrão é usado por `Rock_Crystal_Blue.json` para depósitos de cristal.

Crie:

```
YourMod/Assets/Server/Drops/NPCs/Beast/Drop_Thornbeast.json
```

```json
{
  "Container": {
    "Type": "Multiple",
    "Containers": [
      {
        "Type": "Single",
        "Item": {
          "ItemId": "Ingredient_Hide_Heavy",
          "QuantityMin": 2,
          "QuantityMax": 4
        }
      }
    ]
  }
}
```

Um contêiner `Multiple` com um único filho `Single` garante o drop toda vez. A quantidade é escolhida aleatoriamente entre `QuantityMin` e `QuantityMax` (inclusivo).

---

## Passo 2: Criar uma Tabela de Multi-Drops com Itens Garantidos

Este padrão -- usado por `Drop_Bear_Grizzly.json` -- garante múltiplos drops diferentes usando um contêiner `Multiple` com vários filhos:

```
YourMod/Assets/Server/Drops/NPCs/Beast/Drop_Crystalbeast.json
```

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

O contêiner `Multiple` executa ambos os grupos `Choice`. Como cada grupo `Choice` tem apenas uma opção com `Weight: 100`, ambos os itens são garantidos. Esta estrutura é usada em vez de dois contêineres `Single` simples porque o campo `Weight` nos contêineres `Choice` também controla se o grupo dropa -- um `Weight` de 100 significa 100% de chance.

---

## Passo 3: Criar um Drop Aleatório Ponderado com Loot Raro

Este padrão -- usado por `Drop_Trork_Warrior.json` -- combina drops garantidos com equipamento raro. O contêiner `Choice` escolhe um filho baseado em pesos relativos:

```
YourMod/Assets/Server/Drops/NPCs/Intelligent/Drop_Crystal_Guardian.json
```

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
              "ItemId": "Ingredient_Crystal_Cyan",
              "QuantityMin": 2,
              "QuantityMax": 5
            }
          }
        ]
      },
      {
        "Type": "Choice",
        "Weight": 15,
        "Containers": [
          {
            "Weight": 40,
            "Type": "Single",
            "Item": {
              "ItemId": "Armor_Crystal_Head",
              "QuantityMin": 1,
              "QuantityMax": 1
            }
          },
          {
            "Weight": 40,
            "Type": "Single",
            "Item": {
              "ItemId": "Armor_Crystal_Chest",
              "QuantityMin": 1,
              "QuantityMax": 1
            }
          },
          {
            "Weight": 20,
            "Type": "Single",
            "Item": {
              "ItemId": "Weapon_Sword_Crystal",
              "QuantityMin": 1,
              "QuantityMax": 1
            }
          }
        ]
      }
    ]
  }
}
```

### Como os pesos funcionam

O contêiner externo `Multiple` executa ambos os grupos:

1. **Grupo 1** (`Weight: 100`): Sempre dropa 2-5 cristais
2. **Grupo 2** (`Weight: 15`): 15% de chance de executar. Se executar, escolhe um item:
   - 40% de chance: Capacete de Cristal
   - 40% de chance: Peitoral de Cristal
   - 20% de chance: Espada de Cristal

Os valores internos de `Weight` são relativos entre si dentro do grupo `Choice`: 40 + 40 + 20 = 100 total, então a espada tem 20/100 = 20% de chance *quando o grupo é ativado*.

A chance geral de obter a espada em qualquer abate é: 15% (grupo ativa) x 20% (espada selecionada) = 3%.

---

## Passo 4: Criar uma Tabela de Drops Aninhada com Múltiplos Resultados

Para cenários complexos, aninhe `Multiple` dentro de `Choice` para criar resultados ramificados. Este padrão é usado por `Wood_Branch.json`:

```
YourMod/Assets/Server/Drops/Wood/Drop_Crystalwood_Branch.json
```

```json
{
  "Container": {
    "Type": "Choice",
    "Containers": [
      {
        "Type": "Multiple",
        "Weight": 60,
        "Containers": [
          {
            "Type": "Single",
            "Item": {
              "ItemId": "Ingredient_Stick",
              "QuantityMin": 1,
              "QuantityMax": 3
            }
          },
          {
            "Type": "Single",
            "Item": {
              "ItemId": "Ingredient_Crystal_Cyan",
              "QuantityMin": 0,
              "QuantityMax": 1
            }
          }
        ]
      },
      {
        "Type": "Multiple",
        "Weight": 40,
        "Containers": [
          {
            "Type": "Single",
            "Item": {
              "ItemId": "Ingredient_Stick"
            }
          }
        ]
      }
    ]
  }
}
```

Esta tabela tem dois resultados possíveis escolhidos pelo `Choice` externo:

- **60% de chance**: Dropa 1-3 gravetos E 0-1 cristais (ambos os itens do `Multiple`)
- **40% de chance**: Dropa apenas 1 graveto

Note que quando `QuantityMin` é 0, há uma chance do item não produzir nada. Quando `QuantityMin` e `QuantityMax` são omitidos, a quantidade padrão é 1.

---

## Passo 5: Criar uma Tabela de Drops Vazia

Alguns NPCs (como Esquilos e Sapos vanilla) não dropam nada. Um objeto vazio alcança isso:

```
YourMod/Assets/Server/Drops/NPCs/Critter/Drop_Glowfly.json
```

```json
{}
```

---

## Passo 6: Conectar a Tabela de Drops a um NPC

As tabelas de drops são referenciadas pelas definições de função de NPC através do campo `DropList`. O valor corresponde ao nome do arquivo sem `.json`, e o engine procura em todos os diretórios sob `Assets/Server/Drops/`.

No seu arquivo de função de NPC:

```json
{
  "Type": "Variant",
  "Reference": "Template_Predator",
  "Modify": {
    "Appearance": "Bear_Grizzly",
    "DropList": "Drop_Crystal_Guardian",
    "MaxHealth": 80
  }
}
```

O valor de `DropList` `"Drop_Crystal_Guardian"` resolve para `Assets/Server/Drops/NPCs/Intelligent/Drop_Crystal_Guardian.json`.

---

## Passo 7: Testar No Jogo

1. Coloque sua pasta de mod no diretório de mods do servidor.
2. Inicie o servidor e observe erros sobre IDs de lista de drops desconhecidos ou IDs de itens inválidos.
3. Gere o NPC que usa sua tabela de drops.
4. Mate o NPC múltiplas vezes e verifique:
   - Drops garantidos aparecem toda vez
   - Drops raros aparecem aproximadamente na frequência esperada
   - Quantidades ficam dentro das faixas mín/máx definidas
5. Para drops de recursos (madeira, pedra), quebre o bloco correspondente e verifique os drops.

**Erros comuns e correções:**

| Erro | Causa | Correção |
|------|-------|----------|
| `Unknown drop list` | Nome de arquivo ou diretório errado | Verifique se o arquivo de drop existe e `DropList` corresponde ao nome do arquivo sem `.json` |
| `Unknown item id` | Erro de digitação no ID do item na tabela de drops | Verifique se os valores de `ItemId` correspondem aos nomes de arquivo das definições reais de itens |
| NPC não dropa nada | Contêiner vazio ou `Weight: 0` | Certifique-se de que pelo menos um contêiner tem um peso diferente de zero |
| Sempre mesma quantidade | `QuantityMin` igual a `QuantityMax` | Defina valores diferentes para drops variáveis |
| Drop raro nunca aparece | `Weight` muito baixo | Aumente o valor de `Weight` no contêiner `Choice` ou teste mais abates |

---

## Próximos Passos

- [Criar um NPC Personalizado](/hytale-modding-docs/pt-br/tutorials/beginner/create-an-npc) -- construa o NPC que usa sua tabela de drops
- [Regras de Spawn de NPCs Personalizadas](/hytale-modding-docs/pt-br/tutorials/intermediate/custom-npc-spawning) -- controle onde seus NPCs que dropam loot aparecem
- [Lojas de NPCs e Comércio](/hytale-modding-docs/pt-br/tutorials/intermediate/npc-shops-and-trading) -- crie mercadores que vendem itens das suas tabelas de loot
