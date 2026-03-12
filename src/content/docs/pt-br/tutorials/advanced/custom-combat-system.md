---
title: Crie um Sistema de Combate Personalizado
description: Criando um sistema de combate personalizado com novos tipos de dano, efeitos de entidade, interações de projétil, atributos de arma e balanceamento de combate de NPCs.
---

## Objetivo

Construir um sistema de combate personalizado completo em torno de um novo tipo de dano **Lightning** (Raio). Você criará a definição do tipo de dano, uma arma cajado de raio com configurações de projétil, efeitos de entidade que se aplicam ao acertar, e um NPC que usa ataques de raio com um Combat Action Evaluator ajustado. Este tutorial demonstra como os componentes de combate do Hytale se conectam: tipos de dano, projéteis, interações, itens e IA de NPCs.

## Pré-requisitos

- Uma pasta de mod com um `manifest.json` válido (veja [Configure Seu Ambiente de Desenvolvimento](/hytale-modding-docs/tutorials/beginner/setup-dev-environment))
- Entendimento de tipos de dano (veja [Tipos de Dano](/hytale-modding-docs/reference/combat-and-projectiles/damage-types))
- Entendimento de projéteis (veja [Projéteis](/hytale-modding-docs/reference/combat-and-projectiles/projectiles) e [Configurações de Projétil](/hytale-modding-docs/reference/combat-and-projectiles/projectile-configs))
- Familiaridade com definições de itens (veja [Definições de Itens](/hytale-modding-docs/reference/item-system/item-definitions))
- Entendimento de IA de combate de NPCs (veja [Balanceamento de Combate de NPCs](/hytale-modding-docs/reference/npc-system/npc-combat-balancing))

---

## Arquitetura do Sistema

O sistema de combate envolve cinco tipos de arquivo interconectados:

```
Damage Type  ─── define propriedades de dano (perda de durabilidade, perda de stamina, cor)
    │
Projectile   ─── define física e valores base de dano
    │
Projectile Config ─── define parâmetros de lançamento e cadeias de interação
    │
Item Definition ─── define a arma que lança o projétil
    │
NPC CAE      ─── define a IA que usa as habilidades da arma
```

Cada componente referencia os outros por ID. Construí-los em ordem garante que cada camada tenha suas dependências em vigor.

---

## Passo 1: Criar um Tipo de Dano Personalizado

Tipos de dano definem como o dano interage com o alvo: se causa perda de durabilidade, dreno de stamina, ignora resistências e qual cor os números de dano flutuantes exibem.

Crie `YourMod/Assets/Server/Entity/Damage/Lightning.json`:

```json
{
  "Parent": "Elemental",
  "Inherits": "Elemental",
  "DurabilityLoss": false,
  "StaminaLoss": true,
  "BypassResistances": false,
  "DamageTextColor": "#7DF9FF"
}
```

### Decisões de design

