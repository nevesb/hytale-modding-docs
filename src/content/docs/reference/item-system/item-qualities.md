---
title: Item Qualities
description: Reference for item quality (rarity) tier definitions in Hytale, including tooltip textures, slot textures, text colors, and drop particle systems.
---

## Overview

Item qualities define the rarity tiers displayed on items throughout Hytale's UI. Each quality file specifies a numeric value, tooltip and slot textures, a display text color, a localization key, and the particle effect shown when the item drops in the world. The `Quality` field in an item definition references one of these quality IDs by filename.

## File Location

```
Assets/Server/Item/Qualities/<QualityId>.json
```

Available quality files:
```
Junk.json
Common.json
Uncommon.json
Rare.json
Epic.json
Legendary.json
Tool.json
Developer.json
Template.json
Technical.json
```

## Schema

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `QualityValue` | number | Yes | — | Numeric rank of this quality tier. Higher values indicate greater rarity. Junk=0, Common=1, Uncommon=2, Rare=3, Epic=4, Legendary=5, Tool=9, Developer=10, Template=10. |
| `ItemTooltipTexture` | string | Yes | — | Path to the background texture used for this quality's item tooltip panel. |
| `ItemTooltipArrowTexture` | string | No | — | Path to the arrow/pointer texture on the tooltip panel. |
| `SlotTexture` | string | Yes | — | Path to the inventory slot border texture for items of this quality. |
| `BlockSlotTexture` | string | No | — | Path to the slot texture used in block-placement contexts. |
| `SpecialSlotTexture` | string | No | — | Path to the slot texture used in special UI slots (e.g. equipment slots). |
| `TextColor` | string | Yes | — | Hex color string for the item name text in tooltips and UI (e.g. `"#bb8a2c"`). |
| `LocalizationKey` | string | Yes | — | Localization key for the quality label shown in the tooltip (e.g. `"server.general.qualities.Legendary"`). |
| `VisibleQualityLabel` | boolean | Yes | — | Whether the quality name label is shown on the item tooltip. |
| `RenderSpecialSlot` | boolean | Yes | — | Whether to render the special slot border texture for items of this quality. |
| `ItemEntityConfig` | object | No | — | Configuration for the dropped item entity. Contains `ParticleSystemId` (string) — the particle effect played when this item is on the ground. |
| `HideFromSearch` | boolean | No | `false` | When `true`, items of this quality are hidden from search results (used for Template quality). |

## Quality Tiers

| Quality ID | QualityValue | TextColor | Particle System |
|------------|-------------|-----------|-----------------|
| `Junk` | 0 | `#c9d2dd` | — |
| `Common` | 1 | `#c9d2dd` | `Drop_Common` |
| `Uncommon` | 2 | `#3e9049` | `Drop_Uncommon` |
| `Rare` | 3 | `#2770b7` | `Drop_Rare` |
| `Epic` | 4 | `#8b339e` | `Drop_Epic` |
| `Legendary` | 5 | `#bb8a2c` | `Drop_Legendary` |
| `Tool` | 9 | `#269edc` | — |
| `Developer` | 10 | `#bb2f2c` | — |
| `Template` | 10 | `#ce1624` | — |

## Example

`Assets/Server/Item/Qualities/Legendary.json`:

```json
{
  "QualityValue": 5,
  "ItemTooltipTexture": "UI/ItemQualities/Tooltips/ItemTooltipLegendary.png",
  "ItemTooltipArrowTexture": "UI/ItemQualities/Tooltips/ItemTooltipLegendaryArrow.png",
  "SlotTexture": "UI/ItemQualities/Slots/SlotLegendary.png",
  "BlockSlotTexture": "UI/ItemQualities/Slots/SlotLegendary.png",
  "SpecialSlotTexture": "UI/ItemQualities/Slots/SlotLegendary.png",
  "TextColor": "#bb8a2c",
  "LocalizationKey": "server.general.qualities.Legendary",
  "VisibleQualityLabel": true,
  "RenderSpecialSlot": true,
  "ItemEntityConfig": {
    "ParticleSystemId": "Drop_Legendary"
  }
}
```

`Assets/Server/Item/Qualities/Junk.json`:

```json
{
  "QualityValue": 0,
  "ItemTooltipTexture": "UI/ItemQualities/Tooltips/ItemTooltipJunk.png",
  "ItemTooltipArrowTexture": "UI/ItemQualities/Tooltips/ItemTooltipJunkArrow.png",
  "SlotTexture": "UI/ItemQualities/Slots/SlotJunk.png",
  "BlockSlotTexture": "UI/ItemQualities/Slots/SlotJunk.png",
  "SpecialSlotTexture": "UI/ItemQualities/Slots/SlotJunk.png",
  "TextColor": "#c9d2dd",
  "LocalizationKey": "server.general.qualities.Junk",
  "VisibleQualityLabel": false,
  "RenderSpecialSlot": false
}
```

## Related Pages

- [Item Definitions](/hytale-modding-docs/reference/item-system/item-definitions) — Where the `Quality` field is set on items
- [Item Categories](/hytale-modding-docs/reference/item-system/item-categories) — Category organization for items in menus
