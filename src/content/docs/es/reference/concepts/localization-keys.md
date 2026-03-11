---
title: Claves de localización
description: Cómo Hytale maneja la traducción de texto usando archivos de idioma clave-valor.
---

## Descripción general

Todo el texto visible para el jugador en Hytale usa claves de traducción en lugar de cadenas de texto fijas. Esto permite el soporte multiidioma. Las claves se definen en archivos `.lang` dentro de los directorios `Languages/`.

## Ubicación de archivos

- `Server/Languages/*.lang` — Cadenas del lado del servidor (nombres de objetos, nombres de NPCs, texto de misiones)
- `Common/Languages/*.lang` — Cadenas del lado del cliente (etiquetas de UI, tooltips, menús)

## Formato de archivo de idioma

Los archivos de idioma usan un formato simple `clave=valor`, una entrada por línea:

```
server.items.sword_iron.name=Iron Sword
server.items.sword_iron.description=A sturdy blade forged from iron.
server.npc.chicken.name=Chicken
server.npc.bear_grizzly.name=Grizzly Bear
```

## Uso de claves de traducción

### En definiciones de objetos

```json
{
  "TranslationProperties": {
    "Name": "server.items.sword_iron.name",
    "Description": "server.items.sword_iron.description"
  }
}
```

### En roles de NPC

```json
{
  "Modify": {
    "NameTranslationKey": "server.npc.chicken.name"
  }
}
```

### En tipos de portal

```json
{
  "Description": {
    "DisplayName": "server.portals.dungeon_entrance.name",
    "FlavorText": "server.portals.dungeon_entrance.flavor",
    "Tips": [
      "server.portals.dungeon_entrance.tip1",
      "server.portals.dungeon_entrance.tip2"
    ]
  }
}
```

## Convenciones de nombres de claves

| Patrón | Uso |
|--------|-----|
| `server.items.{id}.name` | Nombres visibles de objetos |
| `server.items.{id}.description` | Descripciones de objetos |
| `server.npc.{id}.name` | Nombres visibles de NPCs |
| `server.blocks.{id}.name` | Nombres visibles de bloques |
| `server.portals.{id}.*` | Texto de UI de portales |
| `server.quests.{id}.*` | Texto de misiones |

## Agregar traducciones para mods

Crea un archivo de idioma en el directorio `Server/Languages/` de tu mod:

```
mymod.items.magic_staff.name=Magic Staff
mymod.items.magic_staff.description=A staff imbued with arcane power.
```

Usa un prefijo único (el nombre de tu mod) para evitar conflictos con las claves del juego base.

## Páginas relacionadas

- [Definiciones de objetos](/hytale-modding-docs/reference/item-system/item-definitions/) — uso de TranslationProperties
- [Roles de NPC](/hytale-modding-docs/reference/npc-system/npc-roles/) — NameTranslationKey
