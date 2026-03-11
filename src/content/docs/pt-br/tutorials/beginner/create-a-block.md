---
title: Criar um Bloco Personalizado
description: Tutorial passo a passo para adicionar um novo bloco posicionável ao Hytale usando JSON de definição de bloco.
---

## Objetivo

Construir um bloco de cristal brilhante que os jogadores podem fabricar, posicionar e coletar. Você vai criar uma textura, definir o bloco em JSON, registrá-lo em uma BlockTypeList e criar uma definição de item para que ele apareça no inventário do jogador.

## Pré-requisitos

- Uma pasta de mod configurada com um `manifest.json` válido (veja [Configure seu Ambiente de Desenvolvimento](/hytale-modding-docs/tutorials/beginner/setup-dev-environment))
- Um editor de imagens PNG (Aseprite, Photoshop, GIMP ou similar) capaz de exportar PNGs 16x16 ou 32x32
- Familiaridade básica com JSON (veja [Fundamentos de JSON](/hytale-modding-docs/getting-started/json-basics))

---

## Passo 1: Criar a Textura

As texturas de blocos no Hytale são arquivos PNG padrão. O engine suporta texturas de **16x16** e **32x32** pixels. Todas as texturas vanilla ficam em `Assets/Common/BlockTextures/` — as texturas do seu mod seguem a mesma convenção, mas dentro da pasta do mod.

Crie um PNG 16x16 e salve em:

```
YourMod/Assets/Common/BlockTextures/MyMod/Crystal_Glow.png
```

**Diretrizes para texturas:**
- Mantenha o estilo pixel art consistente com os blocos vanilla (cores sólidas, sem anti-aliasing)
- 16x16 é a resolução padrão; 32x32 funciona para blocos com mais detalhes
- O nome do arquivo se torna parte do caminho de referência da textura

Se você quiser texturas diferentes no topo, na base e nas laterais, crie três arquivos:

```
YourMod/Assets/Common/BlockTextures/MyMod/Crystal_Glow_Top.png
YourMod/Assets/Common/BlockTextures/MyMod/Crystal_Glow_Side.png
YourMod/Assets/Common/BlockTextures/MyMod/Crystal_Glow_Bottom.png
```

---

## Passo 2: Criar o JSON de Definição do Bloco

Todo bloco precisa de um arquivo JSON de definição. O engine procura arquivos de blocos em:

```
Assets/Server/Item/Block/Blocks/
```

Crie o arquivo do seu bloco em:

```
YourMod/Assets/Server/Item/Block/Blocks/MyMod/Block_Crystal_Glow.json
```

A definição de bloco mais simples — seguindo o padrão de `Assets/Server/Item/Block/Blocks/_Debug/Debug_Test_Block.json` — usa a chave de textura `"All"` para aplicar a mesma textura em todas as faces:

```json
{
  "Textures": [
    {
      "All": "MyMod/Crystal_Glow.png"
    }
  ],
  "Material": "Solid",
  "Light": {
    "Color": "#88ccff"
  }
}
```

### Chaves de textura

| Chave | Em quais faces se aplica |
|-------|--------------------------|
| `All` | Todas as faces |
| `Top` | Apenas a face superior |
| `Bottom` | Apenas a face inferior |
| `Side` | Todas as quatro faces laterais |
| `North` / `South` / `East` / `West` | Faces laterais individuais |

Para um bloco com uma textura distinta no topo:

```json
{
  "Textures": [
    {
      "Top": "MyMod/Crystal_Glow_Top.png",
      "Side": "MyMod/Crystal_Glow_Side.png",
      "Bottom": "MyMod/Crystal_Glow_Bottom.png"
    }
  ],
  "Material": "Solid",
  "Light": {
    "Color": "#88ccff"
  }
}
```

### Valores de Material

| Valor | Comportamento |
|-------|---------------|
| `Solid` | Totalmente opaco, colisão padrão |
| `Transparent` | Transparente (vidro) |
| `Liquid` | Física de fluido |
| `Empty` | Sem colisão (usado para modelos de itens no mundo) |

### Light

O objeto `Light` opcional faz o bloco emitir luz. `Color` é uma string de cor hexadecimal — os valores RGB controlam a tonalidade e o brilho da luz emitida. Omita `Light` completamente para um bloco que não brilha.

---

## Passo 3: Registrar na BlockTypeList

O engine descobre blocos através de arquivos **BlockTypeList** em `Assets/Server/BlockTypeList/`. Cada lista é um objeto JSON contendo um array `"Blocks"` de IDs de blocos. O ID do bloco é o nome do arquivo do seu JSON de bloco sem a extensão `.json`.

Crie um novo arquivo de lista para o seu mod:

```
YourMod/Assets/Server/BlockTypeList/MyMod_Blocks.json
```

```json
{
  "Blocks": [
    "Block_Crystal_Glow"
  ]
}
```

Adicione mais entradas a essa mesma lista conforme o seu mod crescer. Você não precisa modificar nenhum arquivo BlockTypeList vanilla — o engine mescla automaticamente todos os arquivos de lista de todos os mods.

---

## Passo 4: Criar a Definição do Item

