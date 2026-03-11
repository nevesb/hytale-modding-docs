---
title: Máscaras de Mundo
description: Referência para definições de máscaras de mundo no Hytale, que controlam a forma do continente, gradientes de temperatura, zonas climáticas e mapeamento de bioma para cor na geração procedural de mundo.
---

## Visão Geral

Arquivos de máscara de mundo definem a estrutura em larga escala do mundo procedural. O `Mask.json` de nível superior conecta as sub-máscaras de forma de continente, temperatura, intensidade e clima, e declara zonas únicas (pontos de spawn, templos). Arquivos de sub-máscara usam geradores de ruído e atenuações baseadas em distância para produzir campos escalares que o gerador de mundo amostra para decidir qual bioma ocupa uma coordenada dada. Um arquivo companheiro `Zones.json` mapeia cores de máscara para listas de zonas nomeadas.

## Localização dos Arquivos

```
Assets/Server/World/
  Default/
    Mask.json
    World.json
    Zones.json
    Mask/
      Blend_Inner.json
      Blend_Outer.json
      Continent.json
      Intensity.json
      Temperature.json
      Climate/
        Cold.json
        Hot.json
        Temperate.json
        Island/
          Tier1.json
          Tier2.json
          Tier3.json
      Continent/
        Blend_Inner.json
        Blend_Outer.json
        Continent_Inner.json
        Continent_Outer.json
      Temperature/
        Temperature_Inner.json
        Temperature_Outer.json
  Flat/
  Void/
  Instance_Creative_Hub/
  Instance_Dungeon_Goblin/
  Instance_Forgotten_Temple/
```

## Schema

### Mask.json (nível superior)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Randomizer` | `Randomizer` | Não | — | Randomizador de ruído global aplicado a toda amostragem de máscara. |
| `Noise` | `NoiseConfig` | Sim | — | Referências às sub-máscaras de continente, temperatura e intensidade, mais limiares de terra/oceano. |
| `Climate` | `ClimateConfig` | Sim | — | Definições de zonas climáticas e parâmetros de mesclagem. |
| `UniqueZones` | `UniqueZone[]` | Não | `[]` | Zonas nomeadas posicionadas em locais específicos do mundo (ex: spawn, templos). |

### Randomizer

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Generators` | `Generator[]` | Sim | — | Array de geradores de ruído que contribuem para a aleatorização. |

### Generator

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Seed` | `string` | Não | — | String de semente determinística. |
| `NoiseType` | `string` | Sim | — | Algoritmo de ruído: `"SIMPLEX"`, `"OLD_SIMPLEX"`, `"POINT"`. |
| `Scale` | `number` | Sim | — | Escala espacial do ruído. |
| `Amplitude` | `number` | Não | `1` | Multiplicador de amplitude da saída. |
| `Octaves` | `number` | Não | `1` | Número de oitavas fractais. |
| `Persistence` | `number` | Não | `0.5` | Decaimento de amplitude por oitava. |
| `Lacunarity` | `number` | Não | `2.0` | Multiplicador de frequência por oitava. |

### NoiseConfig

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Thresholds` | `Thresholds` | Sim | — | Limiares escalares que separam terra, ilha, praia e oceano raso. |
| `Continent` | `FileRef` | Sim | — | Referência à sub-máscara de forma do continente. |
| `Temperature` | `FileRef` | Sim | — | Referência à sub-máscara de gradiente de temperatura. |
| `Intensity` | `FileRef` | Sim | — | Referência à sub-máscara de intensidade. |

### Thresholds

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Land` | `number` | Sim | — | Valor de ruído acima do qual o terreno é considerado terra. |
| `Island` | `number` | Sim | — | Valor de ruído acima do qual o terreno é considerado uma ilha. |
| `BeachSize` | `number` | Sim | — | Largura da faixa de transição de praia. |
| `ShallowOceanSize` | `number` | Sim | — | Largura da faixa de oceano raso ao redor da terra. |

