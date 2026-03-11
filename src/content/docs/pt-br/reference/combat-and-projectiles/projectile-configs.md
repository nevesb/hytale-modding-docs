---
title: Configuracoes de Projeteis
description: Referencia para arquivos de configuracao de projeteis no Hytale, definindo fisica de lancamento, deslocamentos de spawn e cadeias de interacao para projeteis disparados por armas.
---

## Visao Geral

Os arquivos de configuracao de projeteis definem como uma arma lanca um projetil: o modelo usado, parametros de fisica, posicao de spawn e o que acontece quando o projetil acerta, erra ou quica. Eles atuam como a ponte entre a acao de ataque de uma arma e a entidade de projetil em tempo de execucao. As configuracoes suportam heranca via campo `Parent`, permitindo que configuracoes base compartilhadas sejam substituidas por arma.

## Localizacao dos Arquivos

```
Assets/Server/ProjectileConfigs/
  Weapons/
    Arrows/
    Bows/
    Crossbow/
    Shortbow/
    Staff/
    Throwables/
    ...
  NPCs/
  _Debug/
```

## Schema

| Campo | Tipo | Obrigatorio | Padrao | Descricao |
|-------|------|-------------|--------|-----------|
| `Parent` | `string` | Nao | — | ID de outra configuracao de projetil para herdar campos. Campos do filho sobrescrevem os do pai. |
| `Model` | `string` | Nao | — | ID do modelo visual usado para o projetil (ex: `"Arrow_Crude"`, `"Ice_Ball"`). |
| `Physics` | `PhysicsConfig` | Nao | — | Parametros de simulacao fisica. Veja abaixo. |
| `LaunchForce` | `number` | Nao | — | Forca escalar aplicada no lancamento, escalada pelo nivel de carga quando aplicavel. |
| `LaunchLocalSoundEventId` | `string` | Nao | — | Evento sonoro reproduzido localmente para o atirador no lancamento. |
| `LaunchWorldSoundEventId` | `string` | Nao | — | Evento sonoro reproduzido no mundo (audivel para jogadores proximos) no lancamento. |
| `SpawnOffset` | `Vector3` | Nao | — | Deslocamento em espaco local (X/Y/Z) a partir da origem da arma onde o projetil surge. |
| `SpawnRotationOffset` | `RotationOffset` | Nao | — | Rotacao adicional aplicada ao projetil no spawn. |
| `Interactions` | `InteractionMap` | Nao | — | Eventos de interacao nomeados e suas listas de acoes encadeadas. Veja abaixo. |

### PhysicsConfig

| Campo | Tipo | Obrigatorio | Padrao | Descricao |
|-------|------|-------------|--------|-----------|
| `Type` | `"Standard"` | Nao | `"Standard"` | Modelo de simulacao fisica. Atualmente apenas `"Standard"` e usado. |
| `Gravity` | `number` | Nao | — | Aceleracao gravitacional aplicada por segundo. |
| `TerminalVelocityAir` | `number` | Nao | — | Velocidade maxima no ar. |
| `TerminalVelocityWater` | `number` | Nao | — | Velocidade maxima na agua. |
| `RotationMode` | `"VelocityDamped" \| "Fixed"` | Nao | — | Controla como a orientacao do projetil acompanha seu vetor de velocidade. |
| `Bounciness` | `number` | Nao | `0` | Fracao de velocidade retida apos um quique em superficie. |
| `BounceCount` | `number` | Nao | — | Numero de vezes que o projetil pode quicar antes de parar. |
| `BounceLimit` | `number` | Nao | — | Numero maximo de quiques permitidos. |
| `AllowRolling` | `boolean` | Nao | `false` | Se o projetil pode rolar em superficies apos quicar. |
| `SticksVertically` | `boolean` | Nao | `false` | Se o projetil se crava verticalmente em superficies no impacto. |

### Vector3

| Campo | Tipo | Obrigatorio | Padrao | Descricao |
|-------|------|-------------|--------|-----------|
| `X` | `number` | Sim | — | Deslocamento lateral. |
| `Y` | `number` | Sim | — | Deslocamento vertical. |
| `Z` | `number` | Sim | — | Deslocamento frontal. |

### RotationOffset

| Campo | Tipo | Obrigatorio | Padrao | Descricao |
|-------|------|-------------|--------|-----------|
| `Pitch` | `number` | Nao | `0` | Deslocamento de pitch em graus. |
| `Yaw` | `number` | Nao | `0` | Deslocamento de yaw em graus. |
| `Roll` | `number` | Nao | `0` | Deslocamento de roll em graus. |

