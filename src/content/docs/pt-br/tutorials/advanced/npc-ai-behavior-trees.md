---
title: Árvores de Comportamento de IA de NPCs
description: Aprofundamento na configuração de IA de NPCs usando condições de DecisionMaking, Combat Action Evaluators, prioridades de comportamento, ações de combate e condições de fuga.
---

## Objetivo

Construir um NPC personalizado chamado **Ironclad Sentinel** (Sentinela Blindado) com IA complexa que alterna entre combate corpo a corpo e à distância, se cura quando está com pouca vida, chama aliados por ajuda e foge quando criticamente ferido. Você configurará condições de Decision Making, um Combat Action Evaluator (CAE) e os conectará a um papel de NPC com comportamento de combate multi-estado.

## Pré-requisitos

- Uma pasta de mod com um `manifest.json` válido (veja [Configure Seu Ambiente de Desenvolvimento](/hytale-modding-docs/tutorials/beginner/setup-dev-environment))
- Entendimento de papéis e templates de NPC (veja [Papéis de NPC](/hytale-modding-docs/reference/npc-system/npc-roles) e [Templates de NPC](/hytale-modding-docs/reference/npc-system/npc-templates))
- Familiaridade com o sistema de condições (veja [Tomada de Decisão de NPC](/hytale-modding-docs/reference/npc-system/npc-decision-making))
- Entendimento de avaliadores de combate (veja [Balanceamento de Combate de NPC](/hytale-modding-docs/reference/npc-system/npc-combat-balancing))

---

## Como a IA de NPC Funciona

A IA de NPC do Hytale usa um sistema de decisão baseado em utilidade. A cada tick, a IA avalia ações disponíveis pontuando-as através de condições. A ação com a maior pontuação de utilidade acima de um limite mínimo é executada. Isso cria comportamento emergente e sensível ao contexto sem sequências programadas.

### Visão Geral da Arquitetura

```
NPC Role
├── Instructions (árvore de comportamento: estados Idle, Alert, Combat)
├── Sensors (visão, audição, detecção absoluta)
└── Combat Action Evaluator (CAE)
    ├── RunConditions (o avaliador deve executar neste tick?)
    ├── AvailableActions (ações pontuadas: corpo a corpo, à distância, cura, fuga)
    │   └── Conditions (pontuação por ação: distância, vida, cooldown)
    └── ActionSets (grupos de ações ativos por sub-estado)
```

### Conceitos Principais

| Conceito | Descrição |
|----------|-----------|
| **Condition** | Uma função de pontuação que mapeia um atributo do jogo para uma pontuação de utilidade de 0-1 usando uma curva de resposta |
| **Response Curve** | Função matemática que molda como valores brutos são mapeados para pontuações: Linear, Logistic, Switch |
| **Action** | Um comportamento de combate nomeado com condições, intervalos de distância e referências de habilidade |
| **Action Set** | Um grupo nomeado de ações e ataques básicos ativos durante um sub-estado de combate |
| **Sub-State** | Um modo de combate entre o qual o NPC pode alternar (Default, Ranged, Healing, etc.) |

---

## Passo 1: Entendendo Tipos de Condição

Condições são os blocos de construção das decisões de IA. Cada condição lê um valor do jogo e o mapeia para uma pontuação de 0-1 usando uma curva. Múltiplas condições em uma ação são multiplicadas juntas para produzir a pontuação final de utilidade.

### Referência de tipos de condição

| Tipo | O que lê | Uso comum |
|------|----------|-----------|
| `OwnStatPercent` | Atributo próprio do NPC como % do máximo | Curar quando a vida está baixa |
| `TargetStatPercent` | Atributo do alvo como % do máximo | Focar alvos fracos |
| `TargetDistance` | Distância ao alvo atual em blocos | Escolher corpo a corpo vs à distância |
| `TimeSinceLastUsed` | Segundos desde que esta ação foi usada pela última vez | Ritmo de cooldown |
| `Randomiser` | Valor aleatório entre min e max | Adicionar imprevisibilidade |

### Tipos de curva

