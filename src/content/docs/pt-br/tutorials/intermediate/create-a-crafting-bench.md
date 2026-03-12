---
title: Criar uma Bancada de Trabalho Personalizada
description: Tutorial passo a passo para adicionar uma bancada de trabalho personalizada com categorias de receitas, melhorias por nível e receitas de itens que a utilizam.
sidebar:
  order: 4
---

## Objetivo

Construir uma **Bancada de Runecrafting** personalizada que os jogadores possam colocar no mundo e usar para fabricar itens mágicos. Você definirá o item da bancada com categorias de fabricação, configurará melhorias baseadas em níveis e criará receitas de itens que requerem a bancada.

## O Que Você Vai Aprender

- Como bancadas de trabalho são definidas usando a propriedade de tipo de bloco `Bench`
- Como criar categorias que organizam receitas dentro da interface da bancada
- Como os níveis desbloqueiam progressivamente receitas mais difíceis
- Como receitas de itens referenciam uma bancada via `BenchRequirement`

## Pré-requisitos

- Uma pasta de mod com um `manifest.json` válido (veja [Configurar Seu Ambiente de Desenvolvimento](/hytale-modding-docs/pt-br/tutorials/beginner/setup-dev-environment))
- Familiaridade com definições de blocos (veja [Criar um Bloco Personalizado](/hytale-modding-docs/pt-br/tutorials/beginner/create-a-block))
- Familiaridade com definições de itens (veja [Criar um Item Personalizado](/hytale-modding-docs/pt-br/tutorials/beginner/create-an-item))

---

## Passo 1: Criar a Definição do Item da Bancada

Bancadas de trabalho no Hytale são itens com um `BlockType` que contém um objeto `Bench`. O objeto `Bench` define o tipo da bancada, ID único, categorias e níveis. A Bancada de Agricultura vanilla (`Bench_Farming.json`) e a Bancada de Armas (`Bench_Weapon.json`) seguem esse padrão.

Crie sua definição de bancada em:

```
YourMod/Assets/Server/Item/Items/Bench/Bench_Runecrafting.json
```

```json
{
  "TranslationProperties": {
    "Name": "server.items.Bench_Runecrafting.name",
    "Description": "server.items.Bench_Runecrafting.description"
  },
  "Icon": "Icons/ItemsGenerated/Bench_Runecrafting.png",
  "Categories": [
    "Furniture.Benches"
  ],
  "MaxStack": 1,
  "ItemLevel": 4,
  "BlockType": {
    "Material": "Solid",
    "DrawType": "Model",
    "Opacity": "Transparent",
    "CustomModel": "Blocks/Benches/Runecrafting.blockymodel",
    "CustomModelTexture": [
      {
        "Texture": "Blocks/Benches/Runecrafting_Texture.png",
        "Weight": 1
      }
    ],
    "HitboxType": "Bench_Runecrafting",
    "VariantRotation": "NESW",
    "Bench": {
      "Type": "Crafting",
      "Id": "Runecraftingbench",
      "Categories": [
        {
          "Id": "Runes",
          "Icon": "Icons/CraftingCategories/Runecrafting/Runes.png",
          "Name": "server.benchCategories.runecraftingbench.runes"
        },
        {
          "Id": "Enchantments",
          "Icon": "Icons/CraftingCategories/Runecrafting/Enchantments.png",
          "Name": "server.benchCategories.runecraftingbench.enchantments"
        },
        {
          "Id": "Scrolls",
          "Icon": "Icons/CraftingCategories/Runecrafting/Scrolls.png",
          "Name": "server.benchCategories.runecraftingbench.scrolls"
        }
      ],
      "LocalOpenSoundEventId": "SFX_Bench_Placeholder",
      "LocalCloseSoundEventId": "SFX_Bench_Placeholder",
      "CompletedSoundEventId": "SFX_Bench_Placeholder",
      "BenchUpgradeSoundEventId": "SFX_Workbench_Upgrade_Start_Default",
      "BenchUpgradeCompletedSoundEventId": "SFX_Workbench_Upgrade_Complete_Default",
      "TierLevels": [
        {
          "CraftingTimeReductionModifier": 0.0,
          "UpgradeRequirement": {
            "Material": [
              {
                "ItemId": "Ingredient_Crystal_Cyan",
                "Quantity": 10
              },
              {
                "ItemId": "Ingredient_Bar_Iron",
                "Quantity": 5
              }
            ],
            "TimeSeconds": 3
          }
        },
        {
          "CraftingTimeReductionModifier": 0.15,
          "UpgradeRequirement": {
            "Material": [
              {
                "ItemId": "Ingredient_Crystal_Cyan",
                "Quantity": 25
              },
              {
                "ItemId": "Ingredient_Bar_Thorium",
                "Quantity": 10
              }
            ],
            "TimeSeconds": 3
          }
        },
        {
          "CraftingTimeReductionModifier": 0.3
        }
      ]
    },
    "State": {
      "Id": "crafting",
      "Definitions": {
        "CraftCompleted": {}
      }
    },
    "Gathering": {
      "Breaking": {
        "GatherType": "Benches"
      }
    },
    "BlockParticleSetId": "Stone",
    "ParticleColor": "#4488cc",
    "Support": {
      "Down": [
        {
          "FaceType": "Full"
        }
      ]
    },
    "BlockSoundSetId": "Stone"
  },
  "Recipe": {
    "TimeSeconds": 3,
    "Input": [
      {
        "ResourceTypeId": "Rock",
        "Quantity": 10
      },
      {
        "ItemId": "Ingredient_Crystal_Cyan",
        "Quantity": 5
      }
    ],
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Id": "Workbench",
        "Categories": [
          "Workbench_Crafting"
        ]
      }
    ]
  },
  "PlayerAnimationsId": "Block",
  "Tags": {
    "Type": [
      "Bench"
    ]
  },
  "ItemSoundSetId": "ISS_Blocks_Wood"
}
```

