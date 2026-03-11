---
title: Item Definitions
description: Reference for item definition JSON files in Hytale, covering fields for food, weapons, tools, and all placeable items.
---

## Overview

Item definitions are JSON files that describe every item in Hytale — food, weapons, tools, blocks, and more. Each file lives in a category subfolder under `Assets/Server/Item/Items/` and can extend a parent template to inherit shared fields. The `BlockType` sub-object controls how the item looks when placed in the world.

## File Location

```
Assets/Server/Item/Items/<Category>/<ItemId>.json
```

Examples:
- `Assets/Server/Item/Items/Food/Food_Bread.json`
- `Assets/Server/Item/Items/Weapon/Axe/Weapon_Axe_Copper.json`
- `Assets/Server/Item/Items/Tool/Pickaxe/Tool_Pickaxe_Copper.json`

## Schema

### Top-Level Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Parent` | string | No | — | ID of a template item to inherit fields from (e.g. `"Template_Food"`). |
| `TranslationProperties` | object | Yes | — | Localization keys for the item's display text. |
| `TranslationProperties.Name` | string | Yes | — | Localization key for the item name (e.g. `"server.items.Food_Bread.name"`). |
| `TranslationProperties.Description` | string | No | — | Localization key for the item description. |
| `Quality` | string | No | — | Quality tier ID. One of `Junk`, `Common`, `Uncommon`, `Rare`, `Epic`, `Legendary`, `Tool`, `Developer`, `Template`. |
| `Icon` | string | No | — | Path to the item icon image (e.g. `"Icons/ItemsGenerated/Food_Bread.png"`). |
| `Categories` | string[] | No | — | List of category IDs this item appears in (e.g. `["Items.Foods"]`). |
| `ItemLevel` | number | No | — | Item power level used by progression and crafting unlock systems. |
| `MaxStack` | number | No | — | Maximum number of this item that can stack in one inventory slot. |
| `DropOnDeath` | boolean | No | `false` | Whether this item drops when the carrying player dies. |
| `Scale` | number | No | `1.0` | Visual scale of the item entity when dropped in the world. |
| `Interactions` | object | No | — | Maps interaction slot names (e.g. `Primary`, `Secondary`) to interaction chain IDs. |
| `InteractionVars` | object | No | — | Named interaction variable overrides. Each key is a variable name; each value has an `Interactions` array of inline or parent-referenced chains. |
| `Recipe` | object | No | — | Crafting recipe for this item. See Recipe fields below. |
| `BlockType` | object | No | — | Controls how the item appears when placed as a world block. See BlockType fields below. |
| `ResourceTypes` | object[] | No | — | List of `{ "Id": "<ResourceTypeId>" }` objects. Marks this item as belonging to resource groups used in recipes. |
| `Tags` | object | No | — | Key-value tag groups (e.g. `{ "Type": ["Food"], "Family": ["Axe"] }`). Used for filtering and interactions. |
| `MaxDurability` | number | No | — | Maximum durability for tools and weapons. |
| `DurabilityLossOnHit` | number | No | — | Durability lost per hit for weapons. |
| `Weapon` | object | No | — | Marks this item as a weapon. Usually an empty object `{}` that activates weapon behavior. |
| `Tool` | object | No | — | Tool configuration including `Specs` (gather power per block type) and `DurabilityLossBlockTypes`. |
| `Consumable` | boolean | No | — | Marks this item as a consumable. |
| `PlayerAnimationsId` | string | No | — | Animation set ID used when the player holds this item (e.g. `"Axe"`, `"Item"`). |
| `Model` | string | No | — | Path to the `.blockymodel` file for weapon/tool held-model (e.g. `"Items/Weapons/Axe/Copper.blockymodel"`). |
| `Texture` | string | No | — | Path to the texture used with `Model`. |

