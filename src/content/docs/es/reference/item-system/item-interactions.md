---
title: Interacciones de Objetos
description: Referencia de los archivos JSON de cadenas de interacción de objetos en Hytale, cubriendo tipos de interacción, condiciones, calculadoras de daño y encadenamiento con Next.
---

## Descripción General

Las interacciones de objetos definen cómo se comportan los objetos cuando se usan — ataques, colocación de bloques, consumo, uso de herramientas, rodadas evasivas y más. Cada interacción es un objeto JSON con un `Type` y un campo opcional `Next` que encadena al siguiente paso. Esto crea tuberías que pueden ramificarse en condiciones, causar daño, aplicar efectos, reproducir sonidos y generar partículas. Los archivos de interacción son referenciados por ID desde las definiciones de objetos a través de los campos `Interactions` e `InteractionVars`.

## Ubicación del Archivo

```
Assets/Server/Item/Interactions/<Category>/<InteractionId>.json
```

Interacciones de nivel superior y raíz:
```
Assets/Server/Item/Interactions/Block_Primary.json
Assets/Server/Item/Interactions/Block_Secondary.json
Assets/Server/Item/Interactions/Dodge.json
Assets/Server/Item/Interactions/Stamina_Bar_Flash.json
Assets/Server/Item/RootInteractions/            — Puntos de entrada de interacciones raíz
```

Subcategorías:
```
Interactions/Consumables/   — Condiciones de consumo de comida y pociones
Interactions/Weapons/       — Cadenas de ataque de armas (Hacha, Arco, Maza, etc.)
Interactions/Weapons/Common/Melee/  — Daño cuerpo a cuerpo compartido y selector
Interactions/Tools/         — Interacciones específicas de herramientas
Interactions/Block/         — Interacciones de rotura/ataque de bloques
Interactions/Dodge/         — Interacciones de rodada evasiva
Interactions/NPCs/          — Interacciones activadas por NPCs
Interactions/Stat_Check/    — Condiciones de compuerta por estadísticas
```

## Esquema

### Campos Principales de Interacción

| Campo | Tipo | Requerido | Por Defecto | Descripción |
|-------|------|-----------|-------------|-------------|
| `Type` | string | No | `"Simple"` | Tipo de interacción. Ver lista de tipos abajo. |
| `Next` | string u object | No | — | La siguiente interacción a ejecutar en caso de éxito. Puede ser una cadena de ID de interacción o un objeto de interacción en línea. |
| `Failed` | string u object | No | — | La interacción a ejecutar cuando esta falla (usado por `Condition`, `UseBlock`, `PlaceBlock`, etc.). |
| `RunTime` | number | No | — | Duración en segundos que esta interacción ocupa en la línea de tiempo de la cadena. |
| `Effects` | object | No | — | Efectos aplicados cuando esta interacción se ejecuta exitosamente. Ver campos de Effects abajo. |
| `Parent` | string | No | — | Hereda campos de la interacción nombrada (herencia de plantilla). |

### Tipos de Interacción

| Tipo | Descripción |
|------|-------------|
| `Simple` | Se ejecuta inmediatamente sin lógica, luego procede a `Next`. |
| `Condition` | Verifica una o más condiciones booleanas. Procede a `Next` si pasa, `Failed` si falla. |
| `MovementCondition` | Se ramifica según la dirección de movimiento de la entidad (ForwardLeft, ForwardRight, Left, Right, BackLeft, BackRight). |
| `UseBlock` | Intenta interactuar con un bloque objetivo. Cae a `Failed` si no se impacta ningún bloque. |
| `PlaceBlock` | Coloca el objeto de bloque sostenido en la ubicación objetivo. |
| `Selector` | Barre un arco o volumen de hitbox para detectar entidades y bloques. Enruta los impactos a sub-interacciones `HitEntity` y `HitBlock`. |
| `Serial` | Ejecuta una lista de interacciones hijas en secuencia. Usa un arreglo `Interactions`. |
| `ApplyEffect` | Aplica un efecto de juego por `EffectId`. |
| `Replace` | Lee una variable nombrada (`Var`) y sustituye su valor en la cadena. Recurre a `DefaultValue` si la variable no está establecida y `DefaultOk` es true. |

### Campos de Condición (Type: `"Condition"`)

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `RequiredGameMode` | string | Requiere que la entidad esté en este modo de juego (ej. `"Adventure"`). |
| `Crouching` | boolean | Si se establece, requiere (`true`) o prohíbe (`false`) estar agachado. |
| `Flying` | boolean | Si se establece, requiere (`true`) o prohíbe (`false`) estar volando. |

