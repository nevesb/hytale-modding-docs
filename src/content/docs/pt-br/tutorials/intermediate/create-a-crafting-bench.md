---
title: Criar uma Bancada de Criação Personalizada
description: Tutorial passo a passo para adicionar uma Bigorna de Cristal com modelo personalizado, categorias de receitas e interface de criação.
sidebar:
  order: 4
---

## Objetivo

Construa uma **Bigorna de Cristal** — uma bancada de criação personalizada que os jogadores podem colocar no mundo e usar para forjar armas de cristal. Você vai definir o item da bancada com um `BlockType` inline, configurar categorias de criação, definir o `State` necessário para a interface de criação e adicionar chaves de tradução.

## O Que Você Vai Aprender

- Como as bancadas de criação são definidas usando a propriedade de bloco `Bench`
- Como o `State` com `Id: "crafting"` é **obrigatório** para que a interface da bancada abra
- Como criar categorias que organizam receitas na interface da bancada
- Como os níveis de tier e o `CraftingTimeReductionModifier` controlam a velocidade de criação
- Como as receitas de itens referenciam uma bancada via `BenchRequirement`

## Pré-requisitos

- Uma pasta de mod com um `manifest.json` válido (veja [Configurar o Ambiente de Desenvolvimento](/hytale-modding-docs/pt-br/tutorials/beginner/setup-dev-environment))
- Familiaridade com definições de blocos (veja [Criar um Bloco Personalizado](/hytale-modding-docs/pt-br/tutorials/beginner/create-a-block))
- Familiaridade com definições de itens (veja [Criar um Item Personalizado](/hytale-modding-docs/pt-br/tutorials/beginner/create-an-item))

