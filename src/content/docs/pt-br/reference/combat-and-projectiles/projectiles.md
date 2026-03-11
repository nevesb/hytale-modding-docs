---
title: Projeteis
description: Referencia para definicoes de projeteis no lado do servidor no Hytale, cobrindo parametros de fisica, dano, eventos sonoros e particulas de acerto/erro.
---

## Visao Geral

Arquivos de projeteis definem o comportamento fisico e as propriedades de dano de instancias individuais de projeteis — flechas, feiticos e outros objetos disparados. Eles sao a contraparte de dados das [Configuracoes de Projeteis](/pt-br/hytale-modding-docs/reference/combat-and-projectiles/projectile-configs), que definem parametros de lancamento e cadeias de interacao. Cada arquivo de projetil e referenciado por uma string `Appearance` que o vincula aos visuais do lado do cliente.

## Localizacao dos Arquivos

```
Assets/Server/Projectiles/
```

Subdiretorios agrupam projeteis por categoria:

```
Assets/Server/Projectiles/
  Arrow_FullCharge.json
  Arrow_HalfCharge.json
  Arrow_NoCharge.json
  Ice_Ball.json
  Ice_Bolt.json
  Roots.json
  NPCs/
  Player/
  Spells/
    Fireball.json
```

## Schema

| Campo | Tipo | Obrigatorio | Padrao | Descricao |
|-------|------|-------------|--------|-----------|
| `Appearance` | `string` | Sim | — | ID de aparencia do lado do cliente usado para buscar o modelo visual e textura do projetil. |
| `MuzzleVelocity` | `number` | Sim | — | Velocidade inicial de lancamento em unidades/segundo no momento do disparo. |
| `TerminalVelocity` | `number` | Sim | — | Velocidade maxima que o projetil pode atingir em voo. |
| `Gravity` | `number` | Sim | — | Aceleracao gravitacional descendente aplicada a cada segundo. `0` para tiros perfeitamente retos. |
| `Bounciness` | `number` | Nao | `0` | Fracao de velocidade retida apos quicar em uma superficie. `0` = sem quique. |
| `ImpactSlowdown` | `number` | Nao | `0` | Reducao de velocidade aplicada no impacto. |
| `TimeToLive` | `number` | Nao | `0` | Segundos antes do projetil ser destruido automaticamente. `0` = sem tempo limite. |
| `Damage` | `number` | Sim | — | Dano base causado em um acerto bem-sucedido. |
| `DeadTime` | `number` | Nao | `0` | Segundos que o projetil permanece apos acertar um alvo antes de ser removido. |
| `DeadTimeMiss` | `number` | Nao | — | Segundos que o projetil permanece apos errar (acertar terreno). |
| `SticksVertically` | `boolean` | Nao | `false` | Se `true`, o projetil se crava na vertical em superficies em vez de ficar deitado. |
| `PitchAdjustShot` | `boolean` | Nao | `false` | Se `true`, o pitch do projetil e corrigido com base na trajetoria do arco. |
| `HorizontalCenterShot` | `number` | Nao | `0` | Desvio de precisao horizontal do centro da mira. |
| `VerticalCenterShot` | `number` | Nao | `0` | Desvio de precisao vertical do centro da mira. |
| `DepthShot` | `number` | Nao | `1` | Multiplicador de profundidade para deteccao de acerto. |
| `Radius` | `number` | Nao | — | Raio da esfera de colisao. Se omitido, uma hitbox capsula padrao e usada. |
| `Height` | `number` | Nao | — | Altura da capsula de colisao. |
| `HitSoundEventId` | `string` | Nao | — | Evento sonoro reproduzido ao acertar uma entidade. |
| `MissSoundEventId` | `string` | Nao | — | Evento sonoro reproduzido ao errar no terreno. |
| `BounceSoundEventId` | `string` | Nao | — | Evento sonoro reproduzido a cada quique. |
| `DeathSoundEventId` | `string` | Nao | — | Evento sonoro reproduzido quando o projetil expira naturalmente. |
| `HitParticles` | `ParticleRef` | Nao | — | Sistema de particulas gerado ao acertar uma entidade. |
| `MissParticles` | `ParticleRef` | Nao | — | Sistema de particulas gerado ao errar no terreno. |
| `BounceParticles` | `ParticleRef` | Nao | — | Sistema de particulas gerado a cada quique. |
| `DeathParticles` | `ParticleRef` | Nao | — | Sistema de particulas gerado quando o projetil expira. |
| `DeathEffectsOnHit` | `boolean` | Nao | `false` | Se `true`, particulas e sons de morte tambem disparam em um acerto bem-sucedido em entidade. |
| `ExplosionConfig` | `object` | Nao | — | Configura explosao com area de efeito no impacto (veja abaixo). |

