---
title: Crear un bloque personalizado
description: Tutorial paso a paso para agregar un nuevo bloque colocable en Hytale usando JSON de definición de bloques real.
---

## Objetivo

Construir un bloque de cristal brillante que los jugadores puedan fabricar, colocar y recolectar. Crearás una textura, definirás el bloque en JSON, lo registrarás en un BlockTypeList y crearás una definición de objeto para que pueda aparecer en el inventario del jugador.

## Requisitos previos

- Una carpeta de mod configurada con un `manifest.json` válido (consulta [Configura tu entorno de desarrollo](/hytale-modding-docs/tutorials/beginner/setup-dev-environment))
- Un editor de imágenes PNG (Aseprite, Photoshop, GIMP o similar) capaz de exportar PNGs de 16x16 o 32x32
- Familiaridad básica con JSON (consulta [Conceptos básicos de JSON](/hytale-modding-docs/getting-started/json-basics))

---

## Paso 1: Crear la textura

Las texturas de bloques en Hytale son archivos PNG estándar. El motor soporta texturas de **16x16** y **32x32** píxeles. Todas las texturas del juego base se encuentran en `Assets/Common/BlockTextures/` — las texturas de tu mod siguen la misma convención pero dentro de la carpeta de tu mod.

Crea un PNG de 16x16 y guárdalo en:

```
YourMod/Assets/Common/BlockTextures/MyMod/Crystal_Glow.png
```

**Guías para texturas:**
- Mantén el estilo de pixel art consistente con los bloques del juego base (colores sólidos, sin anti-aliasing)
- 16x16 es la resolución estándar; 32x32 funciona para bloques de alto detalle
- El nombre del archivo se convierte en parte de la ruta de referencia de la textura

Si quieres texturas diferentes en la parte superior, inferior y los lados, crea tres archivos:

```
YourMod/Assets/Common/BlockTextures/MyMod/Crystal_Glow_Top.png
YourMod/Assets/Common/BlockTextures/MyMod/Crystal_Glow_Side.png
YourMod/Assets/Common/BlockTextures/MyMod/Crystal_Glow_Bottom.png
```

---

## Paso 2: Crear el JSON de definición del bloque

Cada bloque necesita un archivo de definición JSON. El motor busca archivos de bloques en:

```
Assets/Server/Item/Block/Blocks/
```

Crea tu archivo de bloque en:

```
YourMod/Assets/Server/Item/Block/Blocks/MyMod/Block_Crystal_Glow.json
```

La definición de bloque más simple — siguiendo el patrón de `Assets/Server/Item/Block/Blocks/_Debug/Debug_Test_Block.json` — usa una clave `"All"` para aplicar la misma textura a todas las caras:

```json
{
  "Textures": [
    {
      "All": "MyMod/Crystal_Glow.png"
    }
  ],
  "Material": "Solid",
  "Light": {
    "Color": "#88ccff"
  }
}
```

### Claves de textura

| Clave | A qué caras se aplica |
|-------|----------------------|
| `All` | Todas las caras |
| `Top` | Solo la cara superior |
| `Bottom` | Solo la cara inferior |
| `Side` | Las cuatro caras laterales |
| `North` / `South` / `East` / `West` | Caras laterales individuales |

Para un bloque con una textura superior distinta:

```json
{
  "Textures": [
    {
      "Top": "MyMod/Crystal_Glow_Top.png",
      "Side": "MyMod/Crystal_Glow_Side.png",
      "Bottom": "MyMod/Crystal_Glow_Bottom.png"
    }
  ],
  "Material": "Solid",
  "Light": {
    "Color": "#88ccff"
  }
}
```

### Valores de Material

| Valor | Comportamiento |
|-------|---------------|
| `Solid` | Completamente opaco, colisión estándar |
| `Transparent` | Transparente (vidrio) |
| `Liquid` | Física de fluidos |
| `Empty` | Sin colisión (usado para modelos de objetos en el mundo) |

### Light

El objeto opcional `Light` hace que el bloque emita luz. `Color` es una cadena de color hexadecimal — los valores RGB controlan el tinte y brillo de la luz emitida. Omite `Light` por completo para un bloque que no brille.

---

## Paso 3: Registrar en un BlockTypeList

El motor descubre bloques a través de archivos **BlockTypeList** en `Assets/Server/BlockTypeList/`. Cada lista es un objeto JSON que contiene un array `"Blocks"` de IDs de bloques. El ID del bloque es el nombre de tu archivo JSON de bloque sin la extensión `.json`.

Crea un nuevo archivo de lista para tu mod:

```
YourMod/Assets/Server/BlockTypeList/MyMod_Blocks.json
```

```json
{
  "Blocks": [
    "Block_Crystal_Glow"
  ]
}
```

Agrega más entradas a esta misma lista a medida que tu mod crezca. No necesitas modificar ningún archivo BlockTypeList del juego base — el motor combina automáticamente todos los archivos de lista de todos los mods.

---

## Paso 4: Crear la definición del objeto

