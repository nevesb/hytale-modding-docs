---
title: Estrutura do Projeto
description: Detalhamento completo da estrutura de pastas de um mod do Hytale.
---

## Diretório Server

A pasta `Server/` contém todas as definições de dados do lado do servidor. O servidor lê esses arquivos JSON para definir o comportamento do jogo.

### Sistema de NPCs

| Caminho | Finalidade |
|---------|------------|
| `Server/NPC/Roles/` | Definições de comportamento de NPCs — stats, IA, aparência |
| `Server/NPC/Spawn/` | Regras de spawn — onde, quando e como os NPCs aparecem |
| `Server/NPC/Attitude/` | Definições de atitude dos NPCs em relação aos jogadores |
| `Server/NPC/DecisionMaking/` | Avaliadores de condições da IA |
| `Server/NPC/Balancing/` | Árvores de comportamento de combate da IA |
| `Server/NPC/Groups/` | Agrupamentos de NPCs para regras de spawn/interação |
| `Server/NPC/Flocks/` | Padrões de comportamento de bando |

### Sistema de Itens

| Caminho | Finalidade |
|---------|------------|
| `Server/Item/Items/` | Definições de itens — stats, receitas, ícones |
| `Server/Item/Block/` | Definições de tipos de bloco — texturas, materiais |
| `Server/Item/Recipes/` | Receitas de crafting |
| `Server/Item/Category/` | Hierarquia de categorias de itens para a UI do inventário |
| `Server/Item/Qualities/` | Níveis de raridade (Comum, Incomum, Raro, Épico) |
| `Server/Item/Interactions/` | Cadeias de interação de blocos/itens |
| `Server/Item/Groups/` | Agrupamentos de itens |
| `Server/Item/ResourceTypes/` | Definições de tipos de recurso |

### Mundo e Combate

| Caminho | Finalidade |
|---------|------------|
| `Server/Models/` | Definições de modelos do servidor — hitboxes, animações |
| `Server/Drops/` | Definições de tabelas de loot |
| `Server/Projectiles/` | Definições simples de projéteis |
| `Server/ProjectileConfigs/` | Configurações avançadas de projéteis |
| `Server/Entity/` | Propriedades de entidades — tipos de dano, stats, efeitos |
| `Server/Environments/` | Configurações de ambiente dos biomas |
| `Server/Weathers/` | Definições visuais de clima |
| `Server/HytaleGenerator/` | Regras de geração de mundo |
| `Server/BarterShops/` | Inventários de lojas de NPCs |
| `Server/Farming/` | Configurações de fazendas e galinheiros |
| `Server/GameplayConfigs/` | Configurações principais do jogo |

## Diretório Common

A pasta `Common/` contém os assets do lado do cliente, renderizados pelo cliente do jogo.

| Caminho | Finalidade |
|---------|------------|
| `Common/Blocks/` | Modelos de blocos (`.blockymodel`), animações (`.blockyanim`), texturas |
| `Common/Characters/` | Modelos e animações de personagens jogáveis |
| `Common/Items/` | Modelos e texturas de itens |
| `Common/NPC/` | Modelos e animações de NPCs no cliente |
| `Common/Icons/` | Ícones de UI para itens e habilidades |
| `Common/Sounds/` | Efeitos sonoros |
| `Common/Music/` | Trilhas musicais |
| `Common/Particles/` | Definições de efeitos de partículas |
| `Common/UI/` | Definições de layout de UI |
| `Common/BlockTextures/` | Texturas das faces dos blocos |

## Notas Sobre Fluxos Modernos com Plugins

Se você estiver criando **plugins Java com asset packs**, os guias da comunidade costumam descrever a parte de assets do plugin em `resources/Common/...` e `resources/Server/...`. Os assets vanilla extraídos documentados neste manual continuam usando a estrutura `Assets/...`, então você precisa traduzir os caminhos conforme o fluxo adotado.

- Para JSONs do servidor extraídos do jogo, continue usando as referências `Assets/Server/...` documentadas aqui.
- Para UI empacotada junto de plugins, procure arquivos `.ui` em `resources/Common/UI/Custom`.
- Para projetos de plugin que enviam arte customizada, garanta que o `manifest.json` tenha `"IncludesAssetPack": true`.

## Páginas Relacionadas

- [Custom UI](/hytale-modding-docs/pt-br/reference/game-configuration/custom-ui) — páginas, HUDs, arquivos `.ui` e fluxo de eventos controlados pelo servidor
- [Plugins Java do Servidor](/hytale-modding-docs/pt-br/getting-started/java-server-plugins) — quando usar Java em vez de conteúdo só com JSON
