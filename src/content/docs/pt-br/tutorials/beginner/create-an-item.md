---
title: Criar um Item Personalizado (Arma)
description: Tutorial passo a passo para adicionar uma arma personalizada ao Hytale, incluindo JSON de definição de item, receita de crafting e chaves de tradução.
---

## Objetivo

Adicionar uma adaga personalizada chamada **Adaga de Espinheiro** ao jogo. Você vai criar o JSON de definição do item com valores de dano e uma receita de crafting, adicionar chaves de tradução para o nome e a descrição, e testá-la no jogo.

## Pré-requisitos

- Uma pasta de mod com um `manifest.json` válido (veja [Configure seu Ambiente de Desenvolvimento](/hytale-modding-docs/tutorials/beginner/setup-dev-environment))
- Blockbench instalado para criar o modelo 3D (opcional — você pode referenciar um modelo vanilla para começar)
- Familiaridade com JSON (veja [Fundamentos de JSON](/hytale-modding-docs/getting-started/json-basics))

---

## Passo 1: Criar o Modelo do Item no Blockbench

O Hytale utiliza o formato `.blockymodel` para modelos 3D de itens. Se você ainda não configurou o Blockbench, pule este passo e referencie um modelo vanilla existente para fazer seu item funcionar primeiro, substituindo-o depois.

Os modelos vanilla de adagas ficam em caminhos como:

```
Items/Weapons/Dagger/Bronze.blockymodel
Items/Weapons/Dagger/Bronze_Texture.png
```

Para o seu item personalizado, crie e exporte:

```
YourMod/Assets/Common/Models/Items/Weapons/Dagger/Thornwood.blockymodel
YourMod/Assets/Common/Models/Items/Weapons/Dagger/Thornwood_Texture.png
```

**Dicas para o Blockbench:**
- Mantenha o modelo centralizado na origem — o Hytale usa o ponto de pivô para posicionamento na mão
- Exporte como **Hytale Blocky Model** usando o plugin do Hytale (veja [Configure seu Ambiente de Desenvolvimento](/hytale-modding-docs/tutorials/beginner/setup-dev-environment))
- O arquivo de textura deve ser um PNG com dimensões em potência de dois (ex: 16x16, 32x32, 64x64)

---

## Passo 2: Criar o JSON de Definição do Item

As definições de itens de armas seguem o padrão estabelecido pelos arquivos em `Assets/Server/Item/Items/Weapon/`. O arquivo das adagas de bronze (`Weapon_Daggers_Bronze.json`) mostra a estrutura: um template `Parent` cuida do comportamento compartilhado, enquanto o arquivo filho sobrescreve valores de dano, caminhos de modelo, qualidade e chaves de tradução.

Crie:

```
YourMod/Assets/Server/Item/Items/MyMod/Weapon_Daggers_Thornwood.json
```

```json
{
  "Parent": "Template_Weapon_Daggers",
  "TranslationProperties": {
    "Name": "server.items.Weapon_Daggers_Thornwood.name",
    "Description": "server.items.Weapon_Daggers_Thornwood.description"
  },
  "Model": "Items/Weapons/Dagger/Thornwood.blockymodel",
  "Texture": "Items/Weapons/Dagger/Thornwood_Texture.png",
  "Icon": "Icons/MyMod/Weapon_Daggers_Thornwood.png",
  "Quality": "Uncommon",
  "ItemLevel": 20,
  "MaxDurability": 80,
  "DurabilityLossOnHit": 0.5,
  "Tags": {
    "Type": ["Weapon"],
    "Family": ["Daggers"]
  },
  "InteractionVars": {
    "Swing_Left_Damage": {
      "Interactions": [
        {
          "Parent": "Weapon_Daggers_Primary_Swing_Left_Damage",
          "DamageCalculator": {
            "BaseDamage": {
              "Physical": 4
            }
          },
          "DamageEffects": {
            "WorldSoundEventId": "SFX_Daggers_T2_Slash_Impact",
            "LocalSoundEventId": "SFX_Daggers_T2_Slash_Impact"
          }
        }
      ]
    },
    "Swing_Right_Damage": {
      "Interactions": [
        {
          "Parent": "Weapon_Daggers_Primary_Swing_Right_Damage",
          "DamageCalculator": {
            "BaseDamage": {
              "Physical": 4
            }
          },
          "DamageEffects": {
            "WorldSoundEventId": "SFX_Daggers_T2_Slash_Impact",
            "LocalSoundEventId": "SFX_Daggers_T2_Slash_Impact"
          }
        }
      ]
    },
    "Stab_Left_Damage": {
      "Interactions": [
        {
          "Parent": "Weapon_Daggers_Primary_Stab_Left_Damage",
          "DamageCalculator": {
            "BaseDamage": {
              "Physical": 9
            }
          },
          "DamageEffects": {
            "WorldSoundEventId": "SFX_Daggers_T2_Slash_Impact",
            "LocalSoundEventId": "SFX_Daggers_T2_Slash_Impact"
          }
        }
      ]
    },
    "Stab_Right_Damage": {
      "Interactions": [
        {
          "Parent": "Weapon_Daggers_Primary_Stab_Right_Damage",
          "DamageCalculator": {
            "BaseDamage": {
              "Physical": 12
            }
          },
          "DamageEffects": {
            "WorldSoundEventId": "SFX_Daggers_T2_Slash_Impact",
            "LocalSoundEventId": "SFX_Daggers_T2_Slash_Impact"
          }
        }
      ]
    }
  }
}
```