A curva transforma um valor bruto em uma pontuação de 0-1:

| Curva | Forma | Caso de uso |
|-------|-------|-------------|
| `"Linear"` | Linha reta, 0 a 1 | Pontuação aumenta proporcionalmente com o valor |
| `"ReverseLinear"` | Linha reta, 1 a 0 | Pontuação mais alta quando o valor é mais baixo (curar quando ferido) |
| `"SimpleLogistic"` | Curva S ascendente | Pontuação salta acentuadamente no intervalo médio (preferir quando perto) |
| `"SimpleDescendingLogistic"` | Curva S descendente | Pontuação cai acentuadamente (evitar quando perto) |
| `Switch` com `SwitchPoint` | Alternância binária 0/1 | Portão rígido: só pontua 1 após o limite |

### Como pontuações se combinam

Quando uma ação tem múltiplas condições, o engine multiplica todas as pontuações juntas. Isso significa:

- Qualquer condição pontuando 0 desabilita a ação inteiramente
- Todas as condições devem pontuar razoavelmente alto para a ação vencer
- Um `Randomiser` com `MinValue: 0.9, MaxValue: 1.0` adiciona leve imprevisibilidade sem dominar a pontuação

**Exemplo**: Uma ação com condições `[OwnStatPercent(Health, ReverseLinear), TimeSinceLastUsed(Linear, 0-5)]` pontua mais alto quando o NPC está ferido E a ação não foi usada recentemente. Se a vida está em 100%, `ReverseLinear` retorna 0, tornando a ação impossível independentemente do cooldown.

---

## Passo 2: Criar Arquivos de Condição de Decision Making

Arquivos de condição independentes em `DecisionMaking/Conditions/` podem ser referenciados por múltiplos CAEs. Crie condições reutilizáveis para padrões comuns.

Crie `YourMod/Assets/Server/NPC/DecisionMaking/Conditions/Condition_LowHealth.json`:

```json
{
  "Type": "OwnStatPercent",
  "Stat": "Health",
  "Curve": "ReverseLinear"
}
```

Esta condição pontua mais alto (próximo de 1.0) quando o NPC tem vida muito baixa, e mais baixo (próximo de 0.0) com vida cheia. Qualquer ação usando esta condição será fortemente preferida quando o NPC estiver ferido.

Crie `YourMod/Assets/Server/NPC/DecisionMaking/Conditions/Condition_TargetClose.json`:

```json
{
  "Type": "TargetDistance",
  "Curve": {
    "ResponseCurve": "SimpleDescendingLogistic",
    "XRange": [0, 12]
  }
}
```

Pontua alto quando o alvo está perto (dentro de ~4 blocos) e cai rapidamente conforme a distância se aproxima de 12 blocos. A curva logística cria uma transição acentuada em vez de gradual.

Crie `YourMod/Assets/Server/NPC/DecisionMaking/Conditions/Condition_TargetFar.json`:

```json
{
  "Type": "TargetDistance",
  "Curve": {
    "ResponseCurve": "SimpleLogistic",
    "XRange": [0, 15]
  }
}
```

O oposto de `Condition_TargetClose` — pontua alto quando o alvo está longe, útil para disparar ataques à distância.

---

## Passo 3: Criar o Combat Action Evaluator

O CAE é o núcleo da inteligência de combate do NPC. Ele define todas as ações de combate disponíveis e as condições sob as quais cada uma é preferida.

Crie `YourMod/Assets/Server/NPC/Balancing/Intelligent/CAE_Ironclad_Sentinel.json`:

```json
{
  "Type": "CombatActionEvaluator",
  "TargetMemoryDuration": 8,
  "CombatActionEvaluator": {
    "RunConditions": [
      {
        "Type": "TimeSinceLastUsed",
        "Curve": {
          "ResponseCurve": "Linear",
          "XRange": [0, 3]
        }
      },
      {
        "Type": "Randomiser",
        "MinValue": 0.9,
        "MaxValue": 1
      }
    ],
    "MinRunUtility": 0.5,
    "MinActionUtility": 0.01,
    "AvailableActions": {
      "SelectTarget": {
        "Type": "SelectBasicAttackTarget",
        "Description": "Select the best target for basic attacks",
        "Conditions": [
          {
            "Type": "TargetDistance",
            "Curve": {
              "ResponseCurve": "SimpleDescendingLogistic",
              "XRange": [0, 20]
            }
          }
        ]
      },
      "MeleeSwing": {
        "Type": "Ability",
        "Description": "Heavy melee swing when target is close",
        "WeaponSlot": 0,
        "SubState": "Melee",
        "Ability": "Sentinel_MeleeSwing",
        "Target": "Hostile",
        "AttackDistanceRange": [2.5, 2.5],
        "PostExecuteDistanceRange": [2.5, 2.5],
        "WeightCoefficient": 1.2,
        "Conditions": [
          {
            "Type": "TargetDistance",
            "Curve": {
              "ResponseCurve": "SimpleDescendingLogistic",
              "XRange": [0, 5]
            }
          },
          {
            "Type": "TimeSinceLastUsed",
            "Curve": {
              "ResponseCurve": "Linear",
              "XRange": [0, 1.5]
            }
          }
        ]
      },
      "ShieldBash": {
        "Type": "Ability",
        "Description": "Shield bash to stagger close targets",
        "WeaponSlot": 1,
        "SubState": "Melee",
        "Ability": "Sentinel_ShieldBash",
        "Target": "Hostile",
        "AttackDistanceRange": [2, 2],
        "PostExecuteDistanceRange": [3, 3],
        "WeightCoefficient": 1.0,
        "ChargeFor": 0.5,
        "Conditions": [
          {
            "Type": "TargetDistance",
            "Curve": {
              "ResponseCurve": "SimpleDescendingLogistic",
              "XRange": [0, 4]
            }
          },
          {
            "Type": "TimeSinceLastUsed",
            "Curve": {
              "Type": "Switch",
              "SwitchPoint": 5
            }
          }
        ]
      },
      "RangedThrow": {
        "Type": "Ability",
        "Description": "Throw projectile when target is at range",
        "WeaponSlot": 0,
        "SubState": "Ranged",
        "Ability": "Sentinel_SpearThrow",
        "Target": "Hostile",
        "AttackDistanceRange": [12, 12],
        "PostExecuteDistanceRange": [2.5, 2.5],
        "WeightCoefficient": 0.9,
        "Conditions": [
          {
            "Type": "TargetDistance",
            "Curve": {
              "ResponseCurve": "SimpleLogistic",
              "XRange": [0, 15]
            }
          },
          {
            "Type": "TimeSinceLastUsed",
            "Curve": {
              "ResponseCurve": "Linear",
              "XRange": [0, 3]
            }
          }
        ]
      },
      "HealSelf": {
        "Type": "Ability",
        "Description": "Heal when health is low",
        "Ability": "Sentinel_HealSelf",
        "Target": "Self",
        "WeightCoefficient": 1.5,
        "Conditions": [
          {
            "Type": "OwnStatPercent",
            "Stat": "Health",
            "Curve": "ReverseLinear"
          },
          {
            "Type": "TimeSinceLastUsed",
            "Curve": {
              "Type": "Switch",
              "SwitchPoint": 10
            }
          }
        ]
      },
      "CallForHelp": {
        "Type": "Ability",
        "Description": "Call nearby allies when hurt",
        "Ability": "Sentinel_CallForHelp",
        "Target": "Self",
        "WeightCoefficient": 1.3,
        "Conditions": [
          {
            "Type": "OwnStatPercent",
            "Stat": "Health",
            "Curve": "ReverseLinear"
          },
          {
            "Type": "TimeSinceLastUsed",
            "Curve": {
              "Type": "Switch",
              "SwitchPoint": 15
            }
          },
          {
            "Type": "Randomiser",
            "MinValue": 0.6,
            "MaxValue": 1
          }
        ]
      }
    },
    "ActionSets": {
      "Default": {
        "BasicAttacks": {
          "Attacks": ["Sentinel_MeleeSwing"],
          "Randomise": false,
          "MaxRange": 2.5,
          "Timeout": 0.5,
          "CooldownRange": [0.5, 1.0]
        },
        "Actions": [
          "SelectTarget",
          "MeleeSwing",
          "ShieldBash",
          "RangedThrow",
          "HealSelf",
          "CallForHelp"
        ]
      },
      "Melee": {
        "BasicAttacks": {
          "Attacks": ["Sentinel_MeleeSwing", "Sentinel_ShieldBash"],
          "Randomise": true,
          "MaxRange": 2.5,
          "Timeout": 0.5,
          "CooldownRange": [0.3, 0.8]
        },
        "Actions": [
          "SelectTarget",
          "ShieldBash",
          "RangedThrow",
          "HealSelf",
          "CallForHelp"
        ]
      },
      "Ranged": {
        "BasicAttacks": {
          "Attacks": ["Sentinel_SpearThrow"],
          "Randomise": false,
          "MaxRange": 12,
          "Timeout": 1.0,
          "CooldownRange": [1.5, 3.0]
        },
        "Actions": [
          "SelectTarget",
          "MeleeSwing",
          "HealSelf"
        ]
      }
    }
  }
}
```

