---
title: Tabelas de Loot Personalizadas
description: Tutorial passo a passo para criar tabelas de drops com drops garantidos, itens raros ponderados e contêineres aninhados usando o NPC Slime.
sidebar:
  order: 2
---

## Objetivo

Criar uma tabela de drops personalizada para o NPC **Slime** do tutorial [Criar um NPC Personalizado](/hytale-modding-docs/pt-br/tutorials/beginner/create-an-npc/). Você construirá um drop garantido, adicionará um item raro ponderado e aprenderá como contêineres aninhados criam lógica de loot complexa.

## O Que Você Vai Aprender

- Como os tipos de `Container` (`Multiple`, `Choice`, `Single`) funcionam juntos para criar lógica de drops
- Como `Weight` controla a probabilidade de drops aleatórios
- Como combinar drops garantidos e raros em uma única tabela
- Como `QuantityMin` e `QuantityMax` criam quantidades de drops variáveis
- Como conectar uma tabela de drops a um NPC via `DropList`

## Pré-requisitos

- Um mod funcional do NPC Slime (veja [Criar um NPC Personalizado](/hytale-modding-docs/pt-br/tutorials/beginner/create-an-npc/))
- O mod da Árvore Encantada instalado (veja [Árvores e Saplings Personalizados](/hytale-modding-docs/pt-br/tutorials/intermediate/custom-trees-and-saplings/)) — usamos sua Fruta Encantada como item de drop
- O mod do bloco Crystal Glow instalado (veja [Criar um Bloco Personalizado](/hytale-modding-docs/pt-br/tutorials/beginner/create-a-block/)) — usamos como drop raro