### Campos principais explicados

| Campo | Finalidade |
|-------|------------|
| `Parent` | Herda todas as animações de ataque, interações e stats base do template |
| `TranslationProperties` | Chaves resolvidas a partir do seu arquivo `.lang` para o nome e tooltip do item |
| `Model` | Caminho para o arquivo `.blockymodel` |
| `Texture` | Caminho para o PNG de textura do modelo |
| `Icon` | PNG do ícone no slot do inventário |
| `Quality` | Nível de raridade — controla a cor da borda e partícula de drop. Valores válidos: `Junk`, `Common`, `Uncommon`, `Rare`, `Epic`, `Legendary` |
| `ItemLevel` | Determina o tier de progressão; afeta a ponderação nas tabelas de loot |
| `MaxDurability` | Quantos golpes até o item quebrar |
| `DurabilityLossOnHit` | Durabilidade subtraída por golpe (suporta decimais) |
| `InteractionVars` | Sobrescreve valores de dano específicos de ataques do template pai |

### Calculadora de dano

Cada entrada em `InteractionVars` sobrescreve uma fase de ataque. `BaseDamage` recebe uma chave de tipo de dano:

| Tipo de dano | Descrição |
|--------------|-----------|
| `Physical` | Dano corpo a corpo padrão |
| `Fire` | Dano elemental de fogo |
| `Poison` | Aplica um efeito de dano ao longo do tempo |
| `Ice` | Dano de gelo |

Você pode combinar tipos em um único golpe:

```json
"BaseDamage": {
  "Physical": 4,
  "Poison": 2
}
```

---

## Passo 3: Adicionar uma Receita de Crafting

Receitas podem ser definidas inline dentro do JSON do item (como visto em `Food_Bread.json`) ou em um arquivo de receita separado. Inline é mais simples para itens únicos. Adicione um bloco `Recipe` à definição do seu item:

```json
{
  "Parent": "Template_Weapon_Daggers",
  "TranslationProperties": {
    "Name": "server.items.Weapon_Daggers_Thornwood.name",
    "Description": "server.items.Weapon_Daggers_Thornwood.description"
  },
  "Model": "Items/Weapons/Dagger/Thornwood.blockymodel",
  "Texture": "Items/Weapons/Dagger/Thornwood_Texture.png",
  "Icon": "Icons/MyMod/Weapon_Daggers_Thornwood.png",
  "Quality": "Uncommon",
  "ItemLevel": 20,
  "MaxDurability": 80,
  "DurabilityLossOnHit": 0.5,
  "Tags": {
    "Type": ["Weapon"],
    "Family": ["Daggers"]
  },
  "Recipe": {
    "Input": [
      {
        "ResourceTypeId": "Wood_Trunk",
        "Quantity": 3
      },
      {
        "ItemId": "Ingredient_Fibre",
        "Quantity": 2
      },
      {
        "ItemId": "Ingredient_Bar_Copper",
        "Quantity": 1
      }
    ],
    "Output": [
      {
        "ItemId": "Weapon_Daggers_Thornwood"
      }
    ],
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Categories": ["Weapon_Daggers"],
        "Id": "Weapon_Bench"
      }
    ],
    "TimeSeconds": 4
  },
  "InteractionVars": {
    "Swing_Left_Damage": {
      "Interactions": [
        {
          "Parent": "Weapon_Daggers_Primary_Swing_Left_Damage",
          "DamageCalculator": {
            "BaseDamage": {
              "Physical": 4
            }
          },
          "DamageEffects": {
            "WorldSoundEventId": "SFX_Daggers_T2_Slash_Impact",
            "LocalSoundEventId": "SFX_Daggers_T2_Slash_Impact"
          }
        }
      ]
    },
    "Swing_Right_Damage": {
      "Interactions": [
        {
          "Parent": "Weapon_Daggers_Primary_Swing_Right_Damage",
          "DamageCalculator": {
            "BaseDamage": {
              "Physical": 4
            }
          },
          "DamageEffects": {
            "WorldSoundEventId": "SFX_Daggers_T2_Slash_Impact",
            "LocalSoundEventId": "SFX_Daggers_T2_Slash_Impact"
          }
        }
      ]
    },
    "Stab_Left_Damage": {
      "Interactions": [
        {
          "Parent": "Weapon_Daggers_Primary_Stab_Left_Damage",
          "DamageCalculator": {
            "BaseDamage": {
              "Physical": 9
            }
          },
          "DamageEffects": {
            "WorldSoundEventId": "SFX_Daggers_T2_Slash_Impact",
            "LocalSoundEventId": "SFX_Daggers_T2_Slash_Impact"
          }
        }
      ]
    },
    "Stab_Right_Damage": {
      "Interactions": [
        {
          "Parent": "Weapon_Daggers_Primary_Stab_Right_Damage",
          "DamageCalculator": {
            "BaseDamage": {
              "Physical": 12
            }
          },
          "DamageEffects": {
            "WorldSoundEventId": "SFX_Daggers_T2_Slash_Impact",
            "LocalSoundEventId": "SFX_Daggers_T2_Slash_Impact"
          }
        }
      ]
    }
  }
}
```

### Campos da receita

| Campo | Finalidade |
|-------|------------|
| `Input` | Lista de ingredientes necessários. Use `ItemId` para um item específico, ou `ResourceTypeId` para uma categoria de recurso (ex: qualquer tronco de madeira conta como `Wood_Trunk`) |
| `Output` | O que o jogador recebe. Omitir `Quantity` usa o padrão 1 |
| `BenchRequirement` | Qual estação de crafting é necessária. `Id` é o identificador da bancada; `Categories` filtra em qual aba da bancada o item aparece |
| `TimeSeconds` | Quanto tempo o crafting leva |
| `KnowledgeRequired` | Defina como `true` se a receita precisa ser aprendida por um pergaminho antes de aparecer |

---

## Passo 4: Adicionar Chaves de Tradução

Crie ou adicione ao arquivo de idioma do seu mod:

```
YourMod/Assets/Languages/en-US.lang
```

```
server.items.Weapon_Daggers_Thornwood.name=Thornwood Dagger
server.items.Weapon_Daggers_Thornwood.description=A light blade carved from thornwood. Fast and precise.
```

O formato de chave de tradução usado no vanilla é: `server.items.<ItemId>.name` e `server.items.<ItemId>.description`. Siga esse padrão exatamente — o engine diferencia maiúsculas e minúsculas.

---

## Passo 5: Testar no Jogo

1. Copie a pasta do seu mod para o diretório de mods do servidor.
2. Inicie o servidor e verifique o console para erros referenciando o arquivo do seu item.
3. Use o spawner de itens do desenvolvedor para dar a si mesmo o `Weapon_Daggers_Thornwood`.
4. Confirme se o modelo, a textura, o ícone e o nome são exibidos corretamente.
5. Ataque um boneco de treino ou uma criatura para verificar se os números de dano correspondem aos valores de `BaseDamage`.
6. Verifique a lista de receitas na Bancada de Armas para encontrar seu item.

**Erros comuns e soluções:**

| Erro | Causa | Solução |
|------|-------|---------|
| `Unknown parent: Template_Weapon_Daggers` | Template não carregado | Verifique se os assets vanilla estão presentes |
| Modelo aparece como cubo padrão | Caminho do `.blockymodel` errado | Confira o caminho em `Model` |
| Receita não aparece na bancada | `BenchRequirement.Id` errado | Use exatamente `Weapon_Bench` |
| Nome mostra a chave bruta | Entrada no `.lang` ausente | Adicione a chave ao `en-US.lang` |

