---
title: Crie Instâncias de Dungeon Personalizadas
description: Como criar instâncias de dungeon personalizadas com prefabs, portais, configurações de jogabilidade, tabelas de loot e encontros com NPCs.
---

## Objetivo

Construir uma instância de dungeon personalizada completa chamada **Sunken Vault** (Cofre Submerso) — uma área instanciada autocontida na qual os jogadores entram através de um portal, lutam em encontros com NPCs, coletam loot de contêineres e saem ao morrer ou completar. Você criará uma configuração de jogabilidade para a instância, definirá pontos de entrada e saída de portal, configurará tabelas de loot da dungeon e conectará spawns de NPCs dentro da instância.

## Pré-requisitos

- Uma pasta de mod com um `manifest.json` válido (veja [Configure Seu Ambiente de Desenvolvimento](/hytale-modding-docs/tutorials/beginner/setup-dev-environment))
- Familiaridade com herança de templates JSON (veja [Herança e Templates](/hytale-modding-docs/reference/concepts/inheritance-and-templates))
- Entendimento de papéis de NPC e regras de spawn (veja [Crie um NPC Personalizado](/hytale-modding-docs/tutorials/beginner/create-an-npc))
- Entendimento de tabelas de drop (veja [Tabelas de Drop](/hytale-modding-docs/reference/economy-and-progression/drop-tables))

---

## Como Instâncias Funcionam

Instâncias do Hytale são zonas de mundo isoladas com suas próprias regras de jogabilidade. Quando um jogador entra em um portal vinculado a uma instância, o engine cria (ou reutiliza) uma cópia dessa instância e teleporta o jogador para dentro dela. Instâncias têm sua própria configuração de jogabilidade que pode sobrescrever penalidades de morte, interação com blocos e comportamento de respawn independentemente do overworld.

Componentes principais:

| Componente | Localização do Arquivo | Propósito |
|-----------|----------------------|-----------|
| Configuração de Jogabilidade | `Server/GameplayConfigs/` | Regras para morte, quebra de blocos, respawn dentro da instância |
| Tipo de Portal | `Server/PortalTypes/` | Define o bloco de portal que transporta jogadores para a instância |
| Ambiente | `Server/Environments/` | Clima e atmosfera dentro da instância |
| Regras de Spawn de NPC | `Server/NPC/Spawn/` | Quais NPCs aparecem dentro da instância |
| Tabelas de Drop | `Server/Drops/` | Loot de contêineres e NPCs na instância |

---

## Passo 1: Criar a Configuração de Jogabilidade da Instância

Configurações de jogabilidade de instância herdam de `Default_Instance` que desabilita quebra de blocos e previne perda de itens na morte. O jogador é ejetado da instância quando morre.

Crie `YourMod/Assets/Server/GameplayConfigs/SunkenVault.json`:

```json
{
  "Parent": "Default_Instance",
  "World": {
    "AllowBlockBreaking": false,
    "AllowBlockGathering": false,
    "DaytimeDurationSeconds": 0,
    "NighttimeDurationSeconds": 0
  },
  "Death": {
    "LoseItems": false,
    "RespawnController": {
      "Type": "ExitInstance"
    }
  },
  "Player": {
    "MovementConfig": "Default",
    "HitboxCollisionConfig": "SoftCollision",
    "ArmorVisibilityOption": "All"
  }
}
```

### Campos da configuração explicados

| Campo | Propósito |
|-------|-----------|
| `Parent` | Herda todos os padrões de `Default_Instance`, que já desabilita interação com blocos |
| `AllowBlockBreaking` | Impede jogadores de destruir a estrutura da dungeon |
| `AllowBlockGathering` | Impede coleta de recursos dentro da dungeon |
| `DaytimeDurationSeconds: 0` | Congela o ciclo dia/noite para que a dungeon tenha um estado de iluminação fixo |
| `LoseItems: false` | Jogadores mantêm todos os itens ao morrer dentro da instância |
| `RespawnController.Type: "ExitInstance"` | Morrer ejeta o jogador de volta ao local do portal no overworld |

