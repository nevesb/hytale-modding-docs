---
title: Configure seu Ambiente de Desenvolvimento
description: Instale as ferramentas necessárias e crie uma estrutura mínima de mod funcional para começar a criar mods no Hytale.
---

## Objetivo

Instalar as ferramentas necessárias, criar uma pasta de mod com um `manifest.json` válido e carregar um mod de teste mínimo no jogo. Ao final, você terá uma base funcional para construir todos os tutoriais seguintes.

## Pré-requisitos

- Hytale instalado (o cliente do jogo ou um build de servidor local)
- Acesso de administrador ou permissão de escrita no diretório de mods do jogo
- Conexão com a internet para baixar ferramentas

---

## Passo 1: Instalar as Ferramentas Necessárias

Você precisa de três ferramentas para trabalhar com mods do Hytale de forma eficiente.

### Hytale (cliente do jogo ou servidor)

O jogo é necessário para carregar e testar mods. Os mods são carregados a partir de uma pasta `mods/` no diretório de dados do jogo — o caminho exato aparece nas configurações do launcher.

### Visual Studio Code

O VS Code é o editor recomendado para arquivos JSON do Hytale. Ele oferece destaque de sintaxe, detecção de erros e validação de schema JSON.

Baixe em: **https://code.visualstudio.com/**

Após instalar, adicione as seguintes extensões pelo painel de Extensões do VS Code (`Ctrl+Shift+X`):

| Extensão | Finalidade |
|----------|------------|
| **JSON** (integrado) | Destaque de sintaxe e correspondência de colchetes |
| **Error Lens** | Exibição inline de erros de validação JSON |
| **Prettier** | Formata automaticamente o JSON ao salvar para manter a estrutura consistente |

### Blockbench

O Blockbench é a ferramenta de modelagem 3D usada para criar arquivos `.blockymodel` para itens, NPCs e decorações. O plugin do Hytale adiciona suporte de exportação para o formato nativo do Hytale.

Baixe em: **https://www.blockbench.net/**

Após instalar o Blockbench:

1. Abra o Blockbench
2. Vá em **File > Plugins**
3. Pesquise por `Hytale`
4. Instale o plugin **Hytale Exporter**
5. Reinicie o Blockbench

O plugin adiciona a opção de exportação **Hytale Blocky Model** em **File > Export**.

---

## Passo 2: Criar a Estrutura de Pastas do Mod

Todo mod do Hytale é uma pasta com um `manifest.json` na raiz. O nome da pasta se torna o identificador interno do seu mod — use apenas letras, números e underscores.

Crie a seguinte estrutura de pastas:

```
MyMod/
  manifest.json
  Assets/
    Common/
      BlockTextures/
        MyMod/
      Models/
        Items/
        NPCs/
    Server/
      Item/
        Block/
          Blocks/
            MyMod/
        Items/
          MyMod/
        Recipes/
          MyMod/
      NPC/
        Roles/
          MyMod/
        Spawn/
          World/
      Drops/
        NPCs/
          MyMod/
      BlockTypeList/
    Languages/
```

Você não precisa de todas as pastas imediatamente — crie-as conforme for adicionando conteúdo. O mínimo necessário é o `manifest.json` e a pasta `Assets/`.

---

## Passo 3: Criar o manifest.json

O arquivo `manifest.json` identifica seu mod para o jogo. O engine o lê na inicialização para registrar o mod e seus caminhos de assets.

Crie `MyMod/manifest.json`:

```json
{
  "Group": "MyMod",
  "Name": "My First Hytale Mod"
}
```

| Campo | Finalidade |
|-------|------------|
| `Group` | Namespace interno do seu mod. Usado para evitar conflitos de nomes com outros mods. Use o mesmo nome da sua pasta |
| `Name` | Nome de exibição mostrado na lista de mods |

Compare com o `manifest.json` vanilla em `Assets/manifest.json`:

```json
{
  "Group": "Hytale",
  "Name": "Hytale"
}
```

O valor de `Group` deve ser único — evite usar `Hytale` ou nomes genéricos como `Mod` que podem conflitar com outros mods.

---

## Passo 4: Configurar o VS Code para Edição de JSON

Abra a pasta do seu mod no VS Code:

```
File > Open Folder > selecione MyMod/
```

### Configurar formatação automática ao salvar