**Repositórios do mod complementar:**
- [hytale-mods-custom-npc](https://github.com/nevesb/hytale-mods-custom-npc) — Slime NPC v1.0.0 (mod base sem loot)
- [hytale-mods-custom-loot-tables](https://github.com/nevesb/hytale-mods-custom-loot-tables) — Slime NPC v1.1.0 (com tabela de drops deste tutorial)

:::note[Este Tutorial Substitui a Tabela de Drops do NPC]
O tutorial [Criar um NPC Personalizado](/hytale-modding-docs/pt-br/tutorials/beginner/create-an-npc/) inclui uma tabela de drops básica no Passo 6. Este tutorial constrói uma versão mais completa que **substitui** aquela tabela de drops. Após completar este tutorial, seu Slime usará a nova tabela de loot.
:::

---

## Visão Geral do Sistema de Drops

As tabelas de drops ficam em `Server/Drops/` e controlam quais itens caem quando um NPC morre, um bloco quebra ou um recurso é coletado. O jogo vanilla as organiza por tipo de fonte:

```
Assets/Server/Drops/
  NPCs/
    Beast/
    Critter/
    Intelligent/
      Feran/
      Trork/
  Crop/
  Wood/
  Rock/
  Plant/
```

Toda tabela de drops é um arquivo JSON com um objeto raiz `Container`. O sistema de contêineres usa três tipos que podem ser aninhados para criar qualquer lógica de drop:

### Tipos de Contêiner

| Tipo | Comportamento |
|------|--------------|
| `Multiple` | Avalia **todos** os contêineres filhos em ordem. Cada filho é executado independentemente |
| `Choice` | Escolhe **um** filho aleatoriamente, ponderado pelos valores de `Weight`. O `Weight` do próprio `Choice` controla se o grupo é ativado |
| `Single` | Nó terminal. Produz o `Item` especificado com uma quantidade aleatória entre `QuantityMin` e `QuantityMax` |

---

## Passo 1: Criar um Drop Garantido

A tabela de drops mais simples garante um item toda vez. Vamos começar fazendo o Slime sempre dropar 1 Fruta Encantada — a mesma fruta do tutorial [Árvores e Saplings Personalizados](/hytale-modding-docs/pt-br/tutorials/intermediate/custom-trees-and-saplings/).

Crie (ou substitua) o arquivo da tabela de drops:

```
CreateACustomNPC/Server/Drops/Drop_Slime.json
```

```json
{
  "Container": {
    "Type": "Multiple",
    "Containers": [
      {
        "Type": "Single",
        "Item": {
          "ItemId": "Plant_Fruit_Enchanted",
          "QuantityMin": 1,
          "QuantityMax": 1
        }
      }
    ]
  }
}
```

Um contêiner `Multiple` com um único filho `Single` garante o drop toda vez. O `ItemId` deve corresponder ao nome do arquivo de uma definição de item existente (sem `.json`).

Este é o mesmo padrão usado por depósitos de cristal vanilla. Por exemplo, `Rock_Crystal_Blue.json` garante 4-5 cristais ciano:

```json
{
  "Container": {
    "Type": "Multiple",
    "Containers": [
      {
        "Type": "Single",
        "Item": {
          "ItemId": "Ingredient_Crystal_Cyan",
          "QuantityMin": 4,
          "QuantityMax": 5
        }
      }
    ]
  }
}
```

---

## Passo 2: Adicionar um Drop Raro de Cristal

Agora vamos tornar o Slime mais interessante — mantemos a fruta garantida, mas adicionamos uma **chance de 10%** de também dropar um bloco Crystal Glow do tutorial [Criar um Bloco Personalizado](/hytale-modding-docs/pt-br/tutorials/beginner/create-a-block/).

Atualize `Server/Drops/Drop_Slime.json`:

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
              "ItemId": "Plant_Fruit_Enchanted",
              "QuantityMin": 1,
              "QuantityMax": 1
            }
          }
        ]
      },
      {
        "Type": "Choice",
        "Weight": 10,
        "Containers": [
          {
            "Type": "Single",
            "Item": {
              "ItemId": "Block_Crystal_Glow",
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

### Como os Pesos Funcionam

O contêiner externo `Multiple` avalia ambos os grupos independentemente:

1. **Grupo 1** (`Weight: 100`): 100% de chance — sempre dropa 1 Fruta Encantada
2. **Grupo 2** (`Weight: 10`): 10% de chance — às vezes também dropa 1 bloco Crystal Glow

O `Weight` em um contêiner `Choice` controla se aquele grupo é ativado. `Weight: 100` significa sempre, `Weight: 10` significa 10% das vezes.

Este é o mesmo padrão que o vanilla usa para drops de equipamento de NPCs. Por exemplo, `Drop_Trork_Warrior.json` usa três grupos:

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
              "ItemId": "Ingredient_Fabric_Scrap_Linen",
              "QuantityMin": 1,
              "QuantityMax": 3
            }
          }
        ]
      },
      {
        "Type": "Choice",
        "Weight": 5,
        "Containers": [
          { "Weight": 25, "Type": "Single", "Item": { "ItemId": "Armor_Trork_Head", "QuantityMin": 1, "QuantityMax": 1 } },
          { "Weight": 25, "Type": "Single", "Item": { "ItemId": "Armor_Trork_Chest", "QuantityMin": 1, "QuantityMax": 1 } },
          { "Weight": 25, "Type": "Single", "Item": { "ItemId": "Armor_Trork_Hands", "QuantityMin": 1, "QuantityMax": 1 } },
          { "Weight": 25, "Type": "Single", "Item": { "ItemId": "Armor_Trork_Legs", "QuantityMin": 1, "QuantityMax": 1 } }
        ]
      },
      {
        "Type": "Choice",
        "Weight": 15,
        "Containers": [
          {
            "Type": "Single",
            "Item": { "ItemId": "Weapon_Battleaxe_Stone_Trork", "QuantityMin": 1, "QuantityMax": 1 }
          }
        ]
      }
    ]
  }
}
```

- **Grupo 1** (`Weight: 100`): Sempre dropa 1-3 retalhos de linho
- **Grupo 2** (`Weight: 5`): 5% de chance de dropar uma peça de armadura (cada uma com peso interno de 25%)
- **Grupo 3** (`Weight: 15`): 15% de chance de dropar um machado de batalha

Os valores internos de `Weight` dentro de um `Choice` são relativos entre si: 25 + 25 + 25 + 25 = 100, então cada peça de armadura tem 25% de chance *quando o grupo é ativado*. A chance total de obter o capacete é 5% x 25% = 1.25%.

---

## Passo 3: Conectar a Tabela de Drops ao NPC

As tabelas de drops são referenciadas pelas definições de papéis de NPC através do campo `DropList`. O valor corresponde ao nome do arquivo da tabela de drops sem `.json`.

Abra o Papel de NPC do seu Slime em `Server/NPC/Roles/Slime.json` e adicione o campo `DropList` ao bloco `Modify`:

```json {7}
{
  "Type": "Variant",
  "Reference": "Template_Predator",
  "Modify": {
    "Appearance": "Slime",
    "MaxHealth": 75,
    "DropList": "Drop_Slime",
    "KnockbackScale": 0.5,
    "IsMemory": true,
    "MemoriesCategory": "Beast",
    "NameTranslationKey": {
      "Compute": "NameTranslationKey"
    }
  },
  "Parameters": {
    "NameTranslationKey": {
      "Value": "server.npcRoles.Slime.name",
      "Description": "Translation key for NPC name display"
    }
  }
}
```

O `"DropList": "Drop_Slime"` diz ao engine para resolver `Server/Drops/Drop_Slime.json` quando o NPC morrer. NPCs vanilla usam o mesmo padrão — por exemplo, `Bear_Grizzly.json` referencia `"Drop_Bear_Grizzly"`.

---

## Passo 4: Contêineres Aninhados para Drops Complexos

Para cenários mais complexos, você pode aninhar `Multiple` dentro de `Choice` para criar resultados ramificados. Este padrão é usado pelo `Wood_Branch.json` vanilla para drops de recursos ao quebrar galhos de madeira:

```json
{
  "Container": {
    "Type": "Choice",
    "Containers": [
      {
        "Type": "Multiple",
        "Weight": 50,
        "Containers": [
          {
            "Type": "Single",
            "Item": {
              "ItemId": "Ingredient_Stick",
              "QuantityMin": 0,
              "QuantityMax": 2
            }
          },
          {
            "Type": "Single",
            "Item": {
              "ItemId": "Ingredient_Tree_Sap",
              "QuantityMin": 0,
              "QuantityMax": 1
            }
          }
        ]
      },
      {
        "Type": "Multiple",
        "Weight": 50,
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

- **50% de chance**: Dropa 0-2 gravetos **e** 0-1 seiva de árvore (ambos os itens do `Multiple`)
- **50% de chance**: Dropa apenas 1 graveto

Quando `QuantityMin` é `0`, há uma chance do item não produzir nada. Quando `QuantityMin` e `QuantityMax` são omitidos, a quantidade padrão é `1`.

:::tip[Resumo de Aninhamento]
- `Multiple` → `Choice`: Cada grupo é avaliado independentemente (garantido + raro, como nosso Slime)
- `Choice` → `Multiple`: Um resultado é escolhido, depois todos os seus itens dropam juntos (ramificação, como Wood Branch)
:::

---

## Passo 5: Tabelas de Drops Vazias

Alguns NPCs não dropam nada. Todos os critters vanilla — Esquilos, Sapos, Geckos, Suricatos — usam um objeto vazio:

```json
{}
```

Assim é como seu Slime funcionava antes deste tutorial — sem um `DropList` no Papel de NPC, ou com uma tabela de drops vazia, o NPC não dropa nada ao morrer.

---

## Passo 6: Testar no Jogo

1. Copie sua pasta `CreateACustomNPC/` atualizada para `%APPDATA%/Hytale/UserData/Mods/`

2. Certifique-se de que os mods **CreateACustomBlock** e **CustomTreesAndSaplings** também estejam instalados — a tabela de drops referencia itens de ambos os mods

3. Inicie Hytale e entre no **Modo Criativo**

4. Spawne e mate o Slime múltiplas vezes:
   ```text
   /op self
   /npc spawn Slime
   ```

5. Verifique:

![Drops do Slime no jogo — Frutas Encantadas e blocos Crystal Glow no chão depois de matar vários Slimes](/hytale-modding-docs/images/tutorials/custom-loot-tables/slime-drops.png)

   - Toda morte dropa 1 Fruta Encantada (garantido)
   - Aproximadamente 1 em cada 10 mortes também dropa um bloco Crystal Glow (10% de chance)
   - As quantidades estão corretas (sempre exatamente 1 de cada)

**Erros comuns e correções:**

| Erro | Causa | Correção |
|------|-------|----------|
| `Unknown drop list` | Nome de arquivo ou caminho errado | Verifique se `Drop_Slime.json` existe em `Server/Drops/` e se `DropList` corresponde sem `.json` |
| `Unknown item id` | Erro de digitação no ID do item ou mod faltando | Verifique se `ItemId` corresponde aos nomes reais dos arquivos. Certifique-se de que os mods que fornecem esses itens estejam instalados |
| NPC não dropa nada | `DropList` faltando no Papel de NPC | Adicione `"DropList": "Drop_Slime"` ao bloco `Modify` em `Slime.json` |
| Sempre mesma quantidade | `QuantityMin` igual a `QuantityMax` | Defina valores diferentes para drops variáveis |
| Drop raro nunca aparece | `Weight` muito baixo ou azar | `Weight: 10` significa ~10% — mate 20+ Slimes para confirmar |

---

## Referência de Tabelas de Drops Vanilla

Aqui está um resumo de padrões reais de tabelas de drops dos assets do jogo:

| Arquivo Vanilla | Padrão | Caso de Uso |
|----------------|--------|-------------|
| `Rock_Crystal_Blue.json` | `Multiple` → `Single` | Drop de recurso garantido |
| `Drop_Bear_Grizzly.json` | `Multiple` → `Choice(100)` + `Choice(100)` | Múltiplos drops garantidos |
| `Drop_Trork_Warrior.json` | `Multiple` → `Choice(100)` + `Choice(5)` + `Choice(15)` | Garantido + loot raro |
| `Wood_Branch.json` | `Choice` → `Multiple(50)` + `Multiple(50)` | Resultados ramificados de recursos |
| `Drop_Frog_*.json` | `{}` | Sem drops |

---

## Próximos Passos

- [Regras de Spawn de NPCs Personalizadas](/hytale-modding-docs/pt-br/tutorials/intermediate/custom-npc-spawning/) — controle onde seus Slimes que dropam loot aparecem no mundo
- [Lojas de NPCs e Comércio](/hytale-modding-docs/pt-br/tutorials/intermediate/npc-shops-and-trading/) — crie mercadores que vendam itens das suas tabelas de loot
- [Referência de Tabelas de Drops](/hytale-modding-docs/pt-br/reference/economy-and-progression/drop-tables/) — referência completa do esquema para todos os tipos de contêineres