### Campos de Selector (Type: `"Selector"`)

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `Selector.Id` | string | Tipo de forma del barrido (ej. `"Horizontal"`). |
| `Selector.Direction` | string | Dirección del barrido (ej. `"ToLeft"`). |
| `Selector.TestLineOfSight` | boolean | Si se verifica la línea de visión antes de registrar impactos. |
| `Selector.StartDistance` | number | Borde cercano del volumen de barrido. |
| `Selector.EndDistance` | number | Borde lejano del volumen de barrido. |
| `Selector.Length` | number | Longitud del arco en grados. |
| `Selector.YawStartOffset` | number | Desplazamiento de guiñada desde la dirección de mirada para iniciar el barrido. |
| `HitEntity` | object | Cadena de interacción ejecutada por cada entidad impactada. |
| `HitBlock` | object | Cadena de interacción ejecutada por cada bloque impactado. |

### Campos de DamageCalculator

Usados dentro de objetos de interacción para definir la salida de daño.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `Type` | string | Método de cálculo. `"Absolute"` usa un valor de daño base fijo. |
| `BaseDamage` | object | Mapa de tipo de daño a cantidad (ej. `{ "Physical": 12 }`). |
| `RandomPercentageModifier` | number | Fracción del daño base agregada como varianza aleatoria (ej. `0.2` = ±20%). |

### Campos de Effects

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `WorldSoundEventId` | string | ID del evento de sonido reproducido en la posición del mundo. |
| `LocalSoundEventId` | string | ID del evento de sonido reproducido localmente (escuchado solo por el jugador que actúa). |
| `WorldParticles` | object[] | Arreglo de sistemas de partículas `{ "SystemId": "<id>" }` generados en la posición del mundo. |
| `Particles` | object[] | Configuraciones de partículas con `SystemId`, `Color`, `TargetNodeName`, `TargetEntityPart`. |
| `Trails` | object[] | Configuraciones de efecto de estela de arma con `TrailId`, `TargetNodeName`, `PositionOffset`, `RotationOffset`. |
| `CameraEffect` | string | ID de sacudida/efecto de cámara aplicado al jugador que actúa (ej. `"Impact"`, `"Sword_Swing_Diagonal_Right"`). |
| `ItemAnimationId` | string | Animación reproducida en el objeto sostenido (ej. `"Consume"`, `"Build"`). |
| `WaitForAnimationToFinish` | boolean | Si la cadena espera a que la animación del objeto termine antes de continuar. |
| `Knockback` | object | Configuración de retroceso con `Type`, `Force`, `Direction` (X/Y/Z), `VelocityType` y `VelocityConfig`. |

## Ejemplos

`Assets/Server/Item/Interactions/Block_Primary.json`:

```json
{
  "Type": "Simple",
  "Next": {
    "Type": "UseBlock",
    "Failed": "Block_Attack"
  }
}
```

`Assets/Server/Item/Interactions/Block_Secondary.json`:

```json
{
  "Type": "UseBlock",
  "Failed": {
    "Type": "PlaceBlock",
    "RunTime": 0.125,
    "Effects": {
      "WaitForAnimationToFinish": false,
      "ItemAnimationId": "Build"
    }
  }
}
```

`Assets/Server/Item/Interactions/Consumables/Condition_Consume_Food.json`:

```json
{
  "Type": "Condition",
  "RequiredGameMode": "Adventure",
  "Crouching": false,
  "Next": "Consume_Charge",
  "Failed": "Block_Secondary"
}
```

`Assets/Server/Item/Interactions/Dodge.json`:

```json
{
  "Type": "Condition",
  "Flying": false,
  "Next": {
    "Type": "MovementCondition",
    "ForwardLeft": { "Type": "Simple" },
    "ForwardRight": { "Type": "Simple" },
    "Left": "Dodge_Left",
    "Right": "Dodge_Right",
    "BackLeft": { "Type": "Simple" },
    "BackRight": { "Type": "Simple" }
  }
}
```

`Assets/Server/Item/Interactions/Weapons/Common/Melee/Common_Melee_Damage.json`:

```json
{
  "Parent": "DamageEntityParent",
  "DamageCalculator": {
    "BaseDamage": {
      "Physical": 6
    }
  },
  "Effects": {
    "CameraEffect": "Impact"
  },
  "DamageEffects": {
    "Knockback": {
      "Type": "Force",
      "Force": 6.5,
      "Direction": { "X": 0.0, "Y": 1.0, "Z": -1.5 },
      "VelocityType": "Set"
    },
    "WorldSoundEventId": "SFX_Sword_T2_Impact",
    "LocalSoundEventId": "SFX_Sword_T2_Impact"
  }
}
```

## Páginas Relacionadas

- [Definiciones de Objetos](/hytale-modding-docs/reference/item-system/item-definitions) — Donde se establecen `Interactions` e `InteractionVars` en los objetos
- [Encadenamiento de Interacciones](/hytale-modding-docs/reference/concepts/interaction-chaining) — Guía conceptual para construir tuberías de interacción
