---
title: Instalación
description: Configura las herramientas necesarias para crear mods de Hytale.
---

## Requisitos previos

Antes de crear mods para Hytale, necesitas tener instaladas las siguientes herramientas:

- **Hytale** — El juego en sí (con acceso al sistema de modding)
- **Blockbench** — Editor 3D gratuito para crear archivos `.blockymodel` y `.blockyanim` ([blockbench.net](https://www.blockbench.net))
- **Editor de texto** — Se recomienda VS Code para editar JSON con resaltado de sintaxis
- **Editor de imágenes** — Cualquier editor de pixel art para crear texturas (Aseprite, GIMP o Piskel)

## Estructura de carpetas de mods en Hytale

Los mods de Hytale se organizan como carpetas ubicadas en el directorio de mods del juego. Cada mod contiene un `manifest.json` en su raíz:

```json
{
  "Group": "MyStudio",
  "Name": "MyMod"
}
```

El campo `Group` identifica al autor u organización, y `Name` es el identificador único del mod. Juntos forman el namespace del mod: `MyStudio:MyMod`.

## Estructura de carpetas del mod

Un mod típico sigue esta estructura:

```
MyMod/
├── manifest.json
├── Server/
│   ├── Models/
│   │   └── Beast/
│   ├── NPC/
│   │   ├── Roles/
│   │   └── Spawn/
│   ├── Item/
│   │   ├── Items/
│   │   ├── Block/
│   │   └── Recipes/
│   ├── Drops/
│   └── GameplayConfigs/
└── Common/
    ├── Blocks/
    ├── Items/
    ├── NPC/
    ├── Sounds/
    └── Icons/
```

- **`Server/`** — Datos del lado del servidor: roles de NPCs, definiciones de objetos, recetas, tablas de botín, reglas de aparición
- **`Common/`** — Assets del lado del cliente: modelos, texturas, animaciones, sonidos, interfaz de usuario

## Siguientes pasos

- [Configuración del servidor](/hytale-modding-docs/getting-started/server-setup/) — Configura un servidor local para pruebas
- [Estructura del proyecto](/hytale-modding-docs/getting-started/project-structure/) — Desglose detallado de cada carpeta
- [Conceptos básicos de JSON](/hytale-modding-docs/getting-started/json-basics/) — Cómo Hytale utiliza JSON para la configuración
