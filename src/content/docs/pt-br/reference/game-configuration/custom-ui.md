---
title: Custom UI
description: Referência para a UI controlada pelo servidor no Hytale, cobrindo assets `.ui`, HUDs, páginas, páginas interativas e o fluxo em Java usado para atualizá-las.
---

## Visão Geral

A UI moddável do Hytale é a **Custom UI controlada pelo servidor**, não a interface nativa do cliente. Segundo a documentação oficial espelhada pelo Hytale Modding, a UI padrão do cliente, como inventário, crafting, menus e HUD base, não é moddável. O que você pode criar é:

- **Custom Pages** — overlays interativos em tela cheia
- **Custom HUDs** — overlays persistentes desenhados durante a gameplay

Essas interfaces dependem de plugins Java do servidor e de arquivos `.ui` enviados no asset pack.

## O Que É e o Que Não É Moddável

### UI do cliente (não moddável)

O site de referência lista explicitamente os seguintes elementos como parte da UI embutida do cliente:

- Menu principal e configurações
- Criação de personagem
- HUD padrão
- Inventário e telas de crafting
- Ferramentas de desenvolvimento

Esses elementos fazem parte do cliente do jogo e não devem ser substituídos diretamente por mods.

### UI em jogo (moddável)

Plugins do servidor podem exibir:

| Tipo de UI | Finalidade | Modelo de interação |
|------------|------------|---------------------|
| `CustomUIHud` | Overlay persistente, rastreador de quest, painel de status, informações do servidor | Apenas exibição |
| `CustomUIPage` | Tela cheia sem entrada do usuário | Página não interativa |
| `InteractiveCustomUIPage<T>` | Diálogos, lojas, menus, formulários | Interativa; eventos retornam para o Java |

## Localização dos Arquivos

Os guias da comunidade colocam assets de Custom UI em:

```text
resources/Common/UI/Custom/
  MyHud.ui
  MyShop.ui
  Common.ui
  MyBackground.png
```

Garanta também que seu `manifest.json` contenha:

```json
{
  "IncludesAssetPack": true
}
```

## Arquitetura Central

A documentação oficial de Custom UI descreve um fluxo orientado a comandos:

1. O Java monta comandos de UI com `UICommandBuilder`
2. O cliente carrega o markup `.ui` e renderiza os elementos
3. O jogador interage com a UI
4. Os eventos voltam para o Java
5. Seu plugin processa os dados e envia atualizações de volta

Por isso, Custom UI pertence à camada de **Java/plugin**, e não à camada de JSON puro usada para itens, NPCs, receitas e conteúdo semelhante.

## Fundamentos de Markup `.ui`

A UI moddável atual do Hytale usa arquivos `.ui`. O guia da comunidade observa que esse formato é o usado hoje no jogo, mesmo com discussões sobre uma futura transição para NoesisGUI.

Conceitos básicos:

- A UI é definida declarativamente em arquivos `.ui`
- Elementos são acessados por IDs como `#MyButton`
- O Java atualiza propriedades por seletores como `#MyLabel.TextSpans`
- Variáveis e estilos compartilhados podem ser importados de arquivos como `Common.ui`

Exemplo mínimo:

```text
$Common = "Common.ui";

Group {
  Label #Title {
    Text: "Hello";
  }
}
```

## Fluxo de HUD

Para um overlay persistente, herde `CustomUIHud` e faça append de um arquivo `.ui` em `build()`:

```java
@Override
public void build(UICommandBuilder uiCommandBuilder) {
  uiCommandBuilder.append("MyHud.ui");
}
```

Exiba ou esconda via HUD manager do jogador:

- `player.getHudManager().setCustomHud(...)`
- `player.getHudManager().hideHudComponents(...)`

### Múltiplas HUDs

O guia de plugins do Hytale Modding **não** documenta uma API oficial chamada `MultipleUI`. O que ele referencia é um helper de comunidade chamado **MultipleHUD** para mostrar mais de uma HUD customizada ao mesmo tempo. Trate isso como utilitário opcional da comunidade, não como recurso nativo garantido do engine.

## Fluxo de Página Interativa

Use `InteractiveCustomUIPage<T>` quando o jogador precisar digitar, clicar ou enviar dados de volta ao servidor.

Peças típicas:

1. Um arquivo `.ui` com IDs de elementos
2. Uma classe de dados com `BuilderCodec<T>`
3. Bindings de evento criados em `build(...)`
4. `handleDataEvent(...)` para processar entrada
5. `sendUpdate()` após tratar o input

Padrão de binding:

```java
uiCommandBuilder.append("MyUI.ui");
uiEventBuilder.addEventBinding(
  CustomUIEventBindingType.ValueChanged,
  "#MyInput",
  EventData.of("@MyInput", "#MyInput.Value"),
  false
);
```

Comportamento importante destacado no guia da comunidade: após receber input, você precisa trocar para outra UI ou chamar `sendUpdate()`, senão o cliente pode ficar preso em estado de carregamento.

## Quando Usar Custom UI

Use Custom UI quando os sistemas nativos baseados em JSON não forem suficientes, por exemplo:

- Lojas customizadas com validação no servidor
- Árvores de diálogo e painéis administrativos
- Formulários, caixas de busca ou filtros
- HUDs de quest
- Painéis de status ligados ao estado de um plugin

Não use Custom UI como primeira opção se já existir um sistema nativo que resolva o problema, como:

- Abas de crafting de bancadas
- UI de troca de barter shops
- Cartões de descoberta de instâncias
- Descrições de loading de portais

Esses casos já são suportados por data assets próprios.

## Armadilhas Comuns

- Arquivo `.ui` não encontrado: o caminho não bate com `resources/Common/UI/Custom/...`
- Asset pack desativado: faltou `"IncludesAssetPack": true`
- Tela presa em loading: a página interativa tratou input mas não chamou `sendUpdate()`
- Tentativa de substituir inventário ou hotbar: isso pertence à UI embutida do cliente

## Páginas Relacionadas

- [Plugins Java do Servidor](/hytale-modding-docs/pt-br/getting-started/java-server-plugins) — quando Java é obrigatório
- [Estrutura do Projeto](/hytale-modding-docs/pt-br/getting-started/project-structure) — layout `Assets/...` versus `resources/...`
- [Instances](/hytale-modding-docs/pt-br/reference/game-configuration/instances) — discovery UI nativa para cartões de instância
- [Chaves de Localização](/hytale-modding-docs/pt-br/reference/concepts/localization-keys) — tradução de labels e textos de UI