Um bloco no mundo e um item no inventário do jogador são dois conceitos separados. Você precisa de uma **definição de item** que diga ao engine como o bloco aparece na mão, qual é sua qualidade e (opcionalmente) como ele é fabricado.

Crie:

```
YourMod/Assets/Server/Item/Items/MyMod/Block_Crystal_Glow.json
```

```json
{
  "TranslationProperties": {
    "Name": "server.items.Block_Crystal_Glow.name",
    "Description": "server.items.Block_Crystal_Glow.description"
  },
  "Quality": "Uncommon",
  "Icon": "Icons/MyMod/Block_Crystal_Glow.png",
  "BlockType": {
    "Material": "Solid",
    "DrawType": "Block",
    "Opacity": "Opaque"
  },
  "MaxStack": 64,
  "Recipe": {
    "Input": [
      {
        "ItemId": "Ingredient_Crystal",
        "Quantity": 4
      }
    ],
    "Output": [
      {
        "ItemId": "Block_Crystal_Glow",
        "Quantity": 4
      }
    ],
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Id": "Craftingbench",
        "Categories": [
          "Blocks"
        ]
      }
    ],
    "TimeSeconds": 3
  }
}
```

**Chaves de tradução** são resolvidas a partir do arquivo de idioma do seu mod. Crie:

```
YourMod/Assets/Languages/en-US.lang
```

```
server.items.Block_Crystal_Glow.name=Glowing Crystal Block
server.items.Block_Crystal_Glow.description=A crystal block that radiates soft blue light.
```

**Ícone:** O caminho do `Icon` aponta para um PNG dentro dos assets do seu mod. No mínimo, exporte um PNG 64x64 do seu bloco para o ícone do slot de inventário.

---

## Passo 5: Testar no Jogo

1. Coloque a pasta do seu mod dentro do diretório de mods do servidor.
2. Inicie o servidor. Observe o console para erros de validação de JSON — eles sempre incluem o nome do arquivo e do campo.
3. Use o spawner de itens do jogo (modo desenvolvedor) para dar a si mesmo o `Block_Crystal_Glow`.
4. Posicione-o no mundo e confirme se a textura e a emissão de luz aparecem corretamente.

**Erros comuns e soluções:**

| Erro | Causa | Solução |
|------|-------|---------|
| `Unknown block id` | Bloco não está em nenhuma BlockTypeList | Adicione-o ao `MyMod_Blocks.json` |
| `Texture not found` | Caminho errado em `"All"` / `"Top"` etc. | Verifique o caminho relativo a `BlockTextures/` |
| `Missing field: Material` | JSON do bloco incompleto | Adicione `"Material": "Solid"` |
| Item não aparece no crafting | `Id` da bancada errado | Use o ID exato da bancada dos dados vanilla |

---

## Arquivos Completos

### `YourMod/Assets/Common/BlockTextures/MyMod/Crystal_Glow.png`
*(sua textura PNG 16x16 — não exibida)*

### `YourMod/Assets/Server/Item/Block/Blocks/MyMod/Block_Crystal_Glow.json`
```json
{
  "Textures": [
    {
      "All": "MyMod/Crystal_Glow.png"
    }
  ],
  "Material": "Solid",
  "Light": {
    "Color": "#88ccff"
  }
}
```

### `YourMod/Assets/Server/BlockTypeList/MyMod_Blocks.json`
```json
{
  "Blocks": [
    "Block_Crystal_Glow"
  ]
}
```

### `YourMod/Assets/Server/Item/Items/MyMod/Block_Crystal_Glow.json`
```json
{
  "TranslationProperties": {
    "Name": "server.items.Block_Crystal_Glow.name",
    "Description": "server.items.Block_Crystal_Glow.description"
  },
  "Quality": "Uncommon",
  "Icon": "Icons/MyMod/Block_Crystal_Glow.png",
  "BlockType": {
    "Material": "Solid",
    "DrawType": "Block",
    "Opacity": "Opaque"
  },
  "MaxStack": 64,
  "Recipe": {
    "Input": [
      {
        "ItemId": "Ingredient_Crystal",
        "Quantity": 4
      }
    ],
    "Output": [
      {
        "ItemId": "Block_Crystal_Glow",
        "Quantity": 4
      }
    ],
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Id": "Craftingbench",
        "Categories": [
          "Blocks"
        ]
      }
    ],
    "TimeSeconds": 3
  }
}
```

### `YourMod/Assets/Languages/en-US.lang`
```
server.items.Block_Crystal_Glow.name=Glowing Crystal Block
server.items.Block_Crystal_Glow.description=A crystal block that radiates soft blue light.
```

---

## Próximos Passos

- [Criar um Item Personalizado](/hytale-modding-docs/tutorials/beginner/create-an-item) — adicione uma arma ou ferramenta que os jogadores podem fabricar
- [Criar um NPC Personalizado](/hytale-modding-docs/tutorials/beginner/create-an-npc) — crie uma criatura que dropa seu novo bloco
- [Fundamentos de JSON](/hytale-modding-docs/getting-started/json-basics) — explicação aprofundada sobre templates, valores calculados e seleção por peso
