---
title: Modelos de Cliente
description: Referência para arquivos blockymodel do lado do cliente no Hytale, o formato binário de malha voxel usado para blocos, bancadas, mobília e outros objetos interativos do mundo.
---

## Visão Geral

Arquivos de modelo de cliente (`.blockymodel`) definem a geometria da malha voxel para blocos, bancadas, mobília, portas e outros objetos que possuem uma forma visual não padrão. Diferente de blocos cúbicos simples que usam apenas texturas, arquivos blockymodel contêm um modelo voxel 3D completo com ossos nomeados para suporte a animação. Eles são referenciados por definições de bloco do lado do servidor e por arquivos de modelo de servidor via o campo `Model`.

Estes são arquivos binários — não são JSON diretamente editáveis por humanos. São criados na ferramenta Hytale Model Maker e exportados para o formato `.blockymodel`. Esta página documenta as convenções de arquivo, layout de diretórios e como eles se integram ao pipeline de assets.

## Localização dos Arquivos

```
Assets/Common/Blocks/
  Animations/           (arquivos .blockyanim pareados)
  Benches/
    Alchemy.blockymodel
    Anvil.blockymodel
    ArcaneTable.blockymodel
    Armor.blockymodel
    Bedroll.blockymodel
    Builder.blockymodel
    Campfire.blockymodel
    Carpenter.blockymodel
    Cooking.blockymodel
    Farming.blockymodel
    Furnace.blockymodel
    ...
  Chests/
  Coffins/
  Containers/
  Doors/
  Fences/
  Furniture/
  Lights/
  Signs/
  Stairs/
  Trapdoors/
  Walls/
```

## Convenções de Nomenclatura

| Padrão | Exemplo | Descrição |
|--------|---------|-----------|
| `{Objeto}.blockymodel` | `Anvil.blockymodel` | Modelo base para um objeto de variante única. |
| `{Objeto}_{Variante}.blockymodel` | `Campfire_Cooking.blockymodel` | Modelo de variante (ex.: estado diferente do mesmo bloco). |
| `{Categoria}_{Material}.blockymodel` | `Door_Wood.blockymodel` | Variante de material dentro de uma categoria. |

## Pontos de Integração

### Referenciado por Definições de Bloco do Servidor

Arquivos JSON de tipo de bloco referenciam caminhos de blockymodel para sobrescrever a forma cúbica padrão:

```json
{
  "Model": "Blocks/Benches/Anvil.blockymodel"
}
```

### Referenciado por Definições de Modelo de Servidor

Arquivos de modelo de servidor para NPCs e entidades usam o mesmo formato:

```json
{
  "Model": "NPC/Beast/Bear_Grizzly/Models/Model.blockymodel"
}
```

### Pareado com Animações

Muitos arquivos blockymodel possuem arquivos `.blockyanim` correspondentes no diretório `Animations/`. Os nomes de ossos definidos no modelo devem corresponder aos referenciados pelos clipes de animação.

## Estrutura de Ossos

Arquivos blockymodel contêm ossos nomeados que servem como pontos de articulação. Nomes comuns de ossos observados nos modelos de bloco:

| Osso | Usado Em | Propósito |
|------|----------|-----------|
| `Lid` | Baús, Caixões | Tampa articulada para animação de abrir/fechar |
| `Door` | Portas | Painel de porta que gira ou desliza |
| `Flame` | Velas, Fogueiras | Elemento de chama animado |
| `Trapdoor` | Alçapões | Painel de alçapão articulado |

## Fluxo de Trabalho Exemplo

1. Criar um modelo voxel no Model Maker com ossos nomeados
2. Exportar como `.blockymodel` para `Assets/Common/Blocks/{Categoria}/`
3. Criar arquivos `.blockyanim` correspondentes em `Assets/Common/Blocks/Animations/{Categoria}/`
4. Referenciar o caminho do modelo na definição de tipo de bloco do lado do servidor
5. Configurar conjuntos de animação se o bloco possuir estados interativos

## Páginas Relacionadas

- [Animações de Cliente](/hytale-modding-docs/pt-br/reference/models-and-visuals/client-animations) — clipes de animação `.blockyanim` pareados com modelos de bloco
- [Modelos de Servidor](/hytale-modding-docs/pt-br/reference/models-and-visuals/server-models) — definições de modelo do lado do servidor que referenciam caminhos `.blockymodel`
- [Texturas de Blocos](/hytale-modding-docs/pt-br/reference/models-and-visuals/block-textures) — convenções de textura para blocos cúbicos padrão
