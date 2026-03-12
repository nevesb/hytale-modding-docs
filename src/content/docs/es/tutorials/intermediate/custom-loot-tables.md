---
title: Tablas de Botín Personalizadas
description: Tutorial paso a paso para crear tablas de botín y drops con entradas ponderadas, contenedores anidados y drops condicionales.
sidebar:
  order: 2
---

## Objetivo

Crear un conjunto de tablas de botín personalizadas que demuestren todo el rango del sistema de drops de Hytale. Construirás un drop garantizado, un drop aleatorio ponderado, una tabla anidada con equipamiento raro y una tabla de drops de recolección de recursos.

## Lo que Aprenderás

- Cómo los tipos de `Container` (`Multiple`, `Choice`, `Single`) trabajan juntos para crear lógica de drops
- Cómo `Weight` controla la probabilidad de drops aleatorios
- Cómo anidar contenedores para tablas de botín complejas con drops garantizados y raros
- Cómo `QuantityMin` y `QuantityMax` crean cantidades de drop variables
- Cómo se organizan las diferentes categorías de tablas de drops (NPCs, Wood, Rock, Crop)

## Requisitos Previos

- Una carpeta de mod con un `manifest.json` válido (ver [Configura tu Entorno de Desarrollo](/es/hytale-modding-docs/tutorials/beginner/setup-dev-environment))
- Al menos un objeto personalizado (ver [Crear un Objeto Personalizado](/es/hytale-modding-docs/tutorials/beginner/create-an-item))

---

## Descripción General del Sistema de Drops

Las tablas de drops se encuentran en `Assets/Server/Drops/` y están organizadas por tipo de fuente:

```
Assets/Server/Drops/
  NPCs/
    Beast/
    Boss/
    Critter/
    Elemental/
    Intelligent/
      Feran/
      Goblin/
      Trork/
    Livestock/
    Undead/
    Void/
  Crop/
  Wood/
  Rock/
  Plant/
  Items/
  Prefabs/
  Traps/
```

Cada tabla de drops es un archivo JSON con un objeto raíz `Container`. El sistema de contenedores utiliza tres tipos que pueden anidarse para crear cualquier lógica de drops.

### Tipos de contenedor

| Tipo | Comportamiento |
|------|----------------|
| `Multiple` | Evalúa **todos** los contenedores hijos en orden. Cada hijo se ejecuta independientemente |
| `Choice` | Elige **uno** de los hijos al azar, ponderado por los valores de `Weight` |
| `Single` | Nodo terminal. Produce el `Item` especificado con una cantidad aleatoria entre `QuantityMin` y `QuantityMax` |

---

## Paso 1: Crear un Drop Garantizado

La tabla de drops más simple garantiza uno o más objetos cada vez. Este patrón es utilizado por `Rock_Crystal_Blue.json` para depósitos de cristal.

Crea:

```
YourMod/Assets/Server/Drops/NPCs/Beast/Drop_Thornbeast.json
```

```json
{
  "Container": {
    "Type": "Multiple",
    "Containers": [
      {
        "Type": "Single",
        "Item": {
          "ItemId": "Ingredient_Hide_Heavy",
          "QuantityMin": 2,
          "QuantityMax": 4
        }
      }
    ]
  }
}
```

Un contenedor `Multiple` con un único hijo `Single` garantiza el drop cada vez. La cantidad se elige aleatoriamente entre `QuantityMin` y `QuantityMax` (inclusive).

---

## Paso 2: Crear una Tabla Multi-Drop con Objetos Garantizados

Este patrón -- utilizado por `Drop_Bear_Grizzly.json` -- garantiza múltiples drops diferentes usando un contenedor `Multiple` con varios hijos:

```
YourMod/Assets/Server/Drops/NPCs/Beast/Drop_Crystalbeast.json
```

