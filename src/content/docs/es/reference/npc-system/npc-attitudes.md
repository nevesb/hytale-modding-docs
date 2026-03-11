---
title: Actitudes de NPC
description: Archivos de actitud que definen cómo un tipo de NPC se relaciona con otros grupos de NPCs y categorías de objetos, controlando combate, evasión y comportamiento social.
---

## Descripción general

Los archivos de actitud definen la disposición social y de combate de un tipo de NPC hacia otros grupos de NPCs y hacia categorías de objetos. Cada archivo corresponde a un rol o familia específica de NPC y lista grupos con nombre mapeados a valores de actitud. El motor lee estos archivos en tiempo de ejecución para determinar si un NPC debe atacar, huir, ignorar o aliarse con otra entidad que detecte.

## Ubicación de archivos

- `Assets/Server/NPC/Attitude/Roles/**/*.json` — Actitud hacia grupos de NPC
- `Assets/Server/NPC/Attitude/Items/**/*.json` — Actitud hacia categorías de objetos

## Esquema

### Archivo de actitud de rol

| Field | Type | Required | Default | Descripción |
|-------|------|----------|---------|-------------|
| `Groups` | object | Sí | — | Mapa de nombres de actitud a arreglos de IDs de grupos de NPC. |

Las claves del objeto `Groups` son nombres de actitud. Los nombres de actitud reconocidos son:

| Actitud | Significado |
|---------|-------------|
| `Friendly` | Este NPC considera a esos grupos como aliados — no los atacará y puede asistirlos. |
| `Hostile` | Este NPC atacará a los miembros de estos grupos a primera vista. |
| `Neutral` | Conciencia pasiva — ni ataca ni asiste. |
| `Ignore` | Ignora completamente a los miembros de estos grupos. |
| `Revered` | Mayor consideración positiva — puede seguirlos o protegerlos. |

### Archivo de actitud de objetos

| Field | Type | Required | Default | Descripción |
|-------|------|----------|---------|-------------|
| `Attitudes` | object | Sí | — | Mapa de nombres de actitud a arreglos de IDs de categorías de objetos. |

Los nombres de actitud de objetos siguen el mismo vocabulario que las actitudes de rol (`Friendly`, `Hostile`, `Dislike`, `Love`, etc.).

## Ejemplos

### Actitud de depredador (archivo de criaturas)

Las criaturas consideran la mayoría de categorías como hostiles (huyen de ellas) pero son amistosas con `Fen_Stalker`.

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

### Actitud de presa (archivo de depredadores)

Los depredadores tratan a las presas como neutrales (rastreables pero no atacadas proactivamente) e ignoran a otros depredadores grandes.

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

### Actitud de facción (Trork)

Los Trorks son amistosos con los de su propia clase, hostiles hacia los Kweebecs, ignoran a los prisioneros y reverencian a su jefe.

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

### Actitudes del mundo viviente

Las actitudes de `LivingWorld/` proporcionan relaciones simples para criaturas ambientales:

**Agresivas** (las criaturas agresivas tratan a las pasivas como hostiles):
```json
{
  "Groups": {
    "Hostile": ["Passive"]
  }
}
```

**Neutrales** (las criaturas neutrales tratan a las agresivas como hostiles):
```json
{
  "Groups": {
    "Hostile": ["Aggressive"]
  }
}
```

### Actitud hacia objetos

```json
{
  "Attitudes": {
    "Dislike": ["Weapon"],
    "Love": ["Food"]
  }
}
```

### Actitud vacía (sin relaciones definidas)

```json
{
  "Groups": {}
}
```

## Relación con los archivos de rol

El parámetro `AttitudeGroup` en la plantilla de un rol (p.ej. `"AttitudeGroup": "Prey"`) declara a qué grupo pertenece ese NPC. Cuando otro NPC lo detecta, el motor busca en el archivo de actitud del NPC que detecta para ver cómo mapea ese grupo.

## Páginas relacionadas

- [Roles de NPC](/hytale-modding-docs/reference/npc-system/npc-roles) — Archivos de rol que declaran `DefaultNPCAttitude`, `DefaultPlayerAttitude` y `AttitudeGroup`
- [Grupos de NPC](/hytale-modding-docs/reference/npc-system/npc-groups) — Definiciones de grupos referenciados en arreglos `Groups`
- [Plantillas de NPC](/hytale-modding-docs/reference/npc-system/npc-templates) — Plantillas que establecen parámetros de actitud predeterminados