Compare com o `Default_Instance.json` vanilla que usa o mesmo padrão. Sua configuração adiciona o ciclo de tempo congelado e configurações explícitas do jogador.

---

## Passo 2: Criar o Ambiente da Instância

O ambiente da instância controla clima e atmosfera. Para uma dungeon, você tipicamente quer um único clima estático sem variação.

Crie `YourMod/Assets/Server/Environments/SunkenVault.json`:

```json
{
  "WaterTint": "#0a3d6b",
  "SpawnDensity": 0.8,
  "Tags": {
    "Dungeon": [],
    "SunkenVault": []
  },
  "WeatherForecasts": {
    "0":  [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "1":  [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "2":  [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "3":  [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "4":  [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "5":  [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "6":  [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "7":  [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "8":  [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "9":  [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "10": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "11": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "12": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "13": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "14": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "15": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "16": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "17": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "18": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "19": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "20": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "21": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "22": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "23": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }]
  }
}
```

Usar um único ID de clima com peso 100 para cada hora cria uma atmosfera constante. O `WaterTint` dá à água subterrânea um tom azul-esverdeado escuro apropriado para uma dungeon submersa. `SpawnDensity` em `0.8` reduz levemente os spawns ambientais de NPCs comparado ao padrão do overworld de `0.5` (valores mais altos significam mais spawns em conteúdo instanciado onde encontros são controlados).

---

## Passo 3: Definir o Tipo de Portal

Tipos de portal definem o bloco com o qual os jogadores interagem para entrar na instância. O portal referencia a configuração de jogabilidade e o ambiente que você criou.

Crie `YourMod/Assets/Server/PortalTypes/Portal_SunkenVault.json`:

```json
{
  "InstanceType": "SunkenVault",
  "GameplayConfig": "SunkenVault",
  "Environment": "SunkenVault",
  "MaxPlayers": 4,
  "PortalAppearance": "Portal_Dungeon",
  "SpawnOffset": {
    "X": 0,
    "Y": 1,
    "Z": 3
  },
  "ExitOffset": {
    "X": 0,
    "Y": 1,
    "Z": -3
  },
  "CooldownSeconds": 30,
  "RequiredItemToEnter": "Key_SunkenVault",
  "ConsumeRequiredItem": true
}
```

### Campos do portal explicados

| Campo | Propósito |
|-------|-----------|
| `InstanceType` | Identificador único para este tipo de instância. Deve corresponder em todos os arquivos de configuração relacionados |
| `GameplayConfig` | Referencia o ID do arquivo de configuração de jogabilidade (nome do arquivo sem `.json`) |
| `Environment` | Referencia o ID do arquivo de ambiente |
| `MaxPlayers` | Máximo de jogadores simultâneos permitidos em uma cópia da instância |
| `PortalAppearance` | Visual do lado do cliente para o bloco do portal |
| `SpawnOffset` | Onde os jogadores aparecem em relação à origem da instância ao entrar |
| `ExitOffset` | Onde os jogadores aparecem em relação ao portal do overworld ao sair |
| `CooldownSeconds` | Segundos mínimos antes de um jogador poder reentrar após sair |
| `RequiredItemToEnter` | ID do item que o jogador deve ter no inventário para usar o portal |
| `ConsumeRequiredItem` | Se o item necessário é consumido na entrada |

Para criar um portal sem requisito de chave, omita tanto `RequiredItemToEnter` quanto `ConsumeRequiredItem`.

---

## Passo 4: Criar Tabelas de Loot da Dungeon

Dungeons precisam de tabelas de loot para contêineres de tesouro posicionados dentro da instância. Use os tipos de contêiner `Multiple` e `Choice` para criar pools de loot variados.

Crie `YourMod/Assets/Server/Drops/Items/SunkenVault_Chest.json`:

```json
{
  "Container": {
    "Type": "Multiple",
    "Containers": [
      {
        "Type": "Choice",
        "Containers": [
          {
            "Type": "Single",
            "Weight": 60,
            "Item": {
              "ItemId": "Weapon_Sword_Copper",
              "QuantityMin": 1,
              "QuantityMax": 1
            }
          },
          {
            "Type": "Single",
            "Weight": 30,
            "Item": {
              "ItemId": "Weapon_Sword_Iron",
              "QuantityMin": 1,
              "QuantityMax": 1
            }
          },
          {
            "Type": "Single",
            "Weight": 10,
            "Item": {
              "ItemId": "Weapon_Sword_Gold",
              "QuantityMin": 1,
              "QuantityMax": 1
            }
          }
        ]
      },
      {
        "Type": "Choice",
        "Containers": [
          {
            "Type": "Single",
            "Weight": 70,
            "Item": {
              "ItemId": "Food_Bread",
              "QuantityMin": 2,
              "QuantityMax": 5
            }
          },
          {
            "Type": "Empty",
            "Weight": 30
          }
        ]
      },
      {
        "Type": "Choice",
        "Containers": [
          {
            "Type": "Single",
            "Weight": 50,
            "Item": {
              "ItemId": "Weapon_Arrow_Crude",
              "QuantityMin": 5,
              "QuantityMax": 15
            }
          },
          {
            "Type": "Empty",
            "Weight": 50
          }
        ]
      }
    ]
  }
}
```

Esta tabela de loot usa uma raiz `Multiple` para avaliar três pools independentes:

1. **Pool de armas** (garantido) — sempre dropa uma arma, com peso para tiers mais baixos
2. **Pool de comida** (70% de chance) — às vezes inclui pão para cura
3. **Pool de munição** (50% de chance) — às vezes inclui flechas

O tipo `Empty` com seu próprio peso cria a possibilidade de nenhum drop daquele pool. Compare este padrão com o `Barrels.json` vanilla que usa `Empty` com peso 800 para tornar drops raros.

Crie uma tabela de loot de nível de chefe para a sala final:

`YourMod/Assets/Server/Drops/Items/SunkenVault_BossChest.json`:

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
              "ItemId": "Weapon_Sword_Gold",
              "QuantityMin": 1,
              "QuantityMax": 1
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
              "ItemId": "Ingredient_Crystal",
              "QuantityMin": 3,
              "QuantityMax": 8
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
              "ItemId": "Food_Bread",
              "QuantityMin": 5,
              "QuantityMax": 10
            }
          }
        ]
      }
    ]
  }
}
```

---

## Passo 5: Criar Encontros com NPCs na Dungeon

Defina NPCs que surgem dentro da dungeon. NPCs de instância tipicamente usam templates agressivos com mais vida do que suas versões do overworld.

Crie `YourMod/Assets/Server/NPC/Roles/MyMod/SunkenVault_Guardian.json`:

```json
{
  "Type": "Variant",
  "Reference": "Template_Intelligent",
  "Modify": {
    "Appearance": "Skeleton_Warrior",
    "DropList": "Drop_SunkenVault_Guardian",
    "MaxHealth": 120,
    "MaxSpeed": 6,
    "ViewRange": 18,
    "HearingRange": 14,
    "AlertedRange": 24,
    "DefaultPlayerAttitude": "Hostile",
    "IsMemory": true,
    "MemoriesCategory": "Undead",
    "MemoriesNameOverride": "Vault Guardian",
    "NameTranslationKey": {
      "Compute": "NameTranslationKey"
    }
  },
  "Parameters": {
    "NameTranslationKey": {
      "Value": "server.npcRoles.SunkenVault_Guardian.name",
      "Description": "Translation key for NPC name display"
    }
  }
}
```

Crie a tabela de drop do guardião em `YourMod/Assets/Server/Drops/NPCs/Intelligent/Drop_SunkenVault_Guardian.json`:

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
              "ItemId": "Ingredient_Bone",
              "QuantityMin": 1,
              "QuantityMax": 3
            }
          }
        ]
      },
      {
        "Type": "Choice",
        "Containers": [
          {
            "Type": "Single",
            "Weight": 15,
            "Item": {
              "ItemId": "Ingredient_Crystal",
              "QuantityMin": 1,
              "QuantityMax": 1
            }
          },
          {
            "Type": "Empty",
            "Weight": 85
          }
        ]
      }
    ]
  }
}
```

---

## Passo 6: Criar Regras de Spawn da Instância

