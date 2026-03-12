---
title: Configurações de Jogabilidade
description: Referência para arquivos de configuração de jogabilidade no Hytale, que controlam penalidades de morte, durabilidade de itens, duração do ciclo dia/noite, configurações do jogador, stamina, respawn e mais.
---

## Visão Geral

Arquivos de configuração de jogabilidade são os arquivos de ajuste de nível superior para um mundo ou instância. Eles suportam herança via campo `Parent` — configurações filhas substituem apenas os campos que declaram, herdando todo o resto da configuração pai. O `Default.json` é a base para todos os mundos padrão; `Default_Instance.json` o estende para conteúdo instanciado com regras diferentes de morte e edição de mundo.

## Localização dos Arquivos

```
Assets/Server/GameplayConfigs/
  Default.json
  Default_Instance.json
  CreativeHub.json
  ForgottenTemple.json
  Portal.json
```

## Schema

### Nível Superior

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `Parent` | `string` | Não | — | ID de uma configuração pai da qual herdar. Apenas campos substituídos precisam ser especificados na configuração filha. |
| `Gathering` | `GatheringConfig` | Não | — | Configurações para feedback de coleta de blocos (blocos inquebráveis, respostas de ferramenta incorreta). |
| `Death` | `DeathConfig` | Não | — | Controla o que acontece com itens e respawn na morte do jogador. |
| `ItemEntity` | `ItemEntityConfig` | Não | — | Configurações para entidades de itens dropados no mundo. |
| `ItemDurability` | `ItemDurabilityConfig` | Não | — | Multiplicadores de penalidade aplicados quando a durabilidade do equipamento chega a zero. |
| `Plugin` | `PluginConfig` | Não | — | Configuração para plugins de jogabilidade: Stamina, Memórias. |
| `Respawn` | `RespawnConfig` | Não | — | Regras de ponto de respawn. |
| `World` | `WorldConfig` | Não | — | Durações do ciclo dia/noite e configurações de interação com blocos. |
| `Player` | `PlayerConfig` | Não | — | Configurações de movimento, hitbox e visibilidade de armadura. |
| `CameraEffects` | `CameraEffectsConfig` | Não | — | Efeitos visuais disparados por tipos de dano. |
| `CreativePlaySoundSet` | `string` | Não | — | Conjunto de sons usado durante o modo criativo. |
| `Spawn` | `SpawnConfig` | Não | — | Efeitos de partículas exibidos no primeiro spawn do jogador. |
| `Ping` | `PingConfig` | Não | — | Configurações de ping do mundo (duração, cooldown, raio, som). |

### DeathConfig

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `ItemsLossMode` | `"Configured" \| "None" \| "All"` | Não | — | Determina quais itens são perdidos na morte. `Configured` usa campos de porcentagem; `None` mantém todos os itens; `All` dropa tudo. |
| `ItemsAmountLossPercentage` | `number` | Não | — | Porcentagem de pilhas de itens perdidas na morte quando `ItemsLossMode` é `"Configured"`. |
| `ItemsDurabilityLossPercentage` | `number` | Não | — | Porcentagem de durabilidade de equipamento perdida na morte. |
| `LoseItems` | `boolean` | Não | — | Substituição simplificada: `false` impede qualquer perda de itens independentemente de outras configurações. |
| `RespawnController` | `object` | Não | — | Comportamento personalizado de respawn. `{ "Type": "ExitInstance" }` ejeta o jogador de uma instância na morte. |

### ItemEntityConfig

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `Lifetime` | `number` | Não | — | Segundos antes de uma entidade de item dropado desaparecer do mundo. |

### ItemDurabilityConfig

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `BrokenPenalties` | `object` | Não | — | Multiplicadores aplicados aos atributos da entidade quando cada categoria de equipamento está totalmente quebrada. |
| `BrokenPenalties.Weapon` | `number` | Não | — | Multiplicador de atributos quando a arma equipada tem zero de durabilidade (ex: `0.75` = 25% de redução de atributos). |
| `BrokenPenalties.Armor` | `number` | Não | — | Multiplicador de atributos quando a armadura equipada está totalmente quebrada. |
| `BrokenPenalties.Tool` | `number` | Não | — | Multiplicador de atributos quando a ferramenta equipada está totalmente quebrada. |

### PluginConfig

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `Stamina` | `StaminaPlugin` | Não | — | Configurações do sistema de stamina. |
| `Memories` | `MemoriesPlugin` | Não | — | Configurações do sistema de memórias (XP). |
| `Weathers` | `object` | Não | — | Substituições do plugin de clima. |

### StaminaPlugin

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `SprintRegenDelay` | `object` | Não | — | Configura como a corrida atrasa a regeneração de stamina. |
| `SprintRegenDelay.EntityStatId` | `string` | Não | — | O ID do atributo de entidade a modificar (ex: `"StaminaRegenDelay"`). |
| `SprintRegenDelay.Value` | `number` | Não | — | Valor aplicado ao atributo (valores negativos reduzem o atraso de regeneração). |

### MemoriesPlugin

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `MemoriesAmountPerLevel` | `number[]` | Não | — | Array de custos de memória por nível, indexado por nível (base 0). |
| `MemoriesRecordParticles` | `string` | Não | — | Sistema de partículas reproduzido quando uma memória é registrada em uma estátua. |
| `MemoriesCatchItemId` | `string` | Não | — | ID do item da partícula de memória coletável no mundo. |
| `MemoriesCatchEntityParticle` | `object` | Não | — | Partícula anexada à entidade ao capturar uma memória. |
| `MemoriesCatchParticleViewDistance` | `number` | Não | — | Distância de visão em unidades na qual as partículas de captura são visíveis. |

