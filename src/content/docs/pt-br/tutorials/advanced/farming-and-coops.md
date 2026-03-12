---
title: Sistema Completo de Fazenda
description: Construa um sistema completo de fazenda com galinheiros personalizados, modificadores de crescimento, gerenciamento de animais, tabelas de drop de produção e integração com cultivos.
---

## Objetivo

Construir um sistema completo de fazenda para um animal personalizado chamado **Silkworm** (Bicho-da-seda). Você criará um galinheiro que abriga Silkworms, configurará tabelas de drop de produção, definirá modificadores de crescimento para condições ambientais, criará o papel de NPC do Silkworm com suporte a domesticação e integrará com o sistema de fabricação. Ao final, você terá um ciclo de fazenda autocontido: capturar Silkworms selvagens, colocá-los em um galinheiro e coletar fibra de seda para fabricação.

## Pré-requisitos

- Uma pasta de mod com um `manifest.json` válido (veja [Configure Seu Ambiente de Desenvolvimento](/hytale-modding-docs/tutorials/beginner/setup-dev-environment))
- Entendimento de papéis de NPC (veja [Papéis de NPC](/hytale-modding-docs/reference/npc-system/npc-roles) e [Crie um NPC Personalizado](/hytale-modding-docs/tutorials/beginner/create-an-npc))
- Entendimento de tabelas de drop (veja [Tabelas de Drop](/hytale-modding-docs/reference/economy-and-progression/drop-tables))
- Familiaridade com o sistema de fazenda (veja [Fazenda e Galinheiros](/hytale-modding-docs/reference/economy-and-progression/farming-coops))

---

## Como o Sistema de Fazenda Funciona

O sistema de fazenda tem dois componentes principais:

### Galinheiros

Galinheiros são estruturas que abrigam animais NPCs e produzem drops em um temporizador. Cada galinheiro define:
- Quais grupos de NPC podem ser colocados dentro
- Número máximo de residentes
- O que cada espécie produz (via referências de tabela de drop)
- Quando residentes perambulam livremente vs ficam dentro

### Modificadores

Modificadores de crescimento são condições ambientais que aceleram ou desaceleram os ciclos de produção. Quatro tipos de modificador existem:

| Modificador | Fonte | Efeito |
|-------------|-------|--------|
| `Water` | Blocos de água próximos ou clima de chuva | Multiplica taxa de crescimento (vanilla: 2,5x) |
| `Fertilizer` | Item fertilizante aplicado ao galinheiro ou solo | Multiplica taxa de crescimento (vanilla: 2x) |
| `LightLevel` | Luz artificial ou luz solar | Multiplica taxa de crescimento quando há luz suficiente |
| `Darkness` | Ausência de luz | Multiplica taxa de crescimento em condições escuras (para espécies que vivem em cavernas) |

### Ciclo de Produção

```
Animal colocado no galinheiro
    → Temporizador inicia (baseado no intervalo ProduceTimeout)
    → Modificadores se aplicam (Água, Luz, Fertilizante aceleram)
    → Temporizador completa
    → Tabela de drop de produção é rolada
    → Itens aparecem na saída do galinheiro
    → Temporizador reinicia
```

---

## Passo 1: Criar o Papel de NPC do Silkworm

O Silkworm é uma criatura passiva que pode ser domesticada e colocada em galinheiros. Ele usa a base `Template_Beasts_Passive_Critter` para comportamento simples de perambulação e fuga.

Crie `YourMod/Assets/Server/NPC/Roles/MyMod/Silkworm.json`:

```json
{
  "Type": "Variant",
  "Reference": "Template_Beasts_Passive_Critter",
  "Modify": {
    "Appearance": "Gecko",
    "DropList": "Drop_Silkworm",
    "MaxHealth": 8,
    "MaxSpeed": 3,
    "ViewRange": 6,
    "HearingRange": 4,
    "IsTameable": true,
    "TameRoleChange": "Tamed_Silkworm",
    "AttractiveItemSet": ["Plant_Crop_Cotton_Item"],
    "AttractiveItemSetParticles": "Want_Food_Plant",
    "ProduceItem": "Ingredient_Silk_Fibre",
    "ProduceTimeout": ["PT12H", "PT36H"],
    "IsMemory": true,
    "MemoriesCategory": "Critter",
    "MemoriesNameOverride": "Silkworm",
    "NameTranslationKey": {
      "Compute": "NameTranslationKey"
    }
  },
  "Parameters": {
    "NameTranslationKey": {
      "Value": "server.npcRoles.Silkworm.name",
      "Description": "Translation key for NPC name display"
    }
  }
}
```

