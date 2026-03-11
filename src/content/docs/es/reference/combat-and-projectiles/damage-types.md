---
title: Tipos de Dano
description: Referencia de la jerarquia de tipos de dano en Hytale, incluyendo subtipos Fisicos, Elementales y Ambientales, y su efecto en la durabilidad y la resistencia.
---

## Descripcion General

Los tipos de dano forman una jerarquia de herencia utilizada por el sistema de combate para determinar resistencias, efectos y penalizaciones. Cada archivo de tipo de dano puede declarar un campo `Parent` y un campo `Inherits` para extender las propiedades de otro tipo. Los tipos hoja (por ejemplo, `Fire`, `Slashing`) son los que las armas y habilidades realmente infligen; los tipos raiz (`Physical`, `Elemental`, `Environment`) existen unicamente para definir el comportamiento compartido de los subtipos.

## Ubicacion de Archivos

```
Assets/Server/Entity/Damage/
```

Un archivo JSON por tipo de dano:

```
Assets/Server/Entity/Damage/
  Physical.json
  Elemental.json
  Environment.json
  Environmental.json
  Bludgeoning.json   (implicito — sin archivo independiente; definido en linea)
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

## Esquema

| Campo | Tipo | Requerido | Por defecto | Descripcion |
|-------|------|-----------|-------------|-------------|
| `Parent` | `string` | No | — | El ID del tipo de dano padre del cual hereda este tipo. |
| `Inherits` | `string` | No | — | Declaracion de herencia adicional (generalmente refleja `Parent`). |
| `DurabilityLoss` | `boolean` | No | `false` | Si los golpes de este tipo causan perdida de durabilidad en el equipo. |
| `StaminaLoss` | `boolean` | No | `false` | Si los golpes de este tipo agotan la resistencia del objetivo. |
| `BypassResistances` | `boolean` | No | `false` | Si es `true`, este tipo de dano ignora todos los calculos de resistencia. |
| `DamageTextColor` | `string` | No | — | Color hexadecimal usado para los numeros de dano flotantes (por ejemplo, `"#00FF00"` para veneno). |
| `$Comment` | `string` | No | — | Cadena de comentario interno, no utilizada en tiempo de ejecucion. |

## Jerarquia

```
(raiz)
├── Physical                    DurabilityLoss: true, StaminaLoss: true
│   ├── Slashing                Parent: Physical
│   ├── Bludgeoning             (heredado de Physical)
│   └── Piercing                (heredado de Physical)
│
├── Elemental                   (tipo base para subtipos elementales)
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
│                               (peligros ambientales: espinas, cactus, etc.)
│
├── Suffocation
├── OutOfWorld
└── Command                     DurabilityLoss: false, StaminaLoss: false, BypassResistances: true
```

## Descripciones de Tipos

| Tipo | Padre | DurabilityLoss | StaminaLoss | BypassResistances | Notas |
|------|-------|---------------|-------------|-------------------|-------|
| `Physical` | — | `true` | `true` | `false` | Tipo fisico raiz; facilita los subtipos. |
| `Slashing` | `Physical` | `true` | `true` | `false` | Dano de espada, hacha. |
| `Elemental` | — | `false` | `false` | `false` | Tipo elemental raiz; facilita los subtipos. |
| `Fire` | `Elemental` | `false` | `false` | `false` | Dano de hechizo de fuego e ignicion. |
| `Ice` | `Elemental` | `false` | `false` | `false` | Dano de hechizo de hielo. |
| `Poison` | — | `false` | `false` | `false` | Texto de dano verde (`#00FF00`). |
| `Projectile` | — | `true` | `false` | `false` | Impactos de flechas y proyectiles lanzados. |
| `Environment` | — | — | — | — | Tipo raiz para dano ambiental. |
| `Fall` | `Environment` | — | — | — | Dano por caida. |
| `Drowning` | `Environment` | — | — | — | Asfixia en el agua. |
| `Environmental` | — | `true` | `true` | `false` | Peligros de plantas (espinas, cactus). |
| `Command` | — | `false` | `false` | `true` | Dano aplicado por admin/script; ignora todas las resistencias. |

## Ejemplos

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

- [Proyectiles](/es/hytale-modding-docs/reference/combat-and-projectiles/projectiles) — campo `Damage` en las definiciones de proyectiles
- [Configuraciones de Proyectiles](/es/hytale-modding-docs/reference/combat-and-projectiles/projectile-configs) — mapa `BaseDamage` en los calculadores de dano de interaccion
