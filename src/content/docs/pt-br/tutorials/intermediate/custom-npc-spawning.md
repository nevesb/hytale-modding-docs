---
title: Regras de Spawn de NPCs Personalizados
description: Tutorial passo a passo para criar regras de spawn que fazem Slimes aparecerem em florestas Azure e um mercador Feran surgir em biomas Feran.
sidebar:
  order: 6
---

## Objetivo

Criar **regras de spawn** que fazem seus NPCs personalizados aparecerem naturalmente no mundo. Você fará o **Slime** do tutorial [Criar um NPC Personalizado](/hytale-modding-docs/pt-br/tutorials/beginner/create-an-npc/) surgir em florestas Azure, e o **Mercador Encantado Feran** do tutorial [Lojas e Comércio de NPCs](/hytale-modding-docs/pt-br/tutorials/intermediate/npc-shops-and-trading/) surgir em biomas Feran.

![Slime surgindo naturalmente em um bioma de floresta Azure](/hytale-modding-docs/images/tutorials/custom-npc-spawning/slime-azure-forest.png)

## O Que Você Vai Aprender

- Como arquivos de spawn do mundo controlam onde e quando NPCs aparecem em biomas
- Como `Environments` conectam regras de spawn a biomas específicos
- Como `Weight`, `Flock` e `DayTimeRange` controlam frequência de spawn, tamanho do grupo e horário
- Como `SpawnBlockSet` restringe NPCs a tipos específicos de superfície

## Pré-requisitos

- O mod do Slime NPC de [Criar um NPC Personalizado](/hytale-modding-docs/pt-br/tutorials/beginner/create-an-npc/)
- O mod do Mercador Encantado Feran de [Lojas e Comércio de NPCs](/hytale-modding-docs/pt-br/tutorials/intermediate/npc-shops-and-trading/)