### Campos principais de fazenda

| Campo | Valor | Propósito |
|-------|-------|-----------|
| `IsTameable: true` | Habilita interação de domesticação | Jogadores podem domesticar Silkworms selvagens alimentando com itens atrativos |
| `TameRoleChange` | `"Tamed_Silkworm"` | Quando domesticado, o NPC muda para uma variante domesticada com comportamento diferente |
| `AttractiveItemSet` | `["Plant_Crop_Cotton_Item"]` | Silkworms são atraídos por algodão — segurar algodão perto de um inicia o processo de domesticação |
| `ProduceItem` | `"Ingredient_Silk_Fibre"` | Silkworms perambulando livremente periodicamente dropam fibra de seda no chão |
| `ProduceTimeout` | `["PT12H", "PT36H"]` | Duração ISO 8601: produz a cada 12-36 horas do jogo quando perambulando livremente |

Compare com a Galinha vanilla que usa `"ProduceItem": "Food_Egg"` e `"ProduceTimeout": ["PT18H", "PT48H"]`.

Crie a variante domesticada em `YourMod/Assets/Server/NPC/Roles/MyMod/Tamed_Silkworm.json`:

```json
{
  "Type": "Variant",
  "Reference": "Template_Beasts_Passive_Critter",
  "Modify": {
    "Appearance": "Gecko",
    "DropList": "Drop_Silkworm",
    "MaxHealth": 8,
    "MaxSpeed": 2,
    "ViewRange": 4,
    "HearingRange": 3,
    "DefaultPlayerAttitude": "Neutral",
    "ProduceItem": "Ingredient_Silk_Fibre",
    "ProduceTimeout": ["PT8H", "PT24H"],
    "IsMemory": false,
    "NameTranslationKey": {
      "Compute": "NameTranslationKey"
    }
  },
  "Parameters": {
    "NameTranslationKey": {
      "Value": "server.npcRoles.Tamed_Silkworm.name",
      "Description": "Translation key for NPC name display"
    }
  }
}
```

A variante domesticada tem um tempo de produção mais curto (8-24 horas vs 12-36), velocidade mais lenta (menos provável de perambular para longe) e uma atitude neutra em relação aos jogadores (não fugirá ao ser abordado).

---

## Passo 2: Criar Grupos de NPC

Grupos de NPC definem quais animais um galinheiro aceita. Galinheiros referenciam grupos, não papéis individuais.

Crie `YourMod/Assets/Server/NPC/Groups/Silkworm.json`:

```json
{
  "Id": "Silkworm",
  "Members": [
    "Silkworm",
    "Tamed_Silkworm"
  ]
}
```

Ambas as variantes selvagem e domesticada pertencem ao mesmo grupo. Isso significa que o galinheiro aceita ambas — um Silkworm selvagem colocado em um galinheiro é tratado da mesma forma que um domesticado para fins de produção.

---

## Passo 3: Criar o Galinheiro do Silkworm

A definição do galinheiro especifica capacidade, grupos de NPC aceitos, tabelas de drop de produção e horários de perambulação.

Crie `YourMod/Assets/Server/Farming/Coops/Coop_Silkworm.json`:

```json
{
  "MaxResidents": 8,
  "ProduceDrops": {
    "Silkworm": "Drop_Silkworm_Produce",
    "Tamed_Silkworm": "Drop_Silkworm_Produce"
  },
  "ResidentRoamTime": [8, 16],
  "ResidentSpawnOffset": {
    "X": 0,
    "Y": 0,
    "Z": 2
  },
  "AcceptedNpcGroups": [
    "Silkworm"
  ],
  "CaptureWildNPCsInRange": true,
  "WildCaptureRadius": 8
}
```

