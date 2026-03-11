---
title: Criar um NPC Personalizado
description: Tutorial passo a passo para adicionar um NPC criatura ao Hytale, incluindo definição de role, tabela de drops e regras de spawn.
---

## Objetivo

Adicionar uma criatura passiva chamada **Mossbug** ao mundo do jogo. Você vai criar um JSON de role de NPC que referencia um modelo, escrever uma tabela de drops para que ele solte ingredientes quando eliminado, e configurar regras de spawn para que ele apareça em ambientes florestais.

## Pré-requisitos

- Uma pasta de mod com um `manifest.json` válido (veja [Configure seu Ambiente de Desenvolvimento](/hytale-modding-docs/tutorials/beginner/setup-dev-environment))
- Familiaridade com herança de templates em JSON (veja [Fundamentos de JSON](/hytale-modding-docs/getting-started/json-basics))

---

## Visão Geral dos Tipos de NPC

O Hytale organiza NPCs em tipos definidos pelo template do qual herdam. Entender os templates disponíveis ajuda a escolher a base certa para o seu NPC.

| Template | Pasta | Comportamento |
|----------|-------|---------------|
| `Template_Beasts_Passive_Critter` | `Creature/Critter/` | Pequeno animal passivo — foge quando ameaçado, vagueia, pode ser atraído por comida |
| `Template_Animal_Neutral` | `Creature/Mammal/` | Fera neutra maior — ataca quando provocada |
| `Template_Predator` | `Creature/` | Caça jogadores ativamente dentro do campo de visão |
| `Template_Livestock` | `Creature/Livestock/` | Animal de fazenda — pode ser mantido em galinheiros ou cercados |
| `Template_Birds_Passive` | `Avian/` | Pássaro passivo voador |
| `Template_Intelligent` | `Intelligent/` | NPC humanoide com capacidade de diálogo e missões |
| `Template_Spirit` | `Elemental/` | Criatura elemental ou mágica |

Para uma criatura passiva pequena como o Mossbug, `Template_Beasts_Passive_Critter` é a base correta. Ele fornece comportamentos de vagueio, fuga e curiosidade opcional — correspondendo ao funcionamento dos Esquilos e Sapos vanilla.

---

## Passo 1: Criar ou Referenciar um Modelo

O campo `Appearance` do seu NPC nomeia o conjunto de modelo que o engine usa para renderização. Nomes de aparência vanilla como `Squirrel`, `Frog_Green` e `Mouse` mapeiam para conjuntos pré-construídos de rig e animação.

Para uma forma de criatura completamente nova, você precisa de um asset de aparência personalizado (um modelo completo, rig e conjunto de animações no Blockbench). Para este tutorial, referenciamos uma aparência vanilla para fazer o NPC funcionar imediatamente, podendo ser substituída depois por um modelo personalizado.

Vamos usar `"Appearance": "Gecko"` como substituto temporário. Todos os nomes de aparência vanilla disponíveis podem ser encontrados verificando o campo `Appearance` nos arquivos em `Assets/Server/NPC/Roles/`.

---

## Passo 2: Criar o JSON de Role do NPC

Os roles de NPC ficam em `Assets/Server/NPC/Roles/`. Organize os NPCs do seu mod em uma subpasta.

Crie:

```
YourMod/Assets/Server/NPC/Roles/MyMod/Mossbug.json
```

O padrão `Type: "Variant"` — usado por toda criatura vanilla incluindo Squirrel e Frog — herda toda a lógica de IA do template e sobrescreve apenas os campos que diferem:

```json
{
  "Type": "Variant",
  "Reference": "Template_Beasts_Passive_Critter",
  "Modify": {
    "Appearance": "Gecko",
    "DropList": "Drop_Mossbug",
    "MaxHealth": 12,
    "IsMemory": true,
    "MemoriesCategory": "Critter",
    "MemoriesNameOverride": "Mossbug",
    "NameTranslationKey": {
      "Compute": "NameTranslationKey"
    }
  },
  "Parameters": {
    "NameTranslationKey": {
      "Value": "server.npcRoles.Mossbug.name",
      "Description": "Translation key for NPC name display"
    }
  }
}
```

### Campos do Modify explicados

| Campo | Finalidade |
|-------|------------|
| `Appearance` | O conjunto de modelo e animação para renderizar. Deve corresponder a um nome de aparência conhecido |
| `DropList` | ID do arquivo da tabela de drops (sem `.json`). Resolvido a partir de `Assets/Server/Drops/` |
| `MaxHealth` | Pontos de vida. Criaturas vanilla usam 10-20. Squirrel e Frog usam 15 |
| `IsMemory` | Se o jogador pode desbloquear essa criatura no bestiário de Memórias |
| `MemoriesCategory` | Aba de categoria no bestiário: `Critter`, `Beast`, `Livestock`, `Other` |
| `MemoriesNameOverride` | O nome de exibição usado na tela de Memórias |
| `NameTranslationKey` | Chave de tradução para o nome exibido acima da cabeça do NPC |