Crie `.vscode/settings.json` dentro da pasta do seu mod:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "[json]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "files.associations": {
    "*.lang": "properties"
  }
}
```

Isso garante que seu JSON esteja sempre formatado corretamente — vírgulas extras e erros de sintaxe são detectados antes de você tentar carregar o mod.

### Ativar dicas de validação JSON

O servidor de linguagem JSON integrado do VS Code sinaliza erros de sintaxe inline. Ao abrir um arquivo `.json`:

- Sublinhados vermelhos indicam erros de sintaxe (vírgulas faltando, colchetes sem par)
- Sublinhados amarelos do Error Lens indicam avisos

**Dica:** O JSON do Hytale usa um superconjunto do JSON padrão em alguns lugares — nomes de campos e valores de string diferenciam maiúsculas e minúsculas. O engine vai rejeitar `"material": "solid"` mas aceitar `"Material": "Solid"`.

---

## Passo 5: Configurar o Blockbench para o Hytale

Após instalar o plugin Hytale Exporter:

1. Abra o Blockbench
2. Crie um novo modelo: **File > New > Hytale Blocky Model**
3. Construa seu modelo usando cubos e grupos de bones
4. Defina a textura no painel **Textures** no lado direito
5. Exporte com **File > Export > Export Hytale Blocky Model**

### Convenções de modelo

| Convenção | Detalhe |
|-----------|---------|
| Escala | 1 unidade do Blockbench = 1/16 de um bloco do Hytale |
| Ponto de pivô | Centralize o modelo em `[0, 0, 0]` para posicionamento correto na mão |
| Tamanho da textura | Apenas potências de dois: 16x16, 32x32, 64x64, 128x128 |
| Nomes dos bones | Siga os padrões de nomes vanilla (`Root`, `Body`, `Head`) para compatibilidade com animações |
| Formato do arquivo | Exporte como `.blockymodel`; texturas são exportadas separadamente como `.png` |

---

## Passo 6: Criar um Mod de Teste Mínimo

Com a estrutura de pastas e o manifest prontos, adicione um único bloco para verificar se todo o pipeline funciona de ponta a ponta.

Crie `MyMod/Assets/Server/Item/Block/Blocks/MyMod/Block_Test.json`:

```json
{
  "Textures": [
    {
      "All": "Blocks/_Debug/Texture.png"
    }
  ],
  "Material": "Solid"
}
```

Isso referencia a textura de debug vanilla, então você não precisa criar nenhuma arte ainda.

Crie `MyMod/Assets/Server/BlockTypeList/MyMod_Blocks.json`:

```json
{
  "Blocks": [
    "Block_Test"
  ]
}
```

Crie `MyMod/Assets/Server/Item/Items/MyMod/Block_Test.json`:

```json
{
  "TranslationProperties": {
    "Name": "server.items.Block_Test.name"
  },
  "Quality": "Common",
  "Icon": "Icons/Items/Block_Rock_Grey.png",
  "BlockType": {
    "Material": "Solid",
    "DrawType": "Block",
    "Opacity": "Opaque"
  },
  "MaxStack": 64
}
```

Crie `MyMod/Assets/Languages/en-US.lang`:

```
server.items.Block_Test.name=Test Block
```

Sua estrutura mínima final do mod:

```
MyMod/
  manifest.json
  Assets/
    Server/
      Item/
        Block/
          Blocks/
            MyMod/
              Block_Test.json
        Items/
          MyMod/
            Block_Test.json
      BlockTypeList/
        MyMod_Blocks.json
    Languages/
      en-US.lang
```

---

## Passo 7: Carregar e Testar o Mod

1. Copie a pasta `MyMod/` para o diretório `mods/` do jogo. O caminho varia conforme a instalação — verifique o launcher ou a configuração do servidor para o local exato.
2. Inicie o jogo ou servidor.
3. Observe o log de inicialização para linhas referenciando os arquivos do seu mod. Erros sempre incluem o caminho do arquivo e o nome do campo problemático.
4. Após carregar, use o console de desenvolvedor ou o spawner de itens do jogo para dar a si mesmo o `Block_Test`.
5. Posicione o bloco e confirme se ele renderiza com a textura de debug.

### Lendo erros de inicialização

| Padrão no log | Significado |
|---------------|-------------|
| `Loaded mod: MyMod` | Manifest encontrado e lido com sucesso |
| `Unknown block id: Block_Test` | Bloco não registrado em nenhuma BlockTypeList |
| `Texture not found: Blocks/_Debug/Texture.png` | Erro de digitação no caminho ou assets vanilla não carregando |
| `JSON parse error in Block_Test.json` | Erro de sintaxe — abra no VS Code para encontrar o sublinhado vermelho |

---

## Arquivos Completos

### `MyMod/manifest.json`
```json
{
  "Group": "MyMod",
  "Name": "My First Hytale Mod"
}
```

### `MyMod/.vscode/settings.json`
```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "[json]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "files.associations": {
    "*.lang": "properties"
  }
}
```

### `MyMod/Assets/Server/Item/Block/Blocks/MyMod/Block_Test.json`
```json
{
  "Textures": [
    {
      "All": "Blocks/_Debug/Texture.png"
    }
  ],
  "Material": "Solid"
}
```

### `MyMod/Assets/Server/BlockTypeList/MyMod_Blocks.json`
```json
{
  "Blocks": [
    "Block_Test"
  ]
}
```

### `MyMod/Assets/Server/Item/Items/MyMod/Block_Test.json`
```json
{
  "TranslationProperties": {
    "Name": "server.items.Block_Test.name"
  },
  "Quality": "Common",
  "Icon": "Icons/Items/Block_Rock_Grey.png",
  "BlockType": {
    "Material": "Solid",
    "DrawType": "Block",
    "Opacity": "Opaque"
  },
  "MaxStack": 64
}
```

### `MyMod/Assets/Languages/en-US.lang`
```
server.items.Block_Test.name=Test Block
```

---

## Próximos Passos

- [Criar um Bloco Personalizado](/hytale-modding-docs/tutorials/beginner/create-a-block) — construa um bloco brilhante completo com textura, receita e definição de item
- [Criar um Item Personalizado](/hytale-modding-docs/tutorials/beginner/create-an-item) — adicione uma arma fabricável com stats de dano
- [Criar um NPC Personalizado](/hytale-modding-docs/tutorials/beginner/create-an-npc) — crie uma criatura passiva com tabela de drops
- [Fundamentos de JSON](/hytale-modding-docs/getting-started/json-basics) — referência aprofundada para herança de templates e validação