### Decisões de design do galinheiro

| Campo | Valor | Justificativa |
|-------|-------|---------------|
| `MaxResidents: 8` | Maior que o galinheiro de Galinha (6) | Silkworms são pequenos, mais podem caber |
| `ProduceDrops` | Mapeia ambas variantes para a mesma tabela de drop | Selvagens e domesticados produzem os mesmos itens |
| `ResidentRoamTime: [8, 16]` | Perambulação apenas durante o dia | Silkworms perambulam das 8h às 16h, ficam dentro nos outros horários |
| `CaptureWildNPCsInRange: true` | Captura automaticamente Silkworms selvagens próximos | Conveniência: Silkworms selvagens perambulando perto do galinheiro são automaticamente capturados |
| `WildCaptureRadius: 8` | Raio de captura de 8 blocos | Alcance moderado — jogadores precisam atrair Silkworms razoavelmente perto |

Compare com o galinheiro de Galinha vanilla:
- Galinheiro de Galinha tem `MaxResidents: 6`, `WildCaptureRadius: 10`
- Galinheiro de Galinha aceita 3 grupos de NPC: `Chicken`, `Chicken_Desert`, `Skrill`
- Galinheiro de Silkworm é mais simples com um grupo mas maior capacidade

---

## Passo 4: Criar Tabelas de Drop de Produção

A tabela de drop de produção define quais itens um residente do galinheiro gera a cada ciclo de produção.

Crie `YourMod/Assets/Server/Drops/NPCs/Critter/Drop_Silkworm_Produce.json`:

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
              "ItemId": "Ingredient_Silk_Fibre",
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
              "ItemId": "Ingredient_Silk_Thread",
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

A cada ciclo de produção, um Silkworm sempre dropa 1-3 Fibra de Seda e tem 15% de chance de também dropar 1 Fio de Seda (um material de fabricação de nível superior).

Também crie a tabela de drop por matar o NPC em `YourMod/Assets/Server/Drops/NPCs/Critter/Drop_Silkworm.json`:

```json
{
  "Container": {
    "Type": "Choice",
    "Containers": [
      {
        "Type": "Single",
        "Weight": 80,
        "Item": {
          "ItemId": "Ingredient_Silk_Fibre",
          "QuantityMin": 1,
          "QuantityMax": 1
        }
      },
      {
        "Type": "Empty",
        "Weight": 20
      }
    ]
  }
}
```

Matar um Silkworm tem 80% de chance de dropar 1 Fibra de Seda — muito menos eficiente do que criá-los em um galinheiro (1-3 fibras por ciclo mais chance de fio). Isso incentiva o ciclo de fazenda em vez da caça.

---

## Passo 5: Criar Modificadores de Crescimento

Modificadores de crescimento aceleram ciclos de produção quando condições ambientais são atendidas. Crie modificadores que afetam a produção de Silkworm.

Os modificadores vanilla em `Assets/Server/Farming/Modifiers/` já se aplicam globalmente. Você pode criar modificadores adicionais para seu sistema de fazenda ou depender dos vanilla.

Para Silkworms, crie um modificador de escuridão já que eles preferem ambientes sombreados:

Crie `YourMod/Assets/Server/Farming/Modifiers/Darkness_Silkworm.json`:

```json
{
  "Type": "Darkness",
  "Modifier": 1.8
}
```

Isso dá aos Silkworms um multiplicador de taxa de crescimento de 1,8x quando seu galinheiro está em uma área escura (subterrânea ou em uma estrutura coberta). Compare com o modificador vanilla de Luz que dá 2x para áreas bem iluminadas — Silkworms são o oposto, preferindo escuridão.

O modificador vanilla de Água (`Modifier: 2.5`) e o modificador de Fertilizante (`Modifier: 2`) também se aplicam a galinheiros. Um galinheiro de Silkworm perto de água em uma caverna escura se beneficiaria de ambos:

- Taxa base de produção: 1x
- Bônus de escuridão: 1,8x
- Bônus de água: 2,5x
- Combinado: aproximadamente 4,5x produção mais rápida

### Entendendo o acúmulo de modificadores

