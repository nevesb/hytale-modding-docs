---
title: Configuração do Servidor
description: Como configurar um servidor local do Hytale para testar mods.
---

## Configurando um Servidor de Testes

Para testar seus mods, você precisa de um servidor local do Hytale rodando com o seu mod carregado.

### Passo 1: Localizar o Servidor

O executável do servidor do Hytale está incluído na instalação do jogo. Procure os arquivos do servidor no diretório de instalação do Hytale.

### Passo 2: Configurar os Mods

Coloque a pasta do seu mod no diretório de mods do servidor. O servidor lê as pastas de mods e carrega o `manifest.json` de cada uma na inicialização.

### Passo 3: Iniciar e Testar

Inicie o servidor e conecte-se a `localhost` pelo cliente do jogo. Alterações em arquivos de configuração JSON geralmente exigem que o servidor seja reiniciado para que tenham efeito.

## Hot Reload

Algumas alterações em assets (texturas, modelos) podem ser detectadas sem reiniciar completamente, mas mudanças em JSONs do lado do servidor (roles de NPCs, definições de itens, regras de spawn) sempre exigem reinicialização.

## Resolução de Problemas

- **Mod não carrega**: Verifique se o `manifest.json` existe na raiz do mod com os campos `Group` e `Name` válidos
- **Erros de parse no JSON**: Valide seus arquivos JSON — problemas comuns incluem vírgulas no final e aspas faltando
- **Assets não encontrados**: Verifique se os caminhos dos arquivos estão exatamente corretos (diferencia maiúsculas e minúsculas em alguns sistemas)