### Campos principais da bancada explicados

| Campo | Finalidade |
|-------|-----------|
| `Bench.Type` | Deve ser `"Crafting"` para bancadas baseadas em receitas |
| `Bench.Id` | Identificador único que as receitas referenciam em seu `BenchRequirement`. Esta é a string que conecta receitas a esta bancada |
| `Bench.Categories` | Array de abas de categoria mostradas na interface da bancada. Cada uma tem um `Id`, `Icon` e `Name` de tradução |
| `Bench.TierLevels` | Array de níveis de melhoria. Cada nível pode ter um `CraftingTimeReductionModifier` (porcentagem mais rápido) e um `UpgradeRequirement` com materiais e tempo |
| `VariantRotation` | `"NESW"` permite que a bancada fique virada em quatro direções quando colocada |
| `State` | Define estados visuais como `CraftCompleted` para animações durante a fabricação |

### Estrutura de categoria

Cada categoria no array `Categories` é um objeto com três campos:

```json
{
  "Id": "Runes",
  "Icon": "Icons/CraftingCategories/Runecrafting/Runes.png",
  "Name": "server.benchCategories.runecraftingbench.runes"
}
```

- **`Id`** -- O identificador da categoria que as receitas referenciam para aparecer sob esta aba
- **`Icon`** -- Caminho para o PNG do ícone exibido na aba da categoria
- **`Name`** -- Chave de tradução para o texto do rótulo da categoria

---

## Passo 2: Criar Receitas Que Usam a Bancada

Qualquer definição de item com um bloco `Recipe` pode referenciar sua bancada. A conexão é feita através do array `BenchRequirement`, onde `Id` corresponde ao `Bench.Id` da sua bancada e `Categories` lista sob quais abas de categoria a receita aparece.

Crie um item que é fabricado na Bancada de Runecrafting:

```
YourMod/Assets/Server/Item/Items/Rune/Rune_Fire.json
```

```json
{
  "TranslationProperties": {
    "Name": "server.items.Rune_Fire.name",
    "Description": "server.items.Rune_Fire.description"
  },
  "Icon": "Icons/MyMod/Rune_Fire.png",
  "Quality": "Rare",
  "MaxStack": 16,
  "ItemLevel": 3,
  "Recipe": {
    "TimeSeconds": 5,
    "Input": [
      {
        "ItemId": "Ingredient_Fire_Essence",
        "Quantity": 3
      },
      {
        "ItemId": "Ingredient_Crystal_Cyan",
        "Quantity": 2
      }
    ],
    "OutputQuantity": 1,
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Id": "Runecraftingbench",
        "Categories": [
          "Runes"
        ],
        "RequiredTierLevel": 1
      }
    ]
  }
}
```

### Campos do BenchRequirement

