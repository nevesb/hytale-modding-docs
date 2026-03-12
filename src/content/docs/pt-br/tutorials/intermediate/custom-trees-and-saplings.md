---
title: Árvores e Mudas Personalizadas
description: Tutorial passo a passo para criar árvores personalizadas com mecânicas de crescimento de mudas, progressão de prefabs em múltiplos estágios e integração com agricultura.
sidebar:
  order: 1
---

## Objetivo

Criar uma árvore **Crystalwood** personalizada que os jogadores possam cultivar a partir de uma muda. Você definirá o item de muda com estágios de agricultura, configurará referências de prefab para cada estágio de crescimento e configurará modificadores de crescimento para que a árvore responda a água e fertilizante.

## O Que Você Vai Aprender

- Como itens de muda usam a propriedade de tipo de bloco `Farming` para crescimento em múltiplos estágios
- Como os estágios de crescimento transitam de tipos de bloco para prefabs
- Como `Duration`, `ReplaceMaskTags` e `ActiveGrowthModifiers` controlam o comportamento de crescimento
- Como usar herança `Parent` para criar variantes de árvores eficientemente

## Pré-requisitos

- Uma pasta de mod com um `manifest.json` válido (veja [Configurar Seu Ambiente de Desenvolvimento](/hytale-modding-docs/pt-br/tutorials/beginner/setup-dev-environment))
- Familiaridade com definições de blocos e itens (veja [Criar um Bloco Personalizado](/hytale-modding-docs/pt-br/tutorials/beginner/create-a-block))
- Arquivos de prefab de árvore criados no editor de prefabs do Hytale (arquivos `.prefab.json`)

---

## Visão Geral do Sistema de Crescimento

As árvores do Hytale crescem através de uma série de estágios definidos na propriedade `BlockType.Farming` da muda. O primeiro estágio é um bloco (a própria muda), e os estágios subsequentes são prefabs (modelos de árvore cada vez maiores). Cada estágio tem uma faixa de duração, e o engine automaticamente transita entre os estágios.

```
Bloco Muda → Prefab Árvore Pequena → Prefab Árvore Média → Prefab Árvore Completa
  Estágio 0       Estágio 1              Estágio 2              Estágio 3
```

A muda de Carvalho vanilla (`Plant_Sapling_Oak.json`) define 6 estágios de crescimento, enquanto a muda de Bétula usa herança `Parent` para reutilizar a maior parte da estrutura do Carvalho com texturas e prefabs diferentes.

---

## Passo 1: Criar a Definição do Item de Muda

A muda é um item que coloca um bloco com componentes de agricultura. Crie:

```
YourMod/Assets/Server/Item/Items/Plant/Plant_Sapling_Crystalwood.json
```