### InteractionMap

O objeto `Interactions` mapeia nomes de eventos para objetos `InteractionHandler`. Chaves de evento suportadas:

| Chave | Quando dispara |
|-------|----------------|
| `ProjectileSpawn` | Imediatamente quando o projetil e criado. |
| `ProjectileHit` | Quando o projetil acerta uma entidade. |
| `ProjectileMiss` | Quando o projetil acerta o terreno ou expira. |
| `ProjectileBounce` | Quando o projetil quica em uma superficie. |

### InteractionHandler

| Campo | Tipo | Obrigatorio | Padrao | Descricao |
|-------|------|-------------|--------|-----------|
| `Cooldown` | `object` | Nao | — | Cooldown opcional controlando este handler. |
| `Interactions` | `string[] \| object[]` | Sim | — | Lista ordenada de IDs de interacao nomeados ou definicoes de interacao inline para executar. |

## Exemplos

**Configuracao base de flecha** (`Assets/Server/ProjectileConfigs/Weapons/Arrows/Projectile_Config_Arrow_Base.json`):

```json
{
  "Model": "Arrow_Crude",
  "SpawnRotationOffset": {
    "Pitch": 2,
    "Yaw": 0.25,
    "Roll": 0
  },
  "Physics": {
    "Type": "Standard",
    "Gravity": 15,
    "TerminalVelocityAir": 50,
    "TerminalVelocityWater": 15,
    "RotationMode": "VelocityDamped",
    "Bounciness": 0.0,
    "SticksVertically": true
  },
  "LaunchForce": 30,
  "SpawnOffset": {
    "X": 0.15,
    "Y": -0.25,
    "Z": 0
  }
}
```

**Flecha de arco de duas maos** (`Projectile_Config_Arrow_Two_Handed_Bow.json`) — herda da base e adiciona interacoes:

```json
{
  "Parent": "Projectile_Config_Arrow_Base",
  "LaunchLocalSoundEventId": "SFX_Bow_T2_Shoot",
  "LaunchWorldSoundEventId": "SFX_Bow_T2_Shoot",
  "LaunchForce": 5,
  "Interactions": {
    "ProjectileHit": {
      "Interactions": [
        "Bow_Two_Handed_Projectile_Damage",
        "Bow_Two_Handed_Projectile_Damage_End"
      ]
    },
    "ProjectileMiss": {
      "Interactions": [
        "Bow_Two_Handed_Projectile_Miss",
        "Bow_Two_Handed_Projectile_Miss_End"
      ]
    }
  }
}
```

**Configuracao de bola de gelo do cajado** (`Assets/Server/ProjectileConfigs/Weapons/Staff/Ice/Projectile_Config_Ice_Ball.json`):

```json
{
  "Model": "Ice_Ball",
  "LaunchForce": 30,
  "Physics": {
    "Type": "Standard",
    "Gravity": 4.4,
    "TerminalVelocityAir": 42.5,
    "TerminalVelocityWater": 15,
    "RotationMode": "VelocityDamped",
    "Bounciness": 0.0,
    "SticksVertically": true
  },
  "LaunchWorldSoundEventId": "SFX_Staff_Ice_Shoot",
  "Interactions": {
    "ProjectileHit": {
      "Interactions": [
        {
          "Parent": "DamageEntityParent",
          "DamageCalculator": {
            "Class": "Charged",
            "BaseDamage": { "Ice": 20 }
          },
          "DamageEffects": {
            "Knockback": {
              "Type": "Force",
              "Force": 20,
              "VelocityType": "Set"
            },
            "WorldParticles": [
              { "SystemId": "Impact_Ice" },
              { "SystemId": "IceBall_Explosion" }
            ],
            "WorldSoundEventId": "SFX_Ice_Ball_Death"
          }
        },
        { "Type": "RemoveEntity", "Entity": "User" }
      ]
    },
    "ProjectileMiss": {
      "Interactions": [
        {
          "Type": "Simple",
          "Effects": {
            "WorldSoundEventId": "SFX_Ice_Ball_Death",
            "WorldParticles": [
              { "SystemId": "IceBall_Explosion" }
            ]
          }
        },
        { "Type": "RemoveEntity", "Entity": "User" }
      ]
    }
  }
}
```

## Paginas Relacionadas

- [Projeteis](/pt-br/hytale-modding-docs/reference/combat-and-projectiles/projectiles) — fisica de projeteis e valores de dano
- [Tipos de Dano](/pt-br/hytale-modding-docs/reference/combat-and-projectiles/damage-types) — hierarquia de tipos de dano usada em `BaseDamage`