### ClimateConfig

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `FadeMode` | `string` | Não | `"CHILDREN"` | Como as fronteiras climáticas desvanecem: `"CHILDREN"` usa configurações por filho. |
| `FadeRadius` | `number` | Não | — | Raio da zona de transição climática. |
| `FadeDistance` | `number` | Não | — | Distância sobre a qual o desvanecimento ocorre. |
| `Climates` | `FileRef[]` | Sim | — | Referências a arquivos individuais de definição de clima. |

### Climate Definition (ex: Cold.json)

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Name` | `string` | Sim | — | Nome de exibição para este clima (ex: `"Zone 3"`). |
| `Color` | `string` | Sim | — | Cor hexadecimal usada para representar este clima em mapas de debug. |
| `Points` | `ClimatePoint[]` | Sim | — | Coordenadas de temperatura/intensidade que definem onde este clima aparece. |
| `Children` | `ClimateTier[]` | Não | `[]` | Sub-níveis dentro deste clima com cores de bioma distintas e configs de ilha. |

### ClimateTier

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Name` | `string` | Sim | — | Nome de exibição do nível (ex: `"Tier 1"`). |
| `Color` | `string` | Sim | — | Cor hexadecimal para o bioma terrestre deste nível. |
| `Shore` | `string` | Não | — | Cor hexadecimal para áreas de costa neste nível. |
| `Ocean` | `string` | Não | — | Cor hexadecimal para oceano profundo neste nível. |
| `ShallowOcean` | `string` | Não | — | Cor hexadecimal para oceano raso neste nível. |
| `Island` | `FileRef` | Não | — | Referência a um arquivo de máscara de ilha para este nível. |
| `Points` | `ClimatePoint[]` | Sim | — | Coordenadas climáticas com `Modifier` opcional. |

### ClimatePoint

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Temperature` | `number` | Sim | — | Valor do eixo de temperatura (0–1). |
| `Intensity` | `number` | Sim | — | Valor do eixo de intensidade (0–1). |
| `Modifier` | `number` | Não | `1` | Modificador de mesclagem para transições de nível. |

### UniqueZone

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Name` | `string` | Sim | — | Identificador de zona referenciado pelo bioma e mapeamento de cores do Zones.json. |
| `Parent` | `string` | Não | — | Nome de uma zona única pai para posicionamento relativo. |
| `Color` | `string` | Sim | — | Cor hexadecimal para renderização em mapa de debug. |
| `Radius` | `number` | Sim | — | Raio da zona em chunks. |
| `OriginX` | `number` | Sim | — | Origem X para cálculos de distância. |
| `OriginY` | `number` | Sim | — | Origem Y para cálculos de distância. |
| `Distance` | `number` | Sim | — | Distância máxima da origem para busca de posicionamento. |
| `MinDistance` | `number` | Não | `0` | Distância mínima da origem (cria uma área de busca anular). |
| `Rule` | `PlacementRule` | Sim | — | Restrições sobre continente, temperatura, intensidade e valores de desvanecimento. |

### PlacementRule

Cada chave (`Continent`, `Temperature`, `Intensity`, `Fade`) contém:

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Target` | `number` | Sim | — | Valor ideal da máscara para posicionamento. |
| `Radius` | `number` | Sim | — | Desvio aceitável do alvo. |
| `Weight` | `number` | Sim | — | Importância desta restrição em relação às outras. |

### Tipos de Sub-máscara

Arquivos de sub-máscara usam um campo `Type` para definir seu comportamento:

| Type | Description | Key Fields |
|------|-------------|------------|
| `DISTORTED` | Máscara baseada em ponto com distorção de ruído | `Noise` (com `NoiseType`, `X`, `Y`, `InnerRadius`, `OuterRadius`), `Randomizer` |
| `BLEND` | Mescla duas máscaras filhas usando uma máscara alfa | `Alpha` (FileRef), `Noise` (FileRef[]), `Thresholds`, `Normalize` |

### Zones.json

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `GridGenerator` | `GridGenerator` | Sim | — | Controla a grade estilo Voronoi usada para atribuir zonas. |
| `MaskMapping` | `object` | Sim | — | Mapa de strings de cores hexadecimais para arrays de strings de nomes de zonas. |

### GridGenerator

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Scale` | `number` | Sim | — | Tamanho da célula da grade. |
| `Jitter` | `number` | Não | `0` | Deslocamento aleatório aplicado aos pontos da grade (0–1). |
| `Randomizer` | `Randomizer` | Não | — | Geradores de ruído para jitter da grade. |

