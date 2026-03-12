---
title: Modificar Geração de Mundo
description: Como modificar a geração de mundo usando configurações do HytaleGenerator, incluindo pesos de bioma, atribuições de ambiente, distribuição de minérios e posicionamento de estruturas.
---

## Objetivo

Modificar a geração procedural de mundo do Hytale para criar uma região de bioma personalizada com configurações de ambiente únicas, distribuição de minérios ajustada, regras de posicionamento de estruturas personalizadas e substituições de spawn de NPCs. Ao final, você entenderá como os arquivos de configuração do HytaleGenerator controlam a forma do terreno, seleção de bioma e posicionamento de recursos.

## Pré-requisitos

- Uma pasta de mod com um `manifest.json` válido (veja [Configure Seu Ambiente de Desenvolvimento](/hytale-modding-docs/tutorials/beginner/setup-dev-environment))
- Familiaridade com herança de templates JSON (veja [Herança e Templates](/hytale-modding-docs/reference/concepts/inheritance-and-templates))
- Entendimento de arquivos de ambiente (veja [Ambientes](/hytale-modding-docs/reference/world-and-environment/environments))
- Entendimento de regras de spawn de NPC (veja [Regras de Spawn de NPC](/hytale-modding-docs/reference/npc-system/npc-spawn-rules))

---

## Como a Geração de Mundo Funciona

O gerador de mundo do Hytale usa um sistema de configuração em camadas armazenado em `Assets/Server/HytaleGenerator/`. O gerador processa o terreno em estágios:

1. **Seleção de zona** — o mundo é dividido em zonas (Zona 1 até Zona 4) baseado na distância do spawn
2. **Atribuição de bioma** — cada chunk dentro de uma zona recebe um bioma baseado em seleção por peso
3. **Modelagem do terreno** — funções de ruído geram elevação, cavernas e recursos de superfície
4. **Posicionamento de blocos** — blocos de superfície, camadas subsuperficiais e veios de minério são posicionados
5. **Geração de estruturas** — estruturas prefab (vilas, ruínas, dungeons) são posicionadas de acordo com regras
6. **Atribuição de ambiente** — cada bioma recebe um arquivo de ambiente que controla o clima
7. **Spawn de NPCs** — regras de spawn vinculadas a ambientes povoam o mundo com NPCs

### Estrutura de Arquivos do Gerador

```
Assets/Server/HytaleGenerator/
  WorldGenerator.json          (configuração de nível superior: limites de zona, configurações de seed)
  Zones/
    Zone1/
      Zone1_Config.json        (lista de biomas, regras de estrutura para Zona 1)
      Biomes/
        Forest.json            (forma do terreno, paleta de blocos, distribuição de minérios)
        Mountains.json
        Plains.json
      Structures/
        Village.json           (regras de posicionamento de estruturas)
        Ruins.json
    Zone2/
      ...
  OreDistribution/
    Default.json               (configurações globais de veios de minério)
  StructureRules/
    Placement.json             (restrições de espaçamento e densidade)
```

---

## Passo 1: Entender a Configuração de Zona

Configurações de zona definem os biomas disponíveis em uma zona e seus pesos relativos. O gerador escolhe um bioma para cada chunk baseado nesses pesos.

Aqui está a estrutura de uma configuração de zona:

```json
{
  "Biomes": [
    {
      "Id": "Forest",
      "Weight": 40,
      "Environment": "Env_Zone1_Forests",
      "MinDistanceFromSpawn": 0,
      "MaxDistanceFromSpawn": -1
    },
    {
      "Id": "Mountains",
      "Weight": 20,
      "Environment": "Env_Zone1_Mountains",
      "MinDistanceFromSpawn": 100,
      "MaxDistanceFromSpawn": -1
    },
    {
      "Id": "Plains",
      "Weight": 30,
      "Environment": "Env_Zone1",
      "MinDistanceFromSpawn": 0,
      "MaxDistanceFromSpawn": -1
    }
  ],
  "Structures": [
    {
      "Id": "Village_Small",
      "Weight": 5,
      "BiomeFilter": ["Forest", "Plains"],
      "MinSpacing": 500,
      "MaxPerZone": 10
    }
  ]
}
```

### Campos da entrada de bioma

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `Id` | string | Identificador único do bioma, referencia um arquivo de definição de bioma |
| `Weight` | number | Probabilidade relativa deste bioma ser selecionado. Maior = mais comum |
| `Environment` | string | ID do arquivo de ambiente que controla o clima neste bioma |
| `MinDistanceFromSpawn` | number | Distância mínima em blocos do spawn do mundo antes que este bioma possa aparecer. `0` = sem mínimo |
| `MaxDistanceFromSpawn` | number | Distância máxima. `-1` = sem limite |

