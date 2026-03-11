---
title: Conceptos básicos de JSON
description: Cómo Hytale utiliza JSON para la configuración del juego y el modding.
---

## JSON en Hytale

Cada pieza de contenido del juego en Hytale — desde NPCs hasta objetos y generación del mundo — se define en archivos JSON. Comprender los patrones comunes te ayudará a crear mods de manera eficiente.

## Patrones comunes

### Herencia de plantillas

La mayoría de los archivos JSON soportan herencia desde una plantilla usando `Parent` o `Reference`:

```json
{
  "Reference": "Template_Beasts_Passive_Critter",
  "Modify": {
    "Appearance": "Chicken",
    "MaxHealth": 10,
    "DropList": "Drop_Chicken"
  }
}
```

El campo `Reference` apunta a un archivo de plantilla, y `Modify` sobrescribe campos específicos. Esto evita duplicar configuración común entre entidades similares.

### Valores calculados

Algunos campos soportan valores calculados que hacen referencia a parámetros:

```json
{
  "Parameters": {
    "BaseHealth": {
      "Value": 100,
      "Description": "Base health for this NPC"
    }
  },
  "MaxHealth": {
    "Compute": "BaseHealth * 1.5"
  }
}
```

### Selección basada en pesos

Los drops, apariciones y tiendas usan un sistema de pesos para la selección aleatoria:

```json
{
  "Container": {
    "Type": "Choice",
    "Containers": [
      { "Weight": 70, "Item": { "ItemId": "Coin_Gold" } },
      { "Weight": 25, "Item": { "ItemId": "Gem_Ruby" } },
      { "Weight": 5, "Item": { "ItemId": "Sword_Legendary" } }
    ]
  }
}
```

Mayor peso = mayor probabilidad. El total no necesita sumar 100 — los pesos son relativos.

### Encadenamiento de interacciones

Los comportamientos complejos se construyen encadenando interacciones con el campo `Next`:

```json
{
  "Type": "Condition",
  "RequiredGameMode": "Adventure",
  "Next": {
    "Type": "ApplyEffect",
    "EffectId": "Poison",
    "Next": {
      "Type": "Damage",
      "DamageCalculator": {
        "BaseDamage": { "Poison": 5 }
      }
    }
  }
}
```

Cada interacción activa la siguiente en secuencia, creando comportamientos de juego complejos.

### Claves de traducción

El texto visible para el jugador usa claves de localización:

```json
{
  "TranslationProperties": {
    "Name": "server.items.sword_iron.name",
    "Description": "server.items.sword_iron.description"
  }
}
```

El texto real se define en archivos de idioma (`Languages/en-US.lang`):
```
server.items.sword_iron.name=Iron Sword
server.items.sword_iron.description=A sturdy blade forged from iron.
```

## Validación de archivos

Hytale valida los archivos JSON al iniciar el servidor. Errores comunes:
- **Comas finales** — JSON no permite comas después del último elemento
- **Referencias faltantes** — `Parent` o `Reference` apuntando a plantillas inexistentes
- **Tipos de campo inválidos** — Cadena de texto donde se espera un número, o viceversa
- **Campos requeridos faltantes** — Algunos campos son obligatorios dependiendo del tipo de entidad
