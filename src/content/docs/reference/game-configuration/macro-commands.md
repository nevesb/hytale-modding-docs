---
title: Macro Commands
description: Reference for macro command definitions in Hytale, which bundle multiple server console commands into a single named shortcut with optional aliases.
---

## Overview

Macro command files define named shortcuts that execute one or more server console commands in sequence. They provide a way to create simple composite operations without scripting — for example, a `/heal` command that restores both health and stamina, or a `/noon` command that sets the time and pauses the clock. Macros can also define command aliases for quicker invocation.

## File Location

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

### Top-level

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `Name` | `string` | Yes | — | Command name used to invoke the macro (e.g. `"heal"` is invoked as `/heal`). |
| `Description` | `string` | Yes | — | Localisation key for the command's help text, shown in the command list. |
| `Commands` | `string[]` | Yes | — | Ordered array of server console commands to execute. Each string is a full command with arguments. |
| `Aliases` | `string[]` | No | `[]` | Alternative names that also invoke this macro. Each alias should include the `/` prefix. |

## Command Syntax

Each entry in `Commands` is a raw server command string without the leading `/`. The engine executes them in order, synchronously. Common command patterns include:

| Pattern | Example | Description |
|---------|---------|-------------|
| `player stat settomax {Stat}` | `"player stat settomax Health"` | Sets a player stat to its maximum value. |
| `time set {TimeOfDay}` | `"time set noon"` | Sets the in-game time. |
| `time pause` | `"time pause"` | Pauses the in-game clock. |
| `tp top` | `"tp top"` | Teleports the player to the top of the block column. |
| `set {BlockType}` | `"set Empty"` | Sets the targeted block to the given type. |

## Examples

**Heal command** (`Assets/Server/MacroCommands/HealCommand.json`):

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

**Noon command with time pause** (`Assets/Server/MacroCommands/NoonCommand.json`):

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

**Delete command with aliases** (`Assets/Server/MacroCommands/DeleteCommand.json`):

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

**Unstuck command** (`Assets/Server/MacroCommands/UnstuckCommand.json`):

```json
{
  "Name": "unstuck",
  "Description": "server.commands.unstuck.desc",
  "Commands": [
    "tp top"
  ]
}
```

## Related Pages

- [Gameplay Configs](/hytale-modding-docs/reference/game-configuration/gameplay-configs) — world settings that macro commands can modify at runtime
- [Instances](/hytale-modding-docs/reference/game-configuration/instances) — instance configurations where macro commands operate
