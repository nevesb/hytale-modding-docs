---
title: Definições de Itens
description: Referência para arquivos JSON de definição de itens no Hytale, cobrindo campos para comidas, armas, ferramentas e todos os itens posicionáveis.
---

## Visão Geral

Definições de itens são arquivos JSON que descrevem cada item no Hytale — comidas, armas, ferramentas, blocos e mais. Cada arquivo fica em uma subpasta de categoria em `Assets/Server/Item/Items/` e pode estender um template pai para herdar campos compartilhados. O sub-objeto `BlockType` controla como o item aparece quando colocado no mundo.

## Localização dos Arquivos

```
Assets/Server/Item/Items/<Category>/<ItemId>.json
```

Exemplos:
- `Assets/Server/Item/Items/Food/Food_Bread.json`
- `Assets/Server/Item/Items/Weapon/Axe/Weapon_Axe_Copper.json`
- `Assets/Server/Item/Items/Tool/Pickaxe/Tool_Pickaxe_Copper.json`

## Schema

### Campos de Nível Superior

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `Parent` | string | Não | — | ID de um item template para herdar campos (ex.: `"Template_Food"`). |
| `TranslationProperties` | object | Sim | — | Chaves de localização para o texto de exibição do item. |
| `TranslationProperties.Name` | string | Sim | — | Chave de localização para o nome do item (ex.: `"server.items.Food_Bread.name"`). |
| `TranslationProperties.Description` | string | Não | — | Chave de localização para a descrição do item. |
| `Quality` | string | Não | — | ID do nível de qualidade. Um entre `Junk`, `Common`, `Uncommon`, `Rare`, `Epic`, `Legendary`, `Tool`, `Developer`, `Template`. |
| `Icon` | string | Não | — | Caminho para a imagem do ícone do item (ex.: `"Icons/ItemsGenerated/Food_Bread.png"`). |
| `Categories` | string[] | Não | — | Lista de IDs de categoria em que este item aparece (ex.: `["Items.Foods"]`). |
| `ItemLevel` | number | Não | — | Nível de poder do item usado pelos sistemas de progressão e desbloqueio de receitas. |
| `MaxStack` | number | Não | — | Número máximo deste item que pode ser empilhado em um slot de inventário. |
| `DropOnDeath` | boolean | Não | `false` | Se o item é dropado quando o jogador que o carrega morre. |
| `Scale` | number | Não | `1.0` | Escala visual da entidade do item quando dropado no mundo. |
| `Interactions` | object | Não | — | Mapeia nomes de slots de interação (ex.: `Primary`, `Secondary`) para IDs de cadeias de interação. |
| `InteractionVars` | object | Não | — | Substituições de variáveis de interação nomeadas. Cada chave é um nome de variável; cada valor tem um array `Interactions` de cadeias inline ou referenciadas por pai. |
| `Recipe` | object | Não | — | Receita de fabricação para este item. Veja os campos de Receita abaixo. |
| `BlockType` | object | Não | — | Controla como o item aparece quando colocado como um bloco no mundo. Veja os campos de BlockType abaixo. |
| `ResourceTypes` | object[] | Não | — | Lista de objetos `{ "Id": "<ResourceTypeId>" }`. Marca este item como pertencente a grupos de recursos usados em receitas. |
| `Tags` | object | Não | — | Grupos de tags chave-valor (ex.: `{ "Type": ["Food"], "Family": ["Axe"] }`). Usados para filtragem e interações. |
| `MaxDurability` | number | Não | — | Durabilidade máxima para ferramentas e armas. |
| `DurabilityLossOnHit` | number | Não | — | Durabilidade perdida por golpe para armas. |
| `Weapon` | object | Não | — | Marca este item como uma arma. Geralmente um objeto vazio `{}` que ativa o comportamento de arma. |
| `Tool` | object | Não | — | Configuração de ferramenta incluindo `Specs` (poder de coleta por tipo de bloco) e `DurabilityLossBlockTypes`. |
| `Consumable` | boolean | Não | — | Marca este item como consumível. |
| `PlayerAnimationsId` | string | Não | — | ID do conjunto de animações usado quando o jogador segura este item (ex.: `"Axe"`, `"Item"`). |
| `Model` | string | Não | — | Caminho para o arquivo `.blockymodel` para o modelo segurado de arma/ferramenta (ex.: `"Items/Weapons/Axe/Copper.blockymodel"`). |
| `Texture` | string | Não | — | Caminho para a textura usada com `Model`. |