```json
{
  "Container": {
    "Type": "Multiple",
    "Containers": [
      {
        "Type": "Choice",
        "Weight": 100,
        "Containers": [
          {
            "Type": "Single",
            "Item": {
              "ItemId": "Ingredient_Hide_Heavy",
              "QuantityMin": 1,
              "QuantityMax": 2
            }
          }
        ]
      },
      {
        "Type": "Choice",
        "Weight": 100,
        "Containers": [
          {
            "Type": "Single",
            "Item": {
              "ItemId": "Food_Wildmeat_Raw",
              "QuantityMin": 2,
              "QuantityMax": 3
            }
          }
        ]
      }
    ]
  }
}
```

El contenedor `Multiple` ejecuta ambos grupos `Choice`. Como cada grupo `Choice` tiene solo una opción con `Weight: 100`, ambos objetos están garantizados. Esta estructura se usa en lugar de dos contenedores `Single` simples porque el campo `Weight` en los contenedores `Choice` también controla si el grupo produce drops -- un `Weight` de 100 significa 100% de probabilidad.

---

## Paso 3: Crear un Drop Aleatorio Ponderado con Botín Raro

Este patrón -- utilizado por `Drop_Trork_Warrior.json` -- combina drops garantizados con equipamiento raro. El contenedor `Choice` elige un hijo basándose en pesos relativos:

```
YourMod/Assets/Server/Drops/NPCs/Intelligent/Drop_Crystal_Guardian.json
```

```json
{
  "Container": {
    "Type": "Multiple",
    "Containers": [
      {
        "Type": "Choice",
        "Weight": 100,
        "Containers": [
          {
            "Type": "Single",
            "Item": {
              "ItemId": "Ingredient_Crystal_Cyan",
              "QuantityMin": 2,
              "QuantityMax": 5
            }
          }
        ]
      },
      {
        "Type": "Choice",
        "Weight": 15,
        "Containers": [
          {
            "Weight": 40,
            "Type": "Single",
            "Item": {
              "ItemId": "Armor_Crystal_Head",
              "QuantityMin": 1,
              "QuantityMax": 1
            }
          },
          {
            "Weight": 40,
            "Type": "Single",
            "Item": {
              "ItemId": "Armor_Crystal_Chest",
              "QuantityMin": 1,
              "QuantityMax": 1
            }
          },
          {
            "Weight": 20,
            "Type": "Single",
            "Item": {
              "ItemId": "Weapon_Sword_Crystal",
              "QuantityMin": 1,
              "QuantityMax": 1
            }
          }
        ]
      }
    ]
  }
}
```

### Cómo funcionan los pesos

El contenedor externo `Multiple` ejecuta ambos grupos:

1. **Grupo 1** (`Weight: 100`): Siempre dropea 2-5 cristales
2. **Grupo 2** (`Weight: 15`): 15% de probabilidad de ejecutarse. Si se ejecuta, elige un objeto:
   - 40% de probabilidad: Casco de Cristal
   - 40% de probabilidad: Pechera de Cristal
   - 20% de probabilidad: Espada de Cristal

Los valores internos de `Weight` son relativos entre sí dentro del grupo `Choice`: 40 + 40 + 20 = 100 total, por lo que la espada tiene una probabilidad de 20/100 = 20% *cuando el grupo se activa*.

La probabilidad total de obtener la espada en cualquier eliminación es: 15% (el grupo se activa) x 20% (la espada es seleccionada) = 3%.

---

## Paso 4: Crear una Tabla de Drops Anidada con Múltiples Resultados

Para escenarios complejos, anida `Multiple` dentro de `Choice` para crear resultados ramificados. Este patrón es utilizado por `Wood_Branch.json`:

```
YourMod/Assets/Server/Drops/Wood/Drop_Crystalwood_Branch.json
```

```json
{
  "Container": {
    "Type": "Choice",
    "Containers": [
      {
        "Type": "Multiple",
        "Weight": 60,
        "Containers": [
          {
            "Type": "Single",
            "Item": {
              "ItemId": "Ingredient_Stick",
              "QuantityMin": 1,
              "QuantityMax": 3
            }
          },
          {
            "Type": "Single",
            "Item": {
              "ItemId": "Ingredient_Crystal_Cyan",
              "QuantityMin": 0,
              "QuantityMax": 1
            }
          }
        ]
      },
      {
        "Type": "Multiple",
        "Weight": 40,
        "Containers": [
          {
            "Type": "Single",
            "Item": {
              "ItemId": "Ingredient_Stick"
            }
          }
        ]
      }
    ]
  }
}
```

