---
title: Comandos Macro
description: Referência para definições de comandos macro no Hytale, que agrupam múltiplos comandos de console do servidor em um único atalho nomeado com aliases opcionais.
---

## Visão Geral

Arquivos de comandos macro definem atalhos nomeados que executam um ou mais comandos de console do servidor em sequência. Eles fornecem uma maneira de criar operações compostas simples sem script — por exemplo, um comando `/heal` que restaura tanto vida quanto stamina, ou um comando `/noon` que define o horário e pausa o relógio. Macros também podem definir aliases de comando para invocação mais rápida.

## Localização dos Arquivos

```
Assets/Server/MacroCommands/
  DeleteCommand.json
  FillSignatureCommand.json
  HealCommand.json
  NearDeathCommand.json
  NoonCommand.json
  ResetRotationCommand.json
  UnstuckCommand.json
  _Examples/
```

## Schema

### Nível Superior

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `Name` | `string` | Sim | — | Nome do comando usado para invocar a macro (ex: `"heal"` é invocado como `/heal`). |
| `Description` | `string` | Sim | — | Chave de localização para o texto de ajuda do comando, exibido na lista de comandos. |
| `Commands` | `string[]` | Sim | — | Array ordenado de comandos de console do servidor a executar. Cada string é um comando completo com argumentos. |
| `Aliases` | `string[]` | Não | `[]` | Nomes alternativos que também invocam esta macro. Cada alias deve incluir o prefixo `/`. |

## Sintaxe de Comandos

Cada entrada em `Commands` é uma string de comando de servidor sem o `/` inicial. O engine os executa em ordem, de forma síncrona. Padrões comuns de comandos incluem:

| Padrão | Exemplo | Descrição |
|--------|---------|-----------|
| `player stat settomax {Stat}` | `"player stat settomax Health"` | Define um atributo do jogador para seu valor máximo. |
| `time set {TimeOfDay}` | `"time set noon"` | Define o horário do jogo. |
| `time pause` | `"time pause"` | Pausa o relógio do jogo. |
| `tp top` | `"tp top"` | Teleporta o jogador para o topo da coluna de blocos. |
| `set {BlockType}` | `"set Empty"` | Define o bloco alvo para o tipo especificado. |

## Exemplos

**Comando de cura** (`Assets/Server/MacroCommands/HealCommand.json`):

```json
{
  "Name": "heal",
  "Description": "server.commands.heal.desc",
  "Commands": [
    "player stat settomax Stamina",
    "player stat settomax Health"
  ]
}
```

**Comando de meio-dia com pausa de tempo** (`Assets/Server/MacroCommands/NoonCommand.json`):

```json
{
  "Name": "noon",
  "Description": "server.commands.noon.desc",
  "Commands": [
    "time set noon",
    "time pause"
  ]
}
```

**Comando de deletar com aliases** (`Assets/Server/MacroCommands/DeleteCommand.json`):

```json
{
  "Name": "delete",
  "Description": "server.commands.delete.desc",
  "Commands": [
    "set Empty"
  ],
  "Aliases": [
    "/del",
    "/d"
  ]
}
```

**Comando de desencalhar** (`Assets/Server/MacroCommands/UnstuckCommand.json`):

```json
{
  "Name": "unstuck",
  "Description": "server.commands.unstuck.desc",
  "Commands": [
    "tp top"
  ]
}
```

## Páginas Relacionadas

- [Configurações de Jogabilidade](/hytale-modding-docs/reference/game-configuration/gameplay-configs) — configurações de mundo que comandos macro podem modificar em tempo de execução
- [Instâncias](/hytale-modding-docs/reference/game-configuration/instances) — configurações de instância onde comandos macro operam
