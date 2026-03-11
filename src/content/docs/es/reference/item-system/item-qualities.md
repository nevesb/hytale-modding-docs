---
title: Calidades de Objetos
description: Referencia de las definiciones de niveles de calidad (rareza) de objetos en Hytale, incluyendo texturas de tooltip, texturas de ranura, colores de texto y sistemas de partículas de drop.
---

## Descripción General

Las calidades de objetos definen los niveles de rareza mostrados en los objetos a lo largo de la interfaz de Hytale. Cada archivo de calidad especifica un valor numérico, texturas de tooltip y ranura, un color de texto de visualización, una clave de localización y el efecto de partículas mostrado cuando el objeto cae al mundo. El campo `Quality` en una definición de objeto referencia uno de estos IDs de calidad por nombre de archivo.

## Ubicación del Archivo

```
Assets/Server/Item/Qualities/<QualityId>.json
```

Archivos de calidad disponibles:
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

## Esquema

| Campo | Tipo | Requerido | Por Defecto | Descripción |
|-------|------|-----------|-------------|-------------|
| `QualityValue` | number | Sí | — | Rango numérico de este nivel de calidad. Valores más altos indican mayor rareza. Junk=0, Common=1, Uncommon=2, Rare=3, Epic=4, Legendary=5, Tool=9, Developer=10, Template=10. |
| `ItemTooltipTexture` | string | Sí | — | Ruta a la textura de fondo usada para el panel de tooltip de esta calidad. |
| `ItemTooltipArrowTexture` | string | No | — | Ruta a la textura de flecha/puntero en el panel de tooltip. |
| `SlotTexture` | string | Sí | — | Ruta a la textura de borde de ranura de inventario para objetos de esta calidad. |
| `BlockSlotTexture` | string | No | — | Ruta a la textura de ranura usada en contextos de colocación de bloques. |
| `SpecialSlotTexture` | string | No | — | Ruta a la textura de ranura usada en ranuras especiales de la interfaz (ej. ranuras de equipamiento). |
| `TextColor` | string | Sí | — | Cadena de color hexadecimal para el texto del nombre del objeto en tooltips e interfaz (ej. `"#bb8a2c"`). |
| `LocalizationKey` | string | Sí | — | Clave de localización para la etiqueta de calidad mostrada en el tooltip (ej. `"server.general.qualities.Legendary"`). |
| `VisibleQualityLabel` | boolean | Sí | — | Si la etiqueta del nombre de calidad se muestra en el tooltip del objeto. |
| `RenderSpecialSlot` | boolean | Sí | — | Si se renderiza la textura de borde de ranura especial para objetos de esta calidad. |
| `ItemEntityConfig` | object | No | — | Configuración para la entidad del objeto soltado. Contiene `ParticleSystemId` (string) — el efecto de partículas reproducido cuando este objeto está en el suelo. |
| `HideFromSearch` | boolean | No | `false` | Cuando es `true`, los objetos de esta calidad se ocultan de los resultados de búsqueda (usado para la calidad Template). |

## Niveles de Calidad

| ID de Calidad | QualityValue | TextColor | Sistema de Partículas |
|---------------|-------------|-----------|----------------------|
| `Junk` | 0 | `#c9d2dd` | — |
| `Common` | 1 | `#c9d2dd` | `Drop_Common` |
| `Uncommon` | 2 | `#3e9049` | `Drop_Uncommon` |
| `Rare` | 3 | `#2770b7` | `Drop_Rare` |
| `Epic` | 4 | `#8b339e` | `Drop_Epic` |
| `Legendary` | 5 | `#bb8a2c` | `Drop_Legendary` |
| `Tool` | 9 | `#269edc` | — |
| `Developer` | 10 | `#bb2f2c` | — |
| `Template` | 10 | `#ce1624` | — |

## Ejemplo

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

## Páginas Relacionadas

- [Definiciones de Objetos](/hytale-modding-docs/reference/item-system/item-definitions) — Donde se establece el campo `Quality` en los objetos
- [Categorías de Objetos](/hytale-modding-docs/reference/item-system/item-categories) — Organización por categoría de objetos en menús
