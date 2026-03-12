---
title: Regras de Spawn de NPCs Personalizadas
description: Tutorial passo a passo para criar regras de spawn de NPCs personalizadas com ambientes, faixas de horário, fases da lua e condições de bioma.
sidebar:
  order: 6
---

## Objetivo

Criar regras de spawn avançadas que controlam onde, quando e como seus NPCs aparecem no mundo. Você construirá arquivos de spawn para criaturas diurnas de floresta, inimigos noturnos do vazio com modificadores de fase lunar e predadores específicos de zona com restrições de nível de luz.

## O Que Você Vai Aprender

- Como arquivos de regras de spawn conectam ambientes a funções de NPC
- Como usar `DayTimeRange` para restrições de hora do dia
- Como `Weight` e `Flock` controlam frequência de spawn e tamanho do grupo
- Como `SpawnBlockSet` determina o tipo de superfície para spawning
- Como `MoonPhaseWeightModifiers`, `LightRanges` e `Despawn` criam comportamento avançado de spawn

## Pré-requisitos

- Uma pasta de mod com um `manifest.json` válido (veja [Configurar Seu Ambiente de Desenvolvimento](/hytale-modding-docs/pt-br/tutorials/beginner/setup-dev-environment))
- Pelo menos uma função de NPC personalizada (veja [Criar um NPC Personalizado](/hytale-modding-docs/pt-br/tutorials/beginner/create-an-npc))

---

## Visão Geral do Sistema de Spawn

As regras de spawn ficam em `Assets/Server/NPC/Spawn/World/` e são organizadas por zona. O engine lê cada arquivo JSON nesses diretórios e os mescla. Cada arquivo associa uma lista de ambientes (biomas) com uma lista de NPCs que podem spawnar lá.

```
Assets/Server/NPC/Spawn/World/
  Zone0/
  Zone1/
    Spawns_Zone1_Forests_Critter.json
    Spawns_Zone1_Forests_Predator.json
    Spawns_Zone1_Mountains_Animal.json
  Zone2/
  Zone3/
  Zone4/
  Void/
  Unique/
```

---

## Passo 1: Criar uma Regra de Spawn Diurna Básica

Este exemplo spawna criaturas nos biomas de floresta da Zona 1 durante o dia -- correspondendo ao padrão usado por arquivos vanilla como `Spawns_Zone1_Forests_Critter.json`.

Crie:

```
YourMod/Assets/Server/NPC/Spawn/World/Zone1/Spawns_Zone1_MyMod_Critter.json
```

```json
{
  "Environments": [
    "Env_Zone1_Forests",
    "Env_Zone1_Autumn",
    "Env_Zone1_Azure"
  ],
  "NPCs": [
    {
      "Weight": 4,
      "SpawnBlockSet": "Soil",
      "Id": "Mossbug",
      "Flock": "One_Or_Two"
    },
    {
      "Weight": 2,
      "SpawnBlockSet": "Birds",
      "Id": "Glowfly",
      "Flock": "Group_Small"
    }
  ],
  "DayTimeRange": [
    6,
    18
  ]
}
```

### Referência de campos

| Campo | Finalidade |
|-------|-----------|
| `Environments` | Array de IDs de ambiente ao qual este arquivo de spawn se aplica. O engine combina estes com o mapa de biomas do gerador de mundo |
| `NPCs` | Array de entradas de NPCs que podem spawnar nos ambientes listados |
| `NPCs[].Weight` | Probabilidade relativa de spawn. Valores mais altos significam mais comuns. Criaturas vanilla usam tipicamente 2-6 |
| `NPCs[].SpawnBlockSet` | Tipo de superfície para spawning: `"Soil"` (chão), `"Birds"` (ar), `"Water"` (aquático) |
| `NPCs[].Id` | ID da função do NPC -- corresponde ao nome do arquivo JSON da função sem `.json` |
| `NPCs[].Flock` | Tamanho do grupo. Valores string: `"One_Or_Two"`, `"Group_Small"`, `"Group_Large"` |
| `DayTimeRange` | `[início, fim]` horas (0-24) durante as quais o spawning está ativo. `[6, 18]` = 6h às 18h |

---

## Passo 2: Criar uma Regra de Spawn Noturna com Fases da Lua

Criaturas do vazio no Hytale usam configurações avançadas de spawn incluindo modificadores de peso por fase lunar e regras de despawn. Este padrão vem de arquivos em `Assets/Server/NPC/Spawn/World/Void/`.

Crie:

```
YourMod/Assets/Server/NPC/Spawn/World/Void/Spawns_MyMod_Night_Void.json
```

```json
{
  "Environments": [
    "Env_Zone1_Plains",
    "Env_Zone2_Savanna",
    "Env_Zone3_Tundra"
  ],
  "Despawn": {
    "DayTimeRange": [
      5,
      19
    ]
  },
  "MoonPhaseWeightModifiers": [
    0.5,
    1,
    1.5,
    1.5,
    1
  ],
  "NPCs": [
    {
      "Weight": 20,
      "SpawnBlockSet": "Soil",
      "Id": "Shadow_Crawler",
      "Flock": {
        "Size": [
          2,
          3
        ]
      }
    }
  ],
  "DayTimeRange": [
    19,
    5
  ],
  "LightRanges": {
    "Light": [
      0,
      8
    ]
  }
}
```

### Campos avançados de spawn