Modificadores se aplicam multiplicativamente ao temporizador base de produção. Se o `ProduceTimeout` de um Silkworm é 24 horas do jogo na taxa base:

| Modificadores ativos | Tempo efetivo de produção |
|---------------------|--------------------------|
| Nenhum | 24 horas |
| Escuridão (1,8x) | ~13,3 horas |
| Água (2,5x) | ~9,6 horas |
| Escuridão + Água | ~5,3 horas |
| Escuridão + Água + Fertilizante (2x) | ~2,7 horas |

---

## Passo 6: Criar Regras de Spawn para Silkworms Selvagens

Silkworms selvagens precisam de regras de spawn para que jogadores possam encontrá-los e capturá-los. Coloque-os em ambientes de floresta onde surgem em pequenos grupos.

Crie `YourMod/Assets/Server/NPC/Spawn/World/Zone1/Spawns_Zone1_Silkworm.json`:

```json
{
  "Environments": [
    "Env_Zone1_Forests",
    "Env_Zone1_Autumn",
    "Env_Zone1_Azure"
  ],
  "NPCs": [
    {
      "Weight": 2,
      "SpawnBlockSet": "Soil",
      "Id": "Silkworm",
      "Flock": "One_Or_Two"
    }
  ],
  "DayTimeRange": [6, 14]
}
```

Peso 2 torna Silkworms incomuns (o Esquilo vanilla usa peso 6). Eles só aparecem durante a manhã e início da tarde, e surgem em pares no máximo — tornando-os um recurso que vale a pena procurar.

---

## Passo 7: Criar Integração com Fabricação

Conecte a produção da fazenda ao sistema de fabricação. Crie itens que usam Fibra de Seda e Fio de Seda.

Crie `YourMod/Assets/Server/Item/Items/MyMod/Ingredient_Silk_Fibre.json`:

```json
{
  "TranslationProperties": {
    "Name": "server.items.Ingredient_Silk_Fibre.name",
    "Description": "server.items.Ingredient_Silk_Fibre.description"
  },
  "Quality": "Common",
  "Icon": "Icons/ItemsGenerated/Ingredient_Silk_Fibre.png",
  "Categories": ["Items.Ingredients"],
  "MaxStack": 50,
  "DropOnDeath": true,
  "ResourceTypes": [
    { "Id": "Fibre" }
  ]
}
```

Crie `YourMod/Assets/Server/Item/Items/MyMod/Ingredient_Silk_Thread.json`:

```json
{
  "TranslationProperties": {
    "Name": "server.items.Ingredient_Silk_Thread.name",
    "Description": "server.items.Ingredient_Silk_Thread.description"
  },
  "Quality": "Uncommon",
  "Icon": "Icons/ItemsGenerated/Ingredient_Silk_Thread.png",
  "Categories": ["Items.Ingredients"],
  "MaxStack": 25,
  "DropOnDeath": true,
  "ResourceTypes": [
    { "Id": "Thread" }
  ],
  "Recipe": {
    "Input": [
      { "ItemId": "Ingredient_Silk_Fibre", "Quantity": 3 }
    ],
    "OutputQuantity": 1,
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Id": "Loom",
        "Categories": ["Textiles"]
      }
    ],
    "TimeSeconds": 4
  }
}
```

Fio de Seda pode ser fabricado a partir de 3 Fibras de Seda em um Tear, ou obtido raramente da produção do galinheiro. Isso cria dois caminhos: jogadores podem esperar por drops sortudos ou fabricar fio ativamente a partir de fibra.

---

## Passo 8: Adicionar Chaves de Tradução

Adicione a `YourMod/Assets/Languages/en-US.lang`:

```
server.npcRoles.Silkworm.name=Silkworm
server.npcRoles.Tamed_Silkworm.name=Silkworm
server.items.Ingredient_Silk_Fibre.name=Silk Fibre
server.items.Ingredient_Silk_Fibre.description=Fine fibre produced by silkworms. Used in textile crafting.
server.items.Ingredient_Silk_Thread.name=Silk Thread
server.items.Ingredient_Silk_Thread.description=Woven silk thread. A premium crafting material for light armour and decoration.
```