| Campo | Valor | Justificativa |
|-------|-------|---------------|
| `Parent: "Elemental"` | Herda da raiz Elemental | Raio é um subtipo elemental, como Fogo e Gelo |
| `DurabilityLoss: false` | Não danifica equipamento | Dano elemental tradicionalmente não desgasta equipamento |
| `StaminaLoss: true` | Drena stamina ao acertar | Raio choca o alvo, esgotando stamina |
| `BypassResistances: false` | Sujeito a verificações de resistência | Permite que armadura e buffs reduzam dano de raio |
| `DamageTextColor: "#7DF9FF"` | Azul elétrico | Distinto de Fogo (padrão) e Veneno (#00FF00) |

A hierarquia de tipos de dano agora se parece com:

```
Elemental
├── Fire
├── Ice
├── Poison
└── Lightning  (seu novo tipo)
```

---

## Passo 2: Criar o Projétil de Raio

Defina a entidade de projétil que voa pelo mundo quando a arma dispara.

Crie `YourMod/Assets/Server/Projectiles/Spells/LightningBolt.json`:

```json
{
  "Appearance": "LightningBolt",
  "Radius": 0.15,
  "Height": 0.3,
  "MuzzleVelocity": 55,
  "TerminalVelocity": 120,
  "Gravity": 2,
  "Bounciness": 0,
  "TimeToLive": 5,
  "Damage": 45,
  "DeadTime": 0,
  "DeathEffectsOnHit": true,
  "HitSoundEventId": "SFX_Lightning_Hit",
  "MissSoundEventId": "SFX_Lightning_Miss",
  "DeathSoundEventId": "SFX_Lightning_Death",
  "HitParticles": {
    "SystemId": "Impact_Lightning"
  },
  "MissParticles": {
    "SystemId": "Lightning_Sparks"
  },
  "DeathParticles": {
    "SystemId": "Lightning_Dissipate"
  },
  "ExplosionConfig": {
    "DamageEntities": true,
    "DamageBlocks": false,
    "EntityDamageRadius": 3,
    "EntityDamageFalloff": 0.5
  }
}
```

### Notas de design do projétil

| Campo | Valor | Comparação |
|-------|-------|------------|
| `MuzzleVelocity: 55` | Mais rápido que Fireball (40) | Raio deve parecer mais rápido que fogo |
| `Gravity: 2` | Gravidade baixa | Trajetória quase reta, diferente de flechas (gravidade 10-15) |
| `Damage: 45` | Entre Ice Ball (20) e Fireball (60) | Balanceado para um elemental de médio alcance |
| `TimeToLive: 5` | 5 segundos de vida | Desaparece se não atingir nada |
| `EntityDamageRadius: 3` | AoE pequena | Efeito de raio em cadeia em entidades próximas, menor que Fireball (5) |
| `EntityDamageFalloff: 0.5` | 50% de dano na borda | Entidades na borda da AoE recebem metade do dano |

Compare com a Fireball vanilla que tem `MuzzleVelocity: 40`, `Gravity: 4`, `Damage: 60` e `EntityDamageRadius: 5`. Raio troca dano bruto por velocidade e precisão.

---

## Passo 3: Criar a Configuração do Projétil

A configuração do projétil faz a ponte entre a arma e o projétil, definindo parâmetros de lançamento e cadeias de interação para eventos de acerto/erro.

Crie `YourMod/Assets/Server/ProjectileConfigs/Weapons/Staff/Lightning/Projectile_Config_LightningBolt.json`:

```json
{
  "Model": "LightningBolt",
  "LaunchForce": 35,
  "Physics": {
    "Type": "Standard",
    "Gravity": 2,
    "TerminalVelocityAir": 55,
    "TerminalVelocityWater": 10,
    "RotationMode": "VelocityDamped",
    "Bounciness": 0.0,
    "SticksVertically": false
  },
  "LaunchWorldSoundEventId": "SFX_Staff_Lightning_Shoot",
  "SpawnOffset": {
    "X": 0.1,
    "Y": -0.2,
    "Z": 0.5
  },
  "Interactions": {
    "ProjectileHit": {
      "Interactions": [
        {
          "Parent": "DamageEntityParent",
          "DamageCalculator": {
            "Class": "Charged",
            "BaseDamage": {
              "Lightning": 45
            }
          },
          "DamageEffects": {
            "Knockback": {
              "Type": "Force",
              "Force": 15,
              "VelocityType": "Set"
            },
            "WorldParticles": [
              { "SystemId": "Impact_Lightning" },
              { "SystemId": "Lightning_Sparks" }
            ],
            "WorldSoundEventId": "SFX_Lightning_Hit"
          }
        },
        {
          "Type": "ApplyEffect",
          "EffectId": "Effect_Lightning_Stun",
          "Duration": 1.5
        },
        {
          "Type": "RemoveEntity",
          "Entity": "User"
        }
      ]
    },
    "ProjectileMiss": {
      "Interactions": [
        {
          "Type": "Simple",
          "Effects": {
            "WorldSoundEventId": "SFX_Lightning_Miss",
            "WorldParticles": [
              { "SystemId": "Lightning_Sparks" }
            ]
          }
        },
        {
          "Type": "RemoveEntity",
          "Entity": "User"
        }
      ]
    },
    "ProjectileSpawn": {
      "Interactions": [
        {
          "Type": "Simple",
          "Effects": {
            "WorldParticles": [
              { "SystemId": "Lightning_Charge" }
            ]
          }
        }
      ]
    }
  }
}
```

### Detalhamento da cadeia de interação

A cadeia `ProjectileHit` executa três interações em sequência:

1. **DamageEntityParent** — calcula e aplica dano usando o tipo de dano `Lightning` com 45 de dano base, com força de knockback 15 e efeitos de partícula/som
2. **ApplyEffect** — aplica um efeito de atordoamento (`Effect_Lightning_Stun`) por 1,5 segundos, impedindo o alvo de agir
3. **RemoveEntity** — destrói o projétil após acertar

O campo `BaseDamage` usa um mapa de tipo de dano para valor: `{ "Lightning": 45 }`. Isso referencia seu tipo de dano personalizado pelo ID do nome de arquivo. Compare com a configuração vanilla Ice Ball que usa `{ "Ice": 20 }`.

---

## Passo 4: Criar a Arma Cajado de Raio

Defina o item de arma que lança raios.

Crie `YourMod/Assets/Server/Item/Items/Weapon/Staff/Weapon_Staff_Lightning.json`:

```json
{
  "Parent": "Template_Weapon",
  "TranslationProperties": {
    "Name": "server.items.Weapon_Staff_Lightning.name",
    "Description": "server.items.Weapon_Staff_Lightning.description"
  },
  "Quality": "Rare",
  "Icon": "Icons/ItemsGenerated/Weapon_Staff_Lightning.png",
  "Categories": ["Items.Weapons.Staves"],
  "ItemLevel": 15,
  "MaxStack": 1,
  "MaxDurability": 250,
  "DurabilityLossOnHit": 2,
  "DropOnDeath": true,
  "PlayerAnimationsId": "Staff",
  "Model": "Items/Weapons/Staff/Lightning.blockymodel",
  "Texture": "Items/Weapons/Staff/Lightning_Texture.png",
  "Weapon": {},
  "Tags": {
    "Type": ["Weapon"],
    "Family": ["Staff"],
    "Element": ["Lightning"]
  },
  "Interactions": {
    "Primary": "Root_Primary_Staff_Lightning"
  },
  "InteractionVars": {
    "ProjectileConfig": {
      "Interactions": [
        {
          "Type": "SpawnProjectile",
          "ProjectileConfigId": "Projectile_Config_LightningBolt"
        }
      ]
    }
  },
  "Recipe": {
    "Input": [
      { "ItemId": "Ingredient_Crystal", "Quantity": 5 },
      { "ItemId": "Ingredient_Wood_Stick", "Quantity": 2 },
      { "ResourceTypeId": "Metal_Ingot", "Quantity": 3 }
    ],
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Id": "MagicBench",
        "Categories": ["Staves"]
      }
    ],
    "TimeSeconds": 10
  }
}
```

### Campos principais da arma

| Campo | Propósito |
|-------|-----------|
| `Weapon: {}` | Objeto vazio que ativa o comportamento de arma no item |
| `PlayerAnimationsId: "Staff"` | Usa o conjunto de animações de cajado para o personagem do jogador |
| `MaxDurability: 250` | Cajado tem 250 usos antes de quebrar |
| `DurabilityLossOnHit: 2` | Cada disparo custa 2 de durabilidade (125 disparos no total) |
| `ProjectileConfigId` | Referencia a configuração de projétil que define o comportamento de lançamento |
| `Tags.Element: ["Lightning"]` | Tag usada para filtragem e consultas de resistência |

---

## Passo 5: Criar Efeitos de Entidade

Efeitos de entidade são condições de status aplicadas aos alvos. Crie um efeito de atordoamento que o raio aplica ao acertar.

Crie `YourMod/Assets/Server/Entity/Effects/Effect_Lightning_Stun.json`:

```json
{
  "Id": "Effect_Lightning_Stun",
  "Duration": 1.5,
  "Stackable": false,
  "MaxStacks": 1,
  "StatModifiers": {
    "MaxSpeed": {
      "Type": "Multiply",
      "Value": 0
    },
    "AttackSpeed": {
      "Type": "Multiply",
      "Value": 0
    }
  },
  "Particles": {
    "SystemId": "Lightning_Stun_Loop",
    "AttachToEntity": true
  },
  "Icon": "Icons/Effects/Lightning_Stun.png",
  "TranslationKey": "server.effects.Lightning_Stun.name"
}
```

### Design do efeito

| Campo | Propósito |
|-------|-----------|
| `Duration: 1.5` | Efeito dura 1,5 segundos |
| `Stackable: false` | Acertar um alvo atordoado não estende o atordoamento |
| `StatModifiers.MaxSpeed` | Multiplicar por 0 = alvo não pode se mover |
| `StatModifiers.AttackSpeed` | Multiplicar por 0 = alvo não pode atacar |
| `Particles` | Indicador visual anexado à entidade atordoada |

Crie um segundo efeito para um debuff de dano ao longo do tempo por raio:

Crie `YourMod/Assets/Server/Entity/Effects/Effect_Lightning_Shock.json`:

```json
{
  "Id": "Effect_Lightning_Shock",
  "Duration": 5,
  "Stackable": true,
  "MaxStacks": 3,
  "TickInterval": 1.0,
  "TickDamage": {
    "DamageType": "Lightning",
    "Amount": 8
  },
  "StatModifiers": {
    "MaxSpeed": {
      "Type": "Multiply",
      "Value": 0.7
    }
  },
  "Particles": {
    "SystemId": "Lightning_Shock_Loop",
    "AttachToEntity": true
  },
  "Icon": "Icons/Effects/Lightning_Shock.png",
  "TranslationKey": "server.effects.Lightning_Shock.name"
}
```

Este acumula até 3 vezes, causando 8 de dano Lightning por segundo por acúmulo (máximo 24/segundo) enquanto desacelera o alvo para 70% da velocidade. Cada acúmulo tem sua própria duração de 5 segundos.

---

## Passo 6: Criar um NPC que Usa Raio

Construa um NPC **Storm Mage** que usa ataques de raio em combate, demonstrando como a IA de NPC se integra com o sistema de combate personalizado.

Crie `YourMod/Assets/Server/NPC/Roles/MyMod/Storm_Mage.json`:

```json
{
  "Type": "Variant",
  "Reference": "Template_Intelligent",
  "Modify": {
    "Appearance": "Mage_Storm",
    "DropList": "Drop_Storm_Mage",
    "MaxHealth": 95,
    "MaxSpeed": 5,
    "ViewRange": 22,
    "ViewSector": 180,
    "HearingRange": 14,
    "AlertedRange": 30,
    "DefaultPlayerAttitude": "Hostile",
    "FleeRange": 18,
    "FleeHealthThreshold": 0.2,
    "FleeSpeed": 7,
    "IsMemory": true,
    "MemoriesCategory": "Other",
    "MemoriesNameOverride": "Storm Mage",
    "NameTranslationKey": {
      "Compute": "NameTranslationKey"
    }
  },
  "Parameters": {
    "NameTranslationKey": {
      "Value": "server.npcRoles.Storm_Mage.name",
      "Description": "Translation key for NPC name display"
    }
  }
}
```

Crie o CAE do Storm Mage em `YourMod/Assets/Server/NPC/Balancing/Intelligent/CAE_Storm_Mage.json`:

```json
{
  "Type": "CombatActionEvaluator",
  "TargetMemoryDuration": 6,
  "CombatActionEvaluator": {
    "RunConditions": [
      {
        "Type": "TimeSinceLastUsed",
        "Curve": { "ResponseCurve": "Linear", "XRange": [0, 4] }
      },
      { "Type": "Randomiser", "MinValue": 0.9, "MaxValue": 1 }
    ],
    "MinRunUtility": 0.5,
    "MinActionUtility": 0.01,
    "AvailableActions": {
      "SelectTarget": {
        "Type": "SelectBasicAttackTarget",
        "Description": "Select target for ranged lightning attacks",
        "Conditions": [
          {
            "Type": "TargetDistance",
            "Curve": { "ResponseCurve": "SimpleDescendingLogistic", "XRange": [0, 25] }
          }
        ]
      },
      "LightningBolt": {
        "Type": "Ability",
        "Description": "Fire a lightning bolt at the target",
        "Ability": "Storm_Mage_LightningBolt",
        "Target": "Hostile",
        "AttackDistanceRange": [15, 15],
        "PostExecuteDistanceRange": [10, 12],
        "WeightCoefficient": 1.0,
        "Conditions": [
          {
            "Type": "TargetDistance",
            "Curve": { "ResponseCurve": "SimpleLogistic", "XRange": [0, 18] }
          },
          {
            "Type": "TimeSinceLastUsed",
            "Curve": { "ResponseCurve": "Linear", "XRange": [0, 2] }
          }
        ]
      },
      "LightningBarrage": {
        "Type": "Ability",
        "Description": "Rapid fire three lightning bolts",
        "Ability": "Storm_Mage_LightningBarrage",
        "Target": "Hostile",
        "AttackDistanceRange": [12, 12],
        "PostExecuteDistanceRange": [8, 10],
        "ChargeFor": 1.0,
        "WeightCoefficient": 1.3,
        "Conditions": [
          {
            "Type": "TargetDistance",
            "Curve": { "ResponseCurve": "SimpleLogistic", "XRange": [0, 15] }
          },
          {
            "Type": "TimeSinceLastUsed",
            "Curve": { "Type": "Switch", "SwitchPoint": 8 }
          },
          {
            "Type": "TargetStatPercent",
            "Stat": "Health",
            "Curve": "Linear"
          }
        ]
      },
      "Retreat": {
        "Type": "Ability",
        "Description": "Teleport away when target gets too close",
        "Ability": "Storm_Mage_Retreat",
        "Target": "Self",
        "WeightCoefficient": 1.4,
        "Conditions": [
          {
            "Type": "TargetDistance",
            "Curve": { "ResponseCurve": "SimpleDescendingLogistic", "XRange": [0, 6] }
          },
          {
            "Type": "TimeSinceLastUsed",
            "Curve": { "Type": "Switch", "SwitchPoint": 5 }
          }
        ]
      }
    },
    "ActionSets": {
      "Default": {
        "BasicAttacks": {
          "Attacks": ["Storm_Mage_LightningBolt"],
          "Randomise": false,
          "MaxRange": 15,
          "Timeout": 1.0,
          "CooldownRange": [1.5, 2.5]
        },
        "Actions": [
          "SelectTarget",
          "LightningBolt",
          "LightningBarrage",
          "Retreat"
        ]
      }
    }
  }
}
```

### Design da IA do Storm Mage

O Storm Mage é um conjurador à distância que:
- **Prefere distância** — `PostExecuteDistanceRange` o mantém 10-12 blocos de distância após atacar
- **Usa LightningBarrage** em alvos com muita vida (a condição `TargetStatPercent(Health, Linear)` pontua mais alto quando o alvo tem muita vida)
- **Recua** quando jogadores se aproximam a menos de 6 blocos (logística descendente pontua alto em curta distância)
- **Foge** com 20% de vida (definido no arquivo de papel)

---

## Passo 7: Adicionar Chaves de Tradução

Adicione a `YourMod/Assets/Languages/en-US.lang`:

```
server.items.Weapon_Staff_Lightning.name=Lightning Staff
server.items.Weapon_Staff_Lightning.description=A crackling staff that channels lightning energy.
server.npcRoles.Storm_Mage.name=Storm Mage
server.effects.Lightning_Stun.name=Stunned
server.effects.Lightning_Shock.name=Shocked
```

---

## Passo 8: Testar o Sistema de Combate

1. Coloque sua pasta de mod no diretório de mods do servidor e inicie o servidor.
2. Dê a si mesmo o Cajado de Raio usando o spawner de itens do desenvolvedor.
3. Teste a arma:

| Teste | Resultado esperado |
|-------|-------------------|
| Disparar no terreno | Raio atinge o terreno, partícula de faíscas é reproduzida, som de erro é reproduzido |
| Disparar em NPC | NPC recebe 45 de dano Lightning (números azuis), fica atordoado por 1,5s, knockback aplicado |
| Verificar stamina do NPC | Stamina do NPC esgotada (StaminaLoss: true) |
| Verificar durabilidade de equipamento | Equipamento do alvo NÃO danificado (DurabilityLoss: false) |
| Disparar em grupo de NPCs | AoE causa dano em entidades dentro de 3 blocos com 50% de falloff |

4. Gere um Storm Mage e teste o combate de NPC:

| Teste | Resultado esperado |
|-------|-------------------|
| Aproximar-se do Storm Mage | Começa a disparar raios a 15 blocos de distância |
| Avançar para corpo a corpo | Storm Mage usa habilidade Retreat para se teleportar para longe |
| Esperar pela barragem | Storm Mage carrega por 1s e depois dispara raios rápidos |
| Causar dano até 20% de HP | Storm Mage foge na velocidade 7 |

### Solução de Problemas

| Problema | Causa | Correção |
|----------|-------|----------|
| Números de dano aparecem brancos | Tipo de dano não encontrado | Verifique se `Lightning.json` existe em `Entity/Damage/` e tem `DamageTextColor` |
| Projétil não causa dano | Chave `BaseDamage` incompatível | Certifique-se de que a chave `BaseDamage` corresponde ao nome de arquivo do tipo de dano: `"Lightning"` |
| Efeito de atordoamento não aplica | ID de efeito incompatível | Verifique se `EffectId` na interação corresponde ao campo `Id` do arquivo de efeito |
| Sem knockback ao acertar | Configuração de knockback ausente | Verifique se `DamageEffects.Knockback` tem `Force` > 0 |
| Arma não pode ser fabricada | ID do bench errado | Verifique se `BenchRequirement.Id` corresponde a uma bancada de fabricação existente |
| NPC não usa raio | CAE não referenciado | Certifique-se de que o papel do NPC referencia o arquivo CAE em sua ligação de template |

---

## Listagem Completa de Arquivos

```
YourMod/
  Assets/
    Server/
      Entity/
        Damage/
          Lightning.json
        Effects/
          Effect_Lightning_Stun.json
          Effect_Lightning_Shock.json
      Projectiles/
        Spells/
          LightningBolt.json
      ProjectileConfigs/
        Weapons/
          Staff/
            Lightning/
              Projectile_Config_LightningBolt.json
      Item/
        Items/
          Weapon/
            Staff/
              Weapon_Staff_Lightning.json
      NPC/
        Roles/
          MyMod/
            Storm_Mage.json
        Balancing/
          Intelligent/
            CAE_Storm_Mage.json
    Languages/
      en-US.lang
```

---

## Próximos Passos

- [Árvores de Comportamento de IA de NPCs](/hytale-modding-docs/tutorials/advanced/npc-ai-behavior-trees) — adicione IA complexa de múltiplos estados ao Storm Mage
- [Dungeons Personalizadas](/hytale-modding-docs/tutorials/advanced/custom-dungeons) — use o sistema de Raio em encontros de dungeon
- [Tipos de Dano](/hytale-modding-docs/reference/combat-and-projectiles/damage-types) — referência completa de tipos de dano
- [Configurações de Projétil](/hytale-modding-docs/reference/combat-and-projectiles/projectile-configs) — schema completo de configuração de projétil
- [Definições de Itens](/hytale-modding-docs/reference/item-system/item-definitions) — referência completa do schema de itens