**Repositório do mod de exemplo:** [hytale-mods-custom-bench](https://github.com/nevesb/hytale-mods-custom-bench)

---

## Visão Geral das Bancadas de Criação

As bancadas de criação no Hytale são **itens** que contêm um `BlockType` inline com uma configuração `Bench`. Diferente de blocos puros que precisam de um JSON de Bloco separado e de uma entrada em `BlockTypeList`, as bancadas definem tudo em um único arquivo JSON de Item — o mesmo padrão usado pelas bancadas vanilla como `Bench_Weapon` e `Bench_Armory`.

Principais diferenças em relação a blocos comuns:
- **Nenhum JSON de Bloco separado** em `Server/Item/Block/Blocks/`
- **Nenhuma entrada em `BlockTypeList`** necessária
- O bloco `State` com `Id: "crafting"` é **obrigatório** para que a interface de criação funcione
- O objeto `Bench` define o tipo de criação, categorias e níveis de tier

---

## Passo 1: Configurar a Estrutura de Arquivos do Mod

```text
CreateACraftingBench/
├── manifest.json
├── Common/
│   ├── Blocks/
│   │   └── HytaleModdingManual/
│   │       └── Armory_Crystal_Glow.blockymodel
│   └── BlockTextures/
│       └── HytaleModdingManual/
│           └── Armory_Crystal_Glow.png
└── Server/
    ├── Item/
    │   └── Items/
    │       └── HytaleModdingManual/
    │           └── Bench_Armory_Crystal_Glow.json
    └── Languages/
        ├── en-US/
        │   └── server.lang
        ├── es/
        │   └── server.lang
        └── pt-BR/
            └── server.lang
```

### manifest.json

```json
{
  "Group": "HytaleModdingManual",
  "Name": "CreateACraftingBench",
  "Version": "1.0.0",
  "Description": "Crystal Anvil crafting bench for forging crystal weapons",
  "Authors": [
    {
      "Name": "HytaleModdingManual"
    }
  ],
  "Dependencies": {},
  "OptionalDependencies": {},
  "IncludesAssetPack": true
}
```

Note que `IncludesAssetPack` é `true` porque temos assets Common (modelo e textura).

---

## Passo 2: Criar a Definição do Item da Bancada

Crie a bancada em `Server/Item/Items/HytaleModdingManual/Bench_Armory_Crystal_Glow.json`:

```json
{
  "TranslationProperties": {
    "Name": "server.items.Bench_Armory_Crystal_Glow.name",
    "Description": "server.items.Bench_Armory_Crystal_Glow.description"
  },
  "Quality": "Rare",
  "Icon": "Icons/ItemsGenerated/Bench_Armory_Crystal_Glow.png",
  "Categories": [
    "Furniture.Benches"
  ],
  "Recipe": {
    "TimeSeconds": 10.0,
    "KnowledgeRequired": false,
    "Input": [
      {
        "ItemId": "Ore_Crystal_Glow",
        "Quantity": 3
      },
      {
        "ItemId": "Wood_Enchanted_Trunk",
        "Quantity": 10
      },
      {
        "ItemId": "Ingredient_Bar_Gold",
        "Quantity": 5
      }
    ],
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Categories": [
          "Workbench_Crafting"
        ],
        "Id": "Workbench",
        "RequiredTierLevel": 2
      }
    ]
  },
  "BlockType": {
    "Material": "Solid",
    "DrawType": "Model",
    "Opacity": "Transparent",
    "CustomModel": "Blocks/HytaleModdingManual/Armory_Crystal_Glow.blockymodel",
    "CustomModelTexture": [
      {
        "Texture": "BlockTextures/HytaleModdingManual/Armory_Crystal_Glow.png",
        "Weight": 1
      }
    ],
    "VariantRotation": "NESW",
    "HitboxType": "Bench_Weapon",
    "State": {
      "Id": "crafting",
      "Definitions": {
        "CraftCompleted": {
          "Looping": true
        },
        "CraftCompletedInstant": {}
      }
    },
    "Gathering": {
      "Breaking": {
        "GatherType": "Benches",
        "ItemId": "Bench_Armory_Crystal_Glow"
      }
    },
    "Light": {
      "Color": "#88ccff"
    },
    "Bench": {
      "Type": "Crafting",
      "LocalOpenSoundEventId": "SFX_Weapon_Bench_Open",
      "LocalCloseSoundEventId": "SFX_Weapon_Bench_Close",
      "CompletedSoundEventId": "SFX_Weapon_Bench_Craft",
      "Id": "Armory_Crystal_Glow",
      "Categories": [
        {
          "Id": "Crystal_Glow_Sword",
          "Name": "server.benchCategories.crystal_glow_sword",
          "Icon": "Icons/CraftingCategories/Armory/Sword.png"
        }
      ],
      "TierLevels": [
        {
          "CraftingTimeReductionModifier": 0.0
        }
      ]
    },
    "BlockSoundSetId": "Crystal",
    "ParticleColor": "#88ccff",
    "Support": {
      "Down": [
        {
          "FaceType": "Full"
        }
      ]
    },
    "BlockParticleSetId": "Crystal"
  },
  "PlayerAnimationsId": "Block",
  "IconProperties": {
    "Scale": 0.5,
    "Rotation": [
      22.5,
      45,
      22.5
    ],
    "Translation": [
      13,
      -14
    ]
  },
  "Tags": {
    "Type": [
      "Bench"
    ]
  },
  "MaxStack": 1,
  "ItemSoundSetId": "ISS_Items_Gems"
}
```

### Principais campos da bancada explicados

| Campo | Finalidade |
|-------|-----------|
| `Bench.Type` | Deve ser `"Crafting"` para bancadas baseadas em receitas |
| `Bench.Id` | Identificador único que as receitas referenciam no `BenchRequirement` |
| `Bench.Categories` | Array de abas de categoria exibidas na interface da bancada. Cada uma tem um `Id`, `Icon` e `Name` de tradução |
| `Bench.TierLevels` | Array de níveis de upgrade. Cada um pode ter `CraftingTimeReductionModifier` (percentual mais rápido) e `UpgradeRequirement` |
| `State` | **Obrigatório.** Deve ter `"Id": "crafting"` para que a interface da bancada abra ao interagir |
| `VariantRotation` | `"NESW"` permite que a bancada fique voltada para quatro direções ao ser colocada |
| `HitboxType` | Reutiliza o hitbox `"Bench_Weapon"` para a área de interação |
| `Light.Color` | Emite um brilho azul suave (`#88ccff`) |
| `Support.Down` | Exige uma face de bloco completa abaixo para ser colocada |

:::caution[State é obrigatório]
Sem o bloco `State`, a bancada será colocada no mundo, mas **a interface de criação não abrirá** quando você interagir com ela. Não há nenhum erro nos logs — ela falha silenciosamente. Todas as bancadas vanilla (`Bench_Weapon`, `Bench_Armory`, `Bench_Campfire`) incluem essa configuração de `State`.
:::

### Estrutura das categorias

Cada categoria no array `Categories` define uma aba na interface de criação:

```json
{
  "Id": "Crystal_Glow_Sword",
  "Name": "server.benchCategories.crystal_glow_sword",
  "Icon": "Icons/CraftingCategories/Armory/Sword.png"
}
```

- **`Id`** — O identificador da categoria que as receitas referenciam para aparecer nessa aba
- **`Icon`** — Caminho para o PNG do ícone exibido na aba da categoria (reutilizamos o ícone vanilla de Espada)
- **`Name`** — Chave de tradução para o texto do rótulo da categoria

---

## Passo 3: Criar uma Receita Que Usa a Bancada

Qualquer item com uma `Recipe` pode referenciar sua bancada através de `BenchRequirement`. A conexão é feita combinando `BenchRequirement.Id` com o `Bench.Id` da sua bancada, e `Categories` com as abas de categoria em que a receita aparece.

Por exemplo, a receita da Espada de Cristal referencia nossa bancada:

```json
{
  "Recipe": {
    "TimeSeconds": 8.0,
    "Input": [
      {
        "ItemId": "Ore_Crystal_Glow",
        "Quantity": 10
      },
      {
        "ItemId": "Wood_Enchanted_Trunk",
        "Quantity": 50
      },
      {
        "ItemId": "Ingredient_Leather_Heavy",
        "Quantity": 10
      }
    ],
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Id": "Armory_Crystal_Glow",
        "Categories": [
          "Crystal_Glow_Sword"
        ]
      }
    ]
  }
}
```

### Campos do BenchRequirement

| Campo | Finalidade |
|-------|-----------|
| `Type` | Deve ser `"Crafting"` para corresponder a uma bancada de criação |
| `Id` | Deve corresponder exatamente ao `Bench.Id` da definição da sua bancada (diferencia maiúsculas de minúsculas) |
| `Categories` | Array de IDs de categoria em que essa receita aparece. Deve corresponder a um `Id` de categoria da bancada |
| `RequiredTierLevel` | Nível mínimo de tier da bancada necessário. Omita para tier 0 (nenhum upgrade necessário) |

---

## Passo 4: Adicionar Chaves de Tradução

Crie os arquivos de idioma em `Server/Languages/<locale>/server.lang`:

### Inglês (`en-US/server.lang`)

```
items.Bench_Armory_Crystal_Glow.name = Crystal Anvil
items.Bench_Armory_Crystal_Glow.description = A crystal anvil for forging crystal weapons.
benchCategories.crystal_glow_sword = Crystal Sword
```

### Espanhol (`es/server.lang`)

```
items.Bench_Armory_Crystal_Glow.name = Yunque de Cristal
items.Bench_Armory_Crystal_Glow.description = Un yunque de cristal para forjar armas de cristal.
benchCategories.crystal_glow_sword = Espada de Cristal
```

### Português BR (`pt-BR/server.lang`)

```
items.Bench_Armory_Crystal_Glow.name = Bigorna de Cristal
items.Bench_Armory_Crystal_Glow.description = Uma bigorna de cristal para forjar armas de cristal.
benchCategories.crystal_glow_sword = Espada de Cristal
```

Note o formato da chave de tradução: `items.<ItemId>.name` e `benchCategories.<category_id>`. O prefixo `server.` no JSON (`"Name": "server.items.Bench_Armory_Crystal_Glow.name"`) mapeia para a chave do arquivo lang sem o prefixo `server.`.

---

## Passo 5: Adicionar o Modelo Personalizado

A bancada usa um `.blockymodel` e uma textura personalizados. Coloque-os na pasta `Common/`:

- **Modelo:** `Common/Blocks/HytaleModdingManual/Armory_Crystal_Glow.blockymodel`
- **Textura:** `Common/BlockTextures/HytaleModdingManual/Armory_Crystal_Glow.png`

Você pode criar o modelo usando o [Blockbench](https://www.blockbench.net/) com o formato **Hytale Block**. O modelo deve caber dentro do limite do bloco (32 unidades = 1 bloco). Para uma bancada com 2 blocos de largura, use o hitbox `"HitboxType": "Bench_Weapon"`, que cobre a área mais larga.

:::tip[Caminhos de Assets Common]
Os assets Common devem estar dentro de um destes diretórios raiz: `Blocks/`, `BlockTextures/`, `Items/`, `Resources/`, `NPC/`, `VFX/` ou `Consumable/`. Colocar arquivos fora dessas pastas causa um erro de carregamento.
:::

---

## Passo 6: Testar no Jogo

1. Coloque a pasta do mod no diretório de mods (`%APPDATA%/Hytale/UserData/Mods/`).
2. Inicie o servidor e verifique os logs em busca de erros de validação.
3. Use o comando `/spawnitem Bench_Armory_Crystal_Glow` para obter a bancada.
4. Coloque a bancada e clique com o botão direito para abrir a interface de criação.
5. Confirme que a aba de categoria Espada de Cristal aparece.

![Bigorna de Cristal colocada no mundo](/hytale-modding-docs/images/tutorials/create-a-crafting-bench/crystal-anvil-ingame.png)

![Interface de criação da Bigorna de Cristal mostrando a receita da Espada de Cristal](/hytale-modding-docs/images/tutorials/create-a-crafting-bench/crystal-anvil-crafting-ui.png)

**Erros comuns e soluções:**

| Erro | Causa | Solução |
|------|-------|---------|
| Bancada é colocada, mas a interface não abre | Bloco `State` ausente | Adicione `"State": { "Id": "crafting", "Definitions": { "CraftCompleted": { "Looping": true }, "CraftCompletedInstant": {} } }` |
| Receita não aparece na bancada | Incompatibilidade de `BenchRequirement.Id` | Certifique-se de que o `Id` corresponde exatamente ao `Bench.Id` (diferencia maiúsculas de minúsculas) |
| Aba de categoria ausente | `Id` da categoria não está na definição da bancada | Adicione a categoria ao array `Categories` da bancada |
| `StackOverflowError` ao carregar | Uso de herança com `Parent` junto com `State` | Torne a bancada autônoma — copie todos os campos em vez de herdar de `Bench_Weapon` |
| Bancada não pode ser colocada | Bloco `Support` ausente | Adicione `"Support": { "Down": [{ "FaceType": "Full" }] }` |
| Erro de carregamento de asset Common | Caminho de asset incorreto | Certifique-se de que os assets estão dentro de `Blocks/`, `BlockTextures/`, etc. — não em `Animations/` ou pastas personalizadas |

---

## Referência de Bancadas Vanilla

Para referência, aqui estão os tipos de bancadas usados no jogo vanilla:

| Bancada | `Bench.Type` | `Bench.Id` | Categorias |
|---------|-------------|------------|-----------|
| Bancada de Armas | `Crafting` | `Weapon_Bench` | Sword, Mace, Battleaxe, Daggers, Bow |
| Arsenal | `DiagramCrafting` | `Armory` | Weapons (Sword, Club, Axe, etc.), Armor (Head, Chest, etc.) |
| Fogueira | `Crafting` | `Campfire` | Cooking |
| Bancada de Trabalho | `Crafting` | `Workbench` | Workbench_Crafting |

---

## Próximos Passos

- [Criar um Bloco Personalizado](/hytale-modding-docs/pt-br/tutorials/beginner/create-a-block) — aprenda como blocos e itens se conectam
- [Tabelas de Loot Personalizadas](/hytale-modding-docs/pt-br/tutorials/intermediate/custom-loot-tables) — configure drops que incluam seus itens criados
- [Lojas e Comércio com NPCs](/hytale-modding-docs/pt-br/tutorials/intermediate/npc-shops-and-trading) — venda itens fabricados na bancada através de mercadores NPCs
