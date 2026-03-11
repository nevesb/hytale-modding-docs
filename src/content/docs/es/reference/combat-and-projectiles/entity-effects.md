---
title: Efectos de Entidad
description: Referencia de las definiciones de efectos de entidad del lado del servidor en Hytale, cubriendo duracion, tintes visuales, modificadores de estadisticas, dano con el tiempo y comportamiento de superposicion.
---

## Descripcion General

Los efectos de entidad son modificadores temporales o permanentes aplicados a las entidades en tiempo de ejecucion. Impulsan una amplia gama de sistemas: tintes visuales y superposiciones de pantalla al recibir dano, mejoras de comida que aumentan la salud maxima, dano con el tiempo por quemaduras y veneno, efectos de control de masas como raiz y aturdimiento, y rastros de particulas cosmeticos en habilidades de armas. Cada archivo de efecto define su duracion, reglas de superposicion, modificaciones de estadisticas y retroalimentacion visual/auditiva.

## Ubicacion de Archivos

```
Assets/Server/Entity/Effects/
```

Los subdirectorios agrupan los efectos por categoria:

```
Assets/Server/Entity/Effects/
  BlockPlacement/     (retroalimentacion de exito/fallo al colocar bloques)
  Damage/             (efectos de destello al recibir golpe)
  Deployables/        (auras de sanacion/ralentizacion de totems)
  Drop/               (efectos de brillo por rareza de objetos)
  Food/
    Boost/            (aumentos de estadisticas maximas por comida)
    Buff/             (sanaciones instantaneas y mejoras con temporizador)
  GameMode/           (visual del modo creativo)
  Immunity/           (invulnerabilidad al esquivar, inmunidad al fuego/ambiente)
  Mana/               (efectos de regeneracion y drenaje de mana)
  Movement/           (efectos direccionales al esquivar)
  Npc/                (muerte de NPC, sanacion, retorno a casa)
  Portals/            (visual de teletransporte)
  Projectiles/        (sub-efectos de flechas, bombas, escombros)
  Stamina/            (resistencia agotada, error, retraso de regeneracion)
  Status/             (quemadura, congelacion, veneno, raiz, ralentizacion, aturdimiento)
  Weapons/            (efectos de firma y habilidad de armas)
```

## Esquema

### Campos de nivel superior

| Campo | Tipo | Requerido | Por defecto | Descripcion |
|-------|------|-----------|-------------|-------------|
| `Duration` | `number` | Si | — | Duracion del efecto en segundos. `0` o `0.0` significa que el efecto se dispara una vez instantaneamente. |
| `Infinite` | `boolean` | No | `false` | Si es `true`, el efecto persiste indefinidamente hasta que se elimine explicitamente. Anula `Duration`. |
| `OverlapBehavior` | `"Overwrite" \| "Extend"` | No | — | Como manejar la re-aplicacion mientras ya esta activo. `Overwrite` reemplaza el temporizador; `Extend` agrega a la duracion restante. |
| `RemovalBehavior` | `string` | No | — | Como se elimina el efecto. Valor conocido: `"Duration"` (se elimina cuando expira el temporizador). |
| `Debuff` | `boolean` | No | `false` | Si es `true`, el efecto se clasifica como debuff y puede ser limpiado por interacciones tipo antidoto. |
| `Invulnerable` | `boolean` | No | `false` | Si es `true`, la entidad no puede recibir dano mientras el efecto esta activo. |
| `StatusEffectIcon` | `string` | No | — | Ruta al icono de la interfaz mostrado en la barra de efectos de estado. |
| `DeathMessageKey` | `string` | No | — | Clave de localizacion para el mensaje de muerte cuando este efecto mata a una entidad. |
| `ApplicationEffects` | `ApplicationEffects` | No | — | Modificaciones visuales, de audio y de movimiento aplicadas mientras el efecto esta activo. |
| `StatModifiers` | `object` | No | — | Mapa de ID de estadistica a valor plano agregado por tick (por ejemplo, `{"Health": 2}`). |
| `ValueType` | `string` | No | — | Como se interpretan los valores de `StatModifiers`. Valor conocido: `"Percent"`. |
| `RawStatModifiers` | `object` | No | — | Mapa de ID de estadistica a un array de objetos modificadores crudos para manipulacion avanzada de estadisticas. |
| `DamageCalculator` | `DamageCalculator` | No | — | Dano periodico aplicado mientras el efecto esta activo. |
| `DamageCalculatorCooldown` | `number` | No | — | Segundos entre cada tick de dano del `DamageCalculator`. |
| `DamageEffects` | `object` | No | — | Eventos de sonido activados en cada tick de dano. |
| `ModelOverride` | `ModelOverride` | No | — | Reemplaza el modelo visual de la entidad durante la duracion del efecto (por ejemplo, enredaderas de raiz). |

### ApplicationEffects

| Campo | Tipo | Requerido | Por defecto | Descripcion |
|-------|------|-----------|-------------|-------------|
| `EntityTopTint` | `string` | No | — | Color hexadecimal aplicado a la parte superior del modelo de la entidad. |
| `EntityBottomTint` | `string` | No | — | Color hexadecimal aplicado a la parte inferior del modelo de la entidad. |
| `ScreenEffect` | `string` | No | — | Ruta a una textura de superposicion de pantalla (por ejemplo, `"ScreenEffects/Fire.png"`). |
| `HorizontalSpeedMultiplier` | `number` | No | — | Multiplicador aplicado a la velocidad de movimiento horizontal. `0.5` = 50% de velocidad. |
| `KnockbackMultiplier` | `number` | No | — | Multiplicador para el retroceso entrante. `0` = inmune al retroceso. |
| `ModelVFXId` | `string` | No | — | ID de un VFX a nivel de modelo para adjuntar a la entidad. |
| `Particles` | `ParticleRef[]` | No | — | Lista de sistemas de particulas para generar en la entidad. |
| `MovementEffects` | `object` | No | — | Anulaciones de movimiento. Contiene `DisableAll: true` para inmovilizar completamente a la entidad. |
| `WorldSoundEventId` | `string` | No | — | Evento de sonido audible para todos los jugadores cercanos. |
| `LocalSoundEventId` | `string` | No | — | Evento de sonido audible solo para el jugador afectado. |

