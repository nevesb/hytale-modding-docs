---
title: Geração de Mundo
description: Referência para arquivos de geração de mundo no Hytale, cobrindo o pipeline HytaleGenerator incluindo biomas, mapas de densidade, atribuições, máscaras de blocos e configurações de estrutura do mundo.
---

## Visão Geral

A geração de mundo no Hytale é conduzida por um pipeline baseado em grafo de nós chamado **HytaleGenerator**. Ele produz terreno através de funções de ruído em camadas, mapas de densidade, definições de biomas e atribuições de prefabs ponderados. Cada componente é definido em um arquivo JSON separado e conectado através de referências de importação/exportação. O sistema suporta formas de continente procedurais, zonas climáticas, redes de cavernas, escavação de rios e posicionamento de dispersão por bioma.

## Localização dos Arquivos

```
Assets/Server/HytaleGenerator/
  Assignments/
    Boreal1/
      Boreal1_Hedera_Trees.json
      Boreal1_Hedera_Mushrooms.json
      ...
    Desert1/
    Plains1/
    Volcanic1/
  Biomes/
    Basic.json
    Boreal1/
      Boreal1_Hedera.json
      Boreal1_Henges.json
    Desert1/
    Plains1/
    Volcanic1/
    Default_Flat/
    Default_Void/
  BlockMasks/
  Density/
    Map_Default.json
    Map_Portals.json
    Map_Tiles.json
    Plains1_Caves_Terrain.json
    ...
  Graphs/
  Settings/
    Settings.json
  WorldStructures/
```

## Schema

### Settings (Settings.json)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `StatsCheckpoints` | `number[]` | Não | — | Limiares de contagem de chunks nos quais estatísticas de geração são registradas. |
| `CustomConcurrency` | `number` | Não | `-1` | Contagem de threads para geração. `-1` usa o padrão do motor. |
| `BufferCapacityFactor` | `number` | Não | `0.1` | Fração da memória total alocada para buffers de geração. |
| `TargetViewDistance` | `number` | Não | `512` | Distância de visualização alvo em blocos usada para pré-computar prioridade de geração. |
| `TargetPlayerCount` | `number` | Não | `3` | Contagem esperada de jogadores usada para dimensionar filas de geração. |

### Nó de Densidade (arquivos de grafo de nós)

Arquivos de densidade definem uma árvore de nós de processamento que produz um campo escalar usado para forma de terreno, escavação de rios ou mapeamento de biomas. Cada nó tem no mínimo:

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `$NodeId` | `string` | Sim | — | Identificador único para este nó no grafo. |
| `Type` | `string` | Sim | — | Tipo do nó. Veja tipos de nós abaixo. |
| `Skip` | `boolean` | Não | `false` | Quando `true`, o nó é ignorado durante a geração. |
| `ExportAs` | `string` | Não | — | Nome sob o qual a saída deste nó é publicada para importação por outros grafos. |
| `SingleInstance` | `boolean` | Não | `false` | Quando `true`, o nó é avaliado uma vez e cacheado globalmente. |
| `Inputs` | `DensityNode[]` | Não | `[]` | Nós filhos cujas saídas alimentam este nó. |

#### Tipos Comuns de Nós de Densidade

| Type | Description | Key Fields |
|------|-------------|------------|
| `SimplexNoise2D` | Gerador de ruído simplex 2D | `Lacunarity`, `Persistence`, `Octaves`, `Scale`, `Seed` |
| `Constant` | Produz um valor fixo | `Value` |
| `Sum` | Soma todos os valores de entrada | — |
| `Min` / `Max` | Retorna o mínimo ou máximo das entradas | — |
| `Clamp` | Limita a entrada entre dois limites | `WallA`, `WallB` |
| `Normalizer` | Remapeia uma faixa de valores | `FromMin`, `FromMax`, `ToMin`, `ToMax` |
| `Inverter` | Nega a entrada | — |
| `Abs` | Valor absoluto | — |
| `Mix` | Mistura duas entradas usando uma terceira como alfa | — |
| `Scale` | Multiplica coordenadas de entrada | `ScaleX`, `ScaleY`, `ScaleZ` |
| `Cache` | Cacheia o resultado dos nós filhos | `Capacity` |
| `YOverride` | Força uma coordenada Y fixa para avaliação 2D | `Value` |
| `Distance` | Distância da origem com uma curva de atenuação | `Curve` |
| `Exported` | Marca a saída de um nó para importação entre grafos | `ExportAs`, `SingleInstance` |
| `Imported` | Referencia um nó exportado por nome | `Name` |

