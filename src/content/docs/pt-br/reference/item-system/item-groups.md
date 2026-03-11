---
title: Grupos de Itens
description: Referência para arquivos JSON de grupos de itens no Hytale, que definem conjuntos nomeados de IDs de blocos usados por receitas, sistemas de fabricação e geração de mundo.
---

## Visão Geral

Grupos de itens definem coleções nomeadas de IDs de blocos. Um grupo reúne variantes de blocos relacionados — por exemplo, todos os tipos de blocos de pedra aqua — sob um único ID de grupo. Outros sistemas referenciam IDs de grupo para operar em todos os blocos membros sem listar cada um individualmente.

## Localização dos Arquivos

```
Assets/Server/Item/Groups/<GroupId>.json
```

Exemplos:
```
Assets/Server/Item/Groups/FullBlocks_Aqua.json
Assets/Server/Item/Groups/FullBlocks_Basalt.json
Assets/Server/Item/Groups/FullBlocks_Blackwood.json
Assets/Server/Item/Groups/Foods.json
Assets/Server/Item/Groups/Metal_Bars.json
Assets/Server/Item/Groups/Rock.json
Assets/Server/Item/Groups/Soils.json
Assets/Server/Item/Groups/Wood_All.json
```

## Schema

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `Blocks` | string[] | Sim | — | Array de IDs de bloco/item que pertencem a este grupo. Cada entrada é o ID exato do item conforme usado nas definições de itens (ex.: `"Rock_Aqua"`, `"Rock_Aqua_Cobble"`). |

## Exemplos

`Assets/Server/Item/Groups/FullBlocks_Aqua.json`:

```json
{
  "Blocks": [
    "Rock_Aqua",
    "Rock_Aqua_Cobble"
  ]
}
```

`Assets/Server/Item/Groups/FullBlocks_Basalt.json`:

```json
{
  "Blocks": [
    "Rock_Basalt",
    "Rock_Basalt_Cobble"
  ]
}
```

`Assets/Server/Item/Groups/FullBlocks_Blackwood.json`:

```json
{
  "Blocks": [
    "Wood_Blackwood_Planks",
    "Wood_Blackwood_Decorative",
    "Wood_Blackwood_Ornate"
  ]
}
```

## Grupos Disponíveis (Lista Parcial)

Grupos cobrem todas as principais famílias de blocos. A convenção de nomenclatura é `FullBlocks_<Material>` para conjuntos de blocos posicionáveis e nomes simples para categorias de itens/ingredientes:

| ID do Grupo | Descrição |
|-------------|-----------|
| `FullBlocks_Aqua` | Variantes de pedra aqua |
| `FullBlocks_Basalt` | Variantes de pedra basalto |
| `FullBlocks_Blackwood` | Variantes de tábua e decoração de blackwood |
| `FullBlocks_Calcite` | Variantes de pedra calcita |
| `FullBlocks_Limestone` | Variantes de calcário |
| `FullBlocks_Marble` | Variantes de mármore |
| `FullBlocks_Stone` | Variantes de pedra padrão |
| `FullBlocks_Softwood` | Variantes de tábua de madeira macia |
| `FullBlocks_Volcanic` | Variantes de pedra vulcânica |
| `Foods` | Todos os itens de comida |
| `Metal_Bars` | Todos os itens de lingote/barra de metal |
| `Rock` | Todos os tipos de bloco de rocha |
| `Soils` | Todos os tipos de bloco de solo |
| `Wood_All` | Todos os tipos de tábua de madeira |
| `Wood_Trunk` | Todos os tipos de tronco de madeira |
| `Bone` | Variantes de itens de osso |
| `Flowers` | Tipos de bloco de flores |
| `Mushrooms` | Tipos de bloco de cogumelos |
| `Meats` | Itens de ingrediente de carne |
| `Fish` | Todos os itens de peixe |
| `Fuel` | Itens que podem ser usados como combustível |
| `Rubble` | Tipos de bloco de entulho |
| `Sands` | Tipos de areia e cascalho |

## Páginas Relacionadas

- [Definições de Itens](/hytale-modding-docs/reference/item-system/item-definitions) — Definições de blocos e itens que os grupos referenciam
- [Definições de Blocos](/hytale-modding-docs/reference/item-system/block-definitions) — Propriedades de textura e material de blocos
- [Tipos de Recurso](/hytale-modding-docs/reference/item-system/resource-types) — Mecanismo alternativo de agrupamento usado em entradas de receitas
