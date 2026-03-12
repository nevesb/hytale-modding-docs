---
title: Comandos Macro
description: Referencia de las definiciones de comandos macro en Hytale, que agrupan múltiples comandos de consola del servidor en un solo atajo con nombre y alias opcionales.
---

## Descripción General

Los archivos de comandos macro definen atajos con nombre que ejecutan uno o más comandos de consola del servidor en secuencia. Proporcionan una forma de crear operaciones compuestas simples sin necesidad de scripting — por ejemplo, un comando `/heal` que restaura tanto la salud como la resistencia, o un comando `/noon` que establece la hora y pausa el reloj. Los macros también pueden definir alias de comandos para una invocación más rápida.

## Ubicación de Archivos

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

## Esquema

### Nivel Superior

| Campo | Tipo | Requerido | Predeterminado | Descripción |
|-------|------|-----------|----------------|-------------|
| `Name` | `string` | Sí | — | Nombre del comando usado para invocar el macro (por ejemplo, `"heal"` se invoca como `/heal`). |
| `Description` | `string` | Sí | — | Clave de localización para el texto de ayuda del comando, mostrado en la lista de comandos. |
| `Commands` | `string[]` | Sí | — | Array ordenado de comandos de consola del servidor a ejecutar. Cada cadena es un comando completo con argumentos. |
| `Aliases` | `string[]` | No | `[]` | Nombres alternativos que también invocan este macro. Cada alias debe incluir el prefijo `/`. |

## Sintaxis de Comandos

Cada entrada en `Commands` es una cadena de comando del servidor sin la `/` inicial. El motor los ejecuta en orden, de forma síncrona. Los patrones de comandos comunes incluyen:

| Patrón | Ejemplo | Descripción |
|--------|---------|-------------|
| `player stat settomax {Stat}` | `"player stat settomax Health"` | Establece una estadística del jugador a su valor máximo. |
| `time set {TimeOfDay}` | `"time set noon"` | Establece la hora del juego. |
| `time pause` | `"time pause"` | Pausa el reloj del juego. |
| `tp top` | `"tp top"` | Teletransporta al jugador a la parte superior de la columna de bloques. |
| `set {BlockType}` | `"set Empty"` | Establece el bloque objetivo al tipo dado. |

## Ejemplos

**Comando de curación** (`Assets/Server/MacroCommands/HealCommand.json`):

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

**Comando de mediodía con pausa de tiempo** (`Assets/Server/MacroCommands/NoonCommand.json`):

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

**Comando de eliminar con alias** (`Assets/Server/MacroCommands/DeleteCommand.json`):

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

**Comando de desatascarse** (`Assets/Server/MacroCommands/UnstuckCommand.json`):

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

- [Gameplay Configs](/hytale-modding-docs/reference/game-configuration/gameplay-configs) — ajustes del mundo que los comandos macro pueden modificar en tiempo de ejecución
- [Instances](/hytale-modding-docs/reference/game-configuration/instances) — configuraciones de instancias donde operan los comandos macro