### Campos da entrada de estrutura

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `Id` | string | Identificador do prefab da estrutura |
| `Weight` | number | Frequência relativa de posicionamento |
| `BiomeFilter` | string[] | Em quais biomas esta estrutura pode aparecer |
| `MinSpacing` | number | Distância mínima em blocos entre instâncias desta estrutura |
| `MaxPerZone` | number | Número máximo desta estrutura em toda a zona |

---

## Passo 2: Criar um Bioma Personalizado

Defina um novo bioma com terreno e propriedades de blocos únicos. Arquivos de bioma controlam os parâmetros de ruído que moldam o terreno, a paleta de blocos de superfície e os veios de minério gerados no subterrâneo.

Crie `YourMod/Assets/Server/HytaleGenerator/Zones/Zone1/Biomes/CrystalGrove.json`:

```json
{
  "Id": "CrystalGrove",
  "TerrainShape": {
    "BaseHeight": 72,
    "HeightVariation": 18,
    "NoiseScale": 0.02,
    "NoiseOctaves": 4,
    "Roughness": 0.45
  },
  "SurfaceBlocks": {
    "TopBlock": "Block_Grass_Azure",
    "FillerBlock": "Block_Dirt",
    "FillerDepth": 4,
    "StoneBlock": "Block_Stone"
  },
  "Features": {
    "Trees": {
      "Density": 0.15,
      "Types": [
        { "Id": "Tree_Azure_Medium", "Weight": 60 },
        { "Id": "Tree_Azure_Large", "Weight": 25 },
        { "Id": "Tree_Azure_Small", "Weight": 15 }
      ]
    },
    "Vegetation": {
      "Density": 0.3,
      "Types": [
        { "Id": "Plant_Fern_Azure", "Weight": 40 },
        { "Id": "Plant_Flower_Crystal", "Weight": 30 },
        { "Id": "Plant_Mushroom_Glow", "Weight": 30 }
      ]
    }
  },
  "OreOverrides": [
    {
      "OreId": "Ore_Crystal",
      "VeinSize": [3, 8],
      "HeightRange": [20, 60],
      "Frequency": 12
    },
    {
      "OreId": "Ore_Copper",
      "VeinSize": [2, 6],
      "HeightRange": [10, 50],
      "Frequency": 8
    }
  ],
  "CaveSettings": {
    "Frequency": 0.6,
    "MinHeight": 5,
    "MaxHeight": 55,
    "CaveWidth": [3, 7]
  }
}
```

### Campos da forma do terreno

| Campo | Propósito |
|-------|-----------|
| `BaseHeight` | Elevação média do terreno em blocos. Florestas vanilla usam ~64-72 |
| `HeightVariation` | Desvio máximo da altura base. Maior = terreno mais montanhoso |
| `NoiseScale` | Controla a frequência dos recursos do terreno. Menor = recursos mais suaves e maiores |
| `NoiseOctaves` | Número de camadas de ruído combinadas. Mais oitavas = mais detalhes |
| `Roughness` | Multiplicador de rugosidade da superfície. 0 = perfeitamente liso, 1 = muito áspero |

### Campos de substituição de minério

| Campo | Propósito |
|-------|-----------|
| `OreId` | ID do bloco de minério a ser gerado |
| `VeinSize` | `[min, max]` número de blocos por veio de minério |
| `HeightRange` | `[min, max]` intervalo de nível Y onde veios podem surgir |
| `Frequency` | Número de tentativas de veio por chunk. Maior = mais minério |

---

## Passo 3: Criar o Ambiente do Bioma

Crie um arquivo de ambiente para o Crystal Grove com uma atmosfera mística que apresenta neblina frequente e clima ocasional com tons azulados.

Crie `YourMod/Assets/Server/Environments/Zone1/Env_Zone1_CrystalGrove.json`:

```json
{
  "WaterTint": "#2a7bc4",
  "SpawnDensity": 0.6,
  "Tags": {
    "Zone1": [],
    "CrystalGrove": []
  },
  "WeatherForecasts": {
    "0":  [
      { "WeatherId": "Zone1_Sunny",       "Weight": 30 },
      { "WeatherId": "Zone1_Foggy_Light", "Weight": 40 },
      { "WeatherId": "Zone1_Cloudy_Medium", "Weight": 30 }
    ],
    "4":  [
      { "WeatherId": "Zone1_Foggy_Light", "Weight": 60 },
      { "WeatherId": "Zone1_Sunny",       "Weight": 30 },
      { "WeatherId": "Zone1_Rain_Light",  "Weight": 10 }
    ],
    "8":  [
      { "WeatherId": "Zone1_Sunny",       "Weight": 50 },
      { "WeatherId": "Zone1_Foggy_Light", "Weight": 30 },
      { "WeatherId": "Zone1_Rain_Light",  "Weight": 20 }
    ],
    "12": [
      { "WeatherId": "Zone1_Sunny",         "Weight": 60 },
      { "WeatherId": "Zone1_Cloudy_Medium",  "Weight": 30 },
      { "WeatherId": "Zone1_Rain_Light",    "Weight": 10 }
    ],
    "16": [
      { "WeatherId": "Zone1_Sunny",       "Weight": 40 },
      { "WeatherId": "Zone1_Foggy_Light", "Weight": 40 },
      { "WeatherId": "Zone1_Rain_Light",  "Weight": 20 }
    ],
    "18": [
      { "WeatherId": "Zone1_Sunny_Fireflies", "Weight": 50 },
      { "WeatherId": "Zone1_Foggy_Light",     "Weight": 40 },
      { "WeatherId": "Zone1_Sunny",           "Weight": 10 }
    ],
    "20": [
      { "WeatherId": "Zone1_Sunny_Fireflies", "Weight": 60 },
      { "WeatherId": "Zone1_Foggy_Light",     "Weight": 30 },
      { "WeatherId": "Zone1_Sunny",           "Weight": 10 }
    ],
    "22": [
      { "WeatherId": "Zone1_Foggy_Light",   "Weight": 50 },
      { "WeatherId": "Zone1_Sunny",         "Weight": 30 },
      { "WeatherId": "Zone1_Cloudy_Medium", "Weight": 20 }
    ]
  }
}
```

Note o peso forte de neblina — isso cria uma atmosfera mística onde neblina aparece cerca de 40-60% do tempo, especialmente ao amanhecer e ao anoitecer. O clima `Sunny_Fireflies` aparece apenas nas horas da noite (18-21), correspondendo ao padrão vanilla da Zona 1.

---

## Passo 4: Registrar o Bioma na Configuração de Zona

Para adicionar seu bioma à geração da Zona 1, crie uma configuração de zona de substituição que adiciona o Crystal Grove à lista de biomas.

Crie `YourMod/Assets/Server/HytaleGenerator/Zones/Zone1/Zone1_Config.json`:

```json
{
  "Biomes": [
    {
      "Id": "CrystalGrove",
      "Weight": 15,
      "Environment": "Env_Zone1_CrystalGrove",
      "MinDistanceFromSpawn": 200,
      "MaxDistanceFromSpawn": -1
    }
  ],
  "Structures": [
    {
      "Id": "Ruins_CrystalShrine",
      "Weight": 3,
      "BiomeFilter": ["CrystalGrove"],
      "MinSpacing": 800,
      "MaxPerZone": 3
    }
  ]
}
```

Um peso de 15 torna o Crystal Grove relativamente incomum (compare com Floresta em 40). Definir `MinDistanceFromSpawn: 200` impede que ele apareça logo no spawn do mundo, criando um senso de descoberta.

---

## Passo 5: Criar Spawns de NPC Específicos do Bioma

Adicione spawns de NPC únicos vinculados ao ambiente do Crystal Grove. Isso segue o mesmo padrão de regras de spawn usado no overworld mas referencia seu ambiente personalizado.

Crie `YourMod/Assets/Server/NPC/Spawn/World/Zone1/Spawns_Zone1_CrystalGrove.json`:

```json
{
  "Environments": [
    "Env_Zone1_CrystalGrove"
  ],
  "NPCs": [
    {
      "Weight": 5,
      "SpawnBlockSet": "Soil",
      "Id": "Gecko",
      "Flock": "One_Or_Two"
    },
    {
      "Weight": 3,
      "SpawnBlockSet": "Soil",
      "Id": "Frog_Green",
      "Flock": "Group_Small"
    }
  ],
  "DayTimeRange": [6, 18]
}
```

Adicione um arquivo de spawn noturno separado para criaturas noturnas:

Crie `YourMod/Assets/Server/NPC/Spawn/World/Zone1/Spawns_Zone1_CrystalGrove_Night.json`:

```json
{
  "Environments": [
    "Env_Zone1_CrystalGrove"
  ],
  "NPCs": [
    {
      "Weight": 4,
      "SpawnBlockSet": "Soil",
      "Id": "Bat",
      "Flock": "Group_Small"
    }
  ],
  "DayTimeRange": [20, 6]
}
```

