---
title: Qualidades de Itens
description: Referência para definições de níveis de qualidade (raridade) de itens no Hytale, incluindo texturas de tooltip, texturas de slot, cores de texto e sistemas de partículas de drop.
---

## Visão Geral

Qualidades de itens definem os níveis de raridade exibidos nos itens em toda a UI do Hytale. Cada arquivo de qualidade especifica um valor numérico, texturas de tooltip e slot, uma cor de texto de exibição, uma chave de localização e o efeito de partícula mostrado quando o item é dropado no mundo. O campo `Quality` em uma definição de item referencia um desses IDs de qualidade pelo nome do arquivo.

## Localização dos Arquivos

```
Assets/Server/Item/Qualities/<QualityId>.json
```

Arquivos de qualidade disponíveis:
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

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `QualityValue` | number | Sim | — | Classificação numérica deste nível de qualidade. Valores maiores indicam maior raridade. Junk=0, Common=1, Uncommon=2, Rare=3, Epic=4, Legendary=5, Tool=9, Developer=10, Template=10. |
| `ItemTooltipTexture` | string | Sim | — | Caminho para a textura de fundo usada no painel de tooltip desta qualidade. |
| `ItemTooltipArrowTexture` | string | Não | — | Caminho para a textura de seta/ponteiro no painel do tooltip. |
| `SlotTexture` | string | Sim | — | Caminho para a textura de borda do slot de inventário para itens desta qualidade. |
| `BlockSlotTexture` | string | Não | — | Caminho para a textura do slot usada em contextos de colocação de bloco. |
| `SpecialSlotTexture` | string | Não | — | Caminho para a textura do slot usada em slots especiais da UI (ex.: slots de equipamento). |
| `TextColor` | string | Sim | — | String de cor hex para o texto do nome do item em tooltips e UI (ex.: `"#bb8a2c"`). |
| `LocalizationKey` | string | Sim | — | Chave de localização para o rótulo de qualidade mostrado no tooltip (ex.: `"server.general.qualities.Legendary"`). |
| `VisibleQualityLabel` | boolean | Sim | — | Se o rótulo do nome da qualidade é mostrado no tooltip do item. |
| `RenderSpecialSlot` | boolean | Sim | — | Se deve renderizar a textura de borda do slot especial para itens desta qualidade. |
| `ItemEntityConfig` | object | Não | — | Configuração para a entidade do item dropado. Contém `ParticleSystemId` (string) — o efeito de partícula reproduzido quando este item está no chão. |
| `HideFromSearch` | boolean | Não | `false` | Quando `true`, itens desta qualidade ficam ocultos dos resultados de busca (usado para qualidade Template). |

## Níveis de Qualidade

| ID da Qualidade | QualityValue | TextColor | Sistema de Partículas |
|-----------------|-------------|-----------|----------------------|
| `Junk` | 0 | `#c9d2dd` | — |
| `Common` | 1 | `#c9d2dd` | `Drop_Common` |
| `Uncommon` | 2 | `#3e9049` | `Drop_Uncommon` |
| `Rare` | 3 | `#2770b7` | `Drop_Rare` |
| `Epic` | 4 | `#8b339e` | `Drop_Epic` |
| `Legendary` | 5 | `#bb8a2c` | `Drop_Legendary` |
| `Tool` | 9 | `#269edc` | — |
| `Developer` | 10 | `#bb2f2c` | — |
| `Template` | 10 | `#ce1624` | — |

## Exemplo

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

- [Definições de Itens](/hytale-modding-docs/reference/item-system/item-definitions) — Onde o campo `Quality` é definido nos itens
- [Categorias de Itens](/hytale-modding-docs/reference/item-system/item-categories) — Organização de categorias para itens nos menus
