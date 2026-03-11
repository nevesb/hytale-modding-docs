---
title: Sistema de Clima
description: Referência para arquivos de definição de clima no Hytale, cobrindo cores do céu, camadas de nuvens, neblina, visuais de sol e lua, e partículas ambientais.
---

## Visão Geral

Arquivos de clima definem o estado visual completo do céu para uma condição climática nomeada. Todas as propriedades de cor e escala usam um array de entradas com chave de tempo — o motor interpola entre keyframes conforme a hora do jogo progride. Camadas de nuvens, densidade de neblina, cores de sol/lua e partículas ambientais são todas controladas aqui. Os IDs de clima definidos nesses arquivos são referenciados pelos [cronogramas de previsão de ambiente](/hytale-modding-docs/reference/world-and-environment/environments).

## Localização dos Arquivos

```
Assets/Server/Weathers/
  Blood_Moon.json
  Creative_Hub.json
  Forgotten_Temple.json
  Void.json
  Unique/
  Zone1/
    Cave_Deep.json
    Cave_Fog.json
    Cave_Goblin.json
    (Zone1_Sunny.json, Zone1_Rain.json, etc.)
  Zone2/
  Zone3/
  Zone4/
  Skylands/
  Minigames/
```

## Schema

### Nível superior

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Stars` | `string` | Não | — | Caminho para a textura do campo de estrelas renderizado à noite. |
| `Moons` | `MoonEntry[]` | Não | — | Texturas de fases da lua, uma por dia no ciclo lunar. |
| `Clouds` | `CloudLayer[]` | Não | — | Lista ordenada de camadas de textura de nuvens compostas sobre o céu. |
| `SkyTopColors` | `HourColor[]` | Não | — | Keyframes de cor do zênite do céu. |
| `SkyBottomColors` | `HourColor[]` | Não | — | Keyframes de cor do horizonte do céu. |
| `SkySunsetColors` | `HourColor[]` | Não | — | Keyframes de cor de tonalidade do pôr/nascer do sol. |
| `FogColors` | `HourColor[]` | Não | — | Keyframes de cor da neblina. |
| `FogDensities` | `HourValue[]` | Não | — | Keyframes de densidade da neblina (0–1). |
| `FogHeightFalloffs` | `HourValue[]` | Não | — | Keyframes de atenuação de altura da neblina. |
| `FogDistance` | `[number, number]` | Não | — | Faixa de distância da neblina `[perto, longe]` em unidades. |
| `FogOptions` | `FogOptions` | Não | — | Opções adicionais de renderização de neblina. |
| `SunColors` | `HourColor[]` | Não | — | Keyframes de cor do disco solar. |
| `SunGlowColors` | `HourColor[]` | Não | — | Keyframes de cor do halo do brilho solar. |
| `SunScales` | `HourValue[]` | Não | — | Keyframes de escala do disco solar. |
| `MoonColors` | `HourColor[]` | Não | — | Keyframes de cor do disco lunar. |
| `MoonGlowColors` | `HourColor[]` | Não | — | Keyframes de cor do halo do brilho lunar. |
| `MoonScales` | `HourValue[]` | Não | — | Keyframes de escala do disco lunar. |
| `Particle` | `WeatherParticle` | Não | — | Sistema de partículas ambientais reproduzido durante este clima (ex: chuva, neve, vagalumes). |

### MoonEntry

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Day` | `number` | Sim | — | Índice do dia no ciclo lunar (base 0). |
| `Texture` | `string` | Sim | — | Caminho para a textura da fase da lua para este dia do ciclo. |

### CloudLayer

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Texture` | `string` | Sim | — | Caminho para a textura de nuvem desta camada. |
| `Colors` | `HourColor[]` | Sim | — | Keyframes de cor RGBA controlando visibilidade e tonalidade da nuvem ao longo do dia. |
| `Speeds` | `HourValue[]` | Sim | — | Keyframes de velocidade de rolagem para esta camada de nuvem. |

### HourColor

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Hour` | `number` | Sim | — | Hora do jogo (0–23) em que esta cor se aplica. O motor interpola entre keyframes. |
| `Color` | `string` | Sim | — | String de cor hexadecimal, opcionalmente com alfa (ex: `"#ffffffe6"`, `"rgba(#2c6788, 1)"`). |

