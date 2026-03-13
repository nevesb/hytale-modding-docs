---
title: Armas de Projétil
description: Tutorial passo a passo para adicionar ataques de projétil carregados a uma espada usando elementos de dano personalizados, configurações de projétil, consumo de munição e cadeias de interação.
sidebar:
  order: 5
---

## Objetivo

Adicionar **ataques de projétil** à Espada de Cristal do tutorial [Criar uma Bancada de Trabalho](/hytale-modding-docs/pt-br/tutorials/intermediate/create-a-crafting-bench/). Você criará um elemento de dano personalizado, munição fabricável e dois ataques de projétil: um **raio carregado** que consome munição no investida, e um **orbe especial** que dispara quando a SignatureEnergy está cheia.

![Raio de cristal disparando da Espada de Cristal durante um ataque de investida carregado](/hytale-modding-docs/images/tutorials/projectile-weapons/crystal-bolt-firing.png)

## O Que Você Vai Aprender

- Como definições de `Projectile` e arquivos `ProjectileConfig` funcionam juntos
- Como interações `Type: "Projectile"` disparam projéteis de armas
- Como `Type: "Charging"` cria ataques de segurar-para-carregar com uma barra de progresso
- Como `Type: "ModifyInventory"` consome munição com um fallback em caso de falha
- Como `EntityStatsOnHit` gera SignatureEnergy a partir de acertos de projétil
- Como `InteractionVars` sobrescrevem o comportamento padrão da espada sem substituir a cadeia completa

## Pré-requisitos

- O mod Bigorna de Cristal do tutorial [Criar uma Bancada de Trabalho](/hytale-modding-docs/pt-br/tutorials/intermediate/create-a-crafting-bench/)
- O mod Bloco Brilho de Cristal do tutorial [Criar um Bloco Personalizado](/hytale-modding-docs/pt-br/tutorials/beginner/create-a-block/)
- O mod Árvore Encantada do tutorial [Árvores e Mudas Personalizadas](/hytale-modding-docs/pt-br/tutorials/intermediate/custom-trees-and-saplings/)

