---
title: Plantillas de NPC
description: Archivos de plantilla base que definen el comportamiento compartido de NPCs y el sistema de herencia de parámetros Reference/Modify.
---

## Descripción general

Las plantillas de NPC son archivos de rol `Abstract` que definen comportamiento, estadísticas y lógica de IA comunes compartidos por una familia de NPCs. Los roles concretos referencian una plantilla a través del campo `Reference` y sobrescriben valores selectivamente vía `Modify`. El sistema de `Parameters` permite que las plantillas declaren valores predeterminados con nombre y documentación que los roles concretos pueden sobrescribir sin cambiar la plantilla en sí.

## Ubicación de archivos

`Assets/Server/NPC/Roles/_Core/Templates/*.json`

## El patrón Reference / Modify

Un archivo de rol `Variant` se vincula a una plantilla y sobrescribe campos específicos:

```json
{
  "Type": "Variant",
  "Reference": "Template_Predator",
  "Modify": {
    "Appearance": "Fox",
    "MaxHealth": 38
  }
}
```

El motor fusiona la definición completa de la plantilla con el bloque `Modify`. Los campos no listados en `Modify` conservan el valor de la plantilla. El valor de `Reference` es el nombre del archivo sin la extensión `.json`.

## El sistema Parameter / Compute

Las plantillas declaran `Parameters` — valores con nombre con un valor predeterminado y una descripción:

```json
{
  "Parameters": {
    "MaxHealth": {
      "Value": 100,
      "Description": "Max health for the NPC"
    },
    "Appearance": {
      "Value": "Bear_Grizzly",
      "Description": "Model to be used"
    }
  }
}
```

Los campos de nivel superior en la plantilla leen de estos parámetros usando la abreviación `Compute`:

```json
{
  "MaxHealth": { "Compute": "MaxHealth" },
  "Appearance": { "Compute": "Appearance" }
}
```

Un rol concreto `Variant` sobrescribe un parámetro proporcionando un nuevo valor en su propio bloque `Parameters` dentro de `Modify`:

```json
{
  "Type": "Variant",
  "Reference": "Template_Predator",
  "Modify": {
    "MaxHealth": 38,
    "Appearance": "Fox"
  },
  "Parameters": {
    "NameTranslationKey": {
      "Value": "server.npcRoles.Fox.name",
      "Description": "Translation key for NPC name display"
    }
  }
}
```

## Esquema — Campos de plantilla (Abstract)

| Field | Type | Descripción |
|-------|------|-------------|
| `Type` | `"Abstract"` | Marca este archivo como una plantilla base no aparecible. |
| `StartState` | string | Estado inicial de IA, p.ej. `"Idle"`. |
| `Parameters` | object | Definiciones de parámetros con nombre. Cada entrada tiene `Value`, `TypeHint` opcional y `Description`. |
| `Appearance` | Compute | Resuelto desde `Parameters.Appearance`. |
| `MaxHealth` | Compute | Resuelto desde `Parameters.MaxHealth`. |
| `DropList` | Compute | Resuelto desde `Parameters.DropList`. |
| `NameTranslationKey` | Compute | Resuelto desde `Parameters.NameTranslationKey`. |
| `MotionControllerList` | array | Controladores de locomoción (Walk, Fly, Swim). |
| `Instructions` | array | Árbol de comportamiento de IA completo compartido por todas las variantes. |
| `KnockbackScale` | number | Multiplicador de retroceso predeterminado. |
| `DisableDamageGroups` | string[] | Grupos de daño bloqueados por defecto. |

## Plantillas base disponibles

| Plantilla | Familia de comportamiento | Valores predeterminados clave |
|-----------|--------------------------|-------------------------------|
| `Template_Predator` | Cazador agresivo, ataca y luego huye si se siente amenazado | `ViewRange: 24`, `AlertedRange: 28`, `FleeIfNotThreatened: true` |
| `Template_Animal_Neutral` | Animal presa pasivo, huye cuando se siente amenazado | `ViewRange: 16`, `AlertedRange: 18`, `StartState: Idle` |
| `Template_Livestock` | Animal de granja domesticable con pastoreo y producción | `AlertedActionRange: 6`, `GrazingBlockSet: Grass` |
| `Template_Birds_Passive` | Ave pasiva voladora con comportamiento de bandada | `FlockArray: ["Template_Birds_Passive"]`, `MotionControllerList: [Fly]` |
| `Template_Intelligent` | NPC de facción con IA de combate y llamada de ayuda | `AlertedRange: 45`, `ChanceToBeAlertedWhenReceivingCallForHelp: 70` |
| `Template_Beasts_Passive_Critter` | Criatura pasiva pequeña | Estadísticas mínimas, comportamiento de manada a escala de criatura |
| `Template_Edible_Critter` | Criatura pasiva que puede ser comida | Extiende criatura con interacción de alimento |
| `Template_Spirit` | Entidad espiritual con movimiento especial | Locomoción espiritual, partículas predeterminadas |
| `Template_Summoned_Ally` | Invocación aliada del jugador | Actitud amistosa hacia el jugador por defecto |
| `Template_Swimming_Aggressive` | NPC acuático agresivo | Locomoción acuática, IA hostil |
| `Template_Swimming_Passive` | NPC acuático pasivo | Locomoción acuática, comportamiento de huida |
| `Template_Temple` | NPC guardián del templo | IA de guardián, salud alta |

## Ejemplo — Template_Animal_Neutral (abreviado)

Esta es la plantilla de la que heredan `Chicken`, `Deer`, `Moose` y otros animales neutrales:

```json
{
  "Type": "Abstract",
  "StartState": "Idle",
  "Parameters": {
    "Appearance": {
      "Value": "Deer_Stag",
      "Description": "The NPC's model."
    },
    "ViewRange": {
      "Value": 16,
      "Description": "The view distance of the NPC, in blocks."
    },
    "ViewSector": {
      "Value": 180,
      "Description": "The view sector of the NPC, in degrees."
    },
    "HearingRange": {
      "Value": 8,
      "Description": "The hearing distance of the NPC, in blocks."
    },
    "AbsoluteDetectionRange": {
      "Value": 4,
      "Description": "The range at which a target is guaranteed to be detected, in blocks."
    },
    "AlertedRange": {
      "Value": 18,
      "Description": "The range within which the target can be seen when alerted, in blocks."
    },
    "AlertedActionRange": {
      "Value": 8,
      "Description": "The range at which an NPC will react to players, in blocks."
    },
    "DropList": {
      "Value": "Empty",
      "Description": "The NPC's drop list."
    },
    "AttractiveItemSet": {
      "Value": [],
      "TypeHint": "String",
      "Description": "Items that are deemed attractive when held nearby."
    },
    "MaxHealth": {
      "Value": 100,
      "Description": "Max health for the NPC"
    },
    "NameTranslationKey": {
      "Value": "server.npcRoles.Template.name",
      "Description": "Translation key for NPC name display"
    }
  }
}
```

## Páginas relacionadas

- [Roles de NPC](/hytale-modding-docs/reference/npc-system/npc-roles) — Esquema completo de archivos de rol y ejemplos de NPCs concretos
- [Toma de decisiones del NPC](/hytale-modding-docs/reference/npc-system/npc-decision-making) — Tipos de condiciones de IA usados dentro de las plantillas
- [Herencia y plantillas](/hytale-modding-docs/reference/concepts/inheritance-and-templates) — Herencia general de plantillas en todos los tipos de configuración
