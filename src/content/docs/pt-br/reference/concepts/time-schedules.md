---
title: Agendamentos por Horario
description: Como o Hytale usa agendamentos por hora para clima, spawn e mudancas visuais.
---

## Visao Geral

Varios sistemas do Hytale usam agendamentos por hora — arrays indexados por hora (0-23) — para variar o comportamento ao longo do ciclo dia/noite. Previsoes do tempo, cores do ceu, densidade de neblina e janelas de spawn de NPCs usam esse padrao.

## Formato do Agendamento

Os agendamentos usam chaves string de `"0"` a `"23"` representando horas:

```json
{
  "WeatherForecasts": {
    "0": [{ "WeatherId": "Zone1_Clear_Night", "Weight": 100 }],
    "6": [{ "WeatherId": "Zone1_Sunny", "Weight": 70 }, { "WeatherId": "Zone1_Cloudy", "Weight": 30 }],
    "12": [{ "WeatherId": "Zone1_Sunny", "Weight": 50 }, { "WeatherId": "Zone1_Rain", "Weight": 50 }],
    "18": [{ "WeatherId": "Zone1_Cloudy", "Weight": 100 }]
  }
}
```

## DayTimeRange

Regras de spawn usam um formato mais simples `[inicio, fim]`:

```json
{
  "DayTimeRange": [6, 18]
}
```

Isso restringe o spawn para as horas 6:00 ate 18:00 (apenas durante o dia).

## Arrays de Cores por Hora

Visuais de clima usam arrays de 24 elementos para transicoes suaves:

```json
{
  "SkyTopColors": [
    "#0a0a2e", "#0a0a2e", "#0a0a2e", "#0a0a2e", "#0a0a2e", "#1a1a4e",
    "#4a6ea0", "#6a9ec0", "#7ab0d0", "#7ab0d0", "#7ab0d0", "#7ab0d0",
    "#7ab0d0", "#7ab0d0", "#7ab0d0", "#7ab0d0", "#6a9ec0", "#4a6ea0",
    "#2a3e6e", "#1a1a4e", "#0a0a2e", "#0a0a2e", "#0a0a2e", "#0a0a2e"
  ]
}
```

Cada elemento corresponde a uma hora. O jogo interpola entre os valores para transicoes suaves.

## Sistemas que Usam Agendamentos por Horario

| Sistema | Formato | Localizacao |
|---------|---------|-------------|
| Previsoes do tempo | Arrays ponderados por hora | `Server/Environments/` |
| Cores de ceu/neblina/sol | Arrays de cores com 24 elementos | `Server/Weathers/` |
| Velocidade das nuvens | Arrays de float com 24 elementos | `Server/Weathers/` |
| Spawn de NPCs | `DayTimeRange` [inicio, fim] | `Server/NPC/Spawn/` |
| Producao de fazenda | `ResidentRoamTime` [inicio, fim] | `Server/Farming/Coops/` |

## Paginas Relacionadas

- [Weather System](/hytale-modding-docs/reference/world-and-environment/weather-system/) — propriedades visuais por hora
- [Environments](/hytale-modding-docs/reference/world-and-environment/environments/) — agendamentos de previsao do tempo
- [NPC Spawn Rules](/hytale-modding-docs/reference/npc-system/npc-spawn-rules/) — DayTimeRange