### Detalhamento do design do CAE

**RunConditions** controlam com que frequência o avaliador dispara:
- `TimeSinceLastUsed` com uma curva Linear de 3 segundos significa que o avaliador pontua mais alto quanto mais tempo passou desde a última execução
- `Randomiser` em 0.9-1.0 adiciona 10% de variância para que o NPC não aja em intervalos perfeitamente previsíveis
- `MinRunUtility: 0.5` significa que ambas condições devem pontuar acima de ~0.7 cada (0.7 * 0.7 = 0.49, logo abaixo do limite) antes do avaliador disparar

**WeightCoefficient** multiplica a pontuação final de utilidade:
- `HealSelf` em 1.5 o torna fortemente preferido quando as condições são atendidas
- `CallForHelp` em 1.3 lhe dá prioridade sobre ataques básicos
- `RangedThrow` em 0.9 o torna levemente menos preferido que corpo a corpo quando ambos são viáveis
- `MeleeSwing` em 1.2 dá ao corpo a corpo uma leve vantagem sobre o padrão

**Alternância de sub-estado**: Quando `MeleeSwing` dispara, ele ativa o sub-estado `Melee`, que tem cooldowns mais rápidos e ataques básicos aleatorizados entre swing e bash. Quando `RangedThrow` dispara, ele muda para `Ranged`, que tem apenas o arremesso de lança como ataque básico com cooldowns mais longos.

**Análise da lógica de HealSelf**:
- `OwnStatPercent(Health, ReverseLinear)`: Em 50% de HP pontua 0.5, em 20% de HP pontua 0.8
- `TimeSinceLastUsed(Switch, 10)`: Portão rígido — não pode curar mais frequentemente que a cada 10 segundos
- `WeightCoefficient: 1.5`: Multiplicado pelas pontuações das condições, isso supera a maioria das ações de combate quando a vida está abaixo de ~40%

---

## Passo 4: Criar o Papel de NPC

Conecte o CAE a um papel de NPC que usa a base `Template_Intelligent`, que fornece IA de combate com reconhecimento de facção com suporte a pedido de ajuda.

Crie `YourMod/Assets/Server/NPC/Roles/MyMod/Ironclad_Sentinel.json`:

```json
{
  "Type": "Variant",
  "Reference": "Template_Intelligent",
  "Modify": {
    "Appearance": "Skeleton_Warrior",
    "DropList": "Drop_Ironclad_Sentinel",
    "MaxHealth": 180,
    "MaxSpeed": 5,
    "ViewRange": 20,
    "ViewSector": 220,
    "HearingRange": 16,
    "AlertedRange": 28,
    "DefaultPlayerAttitude": "Hostile",
    "DefaultNPCAttitude": "Neutral",
    "KnockbackScale": 0.6,
    "FlockArray": ["Ironclad_Sentinel"],
    "IsMemory": true,
    "MemoriesCategory": "Undead",
    "MemoriesNameOverride": "Ironclad Sentinel",
    "NameTranslationKey": {
      "Compute": "NameTranslationKey"
    }
  },
  "Parameters": {
    "NameTranslationKey": {
      "Value": "server.npcRoles.Ironclad_Sentinel.name",
      "Description": "Translation key for NPC name display"
    }
  }
}
```

