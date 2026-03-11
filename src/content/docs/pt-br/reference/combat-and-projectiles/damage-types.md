---
title: Tipos de Dano
description: Referencia para a hierarquia de tipos de dano no Hytale, incluindo subtipos Fisico, Elemental e Ambiental, e seus efeitos na durabilidade e stamina.
---

## Visao Geral

Os tipos de dano formam uma hierarquia de heranca usada pelo sistema de combate para determinar resistencias, efeitos e penalidades. Cada arquivo de tipo de dano pode declarar um campo `Parent` e `Inherits` para estender as propriedades de outro tipo. Os tipos folha (ex: `Fire`, `Slashing`) sao os que armas e habilidades realmente causam; os tipos raiz (`Physical`, `Elemental`, `Environment`) existem apenas para definir o comportamento compartilhado dos subtipos.

## Localizacao dos Arquivos

```
Assets/Server/Entity/Damage/
```

Um arquivo JSON por tipo de dano:

```
Assets/Server/Entity/Damage/
  Physical.json
  Elemental.json
  Environment.json
  Environmental.json
  Bludgeoning.json   (implicito — sem arquivo independente; definido inline)
  Slashing.json
  Fire.json
  Ice.json
  Poison.json
  Projectile.json
  Fall.json
  Drowning.json
  Suffocation.json
  OutOfWorld.json
  Command.json
```

## Schema

| Campo | Tipo | Obrigatorio | Padrao | Descricao |
|-------|------|-------------|--------|-----------|
| `Parent` | `string` | Nao | — | O ID do tipo de dano pai do qual este tipo herda. |
| `Inherits` | `string` | Nao | — | Declaracao de heranca adicional (normalmente espelha `Parent`). |
| `DurabilityLoss` | `boolean` | Nao | `false` | Se acertos deste tipo causam perda de durabilidade no equipamento. |
| `StaminaLoss` | `boolean` | Nao | `false` | Se acertos deste tipo esgotam a stamina do alvo. |
| `BypassResistances` | `boolean` | Nao | `false` | Se `true`, este tipo de dano ignora todos os calculos de resistencia. |
| `DamageTextColor` | `string` | Nao | — | Cor hexadecimal usada para numeros de dano flutuantes (ex: `"#00FF00"` para veneno). |
| `$Comment` | `string` | Nao | — | String de comentario interno, nao usada em tempo de execucao. |

## Hierarquia

```
(raiz)
├── Physical                    DurabilityLoss: true, StaminaLoss: true
│   ├── Slashing                Parent: Physical
│   ├── Bludgeoning             (herdado de Physical)
│   └── Piercing                (herdado de Physical)
│
├── Elemental                   (tipo base para subtipos elementais)
│   ├── Fire                    Parent: Elemental
│   ├── Ice                     Parent: Elemental
│   └── Poison                  DamageTextColor: #00FF00
│
├── Projectile                  DurabilityLoss: true, StaminaLoss: false
│
├── Environment                 (tipo base)
│   ├── Fall                    Parent: Environment
│   └── Drowning                Parent: Environment
│
├── Environmental               DurabilityLoss: true, StaminaLoss: true, BypassResistances: false
│                               (perigos ambientais: espinhos, cacto, etc.)
│
├── Suffocation
├── OutOfWorld
└── Command                     DurabilityLoss: false, StaminaLoss: false, BypassResistances: true
```

## Descricoes dos Tipos

| Tipo | Pai | DurabilityLoss | StaminaLoss | BypassResistances | Notas |
|------|-----|---------------|-------------|-------------------|-------|
| `Physical` | — | `true` | `true` | `false` | Tipo fisico raiz; facilita subtipos. |
| `Slashing` | `Physical` | `true` | `true` | `false` | Dano de espada, machado. |
| `Elemental` | — | `false` | `false` | `false` | Tipo elemental raiz; facilita subtipos. |
| `Fire` | `Elemental` | `false` | `false` | `false` | Dano de feitico de fogo e ignicao. |
| `Ice` | `Elemental` | `false` | `false` | `false` | Dano de feitico de gelo. |
| `Poison` | — | `false` | `false` | `false` | Texto de dano verde (`#00FF00`). |
| `Projectile` | — | `true` | `false` | `false` | Acertos de flechas e projeteis arremessados. |
| `Environment` | — | — | — | — | Tipo raiz para dano ambiental. |
| `Fall` | `Environment` | — | — | — | Dano de queda. |
| `Drowning` | `Environment` | — | — | — | Sufocamento na agua. |
| `Environmental` | — | `true` | `true` | `false` | Perigos de plantas (espinhos, cacto). |
| `Command` | — | `false` | `false` | `true` | Dano aplicado por admin/script; ignora todas as resistencias. |

## Exemplos

**Physical** (`Assets/Server/Entity/Damage/Physical.json`):

```json
{
  "$Comment": "This damage type exists to facilitate sub types",
  "DurabilityLoss": true,
  "StaminaLoss": true
}
```

**Slashing** (`Assets/Server/Entity/Damage/Slashing.json`):

```json
{
  "Parent": "Physical",
  "Inherits": "Physical"
}
```

**Poison** (`Assets/Server/Entity/Damage/Poison.json`):

```json
{
  "DamageTextColor": "#00FF00"
}
```

**Command** (`Assets/Server/Entity/Damage/Command.json`):

```json
{
  "DurabilityLoss": false,
  "StaminaLoss": false,
  "BypassResistances": true
}
```

**Environmental** (`Assets/Server/Entity/Damage/Environmental.json`):

```json
{
  "$Comment": "Damage type for environmental hazards like plants (bushes, cactus, etc.)",
  "DurabilityLoss": true,
  "StaminaLoss": true,
  "BypassResistances": false
}
```

## Paginas Relacionadas

- [Projeteis](/pt-br/hytale-modding-docs/reference/combat-and-projectiles/projectiles) — campo `Damage` nas definicoes de projeteis
- [Configuracoes de Projeteis](/pt-br/hytale-modding-docs/reference/combat-and-projectiles/projectile-configs) — mapa `BaseDamage` nos calculadores de dano de interacao