| Campo | Finalidade |
|-------|-----------|
| `Despawn.DayTimeRange` | `[início, fim]` horas durante as quais NPCs spawnados são forçadamente despawnados. Usado para remover criaturas noturnas ao amanhecer |
| `MoonPhaseWeightModifiers` | Array de multiplicadores aplicados a todos os valores de `Weight` baseados na fase lunar atual. Índice 0 = lua nova, índices maiores = luas mais cheias. Valores acima de 1.0 aumentam spawns; abaixo de 1.0 diminuem |
| `LightRanges.Light` | `[mín, máx]` faixa de nível de luz (0-15) requerida no local de spawn. `[0, 8]` significa que o NPC só spawna em áreas escuras |
| `Flock.Size` | Alternativa aos nomes de flock em string. Array `[mín, máx]` para tamanhos de grupo personalizados |

### DayTimeRange noturno

Quando `início > fim` (ex: `[19, 5]`), a faixa passa pela meia-noite. Isso significa que o spawning está ativo das 19h até as 5h.

---

## Passo 3: Criar um Spawn de Predador Específico de Zona

Predadores usam pesos mais altos e tipicamente spawnam sozinhos. Este padrão corresponde a `Spawns_Zone1_Forests_Predator.json`.

Crie:

```
YourMod/Assets/Server/NPC/Spawn/World/Zone1/Spawns_Zone1_MyMod_Predator.json
```

```json
{
  "Environments": [
    "Env_Zone1_Forests",
    "Env_Zone1_Autumn"
  ],
  "NPCs": [
    {
      "Weight": 5,
      "SpawnBlockSet": "Soil",
      "Id": "Thornbeast"
    },
    {
      "Weight": 3,
      "SpawnBlockSet": "Soil",
      "Id": "Venomfang",
      "Flock": "One_Or_Two"
    }
  ],
  "DayTimeRange": [
    6,
    18
  ]
}
```

Quando nenhum `Flock` é especificado (como com Thornbeast acima), o NPC spawna individualmente.

---

## Passo 4: Criar uma Regra de Spawn Aquática

Para criaturas aquáticas, use o conjunto de blocos de spawn `Water` e o campo `SpawnFluidTag`:

```
YourMod/Assets/Server/NPC/Spawn/World/Zone1/Spawns_Zone1_MyMod_Aquatic.json
```

```json
{
  "Environments": [
    "Env_Zone1_Forests",
    "Env_Zone1_Autumn"
  ],
  "NPCs": [
    {
      "Weight": 10,
      "SpawnBlockSet": "Water",
      "SpawnFluidTag": "Water",
      "Id": "Glowfish",
      "Flock": "Group_Small"
    }
  ],
  "DayTimeRange": [
    6,
    18
  ]
}
```

### SpawnFluidTag

O campo `SpawnFluidTag` restringe o spawning a blocos contendo um fluido específico. Use `"Water"` para spawns de água doce. Este campo é usado em arquivos vanilla como `Spawns_Portals_Oasis_Animal.json` para flamingos perto de água.

---

## IDs de Ambiente Disponíveis

Aqui estão IDs de ambiente comuns por zona:

| Zona | IDs de Ambiente |
|------|----------------|
| Zona 1 | `Env_Zone1_Plains`, `Env_Zone1_Forests`, `Env_Zone1_Autumn`, `Env_Zone1_Azure`, `Env_Zone1_Mountains_Critter` |
| Zona 2 | `Env_Zone2_Savanna`, `Env_Zone2_Desert` |
| Zona 3 | `Env_Zone3_Tundra` |
| Único | `Env_Portals_Oasis` |

Verifique o campo `Environments` nos arquivos de spawn vanilla em cada diretório de zona para a lista completa.

---

## Passo 5: Testar No Jogo

1. Coloque sua pasta de mod no diretório de mods do servidor.
2. Inicie o servidor e observe erros sobre IDs de NPC desconhecidos ou nomes de ambiente inválidos.
3. Use o gerador de NPCs do desenvolvedor para verificar se suas funções de NPC funcionam independentemente.
4. Viaje para o bioma apropriado durante a hora do dia correta.
5. Para spawns noturnos, espere o anoitecer e afaste-se de fontes de luz.
6. Verifique se os tamanhos de flock correspondem à sua configuração.
7. Para testes de fase lunar, avance o relógio do jogo por vários dias.

**Erros comuns e correções:**

| Erro | Causa | Correção |
|------|-------|----------|
| NPC nunca spawna naturalmente | ID de ambiente errado | Compare nomes de ambiente com arquivos de spawn vanilla na mesma zona |
| NPC spawna na hora errada | `DayTimeRange` invertido | Para noturno, use `[19, 5]` não `[5, 19]` |
| Muitos ou poucos spawns | `Weight` desbalanceado | Compare com pesos vanilla: criaturas usam 2-6, predadores usam 3-5 |
| NPC spawna no ar | `SpawnBlockSet` errado | Use `"Soil"` para criaturas terrestres, `"Birds"` apenas para NPCs voadores |
| Criaturas do vazio persistem ao amanhecer | `Despawn` ausente | Adicione `"Despawn": { "DayTimeRange": [5, 19] }` |

---

## Próximos Passos

- [Criar um NPC Personalizado](/hytale-modding-docs/pt-br/tutorials/beginner/create-an-npc) -- defina a função de NPC que suas regras de spawn referenciam
- [Tabelas de Loot Personalizadas](/hytale-modding-docs/pt-br/tutorials/intermediate/custom-loot-tables) -- configure o que seus NPCs spawnados dropam quando derrotados
- [Armas de Projétil](/hytale-modding-docs/pt-br/tutorials/intermediate/projectile-weapons) -- crie armas para combater seus predadores spawnados
