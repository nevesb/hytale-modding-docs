---
title: Listas de Tipos de Blocos
description: Referência para definições de listas de tipos de blocos no Hytale, que agrupam IDs de tipos de blocos em categorias nomeadas usadas pela geração de mundo, regras do jogo e sistemas de filtragem.
---

## Visão Geral

Arquivos de lista de tipos de blocos definem grupos nomeados de IDs de tipos de blocos. Essas listas são referenciadas por outros sistemas — a geração de mundo as utiliza para determinar quais blocos podem ser espalhados, substituídos ou coletados, e as regras do jogo as utilizam para filtrar interações com blocos. Cada lista é simplesmente um objeto JSON com um array `Blocks` contendo IDs em formato de string que correspondem a tipos de blocos registrados.

## Localização dos Arquivos

```
Assets/Server/BlockTypeList/
  AllScatter.json
  Empty.json
  Gravel.json
  Ores.json
  PlantScatter.json
  PlantsAndTrees.json
  Rock.json
  Snow.json
  Soils.json
  TreeLeaves.json
  TreeWood.json
  TreeWoodAndLeaves.json
```

## Schema

### Nível Superior

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `Blocks` | `string[]` | Sim | — | Array de strings com IDs de tipos de blocos. Cada ID deve corresponder a um nome de tipo de bloco registrado. |

## Descrições das Listas

| Lista | Tamanho Aproximado | Descrição |
|-------|---------------------|-----------|
| `AllScatter` | ~160 entradas | Todos os blocos decorativos de dispersão: gramas, flores, samambaias, escombros, ossos, corais e decorações de ninhos. |
| `Empty` | 0 entradas | Lista vazia usada como placeholder "nenhum". |
| `Gravel` | Pequeno | Variantes de blocos de cascalho. |
| `Ores` | Pequeno | Blocos de minério mineráveis em todas as zonas. |
| `PlantScatter` | Médio | Subconjunto de dispersão limitado a plantas e flores. |
| `PlantsAndTrees` | Médio | Plantas, flores e blocos relacionados a árvores. |
| `Rock` | Pequeno | Blocos naturais de rocha e pedra. |
| `Snow` | Pequeno | Variantes de blocos cobertos de neve. |
| `Soils` | ~13 entradas | Blocos de solo e grama de terreno em diferentes tipos de bioma. |
| `TreeLeaves` | Pequeno | Blocos de folhas de todas as espécies de árvores. |
| `TreeWood` | Pequeno | Blocos de tronco/madeira de todas as espécies de árvores. |
| `TreeWoodAndLeaves` | Médio | Blocos combinados de madeira e folhas de árvores. |

## Exemplos

**Lista de solos** (`Assets/Server/BlockTypeList/Soils.json`):

```json
{
  "Blocks": [
    "Soil_Dirt",
    "Soil_Dirt_Burnt",
    "Soil_Dirt_Cold",
    "Soil_Dirt_Dry",
    "Soil_Dirt_Poisoned",
    "Soil_Grass",
    "Soil_Grass_Burnt",
    "Soil_Grass_Cold",
    "Soil_Grass_Deep",
    "Soil_Grass_Dry",
    "Soil_Grass_Full",
    "Soil_Grass_Sunny",
    "Soil_Grass_Wet"
  ]
}
```

**Lista AllScatter** (`Assets/Server/BlockTypeList/AllScatter.json`, resumida):

```json
{
  "Blocks": [
    "Wood_Sticks",
    "Plant_Bush_Green",
    "Plant_Grass_Arid",
    "Plant_Grass_Arid_Short",
    "Plant_Grass_Lush",
    "Plant_Flower_Bushy_Blue",
    "Plant_Flower_Common_Red",
    "Plant_Fern",
    "Rubble_Stone",
    "Rubble_Sandstone",
    "Deco_Bone_Skulls_Feran",
    "Deco_Coral_Shell",
    "Deco_Trash"
  ]
}
```

## Páginas Relacionadas

- [Geração de Mundo](/hytale-modding-docs/reference/world-and-environment/world-generation) — atribuições que referenciam listas de tipos de blocos para posicionamento de dispersão
- [Texturas de Blocos](/hytale-modding-docs/reference/models-and-visuals/block-textures) — arquivos de textura para os blocos referenciados nestas listas
- [Objetivos](/hytale-modding-docs/reference/game-configuration/objectives) — condições de tarefas que filtram por tags de blocos correspondentes a estas listas