### HourValue

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Hour` | `number` | Sim | — | Hora do jogo (0–23). |
| `Value` | `number` | Sim | — | Valor numérico nesta hora (escala, densidade, velocidade, etc.). |

### FogOptions

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `FogHeightCameraFixed` | `number` | Não | — | Trava o plano de altura da neblina relativo à câmera em vez do mundo. |
| `EffectiveViewDistanceMultiplier` | `number` | Não | `1.0` | Escala a distância efetiva de visualização durante este clima. |

### WeatherParticle

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `SystemId` | `string` | Sim | — | ID do sistema de partículas para reproduzir como efeito climático ambiental. |
| `OvergroundOnly` | `boolean` | Não | `false` | Se `true`, partículas só aparecem em áreas acima do solo. |
| `Color` | `string` | Não | — | Cor hexadecimal de tonalidade aplicada ao sistema de partículas. |

## Exemplo

**Clima ensolarado da Zona 1** (`Assets/Server/Weathers/Zone1/Cave_Deep.json` — note que este mostra uma variante de caverna; os climas principais da Zone1 seguem o mesmo schema):

```json
{
  "Stars": "Sky/Stars.png",
  "Moons": [
    { "Day": 0, "Texture": "Sky/MoonCycle/Moon_Full.png"     },
    { "Day": 1, "Texture": "Sky/MoonCycle/Moon_Gibbous.png"  },
    { "Day": 2, "Texture": "Sky/MoonCycle/Moon_Half.png"     },
    { "Day": 3, "Texture": "Sky/MoonCycle/Moon_Crescent.png" },
    { "Day": 4, "Texture": "Sky/MoonCycle/Moon_New.png"      }
  ],
  "Clouds": [
    {
      "Texture": "Sky/Clouds/Light_Base.png",
      "Colors": [
        { "Hour": 3,  "Color": "#1a1a1bc7" },
        { "Hour": 5,  "Color": "#ff5e4366" },
        { "Hour": 7,  "Color": "#ffffffe6" },
        { "Hour": 17, "Color": "#ffffffe6" },
        { "Hour": 19, "Color": "#ff5e4347" },
        { "Hour": 21, "Color": "#1a1a1bc7" }
      ],
      "Speeds": [
        { "Hour": 0, "Value": 0 }
      ]
    }
  ],
  "SkyTopColors": [
    { "Hour": 7,  "Color": "rgba(#2c6788, 1)" },
    { "Hour": 19, "Color": "rgba(#2c6788, 1)" },
    { "Hour": 5,  "Color": "rgba(#000000, 1)" },
    { "Hour": 21, "Color": "rgba(#030000, 1)" }
  ],
  "FogColors": [
    { "Hour": 7, "Color": "#14212e" }
  ],
  "SunColors": [
    { "Hour": 7,  "Color": "#ffffff"  },
    { "Hour": 17, "Color": "#ffffff"  },
    { "Hour": 18, "Color": "#fff7e3"  },
    { "Hour": 19, "Color": "#fec9ae"  },
    { "Hour": 5,  "Color": "#fec9ae"  }
  ],
  "MoonColors": [
    { "Hour": 3,  "Color": "#98aff2ff" },
    { "Hour": 5,  "Color": "#e5c0bcff" },
    { "Hour": 17, "Color": "#e5c0bcff" },
    { "Hour": 19, "Color": "#2241a16e" },
    { "Hour": 21, "Color": "#6e7aaac4" }
  ],
  "FogDistance": [-192, 128]
}
```

**Clima void com partículas ambientais** (`Assets/Server/Weathers/Void.json`, condensado):

```json
{
  "FogDistance": [-128.0, 512.0],
  "FogOptions": {
    "FogHeightCameraFixed": 0.5,
    "EffectiveViewDistanceMultiplier": 1.0
  },
  "Particle": {
    "SystemId": "Magic_Sparks_Heavy_GS",
    "OvergroundOnly": true,
    "Color": "#fd69a4"
  }
}
```

## Páginas Relacionadas

- [Ambientes](/hytale-modding-docs/reference/world-and-environment/environments) — cronogramas horários de previsão de clima que referenciam IDs de clima
- [Fazendas e Galinheiros](/hytale-modding-docs/reference/economy-and-progression/farming-coops) — IDs de clima usados nas condições do modificador Water
