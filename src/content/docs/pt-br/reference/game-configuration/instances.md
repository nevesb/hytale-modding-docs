---
title: Instâncias
description: Referência para arquivos de configuração de instâncias no Hytale, que definem instâncias de mundo autocontidas com pontos de spawn, geração de mundo, modos de jogo, comportamento de NPCs, armazenamento de chunks e UI de descoberta.
---

## Visão Geral

Arquivos de configuração de instâncias definem mundos autocontidos nos quais os jogadores podem entrar — as zonas do overworld, instâncias de dungeon, hubs criativos e destinos de portais. Cada instância possui um `config.json` que especifica a seed do mundo, ponto de spawn, tipo de geração de mundo, modo de jogo e uma ampla gama de configurações de jogabilidade (PvP, dano de queda, spawn de NPCs, tick de blocos, etc.). Instâncias também configuram seu backend de armazenamento de chunks, configurações de plugins e uma UI de descoberta opcional que exibe um cartão de título quando jogadores entram.

Diretórios de instância também contêm uma pasta `resources/` com arquivos de estado em tempo de execução (ex: `InstanceData.json`, `Time.json`) que rastreiam o estado persistente do mundo.

## Localização dos Arquivos

```
Assets/Server/Instances/
  Basic/
  Challenge_Combat_1/
  CreativeHub/
    config.json
    resources/
  Default/
  Default_Flat/
  Default_Void/
  Dungeon_1/
  Dungeon_Goblin/
  Dungeon_Outlander/
  Forgotten_Temple/
    config.json
    resources/
  Movement_Gym/
    config.json
    resources/
  NPC_Faction_Gym/
  NPC_Gym/
  Persistent/
  Portals_Hedera/
  Portals_Henges/
  Portals_Jungles/
  Portals_Oasis/
  Portals_Taiga/
  ShortLived/
  TimeOut/
  Zone1_Plains1/
  Zone2_Desert1/
  Zone3_Taiga1/
  Zone4_Volcanic1/
```

## Schema

### config.json

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `Version` | `number` | Sim | — | Versão do formato de configuração (atualmente `4`). |
| `UUID` | `object` | Sim | — | UUID binário que identifica esta instância. Contém campos `$binary` e `$type`. |
| `DisplayName` | `string` | Não | — | Nome legível para a instância (ex: `"the Crossroads"`). |
| `Seed` | `number` | Sim | — | Seed de geração de mundo. |
| `SpawnProvider` | `SpawnProvider` | Sim | — | Configuração do ponto de spawn. |
| `WorldGen` | `WorldGen` | Sim | — | Configurações de geração de mundo. |
| `WorldMap` | `WorldMap` | Não | — | Configuração de exibição do mapa do mundo. |
| `ChunkStorage` | `ChunkStorage` | Sim | — | Backend para persistência de dados de chunks. |
| `ChunkConfig` | `object` | Não | `{}` | Substituições de configuração adicionais a nível de chunk. |
| `IsTicking` | `boolean` | Não | `false` | Se atualizações de tick de entidades são executadas nesta instância. |
| `IsBlockTicking` | `boolean` | Não | `false` | Se atualizações de tick de blocos são executadas (ex: crescimento de cultivos, propagação de fogo). |
| `IsPvpEnabled` | `boolean` | Não | `false` | Se dano jogador-contra-jogador está habilitado. |
| `IsFallDamageEnabled` | `boolean` | Não | `true` | Se dano de queda é aplicado. |
| `IsGameTimePaused` | `boolean` | Não | `false` | Se o relógio de dia/noite do jogo está congelado. |
| `GameTime` | `string` | Não | — | Hora inicial do jogo como um timestamp ISO 8601. |
| `ClientEffects` | `ClientEffects` | Não | — | Substituições visuais para renderização de sol, bloom e raios de sol. |
| `RequiredPlugins` | `object` | Não | `{}` | Mapa de IDs de plugins necessários para esta instância. |
| `GameMode` | `string` | Não | — | Modo de jogo: `"Creative"`, `"Adventure"`, `"Survival"`. |
| `IsSpawningNPC` | `boolean` | Não | `true` | Se NPCs surgem naturalmente nesta instância. |
| `IsSpawnMarkersEnabled` | `boolean` | Não | `true` | Se marcadores de spawn em prefabs estão ativos. |
| `IsAllNPCFrozen` | `boolean` | Não | `false` | Quando `true`, todos os NPCs ficam congelados e não se movem ou agem. |
| `GameplayConfig` | `string` | Não | `"Default"` | ID da configuração de jogabilidade a usar. Referencia um arquivo em `GameplayConfigs/`. |
| `IsCompassUpdating` | `boolean` | Não | `true` | Se a UI da bússola atualiza nesta instância. |
| `IsSavingPlayers` | `boolean` | Não | `true` | Se o estado do jogador é salvo quando ele sai. |
| `IsSavingChunks` | `boolean` | Não | `true` | Se chunks modificados são salvos no armazenamento. |
| `SaveNewChunks` | `boolean` | Não | `true` | Se chunks recém-gerados são salvos. |
| `IsUnloadingChunks` | `boolean` | Não | `true` | Se chunks são descarregados quando nenhum jogador está próximo. |
| `IsObjectiveMarkersEnabled` | `boolean` | Não | `true` | Se marcadores de objetivo são visíveis. |
| `DeleteOnUniverseStart` | `boolean` | Não | `false` | Se esta instância é deletada quando o universo reinicia. |
| `DeleteOnRemove` | `boolean` | Não | `false` | Se os dados da instância são deletados quando a instância é removida. |
| `ResourceStorage` | `ResourceStorage` | Não | — | Backend para persistência de dados de recursos. |
| `Plugin` | `PluginConfig` | Não | — | Configurações específicas de plugins, incluindo UI de descoberta da instância. |

