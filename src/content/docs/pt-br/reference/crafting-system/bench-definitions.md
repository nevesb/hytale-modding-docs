---
title: Definicoes de Bancadas
description: Referencia para definicoes de itens de bancadas de fabricacao e processamento no Hytale, incluindo configuracao BlockType.Bench, niveis de tier e requisitos de melhoria.
---

## Visao Geral

Bancadas sao itens de bloco colocaveis que habilitam receitas que requerem um ID de bancada especifico. Cada bancada e definida como um arquivo de item padrao em `Assets/Server/Item/Items/Bench/`, com uma secao `BlockType.Bench` descrevendo o tipo operacional da bancada, categorias, eventos sonoros, sistema de tiers e comportamento da UI. O mesmo arquivo de item tambem incorpora a receita usada para fabricar a propria bancada.

## Localizacao dos Arquivos

```
Assets/Server/Item/Items/Bench/
```

Um arquivo JSON por bancada, ex: `Bench_WorkBench.json`, `Bench_Campfire.json`, `Bench_Furnace.json`.

## Schema

### Campos de nivel de item (subconjunto relevante para bancadas)

| Campo | Tipo | Obrigatorio | Padrao | Descricao |
|-------|------|-------------|--------|-----------|
| `TranslationProperties.Name` | `string` | Sim | — | Chave de localizacao para o nome de exibicao da bancada. |
| `BlockType` | `object` | Sim | — | Definicao de comportamento do bloco. Veja abaixo. |
| `Recipe` | `object` | Nao | — | Receita inline para fabricar esta bancada. Usa o schema de receita padrao. |
| `Tags.Type` | `string[]` | Nao | — | Deve incluir `"Bench"` para todos os itens de bancada. |
| `MaxStack` | `number` | Nao | — | Quase sempre `1` para bancadas. |

### Campos de BlockType

| Campo | Tipo | Obrigatorio | Padrao | Descricao |
|-------|------|-------------|--------|-----------|
| `Material` | `string` | Sim | — | Classe de material fisico (ex: `"Solid"`). |
| `DrawType` | `string` | Sim | — | Tipo de renderizacao (ex: `"Model"`). |
| `CustomModel` | `string` | Sim | — | Caminho para o arquivo `.blockymodel`. |
| `Bench` | `BenchConfig` | Sim | — | Configuracao principal da bancada. Veja abaixo. |
| `State` | `object` | Nao | — | Definicoes de estado visual (estados inativo, fabricando, processando). |
| `Gathering.Breaking.GatherType` | `string` | Nao | — | Tipo de coleta ao quebrar o bloco (ex: `"Benches"`). |
| `VariantRotation` | `string` | Nao | — | Variantes de rotacao (ex: `"NESW"`). |

### BenchConfig

| Campo | Tipo | Obrigatorio | Padrao | Descricao |
|-------|------|-------------|--------|-----------|
| `Type` | `"Crafting" \| "Processing"` | Sim | — | Determina se a bancada mostra uma fila de fabricacao ou um pipeline de processamento. |
| `Id` | `string` | Sim | — | Identificador unico da bancada referenciado em `BenchRequirement.Id` nas receitas. |
| `Categories` | `CategoryEntry[]` | Nao | — | Apenas bancadas de fabricacao. Abas de categorias nomeadas mostradas na UI. |
| `TierLevels` | `TierLevel[]` | Nao | — | Definicoes de tier de melhoria. Cada entrada descreve custos de melhoria e bonus. |
| `LocalOpenSoundEventId` | `string` | Nao | — | Som reproduzido localmente quando a UI da bancada abre. |
| `LocalCloseSoundEventId` | `string` | Nao | — | Som reproduzido localmente quando a UI da bancada fecha. |
| `CompletedSoundEventId` | `string` | Nao | — | Som reproduzido quando uma fabricacao e concluida. |
| `FailedSoundEventId` | `string` | Nao | — | Som reproduzido quando uma fabricacao falha. |
| `AllowNoInputProcessing` | `boolean` | Nao | `false` | Apenas bancadas de processamento. Permite que o processamento inicie sem um conjunto completo de entradas. |
| `Fuel` | `FuelSlot[]` | Nao | — | Apenas bancadas de processamento. Define slots de entrada de combustivel. |
| `OutputSlotsCount` | `number` | Nao | — | Apenas bancadas de processamento. Numero de slots de saida. |