---

## Passo 9: Testar o Sistema de Fazenda

1. Coloque sua pasta de mod no diretório de mods do servidor e inicie o servidor.
2. Viaje para um bioma de floresta da Zona 1 e procure Silkworms selvagens durante a manhã.
3. Segure itens de algodão perto de um Silkworm para testar a mecânica de atração e domesticação.
4. Construa ou posicione uma estrutura de galinheiro e teste estas interações:

| Teste | Resultado esperado |
|-------|-------------------|
| Colocar Silkworm domesticado no galinheiro | Silkworm aparece dentro, contagem de residentes aumenta |
| Colocar 9º Silkworm (acima da capacidade) | Galinheiro rejeita — MaxResidents é 8 |
| Esperar pelo ciclo de produção | Fibra de Seda (1-3) aparece na saída do galinheiro. 15% de chance de Fio de Seda |
| Verificar horários de perambulação | Silkworms perambulam livremente das 8h às 16h, retornam ao abrigo nos outros horários |
| Colocar galinheiro perto de água | Temporizador de produção deve acelerar (modificador de Água 2,5x) |
| Colocar galinheiro no subterrâneo | Modificador de Escuridão se aplica (1,8x) |
| Silkworm selvagem perambula dentro de 8 blocos | Capturado automaticamente no galinheiro (CaptureWildNPCsInRange) |
| Matar um Silkworm selvagem | 80% de chance de 1 Fibra de Seda no drop |
| Fabricar Fio de Seda no Tear | 3 Fibras de Seda = 1 Fio de Seda |

### Solução de Problemas

| Problema | Causa | Correção |
|----------|-------|----------|
| Galinheiro não aceita Silkworm | Grupo de NPC incompatível | Certifique-se de que `AcceptedNpcGroups` corresponde ao ID do grupo em `Groups/Silkworm.json` |
| Sem produção na saída | ID da tabela de drop incompatível | Verifique se as chaves de `ProduceDrops` correspondem aos nomes de arquivo dos papéis de NPC |
| Produção muito lenta | Nenhum modificador ativo | Coloque o galinheiro perto de água ou na escuridão para ativar modificadores |
| Captura selvagem não funciona | Raio muito pequeno | Aumente `WildCaptureRadius` ou atraia Silkworms para mais perto |
| Domesticação falha | Item atrativo errado | Confirme que `AttractiveItemSet` contém um ID de item válido |
| Silkworms não surgem | Ambiente incompatível | Verifique se o array `Environments` do arquivo de spawn contém IDs de ambiente válidos |

---

## Listagem Completa de Arquivos

```
YourMod/
  Assets/
    Server/
      NPC/
        Roles/
          MyMod/
            Silkworm.json
            Tamed_Silkworm.json
        Groups/
          Silkworm.json
        Spawn/
          World/
            Zone1/
              Spawns_Zone1_Silkworm.json
      Farming/
        Coops/
          Coop_Silkworm.json
        Modifiers/
          Darkness_Silkworm.json
      Drops/
        NPCs/
          Critter/
            Drop_Silkworm.json
            Drop_Silkworm_Produce.json
      Item/
        Items/
          MyMod/
            Ingredient_Silk_Fibre.json
            Ingredient_Silk_Thread.json
    Languages/
      en-US.lang
```

---

## Próximos Passos

- [Crie um Item Personalizado](/hytale-modding-docs/tutorials/beginner/create-an-item) — crie armaduras e ferramentas a partir de Fio de Seda
- [Receitas](/hytale-modding-docs/reference/crafting-system/recipes) — referência completa de receitas de fabricação
- [Fazenda e Galinheiros](/hytale-modding-docs/reference/economy-and-progression/farming-coops) — referência completa do schema de galinheiros
- [Tabelas de Drop](/hytale-modding-docs/reference/economy-and-progression/drop-tables) — padrões avançados de tabelas de loot
- [Grupos de NPC](/hytale-modding-docs/reference/npc-system/npc-groups) — definições de grupos de NPC
- [Sistema de Clima](/hytale-modding-docs/reference/world-and-environment/weather-system) — IDs de clima usados em condições do modificador de Água