Regras de spawn de instância funcionam como spawns do overworld mas referenciam o ambiente da instância. Crie regras de spawn para os NPCs guardiões do Sunken Vault.

Crie `YourMod/Assets/Server/NPC/Spawn/Instance/Spawns_SunkenVault.json`:

```json
{
  "Environments": [
    "SunkenVault"
  ],
  "NPCs": [
    {
      "Weight": 8,
      "SpawnBlockSet": "Soil",
      "Id": "SunkenVault_Guardian",
      "Flock": "Group_Small"
    }
  ],
  "DayTimeRange": [0, 24]
}
```

Definir `DayTimeRange` como `[0, 24]` garante que guardiões surjam independentemente do horário, o que é importante porque a instância tem um ciclo de tempo congelado. O `Flock: "Group_Small"` gera guardiões em pequenos grupos de 2-4, criando encontros significativos.

---

## Passo 7: Adicionar Chaves de Tradução

Crie `YourMod/Assets/Languages/en-US.lang` (ou adicione ao seu arquivo existente):

```
server.npcRoles.SunkenVault_Guardian.name=Vault Guardian
```

---

## Passo 8: Testar a Dungeon

1. Coloque sua pasta de mod no diretório de mods do servidor.
2. Inicie o servidor e verifique o console para erros sobre referências ausentes.
3. Coloque o bloco de portal no overworld usando as ferramentas de desenvolvedor.
4. Entre no portal e verifique se você é transportado para a instância.
5. Confirme que NPCs surgem e têm comportamento hostil.
6. Abra um contêiner de loot e verifique se os drops correspondem à sua tabela de loot.
7. Morra dentro da instância e confirme que você é ejetado para o overworld sem perder itens.

### Erros comuns e correções

| Erro | Causa | Correção |
|------|-------|----------|
| `Unknown gameplay config: SunkenVault` | Arquivo de configuração não encontrado | Verifique se o arquivo está em `GameplayConfigs/SunkenVault.json` |
| `Unknown environment: SunkenVault` | ID de ambiente incompatível | Certifique-se de que o nome do arquivo de ambiente corresponde ao campo `Environment` do portal |
| `Unknown portal type` | Tipo de portal não registrado | Verifique se `PortalTypes/Portal_SunkenVault.json` existe e tem JSON válido |
| Jogadores não ejetados na morte | `RespawnController` errado | Confirme que `"Type": "ExitInstance"` está definido na configuração de morte |
| NPCs não surgem | Tag de ambiente incompatível | Verifique se o array `Environments` do arquivo de spawn corresponde ao nome de arquivo do ambiente da instância |
| Tabela de loot vazia | Caminho da tabela de drop errado | Confirme que o caminho do arquivo corresponde ao padrão de ID do `DropList` |

---

## Listagem Completa de Arquivos

```
YourMod/
  Assets/
    Server/
      GameplayConfigs/
        SunkenVault.json
      Environments/
        SunkenVault.json
      PortalTypes/
        Portal_SunkenVault.json
      Drops/
        Items/
          SunkenVault_Chest.json
          SunkenVault_BossChest.json
        NPCs/
          Intelligent/
            Drop_SunkenVault_Guardian.json
      NPC/
        Roles/
          MyMod/
            SunkenVault_Guardian.json
        Spawn/
          Instance/
            Spawns_SunkenVault.json
    Languages/
      en-US.lang
```

---

## Próximos Passos

- [Árvores de Comportamento de IA de NPCs](/hytale-modding-docs/tutorials/advanced/npc-ai-behavior-trees) — crie IA complexa para chefes de dungeon
- [Sistema de Combate Personalizado](/hytale-modding-docs/tutorials/advanced/custom-combat-system) — adicione tipos de dano personalizados para perigos de dungeon
- [Mods de Geração de Mundo](/hytale-modding-docs/tutorials/advanced/world-generation-mods) — gere entradas de dungeon no overworld
- [Configurações de Jogabilidade](/hytale-modding-docs/reference/game-configuration/gameplay-configs) — referência completa para campos de configuração de instância
- [Tabelas de Drop](/hytale-modding-docs/reference/economy-and-progression/drop-tables) — padrões avançados de tabelas de loot