**Repositório do mod complementar:** [hytale-mods-custom-projectile](https://github.com/nevesb/hytale-mods-custom-projectile) (v2.0.0)

:::note[Este Tutorial Substitui Mods Anteriores]
O mod complementar deste tutorial inclui tudo dos tutoriais [Criar um Item Personalizado](/hytale-modding-docs/pt-br/tutorials/beginner/create-an-item/) e [Criar uma Bancada de Trabalho](/hytale-modding-docs/pt-br/tutorials/intermediate/create-a-crafting-bench/). Você só precisa instalar `hytale-mods-custom-projectile` — ele substitui tanto `CreateACustomWeapon` quanto `CreateACraftingBench`.
:::

---

## Visão Geral do Sistema de Projéteis

O sistema de projéteis do Hytale possui três camadas:

| Camada | Localização | Finalidade |
|--------|-------------|------------|
| **Definição de Projétil** | `Server/Projectiles/` | A entidade do projétil: aparência, física, hitbox, dano base |
| **Configuração de Projétil** | `Server/ProjectileConfigs/` | Configurações de lançamento: força, deslocamento de spawn, sons e cadeias de interação de acerto/erro |
| **Interação da Arma** | `Server/Item/Interactions/` | `Type: "Projectile"` com uma referência `Config` que dispara o projétil |

O fluxo é:

```
Jogador segura ataque → Interação de carregamento (1s) → ModifyInventory (consome munição)
  → Sucesso: Animação de investida + Projétil dispara da ponta da espada
  → Falha (sem munição): Ataque de investida normal
```

---

## Passo 1: Criar um Elemento de Dano Personalizado

Crie um novo tipo de dano para que projéteis de cristal causem seu próprio elemento de dano com uma cor distinta.

```
Server/Entity/Damage/Crystal_Light.json
```

```json
{
  "Parent": "Elemental",
  "Inherits": "Elemental",
  "DamageTextColor": "#88ccff"
}
```

Os campos `Parent` e `Inherits` fazem Crystal Light se comportar como outros danos elementais (afetado por resistência elemental). O `DamageTextColor` controla a cor do número de dano flutuante — azul claro para combinar com o tema de cristal.

Elementos de dano vanilla como `Fire`, `Ice` e `Nature` seguem o mesmo padrão. Você pode referenciar seu elemento personalizado pelo nome (`"Crystal_Light"`) em qualquer objeto `BaseDamage`.

---

## Passo 2: Criar Definições de Projétil

Definições de projétil descrevem a entidade física que viaja pelo mundo. Crie duas: um raio rápido para o ataque carregado e um orbe grande para o ataque especial.

### Raio de Luz Cristalina

```
Server/Projectiles/Crystal_Light_Bolt.json
```

```json
{
  "Appearance": "Ice_Bolt",
  "Radius": 0.2,
  "Height": 0.2,
  "HorizontalCenterShot": 0.2,
  "VerticalCenterShot": 0.1,
  "DepthShot": 1.5,
  "PitchAdjustShot": true,
  "SticksVertically": false,
  "MuzzleVelocity": 55,
  "TerminalVelocity": 60,
  "Gravity": 2,
  "ImpactSlowdown": 0,
  "TimeToLive": 10,
  "Damage": 18,
  "DeadTimeMiss": 0,
  "DeathEffectsOnHit": true,
  "HitParticles": {
    "SystemId": "Impact_Ice"
  },
  "DeathParticles": {
    "SystemId": "Impact_Ice"
  },
  "HitSoundEventId": "SFX_Ice_Break",
  "DeathSoundEventId": "SFX_Ice_Break"
}
```

### Orbe de Luz Cristalina

```
Server/Projectiles/Crystal_Light_Orb.json
```

```json
{
  "Appearance": "Ice_Ball",
  "Radius": 2.5,
  "Height": 0.3,
  "HorizontalCenterShot": 0.2,
  "DepthShot": 1,
  "PitchAdjustShot": false,
  "SticksVertically": false,
  "MuzzleVelocity": 35,
  "TerminalVelocity": 45,
  "Gravity": 3,
  "Damage": 36,
  "DeathEffectsOnHit": true,
  "TimeToLive": 5,
  "DeadTimeMiss": 0,
  "ImpactSlowdown": 0,
  "VerticalCenterShot": 0,
  "HitParticles": {
    "SystemId": "Impact_Ice"
  },
  "DeathParticles": {
    "SystemId": "IceBall_Explosion"
  },
  "MissParticles": {
    "SystemId": "IceBall_Explosion"
  },
  "DeathSoundEventId": "SFX_Ice_Ball_Death"
}
```

### Diferenças Principais

| Propriedade | Raio | Orbe |
|-------------|------|------|
| `Appearance` | `Ice_Bolt` (pequeno, formato de flecha) | `Ice_Ball` (esfera grande) |
| `MuzzleVelocity` | 55 (rápido) | 35 (mais lento) |
| `Gravity` | 2 (trajetória reta) | 3 (leve arco) |
| `Radius` | 0.2 (estreito) | 2.5 (amplo, com splash) |
| `Damage` | 18 | 36 (o dobro) |

:::tip[Aparências Vanilla]
Valores de `Appearance` de projéteis referenciam modelos visuais integrados. Opções comuns incluem `Ice_Bolt`, `Ice_Ball`, `Arrow_Crude`, `Arrow_FullCharge` e `Bomb`. Você pode encontrá-los navegando em `Assets/Server/Projectiles/`.
:::

---

## Passo 3: Criar Configurações de Projétil

Configurações de Projétil conectam a interação da arma ao projétil. Elas definem força de lançamento, posição de spawn, sons e o que acontece no acerto ou erro.

### Configuração do Raio

```
Server/ProjectileConfigs/HytaleModdingManual/Projectile_Config_Crystal_Light_Bolt.json
```

```json
{
  "Parent": "Projectile_Config_Arrow_Base",
  "Model": "Ice_Bolt",
  "Physics": {
    "Type": "Standard",
    "Gravity": 2,
    "TerminalVelocityAir": 60,
    "TerminalVelocityWater": 15,
    "RotationMode": "VelocityDamped",
    "Bounciness": 0.0,
    "SticksVertically": false
  },
  "LaunchForce": 55,
  "SpawnOffset": {
    "X": 0.3,
    "Y": -0.3,
    "Z": 1.5
  },
  "LaunchLocalSoundEventId": "SFX_Ice_Break",
  "LaunchWorldSoundEventId": "SFX_Ice_Break",
  "Interactions": {
    "ProjectileHit": {
      "Interactions": [
        "Crystal_Light_Bolt_Damage",
        "Common_Projectile_Despawn"
      ]
    },
    "ProjectileMiss": {
      "Interactions": [
        "Common_Projectile_Miss",
        "Common_Projectile_Despawn"
      ]
    }
  }
}
```

O `SpawnOffset` controla onde o projétil aparece em relação ao jogador. `Z: 1.5` empurra para frente até a ponta da espada. `Y: -0.3` abaixa a partir da altura da cabeça.

`Parent: "Projectile_Config_Arrow_Base"` herda a física padrão de flecha e rotação de spawn. Sobrescrevemos `Physics`, `LaunchForce` e `SpawnOffset` para o comportamento do nosso raio de cristal.

### Configuração do Orbe

```
Server/ProjectileConfigs/HytaleModdingManual/Projectile_Config_Crystal_Light_Orb.json
```

```json
{
  "Parent": "Projectile_Config_Arrow_Base",
  "Model": "Ice_Ball",
  "Physics": {
    "Type": "Standard",
    "Gravity": 3,
    "TerminalVelocityAir": 45,
    "TerminalVelocityWater": 10,
    "RotationMode": "VelocityDamped",
    "Bounciness": 0.0,
    "SticksVertically": false
  },
  "LaunchForce": 35,
  "LaunchLocalSoundEventId": "SFX_Ice_Ball_Death",
  "LaunchWorldSoundEventId": "SFX_Ice_Ball_Death",
  "Interactions": {
    "ProjectileHit": {
      "Interactions": [
        "Crystal_Light_Orb_Damage",
        "Common_Projectile_Despawn"
      ]
    },
    "ProjectileMiss": {
      "Interactions": [
        "Common_Projectile_Miss",
        "Common_Projectile_Despawn"
      ]
    }
  }
}
```

---

## Passo 4: Criar Interações de Dano

Interações de dano definem o que acontece quando um projétil acerta uma entidade. Elas especificam quantidades de dano, recuo, partículas, sons e geração de stats.

### Dano do Raio

```
Server/Item/Interactions/HytaleModdingManual/Crystal_Light_Bolt_Damage.json
```

```json
{
  "Parent": "DamageEntityParent",
  "DamageCalculator": {
    "BaseDamage": {
      "Crystal_Light": 18
    }
  },
  "DamageEffects": {
    "Knockback": {
      "Type": "Force",
      "VelocityConfig": {
        "AirResistance": 0.97,
        "AirResistanceMax": 0.96,
        "GroundResistance": 0.94,
        "GroundResistanceMax": 0.3,
        "Threshold": 3.0,
        "Style": "Exp"
      },
      "Direction": {
        "X": 0.0,
        "Y": 1,
        "Z": -3
      },
      "Force": 8,
      "VelocityType": "Add"
    },
    "WorldParticles": [
      {
        "SystemId": "Impact_Ice",
        "Scale": 1
      }
    ],
    "WorldSoundEventId": "SFX_Ice_Break",
    "EntityStatsOnHit": [
      {
        "EntityStatId": "SignatureEnergy",
        "Amount": 5
      }
    ]
  }
}
```

### Dano do Orbe

```
Server/Item/Interactions/HytaleModdingManual/Crystal_Light_Orb_Damage.json
```

```json
{
  "Parent": "DamageEntityParent",
  "DamageCalculator": {
    "BaseDamage": {
      "Crystal_Light": 36
    }
  },
  "DamageEffects": {
    "Knockback": {
      "Type": "Force",
      "VelocityConfig": {
        "AirResistance": 0.97,
        "AirResistanceMax": 0.96,
        "GroundResistance": 0.94,
        "GroundResistanceMax": 0.3,
        "Threshold": 3.0,
        "Style": "Exp"
      },
      "Direction": {
        "X": 0.0,
        "Y": 3,
        "Z": -1
      },
      "Force": 20,
      "VelocityType": "Set"
    },
    "WorldParticles": [
      {
        "SystemId": "Impact_Ice",
        "Scale": 1
      },
      {
        "SystemId": "IceBall_Explosion",
        "Scale": 1
      }
    ],
    "WorldSoundEventId": "SFX_Ice_Ball_Death",
    "EntityStatsOnHit": [
      {
        "EntityStatId": "SignatureEnergy",
        "Amount": 10
      }
    ]
  }
}
```

### Geração de SignatureEnergy

O array `EntityStatsOnHit` é a chave para o ciclo de progressão da espada. Cada acerto de raio concede **+5** de SignatureEnergy, e cada acerto de orbe concede **+10**. Quando a SignatureEnergy atinge 100%, o ataque especial fica disponível. Isso cria um ciclo de gameplay: use ataques carregados para acumular energia, depois libere o poderoso orbe.

---

## Passo 5: Criar o Item de Munição

Cargas de Luz são a munição consumida pelo ataque carregado. Elas são fabricadas na Bigorna de Cristal em lotes de 50.

```
Server/Item/Items/HytaleModdingManual/Weapon_Arrow_Crystal_Glow.json
```

```json
{
  "TranslationProperties": {
    "Name": "server.items.Weapon_Arrow_Crystal_Glow.name",
    "Description": "server.items.Weapon_Arrow_Crystal_Glow.description"
  },
  "Categories": [
    "Items.Weapons"
  ],
  "Quality": "Uncommon",
  "ItemLevel": 25,
  "PlayerAnimationsId": "Dagger",
  "Recipe": {
    "TimeSeconds": 5.0,
    "KnowledgeRequired": false,
    "Input": [
      {
        "ItemId": "Plant_Fruit_Enchanted",
        "Quantity": 1
      },
      {
        "ItemId": "Ore_Crystal_Glow",
        "Quantity": 1
      },
      {
        "ItemId": "Weapon_Arrow_Crude",
        "Quantity": 10
      }
    ],
    "OutputQuantity": 50,
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Categories": [
          "Crystal_Glow"
        ],
        "Id": "Armory_Crystal_Glow"
      }
    ]
  },
  "Model": "Items/Weapons/Arrow/Arrow.blockymodel",
  "Texture": "Items/Weapons/Arrow/Crude_Texture.png",
  "Icon": "Icons/ItemsGenerated/Weapon_Arrow_Crude.png",
  "MaxStack": 100,
  "Tags": {
    "Type": [
      "Weapon"
    ],
    "Family": [
      "Arrow"
    ]
  },
  "Weapon": {},
  "Light": {
    "Radius": 1,
    "Color": "#88ccff"
  },
  "ItemSoundSetId": "ISS_Weapons_Arrows"
}
```

![Interface da Bigorna de Cristal mostrando a receita de Carga de Luz — 1 Fruta Encantada + 1 Brilho de Cristal + 10 Flechas Rústicas = 50 Cargas de Luz](/hytale-modding-docs/images/tutorials/projectile-weapons/crystal-anvil-bench.png)

Pontos importantes:
- `OutputQuantity: 50` produz 50 cargas por fabricação — importante para itens de munição que são consumidos rapidamente
- Sem `Interactions` ou `InteractionVars` — este item é apenas munição, não uma arma que se pode brandir
- O objeto vazio `Weapon: {}` é necessário para que o item apareça nas categorias de armas
- `MaxStack: 100` permite carregar uma quantidade razoável

---

## Passo 6: Criar as Interações de Disparo

Estas são interações simples `Type: "Projectile"` que disparam cada projétil. Elas devem ser **arquivos nomeados**, não inline — o Hytale valida interações por ID de asset e interações de projétil inline podem falhar na validação.

### Disparo do Raio

```
Server/Item/Interactions/HytaleModdingManual/Crystal_Sword_Shoot_Bolt.json
```

```json
{
  "Type": "Projectile",
  "Config": "Projectile_Config_Crystal_Light_Bolt",
  "Next": {
    "Type": "Simple",
    "RunTime": 0.2
  }
}
```

### Disparo do Orbe

```
Server/Item/Interactions/HytaleModdingManual/Crystal_Sword_Shoot_Orb.json
```

```json
{
  "Type": "Projectile",
  "Config": "Projectile_Config_Crystal_Light_Orb",
  "Next": {
    "Type": "Simple",
    "RunTime": 0.2
  }
}
```

O campo `Config` referencia o ProjectileConfig pelo nome do arquivo (sem `.json`). O bloco `Next` adiciona um curto cooldown após o disparo.

:::caution[Arquivos Nomeados São Obrigatórios]
Sempre crie interações de projétil como arquivos nomeados separados. Colocar `Type: "Projectile"` inline dentro de um bloco Serial ou Parallel pode causar erros de validação de assets como `Failed to validate asset: **YourInteraction_Next_Interactions_0`.
:::

---

## Passo 7: Criar a Interação de Carregamento

A interação de carregamento exige que o jogador segure o botão de ataque por 1 segundo antes que o ataque carregado seja ativado.

```
Server/Item/Interactions/HytaleModdingManual/Crystal_Sword_Charge.json
```

```json
{
  "Type": "Charging",
  "AllowIndefiniteHold": false,
  "DisplayProgress": true,
  "HorizontalSpeedMultiplier": 0.5,
  "Next": {
    "0": "Weapon_Sword_Primary_Thrust",
    "1.0": "Crystal_Sword_Charged_Entry"
  }
}
```

| Campo | Finalidade |
|-------|------------|
| `AllowIndefiniteHold` | `false` significa disparo automático quando o maior limiar é atingido |
| `DisplayProgress` | Mostra a barra de carregamento acima da barra de atalhos |
| `HorizontalSpeedMultiplier` | Reduz a velocidade de movimento durante o carregamento (0.5 = metade da velocidade) |
| `Next` | Mapeia limiares de carregamento (em segundos) para interações |

Os limiares funcionam como "maior atingido":
- **Soltar antes de 1.0s** → executa `"0"` → investida vanilla normal (sem consumo de munição)
- **Segurar por 1.0s** → disparo automático `"1.0"` → entrada carregada com projétil

---

## Passo 8: Criar a Entrada Carregada

Este é o núcleo do ataque carregado. Ele verifica a munição, consome-a, reproduz a animação de investida e dispara o raio.

```
Server/Item/Interactions/HytaleModdingManual/Crystal_Sword_Charged_Entry.json
```

```json
{
  "Type": "ModifyInventory",
  "ItemToRemove": {
    "Id": "Weapon_Arrow_Crystal_Glow",
    "Quantity": 1
  },
  "AdjustHeldItemDurability": -0.3,
  "Next": {
    "Type": "Parallel",
    "Interactions": [
      {
        "Interactions": [
          "Weapon_Sword_Primary_Thrust"
        ]
      },
      {
        "Interactions": [
          {
            "Type": "Simple",
            "RunTime": 0.6
          },
          "Crystal_Sword_Shoot_Bolt"
        ]
      }
    ]
  },
  "Failed": "Weapon_Sword_Primary_Thrust"
}
```

### Como funciona

1. `ModifyInventory` verifica se o jogador tem 1 `Weapon_Arrow_Crystal_Glow` no inventário
2. **Se sim** (`Next`): remove a munição, reduz a durabilidade em 0.3, depois executa um `Parallel`:
   - **Ramo 1**: Reproduz a animação de investida vanilla (`Weapon_Sword_Primary_Thrust`)
   - **Ramo 2**: Aguarda 0.6 segundos (sincronizando o projétil com o final da animação de investida), depois dispara o raio
3. **Se não tiver munição** (`Failed`): executa uma investida normal sem projétil

O `Parallel` é essencial para a sincronia — ele permite que o projétil dispare no exato momento em que a animação de investida atinge a extensão máxima (0.6s), em vez de esperar a animação inteira terminar.

:::danger[Evite Recursão de Replace Var]
Nunca use `"Type": "Replace", "Var": "X"` dentro de uma interação que é ela mesma a sobrescrita da variável X. Isso cria um loop de recursão infinita onde a interação continua buscando sua própria sobrescrita. Sempre referencie interações concretas diretamente.
:::

---

## Passo 9: Criar o Ataque Especial

O ataque especial dispara um poderoso Orbe de Luz Cristalina quando a SignatureEnergy atinge 100%.

### Interação Raiz

```
Server/Item/RootInteractions/HytaleModdingManual/Crystal_Sword_Special.json
```

```json
{
  "Interactions": [
    "Crystal_Sword_Special"
  ]
}
```

### Interação Especial

```
Server/Item/Interactions/HytaleModdingManual/Crystal_Sword_Special.json
```

```json
{
  "Type": "StatsCondition",
  "Costs": {
    "SignatureEnergy": 100
  },
  "ValueType": "Percent",
  "Next": {
    "Type": "Serial",
    "Interactions": [
      {
        "Type": "Parallel",
        "Interactions": [
          {
            "Interactions": [
              {
                "Type": "Simple",
                "RunTime": 0.4,
                "Effects": {
                  "ItemPlayerAnimationsId": "Sword",
                  "ItemAnimationId": "Thrust",
                  "ClearAnimationOnFinish": true,
                  "Particles": [
                    {
                      "SystemId": "IceBall",
                      "TargetNodeName": "Handle",
                      "PositionOffset": {
                        "X": 1.0,
                        "Y": 0,
                        "Z": 0
                      }
                    }
                  ]
                }
              }
            ]
          },
          {
            "Interactions": [
              "Crystal_Sword_Shoot_Orb"
            ]
          }
        ]
      },
      {
        "Type": "ChangeStat",
        "StatModifiers": {
          "SignatureEnergy": -100
        },
        "ValueType": "Percent"
      }
    ]
  }
}
```

O fluxo:
1. `StatsCondition` verifica se a SignatureEnergy está em 100% — se não, nada acontece
2. `Parallel` executa a animação de investida (com partículas de IceBall na lâmina) junto com o projétil de orbe
3. `ChangeStat` drena toda a SignatureEnergy após o ataque

---

## Passo 10: Conectar Tudo à Espada

Atualize `Weapon_Sword_Crystal_Glow.json` para conectar todos os novos sistemas. As mudanças principais estão em `Interactions`, `InteractionVars` e `Weapon`:

```json {33-36,74-91,128-140}
{
  "Parent": "Template_Weapon_Sword",
  "Interactions": {
    "Primary": "Root_Weapon_Sword_Primary",
    "Secondary": "Root_Weapon_Sword_Secondary_Guard",
    "Ability1": "Crystal_Sword_Special"
  },
  "InteractionVars": {
    "Thrust_Damage": {
      "Interactions": [
        {
          "Parent": "Weapon_Sword_Primary_Thrust_Damage",
          "DamageCalculator": {
            "BaseDamage": {
              "Physical": 20,
              "Crystal_Light": 12
            }
          }
        }
      ]
    },
    "Thrust_Stamina": {
      "Interactions": [
        "Crystal_Sword_Charge"
      ]
    }
  },
  "Weapon": {
    "EntityStatsToClear": [
      "SignatureEnergy"
    ],
    "StatModifiers": {
      "SignatureEnergy": [
        {
          "Amount": 20,
          "CalculationType": "Additive"
        }
      ]
    }
  },
  "ItemAppearanceConditions": {
    "SignatureEnergy": [
      {
        "Condition": [100, 100],
        "ConditionValueType": "Percent",
        "Particles": [
          {
            "SystemId": "Sword_Signature_Ready",
            "TargetNodeName": "Handle",
            "PositionOffset": { "X": 0.8 },
            "TargetEntityPart": "PrimaryItem"
          }
        ]
      }
    ]
  }
}
```

### O que cada seção faz

**`Interactions`** — Vincula botões de ataque a cadeias de interação:
- `Primary` usa o primário vanilla da espada (`Root_Weapon_Sword_Primary`) — isso preserva o combo completo de golpes
- `Ability1` vincula ao nosso ataque especial personalizado

**`InteractionVars`** — Sobrescreve partes específicas da cadeia vanilla sem substituí-la:
- `Thrust_Damage` adiciona dano Crystal_Light à investida
- `Thrust_Stamina` substitui a verificação de estamina pela nossa interação de carregamento — é assim que o ataque de projétil carregado se conecta ao combo existente da espada

**`Weapon`** — Configura a SignatureEnergy:
- `StatModifiers` adiciona 20 de SignatureEnergy máxima quando equipado
- `EntityStatsToClear` reseta a energia quando a arma é desequipada

**`ItemAppearanceConditions`** — Mostra partículas brilhantes na espada quando a SignatureEnergy atinge 100%, sinalizando que o ataque especial está pronto.

---

## Passo 11: Testar No Jogo

1. Copie a pasta `CreateACraftingBench/` para `%APPDATA%/Hytale/UserData/Mods/`

2. Certifique-se de que os mods **CreateACustomBlock** e **CustomTreesAndSaplings** também estejam instalados (dependências necessárias)

3. Inicie o Hytale e fabrique Cargas de Luz na Bigorna de Cristal

4. Teste o ataque carregado:
   - Equipe a Espada de Cristal com Cargas de Luz no seu inventário
   - Segure o ataque primário — a barra de carregamento deve aparecer
   - Solte antes de 1s → investida normal (sem consumo de munição)
   - Segure por 1s → animação de investida + raio de cristal dispara da ponta da espada

5. Teste o ataque especial:
   - Acerte inimigos com raios carregados para acumular SignatureEnergy (+5 por acerto de raio)
   - Quando a espada brilhar (100% de energia), pressione Habilidade1
   - Um grande Orbe de Luz Cristalina deve disparar com efeito de explosão

**Erros comuns e correções:**

| Erro | Causa | Correção |
|------|-------|----------|
| `Failed to validate asset` | Interação `Type: "Projectile"` inline | Extraia para um arquivo nomeado |
| Projétil sai da cabeça | `SpawnOffset` não definido | Adicione `SpawnOffset` com `Z: 1.5` para mover para frente |
| Munição consumida sem projétil | `RunTime` em um `Type: "Projectile"` | Use `Next: { "Type": "Simple", "RunTime": 0.2 }` em vez disso |
| Disparo rápido infinito | `Replace Var` apontando para sua própria sobrescrita | Referencie interações diretamente, nunca autorreferencie |
| Barra de carregamento não visível | `DisplayProgress` ausente | Defina `"DisplayProgress": true` na interação de Carregamento |
| Especial nunca ativa | Sem `EntityStatsOnHit` no dano | Adicione `EntityStatsOnHit` com quantidade de `SignatureEnergy` nas interações de dano |

---

## Resumo da Estrutura de Arquivos

```
CreateACraftingBench/
  Server/
    Entity/Damage/
      Crystal_Light.json
    Projectiles/
      Crystal_Light_Bolt.json
      Crystal_Light_Orb.json
    ProjectileConfigs/HytaleModdingManual/
      Projectile_Config_Crystal_Light_Bolt.json
      Projectile_Config_Crystal_Light_Orb.json
    Item/
      Interactions/HytaleModdingManual/
        Crystal_Light_Bolt_Damage.json
        Crystal_Light_Orb_Damage.json
        Crystal_Sword_Charge.json
        Crystal_Sword_Charged_Entry.json
        Crystal_Sword_Shoot_Bolt.json
        Crystal_Sword_Shoot_Orb.json
        Crystal_Sword_Special.json
      RootInteractions/HytaleModdingManual/
        Crystal_Sword_Special.json
      Items/HytaleModdingManual/
        Weapon_Arrow_Crystal_Glow.json
        Weapon_Sword_Crystal_Glow.json (atualizado)
```

---

## Próximos Passos

- [Lojas de NPCs e Comércio](/hytale-modding-docs/pt-br/tutorials/intermediate/npc-shops-and-trading/) — venda Cargas de Luz em uma loja de mercador
- [Tabelas de Loot Personalizadas](/hytale-modding-docs/pt-br/tutorials/intermediate/custom-loot-tables/) — faça inimigos droparem Cargas de Luz
- [Referência de Configuração de Projétil](/hytale-modding-docs/pt-br/reference/combat/projectile-configs/) — referência completa do schema para todos os campos de configuração de projétil
