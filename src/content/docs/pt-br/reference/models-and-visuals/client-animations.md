---
title: Animações de Cliente
description: Referência para arquivos de animação blockyanim no Hytale, o formato binário de clipe de animação usado por modelos de bloco e entidade para animação por keyframe baseada em ossos.
---

## Visão Geral

Arquivos de animação de cliente (`.blockyanim`) contêm dados de animação por keyframe baseados em ossos para modelos voxel. Eles animam os ossos nomeados definidos em arquivos `.blockymodel` para produzir movimentos como portas abrindo, tampas de baús levantando, chamas de velas tremulando e fogo queimando. Assim como arquivos blockymodel, estes são assets binários criados na ferramenta Hytale Model Maker — não são diretamente editáveis por humanos.

Definições de modelo de servidor referenciam arquivos blockyanim dentro de seus `AnimationSets`. Animações específicas de blocos ficam junto aos seus modelos na árvore de diretórios `Blocks/Animations/`.

## Localização dos Arquivos

```
Assets/Common/Blocks/Animations/
  Candle/
    Candle_Burn.blockyanim
  Chest/
    Chest_Close.blockyanim
    Chest_Open.blockyanim
  Coffin/
    Coffin_Close.blockyanim
    Coffin_Open.blockyanim
  Door/
    Door_Close_In.blockyanim
    Door_Close_Out.blockyanim
    Door_Open_In.blockyanim
    Door_Open_Out.blockyanim
    Door_Open_Slide_In.blockyanim
    Door_Open_Slide_Out.blockyanim
  Fire/
    Fire_Burn.blockyanim
    Fire_Small_Burn.blockyanim
  Light/
    Light_Off.blockyanim
    Light_On.blockyanim
  Trapdoor/
    ...
```

Animações de entidades ficam em um caminho separado:

```
Assets/Common/Characters/Animations/
  Damage/
    Default/
      Hurt.blockyanim
      Hurt2.blockyanim
  ...

Assets/Common/NPC/
  Beast/
    Bear_Grizzly/
      Animations/
        Default/
          Idle.blockyanim
          Run.blockyanim
        Damage/
          Death.blockyanim
  ...
```

## Convenções de Nomenclatura

| Padrão | Exemplo | Descrição |
|--------|---------|-----------|
| `{Objeto}_{Ação}.blockyanim` | `Chest_Open.blockyanim` | Animação de ação principal para um objeto. |
| `{Objeto}_{Ação}_{Direção}.blockyanim` | `Door_Open_In.blockyanim` | Variante direcional de uma ação. |
| `{Ação}.blockyanim` | `Idle.blockyanim` | Animação de entidade nomeada por estado. |
| `{Ação}{N}.blockyanim` | `Hurt2.blockyanim` | Variante numerada para seleção aleatória. |

## Pareamento de Animação

Cada arquivo blockyanim visa ossos definidos em um blockymodel específico. O sistema de animação faz correspondência por nome de osso, então:

- Os nomes dos ossos na animação **devem** corresponder exatamente aos do modelo alvo.
- Uma única animação pode ser compartilhada entre múltiplos modelos se eles definirem os mesmos nomes de ossos.
- Ossos ausentes são silenciosamente ignorados; ossos extras no modelo permanecem estáticos.

## Como as Animações São Referenciadas

### Em AnimationSets de Modelo de Servidor

```json
{
  "AnimationSets": {
    "Idle": {
      "Animations": [
        {
          "Animation": "NPC/Beast/Bear_Grizzly/Animations/Default/Idle.blockyanim",
          "Speed": 0.6
        }
      ]
    }
  }
}
```

### Em Definições de Tipo de Bloco

Tipos de bloco com estados interativos referenciam animações para suas transições de estado (ex.: abrir/fechar):

```json
{
  "OpenAnimation": "Blocks/Animations/Chest/Chest_Open.blockyanim",
  "CloseAnimation": "Blocks/Animations/Chest/Chest_Close.blockyanim"
}
```

## Categorias Comuns de Animação de Bloco

| Categoria | Animações | Descrição |
|-----------|----------|-----------|
| Baú | `Chest_Open`, `Chest_Close` | Animação de dobradiça da tampa para todos os tipos de baú |
| Caixão | `Coffin_Open`, `Coffin_Close` | Animação de deslize da tampa para blocos de caixão |
| Porta | `Door_Open_In/Out`, `Door_Close_In/Out`, `Door_Open_Slide_In/Out` | Variantes de abertura e deslize para portas |
| Vela | `Candle_Burn` | Tremular de chama em loop |
| Fogo | `Fire_Burn`, `Fire_Small_Burn` | Animações de fogo em loop em duas escalas |
| Luz | `Light_On`, `Light_Off` | Animações de alternância para blocos que emitem luz |

## Páginas Relacionadas

- [Modelos de Cliente](/hytale-modding-docs/pt-br/reference/models-and-visuals/client-models) — arquivos de malha `.blockymodel` que definem os ossos animados por estes clipes
- [Conjuntos de Animação](/hytale-modding-docs/pt-br/reference/models-and-visuals/animation-sets) — como clipes de animação são agrupados em conjuntos nomeados
- [Modelos de Servidor](/hytale-modding-docs/pt-br/reference/models-and-visuals/server-models) — definições de modelo de servidor que conectam animações a estados de entidade