### Notas de design do papel

| Campo | Valor | Justificativa |
|-------|-------|---------------|
| `MaxHealth: 180` | Maior que o Goblin Scrapper vanilla (~80) | Durabilidade de nível de chefe para um guardião de dungeon |
| `ViewRange: 20` | Alcance de visão estendido | Detecta intrusos de mais longe |
| `ViewSector: 220` | Campo de visão amplo | Mais difícil de se esgueirar por trás |
| `AlertedRange: 28` | Alcance de alerta muito longo | Uma vez alertado, rastreia jogadores por salas grandes |
| `KnockbackScale: 0.6` | Knockback reduzido | NPC com armadura pesada resiste a ser empurrado |
| `FlockArray` | Auto-referenciando | Sentinelas coordenam como grupo |

A base `Template_Intelligent` fornece:
- `ChanceToBeAlertedWhenReceivingCallForHelp: 70` — 70% de chance de Sentinelas próximos entrarem em combate quando um pede ajuda
- Máquina de estados completa de IA de combate: Idle, Alert, Combat, Flee
- Atitudes com reconhecimento de facção para interações NPC-para-NPC

---

## Passo 5: Configurar Comportamento de Fuga

O Sentinela deve recuar quando criticamente ferido. O comportamento de fuga é controlado por campos no papel de NPC que o template lê.

Adicione parâmetros de fuga ao bloco `Modify` do seu papel:

```json
{
  "Type": "Variant",
  "Reference": "Template_Intelligent",
  "Modify": {
    "Appearance": "Skeleton_Warrior",
    "DropList": "Drop_Ironclad_Sentinel",
    "MaxHealth": 180,
    "MaxSpeed": 5,
    "ViewRange": 20,
    "ViewSector": 220,
    "HearingRange": 16,
    "AlertedRange": 28,
    "DefaultPlayerAttitude": "Hostile",
    "DefaultNPCAttitude": "Neutral",
    "KnockbackScale": 0.6,
    "FlockArray": ["Ironclad_Sentinel"],
    "FleeRange": 20,
    "FleeHealthThreshold": 0.15,
    "FleeSpeed": 7,
    "FleeIfNotThreatened": false,
    "IsMemory": true,
    "MemoriesCategory": "Undead",
    "MemoriesNameOverride": "Ironclad Sentinel",
    "NameTranslationKey": {
      "Compute": "NameTranslationKey"
    }
  },
  "Parameters": {
    "NameTranslationKey": {
      "Value": "server.npcRoles.Ironclad_Sentinel.name",
      "Description": "Translation key for NPC name display"
    }
  }
}
```

### Campos de fuga explicados

| Campo | Propósito |
|-------|-----------|
| `FleeRange` | Distância que o NPC tenta manter das ameaças ao fugir |
| `FleeHealthThreshold` | Porcentagem de vida abaixo da qual o NPC começa a fugir (0.15 = 15%) |
| `FleeSpeed` | Velocidade de movimento durante a fuga (mais rápido que `MaxSpeed: 5` normal) |
| `FleeIfNotThreatened` | Se `true`, o NPC foge mesmo de alvos não ameaçadores. `false` significa que ele só foge de entidades que considera perigosas |

Com 15% de vida (27 HP de 180), o Sentinela muda para o modo de fuga, correndo na velocidade 7 enquanto tenta manter 20 blocos de distância. Isso dá aos jogadores uma janela para terminar a luta antes do Sentinela escapar.

---

## Passo 6: Adicionar Chaves de Tradução e Tabela de Drop

Adicione a `YourMod/Assets/Languages/en-US.lang`:

```
server.npcRoles.Ironclad_Sentinel.name=Ironclad Sentinel
```