### BlockType Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Material` | string | No | — | Physical material type. One of `Solid`, `Fluid`, `Empty`, `Plant`. |
| `DrawType` | string | No | — | Rendering style. Common values: `Model`, `Block`, `Plant`. |
| `Opacity` | string | No | — | Transparency level. One of `Opaque`, `Semitransparent`, `Transparent`. |
| `CustomModel` | string | No | — | Path to the `.blockymodel` file used when the item is placed as a block (e.g. `"Items/Consumables/Food/Bread.blockymodel"`). |
| `CustomModelTexture` | object[] | No | — | Array of `{ "Texture": "<path>", "Weight": <number> }` objects for randomized texture variants. |
| `CustomModelScale` | number | No | `1.0` | Scale multiplier applied to the custom model. |
| `HitboxType` | string | No | — | ID of the hitbox shape (e.g. `"Food_Medium"`, `"Food_Large"`). |
| `RandomRotation` | string | No | — | Rotation randomization mode applied when placed (e.g. `"YawStep1"`). |
| `ParticleColor` | string | No | — | Hex color used for block break particles (e.g. `"#e4cb69"`). |
| `Textures` | object[] | No | — | For placeable blocks: array of texture objects with face keys. Each entry can have `All`, `Sides`, `UpDown`, `Top`, `Bottom`, `North`, `South`, `East`, `West`, and a `Weight` for random variants. |
| `Gathering` | object | No | — | Defines which gather types apply when this block is harvested or broken (`Harvest`, `Soft`, `Breaking`). |

### Recipe Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Input` | object[] | Yes | — | Array of ingredient objects. Each has either `ItemId` or `ResourceTypeId`, plus an optional `Quantity` (defaults to `1`). |
| `Output` | object[] | No | — | Array of output objects with `ItemId` and optional `Quantity`. Defaults to the item itself with quantity 1. |
| `OutputQuantity` | number | No | `1` | Shorthand for setting output quantity when the output item is the definition's own item. |
| `BenchRequirement` | object[] | No | — | Array of bench requirements. Each has `Type` (`"Crafting"`, `"Processing"`, `"StructuralCrafting"`), `Id` (bench ID), and optional `Categories` array. |
| `TimeSeconds` | number | No | `0` | Crafting duration in seconds. |
| `KnowledgeRequired` | boolean | No | `true` | Whether the player must have learned this recipe before crafting it. |

## Example

`Assets/Server/Item/Items/Food/Food_Bread.json`:

```json
{
  "TranslationProperties": {
    "Name": "server.items.Food_Bread.name",
    "Description": "server.items.Food_Bread.description"
  },
  "Parent": "Template_Food",
  "Interactions": {
    "Secondary": "Root_Secondary_Consume_Food_T2"
  },
  "Quality": "Uncommon",
  "Icon": "Icons/ItemsGenerated/Food_Bread.png",
  "BlockType": {
    "Material": "Empty",
    "DrawType": "Model",
    "Opacity": "Semitransparent",
    "CustomModel": "Items/Consumables/Food/Bread.blockymodel",
    "CustomModelTexture": [
      {
        "Texture": "Items/Consumables/Food/Bread_Texture.png",
        "Weight": 1
      }
    ],
    "HitboxType": "Food_Medium",
    "RandomRotation": "YawStep1",
    "CustomModelScale": 0.5,
    "ParticleColor": "#e4cb69"
  },
  "InteractionVars": {
    "Consume_Charge": {
      "Interactions": [
        {
          "Parent": "Consume_Charge_Food_T1_Inner",
          "Effects": {
            "Particles": [
              {
                "SystemId": "Food_Eat",
                "Color": "#DCC15D",
                "TargetNodeName": "Mouth",
                "TargetEntityPart": "Entity"
              }
            ]
          }
        }
      ]
    },
    "Effect": {
      "Interactions": [
        {
          "Type": "ApplyEffect",
          "EffectId": "Food_Instant_Heal_Bread"
        }
      ]
    }
  },
  "Recipe": {
    "Input": [
      {
        "ItemId": "Ingredient_Dough",
        "Quantity": 1
      },
      {
        "ResourceTypeId": "Fuel",
        "Quantity": 3
      }
    ],
    "Output": [
      {
        "ItemId": "Food_Bread"
      }
    ],
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Id": "Cookingbench",
        "Categories": [
          "Baked"
        ]
      }
    ],
    "TimeSeconds": 5
  },
  "Scale": 1.5,
  "ItemLevel": 7,
  "MaxStack": 25,
  "DropOnDeath": true
}
```

## Related Pages

- [Block Definitions](/hytale-modding-docs/reference/item-system/block-definitions) — Block-specific texture and material fields
- [Item Qualities](/hytale-modding-docs/reference/item-system/item-qualities) — Quality tier definitions
- [Item Interactions](/hytale-modding-docs/reference/item-system/item-interactions) — Interaction chain reference
- [Item Categories](/hytale-modding-docs/reference/item-system/item-categories) — Category hierarchy
- [Resource Types](/hytale-modding-docs/reference/item-system/resource-types) — Resource type IDs used in recipes
