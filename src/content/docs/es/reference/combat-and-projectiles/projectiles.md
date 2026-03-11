---
title: Proyectiles
description: Referencia de las definiciones de proyectiles del lado del servidor en Hytale, cubriendo parámetros de física, daño, eventos de sonido y partículas de impacto/fallo.
---

## Descripción General

Los archivos de proyectiles definen el comportamiento físico y las propiedades de daño de instancias individuales de proyectiles — flechas, hechizos y otros objetos disparados. Son la contraparte de datos de las [Configuraciones de Proyectiles](/hytale-modding-docs/reference/combat-and-projectiles/projectile-configs), que definen parámetros de lanzamiento y cadenas de interacción. Cada archivo de proyectil es referenciado por una cadena `Appearance` que lo vincula a los visuales del lado del cliente.

## Ubicación del Archivo

```
Assets/Server/Projectiles/
```

Los subdirectorios agrupan los proyectiles por categoría:

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

## Esquema

| Campo | Tipo | Requerido | Por Defecto | Descripción |
|-------|------|-----------|-------------|-------------|
| `Appearance` | `string` | Sí | — | ID de apariencia del lado del cliente usado para buscar el modelo visual y textura del proyectil. |
| `MuzzleVelocity` | `number` | Sí | — | Velocidad inicial de lanzamiento en unidades/segundo en el momento del disparo. |
| `TerminalVelocity` | `number` | Sí | — | Velocidad máxima que el proyectil puede alcanzar en vuelo. |
| `Gravity` | `number` | Sí | — | Aceleración gravitacional descendente aplicada cada segundo. `0` para tiros perfectamente rectos. |
| `Bounciness` | `number` | No | `0` | Fracción de velocidad retenida después de rebotar en una superficie. `0` = sin rebote. |
| `ImpactSlowdown` | `number` | No | `0` | Reducción de velocidad aplicada en el impacto. |
| `TimeToLive` | `number` | No | `0` | Segundos antes de que el proyectil sea destruido automáticamente. `0` = sin límite de tiempo. |
| `Damage` | `number` | Sí | — | Daño base causado en un impacto exitoso. |
| `DeadTime` | `number` | No | `0` | Segundos que el proyectil permanece después de impactar un objetivo antes de ser eliminado. |
| `DeadTimeMiss` | `number` | No | — | Segundos que el proyectil permanece después de fallar (impactar terreno). |
| `SticksVertically` | `boolean` | No | `false` | Si es `true`, el proyectil se incrusta verticalmente en las superficies en lugar de quedar acostado. |
| `PitchAdjustShot` | `boolean` | No | `false` | Si es `true`, la inclinación del proyectil se corrige basándose en la trayectoria del arco. |
| `HorizontalCenterShot` | `number` | No | `0` | Desplazamiento horizontal de precisión desde el centro de la mira. |
| `VerticalCenterShot` | `number` | No | `0` | Desplazamiento vertical de precisión desde el centro de la mira. |
| `DepthShot` | `number` | No | `1` | Multiplicador de profundidad para la detección de impactos. |
| `Radius` | `number` | No | — | Radio de la esfera de colisión. Si se omite, se usa un hitbox de cápsula por defecto. |
| `Height` | `number` | No | — | Altura de la cápsula de colisión. |
| `HitSoundEventId` | `string` | No | — | Evento de sonido reproducido al impactar una entidad. |
| `MissSoundEventId` | `string` | No | — | Evento de sonido reproducido al fallar contra el terreno. |
| `BounceSoundEventId` | `string` | No | — | Evento de sonido reproducido en cada rebote. |
| `DeathSoundEventId` | `string` | No | — | Evento de sonido reproducido cuando el proyectil expira naturalmente. |
| `HitParticles` | `ParticleRef` | No | — | Sistema de partículas generado al impactar una entidad. |
| `MissParticles` | `ParticleRef` | No | — | Sistema de partículas generado al fallar contra el terreno. |
| `BounceParticles` | `ParticleRef` | No | — | Sistema de partículas generado en cada rebote. |
| `DeathParticles` | `ParticleRef` | No | — | Sistema de partículas generado cuando el proyectil expira. |
| `DeathEffectsOnHit` | `boolean` | No | `false` | Si es `true`, las partículas y sonidos de muerte también se activan en un impacto exitoso contra una entidad. |
| `ExplosionConfig` | `object` | No | — | Configura una explosión de área de efecto en el impacto (ver abajo). |

### ParticleRef

| Campo | Tipo | Requerido | Por Defecto | Descripción |
|-------|------|-----------|-------------|-------------|
| `SystemId` | `string` | Sí | — | ID del sistema de partículas a generar. |

### ExplosionConfig

| Campo | Tipo | Requerido | Por Defecto | Descripción |
|-------|------|-----------|-------------|-------------|
| `DamageEntities` | `boolean` | No | `false` | Si la explosión daña entidades cercanas. |
| `DamageBlocks` | `boolean` | No | `false` | Si la explosión daña bloques cercanos. |
| `EntityDamageRadius` | `number` | No | — | Radio en unidades dentro del cual las entidades reciben daño. |
| `EntityDamageFalloff` | `number` | No | `1.0` | Multiplicador de reducción de daño aplicado en el borde del radio. |
| `BlockDamageRadius` | `number` | No | — | Radio en unidades dentro del cual los bloques son dañados. |
| `Knockback` | `object` | No | — | Retroceso aplicado a las entidades en el radio de explosión. |

## Ejemplos

**Flecha de carga completa** (`Assets/Server/Projectiles/Arrow_FullCharge.json`):

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

**Hechizo de bola de fuego** (`Assets/Server/Projectiles/Spells/Fireball.json`):

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

## Páginas Relacionadas

- [Configuraciones de Proyectiles](/hytale-modding-docs/reference/combat-and-projectiles/projectile-configs) — Parámetros de lanzamiento y cadenas de interacción
- [Tipos de Daño](/hytale-modding-docs/reference/combat-and-projectiles/damage-types) — Jerarquía de tipos de daño