### SpawnProvider

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `Id` | `string` | Sim | — | Tipo do provedor de spawn: `"Global"` para um spawn fixo no mundo. |
| `SpawnPoint` | `SpawnPoint` | Sim | — | Coordenadas do mundo e rotação para a posição de spawn. |

### SpawnPoint

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `X` | `number` | Sim | — | Coordenada X em blocos. |
| `Y` | `number` | Sim | — | Coordenada Y (vertical) em blocos. |
| `Z` | `number` | Sim | — | Coordenada Z em blocos. |
| `Pitch` | `number` | Não | `0` | Ângulo de pitch da câmera em graus. |
| `Yaw` | `number` | Não | `0` | Ângulo de yaw da câmera em graus. |
| `Roll` | `number` | Não | `0` | Ângulo de roll da câmera em graus. |

### WorldGen

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `Type` | `string` | Sim | — | Tipo do gerador: `"Hytale"` (legado), `"HytaleGenerator"` (grafo de nós). |
| `Name` | `string` | Não | — | Nome do perfil de geração de mundo (usado com o tipo `"Hytale"`). |
| `Environment` | `string` | Não | — | ID do ambiente para este mundo (usado com o tipo `"Hytale"`). |
| `WorldStructure` | `string` | Não | — | Nome da estrutura de mundo (usado com o tipo `"HytaleGenerator"`). |

### WorldMap

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `Type` | `string` | Sim | — | `"WorldGen"` (mostra mapa de bioma), `"Disabled"` (sem mapa). |

### ClientEffects

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `SunHeightPercent` | `number` | Não | — | Substituição da altura do sol como porcentagem. |
| `SunAngleDegrees` | `number` | Não | — | Substituição do ângulo do sol em graus. |
| `BloomIntensity` | `number` | Não | — | Intensidade do bloom de pós-processamento. |
| `BloomPower` | `number` | Não | — | Expoente de potência do bloom. |
| `SunIntensity` | `number` | Não | — | Multiplicador de intensidade da luz solar. |
| `SunshaftIntensity` | `number` | Não | — | Intensidade dos raios de luz. |
| `SunshaftScaleFactor` | `number` | Não | — | Fator de escala dos raios de luz. |

