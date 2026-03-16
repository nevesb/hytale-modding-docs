---
title: Crie um Sistema de Combate Personalizado
description: Construa uma luta de chefe com múltiplas fases, mecânicas de escudo, mudanças de aparência, invocação de lacaios, animações de ataque personalizadas e spawns no mundo.
---

import { Aside } from '@astrojs/starlight/components';

## O que Você Vai Aprender

Construa um encontro completo com o **Slime Chefe** incluindo:
- Um chefe com múltiplas fases que muda de aparência conforme perde HP
- Efeitos de entidade de escudo com resistência a dano
- Animações de ataque personalizadas usando `ItemPlayerAnimations`
- Movimentação de combate com strafing via `MaintainDistance`
- Invocação de lacaios durante transições de fase
- Configuração de world spawn para geração natural
- Drops de loot com um item troféu

<Aside type="tip">
O mod completo está disponível no GitHub: [hytale-mod-custom-combat-system](https://github.com/nevesb/hytale-mod-custom-combat-system)
</Aside>

## Pré-requisitos

- Um mod funcional com um NPC personalizado (veja [Criar um NPC](/hytale-modding-docs/tutorials/beginner/create-an-npc))
- Entendimento de spawning de NPCs (veja [Spawning Personalizado de NPCs](/hytale-modding-docs/tutorials/intermediate/custom-npc-spawning))
- Familiaridade com cadeias de interação (veja [Árvores de Comportamento de IA de NPCs](/hytale-modding-docs/tutorials/advanced/npc-ai-behavior-trees))

---

## Arquitetura do Sistema

O sistema de chefe conecta vários tipos de arquivo:

```
ModelAsset (BossSlime_Giant)     ─── define hitbox, animações de estado, aparência
    │
ItemPlayerAnimations             ─── mapeia IDs de animação de ataque para arquivos .blockyanim
    │
Interaction (Boss_Slime_Attack)  ─── dispara a animação de ataque + cadeia de dano
    │
NPC Role (Boss_Slime_Giant)      ─── define fases, movimentação, estados de combate
    │
Entity Effect (Shield_Crystal)   ─── escudo com resistência a dano + partículas
    │
World Spawn                      ─── geração natural nas florestas da Zona 1
```

---

## Passo 1: Criar o Model Asset do Chefe

O chefe precisa de uma definição de modelo que mapeie animações de estado (Idle, Walk, Death, etc.), mas **não** animações de ataque. Animações de ataque são tratadas separadamente via `ItemPlayerAnimations`.

Crie `Server/Models/Beast/BossSlime_Giant.json`:

```json
{
  "Model": "NPC/Beast/BossSlime/Model/Model_Giant.blockymodel",
  "Texture": "NPC/Beast/BossSlime/Model/Texture_Giant.png",
  "EyeHeight": 1.5,
  "CrouchOffset": -0.5,
  "HitBox": {
    "Max": { "X": 1.5, "Y": 1.5, "Z": 1.5 },
    "Min": { "X": -3.0, "Y": 0, "Z": -3.0 }
  },
  "AnimationSets": {
    "Walk": {
      "Animations": [
        { "Animation": "NPC/Beast/BossSlime/Animations/Default/Walk.blockyanim" }
      ]
    },
    "Idle": {
      "Animations": [
        { "Animation": "NPC/Beast/BossSlime/Animations/Default/Idle.blockyanim" }
      ]
    },
    "Death": {
      "Animations": [
        { "Animation": "NPC/Beast/BossSlime/Animations/Default/Death.blockyanim", "Loop": false }
      ]
    },
    "Run": {
      "Animations": [
        { "Animation": "NPC/Beast/BossSlime/Animations/Default/Run.blockyanim" }
      ]
    },
    "Walk_Backward": {
      "Animations": [
        { "Animation": "NPC/Beast/BossSlime/Animations/Default/Walk_Backward.blockyanim" }
      ]
    }
  }
}
```

<Aside type="caution">
**Não** adicione animações de ataque ao `AnimationSets`. Animações de ataque para NPCs devem ser definidas em um arquivo `ItemPlayerAnimations` separado (Passo 2). Misturá-las faz com que a animação não seja reproduzida.
</Aside>

Você também precisa dos model assets `BossSlime_Medium.json` e `BossSlime_Small.json` para as transições de fase (mesmas animações, modelos/texturas diferentes). O `BossSlime.json` base serve como a aparência padrão.

---

## Passo 2: Criar o Mapeamento de Animação de Ataque

As bestas vanilla (Bear, Cactee, etc.) usam arquivos `ItemPlayerAnimations` para mapear IDs de animação de combate para arquivos `.blockyanim`. Seu chefe precisa do mesmo.

Crie `Server/Item/Animations/NPC/Beast/BossSlime/BossSlime_Default.json`:

```json
{
  "Animations": {
    "Attack": {
      "ThirdPerson": "NPC/Beast/BossSlime/Animations/Default/Attack.blockyanim",
      "Looping": false,
      "Speed": 1
    }
  },
  "Camera": {
    "Pitch": {
      "AngleRange": { "Max": 15, "Min": -15 },
      "TargetNodes": ["Head"]
    },
    "Yaw": {
      "AngleRange": { "Max": 15, "Min": -15 },
      "TargetNodes": ["Head"]
    }
  },
  "WiggleWeights": {
    "Pitch": 2, "PitchDeceleration": 0.1,
    "Roll": 0.1, "RollDeceleration": 0.1,
    "X": 3, "XDeceleration": 0.1,
    "Y": 0.1, "YDeceleration": 0.1,
    "Z": 0.1, "ZDeceleration": 0.1
  }
}
```

### Como funciona

| Seção | Propósito |
|-------|-----------|
| `Animations.Attack` | Mapeia o ID `"Attack"` para o arquivo `.blockyanim` |
| `Camera` | Limites de rastreamento da cabeça durante combate |
| `WiggleWeights` | Balanço visual quando o NPC se move/ataca |

A chave `"Attack"` é o que você referencia no `ItemAnimationId` da interação. O nome do arquivo `BossSlime_Default` se torna o `ItemPlayerAnimationsId`.

---

## Passo 3: Criar a Interação de Ataque

O chefe usa a cadeia vanilla `Root_NPC_Attack_Melee`, mas sobrescreve a animação inicial para usar o ataque personalizado do slime.

Crie `Server/Item/Interactions/Boss_Slime_Attack_Start.json`:

```json
{
  "Type": "Simple",
  "Effects": {
    "ItemPlayerAnimationsId": "BossSlime_Default",
    "ItemAnimationId": "Attack",
    "ClearAnimationOnFinish": false,
    "ClearSoundEventOnFinish": false
  },
  "RunTime": 0.1,
  "Next": {
    "Type": "Replace",
    "DefaultValue": {
      "Interactions": ["NPC_Attack_Selector_Left"]
    },
    "Var": "Melee_Selector"
  }
}
```

Isso substitui o vanilla `NPC_Attack_Melee_Simple` (que usa a animação humanoide `SwingLeft`) por uma interação que reproduz a animação `Attack` do slime.

Crie a interação de dano em `Server/Item/Interactions/Boss_Slime_Slam_Damage.json`:

```json
{
  "Parent": "DamageEntityParent",
  "DamageCalculator": {
    "BaseDamage": { "Physical": 15 }
  },
  "DamageEffects": {
    "Knockback": { "Force": 3, "VelocityY": 4 },
    "WorldSoundEventId": "SFX_Unarmed_Impact",
    "LocalSoundEventId": "SFX_Unarmed_Impact"
  }
}
```

---

## Passo 4: Criar o Entity Effect de Escudo

O escudo fornece resistência temporária a dano e um efeito visual de partículas.

Crie `Server/Entity/Effects/Shield_Crystal.json`:

```json
{
  "Duration": 1,
  "DamageResistance": {
    "Physical": [{ "Amount": 1.0, "CalculationType": "Multiplicative" }],
    "Slashing": [{ "Amount": 1.0, "CalculationType": "Multiplicative" }],
    "Bludgeoning": [{ "Amount": 1.0, "CalculationType": "Multiplicative" }],
    "Projectile": [{ "Amount": 1.0, "CalculationType": "Multiplicative" }],
    "Fire": [{ "Amount": 1.0, "CalculationType": "Multiplicative" }],
    "Ice": [{ "Amount": 1.0, "CalculationType": "Multiplicative" }],
    "Poison": [{ "Amount": 1.0, "CalculationType": "Multiplicative" }],
    "Environment": [{ "Amount": 1.0, "CalculationType": "Multiplicative" }]
  },
  "ApplicationEffects": {
    "Particles": [{ "SystemId": "Example_Shield" }]
  },
  "Invulnerable": false
}
```

### Notas de design

| Campo | Valor | Propósito |
|-------|-------|-----------|
| `Duration: 1` | 1 segundo | Duração curta, mas continuamente renovada pelos blocos de instrução do chefe |
| `Amount: 1.0` + `Multiplicative` | 100% de resistência | Imunidade total a dano enquanto o escudo está ativo |
| `SystemId: "Example_Shield"` | Partícula embutida | Exibe um efeito de bolha de escudo ao redor do chefe |
| `Invulnerable: false` | Não invulnerável | Permite que o escudo seja quebrado ao receber dano suficiente |

---

## Passo 5: Criar a Role do Chefe

Este é o arquivo principal. O chefe usa `Type: "Generic"` com uma máquina de estados controlando fases, movimentação de combate e ataques.

Crie `Server/NPC/Roles/Boss_Slime_Giant.json`:

```json
{
  "Type": "Generic",
  "Appearance": "BossSlime_Giant",
  "MaxHealth": 450,
  "KnockbackScale": 0.5,
  "DisableDamageGroups": ["Self"],
  "DefaultNPCAttitude": "Ignore",
  "DefaultPlayerAttitude": "Neutral",
  "DropList": "Drop_BossSlime_Crown",
  "IsMemory": true,
  "MemoriesCategory": "Boss",
  "StartState": "Idle",
  "MotionControllerList": [
    {
      "Type": "Walk",
      "MaxWalkSpeed": 6,
      "Gravity": 10,
      "RunThreshold": 0.3,
      "MaxFallSpeed": 15,
      "MaxRotationSpeed": 360,
      "Acceleration": 8
    }
  ],
  "CombatConfig": {
    "EntityEffect": "Shield_Crystal"
  },
  "InteractionVars": {
    "Melee_Start": {
      "Interactions": ["Boss_Slime_Attack_Start"]
    },
    "Melee_Damage": {
      "Interactions": [{ "Parent": "Boss_Slime_Slam_Damage" }]
    }
  }
}
```

### Campos principais explicados

| Campo | Propósito |
|-------|-----------|
| `Type: "Generic"` | Controle manual total via blocos de instrução (sem IA de template) |
| `InteractionVars.Melee_Start` | Sobrescreve `Root_NPC_Attack_Melee` para usar a animação de ataque do slime |
| `InteractionVars.Melee_Damage` | Sobrescreve a interação de dano com valores personalizados |
| `CombatConfig.EntityEffect` | Aplica o efeito `Shield_Crystal` durante o combate |
| `DefaultPlayerAttitude: "Neutral"` | O chefe ignora jogadores até ser atacado |
| `StartState: "Idle"` | O chefe começa no estado Idle |

---

## Passo 6: Adicionar Transições de Fase

As transições de fase usam sensores `Once` que disparam quando o HP cai abaixo de limites. Adicione-os como `Instructions` com `Continue: true` para que executem junto com outros blocos.

```json
{
  "$Comment": "Phase 1 end: HP <= 77.8% - spawn 1 slime",
  "Continue": true,
  "Instructions": [{
    "Sensor": {
      "Type": "Self", "Once": true,
      "Filters": [{
        "Type": "Stat", "Stat": "Health", "StatTarget": "Value",
        "RelativeTo": "Health", "RelativeToTarget": "Max",
        "ValueRange": [0, 0.778]
      }]
    },
    "Actions": [{
      "Type": "Spawn", "FanOut": true, "SpawnAngle": 360,
      "DistanceRange": [3, 5], "CountRange": [1, 1],
      "DelayRange": [0, 0], "Kind": "Slime"
    }]
  }]
}
```

O chefe completo tem quatro gatilhos de fase:

| Fase | Limite de HP | Ações |
|------|-------------|-------|
| Fim da Fase 1 | 77,8% (350 HP) | Invoca 1 Slime |
| Início da Fase 2 | 55,6% (250 HP) | Muda para aparência Média, reativa escudo, invoca 2 Slimes |
| Fim da Fase 2 | 38,9% (175 HP) | Invoca 1 Slime |
| Início da Fase 3 | 22,2% (100 HP) | Muda para aparência Pequena, invoca 2 Slimes |

A mudança de aparência usa ações `"Type": "Appearance"`:

```json
{ "Type": "Appearance", "Appearance": "BossSlime_Medium" }
```

Blocos de renovação de escudo usam sensores contínuos (sem `Once`) para reaplicar o escudo a cada segundo durante fases protegidas:

```json
{
  "Continue": true,
  "Instructions": [{
    "Sensor": {
      "Type": "Self",
      "Filters": [{
        "Type": "Stat", "Stat": "Health", "StatTarget": "Value",
        "RelativeTo": "Health", "RelativeToTarget": "Max",
        "ValueRange": [0.778, 1.0]
      }]
    },
    "Actions": [{
      "Type": "ApplyEntityEffect", "UseTarget": false,
      "EntityEffect": "Shield_Crystal"
    }]
  }]
}
```

---

## Passo 7: Adicionar Movimentação de Combate

O chefe usa dois modos de movimentação controlados por estado:

**Estado Idle** — Vagueia aleatoriamente, observa jogadores próximos:

```json
{
  "Sensor": { "Type": "State", "State": "Idle" },
  "Instructions": [
    {
      "Sensor": { "Type": "Player", "Range": 20 },
      "HeadMotion": { "Type": "Watch" },
      "BodyMotion": { "Type": "Nothing" }
    },
    {
      "Sensor": { "Type": "Any" },
      "BodyMotion": {
        "Type": "Wander",
        "MaxHeadingChange": 45,
        "RelativeSpeed": 0.3
      }
    }
  ]
}
```

**Estado Combat** — Mantém distância e faz strafing:

```json
{
  "Sensor": { "Type": "State", "State": "Combat" },
  "Instructions": [{
    "Sensor": { "Type": "Player", "Range": 30 },
    "BodyMotion": {
      "Type": "MaintainDistance",
      "DesiredDistanceRange": [1.5, 3.5],
      "MoveThreshold": 0.5,
      "RelativeForwardsSpeed": 0.6,
      "RelativeBackwardsSpeed": 0.5,
      "StrafingDurationRange": [1, 1],
      "StrafingFrequencyRange": [2, 2]
    }
  }]
}
```

### Parâmetros do MaintainDistance

| Campo | Valor | Propósito |
|-------|-------|-----------|
| `DesiredDistanceRange: [1.5, 3.5]` | Ficar a 1,5-3,5 blocos do jogador | Perto o suficiente para corpo a corpo, compatível com Template_Predator vanilla |
| `StrafingDurationRange: [1, 1]` | Strafing por 1 segundo | Cria o movimento de "dança de combate" |
| `StrafingFrequencyRange: [2, 2]` | Strafing a cada 2 segundos | Reposicionamento regular durante o combate |
| `RelativeForwardsSpeed: 0.6` | 60% da velocidade ao se aproximar | Aproximação cautelosa |

<Aside type="caution">
Definir `DesiredDistanceRange` muito alto (ex.: `[3, 5]`) manterá o chefe fora do alcance corpo a corpo. Predadores corpo a corpo vanilla usam `[1.5, 3.5]` calculado a partir de `AttackDistance - 1`.
</Aside>

---

## Passo 8: Adicionar Ações de Combate

O bloco de combate controla transições de estado e ataques:

```json
{
  "Instructions": [
    {
      "Sensor": { "Type": "State", "State": "Idle" },
      "Instructions": [
        {
          "Sensor": { "Type": "Damage" },
          "Actions": [{ "Type": "State", "State": "Combat" }]
        },
        {
          "Sensor": { "Type": "Any" },
          "Actions": [{ "Type": "Nothing" }]
        }
      ]
    },
    {
      "Sensor": { "Type": "State", "State": "Combat" },
      "Instructions": [
        {
          "Sensor": { "Type": "Player", "Range": 14 },
          "ActionsBlocking": true,
          "Actions": [
            {
              "Type": "Attack",
              "Attack": "Root_NPC_Attack_Melee",
              "AttackPauseRange": [1.0, 2.0]
            },
            { "Type": "Timeout", "Delay": [0.2, 0.2] }
          ],
          "HeadMotion": { "Type": "Aim", "RelativeTurnSpeed": 1.5 }
        },
        {
          "Sensor": { "Type": "Not", "Sensor": { "Type": "Player", "Range": 40 } },
          "Actions": [{ "Type": "State", "State": "Idle" }]
        }
      ]
    }
  ]
}
```

### Como InteractionVars sobrescrevem a cadeia de ataque

A cadeia vanilla `Root_NPC_Attack_Melee` funciona através de Replace Vars:

```
Root_NPC_Attack_Melee
  └─ Replace Var "Melee_Start" (padrão: NPC_Attack_Melee_Simple → SwingLeft)
       └─ Replace Var "Melee_Selector" (padrão: NPC_Attack_Selector_Left)
            └─ Replace Var "Melee_Damage" (padrão: dano genérico)
```

Ao definir `InteractionVars` na role do chefe, você sobrescreve elos específicos:
- `Melee_Start` → `Boss_Slime_Attack_Start` (reproduz a animação do slime em vez do golpe humanoide)
- `Melee_Damage` → `Boss_Slime_Slam_Damage` (valores de dano e knockback personalizados)

---

## Passo 9: Criar Drops de Loot

Crie `Server/Drops/Drop_BossSlime_Crown.json`:

```json
{
  "Container": {
    "Type": "Choice",
    "Containers": [
      {
        "Type": "Single",
        "Item": { "ItemId": "Trophy_Slime_Crown", "QuantityMin": 1, "QuantityMax": 1 },
        "Weight": 100
      },
      {
        "Type": "Single",
        "Item": { "ItemId": "Ore_Crystal_Glow", "QuantityMin": 1, "QuantityMax": 3 },
        "Weight": 80
      }
    ]
  }
}
```

Crie o item troféu em `Server/Item/Items/Trophy_Slime_Crown.json`:

```json
{
  "TranslationProperties": {
    "Name": "Slime Crown",
    "Description": "A trophy from the defeated Slime King"
  },
  "Model": "NPC/Beast/BossSlime/Model/Model_Crown.blockymodel",
  "Texture": "NPC/Beast/BossSlime/Model/Texture.png",
  "MaxStack": 1,
  "Scale": 0.5,
  "Icon": "Icons/ItemsGenerated/Trophy_Slime_Crown.png"
}
```

---

## Passo 10: Configurar World Spawns

Adicione o chefe e os slimes regulares às florestas da Zona 1.

Crie `Server/NPC/Spawn/World/Zone1/Spawns_Zone1_Forests_Slime.json`:

```json
{
  "Environments": [
    "Env_Zone1_Forests",
    "Env_Zone1_Autumn",
    "Env_Zone1_Azure"
  ],
  "NPCs": [
    {
      "Weight": 8,
      "SpawnBlockSet": "Soil",
      "Id": "Slime"
    },
    {
      "Weight": 1,
      "SpawnBlockSet": "Soil",
      "Id": "Boss_Slime_Giant"
    }
  ],
  "DayTimeRange": [6, 18]
}
```

### Design do spawn

| Campo | Propósito |
|-------|-----------|
| `Environments` | Todas as três variantes de floresta da Zona 1 |
| `Weight: 8` vs `Weight: 1` | Slimes regulares são 8x mais comuns que o chefe |
| `SpawnBlockSet: "Soil"` | Aparecem em blocos de grama/terra |
| `DayTimeRange: [6, 18]` | Apenas durante o dia (6h às 18h) |

---

## Passo 11: Testar o Chefe

1. Ative o mod e inicie um servidor na Zona 1.
2. Explore a Floresta Azure para encontrar slimes gerados naturalmente.
3. Encontre ou invoque o Boss Slime Giant com o console de desenvolvedor.

| Teste | Resultado Esperado |
|-------|--------------------|
| Chefe vagueia em Idle | Move-se lentamente, muda de direção aleatoriamente |
| Jogador se aproxima a 20 blocos | Chefe observa o jogador mas não ataca |
| Jogador atinge o chefe | Chefe entra no estado Combat, começa a fazer strafing |
| Chefe ataca | Reproduz animação de ataque do slime, causa 15 de dano físico com knockback |
| HP cai abaixo de 77,8% | Invoca 1 Slime próximo |
| HP cai abaixo de 55,6% | Muda para aparência Média, escudo reativa, invoca 2 Slimes |
| HP cai abaixo de 38,9% | Invoca 1 Slime |
| HP cai abaixo de 22,2% | Muda para aparência Pequena, invoca 2 Slimes |
| Chefe morre | Dropa troféu Coroa do Slime ou minério Crystal Glow |

### Solução de Problemas

| Problema | Causa | Solução |
|----------|-------|---------|
| Sem animação de ataque | `AnimationSets` contém `Attack` | Remova `Attack` do `AnimationSets` do modelo, defina-o apenas em `ItemPlayerAnimations` |
| Chefe fica longe demais para acertar | `DesiredDistanceRange` muito alto | Use `[1.5, 3.5]` para alcance corpo a corpo |
| Chefe não se move em idle | `BodyMotion` definido como `Nothing` | Adicione `"Type": "Wander"` com `RelativeSpeed: 0.3` |
| Servidor falha ao carregar | `ItemPlayerAnimationsId` inválido | Certifique-se de que o arquivo de animação existe em `Server/Item/Animations/` e inclui as seções `Camera` + `WiggleWeights` |
| Chefe ataca mas não causa dano | `InteractionVars.Melee_Damage` ausente | Adicione a sobrescrita de dano referenciando `Boss_Slime_Slam_Damage` |

---

## Estrutura Completa de Arquivos

```
CreateACustomNPC/
  Common/
    NPC/Beast/BossSlime/
      Animations/Default/
        Attack.blockyanim, Idle.blockyanim, Walk.blockyanim,
        Death.blockyanim, Run.blockyanim, Walk_Backward.blockyanim, ...
      Model/
        Model_Giant.blockymodel, Model_Medium.blockymodel,
        Model.blockymodel, Model_Crown.blockymodel,
        Texture_Giant.png, Texture_Medium.png, Texture.png
    Icons/
      ModelsGenerated/  (BossSlime_Giant.png, etc.)
      ItemsGenerated/   (Trophy_Slime_Crown.png)
  Server/
    Models/Beast/
      BossSlime_Giant.json, BossSlime_Medium.json,
      BossSlime_Small.json, BossSlime.json
    Item/
      Animations/NPC/Beast/BossSlime/BossSlime_Default.json
      Interactions/
        Boss_Slime_Attack_Start.json, Boss_Slime_Slam_Damage.json
      Items/Trophy_Slime_Crown.json
    Entity/Effects/Shield_Crystal.json
    Drops/Drop_BossSlime_Crown.json
    NPC/
      Roles/Boss_Slime_Giant.json
      Spawn/World/Zone1/Spawns_Zone1_Forests_Slime.json
  manifest.json
```

---

## Próximos Passos

- [Criar um NPC](/hytale-modding-docs/tutorials/beginner/create-an-npc) -- crie o NPC Slime base que o chefe invoca
- [Spawning Personalizado de NPCs](/hytale-modding-docs/tutorials/intermediate/custom-npc-spawning) -- saiba mais sobre configuração de world spawn
- [Árvores de Comportamento de IA de NPCs](/hytale-modding-docs/tutorials/advanced/npc-ai-behavior-trees) -- padrões avançados de IA para NPCs
- [Entity Effects](/hytale-modding-docs/reference/combat-and-projectiles/entity-effects) -- referência completa de entity effects
- [NPC Roles](/hytale-modding-docs/reference/npc-system/npc-roles) -- schema completo de NPC roles