**Repositório do mod complementar:** [hytale-mods-custom-npc-spawns](https://github.com/nevesb/hytale-mods-custom-npc-spawns)

---

## Visão Geral do Sistema de Spawn

Hytale usa **spawns do mundo** para fazer NPCs aparecerem naturalmente conforme os jogadores exploram. Os arquivos de spawn ficam em `Server/NPC/Spawn/World/` e são organizados por zona. O motor lê cada arquivo JSON no diretório de cada zona e os mescla. Cada arquivo associa uma lista de ambientes (biomas) com NPCs que podem surgir ali.

```
Server/NPC/Spawn/
  World/
    Zone0/          (Oceano)
    Zone1/          (Floresta Azure, Planícies, Montanhas)
    Zone2/          (Feran, Savana, Deserto)
    Zone3/          (Tundra)
    Void/           (Criaturas noturnas)
```

### IDs de Ambiente

Ambientes representam biomas. Cada zona possui diversas variantes de ambiente:

| Zona | Ambientes Comuns |
|------|-----------------|
| Zone 1 | `Env_Zone1_Forests`, `Env_Zone1_Azure`, `Env_Zone1_Autumn`, `Env_Zone1_Plains`, `Env_Zone1_Mountains_Critter` |
| Zone 2 | `Env_Zone2_Feran`, `Env_Zone2_Savanna`, `Env_Zone2_Desert`, `Env_Zone2_Oasis`, `Env_Zone2_Plateau` |
| Zone 3 | `Env_Zone3_Tundra` |

---

## Passo 1: Criar o Spawn do Slime no Mundo

Spawns do mundo fazem NPCs aparecerem naturalmente conforme o jogador explora. Predadores vanilla como Ursos e Aranhas usam este sistema para povoar florestas.

Aqui está o spawn de predadores de floresta vanilla como referência:

```json
// Vanilla: Spawns_Zone1_Forests_Predator.json
{
  "Environments": [
    "Env_Zone1_Forests",
    "Env_Zone1_Autumn",
    "Env_Zone1_Azure"
  ],
  "NPCs": [
    {
      "Weight": 5,
      "SpawnBlockSet": "Soil",
      "Id": "Bear_Grizzly"
    },
    {
      "Weight": 5,
      "SpawnBlockSet": "Soil",
      "Id": "Spider"
    }
  ],
  "DayTimeRange": [6, 18]
}
```

Agora crie um arquivo de spawn para Slimes em florestas Azure e padrão:

```
NPCSpawning/Server/NPC/Spawn/World/Zone1/Spawns_Zone1_Azure_Slime.json
```

```json
{
  "Environments": [
    "Env_Zone1_Azure",
    "Env_Zone1_Forests"
  ],
  "NPCs": [
    {
      "Weight": 15,
      "SpawnBlockSet": "Soil",
      "Id": "Slime",
      "Flock": "One_Or_Two"
    }
  ],
  "DayTimeRange": [
    6,
    18
  ]
}
```

### Detalhamento dos Campos

| Campo | Valor | Finalidade |
|-------|-------|------------|
| `Environments` | `["Env_Zone1_Azure", "Env_Zone1_Forests"]` | Slimes surgem em biomas de floresta Azure e floresta padrão |
| `Weight` | `15` | Frequência de spawn relativa a outros NPCs. Compare: predadores vanilla usam 5 |
| `SpawnBlockSet` | `"Soil"` | Surge apenas em blocos de solo. Outras opções: `"Birds"` (ar), `"Water"` (aquático), `"Volcanic"` (caverna) |
| `Id` | `"Slime"` | Corresponde ao nome do arquivo de role do NPC (`Slime.json`) sem o `.json` |
| `Flock` | `"One_Or_Two"` | Surge 1-2 Slimes juntos. Outras opções: `"Group_Small"`, `"Group_Medium"`, `"Group_Large"` |
| `DayTimeRange` | `[6, 18]` | Ativo das 6h às 18h (apenas durante o dia) |

:::tip[Spawns Noturnos]
Para NPCs noturnos, defina `DayTimeRange` como `[19, 5]` (ultrapassa a meia-noite — 19h às 5h). Adicione `"Despawn": { "DayTimeRange": [5, 19] }` para fazê-los desaparecer ao amanhecer, como criaturas Void vanilla.
:::

### Opções de Flock

| Valor de Flock | Tamanho do Grupo | Caso de Uso |
|----------------|-----------------|-------------|
| *(omitido)* | 1 | Predadores solitários (Ursos, Aranhas) |
| `"One_Or_Two"` | 1-2 | Grupos leves |
| `"Group_Small"` | 2-4 | Rebanhos de criaturas |
| `"Group_Medium"` | 3-6 | Rebanhos de animais |
| `"Group_Large"` | 5-10 | Grandes bandos |
| `{"Size": [2, 3]}` | 2-3 | Intervalo personalizado |

---

## Passo 2: Criar o Spawn do Mercador no Mundo

O Mercador Encantado Feran surge naturalmente em biomas Feran. Isso faz o mercador aparecer dentro e nos arredores das cidades Feran:

```
NPCSpawning/Server/NPC/Spawn/World/Zone2/Spawns_Zone2_Feran_Merchant.json
```

```json
{
  "Environments": [
    "Env_Zone2_Feran"
  ],
  "NPCs": [
    {
      "Weight": 100,
      "SpawnBlockSet": "Soil",
      "Id": "Feran_Enchanted_Merchant",
      "Flock": "One_Or_Two"
    }
  ],
  "DayTimeRange": [
    6,
    18
  ]
}
```

![Mercador Encantado Feran surgido em uma cidade Feran — "Pressione F para comerciar"](/hytale-modding-docs/images/tutorials/custom-npc-spawning/feran-merchant-city.png)

| Campo | Valor | Finalidade |
|-------|-------|------------|
| `Environments` | `["Env_Zone2_Feran"]` | Surge apenas em biomas Feran (Zone 2) |
| `Weight` | `100` | Peso alto garante spawn frequente. Compare: criaturas vanilla usam 5-20 |
| `Id` | `"Feran_Enchanted_Merchant"` | Corresponde ao nome do arquivo de role do NPC do mod NPCShopsAndTrading |
| `Flock` | `"One_Or_Two"` | Surge 1-2 mercadores juntos |

:::tip[Múltiplos Ambientes]
Para fazer o mercador surgir em todos os biomas da Zone 2, adicione mais ambientes ao array: `["Env_Zone2_Feran", "Env_Zone2_Savanna", "Env_Zone2_Desert", "Env_Zone2_Oasis", "Env_Zone2_Plateau"]`.
:::

---

## Passo 3: Criar o Manifesto

O mod de spawn depende tanto do mod do Slime NPC quanto do mod do NPC de comércio:

```
NPCSpawning/manifest.json
```

```json
{
  "Group": "HytaleModdingManual",
  "Name": "NPCSpawning",
  "Version": "1.0.0",
  "Description": "Custom NPC spawn rules for Slime in Azure forests and Feran Enchanted Merchant in Feran cities",
  "Authors": [
    {
      "Name": "HytaleModdingManual"
    }
  ],
  "Dependencies": {
    "HytaleModdingManual:CreateACustomNPC": "1.0.0",
    "HytaleModdingManual:NPCShopsAndTrading": "1.0.0"
  },
  "OptionalDependencies": {},
  "IncludesAssetPack": false
}
```

Note que `IncludesAssetPack` é `false` — regras de spawn são arquivos exclusivos do servidor sem assets do lado do cliente (sem modelos, texturas ou ícones).

---

## Passo 4: Opções Avançadas de Spawn

### Spawns Noturnos com Fases da Lua

Criaturas Void usam spawns exclusivamente noturnos com modificadores de fase lunar. Este padrão faz NPCs ficarem mais comuns durante a lua cheia:

```json
{
  "Environments": [
    "Env_Zone1_Plains",
    "Env_Zone1_Forests"
  ],
  "NPCs": [
    {
      "Weight": 20,
      "SpawnBlockSet": "Soil",
      "Id": "Slime",
      "Flock": {
        "Size": [2, 4]
      }
    }
  ],
  "DayTimeRange": [19, 5],
  "MoonPhaseWeightModifiers": [0.5, 1, 1.5, 1.5, 1],
  "LightRanges": {
    "Light": [0, 8]
  },
  "Despawn": {
    "DayTimeRange": [5, 19]
  }
}
```

| Campo | Finalidade |
|-------|------------|
| `MoonPhaseWeightModifiers` | Array de multiplicadores por fase lunar (índice 0 = lua nova). `1.5` dobra spawns na lua cheia, `0.5` reduz pela metade na lua nova |
| `LightRanges.Light` | `[min, max]` nível de luz (0-15). `[0, 8]` restringe a áreas escuras |
| `Despawn.DayTimeRange` | NPCs desaparecem forçadamente durante essas horas (limpeza ao amanhecer) |

### Spawns Aquáticos

Para NPCs que vivem na água, use o block set `Water` com `SpawnFluidTag`:

```json
{
  "Environments": ["Env_Zone1_Forests"],
  "NPCs": [
    {
      "Weight": 10,
      "SpawnBlockSet": "Water",
      "SpawnFluidTag": "Water",
      "Id": "Glowfish",
      "Flock": "Group_Small"
    }
  ]
}
```

---

## Passo 5: Testar no Jogo

1. Copie a pasta `NPCSpawning/` para `%APPDATA%/Hytale/UserData/Mods/`

2. Certifique-se de que os mods **CreateACustomNPC** e **NPCShopsAndTrading** também estejam instalados (dependências obrigatórias)

3. Inicie o Hytale e teste o spawn do Slime:
   - Viaje para um bioma de **Floresta Azure** ou **Floresta padrão** na Zone 1
   - Explore durante o dia (6h - 18h)
   - Slimes devem aparecer naturalmente em grupos de 1-2

4. Teste o spawn do Mercador:
   - Viaje para um **bioma Feran** na Zone 2
   - O Mercador Encantado deve aparecer naturalmente próximo às cidades Feran
   - Clique com o botão direito para abrir a interface de comércio

**Erros comuns e correções:**

| Erro | Causa | Correção |
|------|-------|----------|
| NPC nunca surge | ID de ambiente errado | Verifique se `Environments` corresponde aos nomes de bioma dos arquivos de spawn vanilla na mesma zona |
| `Unknown NPC role` | Role de NPC não encontrado | Verifique se o mod de dependência está instalado e se `Id` corresponde ao nome do arquivo de role |
| NPC surge no horário errado | `DayTimeRange` invertido | Diurno: `[6, 18]`. Noturno: `[19, 5]` (início > fim ultrapassa a meia-noite) |
| Spawns demais | `Weight` muito alto | Compare com vanilla: criaturas usam 2-6, predadores usam 3-5 |
| NPC flutua no ar | `SpawnBlockSet` errado | Use `"Soil"` para criaturas terrestres, `"Birds"` apenas para NPCs voadores |

---

## Resumo da Estrutura de Arquivos

```
NPCSpawning/
  manifest.json
  Server/
    NPC/
      Spawn/
        World/
          Zone1/
            Spawns_Zone1_Azure_Slime.json
          Zone2/
            Spawns_Zone2_Feran_Merchant.json
```

---

## Referência de Spawn Vanilla

| Arquivo Vanilla | Padrão | Caso de Uso |
|----------------|--------|-------------|
| `Spawns_Zone1_Forests_Predator.json` | Spawn do mundo, diurno, pesos iguais | Predadores de floresta (Ursos, Aranhas) |
| `Spawns_Zone1_Forests_Critter.json` | Spawn do mundo, diurno, pesos variados + flocks | Criaturas de floresta (Javalis, Coelhos) |
| `Spawns_Void_Zone1.json` | Spawn noturno, fases da lua, intervalos de luz | Criaturas Void |
| `Kweebec_Merchant.json` | Marcador dedicado de mercador | Mercador solo em vilas Kweebec |

---

## Próximos Passos

- [Criar um NPC Personalizado](/hytale-modding-docs/pt-br/tutorials/beginner/create-an-npc/) — defina os roles de NPC que suas regras de spawn referenciam
- [Lojas e Comércio de NPCs](/hytale-modding-docs/pt-br/tutorials/intermediate/npc-shops-and-trading/) — crie o NPC mercador Feran que surge em assentamentos
- [Tabelas de Loot Personalizadas](/hytale-modding-docs/pt-br/tutorials/intermediate/custom-loot-tables/) — configure o que seus NPCs spawnados dropam ao serem derrotados