### Assignment (posicionamento de dispersão/prefab)

Arquivos de atribuição controlam quais decorações, vegetação ou estruturas são colocadas em uma região de bioma. Eles usam uma abordagem de função de campo com delimitadores.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Type` | `string` | Sim | — | Tipo de nível superior, tipicamente `"FieldFunction"`. |
| `ExportAs` | `string` | Não | — | Nome de exportação para esta atribuição. |
| `FieldFunction` | `FieldFunction` | Sim | — | Função de ruído que produz o campo de densidade de posicionamento. |
| `Delimiters` | `Delimiter[]` | Sim | — | Faixas dentro da saída da função de campo que ativam o posicionamento. |

#### FieldFunction

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Type` | `string` | Sim | — | Tipo de ruído, ex: `"SimplexNoise2D"`. |
| `Skip` | `boolean` | Não | `false` | Ignora esta função. |
| `Lacunarity` | `number` | Não | `2` | Multiplicador de frequência por oitava. |
| `Persistence` | `number` | Não | `0.5` | Multiplicador de amplitude por oitava. |
| `Octaves` | `number` | Não | `1` | Número de oitavas de ruído. |
| `Scale` | `number` | Sim | — | Escala espacial do ruído. |
| `Seed` | `string` | Sim | — | String de semente para geração determinística. |

#### Delimiter

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Min` | `number` | Sim | — | Valor mínimo do campo para esta faixa. |
| `Max` | `number` | Sim | — | Valor máximo do campo para esta faixa. |
| `Assignments` | `AssignmentNode` | Sim | — | O que posicionar quando o valor do campo cai nesta faixa. |

#### AssignmentNode

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Type` | `string` | Sim | — | `"Weighted"`, `"Constant"` ou `"Cluster"`. |
| `SkipChance` | `number` | Não | `0` | Probabilidade (0–1) de pular o posicionamento inteiramente. |
| `Seed` | `string` | Não | — | Semente para seleção aleatória ponderada. |
| `WeightedAssignments` | `WeightedEntry[]` | Não | — | Array de opções ponderadas (quando `Type` é `"Weighted"`). |
| `Prop` | `PropConfig` | Não | — | Prefab/prop a ser posicionado (quando `Type` é `"Constant"` ou dentro de uma entrada ponderada). |

## Exemplo

**Mapa de densidade** (`Assets/Server/HytaleGenerator/Density/Map_Default.json`, condensado para mostrar a estrutura):

```json
{
  "$NodeId": "Exported.Density-ed27c3c9",
  "Type": "Exported",
  "ExportAs": "Biome-Map",
  "SingleInstance": true,
  "Inputs": [
    {
      "Type": "YOverride",
      "Value": 0,
      "Inputs": [
        {
          "Type": "Cache",
          "Capacity": 1,
          "Inputs": [
            {
              "Type": "Mix",
              "Inputs": [
                { "Type": "Imported", "Name": "Biome-Map-Tiles" },
                { "Type": "Constant", "Value": -0.3 },
                {
                  "Type": "Clamp",
                  "WallA": 0,
                  "WallB": 1,
                  "Inputs": [
                    {
                      "Type": "Normalizer",
                      "FromMin": 0.62,
                      "FromMax": 0.62,
                      "ToMin": 0,
                      "ToMax": 1,
                      "Inputs": [
                        { "Type": "Exported", "ExportAs": "World-River-Map" }
                      ]
                    }
                  ]
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

**Configurações do gerador** (`Assets/Server/HytaleGenerator/Settings/Settings.json`):

```json
{
  "StatsCheckpoints": [1, 100, 500, 1000],
  "CustomConcurrency": -1,
  "BufferCapacityFactor": 0.1,
  "TargetViewDistance": 512,
  "TargetPlayerCount": 3
}
```

## Páginas Relacionadas

- [Máscaras de Mundo](/hytale-modding-docs/reference/world-and-environment/world-masks) — máscaras de ruído para forma de continente, temperatura e clima
- [Ambientes](/hytale-modding-docs/reference/world-and-environment/environments) — definições de ambiente atribuídas por zona
- [Instâncias](/hytale-modding-docs/reference/game-configuration/instances) — configs de instância que selecionam um perfil de geração de mundo
