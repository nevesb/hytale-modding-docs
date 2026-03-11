---
title: Patrones de etiquetas
description: Sistema de coincidencia lógica de etiquetas utilizado en toda la configuración de Hytale.
---

## Descripción general

Los patrones de etiquetas proporcionan un sistema de lógica booleana para hacer coincidir contenido etiquetado. Usan operadores como `And`, `Or`, `Not` y `Equals` para crear reglas de coincidencia complejas para entornos, bloques, NPCs y otras entidades etiquetadas.

## Ubicación de archivos

`Server/TagPatterns/*.json`

## Operadores

| Operador | Propósito | Campos |
|----------|-----------|--------|
| `Equals` | Coincide con una sola etiqueta | `Tag` |
| `Or` | Coincide con cualquiera de los patrones | `Patterns` (arreglo) |
| `And` | Coincide con todos los patrones | `Patterns` (arreglo) |
| `Not` | Invierte un patrón | `Pattern` (único) |

## Ejemplos

### Coincidencia OR simple

```json
{
  "Op": "Or",
  "Patterns": [
    { "Op": "Equals", "Tag": "Bush" },
    { "Op": "Equals", "Tag": "Seed" }
  ]
}
```

Coincide con cualquier bloque etiquetado como `Bush` o `Seed`.

### AND + NOT complejo

```json
{
  "Op": "And",
  "Patterns": [
    { "Op": "Equals", "Tag": "Caves" },
    {
      "Op": "Not",
      "Pattern": {
        "Op": "Or",
        "Patterns": [
          { "Op": "Equals", "Tag": "Volcanic" },
          { "Op": "Equals", "Tag": "Spiders" },
          { "Op": "Equals", "Tag": "Dungeons" }
        ]
      }
    }
  ]
}
```

Coincide con entornos etiquetados como `Caves` pero NO `Volcanic`, `Spiders` ni `Dungeons`.

## Dónde se usan las etiquetas

- **Audio ambiental** — selecciona sonidos ambientales basados en etiquetas del entorno
- **Aparición de NPCs** — restringe apariciones a biomas etiquetados específicos
- **Interacciones de bloques** — coincide tipos de bloques por grupos de etiquetas

## Páginas relacionadas

- [Entornos](/hytale-modding-docs/reference/world-and-environment/environments/) — uso de etiquetas de entorno
- [Reglas de aparición de NPCs](/hytale-modding-docs/reference/npc-system/npc-spawn-rules/) — filtrado de apariciones por etiquetas