### Parameters

O bloco `Parameters` define valores que o template acessa via `{ "Compute": "FieldName" }`. Definir `NameTranslationKey` aqui alimenta a expressão `"NameTranslationKey": { "Compute": "NameTranslationKey" }` do template.

### Sobrescritas opcionais

O template `Template_Beasts_Passive_Critter` expõe parâmetros adicionais que você pode definir dentro do `Modify`:

```json
"Modify": {
  "Appearance": "Gecko",
  "DropList": "Drop_Mossbug",
  "MaxHealth": 12,
  "MaxSpeed": 7,
  "WanderRadius": 8,
  "ViewRange": 12,
  "HearingRange": 12,
  "AttractiveItems": ["Food_Bread", "Ingredient_Fibre"]
}
```

`AttractiveItems` faz a criatura investigar e pegar itens dropados da lista indicada — útil para mecânicas de domesticação ou isca.

---

## Passo 3: Criar uma Tabela de Drops

As tabelas de drops ficam em `Assets/Server/Drops/`. Os drops de NPCs vanilla são organizados em `Drops/NPCs/<Categoria>/`. Crie:

```
YourMod/Assets/Server/Drops/NPCs/Critter/Drop_Mossbug.json
```

A estrutura `Container` usa um sistema de seleção por peso. `Type: "Multiple"` executa todos os containers filhos em ordem. `Type: "Choice"` escolhe um filho aleatoriamente, ponderado pelo campo `Weight`.

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
              "ItemId": "Ingredient_Fibre",
              "QuantityMin": 1,
              "QuantityMax": 2
            }
          }
        ]
      },
      {
        "Type": "Choice",
        "Weight": 30,
        "Containers": [
          {
            "Type": "Single",
            "Item": {
              "ItemId": "Ingredient_Crystal",
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

Essa tabela sempre dropa 1-2 Fibras (peso 100 de 100 naquele grupo) e tem 30% de chance de também dropar 1 Cristal. Compare com `Drop_Bear_Grizzly.json` que usa dois grupos `Choice` separados, cada um com `Weight: 100`, para garantir o drop de couro e carne.

### Tipos de container de drop

| Tipo | Comportamento |
|------|---------------|
| `Multiple` | Avalia todos os containers filhos |
| `Choice` | Escolhe um filho proporcionalmente ao `Weight` |
| `Single` | Produz o `Item` especificado com uma quantidade aleatória entre `QuantityMin` e `QuantityMax` |

Se você quiser que uma criatura não drope nada (como os Squirrel e Frog vanilla), simplesmente crie um objeto vazio:

```json
{}
```

---

## Passo 4: Criar Regras de Spawn

As regras de spawn dizem ao gerador de mundo onde e quando posicionar seu NPC. Os arquivos de spawn ficam em `Assets/Server/NPC/Spawn/World/<Zona>/`.

Crie:

```
YourMod/Assets/Server/NPC/Spawn/World/Zone1/Spawns_Zone1_MyMod_Critter.json
```

```json
{
  "Environments": [
    "Env_Zone1_Forests",
    "Env_Zone1_Autumn"
  ],
  "NPCs": [
    {
      "Weight": 3,
      "SpawnBlockSet": "Soil",
      "Id": "Mossbug",
      "Flock": "One_Or_Two"
    }
  ],
  "DayTimeRange": [
    6,
    18
  ]
}
```

### Campos de spawn explicados

| Campo | Finalidade |
|-------|------------|
| `Environments` | Em quais biomas de ambiente este arquivo se aplica. Corresponde aos IDs de ambiente usados pela geração de mundo |
| `NPCs` | Lista de NPCs que podem spawnar nesses ambientes |
| `Weight` | Probabilidade relativa deste NPC ser escolhido em comparação com outros no mesmo arquivo. Maior = mais comum. O Squirrel usa `Weight: 6` nas florestas da Zona 1 |
| `SpawnBlockSet` | Tipo de superfície onde o NPC spawna: `Soil` (chão), `Birds` (ar, para NPCs voadores), `Water` (aquático) |
| `Id` | O ID do role do NPC — corresponde ao nome do arquivo do seu JSON de role sem `.json` |
| `Flock` | Tamanho do grupo ao spawnar. Valores disponíveis: `One_Or_Two`, `Group_Small`, `Group_Large` |
| `DayTimeRange` | Intervalo de horas `[início, fim]` durante o qual os spawns deste arquivo estão ativos. `[6, 18]` = apenas durante o dia |

Para uma criatura noturna, use `"DayTimeRange": [20, 6]` (atravessa a meia-noite).

### Ambientes disponíveis (exemplos da Zona 1)

| ID do Ambiente | Descrição |
|----------------|-----------|
| `Env_Zone1_Forests` | Floresta temperada padrão |
| `Env_Zone1_Autumn` | Floresta com cores de outono |
| `Env_Zone1_Azure` | Variante de floresta azulada |
| `Env_Zone1_Mountains_Critter` | Terreno montanhoso |

---

## Passo 5: Adicionar Chaves de Tradução

Adicione o texto do nome do NPC ao arquivo de idioma do seu mod:

```
YourMod/Assets/Languages/en-US.lang
```

```
server.npcRoles.Mossbug.name=Mossbug
```

---

## Passo 6: Testar no Jogo

1. Coloque a pasta do seu mod no diretório de mods do servidor.
2. Inicie o servidor. Observe o console para erros sobre IDs de role desconhecidos, aparências ausentes ou referências inválidas de tabelas de drops.
3. Use o spawner de NPCs do desenvolvedor para forçar o spawn de `Mossbug` na sua localização.
4. Confirme se o modelo renderiza, o NPC vagueia e foge quando você se aproxima.
5. Elimine o Mossbug e verifique se a tabela de drops produz Fibra (e ocasionalmente Cristal).
6. Viaje até um bioma de Floresta da Zona 1 e confirme que os Mossbugs aparecem naturalmente durante o dia.

**Erros comuns e soluções:**

| Erro | Causa | Solução |
|------|-------|---------|
| `Unknown reference: Template_Beasts_Passive_Critter` | Template não encontrado | Verifique se os assets vanilla são carregados antes do seu mod |
| `Unknown appearance: Gecko` | Erro de digitação no nome da aparência | Verifique `Assets/Server/NPC/Roles/` para nomes de aparência válidos |
| `Unknown drop list: Drop_Mossbug` | Caminho do arquivo de drop errado | Confirme se o arquivo está em `Drops/NPCs/Critter/Drop_Mossbug.json` |
| NPC não spawna naturalmente | ID do ambiente errado | Compare os nomes de ambiente com os arquivos de spawn vanilla |

---

## Arquivos Completos

### `YourMod/Assets/Server/NPC/Roles/MyMod/Mossbug.json`
```json
{
  "Type": "Variant",
  "Reference": "Template_Beasts_Passive_Critter",
  "Modify": {
    "Appearance": "Gecko",
    "DropList": "Drop_Mossbug",
    "MaxHealth": 12,
    "IsMemory": true,
    "MemoriesCategory": "Critter",
    "MemoriesNameOverride": "Mossbug",
    "NameTranslationKey": {
      "Compute": "NameTranslationKey"
    }
  },
  "Parameters": {
    "NameTranslationKey": {
      "Value": "server.npcRoles.Mossbug.name",
      "Description": "Translation key for NPC name display"
    }
  }
}
```

### `YourMod/Assets/Server/Drops/NPCs/Critter/Drop_Mossbug.json`
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
              "ItemId": "Ingredient_Fibre",
              "QuantityMin": 1,
              "QuantityMax": 2
            }
          }
        ]
      },
      {
        "Type": "Choice",
        "Weight": 30,
        "Containers": [
          {
            "Type": "Single",
            "Item": {
              "ItemId": "Ingredient_Crystal",
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

### `YourMod/Assets/Server/NPC/Spawn/World/Zone1/Spawns_Zone1_MyMod_Critter.json`
```json
{
  "Environments": [
    "Env_Zone1_Forests",
    "Env_Zone1_Autumn"
  ],
  "NPCs": [
    {
      "Weight": 3,
      "SpawnBlockSet": "Soil",
      "Id": "Mossbug",
      "Flock": "One_Or_Two"
    }
  ],
  "DayTimeRange": [
    6,
    18
  ]
}
```

### `YourMod/Assets/Languages/en-US.lang`
```
server.npcRoles.Mossbug.name=Mossbug
```

---

## Próximos Passos

- [Criar um Item Personalizado](/hytale-modding-docs/tutorials/beginner/create-an-item) — adicione uma arma que seu NPC pode potencialmente dropar
- [Criar um Bloco Personalizado](/hytale-modding-docs/tutorials/beginner/create-a-block) — crie um bloco como drop para a tabela de loot do seu NPC
- [Fundamentos de JSON](/hytale-modding-docs/getting-started/json-basics) — referência para seleção por peso e valores calculados
