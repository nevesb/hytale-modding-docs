---
title: Tiendas de NPCs y Comercio
description: Tutorial paso a paso para configurar tiendas de trueque de NPCs con espacios de comercio fijos y basados en pool, límites de stock e intervalos de reabastecimiento.
---

## Objetivo

Crear un NPC mercader personalizado con una **tienda de trueque** que ofrezca tanto intercambios fijos (siempre disponibles) como intercambios de pool aleatorios (stock rotativo). Construirás la definición de la tienda, configurarás límites de stock e intervalos de reabastecimiento, y conectarás la tienda a un rol de NPC.

## Lo que Aprenderás

- Cómo las definiciones de tiendas de trueque controlan los inventarios de comercio de NPCs
- Cómo los espacios de comercio `Fixed` ofrecen intercambios consistentes y siempre disponibles
- Cómo los espacios de comercio `Pool` crean selecciones aleatorias rotativas con pesos
- Cómo `Stock`, `RefreshInterval` y `RestockHour` gestionan el inventario y los resets
- Cómo conectar una tienda a un rol de NPC

## Requisitos Previos

- Una carpeta de mod con un `manifest.json` válido (ver [Configura tu Entorno de Desarrollo](/es/hytale-modding-docs/tutorials/beginner/setup-dev-environment))
- Un rol de NPC personalizado (ver [Crear un NPC Personalizado](/es/hytale-modding-docs/tutorials/beginner/create-an-npc))

---

## Descripción General de la Tienda de Trueque

Las tiendas de trueque se encuentran en `Assets/Server/BarterShops/`. Cada tienda es un archivo JSON que define lo que un NPC mercader vende y compra. El juego vanilla incluye tiendas como `Kweebec_Merchant.json` (con intercambios fijos y basados en pool) y `Klops_Merchant.json` (con un solo intercambio fijo).

Hytale usa un sistema de **trueque** en lugar de un sistema de moneda -- los jugadores intercambian objetos directamente por otros objetos. Cada intercambio tiene un `Input` (lo que el jugador paga) y un `Output` (lo que el jugador recibe).

---

## Paso 1: Crear la Definición de la Tienda

Crea tu archivo de tienda en:

```
YourMod/Assets/Server/BarterShops/Crystal_Merchant.json
```

```json
{
  "DisplayNameKey": "server.barter.crystal_merchant.title",
  "RefreshInterval": {
    "Days": 2
  },
  "RestockHour": 6,
  "TradeSlots": [
    {
      "Type": "Fixed",
      "Trade": {
        "Output": { "ItemId": "Ingredient_Crystal_Cyan", "Quantity": 5 },
        "Input": [{ "ItemId": "Ingredient_Life_Essence", "Quantity": 25 }],
        "Stock": 20
      }
    },
    {
      "Type": "Fixed",
      "Trade": {
        "Output": { "ItemId": "Ingredient_Bar_Iron", "Quantity": 2 },
        "Input": [{ "ItemId": "Ingredient_Crystal_Cyan", "Quantity": 10 }],
        "Stock": 10
      }
    },
    {
      "Type": "Pool",
      "SlotCount": 3,
      "Trades": [
        {
          "Weight": 40,
          "Output": { "ItemId": "Food_Kebab_Meat", "Quantity": 1 },
          "Input": [{ "ItemId": "Ingredient_Crystal_Cyan", "Quantity": 3 }],
          "Stock": [4, 8]
        },
        {
          "Weight": 30,
          "Output": { "ItemId": "Food_Pie_Apple", "Quantity": 1 },
          "Input": [{ "ItemId": "Ingredient_Crystal_Cyan", "Quantity": 5 }],
          "Stock": [3, 6]
        },
        {
          "Weight": 20,
          "Output": { "ItemId": "Weapon_Sword_Crystal", "Quantity": 1 },
          "Input": [{ "ItemId": "Ingredient_Crystal_Cyan", "Quantity": 30 }],
          "Stock": [1, 2]
        },
        {
          "Weight": 20,
          "Output": { "ItemId": "Armor_Crystal_Chest", "Quantity": 1 },
          "Input": [{ "ItemId": "Ingredient_Crystal_Cyan", "Quantity": 40 }],
          "Stock": [1, 2]
        },
        {
          "Weight": 10,
          "Output": { "ItemId": "Rune_Fire", "Quantity": 1 },
          "Input": [{ "ItemId": "Ingredient_Crystal_Cyan", "Quantity": 50 }],
          "Stock": [1]
        }
      ]
    },
    {
      "Type": "Pool",
      "SlotCount": 2,
      "Trades": [
        {
          "Weight": 30,
          "Output": { "ItemId": "Recipe_Food_Pie_Apple", "Quantity": 1 },
          "Input": [{ "ItemId": "Ingredient_Life_Essence_Concentrated", "Quantity": 2 }],
          "Stock": [1]
        },
        {
          "Weight": 30,
          "Output": { "ItemId": "Recipe_Food_Pie_Pumpkin", "Quantity": 1 },
          "Input": [{ "ItemId": "Ingredient_Life_Essence_Concentrated", "Quantity": 2 }],
          "Stock": [1]
        },
        {
          "Weight": 20,
          "Output": { "ItemId": "Recipe_Food_Pie_Meat", "Quantity": 1 },
          "Input": [{ "ItemId": "Ingredient_Life_Essence_Concentrated", "Quantity": 3 }],
          "Stock": [1]
        }
      ]
    }
  ]
}
```

