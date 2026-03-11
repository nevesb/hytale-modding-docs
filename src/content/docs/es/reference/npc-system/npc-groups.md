---
title: Grupos de NPC
description: Archivos de definición de grupos que reúnen IDs de roles de NPC en conjuntos con nombre usados por tablas de aparición, búsquedas de actitud y volúmenes de supresión.
---

## Descripción general

Los archivos de grupo de NPC definen colecciones con nombre de IDs de roles. Un grupo le da un solo nombre a un conjunto de roles para que las reglas de aparición, tablas de actitud y volúmenes de supresión puedan referirse al conjunto completo sin listar cada rol individual. Los IDs de rol soportan un sufijo comodín `*` para coincidir con todos los roles cuyo nombre comience con un prefijo dado.

## Ubicación de archivos

`Assets/Server/NPC/Groups/**/*.json`

Los grupos se organizan en subdirectorios que reflejan el árbol de `Roles/` (p.ej. `Groups/Creature/Livestock/Chicken.json` para el grupo de manada de gallinas, `Groups/Birds.json` para todas las aves).

## Esquema

| Field | Type | Required | Default | Descripción |
|-------|------|----------|---------|-------------|
| `IncludeRoles` | string[] | Sí | — | Lista de IDs de roles a incluir en este grupo. Soporta un sufijo comodín `*` (p.ej. `"Trilobite*"` coincide con todos los roles cuyo ID comience con `"Trilobite"`). |

## Coincidencia por comodín

Un `*` al final de un ID de rol coincide con todos los roles con ese prefijo. Esto es útil para familias de variantes:

```json
{ "IncludeRoles": ["Trilobite*", "Jellyfish*", "Tang*"] }
```

Esto coincide con `Trilobite`, `Trilobite_Small`, `Jellyfish_Blue`, etc. sin listar cada variante explícitamente.

## Ejemplos

### Grupo de aves

```json
{
  "IncludeRoles": [
    "Bluebird",
    "Crow",
    "Finch_Green",
    "Owl_Brown",
    "Owl_Snow",
    "Parrot",
    "Pigeon",
    "Raven",
    "Sparrow",
    "Woodpecker",
    "Duck",
    "Archaeopteryx",
    "Hawk",
    "Pterodactyl",
    "Vulture"
  ]
}
```

### Grupo acuático (con comodines)

```json
{
  "IncludeRoles": [
    "Eel_Moray",
    "Shark_Hammerhead",
    "Shellfish_Lava",
    "Trilobite*",
    "Whale_Humpback",
    "Bluegill",
    "Frostgill",
    "Minnow",
    "Pike",
    "Piranha_Black",
    "Piranha",
    "Salmon",
    "Snapjaw",
    "Trout_Rainbow",
    "Clownfish",
    "Jellyfish*",
    "Pufferfish",
    "Tang*"
  ]
}
```

### Grupo de especie única (manada de gallinas)

```json
{
  "IncludeRoles": [
    "Chicken",
    "Chicken_Chick"
  ]
}
```

## Cómo se usan los grupos

- Las **reglas de aparición** referencian IDs de grupo en el campo `Flock` de una entrada de aparición de NPC para definir qué roles pueden aparecer juntos.
- Los **archivos de actitud** referencian IDs de grupo en el objeto `Groups` para definir cómo un tipo de NPC se siente acerca de toda una categoría (p.ej. todos los `"Predators"` son `"Hostile"` hacia los animales presa).
- Los **volúmenes de supresión** referencian IDs de grupo en `SuppressedGroups` para evitar que una categoría de NPCs aparezca en un área.

## Páginas relacionadas

- [Roles de NPC](/hytale-modding-docs/reference/npc-system/npc-roles) — Archivos de rol individuales listados dentro de los grupos
- [Reglas de aparición de NPCs](/hytale-modding-docs/reference/npc-system/npc-spawn-rules) — Archivos de aparición que referencian IDs de grupo vía `Flock` y `SuppressedGroups`
- [Actitudes de NPC](/hytale-modding-docs/reference/npc-system/npc-attitudes) — Archivos de actitud que referencian IDs de grupo para definiciones de relaciones
