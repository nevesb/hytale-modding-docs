---
title: Criar um Bloco Personalizado
description: Construa um bloco personalizado no Blockbench, conecte-o ao JSON do Hytale e teste-o no jogo.
---

## Objetivo

Neste tutorial você vai montar um fluxo real de bloco personalizado:

1. modelar o bloco no Blockbench
2. exportar o `.blockymodel` de runtime
3. salvar a textura e o ícone
4. registrar o bloco e o item em JSON
5. empacotar o mod e testar no jogo

O exemplo usado aqui é um bloco de cristal brilhante chamado `Block_Crystal_Glow`.

Repositório do exemplo:

- `https://github.com/nevesb/hytale-mods-custom-block`

Arquivos principais desse repositório:

- `https://github.com/nevesb/hytale-mods-custom-block/blob/master/source-assets/blockbench/Crystal_Glow.bbmodel`
- `https://github.com/nevesb/hytale-mods-custom-block/blob/master/Assets/Common/Blocks/HytaleModdingManual/Crystal_Glow.blockymodel`
- `https://github.com/nevesb/hytale-mods-custom-block/blob/master/Assets/Common/BlockTextures/HytaleModdingManual/Crystal_Glow.png`
- `https://github.com/nevesb/hytale-mods-custom-block/blob/master/Assets/Server/Item/Block/Blocks/HytaleModdingManual/Block_Crystal_Glow.json`
- `https://github.com/nevesb/hytale-mods-custom-block/blob/master/Assets/Server/Item/Items/HytaleModdingManual/Block_Crystal_Glow.json`
- `https://github.com/nevesb/hytale-mods-custom-block/blob/master/Assets/Server/Languages/en-US/server.lang`

## Pré-requisitos

- Uma pasta de mod com `manifest.json` válido
- Blockbench para autorar o modelo-fonte
- Uma build do Hytale compatível com o seu `TargetServerVersion`
- Familiaridade básica com JSON

Para um mod de tutorial apenas com assets, o `manifest.json` deve se parecer com isto:

```json
{
  "Group": "HytaleModdingManual",
  "Name": "CreateACustomBlock",
  "Version": "1.0.0",
  "Description": "Implements the Create A Block tutorial with a custom crystal block",
  "Authors": [
    {
      "Name": "HytaleModdingManual"
    }
  ],
  "Dependencies": {},
  "OptionalDependencies": {},
  "IncludesAssetPack": true,
  "TargetServerVersion": "2026.02.19-1a311a592"
}
```

## Passo 1: Construir o bloco no Blockbench

Em vez de usar um cubo simples com uma textura aplicada, comece a partir de um modelo real do Blockbench.

Para o exemplo do cristal, o arquivo de autoria é:

```text
source-assets/blockbench/Crystal_Glow.bbmodel
```

Esse modelo-fonte contém:

- a silhueta personalizada do cristal
- o layout UV final
- o atlas de textura pintado usado pelo bloco exportado

Quando o modelo estiver pronto, exporte para:

```text
Assets/Common/Blocks/HytaleModdingManual/Crystal_Glow.blockymodel
```

## Passo 2: Salvar a textura e o ícone

A textura usada pelo modelo exportado vai em:

```text
Assets/Common/BlockTextures/HytaleModdingManual/Crystal_Glow.png
```

O ícone do inventário vai em:

```text
Assets/Common/Icons/ItemsGenerated/Block_Crystal_Glow.png
```

Neste exemplo:

- o bloco usa um atlas de textura pintado à mão
- o ícone do item é derivado da arte final do bloco

## Passo 3: Criar a definição standalone do bloco

Crie a definição do bloco em:

```text
Assets/Server/Item/Block/Blocks/HytaleModdingManual/Block_Crystal_Glow.json
```

Para o fluxo com modelo customizado, o bloco precisa apontar para o `.blockymodel` exportado e para a textura:

```json
{
  "Material": "Solid",
  "DrawType": "Model",
  "Opacity": "Transparent",
  "VariantRotation": "NESW",
  "CustomModel": "Blocks/HytaleModdingManual/Crystal_Glow.blockymodel",
  "CustomModelTexture": [
    {
      "Texture": "BlockTextures/HytaleModdingManual/Crystal_Glow.png",
      "Weight": 1
    }
  ],
  "HitboxType": "Full",
  "Gathering": {
    "Breaking": {
      "GatherType": "Rocks",
      "ItemId": "Block_Crystal_Glow"
    }
  },
  "Light": {
    "Color": "#88ccff",
    "Level": 14
  },
  "BlockSoundSetId": "Crystal",
  "ParticleColor": "#88ccff"
}
```

Observações:

- `DrawType: "Model"` diz ao Hytale para usar o modelo exportado em vez de um cubo padrão
- `CustomModel` aponta para o `.blockymodel`
- `CustomModelTexture` aponta para a textura usada por esse modelo
- `Gathering.Breaking.ItemId` faz o bloco dropar ele mesmo quando for quebrado

## Passo 4: Registrar o bloco em uma BlockTypeList

Crie o arquivo de lista em:

```text
Assets/Server/BlockTypeList/HytaleModdingManual_Blocks.json
```

```json
{
  "Blocks": [
    "Block_Crystal_Glow"
  ]
}
```

O Hytale combina automaticamente as listas de blocos vindas dos mods. Você não precisa editar nenhum arquivo vanilla.

## Passo 5: Criar a definição do item

A definição do item faz o bloco aparecer no inventário e diz ao jogo como ele deve ser colocado.

