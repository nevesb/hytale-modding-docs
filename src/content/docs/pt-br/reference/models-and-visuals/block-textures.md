---
title: Texturas de Blocos
description: Referência para convenções de texturas de blocos no Hytale, cobrindo padrões de nomenclatura, layout de diretórios e sistema de texturas por face usado por blocos cúbicos padrão.
---

## Visão Geral

Texturas de blocos são imagens PNG que definem a aparência visual de blocos cúbicos padrão. Diferente de blocos baseados em blockymodel que possuem geometria voxel 3D completa, blocos padrão usam um conjunto de texturas por face aplicadas a um cubo unitário. O motor resolve texturas por convenção de nomenclatura — um bloco chamado `Calcite` procura por `Calcite.png`, `Calcite_Top.png`, `Calcite_Side.png`, etc. no diretório `BlockTextures`. Todas as texturas usam uma resolução de pixels consistente e são empacotadas em um atlas de texturas no momento do carregamento.

## Localização dos Arquivos

```
Assets/Common/BlockTextures/
  Bone_Side.png
  Bone_Top.png
  Calcite.png
  Calcite_Brick_Decorative.png
  Calcite_Brick_Decorative_Top.png
  Calcite_Brick_Ornate.png
  Calcite_Brick_Side.png
  Calcite_Brick_Smooth.png
  Calcite_Brick_Top.png
  Calcite_Cobble.png
  Calcite_Cobble_Top.png
  Calcite_Top.png
  Chalk.png
  Clay_Black.png
  Clay_Blue.png
  Clay_Smooth_Black.png
  ...
```

## Convenções de Nomenclatura

### Texturas Específicas por Face

O motor usa um sistema baseado em sufixos para atribuir texturas a faces específicas do cubo. Se uma textura específica de face não for encontrada, o motor recorre à textura base.

| Sufixo | Faces Aplicadas | Descrição |
|--------|----------------|-----------|
| _(nenhum)_ | Todas as faces (fallback) | Textura base usada para qualquer face sem uma sobreposição específica. |
| `_Top` | Topo (+Y) | Textura da face superior. Comum para blocos com aparência diferente no topo/laterais (ex.: grama, minério). |
| `_Side` | Norte, Sul, Leste, Oeste | Textura das faces laterais, usada quando as laterais diferem do topo e da base. |
| `_Bottom` | Base (-Y) | Textura da face inferior. Raramente necessária; recorre à base se ausente. |

### Ordem de Resolução

Para um bloco chamado `Calcite_Brick`:

1. **Face superior**: `Calcite_Brick_Top.png` -> `Calcite_Brick.png`
2. **Faces laterais**: `Calcite_Brick_Side.png` -> `Calcite_Brick.png`
3. **Face inferior**: `Calcite_Brick_Bottom.png` -> `Calcite_Brick.png`

### Padrões de Material e Variante

| Padrão | Exemplo | Descrição |
|--------|---------|-----------|
| `{Material}.png` | `Chalk.png` | Bloco uniforme simples — mesma textura em todas as faces. |
| `{Material}_{Acabamento}.png` | `Calcite_Brick_Smooth.png` | Variante processada de um material base. |
| `{Material}_{Acabamento}_{Face}.png` | `Calcite_Brick_Decorative_Top.png` | Textura específica de face para uma variante processada. |
| `{Categoria}_{Cor}.png` | `Clay_Blue.png` | Variante de cor dentro de uma categoria de material. |
| `{Categoria}_{Acabamento}_{Cor}.png` | `Clay_Smooth_Blue.png` | Variante de cor de um acabamento processado. |

## Especificações de Textura

| Propriedade | Valor | Descrição |
|-------------|-------|-----------|
| Formato | PNG | Imagens PNG RGBA padrão. |
| Resolução | 16x16 pixels (padrão) | Todas as texturas de blocos usam a mesma resolução para empacotamento no atlas. |
| Transparência | Suportada | Canal alfa permite blocos parcialmente transparentes (vidro, folhas). |
| Espaço de Cor | sRGB | Espaço de cor padrão; o motor cuida da conversão linear. |

## Categorias Comuns de Material

| Categoria | Exemplos | Descrição |
|-----------|----------|-----------|
| Solo | `Soil_Grass.png`, `Soil_Dirt.png` | Blocos de superfície de terreno natural. |
| Pedra | `Stone.png`, `Stone_Mossy.png` | Rocha subterrânea e de superfície. |
| Calcita | `Calcite.png`, `Calcite_Brick_Ornate.png` | Pedra de construção de cor clara com muitas variantes decorativas. |
| Argila | `Clay_Black.png` até `Clay_Purple.png` | Blocos de argila coloridos para construção. |
| Minério | Vários minérios por zona | Depósitos minerais com texturas de face distintas. |
| Madeira | Várias espécies de árvores | Texturas de casca (lateral) e anéis (topo). |

## Páginas Relacionadas

- [Modelos de Cliente](/hytale-modding-docs/pt-br/reference/models-and-visuals/client-models) — arquivos `.blockymodel` para blocos com geometria não cúbica
- [Listas de Tipos de Bloco](/hytale-modding-docs/pt-br/reference/game-configuration/block-type-lists) — listas nomeadas que agrupam tipos de blocos por categoria
