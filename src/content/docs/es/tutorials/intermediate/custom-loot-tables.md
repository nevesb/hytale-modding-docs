---
title: Tablas de Botín Personalizadas
description: Tutorial paso a paso para crear tablas de drops con drops garantizados, objetos raros ponderados y contenedores anidados usando el NPC Slime.
sidebar:
  order: 2
---

## Objetivo

Crear una tabla de drops personalizada para el NPC **Slime** del tutorial [Crear un NPC Personalizado](/hytale-modding-docs/es/tutorials/beginner/create-an-npc/). Construirás un drop garantizado, agregarás un objeto raro ponderado y aprenderás cómo los contenedores anidados crean lógica de botín compleja.

## Lo que Aprenderás

- Cómo los tipos de `Container` (`Multiple`, `Choice`, `Single`) trabajan juntos para crear lógica de drops
- Cómo `Weight` controla la probabilidad de drops aleatorios
- Cómo combinar drops garantizados y raros en una sola tabla
- Cómo `QuantityMin` y `QuantityMax` crean cantidades de drop variables
- Cómo conectar una tabla de drops a un NPC mediante `DropList`

## Requisitos Previos

- Un mod funcional del NPC Slime (ver [Crear un NPC Personalizado](/hytale-modding-docs/es/tutorials/beginner/create-an-npc/))
- El mod del Árbol Encantado instalado (ver [Árboles y Saplings Personalizados](/hytale-modding-docs/es/tutorials/intermediate/custom-trees-and-saplings/)) — usamos su Fruta Encantada como objeto de drop
- El mod del bloque Crystal Glow instalado (ver [Crear un Bloque Personalizado](/hytale-modding-docs/es/tutorials/beginner/create-a-block/)) — lo usamos como drop raro