### Campos de BlockType

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `Material` | string | Não | — | Tipo de material físico. Um entre `Solid`, `Fluid`, `Empty`, `Plant`. |
| `DrawType` | string | Não | — | Estilo de renderização. Valores comuns: `Model`, `Block`, `Plant`. |
| `Opacity` | string | Não | — | Nível de transparência. Um entre `Opaque`, `Semitransparent`, `Transparent`. |
| `CustomModel` | string | Não | — | Caminho para o arquivo `.blockymodel` usado quando o item é colocado como bloco (ex.: `"Items/Consumables/Food/Bread.blockymodel"`). |
| `CustomModelTexture` | object[] | Não | — | Array de objetos `{ "Texture": "<caminho>", "Weight": <número> }` para variantes de textura aleatórias. |
| `CustomModelScale` | number | Não | `1.0` | Multiplicador de escala aplicado ao modelo personalizado. |
| `HitboxType` | string | Não | — | ID da forma do hitbox (ex.: `"Food_Medium"`, `"Food_Large"`). |
| `RandomRotation` | string | Não | — | Modo de rotação aleatória aplicado quando colocado (ex.: `"YawStep1"`). |
| `ParticleColor` | string | Não | — | Cor hex usada para partículas de quebra de bloco (ex.: `"#e4cb69"`). |
| `Textures` | object[] | Não | — | Para blocos posicionáveis: array de objetos de textura com chaves de face. Cada entrada pode ter `All`, `Sides`, `UpDown`, `Top`, `Bottom`, `North`, `South`, `East`, `West`, e um `Weight` para variantes aleatórias. |
| `Gathering` | object | Não | — | Define quais tipos de coleta se aplicam quando este bloco é colhido ou quebrado (`Harvest`, `Soft`, `Breaking`). |

### Campos de Receita

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `Input` | object[] | Sim | — | Array de objetos de ingrediente. Cada um tem `ItemId` ou `ResourceTypeId`, mais um `Quantity` opcional (padrão `1`). |
| `Output` | object[] | Não | — | Array de objetos de saída com `ItemId` e `Quantity` opcional. Padrão é o próprio item com quantidade 1. |
| `OutputQuantity` | number | Não | `1` | Atalho para definir a quantidade de saída quando o item de saída é o próprio item da definição. |
| `BenchRequirement` | object[] | Não | — | Array de requisitos de bancada. Cada um tem `Type` (`"Crafting"`, `"Processing"`, `"StructuralCrafting"`), `Id` (ID da bancada), e array opcional `Categories`. |
| `TimeSeconds` | number | Não | `0` | Duração da fabricação em segundos. |
| `KnowledgeRequired` | boolean | Não | `true` | Se o jogador precisa ter aprendido esta receita antes de fabricá-la. |

## Exemplo

`Assets/Server/Item/Items/Food/Food_Bread.json`:

```json
{
  "TranslationProperties": {
    "Name": "server.items.Food_Bread.name",
    "Description": "server.items.Food_Bread.description"
  },
  "Parent": "Template_Food",
  "Interactions": {
    "Secondary": "Root_Secondary_Consume_Food_T2"
  },
  "Quality": "Uncommon",
  "Icon": "Icons/ItemsGenerated/Food_Bread.png",
  "BlockType": {
    "Material": "Empty",
    "DrawType": "Model",
    "Opacity": "Semitransparent",
    "CustomModel": "Items/Consumables/Food/Bread.blockymodel",
    "CustomModelTexture": [
      {
        "Texture": "Items/Consumables/Food/Bread_Texture.png",
        "Weight": 1
      }
    ],
    "HitboxType": "Food_Medium",
    "RandomRotation": "YawStep1",
    "CustomModelScale": 0.5,
    "ParticleColor": "#e4cb69"
  },
  "InteractionVars": {
    "Consume_Charge": {
      "Interactions": [
        {
          "Parent": "Consume_Charge_Food_T1_Inner",
          "Effects": {
            "Particles": [
              {
                "SystemId": "Food_Eat",
                "Color": "#DCC15D",
                "TargetNodeName": "Mouth",
                "TargetEntityPart": "Entity"
              }
            ]
          }
        }
      ]
    },
    "Effect": {
      "Interactions": [
        {
          "Type": "ApplyEffect",
          "EffectId": "Food_Instant_Heal_Bread"
        }
      ]
    }
  },
  "Recipe": {
    "Input": [
      {
        "ItemId": "Ingredient_Dough",
        "Quantity": 1
      },
      {
        "ResourceTypeId": "Fuel",
        "Quantity": 3
      }
    ],
    "Output": [
      {
        "ItemId": "Food_Bread"
      }
    ],
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Id": "Cookingbench",
        "Categories": [
          "Baked"
        ]
      }
    ],
    "TimeSeconds": 5
  },
  "Scale": 1.5,
  "ItemLevel": 7,
  "MaxStack": 25,
  "DropOnDeath": true
}
```

## Páginas Relacionadas

- [Definições de Blocos](/hytale-modding-docs/reference/item-system/block-definitions) — Campos de textura e material específicos de blocos
- [Qualidades de Itens](/hytale-modding-docs/reference/item-system/item-qualities) — Definições de níveis de qualidade
- [Interações de Itens](/hytale-modding-docs/reference/item-system/item-interactions) — Referência de cadeias de interação
- [Categorias de Itens](/hytale-modding-docs/reference/item-system/item-categories) — Hierarquia de categorias
- [Tipos de Recurso](/hytale-modding-docs/reference/item-system/resource-types) — IDs de tipos de recurso usados em receitas
