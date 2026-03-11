---
title: Plugins Java do Servidor
description: Quando mods de Hytale precisam de lógica em Java, para que servem plugins e onde data assets em JSON continuam sendo a melhor escolha.
---

## Resposta Curta

Use Java quando seu mod precisar de **lógica em tempo de execução** que data assets sozinhos não conseguem expressar.

Se você só está definindo conteúdo que o engine já entende, fique em JSON. Se precisa reagir a eventos, gerenciar estado, abrir UI customizada, interceptar inputs ou criar comportamento novo de gameplay, é aí que entram os plugins Java do servidor.

## O Que o JSON Já Resolve Bem

Os assets extraídos do jogo mostram que muito conteúdo do Hytale já é orientado a dados:

- Itens e blocos
- Roles, regras de spawn, grupos e atitudes de NPC
- Receitas, bancadas, tabelas de drop e barter shops
- Tipos de dano, stats, projéteis e efeitos
- Environments, clima, instances e dados de geração de mundo

Para esses sistemas, comece por JSON. É mais simples, mais fácil de validar e mais próximo da forma como o conteúdo vanilla é estruturado.

## Quando Java É a Ferramenta Certa

Com base na referência do Hytale Modding, plugins Java do servidor são a camada certa para:

| Use Java para... | Por que JSON não basta |
|------------------|------------------------|
| Comandos | Comandos são ações em runtime tratadas por código de plugin |
| Listeners de eventos | Você precisa reagir quando jogadores entram, clicam, movem, lutam ou acionam sistemas |
| Custom UI | Páginas e HUDs customizadas dependem de Java e assets `.ui` |
| Estado persistente customizado | Dados geridos pelo plugin vão além de um JSON estático |
| Interceptação de input / comportamento tipo keybind | Isso é tratado por código de servidor e hooks de input |
| Orquestração avançada de instances | Spawnar, carregar e mover jogadores entre instances é lógica de plugin |
| Novos sistemas de gameplay | Se o engine não possui schema JSON pronto para isso, você precisa de código |

## Regra Prática de Decisão

Pergunte nesta ordem:

1. O Hytale vanilla já possui um schema JSON para o que eu quero fazer?
2. Eu consigo expressar o comportamento completo com os campos, referências e templates existentes?
3. Eu preciso reagir a ações do jogador ou eventos do servidor em runtime?
4. Eu preciso de UI customizada ou de uma máquina de estados customizada?

Se a resposta for "sim" para as duas primeiras e "não" para as duas últimas, fique em JSON.

Se a resposta for "não" para as duas primeiras ou "sim" para qualquer uma das perguntas de runtime, use Java.

## Exemplos Comuns

### Exemplos para JSON primeiro

- Um novo minério com drops e receitas de crafting
- Um NPC passivo com regras de spawn e tabela de loot
- Um item de projétil usando campos existentes de projectile config
- Um portal que envia o jogador para uma instance já existente

### Exemplos que pedem Java

- Um comando `/home` com locais salvos por jogador
- Um sistema de fila para dungeons com matchmaking e rotação de instances
- Uma página de loja customizada com filtros, paginação e validação
- Uma habilidade de hotbar ligada a lógica especial do servidor
- Um HUD de quest que atualiza com estado vivo do plugin

## Singleplayer Também Entra Aqui

A referência do Hytale Modding também observa que "server plugins" continuam valendo em singleplayer, porque o modo solo roda uma instância local do servidor. Então lógica em Java não serve apenas para servidores multiplayer grandes.

## Notas de Precisão

A API mais ampla de plugins Java ainda não está totalmente documentada de forma oficial. O próprio site Hytale Modding trata parte do conhecimento sobre Java como informação estabelecida e parte como guias da comunidade. Isso significa:

- Use Java para as categorias acima com confiança
- Evite assumir que APIs não documentadas existem sem verificar
- Prefira JSON quando já houver schema nativo para o sistema

## Páginas Relacionadas

- [Custom UI](/hytale-modding-docs/pt-br/reference/game-configuration/custom-ui) — um dos casos mais claros em que Java é obrigatório
- [Estrutura do Projeto](/hytale-modding-docs/pt-br/getting-started/project-structure) — onde ficam os assets JSON versus recursos de plugin
- [Fundamentos de JSON](/hytale-modding-docs/pt-br/getting-started/json-basics) — até onde vai a camada orientada a dados antes de precisar de código