### ParticleRef

| Campo | Tipo | Requerido | Por defecto | Descripcion |
|-------|------|-----------|-------------|-------------|
| `SystemId` | `string` | Si | — | ID del sistema de particulas a generar. |
| `TargetEntityPart` | `string` | No | — | Parte de la entidad a la que adjuntar la particula (por ejemplo, `"Entity"`). |
| `TargetNodeName` | `string` | No | — | Nombre del hueso o nodo para el anclaje (por ejemplo, `"Hip"`). |
| `PositionOffset` | `Vector3` | No | — | Desplazamiento local desde el punto de anclaje. |
| `Color` | `string` | No | — | Color hexadecimal de anulacion para el sistema de particulas. |

### RawStatModifier

| Campo | Tipo | Requerido | Por defecto | Descripcion |
|-------|------|-----------|-------------|-------------|
| `Amount` | `number` | Si | — | Valor del modificador. La interpretacion depende de `CalculationType`. |
| `CalculationType` | `"Additive" \| "Multiplicative"` | Si | — | `Additive` agrega un valor plano al objetivo; `Multiplicative` escala el objetivo por la cantidad. |
| `Target` | `string` | Si | — | Que aspecto de la estadistica modificar. Valor conocido: `"Max"` (modifica el maximo de la estadistica). |

### DamageCalculator

| Campo | Tipo | Requerido | Por defecto | Descripcion |
|-------|------|-----------|-------------|-------------|
| `BaseDamage` | `object` | Si | — | Mapa de ID de tipo de dano a valor de dano (por ejemplo, `{"Fire": 5}`). |

### ModelOverride

| Campo | Tipo | Requerido | Por defecto | Descripcion |
|-------|------|-----------|-------------|-------------|
| `Model` | `string` | Si | — | Ruta al archivo `.blockymodel` de reemplazo. |
| `Texture` | `string` | Si | — | Ruta a la textura de reemplazo. |
| `AnimationSets` | `object` | No | — | Mapa de nombre de estado de animacion a definiciones de animacion (por ejemplo, `Spawn`, `Despawn`). |

## Ejemplos

**Efecto de estado de quemadura** (`Assets/Server/Entity/Effects/Status/Burn.json`):

```json
{
  "ApplicationEffects": {
    "EntityBottomTint": "#100600",
    "EntityTopTint": "#cf2302",
    "ScreenEffect": "ScreenEffects/Fire.png",
    "WorldSoundEventId": "SFX_Effect_Burn_World",
    "LocalSoundEventId": "SFX_Effect_Burn_Local",
    "Particles": [{ "SystemId": "Effect_Fire" }],
    "ModelVFXId": "Burn"
  },
  "DamageCalculatorCooldown": 1,
  "DamageCalculator": {
    "BaseDamage": { "Fire": 5 }
  },
  "DamageEffects": {
    "WorldSoundEventId": "SFX_Effect_Burn_World",
    "PlayerSoundEventId": "SFX_Effect_Burn_Local"
  },
  "OverlapBehavior": "Overwrite",
  "Debuff": true,
  "StatusEffectIcon": "UI/StatusEffects/Burn.png",
  "Duration": 3,
  "DeathMessageKey": "server.general.deathCause.burn"
}
```

**Mejora de comida con aumento de salud maxima** (`Assets/Server/Entity/Effects/Food/Boost/Food_Health_Boost_Large.json`):

```json
{
  "RawStatModifiers": {
    "Health": [
      {
        "Amount": 30,
        "CalculationType": "Additive",
        "Target": "Max"
      }
    ]
  },
  "Duration": 480,
  "OverlapBehavior": "Overwrite",
  "StatusEffectIcon": "UI/StatusEffects/AddHealth/Large.png"
}
```

**Invulnerabilidad de carrera de daga** (`Assets/Server/Entity/Effects/Weapons/Dagger_Dash.json`):

```json
{
  "Duration": 0.25,
  "ApplicationEffects": {
    "Particles": [
      {
        "SystemId": "Daggers_Dash_Straight",
        "TargetEntityPart": "Entity",
        "TargetNodeName": "Hip",
        "PositionOffset": { "Y": 1.0 },
        "Color": "#d7e5ec"
      }
    ],
    "ModelVFXId": "Dagger_Dash"
  },
  "OverlapBehavior": "Extend",
  "Invulnerable": true
}
```

## Paginas Relacionadas

- [Estadisticas de Entidad](/es/hytale-modding-docs/reference/combat-and-projectiles/entity-stats) — estadisticas modificadas por efectos
- [Tipos de Dano](/es/hytale-modding-docs/reference/combat-and-projectiles/damage-types) — IDs de tipo de dano usados en `DamageCalculator`
- [Configuraciones de Proyectiles](/es/hytale-modding-docs/reference/combat-and-projectiles/projectile-configs) — proyectiles que aplican efectos al impactar
