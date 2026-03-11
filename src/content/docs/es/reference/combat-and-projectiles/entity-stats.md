---
title: Estadisticas de Entidad
description: Referencia de las definiciones de estadisticas de entidad del lado del servidor en Hytale, cubriendo valores base, reglas de regeneracion, condiciones y efectos de umbral.
---

## Descripcion General

Las estadisticas de entidad definen atributos numericos como salud, resistencia, mana y oxigeno que se rastrean por entidad. Cada archivo de estadistica declara el rango de valores, reglas opcionales de regeneracion con logica condicional y efectos activados por umbral. Las estadisticas son consumidas por el sistema de combate, el sistema de movimiento y el sistema de efectos para controlar habilidades, aplicar dano y activar cambios de estado.

## Ubicacion de Archivos

```
Assets/Server/Entity/Stats/
```

Un archivo JSON por estadistica:

```
Assets/Server/Entity/Stats/
  Ammo.json
  DeployablePreview.json
  GlidingActive.json
  Health.json
  Immunity.json
  MagicCharges.json
  Mana.json
  Oxygen.json
  SignatureCharges.json
  SignatureEnergy.json
  Stamina.json
  StaminaRegenDelay.json
```

## Esquema

### Campos de nivel superior

| Campo | Tipo | Requerido | Por defecto | Descripcion |
|-------|------|-----------|-------------|-------------|
| `InitialValue` | `number` | Si | — | Valor inicial de la estadistica cuando la entidad aparece. |
| `Min` | `number` | Si | — | Valor minimo que la estadistica puede alcanzar. Puede ser negativo (por ejemplo, estado de resistencia sobregirada). |
| `Max` | `number` | Si | — | Valor maximo que la estadistica puede alcanzar. `0` significa que el tope se establece dinamicamente (por ejemplo, por equipo). |
| `Shared` | `boolean` | No | `false` | Si es `true`, el valor de la estadistica se sincroniza con todos los clientes cercanos para la visualizacion del HUD. |
| `ResetType` | `string` | No | — | Como se restablece la estadistica al reaparecer. Valor conocido: `"MaxValue"` (se restablece a `Max`). |
| `IgnoreInvulnerability` | `boolean` | No | `false` | Si es `true`, las modificaciones a esta estadistica ignoran las verificaciones de invulnerabilidad. |
| `HideFromTooltip` | `boolean` | No | `false` | Si es `true`, la estadistica se oculta de la interfaz de informacion emergente del jugador. |
| `Regenerating` | `RegenRule[]` | No | — | Lista de reglas de regeneracion evaluadas en orden. Multiples reglas pueden apilarse o entrar en conflicto. |
| `MinValueEffects` | `ThresholdEffects` | No | — | Interacciones activadas cuando la estadistica alcanza su valor minimo. |
| `MaxValueEffects` | `ThresholdEffects` | No | — | Interacciones activadas cuando la estadistica alcanza su valor maximo. |

### RegenRule

| Campo | Tipo | Requerido | Por defecto | Descripcion |
|-------|------|-----------|-------------|-------------|
| `$Comment` | `string` | No | — | Nota legible por humanos ignorada por el motor. |
| `Interval` | `number` | Si | — | Segundos entre cada tick de regeneracion. |
| `Amount` | `number` | Si | — | Valor agregado (o restado si es negativo) por tick. |
| `RegenType` | `"Additive" \| "Percentage"` | Si | — | `Additive` agrega un valor plano; `Percentage` agrega una fraccion del maximo. |
| `ClampAtZero` | `boolean` | No | `false` | Si es `true`, el tick de regeneracion no empujara el valor por debajo de cero. |
| `Conditions` | `Condition[]` | No | — | Todas las condiciones deben cumplirse para que esta regla este activa. |

### Condition

| Campo | Tipo | Requerido | Por defecto | Descripcion |
|-------|------|-----------|-------------|-------------|
| `Id` | `string` | Si | — | Identificador del tipo de condicion. Valores conocidos: `"Alive"`, `"Player"`, `"NoDamageTaken"`, `"Stat"`, `"Wielding"`, `"Sprinting"`, `"Gliding"`, `"Charging"`, `"Suffocating"`, `"RegenHealth"`. |
| `Inverse` | `boolean` | No | `false` | Si es `true`, la condicion se niega (NO debe cumplirse). |
| `Delay` | `number` | No | — | Segundos que deben transcurrir desde que la condicion fue verdadera por ultima vez. Se usa con `"NoDamageTaken"` para crear retrasos de regeneracion. |
| `GameMode` | `string` | No | — | Modo de juego requerido. Se usa con la condicion `"Player"`, por ejemplo, `"Creative"`. |
| `Stat` | `string` | No | — | ID de estadistica para comparar. Se usa con la condicion `"Stat"`. |
| `Amount` | `number` | No | — | Valor umbral para la comparacion de estadisticas. Se usa con la condicion `"Stat"`. |
| `Comparison` | `string` | No | — | Operador de comparacion. Valores conocidos: `"Gte"` (mayor-o-igual), `"Lt"` (menor-que). |

### ThresholdEffects

| Campo | Tipo | Requerido | Por defecto | Descripcion |
|-------|------|-----------|-------------|-------------|
| `TriggerAtZero` | `boolean` | No | `false` | Si es `true`, se dispara cuando la estadistica alcanza exactamente cero en lugar del minimo real. |
| `Interactions` | `object` | No | — | Contenedor con un array `Interactions` de objetos de interaccion (por ejemplo, `ChangeStat`, `ClearEntityEffect`, `ApplyEffect`). |

## Ejemplos

**Health** (`Assets/Server/Entity/Stats/Health.json`):

```json
{
  "InitialValue": 100,
  "Min": 0,
  "Max": 100,
  "Shared": true,
  "ResetType": "MaxValue",
  "Regenerating": [
    {
      "$Comment": "NPC",
      "Interval": 0.5,
      "Amount": 0.05,
      "RegenType": "Percentage",
      "Conditions": [
        { "Id": "Alive" },
        { "Id": "Player", "Inverse": true },
        { "Id": "NoDamageTaken", "Delay": 15 },
        { "Id": "RegenHealth" }
      ]
    },
    {
      "$Comment": "Player in creative mode",
      "Interval": 0.5,
      "Amount": 1.0,
      "RegenType": "Percentage",
      "Conditions": [
        { "Id": "Alive" },
        { "Id": "Player", "GameMode": "Creative" }
      ]
    }
  ]
}
```

**Immunity** (`Assets/Server/Entity/Stats/Immunity.json`):

```json
{
  "InitialValue": 0,
  "Min": 0,
  "Max": 100,
  "Shared": true,
  "Regenerating": [
    {
      "Interval": 0.1,
      "Amount": -0.1,
      "RegenType": "Additive"
    }
  ],
  "MaxValueEffects": {
    "Interactions": {
      "Interactions": [
        {
          "Type": "ApplyEffect",
          "EffectId": "Immune"
        }
      ]
    }
  }
}
```

## Paginas Relacionadas

- [Efectos de Entidad](/es/hytale-modding-docs/reference/combat-and-projectiles/entity-effects) — efectos activados por umbrales de estadisticas
- [Tipos de Dano](/es/hytale-modding-docs/reference/combat-and-projectiles/damage-types) — dano que modifica la estadistica de Salud
- [Proyectiles](/es/hytale-modding-docs/reference/combat-and-projectiles/projectiles) — dano de proyectiles aplicado a estadisticas
