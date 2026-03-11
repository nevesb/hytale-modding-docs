---
title: Atitudes de NPC
description: Arquivos de atitude que definem como um tipo de NPC se relaciona com outros grupos de NPCs e categorias de itens, controlando combate, evasao e comportamento social.
---

## Visao Geral

Arquivos de atitude definem a disposicao social e de combate de um tipo de NPC em relacao a outros grupos de NPCs e categorias de itens. Cada arquivo corresponde a um role ou familia especifica de NPC e lista grupos nomeados mapeados para valores de atitude. O engine le esses arquivos em tempo de execucao para determinar se um NPC deve atacar, fugir, ignorar ou se aliar a outra entidade que detectar.

## Localizacao dos Arquivos

- `Assets/Server/NPC/Attitude/Roles/**/*.json` — Atitude em relacao a grupos de NPCs
- `Assets/Server/NPC/Attitude/Items/**/*.json` — Atitude em relacao a categorias de itens

## Schema

### Arquivo de Atitude de Role

| Field | Type | Required | Default | Descricao |
|-------|------|----------|---------|-----------|
| `Groups` | object | Sim | — | Mapa de nomes de atitude para arrays de IDs de grupos de NPC. |

As chaves do objeto `Groups` sao nomes de atitude. Os nomes de atitude reconhecidos sao:

| Atitude | Significado |
|---------|-------------|
| `Friendly` | Este NPC considera esses grupos como aliados — nao os atacara e pode assisti-los. |
| `Hostile` | Este NPC atacara membros desses grupos ao avistar. |
| `Neutral` | Consciencia passiva — nao ataca nem assiste. |
| `Ignore` | Desconsidera completamente membros desses grupos. |
| `Revered` | Maior consideracao positiva — pode seguir ou proteger. |

### Arquivo de Atitude de Item

| Field | Type | Required | Default | Descricao |
|-------|------|----------|---------|-----------|
| `Attitudes` | object | Sim | — | Mapa de nomes de atitude para arrays de IDs de categorias de itens. |

Nomes de atitude de itens seguem o mesmo vocabulario das atitudes de role (`Friendly`, `Hostile`, `Dislike`, `Love`, etc.).

## Exemplos

### Atitude de predador (arquivo de Critters)

Critters consideram a maioria das categorias como hostis (fogem delas) mas sao amigaveis com `Fen_Stalker`.

```json
{
  "Groups": {
    "Friendly": [
      "Fen_Stalker"
    ],
    "Hostile": [
      "Vermin",
      "Birds",
      "Predators",
      "PredatorsBig",
      "Void"
    ]
  }
}
```

### Atitude de presa (arquivo de Predators)

Predadores tratam presas como neutras (rastreavels mas nao atacam proativamente) e ignoram outros predadores grandes.

```json
{
  "Groups": {
    "Neutral": [
      "Prey"
    ],
    "Ignore": [
      "Predators",
      "PreyBig"
    ]
  }
}
```

### Atitude de faccao (Trork)

Trorks sao amigaveis com os seus, hostis a Kweebecs, ignoram prisioneiros e reverenciam seu chefe.

```json
{
  "Groups": {
    "Friendly": [
      "Trork"
    ],
    "Hostile": [
      "Kweebec"
    ],
    "Ignore": [
      "Kweebec_Prisoner"
    ],
    "Revered": [
      "Trork_Chieftain"
    ]
  }
}
```

### Atitudes de mundo vivo

As atitudes de `LivingWorld/` fornecem relacionamentos simples para criaturas ambientes:

**Agressivo** (criaturas agressivas tratam passivas como hostis):
```json
{
  "Groups": {
    "Hostile": ["Passive"]
  }
}
```

**Neutro** (criaturas neutras tratam agressivas como hostis):
```json
{
  "Groups": {
    "Hostile": ["Aggressive"]
  }
}
```

### Atitude de item

```json
{
  "Attitudes": {
    "Dislike": ["Weapon"],
    "Love": ["Food"]
  }
}
```

### Atitude vazia (sem relacionamentos definidos)

```json
{
  "Groups": {}
}
```

## Relacao com Arquivos de Role

O parametro `AttitudeGroup` no template de um role (ex: `"AttitudeGroup": "Prey"`) declara a qual grupo aquele NPC pertence. Quando outro NPC o detecta, o engine consulta o arquivo de atitude do NPC detector para ver como ele mapeia aquele grupo.

## Paginas Relacionadas

- [NPC Roles](/hytale-modding-docs/reference/npc-system/npc-roles) — Arquivos de role que declaram `DefaultNPCAttitude`, `DefaultPlayerAttitude` e `AttitudeGroup`
- [NPC Groups](/hytale-modding-docs/reference/npc-system/npc-groups) — Definicoes de grupo referenciadas nos arrays de `Groups`
- [NPC Templates](/hytale-modding-docs/reference/npc-system/npc-templates) — Templates que definem parametros de atitude padrao