Esta tabla tiene dos resultados posibles elegidos por el `Choice` externo:

- **60% de probabilidad**: Dropea 1-3 palos Y 0-1 cristales (ambos objetos del `Multiple`)
- **40% de probabilidad**: Dropea solo 1 palo

Ten en cuenta que cuando `QuantityMin` es 0, hay una posibilidad de que el objeto no produzca nada. Cuando `QuantityMin` y `QuantityMax` se omiten, la cantidad predeterminada es 1.

---

## Paso 5: Crear una Tabla de Drops Vacía

Algunos NPCs (como las Ardillas y Ranas vanilla) no dropean nada. Un objeto vacío logra esto:

```
YourMod/Assets/Server/Drops/NPCs/Critter/Drop_Glowfly.json
```

```json
{}
```

---

## Paso 6: Conectar la Tabla de Drops a un NPC

Las tablas de drops son referenciadas por las definiciones de roles de NPC a través del campo `DropList`. El valor coincide con el nombre del archivo sin `.json`, y el motor busca en todos los directorios bajo `Assets/Server/Drops/`.

En tu archivo de rol de NPC:

```json
{
  "Type": "Variant",
  "Reference": "Template_Predator",
  "Modify": {
    "Appearance": "Bear_Grizzly",
    "DropList": "Drop_Crystal_Guardian",
    "MaxHealth": 80
  }
}
```

El valor de `DropList` `"Drop_Crystal_Guardian"` se resuelve a `Assets/Server/Drops/NPCs/Intelligent/Drop_Crystal_Guardian.json`.

---

## Paso 7: Probar en el Juego

1. Coloca la carpeta de tu mod en el directorio de mods del servidor.
2. Inicia el servidor y observa si hay errores sobre IDs de lista de drops desconocidos o IDs de objetos inválidos.
3. Genera el NPC que usa tu tabla de drops.
4. Elimina al NPC múltiples veces y verifica:
   - Los drops garantizados aparecen cada vez
   - Los drops raros aparecen aproximadamente con la frecuencia esperada
   - Las cantidades caen dentro de los rangos min/max definidos
5. Para drops de recursos (madera, roca), rompe el bloque correspondiente y verifica los drops.

**Errores comunes y soluciones:**

| Error | Causa | Solución |
|-------|-------|----------|
| `Unknown drop list` | Nombre de archivo o directorio incorrecto | Verifica que el archivo de drop exista y que `DropList` coincida con el nombre del archivo sin `.json` |
| `Unknown item id` | Error tipográfico en el ID del objeto en la tabla de drops | Verifica que los valores de `ItemId` coincidan con los nombres de archivo de definición de objetos reales |
| El NPC no dropea nada | Contenedor vacío o `Weight: 0` | Asegúrate de que al menos un contenedor tenga un peso no nulo |
| Siempre la misma cantidad | `QuantityMin` es igual a `QuantityMax` | Establece valores diferentes para drops variables |
| El drop raro nunca aparece | `Weight` demasiado bajo | Aumenta el valor de `Weight` en el contenedor `Choice` o prueba con más eliminaciones |

---

## Próximos Pasos

- [Crear un NPC Personalizado](/es/hytale-modding-docs/tutorials/beginner/create-an-npc) -- construye el NPC que usa tu tabla de drops
- [Reglas de Aparición de NPCs](/es/hytale-modding-docs/tutorials/intermediate/custom-npc-spawning) -- controla dónde aparecen tus NPCs que dropean botín
- [Tiendas de NPCs y Comercio](/es/hytale-modding-docs/tutorials/intermediate/npc-shops-and-trading) -- crea mercaderes que vendan objetos de tus tablas de botín