```json
{
  "TranslationProperties": {
    "Name": "server.items.Plant_Sapling_Crystalwood.name",
    "Description": "server.items.Plant_Sapling_Crystalwood.description"
  },
  "Icon": "Icons/MyMod/Plant_Crystalwood_Sapling.png",
  "Categories": [
    "Blocks.Plants"
  ],
  "Interactions": {
    "Primary": "Block_Primary",
    "Secondary": "Block_Secondary"
  },
  "ItemLevel": 5,
  "Recipe": {
    "TimeSeconds": 0,
    "Input": [
      {
        "ItemId": "Ingredient_Life_Essence",
        "Quantity": 12
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
        "Id": "Farmingbench",
        "Categories": [
          "Saplings"
        ],
        "RequiredTierLevel": 3
      }
    ]
  },
  "BlockType": {
    "DrawType": "Model",
    "CustomModel": "Blocks/Foliage/Tree/Sapling.blockymodel",
    "CustomModelTexture": [
      {
        "Texture": "Blocks/Foliage/Tree/Sapling_Textures/Crystalwood.png",
        "Weight": 1
      }
    ],
    "Group": "Wood",
    "HitboxType": "Plant_Large",
    "Flags": {},
    "RandomRotation": "YawStep1",
    "BlockEntity": {
      "Components": {
        "FarmingBlock": {}
      }
    },
    "Farming": {
      "Stages": {
        "Default": [
          {
            "Block": "Plant_Sapling_Crystalwood",
            "Duration": {
              "Min": 30000,
              "Max": 50000
            },
            "Type": "BlockType"
          },
          {
            "Prefabs": [
              {
                "Path": "Trees/Crystalwood/Stage_0/Crystalwood_Stage0_001.prefab.json",
                "Weight": 1
              }
            ],
            "Duration": {
              "Min": 40000,
              "Max": 60000
            },
            "Type": "Prefab",
            "ReplaceMaskTags": [
              "Soil"
            ],
            "SoundEventId": "SFX_Crops_Grow"
          },
          {
            "Prefabs": [
              {
                "Path": "Trees/Crystalwood/Stage_1/Crystalwood_Stage1_001.prefab.json",
                "Weight": 1
              }
            ],
            "Duration": {
              "Min": 40000,
              "Max": 60000
            },
            "Type": "Prefab",
            "ReplaceMaskTags": [
              "Soil"
            ],
            "SoundEventId": "SFX_Crops_Grow"
          },
          {
            "Prefabs": [
              {
                "Path": "Trees/Crystalwood/Stage_2/Crystalwood_Stage2_001.prefab.json",
                "Weight": 1
              },
              {
                "Path": "Trees/Crystalwood/Stage_2/Crystalwood_Stage2_002.prefab.json",
                "Weight": 1
              }
            ],
            "Duration": {
              "Min": 60000,
              "Max": 80000
            },
            "Type": "Prefab",
            "ReplaceMaskTags": [
              "Soil"
            ],
            "SoundEventId": "SFX_Crops_Grow"
          },
          {
            "Prefabs": [
              {
                "Path": "Trees/Crystalwood/Stage_3/Crystalwood_Stage3_001.prefab.json",
                "Weight": 1
              },
              {
                "Path": "Trees/Crystalwood/Stage_3/Crystalwood_Stage3_002.prefab.json",
                "Weight": 1
              }
            ],
            "Type": "Prefab",
            "ReplaceMaskTags": [
              "Soil"
            ],
            "SoundEventId": "SFX_Crops_Grow"
          }
        ]
      },
      "StartingStageSet": "Default",
      "ActiveGrowthModifiers": [
        "Fertilizer",
        "Water",
        "LightLevel"
      ]
    },
    "Gathering": {
      "Soft": {
        "ItemId": "Plant_Sapling_Crystalwood"
      }
    },
    "Support": {
      "Down": [
        {
          "TagId": "Type=Soil"
        }
      ]
    },
    "BlockParticleSetId": "Flower",
    "BlockSoundSetId": "Bush",
    "ParticleColor": "#44aacc"
  },
  "PlayerAnimationsId": "Item",
  "Tags": {
    "Type": [
      "Plant"
    ],
    "Family": [
      "Sapling"
    ]
  },
  "ItemSoundSetId": "ISS_Items_Foliage"
}
```

### Estágios de agricultura explicados

O array `Farming.Stages.Default` define cada estágio de crescimento em ordem:

| Estágio | Tipo | Finalidade |
|---------|------|-----------|
| 0 | `BlockType` | O próprio bloco de muda. `Block` referencia o ID de bloco deste mesmo item |
| 1-2 | `Prefab` | Prefabs de árvore pequena e média colocados conforme a árvore cresce |
| 3-4 | `Prefab` | Prefabs de árvore maiores. O estágio final não tem `Duration` (permanece para sempre) |

### Campos principais de agricultura

| Campo | Finalidade |
|-------|-----------|
| `Stages.Default[].Type` | `"BlockType"` para o bloco de muda inicial, `"Prefab"` para estágios de modelo de árvore |
| `Stages.Default[].Block` | Para estágios `BlockType`: o ID do bloco a colocar (geralmente a própria muda) |
| `Stages.Default[].Prefabs` | Para estágios `Prefab`: array de caminhos de prefab com pesos para seleção aleatória |
| `Stages.Default[].Duration.Min` / `Max` | Faixa de tempo em ticks do jogo antes de avançar para o próximo estágio. O engine escolhe um valor aleatório dentro da faixa |
| `Stages.Default[].ReplaceMaskTags` | Tags de bloco que o prefab pode substituir quando cresce. `"Soil"` permite que as raízes penetrem na terra |
| `Stages.Default[].SoundEventId` | Som tocado quando a transição de estágio ocorre |
| `StartingStageSet` | Qual conjunto de estágios começar. `"Default"` é o padrão |
| `ActiveGrowthModifiers` | Array de modificadores que afetam a velocidade de crescimento: `"Fertilizer"` (composto), `"Water"` (chuva/irrigação), `"LightLevel"` (luz solar) |

