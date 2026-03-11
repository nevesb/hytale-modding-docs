---
title: Instalação
description: Configure as ferramentas necessárias para criar mods no Hytale.
---

## Pré-requisitos

Antes de criar mods para o Hytale, você precisa ter as seguintes ferramentas instaladas:

- **Hytale** — O jogo em si (com acesso ao sistema de modding)
- **Blockbench** — Editor 3D gratuito para criar arquivos `.blockymodel` e `.blockyanim` ([blockbench.net](https://www.blockbench.net))
- **Editor de Texto** — VS Code é recomendado para edição de JSON com destaque de sintaxe
- **Editor de Imagens** — Qualquer editor de pixel art para criar texturas (Aseprite, GIMP ou Piskel)

## Estrutura de Pastas de um Mod

Os mods do Hytale são organizados como pastas colocadas no diretório de mods do jogo. Cada mod contém um `manifest.json` na raiz:

```json
{
  "Group": "MyStudio",
  "Name": "MyMod"
}
```

O `Group` identifica o autor ou organização, e o `Name` é o identificador único do mod. Juntos, eles formam o namespace do mod: `MyStudio:MyMod`.

## Layout das Pastas do Mod

Um mod típico segue esta estrutura:

```
MyMod/
├── manifest.json
├── Server/
│   ├── Models/
│   │   └── Beast/
│   ├── NPC/
│   │   ├── Roles/
│   │   └── Spawn/
│   ├── Item/
│   │   ├── Items/
│   │   ├── Block/
│   │   └── Recipes/
│   ├── Drops/
│   └── GameplayConfigs/
└── Common/
    ├── Blocks/
    ├── Items/
    ├── NPC/
    ├── Sounds/
    └── Icons/
```

- **`Server/`** — Dados do lado do servidor: roles de NPCs, definições de itens, receitas, tabelas de loot, regras de spawn
- **`Common/`** — Assets do lado do cliente: modelos, texturas, animações, sons, UI

## Próximos Passos

- [Configuração do Servidor](/hytale-modding-docs/getting-started/server-setup/) — Configure um servidor local para testes
- [Estrutura do Projeto](/hytale-modding-docs/getting-started/project-structure/) — Detalhamento completo de cada pasta
- [Fundamentos de JSON](/hytale-modding-docs/getting-started/json-basics/) — Como o Hytale utiliza JSON para configuração
