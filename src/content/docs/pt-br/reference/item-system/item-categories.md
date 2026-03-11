---
title: Categorias de Itens
description: Referência para arquivos JSON de categoria de itens no Hytale, definindo a árvore hierárquica de categorias usada em menus de fabricação e na biblioteca criativa.
---

## Visão Geral

Categorias de itens definem a estrutura em árvore que organiza itens nos menus de fabricação e na biblioteca criativa. Cada arquivo JSON representa um nó de categoria de nível superior e contém uma lista ordenada de entradas de categorias filhas. Itens são atribuídos a categorias pelo array `Categories` em sua definição de item.

## Localização dos Arquivos

```
Assets/Server/Item/Category/<LibraryId>/<CategoryId>.json
```

As duas raízes de biblioteca são:
- `Assets/Server/Item/Category/CreativeLibrary/` — Navegador de itens do modo criativo (Blocks, Furniture, Items, Tool)
- `Assets/Server/Item/Category/Fieldcraft/` — Menus de fabricação de sobrevivência (Tools)

## Schema

### Campos do Arquivo de Categoria

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `Icon` | string | Sim | — | Caminho para a imagem do ícone desta categoria de nível superior (ex.: `"Icons/ItemCategories/Natural.png"`). |
| `Order` | number | Não | `0` | Ordem de classificação desta categoria em relação às suas irmãs. Valores menores aparecem primeiro. |
| `Name` | string | Não | — | Chave de localização para o nome de exibição da categoria (usado em nós folha/subcategoria). |
| `Children` | object[] | Não | — | Array ordenado de entradas de categorias filhas. |

### Campos de Entrada de Children

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `Id` | string | Sim | — | Identificador único para esta categoria filha. Usado como segundo segmento nos valores `Categories` do item (ex.: `"Foods"` mapeia para `"Items.Foods"`). |
| `Name` | string | Sim | — | Chave de localização para o rótulo de exibição da categoria filha (ex.: `"server.ui.itemcategory.foods"`). |
| `Icon` | string | Sim | — | Caminho para a imagem do ícone desta categoria filha. |

## Exemplo

`Assets/Server/Item/Category/CreativeLibrary/Blocks.json`:

```json
{
  "Icon": "Icons/ItemCategories/Natural.png",
  "Order": 0,
  "Children": [
    {
      "Id": "Rocks",
      "Name": "server.ui.itemcategory.rocks",
      "Icon": "Icons/ItemCategories/Blocks.png"
    },
    {
      "Id": "Structural",
      "Name": "server.ui.itemcategory.structural",
      "Icon": "Icons/ItemCategories/Build-Roofs.png"
    },
    {
      "Id": "Soils",
      "Name": "server.ui.itemcategory.soils",
      "Icon": "Icons/ItemCategories/Soil.png"
    },
    {
      "Id": "Ores",
      "Name": "server.ui.itemcategory.ores",
      "Icon": "Icons/ItemCategories/Natural-Ore.png"
    },
    {
      "Id": "Plants",
      "Name": "server.ui.itemcategory.plants",
      "Icon": "Icons/ItemCategories/Natural-Vegetal.png"
    },
    {
      "Id": "Fluids",
      "Name": "server.ui.itemcategory.fluids",
      "Icon": "Icons/ItemCategories/Natural-Fluid.png"
    },
    {
      "Id": "Portals",
      "Name": "server.ui.itemcategory.portals",
      "Icon": "Icons/ItemCategories/Portal.png"
    },
    {
      "Id": "Deco",
      "Name": "server.ui.itemcategory.deco",
      "Icon": "Icons/ItemCategories/Natural-Fire.png"
    }
  ]
}
```

`Assets/Server/Item/Category/CreativeLibrary/Items.json`:

```json
{
  "Icon": "Icons/ItemCategories/Items.png",
  "Order": 2,
  "Children": [
    {
      "Id": "Tools",
      "Name": "server.ui.itemcategory.tools",
      "Icon": "Icons/ItemCategories/Items-Tools.png"
    },
    {
      "Id": "Weapons",
      "Name": "server.ui.itemcategory.weapons",
      "Icon": "Icons/ItemCategories/Items-Weapons.png"
    },
    {
      "Id": "Armors",
      "Name": "server.ui.itemcategory.armors",
      "Icon": "Icons/ItemCategories/Items-Armor.png"
    },
    {
      "Id": "Foods",
      "Name": "server.ui.itemcategory.foods",
      "Icon": "Icons/ItemCategories/Items-Food.png"
    },
    {
      "Id": "Potions",
      "Name": "server.ui.itemcategory.potions",
      "Icon": "Icons/ItemCategories/Items-Potion.png"
    },
    {
      "Id": "Recipes",
      "Name": "server.ui.itemcategory.recipes",
      "Icon": "Icons/ItemCategories/Items-Recipe.png"
    },
    {
      "Id": "Ingredients",
      "Name": "server.ui.itemcategory.ingredients",
      "Icon": "Icons/ItemCategories/Items-Ingredients.png"
    }
  ]
}
```

## Atribuindo Itens a Categorias

No arquivo de definição de um item, defina o campo `Categories` como uma lista de strings `"<LibraryId>.<ChildId>"`:

```json
{
  "Categories": [
    "Items.Foods"
  ]
}
```

Um único item pode pertencer a múltiplas categorias adicionando mais entradas ao array.

## Páginas Relacionadas

- [Definições de Itens](/hytale-modding-docs/reference/item-system/item-definitions) — Onde o campo `Categories` é definido nos itens
- [Grupos de Itens](/hytale-modding-docs/reference/item-system/item-groups) — Conjuntos nomeados de blocos/itens (distintos das categorias)
- [Tipos de Recurso](/hytale-modding-docs/reference/item-system/resource-types) — Agrupamentos de recursos usados em receitas
