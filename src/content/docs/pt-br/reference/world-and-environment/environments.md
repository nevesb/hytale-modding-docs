---
title: Ambientes
description: Referência para definições de ambientes no Hytale, que agendam previsões de clima ponderadas para cada hora do jogo em uma zona ou região.
---

## Visão Geral

Arquivos de ambiente definem o cronograma de clima para uma região do mundo do jogo. Cada arquivo contém um mapa `WeatherForecasts` com 24 entradas — uma por hora do jogo (0–23). A cada hora, o motor amostra da lista ponderada de IDs de clima para determinar qual clima será reproduzido. Múltiplos arquivos de ambiente podem existir para a mesma zona, representando variantes sazonais ou temáticas.

## Localização dos Arquivos

```
Assets/Server/Environments/
  Default.json
  ForgottenTemple.json
  CreativeHub.json
  Portal.json
  Legacy/
  Unique/
  Zone0/
  Zone1/
    Env_Zone1.json
    Env_Zone1_Autumn.json
    Env_Zone1_Azure.json
  Zone2/
  Zone3/
  Zone4/
```

## Schema

### Nível superior

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `WeatherForecasts` | `object` | Sim | — | Mapa de strings de hora (`"0"`–`"23"`) para arrays de `WeatherForecastEntry`. |
| `WaterTint` | `string` | Não | — | Cor hexadecimal aplicada às superfícies de água neste ambiente. |
| `SpawnDensity` | `number` | Não | — | Multiplicador para a densidade de spawn de NPCs neste ambiente. |
| `Tags` | `object` | Não | — | Mapa arbitrário de tags chave-valor usado por outros sistemas para identificar este ambiente. |

### WeatherForecastEntry

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `WeatherId` | `string` | Sim | — | ID da definição de clima a ser potencialmente reproduzida nesta hora. Referencia um arquivo em `Assets/Server/Weathers/`. |
| `Weight` | `number` | Sim | — | Probabilidade relativa de este clima ser selecionado. Um peso de `0` desabilita o clima para aquela hora sem remover a entrada. |

## Como a Amostragem Funciona

A cada hora do jogo, o motor consulta o array naquela chave de hora e realiza uma seleção aleatória ponderada. Entradas com `Weight: 0` nunca são escolhidas. A soma de todos os pesos no array de uma hora não precisa ser igual a 100 — a seleção é proporcional.

## Exemplos

**Ambiente padrão da Zona 1** (`Assets/Server/Environments/Zone1/Env_Zone1.json`, condensado para as horas 0, 4, 18–19):

```json
{
  "WaterTint": "#1983d9",
  "SpawnDensity": 0.5,
  "Tags": {
    "Zone1": []
  },
  "WeatherForecasts": {
    "0": [
      { "WeatherId": "Zone1_Foggy_Light",     "Weight": 0  },
      { "WeatherId": "Zone1_Sunny_Fireflies", "Weight": 0  },
      { "WeatherId": "Zone1_Storm",           "Weight": 1  },
      { "WeatherId": "Zone1_Sunny",           "Weight": 52 },
      { "WeatherId": "Zone1_Cloudy_Medium",   "Weight": 10 },
      { "WeatherId": "Zone1_Rain",            "Weight": 1  },
      { "WeatherId": "Zone1_Rain_Light",      "Weight": 2  }
    ],
    "4": [
      { "WeatherId": "Zone1_Foggy_Light",     "Weight": 30 },
      { "WeatherId": "Zone1_Sunny_Fireflies", "Weight": 0  },
      { "WeatherId": "Zone1_Storm",           "Weight": 1  },
      { "WeatherId": "Zone1_Sunny",           "Weight": 52 },
      { "WeatherId": "Zone1_Cloudy_Medium",   "Weight": 10 },
      { "WeatherId": "Zone1_Rain",            "Weight": 1  },
      { "WeatherId": "Zone1_Rain_Light",      "Weight": 2  }
    ],
    "18": [
      { "WeatherId": "Zone1_Foggy_Light",     "Weight": 0  },
      { "WeatherId": "Zone1_Sunny_Fireflies", "Weight": 20 },
      { "WeatherId": "Zone1_Storm",           "Weight": 1  },
      { "WeatherId": "Zone1_Sunny",           "Weight": 35 },
      { "WeatherId": "Zone1_Cloudy_Medium",   "Weight": 10 },
      { "WeatherId": "Zone1_Rain",            "Weight": 1  },
      { "WeatherId": "Zone1_Rain_Light",      "Weight": 2  }
    ],
    "19": [
      { "WeatherId": "Zone1_Sunny_Fireflies", "Weight": 40 },
      { "WeatherId": "Zone1_Sunny",           "Weight": 35 }
    ]
  }
}
```

Note que `Zone1_Foggy_Light` tem `Weight: 0` durante o dia (horas 0–2) mas ganha peso ao amanhecer (horas 3–7), tornando a neblina um fenômeno apenas matinal. `Zone1_Sunny_Fireflies` só aparece nas horas da noite 18–21.

**Ambiente simples com um único clima** (`Assets/Server/Environments/Default.json`, condensado):

```json
{
  "WeatherForecasts": {
    "0":  [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "1":  [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }],
    "23": [{ "WeatherId": "Zone1_Cloudy_Medium", "Weight": 100 }]
  }
}
```

## Páginas Relacionadas

- [Sistema de Clima](/hytale-modding-docs/reference/world-and-environment/weather-system) — formato de arquivo de clima com parâmetros de céu, nuvens e neblina
- [Fazendas e Galinheiros](/hytale-modding-docs/reference/economy-and-progression/farming-coops) — IDs de clima usados nas condições do modificador Water
- [Configs de Gameplay](/hytale-modding-docs/reference/game-configuration/gameplay-configs) — duração dia/noite que impulsiona a progressão das horas