### World.json

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Masks` | `string[]` | Sim | — | Array de referências de arquivos de máscara (ex: `["Mask.json"]`). |
| `PrefabStore` | `string` | Não | `"ASSETS"` | Fonte para dados de prefab: `"ASSETS"` ou `"DISK"`. |
| `Height` | `number` | Sim | — | Altura do mundo em regiões. |
| `Width` | `number` | Sim | — | Largura do mundo em regiões. |
| `OffsetX` | `number` | Não | `0` | Deslocamento horizontal da origem. |
| `OffsetY` | `number` | Não | `0` | Deslocamento vertical da origem. |
| `Randomizer` | `Randomizer` | Não | — | Randomizador adicional para ruído em nível de mundo. |

## Exemplos

**Máscara de nível superior** (`Assets/Server/World/Default/Mask.json`, condensado):

```json
{
  "Randomizer": {
    "Generators": [
      { "Seed": "RANDOMIZER", "NoiseType": "SIMPLEX", "Scale": 0.01, "Amplitude": 16.0 }
    ]
  },
  "Noise": {
    "Thresholds": {
      "Land": 0.5,
      "Island": 0.75,
      "BeachSize": 0.02,
      "ShallowOceanSize": 0.08
    },
    "Continent": { "File": "Mask.Continent" },
    "Temperature": { "File": "Mask.Temperature" },
    "Intensity": { "File": "Mask.Intensity" }
  },
  "Climate": {
    "FadeMode": "CHILDREN",
    "FadeRadius": 50.0,
    "FadeDistance": 100.0,
    "Climates": [
      { "File": "Mask.Climate.Temperate" },
      { "File": "Mask.Climate.Cold" },
      { "File": "Mask.Climate.Hot" }
    ]
  },
  "UniqueZones": [
    {
      "Name": "Zone1_Spawn",
      "Color": "#ff0000",
      "Radius": 35,
      "OriginX": 0,
      "OriginY": 0,
      "Distance": 3000,
      "Rule": {
        "Continent":   { "Target": 0.0, "Radius": 0.3, "Weight": 1.0 },
        "Temperature": { "Target": 0.5, "Radius": 0.2, "Weight": 1.0 },
        "Intensity":   { "Target": 0.1, "Radius": 0.3, "Weight": 1.0 },
        "Fade":        { "Target": 1.0, "Radius": 0.5, "Weight": 0.5 }
      }
    }
  ]
}
```

**Sub-máscara de mesclagem de continente** (`Assets/Server/World/Default/Mask/Blend_Inner.json`):

```json
{
  "Type": "DISTORTED",
  "Noise": {
    "NoiseType": "POINT",
    "X": 0.0,
    "Y": 0.0,
    "InnerRadius": 1700.0,
    "OuterRadius": 2500.0
  },
  "Randomizer": {
    "Generators": [
      {
        "Seed": "CONTINENT-INNER-WARP-1",
        "NoiseType": "SIMPLEX",
        "Scale": 0.00085,
        "Octaves": 1,
        "Persistence": 0.5,
        "Lacunarity": 2.5,
        "Amplitude": 450
      }
    ]
  }
}
```

## Páginas Relacionadas

- [Geração de Mundo](/hytale-modding-docs/reference/world-and-environment/world-generation) — o pipeline HytaleGenerator que consome essas máscaras
- [Ambientes](/hytale-modding-docs/reference/world-and-environment/environments) — arquivos de ambiente atribuídos a zonas definidas pelas máscaras
- [Instâncias](/hytale-modding-docs/reference/game-configuration/instances) — configs de instância que selecionam uma definição de mundo
