---
title: NPC Shops and Trading
description: Step-by-step tutorial for setting up NPC barter shops with fixed and pool-based trading slots, stock limits, and refresh intervals.
sidebar:
  order: 3
---

## Goal

Create a custom NPC merchant with a **barter shop** that offers both fixed trades (always available) and randomised pool trades (rotating stock). You will build the shop definition, configure stock limits and refresh intervals, and connect the shop to an NPC role.

## What You'll Learn

- How barter shop definitions control NPC trading inventories
- How `Fixed` trade slots offer consistent, always-available trades
- How `Pool` trade slots create rotating random selections with weights
- How `Stock`, `RefreshInterval`, and `RestockHour` manage inventory and resets
- How to connect a shop to an NPC role

## Prerequisites

- A mod folder with a valid `manifest.json` (see [Setup Your Dev Environment](/hytale-modding-docs/tutorials/beginner/setup-dev-environment))
- A custom NPC role (see [Create a Custom NPC](/hytale-modding-docs/tutorials/beginner/create-an-npc))

---

## Barter Shop Overview

Barter shops live in `Assets/Server/BarterShops/`. Each shop is a JSON file that defines what an NPC merchant sells and buys. The vanilla game includes shops like `Kweebec_Merchant.json` (with both fixed and pool-based trades) and `Klops_Merchant.json` (with a single fixed trade).

Hytale uses a **barter** system rather than a currency system -- players trade items directly for other items. Each trade has an `Input` (what the player pays) and an `Output` (what the player receives).

---

## Step 1: Create the Shop Definition

Create your shop file at:

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

### Top-level shop fields

| Field | Purpose |
|-------|---------|
| `DisplayNameKey` | Translation key for the shop title shown in the trading UI |
| `RefreshInterval.Days` | Number of in-game days between stock refreshes. The Kweebec Merchant uses 3 days, Klops uses 1 day |
| `RestockHour` | Hour of day (0-24) when the restock happens. `6` = 6 AM |
| `TradeSlots` | Array of trade slot definitions. Each slot is either `Fixed` or `Pool` |

---

## Step 2: Understanding Fixed Trade Slots

Fixed slots always appear in the shop UI and offer the same trade every restock cycle.

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

### Fixed trade fields

| Field | Purpose |
|-------|---------|
| `Type` | Must be `"Fixed"` |
| `Trade.Output` | The item and quantity the player receives |
| `Trade.Input` | Array of items the player must pay. Multiple entries require all items |
| `Trade.Stock` | Number of times this trade can be completed before the slot is empty. Restocked on the refresh interval |

### Multiple input items

A trade can require multiple different items as payment:

```json
"Input": [
  { "ItemId": "Ingredient_Crystal_Cyan", "Quantity": 10 },
  { "ItemId": "Ingredient_Life_Essence", "Quantity": 5 }
]
```

The player must provide both items to complete the trade.

---

## Step 3: Understanding Pool Trade Slots

Pool slots randomly select a subset of trades from a larger pool on each restock. This creates a rotating inventory that encourages players to check back regularly.

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

### Pool trade fields

| Field | Purpose |
|-------|---------|
| `Type` | Must be `"Pool"` |
| `SlotCount` | Number of trades randomly selected from the pool on each restock. Must be less than or equal to the total number of trades in the pool |
| `Trades` | Array of possible trades to choose from |
| `Trades[].Weight` | Relative probability of this trade being selected. Higher weight = more likely to appear. The Kweebec Merchant uses weights from 20 to 50 |
| `Trades[].Stock` | For pool trades, this is an array: `[fixed]` for exact stock or `[min, max]` for random stock amount |

### Stock as an array

In pool trades, `Stock` uses an array format:

| Format | Meaning |
|--------|---------|
| `[1]` | Exactly 1 in stock per restock |
| `[4, 8]` | Random stock between 4 and 8 per restock |
| `[10, 20]` | Random stock between 10 and 20 per restock |

Compare to fixed trades where `Stock` is a simple integer.

---

## Step 4: Connect the Shop to an NPC Role

The barter shop is connected to an NPC role definition. The NPC role must reference the shop file. In your NPC role:

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

The `BarterShop` field references the shop file by name (without `.json`). The engine resolves this from `Assets/Server/BarterShops/`.

---

## Step 5: Add Translation Keys

```
YourMod/Assets/Languages/en-US.lang
```

```
server.barter.crystal_merchant.title=Crystal Merchant
server.npcRoles.Crystal_Merchant.name=Crystal Merchant
```

---

## Step 6: Test In-Game

1. Place your mod folder in the server mods directory.
2. Start the server and watch for errors about unknown barter shop IDs or invalid item references.
3. Spawn the Crystal Merchant NPC using the developer spawner.
4. Right-click the NPC to open the trading UI.
5. Verify fixed trade slots appear with the correct items, quantities, and stock.
6. Verify pool trade slots show `SlotCount` randomly selected trades.
7. Purchase items until stock runs out and confirm the slot shows as empty.
8. Advance time past the `RefreshInterval` and `RestockHour`, then reopen the shop.
9. Confirm fixed slots have restocked and pool slots have re-randomised.

**Common errors and fixes:**

| Error | Cause | Fix |
|-------|-------|-----|
| `Unknown barter shop` | `BarterShop` value does not match filename | Ensure the value exactly matches the JSON filename without `.json` |
| Shop UI is empty | `TradeSlots` array is empty or malformed | Verify the JSON structure with at least one trade slot |
| Pool shows fewer trades than expected | `SlotCount` exceeds available trades | Ensure `SlotCount` is less than or equal to the number of entries in `Trades` |
| Trade cannot be completed | Item IDs in `Input` are wrong | Verify all `ItemId` values match real item definitions |
| Shop never restocks | `RefreshInterval` not set | Add `"RefreshInterval": { "Days": 1 }` |

---

## Design Tips

- **Fixed slots** work well for staple items that players always need (basic materials, food)
- **Pool slots** work well for rare items, equipment, and recipes that create excitement when they appear
- Use multiple pool groups to create different rarity tiers (common food pool vs rare recipe pool)
- Keep `Stock` values low for powerful items to prevent players from buying unlimited quantities
- Set `Weight` values proportional to how often you want each trade to appear. The Kweebec Merchant uses weights from 20 (rare recipes) to 50 (common crops)

---

## Next Steps

- [Create a Custom NPC](/hytale-modding-docs/tutorials/beginner/create-an-npc) -- build the NPC role that hosts your shop
- [Custom Loot Tables](/hytale-modding-docs/tutorials/intermediate/custom-loot-tables) -- set up drops for items your shop sells
- [Create a Crafting Bench](/hytale-modding-docs/tutorials/intermediate/create-a-crafting-bench) -- let players craft the items your merchant trades for