### Discovery (Plugin.Instance.Discovery)

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `TitleKey` | `string` | Sim | — | Chave de localização para o título exibido ao entrar. |
| `SubtitleKey` | `string` | Não | — | Chave de localização para o subtítulo. |
| `Display` | `boolean` | Não | `true` | Se o cartão de descoberta é exibido. |
| `AlwaysDisplay` | `boolean` | Não | `false` | Exibir o cartão toda vez, não apenas na primeira entrada. |
| `Icon` | `string` | Não | — | Nome do arquivo de ícone para o cartão de descoberta. |
| `Major` | `boolean` | Não | `false` | Se esta é uma descoberta importante (tratamento de UI maior). |
| `Duration` | `number` | Não | — | Segundos que o cartão de descoberta é exibido. |
| `FadeInDuration` | `number` | Não | — | Segundos para a transição de fade-in do cartão. |
| `FadeOutDuration` | `number` | Não | — | Segundos para a transição de fade-out do cartão. |

### Configuração de Plugin de Instância

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `RemovalConditions` | `array` | Não | `[]` | Condições sob as quais esta instância é automaticamente removida. |
| `PreventReconnection` | `boolean` | Não | `false` | Quando `true`, jogadores não podem reconectar a esta instância após desconectar. |
| `Discovery` | `Discovery` | Não | — | Configuração da UI de descoberta. |

## Exemplos

**Hub Criativo** (`Assets/Server/Instances/CreativeHub/config.json`, resumido):

```json
{
  "Version": 4,
  "DisplayName": "the Crossroads",
  "Seed": 1618917989368,
  "SpawnProvider": {
    "Id": "Global",
    "SpawnPoint": { "X": 5103.5, "Y": 168.0, "Z": 4982.5, "Yaw": 90.0 }
  },
  "WorldGen": {
    "Type": "Hytale",
    "Name": "Instance_Creative_Hub",
    "Environment": "Env_Creative_Hub"
  },
  "WorldMap": { "Type": "Disabled" },
  "GameMode": "Creative",
  "IsSpawningNPC": false,
  "IsAllNPCFrozen": true,
  "IsGameTimePaused": true,
  "GameplayConfig": "CreativeHub",
  "IsSavingPlayers": false,
  "Plugin": {
    "Instance": {
      "PreventReconnection": true,
      "Discovery": {
        "TitleKey": "server.instances.creative_hub.title",
        "SubtitleKey": "server.instances.creative_hub.subtitle",
        "Display": true,
        "Icon": "Forgotten_Temple.png",
        "Major": true,
        "Duration": 4.0,
        "FadeInDuration": 1.5,
        "FadeOutDuration": 1.5
      }
    }
  }
}
```

**Movement Gym com substituições visuais** (`Assets/Server/Instances/Movement_Gym/config.json`, resumido):

```json
{
  "Version": 4,
  "WorldGen": {
    "Type": "HytaleGenerator",
    "WorldStructure": "Default_Flat"
  },
  "WorldMap": { "Type": "WorldGen" },
  "ClientEffects": {
    "SunHeightPercent": 100.0,
    "BloomIntensity": 0.3,
    "BloomPower": 8.0,
    "SunIntensity": 0.25,
    "SunshaftIntensity": 0.3,
    "SunshaftScaleFactor": 4.0
  },
  "GameMode": "Creative",
  "IsGameTimePaused": true,
  "IsObjectiveMarkersEnabled": true
}
```

## Páginas Relacionadas

- [Configurações de Jogabilidade](/hytale-modding-docs/reference/game-configuration/gameplay-configs) — regras de jogabilidade aplicadas dentro de instâncias
- [Tipos de Portal](/hytale-modding-docs/reference/world-and-environment/portal-types) — definições de portais que conectam a IDs de instância
- [Geração de Mundo](/hytale-modding-docs/reference/world-and-environment/world-generation) — pipeline do gerador selecionado por `WorldGen.Type`
- [Ambientes](/hytale-modding-docs/reference/world-and-environment/environments) — arquivos de ambiente referenciados por `WorldGen.Environment`