| Campo | Finalidade |
|-------|-----------|
| `Type` | Deve ser `"Crafting"` para corresponder a uma bancada de fabricação |
| `Id` | Deve corresponder exatamente ao `Bench.Id` da sua definição de bancada (sensível a maiúsculas/minúsculas) |
| `Categories` | Array de IDs de categoria sob os quais esta receita aparece. Deve corresponder a um `Id` de categoria da bancada |
| `RequiredTierLevel` | Nível mínimo da bancada necessário. Os níveis são indexados a partir de 1 do array `TierLevels`. Omita para nível 0 (sem melhoria necessária) |

---

## Passo 3: Adicionar uma Receita Bloqueada por Nível

Para criar uma receita que só desbloqueia depois que o jogador melhora sua bancada, defina `RequiredTierLevel` com um valor mais alto:

```
YourMod/Assets/Server/Item/Items/Rune/Rune_Void.json
```

```json
{
  "TranslationProperties": {
    "Name": "server.items.Rune_Void.name",
    "Description": "server.items.Rune_Void.description"
  },
  "Icon": "Icons/MyMod/Rune_Void.png",
  "Quality": "Epic",
  "MaxStack": 8,
  "ItemLevel": 6,
  "Recipe": {
    "TimeSeconds": 10,
    "Input": [
      {
        "ItemId": "Ingredient_Void_Essence",
        "Quantity": 5
      },
      {
        "ItemId": "Ingredient_Crystal_Cyan",
        "Quantity": 8
      }
    ],
    "OutputQuantity": 1,
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Id": "Runecraftingbench",
        "Categories": [
          "Runes"
        ],
        "RequiredTierLevel": 2
      }
    ]
  }
}
```

Esta receita aparece acinzentada até que o jogador melhore a Bancada de Runecrafting para o nível 2.

---

## Passo 4: Adicionar Chaves de Tradução

Adicione todas as chaves de tradução ao seu arquivo de idioma:

```
YourMod/Assets/Languages/en-US.lang
```

```
server.items.Bench_Runecrafting.name=Runecrafting Bench
server.items.Bench_Runecrafting.description=A bench for crafting runes and enchantments.
server.benchCategories.runecraftingbench.runes=Runes
server.benchCategories.runecraftingbench.enchantments=Enchantments
server.benchCategories.runecraftingbench.scrolls=Scrolls
server.items.Rune_Fire.name=Fire Rune
server.items.Rune_Fire.description=A rune imbued with the essence of fire.
server.items.Rune_Void.name=Void Rune
server.items.Rune_Void.description=A rune channelling void energy.
```

---

## Passo 5: Testar No Jogo

1. Coloque sua pasta de mod no diretório de mods do servidor.
2. Inicie o servidor e observe erros de validação JSON.
3. Use o gerador de itens do desenvolvedor para obter `Bench_Runecrafting`.
4. Coloque a bancada e clique com o botão direito para abrir a interface de fabricação.
5. Confirme que todas as três abas de categoria (Runes, Enchantments, Scrolls) aparecem.
6. Verifique que `Rune_Fire` aparece na aba Runes e pode ser fabricada.
7. Confirme que `Rune_Void` aparece acinzentada até você melhorar a bancada para o nível 2.
8. Melhore a bancada fornecendo os materiais necessários e verifique que a receita de nível 2 desbloqueia.

**Erros comuns e correções:**

| Erro | Causa | Correção |
|------|-------|----------|
| Receita não aparece na bancada | `BenchRequirement.Id` não corresponde | Certifique-se de que `Id` corresponde exatamente ao `Bench.Id` (sensível a maiúsculas/minúsculas) |
| Aba de categoria ausente | `Id` da categoria não está na definição da bancada | Adicione a categoria ao array `Categories` da bancada |
| Receita sempre acinzentada | `RequiredTierLevel` muito alto | Verifique se o nível existe no array `TierLevels` da bancada |
| Bancada não pode ser colocada | Bloco `Support` ausente | Adicione `"Support": { "Down": [{ "FaceType": "Full" }] }` |

---

## Próximos Passos

- [Criar um Bloco Personalizado](/hytale-modding-docs/pt-br/tutorials/beginner/create-a-block) -- aprenda como blocos e itens se conectam
- [Tabelas de Loot Personalizadas](/hytale-modding-docs/pt-br/tutorials/intermediate/custom-loot-tables) -- configure drops que incluem seus itens fabricados
- [Lojas de NPCs e Comércio](/hytale-modding-docs/pt-br/tutorials/intermediate/npc-shops-and-trading) -- venda itens fabricados na bancada através de mercadores NPCs