Crie `YourMod/Assets/Server/Drops/NPCs/Intelligent/Drop_Ironclad_Sentinel.json`:

```json
{
  "Container": {
    "Type": "Multiple",
    "Containers": [
      {
        "Type": "Choice",
        "Weight": 100,
        "Containers": [
          {
            "Type": "Single",
            "Item": {
              "ItemId": "Ingredient_Bone",
              "QuantityMin": 2,
              "QuantityMax": 4
            }
          }
        ]
      },
      {
        "Type": "Choice",
        "Containers": [
          {
            "Type": "Single",
            "Weight": 20,
            "Item": {
              "ItemId": "Ingredient_Hide_Heavy",
              "QuantityMin": 1,
              "QuantityMax": 2
            }
          },
          {
            "Type": "Empty",
            "Weight": 80
          }
        ]
      },
      {
        "Type": "Choice",
        "Containers": [
          {
            "Type": "Single",
            "Weight": 5,
            "Item": {
              "ItemId": "Weapon_Sword_Iron",
              "QuantityMin": 1,
              "QuantityMax": 1
            }
          },
          {
            "Type": "Empty",
            "Weight": 95
          }
        ]
      }
    ]
  }
}
```

---

## Passo 7: Testar a IA

1. Coloque sua pasta de mod no diretório de mods do servidor.
2. Inicie o servidor e gere um Ironclad Sentinel usando o spawner de NPC do desenvolvedor.
3. Observe o comportamento idle — o Sentinela deve ficar de guarda e escanear seus arredores.
4. Aproxime-se a 20 blocos e confirme que o Sentinela fica em alerta.
5. Entre em combate e teste os seguintes comportamentos:

| Teste | Comportamento esperado |
|-------|----------------------|
| Ficar em alcance corpo a corpo (< 3 blocos) | Sentinela usa MeleeSwing e ShieldBash |
| Ficar à distância (8-12 blocos) | Sentinela muda para RangedThrow |
| Causar dano no Sentinela abaixo de 50% HP | Ação HealSelf ativa (se cooldown de 10s já passou) |
| Causar dano no Sentinela abaixo de 15% HP | Sentinela foge na velocidade 7 |
| Gerar 2 Sentinelas, atacar um | Sentinela atacado pede ajuda, segundo tem 70% de chance de participar |
| Esperar após Sentinela fugir | Sentinela mantém 20 blocos de distância |

### Solução de Problemas

| Problema | Causa | Correção |
|----------|-------|----------|
| NPC nunca ataca | `MinActionUtility` muito alto | Reduza `MinActionUtility` para `0.001` |
| NPC sempre usa o mesmo ataque | Desequilíbrio de `WeightCoefficient` | Ajuste coeficientes para que fiquem mais próximos em valor |
| Cura nunca dispara | Switch point muito alto ou limite de vida incompatível | Reduza `SwitchPoint` na condição de cooldown de cura |
| NPC não foge | `FleeHealthThreshold` muito baixo | Aumente para 0.25 para testes |
| Pedido de ajuda não funciona | NPCs próximos não estão no mesmo flock | Certifique-se de que `FlockArray` inclui o ID do papel do NPC auxiliar |
| IA parece muito lenta | `RunConditions` pontuando muito baixo | Reduza `XRange` em `TimeSinceLastUsed` para fazer o avaliador disparar mais frequentemente |

---

## Próximos Passos

- [Sistema de Combate Personalizado](/hytale-modding-docs/tutorials/advanced/custom-combat-system) — adicione tipos de dano personalizados aos ataques do Sentinela
- [Dungeons Personalizadas](/hytale-modding-docs/tutorials/advanced/custom-dungeons) — gere Sentinelas dentro de instâncias de dungeon
- [Tomada de Decisão de NPC](/hytale-modding-docs/reference/npc-system/npc-decision-making) — referência completa de tipos de condição
- [Balanceamento de Combate de NPC](/hytale-modding-docs/reference/npc-system/npc-combat-balancing) — referência do schema CAE
- [Curvas de Resposta](/hytale-modding-docs/reference/concepts/response-curves) — detalhes matemáticos das formas de curva