### ParticleRef

| Campo | Tipo | Obrigatorio | Padrao | Descricao |
|-------|------|-------------|--------|-----------|
| `SystemId` | `string` | Sim | — | ID do sistema de particulas a ser gerado. |

### ExplosionConfig

| Campo | Tipo | Obrigatorio | Padrao | Descricao |
|-------|------|-------------|--------|-----------|
| `DamageEntities` | `boolean` | Nao | `false` | Se a explosao causa dano a entidades proximas. |
| `DamageBlocks` | `boolean` | Nao | `false` | Se a explosao causa dano a blocos proximos. |
| `EntityDamageRadius` | `number` | Nao | — | Raio em unidades dentro do qual entidades recebem dano. |
| `EntityDamageFalloff` | `number` | Nao | `1.0` | Multiplicador de reducao de dano aplicado na borda do raio. |
| `BlockDamageRadius` | `number` | Nao | — | Raio em unidades dentro do qual blocos sao danificados. |
| `Knockback` | `object` | Nao | — | Repulsao aplicada a entidades no raio da explosao. |

## Exemplos

**Flecha com carga total** (`Assets/Server/Projectiles/Arrow_FullCharge.json`):

```json
{
  "Appearance": "Arrow_Crude",
  "SticksVertically": true,
  "MuzzleVelocity": 50,
  "TerminalVelocity": 50,
  "Gravity": 10,
  "Bounciness": 0,
  "ImpactSlowdown": 0,
  "TimeToLive": 20,
  "Damage": 20,
  "DeadTime": 0.1,
  "HorizontalCenterShot": 0.1,
  "VerticalCenterShot": 0.1,
  "DepthShot": 1,
  "PitchAdjustShot": true,
  "HitSoundEventId": "SFX_Arrow_FullCharge_Hit",
  "MissSoundEventId": "SFX_Arrow_FullCharge_Miss",
  "HitParticles": {
    "SystemId": "Impact_Blade_01"
  }
}
```

**Feitico de bola de fogo** (`Assets/Server/Projectiles/Spells/Fireball.json`):

```json
{
  "Appearance": "Fireball",
  "Radius": 0.1,
  "Height": 0.2,
  "MuzzleVelocity": 40,
  "TerminalVelocity": 100,
  "Gravity": 4,
  "Bounciness": 0,
  "TimeToLive": 0,
  "Damage": 60,
  "DeadTime": 0,
  "DeathEffectsOnHit": true,
  "MissParticles": { "SystemId": "Explosion_Medium" },
  "BounceParticles": { "SystemId": "Impact_Fire" },
  "DeathParticles": { "SystemId": "Explosion_Medium" },
  "MissSoundEventId": "SFX_Fireball_Miss",
  "DeathSoundEventId": "SFX_Fireball_Death",
  "ExplosionConfig": {
    "DamageEntities": true,
    "DamageBlocks": false,
    "EntityDamageRadius": 5,
    "EntityDamageFalloff": 1.0
  }
}
```

## Paginas Relacionadas

- [Configuracoes de Projeteis](/pt-br/hytale-modding-docs/reference/combat-and-projectiles/projectile-configs) — parametros de lancamento e cadeias de interacao
- [Tipos de Dano](/pt-br/hytale-modding-docs/reference/combat-and-projectiles/damage-types) — hierarquia de tipos de dano