Crie:

```text
Assets/Server/Item/Items/HytaleModdingManual/Block_Crystal_Glow.json
```

```json
{
  "TranslationProperties": {
    "Name": "server.items.Block_Crystal_Glow.name",
    "Description": "server.items.Block_Crystal_Glow.description"
  },
  "Interactions": {
    "Primary": "Block_Primary",
    "Secondary": "Block_Secondary"
  },
  "Quality": "Uncommon",
  "Icon": "Icons/ItemsGenerated/Block_Crystal_Glow.png",
  "PlayerAnimationsId": "Block",
  "BlockType": {
    "Material": "Solid",
    "DrawType": "Model",
    "Opacity": "Transparent",
    "VariantRotation": "NESW",
    "CustomModel": "Blocks/HytaleModdingManual/Crystal_Glow.blockymodel",
    "CustomModelTexture": [
      {
        "Texture": "BlockTextures/HytaleModdingManual/Crystal_Glow.png",
        "Weight": 1
      }
    ],
    "HitboxType": "Full",
    "Flags": {},
    "Gathering": {
      "Breaking": {
        "GatherType": "Rocks",
        "ItemId": "Block_Crystal_Glow"
      }
    },
    "Light": {
      "Color": "#88ccff",
      "Level": 14
    },
    "BlockParticleSetId": "Stone",
    "BlockSoundSetId": "Crystal",
    "ParticleColor": "#88ccff"
  },
  "MaxStack": 64,
  "IconProperties": {
    "Scale": 0.58823,
    "Rotation": [22.5, 45, 22.5],
    "Translation": [0, -13.5]
  }
}
```

Essa é a principal diferença em relação a um tutorial simples de “cubo texturizado”: o item e o bloco standalone apontam para o mesmo modelo customizado exportado e para a mesma textura.

## Passo 6: Adicionar localização

Crie um arquivo de idioma para cada locale que você quiser suportar:

```text
Assets/Server/Languages/en-US/server.lang
Assets/Server/Languages/pt-BR/server.lang
Assets/Server/Languages/es/server.lang
```

Exemplo:

```text
items.Block_Crystal_Glow.name = Glowing Crystal Block
items.Block_Crystal_Glow.description = A crystal block that radiates soft blue light.
```

E no JSON do item, mantenha as chaves assim:

```json
{
  "TranslationProperties": {
    "Name": "server.items.Block_Crystal_Glow.name",
    "Description": "server.items.Block_Crystal_Glow.description"
  }
}
```

## Passo 7: Empacotar o mod

Para runtime, a pasta do mod deve ficar achatada:

```text
CreateACustomBlock/
  Common/
  Server/
  manifest.json
```

Neste projeto prático, a saída empacotada fica em:

```text
dist/CreateACustomBlock
```

Essa é a pasta que você copia para o diretório de mods do Hytale.

## Passo 8: Testar no jogo

1. Copie `dist/CreateACustomBlock` para a pasta de mods do Hytale.
2. Inicie o jogo ou recarregue o ambiente de mods.
3. Gere o item `Block_Crystal_Glow`.
4. Coloque o bloco no mundo.
5. Confirme:
   - o modelo customizado do cristal aparece corretamente
   - o bloco emite luz
   - o conjunto de sons de cristal é usado
   - o bloco dropa ele mesmo quando quebrado

### Resultado final

Adicione uma screenshot real em jogo em:

```text
../tutorials/hytale-guide-create-a-block/qa/screenshots/create-a-block/final-result.png
```

Legenda sugerida:

> Bloco de cristal personalizado colocado no jogo com o modelo exportado do Blockbench, textura final e emissão de luz.

## Problemas comuns

| Problema | Causa | Correção |
|---|---|---|
| O bloco aparece como um cubo | `DrawType` ou `CustomModel` está errado, ou o `.blockymodel` falhou ao parsear | Reexporte o modelo e verifique `DrawType: "Model"` |
| O mod falha com erro de parent | O JSON do bloco tem um campo `Parent` acidental | Remova a herança inválida |
| O ícone está ausente | O caminho de `Icon` está errado | Use um caminho válido em `Icons/Items` ou `Icons/ItemsGenerated` |
| A textura do bloco está errada | UVs ou caminho da textura estão incorretos | Revise os UVs no Blockbench e `CustomModelTexture` |
| O nome aparece como chave em vez de texto | O caminho ou o formato da localização está errado | Verifique `Server/Languages/<locale>/server.lang` e as chaves `server.items.*` no JSON |

## Conjunto completo de arquivos

```text
manifest.json
Assets/Common/Blocks/HytaleModdingManual/Crystal_Glow.blockymodel
Assets/Common/BlockTextures/HytaleModdingManual/Crystal_Glow.png
Assets/Common/Icons/ItemsGenerated/Block_Crystal_Glow.png
Assets/Server/BlockTypeList/HytaleModdingManual_Blocks.json
Assets/Server/Item/Block/Blocks/HytaleModdingManual/Block_Crystal_Glow.json
Assets/Server/Item/Items/HytaleModdingManual/Block_Crystal_Glow.json
Assets/Server/Languages/en-US/server.lang
source-assets/blockbench/Crystal_Glow.bbmodel
```

## Próximos passos

- [Criar um Item Personalizado](/hytale-modding-docs/tutorials/beginner/create-an-item)
- [Criar um NPC Personalizado](/hytale-modding-docs/tutorials/beginner/create-an-npc)
- [Fundamentos de JSON](/hytale-modding-docs/getting-started/json-basics)
