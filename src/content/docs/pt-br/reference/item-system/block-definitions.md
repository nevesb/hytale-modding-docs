---
title: Definições de Blocos
description: Referência para arquivos JSON de definição de blocos no Hytale, cobrindo texturas, materiais, luz e tipos de desenho para blocos do mundo.
---

## Visão Geral

Definições de blocos descrevem as propriedades visuais e físicas dos blocos colocados no mundo. A maioria dos dados de blocos fica dentro do objeto `BlockType` de um arquivo de definição de item, mas arquivos de bloco independentes existem para fluidos, efeitos de fluido e decalques de quebra. Texturas podem ser especificadas por face ou como um atalho único `All`, com valores opcionais de `Weight` para variantes aleatórias.

## Localização dos Arquivos

Dados de blocos são armazenados em dois lugares:

- **Blocos embutidos em itens** (rochas, madeira, solo, etc.): objeto `BlockType` dentro de `Assets/Server/Item/Items/<Category>/<ItemId>.json`
- **Arquivos de bloco independentes** (fluidos, decalques, efeitos de fluido): `Assets/Server/Item/Block/<Subcategory>/<BlockId>.json`

Subcategorias em `Assets/Server/Item/Block/`:
```
Block/Fluids/          — Blocos de fluido (Lava, Água, Slime, Veneno, Fogo)
Block/BreakingDecals/  — Sobreposições de rachaduras na animação de quebra
Block/FluidFX/         — Configs de efeitos visuais de fluidos
Block/Hitboxes/        — Definições de formas de hitbox personalizadas
Block/Blocks/_Debug/   — Blocos de teste apenas para debug
```

## Schema

### Campos do Objeto de Textura

Cada entrada no array `Textures` define uma variante de textura. Múltiplas entradas com valores de `Weight` habilitam seleção aleatória de texturas.

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `All` | string | Não | — | Caminho de textura aplicado a todas as seis faces do bloco. |
| `Sides` | string | Não | — | Textura aplicada às quatro faces laterais (Norte, Sul, Leste, Oeste). |
| `UpDown` | string | Não | — | Textura aplicada às faces superior e inferior. |
| `Top` | string | Não | — | Textura aplicada apenas à face superior. |
| `Bottom` | string | Não | — | Textura aplicada apenas à face inferior. |
| `North` | string | Não | — | Textura aplicada apenas à face norte. |
| `South` | string | Não | — | Textura aplicada apenas à face sul. |
| `East` | string | Não | — | Textura aplicada apenas à face leste. |
| `West` | string | Não | — | Textura aplicada apenas à face oeste. |
| `Weight` | number | Não | `1` | Peso de probabilidade relativa para esta variante quando múltiplas entradas de textura estão presentes. |

### Campos de BlockType / Nível de Bloco

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `Textures` | object[] | Não | — | Array de objetos de variante de textura (veja acima). |
| `Material` | string | Não | — | Categoria de material físico. Valores: `Solid`, `Fluid`, `Empty`, `Plant`. Controla colisão e comportamento de interação. |
| `DrawType` | string | Não | — | Modo de renderização. Valores comuns: `Model` (mesh personalizado), `Block` (cubo padrão), `Plant` (folhagem billboard). |
| `Opacity` | string | Não | — | Nível de transparência. Valores: `Opaque`, `Semitransparent`, `Transparent`. |
| `Light` | object | Não | — | Config de emissão de luz. Contém `Color` (string hex, ex.: `"#e90"`) e opcionalmente `Level` (número). |
| `ParticleColor` | string | Não | — | Cor hex para efeitos de partículas de quebra de bloco (ex.: `"#58ad9b"`). |
| `CustomModel` | string | Não | — | Caminho para um arquivo `.blockymodel` usado em vez de um mesh de cubo padrão. |
| `CustomModelTexture` | object[] | Não | — | Array de `{ "Texture": "<caminho>", "Weight": <número> }` para variantes de textura de modelo personalizado. |
| `CustomModelScale` | number | Não | `1.0` | Multiplicador de escala para o modelo personalizado. |
| `HitboxType` | string | Não | — | ID de uma definição de hitbox de `Block/Hitboxes/`. |
| `RandomRotation` | string | Não | — | Rotação aleatória ao colocar. Exemplo: `"YawStep1"`. |
| `BlockParticleSetId` | string | Não | — | Conjunto de partículas usado para partículas ambientes do bloco (ex.: `"Lava"`, `"Dust"`). |
| `BlockSoundSetId` | string | Não | — | ID do conjunto de sons para sons de interação com o bloco. |
| `Gathering` | object | Não | — | Configuração de colheita. Objetos filhos `Harvest`, `Soft` e `Breaking` aceitam cada um uma string `GatherType`. |
| `Aliases` | string[] | Não | — | IDs de string alternativos para este bloco, usados por comandos e geração de mundo. |

