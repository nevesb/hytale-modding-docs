---
title: Visão Geral dos Assets
description: Entendendo os tipos de assets e formatos de arquivo do Hytale.
---

## Formatos de Arquivo

O Hytale utiliza diversos formatos de arquivo personalizados junto com formatos padrão:

### Configuração JSON (`.json`)

O formato principal para todos os dados do jogo. Usado para:
- Definições de roles de NPCs
- Definições de itens e blocos
- Receitas e tabelas de loot
- Regras de spawn e geração de mundo
- Definições de modelos (lado do servidor)
- Configurações de gameplay

### Modelo Blocky (`.blockymodel`)

O formato de modelo 3D do Hytale. Internamente baseado em JSON, contendo:
- Geometria de cuboides (posição, tamanho, rotação)
- Mapeamento UV para folhas de textura
- Hierarquia de bones para animação
- Pontos de fixação para equipamentos

Criado e editado com o **Blockbench** usando o plugin do Hytale.

### Animação Blocky (`.blockyanim`)

O formato de animação do Hytale. Baseado em JSON, contendo:
- Dados de keyframes para bones
- Canais de posição, rotação e escala
- Configurações de loop e timing

### Texturas (`.png`)

Imagens PNG padrão usadas para:
- Faces de blocos
- Texturas de modelos (resolução varia conforme a complexidade do modelo)
- Elementos de UI e ícones
- Efeitos de partículas

O Hytale utiliza texturas em estilo pixel art. Resoluções comuns:
- **Densidade de 32 px** — Blocos cúbicos padrão
- **Densidade de 64 px** — Modelos de player e a maior parte dos equipamentos em escala de personagem
- **Densidade de 64 px (melhor suposição atual)** — NPCs e mobs, com base na referência da comunidade Hytale Modding

Ao escolher o tamanho de uma textura, combine primeiro a densidade do tipo de asset. Por exemplo, a face de um bloco pode ser `32x32`, enquanto uma textura de personagem pode ser `64x64` ou `128x128` se mantiver a mesma densidade visual.

## Conceitos Importantes

### Namespace

Cada asset é identificado pelo namespace do seu mod: `Group:Name`. Por exemplo, `Hytale:Sword_Iron` refere-se à espada de ferro do jogo base.

### Herança

Muitos arquivos JSON suportam herança através dos campos `Parent` ou `Reference`. Isso permite criar novo conteúdo estendendo definições existentes em vez de escrever tudo do zero. Veja [Herança e Templates](/hytale-modding-docs/reference/concepts/inheritance-and-templates/) para mais detalhes.

### Localização

Todo texto visível para o jogador utiliza chaves de tradução em vez de strings fixas no código. As chaves são definidas em arquivos `.lang` nos diretórios `Languages/`. Veja [Chaves de Localização](/hytale-modding-docs/reference/concepts/localization-keys/) para o formato.