### TierLevel

| Campo | Tipo | Obrigatorio | Padrao | Descricao |
|-------|------|-------------|--------|-----------|
| `UpgradeRequirement` | `object` | Nao | — | Materiais e tempo necessarios para atingir este tier. |
| `UpgradeRequirement.Material` | `OutputEntry[]` | Nao | — | Itens consumidos na melhoria. |
| `UpgradeRequirement.TimeSeconds` | `number` | Nao | — | Tempo em segundos para completar a melhoria. |
| `CraftingTimeReductionModifier` | `number` | Nao | `0` | Reducao fracional aplicada a todos os `TimeSeconds` de receitas neste tier (ex: `0.15` = 15% mais rapido). |

## Exemplo

**Bancada de fabricacao** (`Assets/Server/Item/Items/Bench/Bench_WorkBench.json`, condensado):

```json
{
  "TranslationProperties": {
    "Name": "server.items.Bench_WorkBench.name"
  },
  "Recipe": {
    "Input": [
      { "Quantity": 4, "ResourceTypeId": "Wood_Trunk" },
      { "Quantity": 3, "ResourceTypeId": "Rock" }
    ],
    "BenchRequirement": [
      { "Type": "Crafting", "Categories": ["Tools"], "Id": "Fieldcraft" }
    ]
  },
  "BlockType": {
    "Bench": {
      "Type": "Crafting",
      "Id": "Workbench",
      "Categories": [
        { "Id": "Workbench_Survival", "Icon": "Icons/CraftingCategories/Workbench/WeaponsCrude.png", "Name": "server.benchCategories.workbench.survival" },
        { "Id": "Workbench_Tools",    "Icon": "Icons/CraftingCategories/Workbench/Tools.png",       "Name": "server.benchCategories.workbench.tools" }
      ],
      "TierLevels": [
        {
          "CraftingTimeReductionModifier": 0.0,
          "UpgradeRequirement": {
            "Material": [
              { "ItemId": "Ingredient_Bar_Copper", "Quantity": 30 },
              { "ItemId": "Ingredient_Bar_Iron",   "Quantity": 20 }
            ],
            "TimeSeconds": 5.0
          }
        },
        {
          "CraftingTimeReductionModifier": 0.15,
          "UpgradeRequirement": {
            "Material": [
              { "ItemId": "Ingredient_Bar_Thorium", "Quantity": 30 }
            ],
            "TimeSeconds": 10.0
          }
        },
        { "CraftingTimeReductionModifier": 0.3 }
      ],
      "LocalOpenSoundEventId": "SFX_Workbench_Open",
      "CompletedSoundEventId": "SFX_Workbench_Craft"
    }
  },
  "Tags": { "Type": ["Bench"] },
  "MaxStack": 1
}
```

**Bancada de processamento** (`Assets/Server/Item/Items/Bench/Bench_Campfire.json`, condensado):

```json
{
  "BlockType": {
    "Bench": {
      "Type": "Processing",
      "Id": "Campfire",
      "AllowNoInputProcessing": true,
      "Fuel": [
        { "ResourceTypeId": "Fuel", "Icon": "Icons/Processing/FuelSlotIcon.png" }
      ],
      "OutputSlotsCount": 4
    }
  }
}
```

## Paginas Relacionadas

- [Receitas](/pt-br/hytale-modding-docs/reference/crafting-system/recipes) — formato de receita e campo de requisito de bancada
- [Reciclagem](/pt-br/hytale-modding-docs/reference/crafting-system/salvage) — a bancada de Reciclagem e seu formato de receita
