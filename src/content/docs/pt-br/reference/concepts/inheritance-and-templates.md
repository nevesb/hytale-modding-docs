---
title: Heranca e Templates
description: Como o Hytale usa heranca de templates para reduzir duplicacao nos arquivos de configuracao JSON.
---

## Visao Geral

O sistema de configuracao do Hytale usa um modelo de heranca por templates. Em vez de definir todos os campos para cada entidade, voce cria templates base com propriedades compartilhadas e depois os estende com overrides especificos. Esse padrao aparece em roles de NPCs, itens, configs de gameplay e tipos de dano.

## Como a Heranca Funciona

```mermaid
flowchart TD;
    A["Base Template<br>Template_Beasts_Passive"] --> B[Chicken Role];
    A --> C[Rabbit Role];
    A --> D[Sheep Role];
    B -->|"Reference + Modify"| E["Chicken<br>HP: 15, Speed: 1.2<br>Drops: Feathers"];
    C -->|"Reference + Modify"| F["Rabbit<br>HP: 10, Speed: 2.0<br>Drops: Rabbit Hide"];
    D -->|"Reference + Modify"| G["Sheep<br>HP: 20, Speed: 1.0<br>Drops: Wool"];
    H[Shared from Template] --> I[AI: Passive Wander];
    H --> J[Flee when attacked];
    H --> K[Sensing range: 10];
    H --> L[Sound reactions];
    style A fill:rgb(74,61,143),color:white;
    style E fill:rgb(45,90,39),color:white;
    style F fill:rgb(45,90,39),color:white;
    style G fill:rgb(45,90,39),color:white;
    style H fill:rgb(45,106,143),color:white
```

### Ordem de Resolucao

```mermaid
flowchart LR;
    A["Role File<br>Chicken.json"] -->|"1. Read Reference"| B["Template File<br>Template_Beasts_Passive"];
    B -->|"2. Load Base"| C["Full Template<br>All fields defined"];
    C -->|"3. Apply Modify"| D["Override<br>Appearance, Stats,<br>Drops, Speed"];
    D -->|"4. Result"| E["Final NPC Definition<br>Template + Overrides"];
    style A fill:rgb(139,101,0),color:white;
    style E fill:rgb(45,90,39),color:white
```

## Mecanismos de Heranca

### Reference + Modify (NPC Roles)

O padrao mais comum para NPCs. O campo `Reference` aponta para um template, e `Modify` sobrescreve campos especificos:

```json
{
  "Reference": "Template_Beasts_Passive_Critter",
  "Modify": {
    "Appearance": "Chicken",
    "MaxHealth": 10,
    "MaxSpeed": 3.0,
    "DropList": "Drop_Chicken",
    "NameTranslationKey": "server.npc.chicken.name"
  }
}
```

O NPC resultante herda todas as propriedades de `Template_Beasts_Passive_Critter` (comportamento de IA, alcance de visao, audicao, padroes de bando, etc.) e sobrescreve apenas os cinco campos listados em `Modify`.

### Parent (Itens, Configs)

Itens e configs de gameplay usam um campo `Parent` para heranca de nivel unico:

```json
{
  "Parent": "Template_Food",
  "TranslationProperties": {
    "Name": "server.items.food_bread.name",
    "Description": "server.items.food_bread.description"
  },
  "Quality": "Uncommon",
  "Recipe": {
    "Input": [{ "ItemId": "Ingredient_Dough", "Quantity": 1 }],
    "Output": [{ "ItemId": "Food_Bread", "Quantity": 1 }],
    "BenchRequirement": { "Type": "Processing", "Id": "Cookingbench" },
    "TimeSeconds": 8
  }
}
```

### Inherits (Tipos de Dano)

Tipos de dano usam `Inherits` para hierarquias de classificacao:

```json
{
  "Inherits": "Physical"
}
```

Isso cria uma cadeia: `Bludgeoning` herda de `Physical`, que herda do tipo base `Damage`.

### Variant Type

Alguns arquivos de NPC usam `"Type": "Variant"` para definir multiplas variacoes da mesma entidade base:

```json
{
  "Type": "Variant",
  "Reference": "Template_Livestock_Cow",
  "Modify": {
    "Appearance": "Cow_Brown"
  }
}
```

## Parameters e Compute

Templates podem definir parametros com valores padrao, que entidades concretas podem sobrescrever:

```json
{
  "Parameters": {
    "BaseHealth": {
      "Value": 100,
      "Description": "Base health for this NPC tier"
    },
    "SpeedMultiplier": {
      "Value": 1.0,
      "Description": "Movement speed modifier"
    }
  },
  "MaxHealth": { "Compute": "BaseHealth" },
  "MaxSpeed": { "Compute": "4.0 * SpeedMultiplier" }
}
```

Uma entidade filha sobrescreve parametros para alterar valores computados sem redefinir as formulas.

## Hierarquia de Templates

Os templates sao tipicamente organizados em diretorios `_Core/Templates/`:

```
Server/NPC/Roles/
├── _Core/
│   └── Templates/
│       ├── Template_Beasts_Passive_Critter.json
│       ├── Template_Beasts_Hostile.json
│       ├── Template_Livestock_Cow.json
│       └── Template_Intelligent_Villager.json
├── Critter/
│   ├── Chicken.json          (References Template_Beasts_Passive_Critter)
│   └── Rabbit.json           (References Template_Beasts_Passive_Critter)
└── Beast/
    ├── Bear_Grizzly.json     (References Template_Beasts_Hostile)
    └── Wolf.json             (References Template_Beasts_Hostile)
```

## Boas Praticas

- **Sempre referencie um template** ao criar novas entidades — nao defina todos os campos do zero
- **Sobrescreva apenas o que e diferente** — mantenha os blocos `Modify` pequenos
- **Use Parameters para ajustes** — facilita o balanceamento sem mexer nas formulas
- **Verifique o template primeiro** — leia o arquivo do template para entender quais padroes voce herda

## Paginas Relacionadas

- [NPC Roles](/hytale-modding-docs/reference/npc-system/npc-roles/) — onde Reference/Modify e mais usado
- [NPC Templates](/hytale-modding-docs/reference/npc-system/npc-templates/) — templates base disponiveis
- [Item Definitions](/hytale-modding-docs/reference/item-system/item-definitions/) — heranca Parent para itens
- [Damage Types](/hytale-modding-docs/reference/combat-and-projectiles/damage-types/) — hierarquia Inherits
