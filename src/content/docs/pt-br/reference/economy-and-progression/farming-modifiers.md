---
title: Modificadores de Fazenda
description: Referência para definições de modificadores de crescimento de fazenda no Hytale, cobrindo multiplicadores de água, fertilizante e nível de luz que aceleram o crescimento das plantações.
---

## Visão Geral

Os modificadores de fazenda definem condições ambientais que aceleram ou habilitam o crescimento de plantas e animais. Cada modificador especifica um multiplicador de taxa de crescimento e as condições sob as quais ele se aplica. O sistema suporta três tipos de modificadores: **Water** (proximidade de fluidos ou clima de chuva), **Fertilizer** (aplicado via itens) e **LightLevel** (limiares de luz ambiente ou artificial). Quando múltiplos modificadores estão ativos simultaneamente, seus multiplicadores se acumulam para determinar a taxa de crescimento final.

## Localização dos Arquivos

```
Assets/Server/Farming/Modifiers/
```

Um arquivo JSON por modificador:

```
Assets/Server/Farming/Modifiers/
  Darkness.json
  Fertilizer.json
  LightLevel.json
  Water.json
```

## Schema

### Campos comuns

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Type` | `"Water" \| "LightLevel" \| "Fertilizer"` | Sim | — | Categoria do modificador. Determina quais campos adicionais são relevantes. |
| `Modifier` | `number` | Sim | — | Multiplicador da taxa de crescimento aplicado quando as condições do modificador são atendidas. Valores maiores que `1` aceleram o crescimento; um valor de `2` dobra a taxa, `2.5` multiplica por 2,5x, etc. |

### Campos específicos de Water

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Fluids` | `string[]` | Não | — | IDs de blocos de fontes de fluido que satisfazem a condição de água quando adjacentes (ex: `"Water_Source"`, `"Water"`). |
| `Weathers` | `string[]` | Não | — | IDs de clima que satisfazem a condição de água globalmente (ex: `"Zone1_Rain"`, `"Zone1_Storm"`). |

### Campos específicos de LightLevel

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `ArtificialLight` | `LightChannelRange` | Não | — | Faixa aceitável para fontes de luz artificial (colocadas), definida por canal RGB. |
| `Sunlight` | `Range` | Não | — | Faixa aceitável para intensidade de luz solar. |
| `RequireBoth` | `boolean` | Não | `false` | Se `true`, ambas as condições `ArtificialLight` e `Sunlight` devem ser atendidas simultaneamente. Se `false`, qualquer uma é suficiente. |

### LightChannelRange

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Red` | `Range` | Sim | — | Faixa aceitável para o canal de luz vermelha. |
| `Green` | `Range` | Sim | — | Faixa aceitável para o canal de luz verde. |
| `Blue` | `Range` | Sim | — | Faixa aceitável para o canal de luz azul. |

### Range

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Min` | `number` | Sim | — | Valor mínimo aceitável (inclusivo). |
| `Max` | `number` | Sim | — | Valor máximo aceitável (inclusivo). |

## Exemplos

**Modificador de água** (`Assets/Server/Farming/Modifiers/Water.json`):

```json
{
  "Type": "Water",
  "Modifier": 2.5,
  "Fluids": [
    "Water_Source",
    "Water"
  ],
  "Weathers": [
    "Zone1_Rain",
    "Zone1_Rain_Light",
    "Zone1_Storm",
    "Zone3_Rain"
  ]
}
```

Plantações adjacentes a blocos de água ou expostas à chuva crescem a 2,5x da taxa base.

**Modificador de nível de luz** (`Assets/Server/Farming/Modifiers/LightLevel.json`):

```json
{
  "Type": "LightLevel",
  "Modifier": 2,
  "ArtificialLight": {
    "Red": { "Min": 5, "Max": 127 },
    "Green": { "Min": 5, "Max": 127 },
    "Blue": { "Min": 5, "Max": 127 }
  },
  "Sunlight": {
    "Min": 5.0,
    "Max": 15.0
  },
  "RequireBoth": false
}
```

Plantas que recebem luz solar suficiente OU luz artificial crescem a 2x da taxa base.

**Modificador de escuridão** (`Assets/Server/Farming/Modifiers/Darkness.json`):

```json
{
  "Type": "LightLevel",
  "Modifier": 2,
  "ArtificialLight": {
    "Red": { "Min": 0, "Max": 4 },
    "Green": { "Min": 0, "Max": 4 },
    "Blue": { "Min": 0, "Max": 4 }
  },
  "Sunlight": {
    "Min": 0,
    "Max": 5
  },
  "RequireBoth": true
}
```

Certas plantas que amam sombra prosperam na escuridão. Tanto a luz artificial QUANTO a luz solar devem estar dentro das faixas baixas para que este modificador se aplique.

**Modificador de fertilizante** (`Assets/Server/Farming/Modifiers/Fertilizer.json`):

```json
{
  "Type": "Fertilizer",
  "Modifier": 2
}
```

Quando fertilizante é aplicado a um canteiro, a taxa de crescimento dobra. O tipo fertilizante não tem condições adicionais além de ser aplicado.

## Páginas Relacionadas

- [Fazendas e Galinheiros](/hytale-modding-docs/reference/economy-and-progression/farming-coops) — definições de galinheiros e drops de produtos que funcionam junto com os modificadores de crescimento
- [Tabelas de Drop](/hytale-modding-docs/reference/economy-and-progression/drop-tables) — tabelas de drop de produtos referenciadas pelos galinheiros de fazenda