---

## Arquivos Completos

### `YourMod/Assets/Server/Item/Items/MyMod/Weapon_Daggers_Thornwood.json`
```json
{
  "Parent": "Template_Weapon_Daggers",
  "TranslationProperties": {
    "Name": "server.items.Weapon_Daggers_Thornwood.name",
    "Description": "server.items.Weapon_Daggers_Thornwood.description"
  },
  "Model": "Items/Weapons/Dagger/Thornwood.blockymodel",
  "Texture": "Items/Weapons/Dagger/Thornwood_Texture.png",
  "Icon": "Icons/MyMod/Weapon_Daggers_Thornwood.png",
  "Quality": "Uncommon",
  "ItemLevel": 20,
  "MaxDurability": 80,
  "DurabilityLossOnHit": 0.5,
  "Tags": {
    "Type": ["Weapon"],
    "Family": ["Daggers"]
  },
  "Recipe": {
    "Input": [
      {
        "ResourceTypeId": "Wood_Trunk",
        "Quantity": 3
      },
      {
        "ItemId": "Ingredient_Fibre",
        "Quantity": 2
      },
      {
        "ItemId": "Ingredient_Bar_Copper",
        "Quantity": 1
      }
    ],
    "Output": [
      {
        "ItemId": "Weapon_Daggers_Thornwood"
      }
    ],
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Categories": ["Weapon_Daggers"],
        "Id": "Weapon_Bench"
      }
    ],
    "TimeSeconds": 4
  },
  "InteractionVars": {
    "Swing_Left_Damage": {
      "Interactions": [
        {
          "Parent": "Weapon_Daggers_Primary_Swing_Left_Damage",
          "DamageCalculator": {
            "BaseDamage": { "Physical": 4 }
          },
          "DamageEffects": {
            "WorldSoundEventId": "SFX_Daggers_T2_Slash_Impact",
            "LocalSoundEventId": "SFX_Daggers_T2_Slash_Impact"
          }
        }
      ]
    },
    "Swing_Right_Damage": {
      "Interactions": [
        {
          "Parent": "Weapon_Daggers_Primary_Swing_Right_Damage",
          "DamageCalculator": {
            "BaseDamage": { "Physical": 4 }
          },
          "DamageEffects": {
            "WorldSoundEventId": "SFX_Daggers_T2_Slash_Impact",
            "LocalSoundEventId": "SFX_Daggers_T2_Slash_Impact"
          }
        }
      ]
    },
    "Stab_Left_Damage": {
      "Interactions": [
        {
          "Parent": "Weapon_Daggers_Primary_Stab_Left_Damage",
          "DamageCalculator": {
            "BaseDamage": { "Physical": 9 }
          },
          "DamageEffects": {
            "WorldSoundEventId": "SFX_Daggers_T2_Slash_Impact",
            "LocalSoundEventId": "SFX_Daggers_T2_Slash_Impact"
          }
        }
      ]
    },
    "Stab_Right_Damage": {
      "Interactions": [
        {
          "Parent": "Weapon_Daggers_Primary_Stab_Right_Damage",
          "DamageCalculator": {
            "BaseDamage": { "Physical": 12 }
          },
          "DamageEffects": {
            "WorldSoundEventId": "SFX_Daggers_T2_Slash_Impact",
            "LocalSoundEventId": "SFX_Daggers_T2_Slash_Impact"
          }
        }
      ]
    }
  }
}
```

### `YourMod/Assets/Languages/en-US.lang`
```
server.items.Weapon_Daggers_Thornwood.name=Thornwood Dagger
server.items.Weapon_Daggers_Thornwood.description=A light blade carved from thornwood. Fast and precise.
```

---

## Próximos Passos

- [Criar um Bloco Personalizado](/hytale-modding-docs/tutorials/beginner/create-a-block) — adicione um bloco posicionável que dropa de NPCs
- [Criar um NPC Personalizado](/hytale-modding-docs/tutorials/beginner/create-an-npc) — crie uma criatura que dropa sua nova arma
- [Fundamentos de JSON](/hytale-modding-docs/getting-started/json-basics) — referência para herança de templates e encadeamento de interações