### RespawnConfig

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `RadiusLimitRespawnPoint` | `number` | Não | — | Distância máxima em unidades do local de morte do jogador onde um ponto de respawn pode ser usado. |
| `MaxRespawnPointsPerPlayer` | `number` | Não | — | Número máximo de pontos de respawn ativos que um jogador pode ter simultaneamente. |

### WorldConfig

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `DaytimeDurationSeconds` | `number` | Não | — | Segundos reais para um período completo de dia. |
| `NighttimeDurationSeconds` | `number` | Não | — | Segundos reais para um período completo de noite. |
| `BlockPlacementFragilityTimer` | `number` | Não | — | Segundos após a colocação durante os quais um bloco pode ser instantaneamente quebrado pelo colocador. `0` desabilita. |
| `AllowBlockBreaking` | `boolean` | Não | — | Se jogadores podem quebrar blocos neste mundo. |
| `AllowBlockGathering` | `boolean` | Não | — | Se jogadores podem coletar recursos de blocos. |
| `Sleep` | `SleepConfig` | Não | — | Configuração do sistema de sono. |

### SleepConfig

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `WakeUpHour` | `number` | Não | — | Hora do jogo em que jogadores dormindo acordam. |
| `AllowedSleepHoursRange` | `[number, number]` | Não | — | Intervalo de horas `[início, fim]` durante o qual jogadores podem dormir. Funciona através da meia-noite. |

### PlayerConfig

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `MovementConfig` | `string` | Não | — | ID do preset de configuração de movimento para jogadores. |
| `HitboxCollisionConfig` | `string` | Não | — | ID do preset de colisão de hitbox (ex: `"SoftCollision"`). |
| `ArmorVisibilityOption` | `"All" \| "None" \| "Cosmetic"` | Não | — | Controla quais camadas de armadura são visíveis no modelo do jogador. |

### SpawnConfig

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `FirstSpawnParticles` | `ParticleEntry[]` | Não | — | Sistemas de partículas gerados na localização do jogador no primeiro spawn. |

### PingConfig

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `PingDuration` | `number` | Não | — | Segundos que um marcador de ping permanece visível. |
| `PingCooldown` | `number` | Não | — | Segundos entre pings permitidos para um jogador. |
| `PingBroadcastRadius` | `number` | Não | — | Raio em unidades dentro do qual outros jogadores veem o ping. |
| `PingSound` | `string` | Não | — | Evento de som reproduzido quando um ping é colocado. |

## Exemplos

**Configuração de mundo padrão** (`Assets/Server/GameplayConfigs/Default.json`):

```json
{
  "Death": {
    "ItemsLossMode": "Configured",
    "ItemsAmountLossPercentage": 50.0,
    "ItemsDurabilityLossPercentage": 10.0
  },
  "ItemEntity": {
    "Lifetime": 600.0
  },
  "ItemDurability": {
    "BrokenPenalties": {
      "Weapon": 0.75,
      "Armor": 0.75,
      "Tool": 0.75
    }
  },
  "Plugin": {
    "Stamina": {
      "SprintRegenDelay": {
        "EntityStatId": "StaminaRegenDelay",
        "Value": -0.75
      }
    },
    "Memories": {
      "MemoriesAmountPerLevel": [10, 25, 50, 100, 200],
      "MemoriesRecordParticles": "MemoryRecordedStatue",
      "MemoriesCatchItemId": "Memory_Particle",
      "MemoriesCatchParticleViewDistance": 64
    }
  },
  "Respawn": {
    "RadiusLimitRespawnPoint": 500,
    "MaxRespawnPointsPerPlayer": 3
  },
  "World": {
    "DaytimeDurationSeconds": 1728,
    "NighttimeDurationSeconds": 1152,
    "BlockPlacementFragilityTimer": 0,
    "Sleep": {
      "WakeUpHour": 4.79,
      "AllowedSleepHoursRange": [19.5, 4.79]
    }
  },
  "Player": {
    "MovementConfig": "Default",
    "HitboxCollisionConfig": "SoftCollision",
    "ArmorVisibilityOption": "All"
  },
  "Ping": {
    "PingDuration": 5.0,
    "PingCooldown": 1.0,
    "PingBroadcastRadius": 100.0,
    "PingSound": "SFX_Ping"
  }
}
```

**Configuração de instância** (`Assets/Server/GameplayConfigs/Default_Instance.json`) — herda de Default e substitui:

```json
{
  "Parent": "Default",
  "World": {
    "AllowBlockBreaking": false,
    "AllowBlockGathering": false
  },
  "Death": {
    "LoseItems": false,
    "RespawnController": {
      "Type": "ExitInstance"
    }
  }
}
```

## Páginas Relacionadas

- [Ambientes](/hytale-modding-docs/reference/world-and-environment/environments) — progressão de horas dia/noite controlada por `DaytimeDurationSeconds`
- [Tabelas de Drop](/hytale-modding-docs/reference/economy-and-progression/drop-tables) — itens dropados na morte sujeitos a `ItemsLossMode`
- [Sistema de Clima](/hytale-modding-docs/reference/world-and-environment/weather-system) — clima controlado por `Plugin.Weathers`