### Múltiplas variantes de prefab

Quando um estágio tem múltiplas entradas em seu array `Prefabs`, o engine escolhe uma aleatoriamente baseado em `Weight`. Isso cria variedade natural:

```json
"Prefabs": [
  {
    "Path": "Trees/Crystalwood/Stage_2/Crystalwood_Stage2_001.prefab.json",
    "Weight": 1
  },
  {
    "Path": "Trees/Crystalwood/Stage_2/Crystalwood_Stage2_002.prefab.json",
    "Weight": 1
  }
]
```

Pesos iguais dão 50/50 de chance. Use pesos diferentes para tornar algumas variantes mais raras.

---

## Passo 2: Criar o Componente de Entidade de Bloco

O objeto `BlockEntity.Components.FarmingBlock` diz ao engine que este bloco usa o sistema de agricultura. O objeto vazio `{}` herda o comportamento padrão de agricultura. A propriedade `Farming` no mesmo `BlockType` fornece a configuração real dos estágios.

```json
"BlockEntity": {
  "Components": {
    "FarmingBlock": {}
  }
}
```

Este componente é obrigatório. Sem ele, os estágios de `Farming` serão ignorados.

---

## Passo 3: Configurar Suporte de Bloco e Coleta

Duas propriedades adicionais de `BlockType` garantem que a muda se comporte corretamente:

### Suporte

```json
"Support": {
  "Down": [
    {
      "TagId": "Type=Soil"
    }
  ]
}
```

A muda requer um bloco com a tag `Type=Soil` diretamente abaixo dela. Se o solo for removido, a muda quebra e dropa a si mesma.

### Coleta

```json
"Gathering": {
  "Soft": {
    "ItemId": "Plant_Sapling_Crystalwood"
  }
}
```

O tipo de coleta `Soft` significa que os jogadores podem quebrar a muda com qualquer ferramenta (ou com as mãos) e receber o item de muda de volta.

---

## Passo 4: Criar uma Variante Usando Herança Parent

Para criar uma variante de cor da sua árvore sem duplicar o arquivo inteiro, use herança `Parent`. A muda de Bétula vanilla usa exatamente este padrão:

```
YourMod/Assets/Server/Item/Items/Plant/Plant_Sapling_Crystalwood_Red.json
```

```json
{
  "TranslationProperties": {
    "Name": "server.items.Plant_Sapling_Crystalwood_Red.name",
    "Description": "server.items.Plant_Sapling_Crystalwood_Red.description"
  },
  "Parent": "Plant_Sapling_Crystalwood",
  "Icon": "Icons/MyMod/Plant_Crystalwood_Red_Sapling.png",
  "ItemLevel": 6,
  "Recipe": {
    "TimeSeconds": 0,
    "Input": [
      {
        "ItemId": "Ingredient_Life_Essence",
        "Quantity": 18
      },
      {
        "ItemId": "Ingredient_Crystal_Cyan",
        "Quantity": 4
      }
    ],
    "OutputQuantity": 1,
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Id": "Farmingbench",
        "Categories": [
          "Saplings"
        ],
        "RequiredTierLevel": 4
      }
    ]
  },
  "BlockType": {
    "CustomModelTexture": [
      {
        "Texture": "Blocks/Foliage/Tree/Sapling_Textures/Crystalwood_Red.png",
        "Weight": 1
      }
    ],
    "Farming": {
      "Stages": {
        "Default": [
          {
            "Block": "Plant_Sapling_Crystalwood_Red",
            "Duration": {
              "Min": 30000,
              "Max": 50000
            },
            "Type": "BlockType"
          },
          {
            "Prefabs": [
              {
                "Path": "Trees/Crystalwood_Red/Stage_0/Crystalwood_Red_Stage0_001.prefab.json",
                "Weight": 1
              }
            ],
            "Duration": {
              "Min": 40000,
              "Max": 60000
            },
            "Type": "Prefab",
            "ReplaceMaskTags": [
              "Soil"
            ],
            "SoundEventId": "SFX_Crops_Grow"
          },
          {
            "Prefabs": [
              {
                "Path": "Trees/Crystalwood_Red/Stage_1/Crystalwood_Red_Stage1_001.prefab.json",
                "Weight": 1
              }
            ],
            "Type": "Prefab",
            "ReplaceMaskTags": [
              "Soil"
            ],
            "SoundEventId": "SFX_Crops_Grow"
          }
        ]
      },
      "StartingStageSet": "Default",
      "ActiveGrowthModifiers": [
        "Fertilizer",
        "Water",
        "LightLevel"
      ]
    },
    "Gathering": {
      "Soft": {
        "ItemId": "Plant_Sapling_Crystalwood_Red"
      }
    },
    "ParticleColor": "#cc4444"
  }
}
```