Un bloque en el mundo y un objeto en el inventario del jugador son dos conceptos separados. Necesitas una **definición de objeto** que le indique al motor cómo se ve el bloque en la mano, qué calidad tiene y (opcionalmente) cómo se fabrica.

Crea:

```
YourMod/Assets/Server/Item/Items/MyMod/Block_Crystal_Glow.json
```

```json
{
  "TranslationProperties": {
    "Name": "server.items.Block_Crystal_Glow.name",
    "Description": "server.items.Block_Crystal_Glow.description"
  },
  "Quality": "Uncommon",
  "Icon": "Icons/MyMod/Block_Crystal_Glow.png",
  "BlockType": {
    "Material": "Solid",
    "DrawType": "Block",
    "Opacity": "Opaque"
  },
  "MaxStack": 64,
  "Recipe": {
    "Input": [
      {
        "ItemId": "Ingredient_Crystal",
        "Quantity": 4
      }
    ],
    "Output": [
      {
        "ItemId": "Block_Crystal_Glow",
        "Quantity": 4
      }
    ],
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Id": "Craftingbench",
        "Categories": [
          "Blocks"
        ]
      }
    ],
    "TimeSeconds": 3
  }
}
```

**Las claves de traducción** se resuelven desde el archivo de idioma de tu mod. Crea:

```
YourMod/Assets/Languages/en-US.lang
```

```
server.items.Block_Crystal_Glow.name=Glowing Crystal Block
server.items.Block_Crystal_Glow.description=A crystal block that radiates soft blue light.
```

**Ícono:** La ruta `Icon` apunta a un PNG dentro de los assets de tu mod. Como mínimo, exporta un PNG de 64x64 de tu bloque para el espacio del inventario.

---

## Paso 5: Probar en el juego

1. Coloca la carpeta de tu mod dentro del directorio de mods del servidor.
2. Inicia el servidor. Observa la consola en busca de errores de validación JSON — siempre incluyen el nombre del archivo y del campo.
3. Usa el generador de objetos del juego (modo desarrollador) para darte `Block_Crystal_Glow`.
4. Colócalo en el mundo y confirma que la textura y la emisión de luz aparezcan correctamente.

**Errores comunes y soluciones:**

| Error | Causa | Solución |
|-------|-------|----------|
| `Unknown block id` | El bloque no está en ningún BlockTypeList | Agrégalo a `MyMod_Blocks.json` |
| `Texture not found` | Ruta incorrecta en `"All"` / `"Top"` etc. | Verifica la ruta relativa a `BlockTextures/` |
| `Missing field: Material` | JSON del bloque incompleto | Agrega `"Material": "Solid"` |
| El objeto no aparece en fabricación | `Id` del banco incorrecto | Usa el ID exacto del banco de los datos del juego base |

---

## Archivos completos

### `YourMod/Assets/Common/BlockTextures/MyMod/Crystal_Glow.png`
*(tu textura PNG de 16x16 — no se muestra)*

### `YourMod/Assets/Server/Item/Block/Blocks/MyMod/Block_Crystal_Glow.json`
```json
{
  "Textures": [
    {
      "All": "MyMod/Crystal_Glow.png"
    }
  ],
  "Material": "Solid",
  "Light": {
    "Color": "#88ccff"
  }
}
```

### `YourMod/Assets/Server/BlockTypeList/MyMod_Blocks.json`
```json
{
  "Blocks": [
    "Block_Crystal_Glow"
  ]
}
```

### `YourMod/Assets/Server/Item/Items/MyMod/Block_Crystal_Glow.json`
```json
{
  "TranslationProperties": {
    "Name": "server.items.Block_Crystal_Glow.name",
    "Description": "server.items.Block_Crystal_Glow.description"
  },
  "Quality": "Uncommon",
  "Icon": "Icons/MyMod/Block_Crystal_Glow.png",
  "BlockType": {
    "Material": "Solid",
    "DrawType": "Block",
    "Opacity": "Opaque"
  },
  "MaxStack": 64,
  "Recipe": {
    "Input": [
      {
        "ItemId": "Ingredient_Crystal",
        "Quantity": 4
      }
    ],
    "Output": [
      {
        "ItemId": "Block_Crystal_Glow",
        "Quantity": 4
      }
    ],
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Id": "Craftingbench",
        "Categories": [
          "Blocks"
        ]
      }
    ],
    "TimeSeconds": 3
  }
}
```

### `YourMod/Assets/Languages/en-US.lang`
```
server.items.Block_Crystal_Glow.name=Glowing Crystal Block
server.items.Block_Crystal_Glow.description=A crystal block that radiates soft blue light.
```

---

## Siguientes pasos

- [Crear un objeto personalizado](/hytale-modding-docs/tutorials/beginner/create-an-item) — agrega un arma o herramienta que los jugadores puedan fabricar
- [Crear un NPC personalizado](/hytale-modding-docs/tutorials/beginner/create-an-npc) — genera una criatura que suelte tu nuevo bloque
- [Conceptos básicos de JSON](/hytale-modding-docs/getting-started/json-basics) — explicación más detallada de plantillas, valores calculados y selección basada en pesos
