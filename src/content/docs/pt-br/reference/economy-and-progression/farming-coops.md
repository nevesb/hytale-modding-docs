---
title: Fazendas e Galinheiros
description: Referência para definições de galinheiros de fazenda e modificadores de crescimento no Hytale, incluindo grupos de NPCs residentes, tabelas de drop de produtos, cronogramas de perambulação e modificadores ambientais.
---

## Visão Geral

O sistema de fazenda possui dois tipos de assets: **Coops** (galinheiros) e **Modifiers** (modificadores). Os galinheiros definem cercados que abrigam NPCs animais e produzem drops ao longo do tempo — eles especificam quais grupos de NPCs podem morar no galinheiro, quantos residentes são permitidos e qual tabela de drop cada espécie produz. Os modificadores definem multiplicadores ambientais (água, luz, fertilizante) que aceleram as taxas de crescimento de plantas ou animais.

## Localização dos Arquivos

```
Assets/Server/Farming/
  Coops/
    Coop_Chicken.json
  Modifiers/
    Darkness.json
    Fertilizer.json
    LightLevel.json
    Water.json
```

## Schema do Coop

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `MaxResidents` | `number` | Sim | — | Número máximo de NPCs residentes que o galinheiro pode abrigar simultaneamente. |
| `ProduceDrops` | `object` | Sim | — | Mapa de ID do grupo de NPC → ID da tabela de drop. Cada espécie residente tem sua própria tabela de drop de produtos. |
| `ResidentRoamTime` | `[number, number]` | Sim | — | Faixa de horas no jogo `[início, fim]` durante as quais os residentes perambulam livremente dentro do galinheiro. |
| `ResidentSpawnOffset` | `Vector3` | Não | — | Deslocamento local aplicado ao spawnar um residente dentro da estrutura do galinheiro. |
| `AcceptedNpcGroups` | `string[]` | Sim | — | Lista de IDs de grupos de NPCs que podem ser colocados ou capturados neste tipo de galinheiro. |
| `CaptureWildNPCsInRange` | `boolean` | Não | `false` | Se `true`, NPCs selvagens de grupos aceitos dentro do alcance são automaticamente capturados no galinheiro. |
| `WildCaptureRadius` | `number` | Não | — | Raio em unidades dentro do qual NPCs selvagens são auto-capturados quando `CaptureWildNPCsInRange` é `true`. |

### Vector3

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `X` | `number` | Sim | — | Deslocamento lateral. |
| `Y` | `number` | Sim | — | Deslocamento vertical. |
| `Z` | `number` | Sim | — | Deslocamento frontal. |

## Schema do Modifier

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Type` | `"Water" \| "Fertilizer" \| "LightLevel" \| "Darkness"` | Sim | — | Categoria do modificador, usada para corresponder o modificador aos sistemas de crescimento aplicáveis. |
| `Modifier` | `number` | Sim | — | Multiplicador da taxa de crescimento aplicado quando as condições deste modificador são satisfeitas (ex: `2.5` = 2,5x mais rápido). |
| `Fluids` | `string[]` | Não | — | Apenas tipo `Water`. IDs de blocos fluidos cuja presença satisfaz a condição de água. |
| `Weathers` | `string[]` | Não | — | Apenas tipo `Water`. IDs de clima que também contam como fonte de água (ex: chuva). |
| `ArtificialLight` | `LightRange` | Não | — | Apenas tipo `LightLevel`. Faixas de canais RGB que devem ser atendidas por fontes de luz artificial. |
| `Sunlight` | `SunlightRange` | Não | — | Apenas tipo `LightLevel`. Faixa de nível de luz solar que deve ser atendida. |
| `RequireBoth` | `boolean` | Não | `false` | Apenas tipo `LightLevel`. Se `true`, ambas as condições `ArtificialLight` e `Sunlight` devem ser atendidas simultaneamente. |

### LightRange (por canal RGB)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Min` | `number` | Sim | — | Nível mínimo de luz (0–255). |
| `Max` | `number` | Sim | — | Nível máximo de luz (0–255). |

### SunlightRange

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Min` | `number` | Sim | — | Nível mínimo de luz solar (0–15). |
| `Max` | `number` | Sim | — | Nível máximo de luz solar (0–15). |

## Exemplos

**Galinheiro de galinhas** (`Assets/Server/Farming/Coops/Coop_Chicken.json`):

```json
{
  "MaxResidents": 6,
  "ProduceDrops": {
    "Chicken": "Drop_Chicken_Produce",
    "Chicken_Desert": "Drop_Chicken_Produce",
    "Skrill": "Drop_Chicken_Produce"
  },
  "ResidentRoamTime": [6, 18],
  "ResidentSpawnOffset": {
    "X": 0,
    "Y": 0,
    "Z": 3
  },
  "AcceptedNpcGroups": [
    "Chicken",
    "Chicken_Desert",
    "Skrill"
  ],
  "CaptureWildNPCsInRange": true,
  "WildCaptureRadius": 10
}
```

**Modificador de água** (`Assets/Server/Farming/Modifiers/Water.json`):

```json
{
  "Type": "Water",
  "Modifier": 2.5,
  "Fluids": ["Water_Source", "Water"],
  "Weathers": ["Zone1_Rain", "Zone1_Rain_Light", "Zone1_Storm", "Zone3_Rain"]
}
```

**Modificador de fertilizante** (`Assets/Server/Farming/Modifiers/Fertilizer.json`):

```json
{
  "Type": "Fertilizer",
  "Modifier": 2
}
```

**Modificador de nível de luz** (`Assets/Server/Farming/Modifiers/LightLevel.json`):

```json
{
  "Type": "LightLevel",
  "Modifier": 2,
  "ArtificialLight": {
    "Red":   { "Min": 5, "Max": 127 },
    "Green": { "Min": 5, "Max": 127 },
    "Blue":  { "Min": 5, "Max": 127 }
  },
  "Sunlight": {
    "Min": 5.0,
    "Max": 15.0
  },
  "RequireBoth": false
}
```

## Páginas Relacionadas

- [Tabelas de Drop](/hytale-modding-docs/reference/economy-and-progression/drop-tables) — formato de tabela de drop usado em `ProduceDrops`
- [Sistema de Clima](/hytale-modding-docs/reference/world-and-environment/weather-system) — IDs de clima referenciados em `Water.Weathers`
- [Lojas de Troca](/hytale-modding-docs/reference/economy-and-progression/barter-shops) — venda de produtos da fazenda