O campo `Parent` herda todas as propriedades de `Plant_Sapling_Crystalwood`. Apenas os campos que você especifica são sobrescritos -- o modelo, hitbox, conjunto de sons, regras de suporte e outras propriedades são todas herdadas automaticamente.

---

## Passo 5: Adicionar Chaves de Tradução

```
YourMod/Assets/Languages/en-US.lang
```

```
server.items.Plant_Sapling_Crystalwood.name=Crystalwood Sapling
server.items.Plant_Sapling_Crystalwood.description=A sapling that grows into a tree with crystalline bark.
server.items.Plant_Sapling_Crystalwood_Red.name=Red Crystalwood Sapling
server.items.Plant_Sapling_Crystalwood_Red.description=A variant crystalwood sapling with crimson foliage.
```

---

## Passo 6: Testar No Jogo

1. Coloque sua pasta de mod no diretório de mods do servidor.
2. Inicie o servidor e observe erros sobre caminhos de prefab ausentes ou IDs de bloco desconhecidos.
3. Use o gerador de itens do desenvolvedor para obter `Plant_Sapling_Crystalwood`.
4. Coloque a muda em um bloco de terra/solo e confirme que renderiza corretamente.
5. Espere pelo primeiro estágio de crescimento (ou use comandos de aceleração de tempo) e verifique que a muda transita para o primeiro prefab de árvore.
6. Confirme que cada estágio subsequente carrega o modelo de prefab correto.
7. Verifique que o estágio final permanece permanentemente (sem `Duration` definido).
8. Quebre a muda antes dela crescer e confirme que você recebe o item de muda de volta.
9. Teste que remover o bloco de solo abaixo da muda faz com que ela quebre.

**Erros comuns e correções:**

| Erro | Causa | Correção |
|------|-------|----------|
| Muda é colocada mas nunca cresce | Componente `FarmingBlock` ausente | Adicione `"BlockEntity": { "Components": { "FarmingBlock": {} } }` |
| `Unknown prefab path` | Arquivo de prefab ausente ou caminho errado | Verifique se os arquivos `.prefab.json` existem nos caminhos referenciados |
| Muda flutua no ar | Configuração `Support` ausente | Adicione `"Support": { "Down": [{ "TagId": "Type=Soil" }] }` |
| Crescimento muito rápido ou lento | Valores de `Duration` precisam de ajuste | Vanilla usa 40000-60000 para a maioria dos estágios, 80000-100000 para estágios tardios |
| Variante herda estágios errados | `Parent` não sobrescrevendo `Farming` | A variante deve fornecer o objeto `Farming.Stages` completo para sobrescrever estágios |

---

## Próximos Passos

- [Criar um Bloco Personalizado](/hytale-modding-docs/pt-br/tutorials/beginner/create-a-block) -- entenda definições de blocos que seus prefabs de árvore contêm
- [Tabelas de Loot Personalizadas](/hytale-modding-docs/pt-br/tutorials/intermediate/custom-loot-tables) -- configure drops quando jogadores cortam suas árvores personalizadas
- [Criar uma Bancada de Trabalho](/hytale-modding-docs/pt-br/tutorials/intermediate/create-a-crafting-bench) -- construa a Bancada de Agricultura onde mudas são fabricadas
