---
title: Encadeamento de Interacoes
description: Como o Hytale encadeia interacoes usando o campo Next para criar comportamentos complexos.
---

## Visao Geral

O Hytale constroi comportamentos de gameplay complexos encadeando interacoes simples. Cada interacao tem um `Type` e um campo opcional `Next` apontando para a acao seguinte. Isso cria pipelines sequenciais que podem incluir condicoes, dano, efeitos, sons e mais.

## Como as Cadeias de Interacao Funcionam

```mermaid
flowchart TD
    A[Player Uses Item] --> B{Condition Check}
    B -->|Game Mode = Adventure| C[Apply Effect]
    B -->|Wrong Game Mode| X[Chain Stops]
    C -->|EffectId: Burning| D[Deal Damage]
    D -->|BaseDamage: Fire 10| E[Chain Complete]

    style A fill:#2d5a27,color:#fff
    style X fill:#8b2500,color:#fff
    style E fill:#2d6a8f,color:#fff
```

### Cadeia de Acerto de Projetil

```mermaid
flowchart LR
    A[Projectile Hits Entity] --> B[DamageEntity\nFire: 15]
    B --> C[RemoveEntity\nProjectile destroyed]

    style A fill:#8b6500,color:#fff
    style C fill:#8b2500,color:#fff
```

### Cadeia Complexa de Arma

```mermaid
flowchart TD
    A[Player Swings Sword] --> B{Check Durability}
    B -->|Has durability| C[Damage Target]
    B -->|Broken| X[Play Break Sound]
    C --> D[Apply Knockback]
    D --> E{Critical Hit?}
    E -->|Yes| F[Apply Stun Effect]
    E -->|No| G[Play Hit Sound]
    F --> G
    G --> H[Reduce Durability]

    style A fill:#2d5a27,color:#fff
    style X fill:#8b2500,color:#fff
```

## Estrutura da Cadeia

```json
{
  "Type": "Condition",
  "RequiredGameMode": "Adventure",
  "Next": {
    "Type": "ApplyEffect",
    "EffectId": "Burning",
    "Next": {
      "Type": "Damage",
      "DamageCalculator": {
        "BaseDamage": { "Fire": 10 }
      }
    }
  }
}
```

Essa cadeia: verifica o modo de jogo -> aplica efeito de queimadura -> causa dano de fogo.

## Tipos de Interacao

| Type | Proposito | Campos Principais |
|------|-----------|-------------------|
| `Condition` | Condicao baseada em requisitos | `RequiredGameMode` |
| `ApplyEffect` | Aplica um efeito de status | `EffectId` |
| `Damage` | Causa dano | `DamageCalculator`, `BaseDamage` |
| `DamageEntity` | Dano ao acertar projetil | `DamageCalculator` |
| `RemoveEntity` | Destroi a entidade | — |
| `Simple` | Interacao basica | Varia |
| `Consume` | Usa um item consumivel | `Consume_Charge`, efeitos |

## Onde as Cadeias Sao Usadas

- **Interacoes de Itens** (`Server/Item/Interactions/`) — quebra de blocos, uso de ferramentas
- **Configs de Projeteis** (`Server/ProjectileConfigs/`) — acoes ao acertar e ao quicar
- **Acoes de NPCs** — sequencias de habilidades de combate

## Exemplo de Interacao de Projetil

```json
{
  "Interactions": {
    "ProjectileHit": {
      "Cooldown": 0,
      "Interactions": [
        {
          "Type": "DamageEntity",
          "DamageCalculator": { "BaseDamage": { "Fire": 15 } },
          "Next": {
            "Type": "RemoveEntity"
          }
        }
      ]
    }
  }
}
```

## Paginas Relacionadas

- [Item Interactions](/hytale-modding-docs/reference/item-system/item-interactions/) — cadeias de interacao de blocos e itens
- [Projectile Configs](/hytale-modding-docs/reference/combat-and-projectiles/projectile-configs/) — cadeias de eventos de projeteis
- [Damage Types](/hytale-modding-docs/reference/combat-and-projectiles/damage-types/) — hierarquia de tipos de dano
