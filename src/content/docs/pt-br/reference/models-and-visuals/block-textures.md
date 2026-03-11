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
| Densidade de pixels | 32 px por face de bloco | O guia do Hytale Modding descreve blocos com padrão de densidade de 32 px. |
| Transparência | Suportada | Canal alfa permite blocos parcialmente transparentes (vidro, folhas). |
| Espaço de Cor | sRGB | Espaço de cor padrão; o motor cuida da conversão linear. |

## Guia Prático de Tamanhos

A referência do Hytale Modding diferencia melhor **densidade de pixels** de tamanho fixo de arquivo. A regra mais segura é combinar a densidade do tipo de asset, em vez de forçar tudo para a mesma resolução.

| Tipo de asset | Densidade recomendada | Exemplos práticos | Observações |
|---------------|-----------------------|-------------------|-------------|
| Blocos cúbicos | 32 px por face de bloco | `32x32` para uma face normal, `64x64` para uma variante 2x mantendo a mesma densidade | Este é o padrão mais claramente documentado. |
| Modelos de player | 64 px de densidade | `64x64`, `128x128` | Tamanhos maiores funcionam se preservarem a mesma densidade visual. |
| Modelos de NPC / mob | 64 px de densidade | `64x64`, `128x128` | O guia externo descreve mobs como "provavelmente também 64px"; trate isso como melhor prática atual, não como regra absoluta do engine. |
| Equipamentos / itens segurados com modelo | 64 px de densidade | textura de espada `64x64`, textura de armadura `128x128` | Isso vale para texturas de modelo, não para ícones de inventário. |
| Ícones de item / UI | Varia conforme a direção de arte da UI | `32x32`, `64x64`, `128x128` | A referência não define uma densidade canônica única para ícones, então mantenha consistência dentro do mesmo conjunto visual. |

### Exemplos

- Um bloco de pedra simples: uma textura `32x32`, opcionalmente com variantes `_Top`, `_Side` e `_Bottom`.
- Uma textura de peitoral de player: `64x64` ou `128x128`, desde que respeite a densidade de 64 px do modelo do personagem.
- Uma textura de NPC grande ou chefe: `128x128` ainda pode estar correta se o modelo preservar a mesma densidade visual dos demais personagens 64 px.
- Um ícone de espada no inventário: mantenha alinhado com o restante do atlas de ícones; isso é uma decisão de UI, não a mesma regra de blocos ou personagens.

## Nota de Precisão

Uma versão anterior deste manual descrevia texturas de blocos como "16x16 pixels (padrão)". Isso era rígido demais em relação à referência atual do Hytale Modding, que aponta para um padrão de **densidade de 32 px para blocos**.

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