### Campos Específicos de Fluidos

Estes campos aparecem em arquivos de bloco de fluido independentes em `Block/Fluids/`.

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `MaxFluidLevel` | number | Não | — | Nível máximo inteiro do fluido. Blocos fonte tipicamente usam `1`; fluidos em movimento usam `8`. |
| `Effect` | string[] | Não | — | Lista de IDs de efeito aplicados quando uma entidade entra neste fluido (ex.: `["Lava"]`). |
| `FluidFXId` | string | Não | — | Referencia uma config de efeito visual de fluido de `Block/FluidFX/`. |
| `Ticker` | object | Não | — | Comportamento de fluxo do fluido. Contém `CanDemote` (boolean), `SpreadFluid` (string), `FlowRate` (número), `SupportedBy` (string) e `Collisions` (objeto mapeando IDs de bloco para resultados de colocação). |
| `Interactions` | object | Não | — | Cadeias de interação no nível do bloco (ex.: efeitos de colisão). Usa o mesmo formato de cadeia das interações de item. |
| `Parent` | string | Não | — | ID de um bloco pai para herdar campos. |

## Exemplo

`Assets/Server/Item/Items/Rock/Rock_Aqua.json` (seção BlockType):

```json
{
  "TranslationProperties": {
    "Name": "server.items.Rock_Aqua.name"
  },
  "Icon": "Icons/ItemsGenerated/Rock_Aqua.png",
  "Parent": "Rock_Stone",
  "BlockType": {
    "Textures": [
      {
        "All": "BlockTextures/Rock_Aqua.png",
        "Weight": 1
      }
    ],
    "ParticleColor": "#58ad9b",
    "Gathering": {
      "Breaking": {
        "GatherType": "Rocks"
      }
    },
    "Aliases": [
      "aqua",
      "aqua00"
    ]
  }
}
```

`Assets/Server/Item/Block/Blocks/_Debug/Debug_Test_Block.json` (bloco independente com luz):

```json
{
  "Textures": [
    {
      "All": "Blocks/_Debug/Texture.png"
    }
  ],
  "Material": "Solid",
  "Light": {
    "Color": "#f0f"
  }
}
```

`Assets/Server/Item/Block/Fluids/Lava_Source.json` (bloco de fluido):

```json
{
  "MaxFluidLevel": 1,
  "Effect": ["Lava"],
  "Opacity": "Transparent",
  "Textures": [
    {
      "Weight": 1,
      "All": "BlockTextures/Fluid_Lava.png"
    }
  ],
  "Light": {
    "Color": "#e90"
  },
  "Ticker": {
    "CanDemote": false,
    "SpreadFluid": "Lava",
    "FlowRate": 2.0,
    "Collisions": {
      "Water": {
        "BlockToPlace": "Rock_Stone_Cobble",
        "SoundEvent": "SFX_Flame_Break"
      }
    }
  }
}
```

## Páginas Relacionadas

- [Definições de Itens](/hytale-modding-docs/reference/item-system/item-definitions) — Schema completo de definição de itens incluindo BlockType
- [Grupos de Itens](/hytale-modding-docs/reference/item-system/item-groups) — Conjuntos nomeados de IDs de bloco usados por receitas e sistemas
- [Interações de Itens](/hytale-modding-docs/reference/item-system/item-interactions) — Cadeias de interação usadas em gatilhos de colisão de fluidos
