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
- Faces de blocos (geralmente 16x16 ou 32x32)
- Texturas de modelos (resolução varia conforme a complexidade do modelo)
- Elementos de UI e ícones
- Efeitos de partículas

O Hytale utiliza texturas em estilo pixel art. Resoluções comuns:
- **16x16** — Blocos simples e itens pequenos
- **32x32** — Blocos detalhados e equipamentos
- **64x64** — Modelos grandes ou complexos

## Conceitos Importantes

### Namespace

Cada asset é identificado pelo namespace do seu mod: `Group:Name`. Por exemplo, `Hytale:Sword_Iron` refere-se à espada de ferro do jogo base.

### Herança

Muitos arquivos JSON suportam herança através dos campos `Parent` ou `Reference`. Isso permite criar novo conteúdo estendendo definições existentes em vez de escrever tudo do zero. Veja [Herança e Templates](/hytale-modding-docs/reference/concepts/inheritance-and-templates/) para mais detalhes.

### Localização

Todo texto visível para o jogador utiliza chaves de tradução em vez de strings fixas no código. As chaves são definidas em arquivos `.lang` nos diretórios `Languages/`. Veja [Chaves de Localização](/hytale-modding-docs/reference/concepts/localization-keys/) para o formato.