**Repositorios del mod complementario:**
- [hytale-mods-custom-npc](https://github.com/nevesb/hytale-mods-custom-npc) — Slime NPC v1.0.0 (mod base sin botín)
- [hytale-mods-custom-loot-tables](https://github.com/nevesb/hytale-mods-custom-loot-tables) — Slime NPC v1.1.0 (con tabla de drops de este tutorial)

:::note[Este Tutorial Reemplaza la Tabla de Drops del NPC]
El tutorial [Crear un NPC Personalizado](/hytale-modding-docs/es/tutorials/beginner/create-an-npc/) incluye una tabla de drops básica en el Paso 6. Este tutorial construye una versión más completa que **reemplaza** esa tabla de drops. Después de completar este tutorial, tu Slime usará la nueva tabla de botín.
:::

---

## Descripción General del Sistema de Drops

Las tablas de drops se encuentran en `Server/Drops/` y controlan qué objetos caen cuando un NPC muere, un bloque se rompe o un recurso es recolectado. El juego vanilla las organiza por tipo de fuente:

```
Assets/Server/Drops/
  NPCs/
    Beast/
    Critter/
    Intelligent/
      Feran/
      Trork/
  Crop/
  Wood/
  Rock/
  Plant/
```

Cada tabla de drops es un archivo JSON con un objeto raíz `Container`. El sistema de contenedores usa tres tipos que pueden anidarse para crear cualquier lógica de drops:

### Tipos de Contenedor

| Tipo | Comportamiento |
|------|----------------|
| `Multiple` | Evalúa **todos** los contenedores hijos en orden. Cada hijo se ejecuta independientemente |
| `Choice` | Elige **uno** de los hijos al azar, ponderado por los valores de `Weight`. El `Weight` del propio `Choice` controla si el grupo se activa |
| `Single` | Nodo terminal. Produce el `Item` especificado con una cantidad aleatoria entre `QuantityMin` y `QuantityMax` |

---

## Paso 1: Crear un Drop Garantizado

La tabla de drops más simple garantiza un objeto cada vez. Empecemos haciendo que el Slime siempre deje caer 1 Fruta Encantada — la misma fruta del tutorial [Árboles y Saplings Personalizados](/hytale-modding-docs/es/tutorials/intermediate/custom-trees-and-saplings/).

Crea (o reemplaza) el archivo de tabla de drops:

```
CreateACustomNPC/Server/Drops/Drop_Slime.json
```

```json
{
  "Container": {
    "Type": "Multiple",
    "Containers": [
      {
        "Type": "Single",
        "Item": {
          "ItemId": "Plant_Fruit_Enchanted",
          "QuantityMin": 1,
          "QuantityMax": 1
        }
      }
    ]
  }
}
```

Un contenedor `Multiple` con un único hijo `Single` garantiza el drop cada vez. El `ItemId` debe coincidir con el nombre del archivo de una definición de objeto existente (sin `.json`).

Este es el mismo patrón usado por los depósitos de cristal vanilla. Por ejemplo, `Rock_Crystal_Blue.json` garantiza 4-5 cristales cian:

```json
{
  "Container": {
    "Type": "Multiple",
    "Containers": [
      {
        "Type": "Single",
        "Item": {
          "ItemId": "Ingredient_Crystal_Cyan",
          "QuantityMin": 4,
          "QuantityMax": 5
        }
      }
    ]
  }
}
```

---

## Paso 2: Agregar un Drop Raro de Cristal

Ahora hagamos al Slime más interesante — mantenemos la fruta garantizada, pero agregamos un **10% de probabilidad** de también dejar caer un bloque Crystal Glow del tutorial [Crear un Bloque Personalizado](/hytale-modding-docs/es/tutorials/beginner/create-a-block/).

Actualiza `Server/Drops/Drop_Slime.json`:

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
              "ItemId": "Plant_Fruit_Enchanted",
              "QuantityMin": 1,
              "QuantityMax": 1
            }
          }
        ]
      },
      {
        "Type": "Choice",
        "Weight": 10,
        "Containers": [
          {
            "Type": "Single",
            "Item": {
              "ItemId": "Ore_Crystal_Glow",
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

### Cómo Funcionan los Pesos

El contenedor externo `Multiple` evalúa ambos grupos independientemente:

1. **Grupo 1** (`Weight: 100`): 100% de probabilidad — siempre deja caer 1 Fruta Encantada
2. **Grupo 2** (`Weight: 10`): 10% de probabilidad — a veces también deja caer 1 bloque Crystal Glow

El `Weight` en un contenedor `Choice` controla si ese grupo se activa. `Weight: 100` significa siempre, `Weight: 10` significa 10% de las veces.

Este es el mismo patrón que vanilla usa para drops de equipamiento de NPCs. Por ejemplo, `Drop_Trork_Warrior.json` usa tres grupos:

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
              "ItemId": "Ingredient_Fabric_Scrap_Linen",
              "QuantityMin": 1,
              "QuantityMax": 3
            }
          }
        ]
      },
      {
        "Type": "Choice",
        "Weight": 5,
        "Containers": [
          { "Weight": 25, "Type": "Single", "Item": { "ItemId": "Armor_Trork_Head", "QuantityMin": 1, "QuantityMax": 1 } },
          { "Weight": 25, "Type": "Single", "Item": { "ItemId": "Armor_Trork_Chest", "QuantityMin": 1, "QuantityMax": 1 } },
          { "Weight": 25, "Type": "Single", "Item": { "ItemId": "Armor_Trork_Hands", "QuantityMin": 1, "QuantityMax": 1 } },
          { "Weight": 25, "Type": "Single", "Item": { "ItemId": "Armor_Trork_Legs", "QuantityMin": 1, "QuantityMax": 1 } }
        ]
      },
      {
        "Type": "Choice",
        "Weight": 15,
        "Containers": [
          {
            "Type": "Single",
            "Item": { "ItemId": "Weapon_Battleaxe_Stone_Trork", "QuantityMin": 1, "QuantityMax": 1 }
          }
        ]
      }
    ]
  }
}
```

- **Grupo 1** (`Weight: 100`): Siempre deja caer 1-3 retazos de lino
- **Grupo 2** (`Weight: 5`): 5% de probabilidad de dejar caer una pieza de armadura (cada una con peso interno de 25%)
- **Grupo 3** (`Weight: 15`): 15% de probabilidad de dejar caer un hacha de batalla

Los valores internos de `Weight` dentro de un `Choice` son relativos entre sí: 25 + 25 + 25 + 25 = 100, así que cada pieza de armadura tiene 25% de probabilidad *cuando el grupo se activa*. La probabilidad total de obtener el casco es 5% x 25% = 1.25%.

---

## Paso 3: Conectar la Tabla de Drops al NPC

Las tablas de drops son referenciadas por las definiciones de roles de NPC a través del campo `DropList`. El valor coincide con el nombre del archivo de la tabla de drops sin `.json`.

Abre el Rol de NPC de tu Slime en `Server/NPC/Roles/Slime.json` y agrega el campo `DropList` al bloque `Modify`:

```json {7}
{
  "Type": "Variant",
  "Reference": "Template_Predator",
  "Modify": {
    "Appearance": "Slime",
    "MaxHealth": 75,
    "DropList": "Drop_Slime",
    "KnockbackScale": 0.5,
    "IsMemory": true,
    "MemoriesCategory": "Beast",
    "NameTranslationKey": {
      "Compute": "NameTranslationKey"
    }
  },
  "Parameters": {
    "NameTranslationKey": {
      "Value": "server.npcRoles.Slime.name",
      "Description": "Translation key for NPC name display"
    }
  }
}
```

El `"DropList": "Drop_Slime"` indica al motor que resuelva `Server/Drops/Drop_Slime.json` cuando el NPC muera. Los NPCs vanilla usan el mismo patrón — por ejemplo, `Bear_Grizzly.json` referencia `"Drop_Bear_Grizzly"`.

---

## Paso 4: Contenedores Anidados para Drops Complejos

Para escenarios más complejos, puedes anidar `Multiple` dentro de `Choice` para crear resultados ramificados. Este patrón es usado por el `Wood_Branch.json` vanilla para drops de recursos al romper ramas de madera:

```json
{
  "Container": {
    "Type": "Choice",
    "Containers": [
      {
        "Type": "Multiple",
        "Weight": 50,
        "Containers": [
          {
            "Type": "Single",
            "Item": {
              "ItemId": "Ingredient_Stick",
              "QuantityMin": 0,
              "QuantityMax": 2
            }
          },
          {
            "Type": "Single",
            "Item": {
              "ItemId": "Ingredient_Tree_Sap",
              "QuantityMin": 0,
              "QuantityMax": 1
            }
          }
        ]
      },
      {
        "Type": "Multiple",
        "Weight": 50,
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

- **50% de probabilidad**: Deja caer 0-2 palos **y** 0-1 savia de árbol (ambos objetos del `Multiple`)
- **50% de probabilidad**: Deja caer solo 1 palo

Cuando `QuantityMin` es `0`, hay una posibilidad de que el objeto no produzca nada. Cuando `QuantityMin` y `QuantityMax` se omiten, la cantidad predeterminada es `1`.

:::tip[Resumen de Anidamiento]
- `Multiple` → `Choice`: Cada grupo se evalúa independientemente (garantizado + raro, como nuestro Slime)
- `Choice` → `Multiple`: Se elige un resultado, luego todos sus objetos caen juntos (ramificación, como Wood Branch)
:::

---

## Paso 5: Tablas de Drops Vacías

Algunos NPCs no dejan caer nada. Todos los critters vanilla — Ardillas, Ranas, Geckos, Suricatas — usan un objeto vacío:

```json
{}
```

Así es como tu Slime funcionaba antes de este tutorial — sin un `DropList` en el Rol de NPC, o con una tabla de drops vacía, el NPC no deja caer nada al morir.

---

## Paso 6: Probar en el Juego

1. Copia tu carpeta `CreateACustomNPC/` actualizada a `%APPDATA%/Hytale/UserData/Mods/`

2. Asegúrate de que los mods **CreateACustomBlock** y **CustomTreesAndSaplings** también estén instalados — la tabla de drops referencia objetos de ambos mods

3. Inicia Hytale y entra en **Modo Creativo**

4. Genera y mata al Slime múltiples veces:
   ```text
   /op self
   /npc spawn Slime
   ```

5. Verifica:

![Drops del Slime en el juego — Frutas Encantadas y bloques Crystal Glow en el suelo después de matar varios Slimes](/hytale-modding-docs/images/tutorials/custom-loot-tables/slime-drops.png)

   - Cada muerte deja caer 1 Fruta Encantada (garantizado)
   - Aproximadamente 1 de cada 10 muertes también deja caer un bloque Crystal Glow (10% de probabilidad)
   - Las cantidades son correctas (siempre exactamente 1 de cada uno)

**Errores comunes y soluciones:**

| Error | Causa | Solución |
|-------|-------|----------|
| `Unknown drop list` | Nombre de archivo o ruta incorrecta | Verifica que `Drop_Slime.json` exista en `Server/Drops/` y que `DropList` coincida sin `.json` |
| `Unknown item id` | Error tipográfico en ID de objeto o mod faltante | Verifica que `ItemId` coincida con nombres de archivo reales. Asegúrate de que los mods que proveen esos objetos estén instalados |
| NPC no deja nada | `DropList` faltante en Rol de NPC | Agrega `"DropList": "Drop_Slime"` al bloque `Modify` en `Slime.json` |
| Siempre misma cantidad | `QuantityMin` igual a `QuantityMax` | Establece valores diferentes para drops variables |
| Drop raro nunca aparece | `Weight` muy bajo o mala suerte | `Weight: 10` significa ~10% — mata 20+ Slimes para confirmar |

---

## Referencia de Tablas de Drops Vanilla

Aquí hay un resumen de patrones reales de tablas de drops de los assets del juego:

| Archivo Vanilla | Patrón | Caso de Uso |
|----------------|--------|-------------|
| `Rock_Crystal_Blue.json` | `Multiple` → `Single` | Drop de recurso garantizado |
| `Drop_Bear_Grizzly.json` | `Multiple` → `Choice(100)` + `Choice(100)` | Múltiples drops garantizados |
| `Drop_Trork_Warrior.json` | `Multiple` → `Choice(100)` + `Choice(5)` + `Choice(15)` | Garantizado + botín raro |
| `Wood_Branch.json` | `Choice` → `Multiple(50)` + `Multiple(50)` | Resultados ramificados de recursos |
| `Drop_Frog_*.json` | `{}` | Sin drops |

---

## Próximos Pasos

- [Reglas de Aparición de NPCs Personalizadas](/hytale-modding-docs/es/tutorials/intermediate/custom-npc-spawning/) — controla dónde aparecen tus Slimes que dejan botín
- [Tiendas de NPCs y Comercio](/hytale-modding-docs/es/tutorials/intermediate/npc-shops-and-trading/) — crea mercaderes que vendan objetos de tus tablas de botín
- [Referencia de Tablas de Drops](/hytale-modding-docs/es/reference/economy-and-progression/drop-tables/) — referencia completa del esquema para todos los tipos de contenedores