---

## Passo 6: Definir Regras de Posicionamento de Estruturas

Estruturas são construções ou ruínas prefab posicionadas durante a geração de mundo. Defina uma estrutura Crystal Shrine que só aparece no seu bioma.

Crie `YourMod/Assets/Server/HytaleGenerator/StructureRules/Ruins_CrystalShrine.json`:

```json
{
  "Id": "Ruins_CrystalShrine",
  "PrefabId": "Prefab_CrystalShrine",
  "Placement": {
    "SurfaceSnap": true,
    "MinTerrainFlatness": 0.7,
    "ClearAbove": 10,
    "RotationMode": "Random90"
  },
  "LootContainers": [
    {
      "ContainerId": "Chest_CrystalShrine",
      "DropTable": "SunkenVault_Chest",
      "MaxPerStructure": 2
    }
  ],
  "NPCSpawners": [
    {
      "RoleId": "SunkenVault_Guardian",
      "Count": [1, 3],
      "SpawnRadius": 8
    }
  ]
}
```

### Campos de posicionamento

| Campo | Propósito |
|-------|-----------|
| `SurfaceSnap` | Alinha a estrutura à altura da superfície do terreno |
| `MinTerrainFlatness` | Pontuação mínima de planura (0-1) necessária no local de posicionamento. Maior = terreno mais plano necessário |
| `ClearAbove` | Mínimo de blocos de espaço livre acima da área da estrutura |
| `RotationMode` | Como a estrutura é rotacionada: `Random90` escolhe 0/90/180/270 graus aleatoriamente |

---

## Passo 7: Testar Sua Geração de Mundo

1. Coloque sua pasta de mod no diretório de mods do servidor.
2. Inicie o servidor com uma **nova seed de mundo** — mundos existentes não regenerarão chunks que já foram carregados.
3. Viaje pelo menos 200 blocos do spawn (sua configuração `MinDistanceFromSpawn`).
4. Procure o bioma Crystal Grove — grama azulada e vegetação cristalina.
5. Verifique se os spawns de NPC correspondem às suas regras de spawn (geckos e sapos durante o dia, morcegos à noite).
6. Procure estruturas Crystal Shrine dentro do bioma.

### Solução de Problemas

| Problema | Causa | Correção |
|----------|-------|----------|
| Bioma nunca aparece | Peso muito baixo ou requisito de distância muito alto | Aumente `Weight` para 25+ para testes, ou reduza `MinDistanceFromSpawn` para 0 |
| Clima errado no bioma | ID de ambiente incompatível | Verifique se o campo `Environment` da configuração de zona corresponde ao nome de arquivo do seu ambiente |
| Sem minérios personalizados no subterrâneo | Substituição de minério não aplicada | Confirme que `OreOverrides` usa IDs de blocos válidos que existem no registro de blocos |
| Estrutura flutuando acima do terreno | `SurfaceSnap` não definido | Defina `"SurfaceSnap": true` nas regras de posicionamento |
| Estrutura surgindo na água | Sem verificação de água | Adicione `"AvoidWater": true` às regras de posicionamento |
| Mundo existente inalterado | Chunks já gerados | Crie um novo mundo — o gerador só executa para chunks não visitados |

---

## Listagem Completa de Arquivos

```
YourMod/
  Assets/
    Server/
      HytaleGenerator/
        Zones/
          Zone1/
            Zone1_Config.json
            Biomes/
              CrystalGrove.json
        StructureRules/
          Ruins_CrystalShrine.json
      Environments/
        Zone1/
          Env_Zone1_CrystalGrove.json
      NPC/
        Spawn/
          World/
            Zone1/
              Spawns_Zone1_CrystalGrove.json
              Spawns_Zone1_CrystalGrove_Night.json
```

---

## Próximos Passos

- [Dungeons Personalizadas](/hytale-modding-docs/tutorials/advanced/custom-dungeons) — posicione portais de dungeon dentro de estruturas geradas
- [Árvores de Comportamento de IA de NPCs](/hytale-modding-docs/tutorials/advanced/npc-ai-behavior-trees) — crie IA única para NPCs específicos do bioma
- [Ambientes](/hytale-modding-docs/reference/world-and-environment/environments) — referência completa de cronograma de clima
- [Regras de Spawn de NPC](/hytale-modding-docs/reference/npc-system/npc-spawn-rules) — detalhes do formato de regras de spawn
- [Sistema de Clima](/hytale-modding-docs/reference/world-and-environment/weather-system) — parâmetros de definição de clima