### Campos de nivel superior de la tienda

| Campo | Propósito |
|-------|-----------|
| `DisplayNameKey` | Clave de traducción para el título de la tienda mostrado en la interfaz de comercio |
| `RefreshInterval.Days` | Número de días del juego entre reabastecimientos de stock. El Mercader Kweebec usa 3 días, Klops usa 1 día |
| `RestockHour` | Hora del día (0-24) cuando ocurre el reabastecimiento. `6` = 6 AM |
| `TradeSlots` | Array de definiciones de espacios de comercio. Cada espacio es `Fixed` o `Pool` |

---

## Paso 2: Entendiendo los Espacios de Comercio Fijos

Los espacios fijos siempre aparecen en la interfaz de la tienda y ofrecen el mismo intercambio en cada ciclo de reabastecimiento.

```json
{
  "Type": "Fixed",
  "Trade": {
    "Output": { "ItemId": "Ingredient_Crystal_Cyan", "Quantity": 5 },
    "Input": [{ "ItemId": "Ingredient_Life_Essence", "Quantity": 25 }],
    "Stock": 20
  }
}
```

### Campos de comercio fijo

| Campo | Propósito |
|-------|-----------|
| `Type` | Debe ser `"Fixed"` |
| `Trade.Output` | El objeto y cantidad que el jugador recibe |
| `Trade.Input` | Array de objetos que el jugador debe pagar. Múltiples entradas requieren todos los objetos |
| `Trade.Stock` | Número de veces que este intercambio puede completarse antes de que el espacio esté vacío. Se reabastece en el intervalo de reabastecimiento |

### Múltiples objetos de entrada

Un intercambio puede requerir múltiples objetos diferentes como pago:

```json
"Input": [
  { "ItemId": "Ingredient_Crystal_Cyan", "Quantity": 10 },
  { "ItemId": "Ingredient_Life_Essence", "Quantity": 5 }
]
```

El jugador debe proporcionar ambos objetos para completar el intercambio.

---

## Paso 3: Entendiendo los Espacios de Comercio Pool

Los espacios pool seleccionan aleatoriamente un subconjunto de intercambios de un pool más grande en cada reabastecimiento. Esto crea un inventario rotativo que anima a los jugadores a volver regularmente.

```json
{
  "Type": "Pool",
  "SlotCount": 3,
  "Trades": [
    {
      "Weight": 40,
      "Output": { "ItemId": "Food_Kebab_Meat", "Quantity": 1 },
      "Input": [{ "ItemId": "Ingredient_Crystal_Cyan", "Quantity": 3 }],
      "Stock": [4, 8]
    },
    {
      "Weight": 10,
      "Output": { "ItemId": "Rune_Fire", "Quantity": 1 },
      "Input": [{ "ItemId": "Ingredient_Crystal_Cyan", "Quantity": 50 }],
      "Stock": [1]
    }
  ]
}
```

### Campos de comercio pool

| Campo | Propósito |
|-------|-----------|
| `Type` | Debe ser `"Pool"` |
| `SlotCount` | Número de intercambios seleccionados aleatoriamente del pool en cada reabastecimiento. Debe ser menor o igual al número total de intercambios en el pool |
| `Trades` | Array de intercambios posibles para elegir |
| `Trades[].Weight` | Probabilidad relativa de que este intercambio sea seleccionado. Mayor peso = más probabilidad de aparecer. El Mercader Kweebec usa pesos de 20 a 50 |
| `Trades[].Stock` | Para intercambios pool, esto es un array: `[fijo]` para stock exacto o `[min, max]` para cantidad de stock aleatoria |

### Stock como array

En intercambios pool, `Stock` usa un formato de array:

| Formato | Significado |
|---------|-------------|
| `[1]` | Exactamente 1 en stock por reabastecimiento |
| `[4, 8]` | Stock aleatorio entre 4 y 8 por reabastecimiento |
| `[10, 20]` | Stock aleatorio entre 10 y 20 por reabastecimiento |

Compara con intercambios fijos donde `Stock` es un entero simple.

---

## Paso 4: Conectar la Tienda a un Rol de NPC

La tienda de trueque se conecta a una definición de rol de NPC. El rol de NPC debe referenciar el archivo de tienda. En tu rol de NPC:

```
YourMod/Assets/Server/NPC/Roles/MyMod/Crystal_Merchant.json
```

```json
{
  "Type": "Variant",
  "Reference": "Template_Intelligent",
  "Modify": {
    "Appearance": "Kweebec_Elder",
    "MaxHealth": 100,
    "BarterShop": "Crystal_Merchant",
    "NameTranslationKey": {
      "Compute": "NameTranslationKey"
    }
  },
  "Parameters": {
    "NameTranslationKey": {
      "Value": "server.npcRoles.Crystal_Merchant.name",
      "Description": "Translation key for NPC name"
    }
  }
}
```

El campo `BarterShop` referencia el archivo de tienda por nombre (sin `.json`). El motor lo resuelve desde `Assets/Server/BarterShops/`.

---

## Paso 5: Agregar Claves de Traducción

```
YourMod/Assets/Languages/en-US.lang
```

```
server.barter.crystal_merchant.title=Crystal Merchant
server.npcRoles.Crystal_Merchant.name=Crystal Merchant
```

---

## Paso 6: Probar en el Juego

1. Coloca la carpeta de tu mod en el directorio de mods del servidor.
2. Inicia el servidor y observa si hay errores sobre IDs de tienda de trueque desconocidos o referencias de objetos inválidas.
3. Genera el NPC Mercader de Cristal usando el spawner del desarrollador.
4. Haz clic derecho en el NPC para abrir la interfaz de comercio.
5. Verifica que los espacios de comercio fijos aparezcan con los objetos, cantidades y stock correctos.
6. Verifica que los espacios de comercio pool muestren `SlotCount` intercambios seleccionados aleatoriamente.
7. Compra objetos hasta que el stock se agote y confirma que el espacio se muestra como vacío.
8. Avanza el tiempo más allá del `RefreshInterval` y `RestockHour`, luego reabre la tienda.
9. Confirma que los espacios fijos se han reabastecido y los espacios pool se han re-aleatorizado.

**Errores comunes y soluciones:**

| Error | Causa | Solución |
|-------|-------|----------|
| `Unknown barter shop` | El valor de `BarterShop` no coincide con el nombre del archivo | Asegúrate de que el valor coincida exactamente con el nombre del archivo JSON sin `.json` |
| La interfaz de la tienda está vacía | El array `TradeSlots` está vacío o malformado | Verifica la estructura JSON con al menos un espacio de comercio |
| El pool muestra menos intercambios de lo esperado | `SlotCount` excede los intercambios disponibles | Asegúrate de que `SlotCount` sea menor o igual al número de entradas en `Trades` |
| El intercambio no se puede completar | Los IDs de objetos en `Input` son incorrectos | Verifica que todos los valores de `ItemId` coincidan con definiciones de objetos reales |
| La tienda nunca se reabastece | `RefreshInterval` no establecido | Agrega `"RefreshInterval": { "Days": 1 }` |

---

## Consejos de Diseño

- Los **espacios fijos** funcionan bien para objetos básicos que los jugadores siempre necesitan (materiales básicos, comida)
- Los **espacios pool** funcionan bien para objetos raros, equipamiento y recetas que generan emoción cuando aparecen
- Usa múltiples grupos pool para crear diferentes niveles de rareza (pool de comida común vs pool de recetas raras)
- Mantén los valores de `Stock` bajos para objetos poderosos para evitar que los jugadores compren cantidades ilimitadas
- Establece valores de `Weight` proporcionales a la frecuencia con la que quieres que aparezca cada intercambio. El Mercader Kweebec usa pesos de 20 (recetas raras) a 50 (cultivos comunes)

---

## Próximos Pasos

- [Crear un NPC Personalizado](/es/hytale-modding-docs/tutorials/beginner/create-an-npc) -- construye el rol de NPC que aloja tu tienda
- [Tablas de Botín Personalizadas](/es/hytale-modding-docs/tutorials/intermediate/custom-loot-tables) -- configura drops para los objetos que tu tienda vende
- [Crear un Banco de Crafteo](/es/hytale-modding-docs/tutorials/intermediate/create-a-crafting-bench) -- permite a los jugadores fabricar los objetos por los que tu mercader comercia
