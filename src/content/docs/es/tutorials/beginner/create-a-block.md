---
title: Crear un bloque personalizado
description: Construye un bloque personalizado en Blockbench, conéctalo al JSON de Hytale y pruébalo en el juego.
---

## Objetivo

En este tutorial vas a montar un flujo real de bloque personalizado:

1. modelar el bloque en Blockbench
2. exportar el `.blockymodel` de runtime
3. guardar la textura y el icono
4. registrar el bloque y el objeto en JSON
5. empaquetar el mod y probarlo en el juego

El ejemplo usado aquí es un bloque de cristal brillante llamado `Block_Crystal_Glow`.

Repositorio del ejemplo:

- `https://github.com/nevesb/hytale-mods-custom-block`

Archivos principales de ese repositorio:

- `https://github.com/nevesb/hytale-mods-custom-block/blob/master/source-assets/blockbench/Crystal_Glow.bbmodel`
- `https://github.com/nevesb/hytale-mods-custom-block/blob/master/Assets/Common/Blocks/HytaleModdingManual/Crystal_Glow.blockymodel`
- `https://github.com/nevesb/hytale-mods-custom-block/blob/master/Assets/Common/BlockTextures/HytaleModdingManual/Crystal_Glow.png`
- `https://github.com/nevesb/hytale-mods-custom-block/blob/master/Assets/Server/Item/Block/Blocks/HytaleModdingManual/Block_Crystal_Glow.json`
- `https://github.com/nevesb/hytale-mods-custom-block/blob/master/Assets/Server/Item/Items/HytaleModdingManual/Block_Crystal_Glow.json`
- `https://github.com/nevesb/hytale-mods-custom-block/blob/master/Assets/Server/Languages/en-US/server.lang`

## Requisitos previos

- Una carpeta de mod con un `manifest.json` válido
- Blockbench para crear el modelo fuente
- Una build de Hytale compatible con tu `TargetServerVersion`
- Familiaridad básica con JSON

Para un mod de tutorial solo con assets, el `manifest.json` debería verse así:

```json
{
  "Group": "HytaleModdingManual",
  "Name": "CreateACustomBlock",
  "Version": "1.0.0",
  "Description": "Implements the Create A Block tutorial with a custom crystal block",
  "Authors": [
    {
      "Name": "HytaleModdingManual"
    }
  ],
  "Dependencies": {},
  "OptionalDependencies": {},
  "IncludesAssetPack": true,
  "TargetServerVersion": "2026.02.19-1a311a592"
}
```

## Paso 1: Construir el bloque en Blockbench

En lugar de usar un cubo simple con una única textura, parte de un modelo real de Blockbench.

Para el ejemplo del cristal, el archivo de autoría es:

```text
source-assets/blockbench/Crystal_Glow.bbmodel
```

Este modelo fuente contiene:

- la silueta personalizada del cristal
- el layout UV final
- el atlas de textura pintado usado por el bloque exportado

Cuando el modelo esté listo, expórtalo a:

```text
Assets/Common/Blocks/HytaleModdingManual/Crystal_Glow.blockymodel
```

## Paso 2: Guardar la textura y el icono

La textura usada por el modelo exportado va en:

```text
Assets/Common/BlockTextures/HytaleModdingManual/Crystal_Glow.png
```

El icono del inventario va en:

```text
Assets/Common/Icons/ItemsGenerated/Block_Crystal_Glow.png
```

En este ejemplo:

- el bloque usa un atlas de textura pintado a mano
- el icono del objeto se deriva del arte final del bloque

## Paso 3: Crear la definición standalone del bloque

Crea la definición del bloque en:

```text
Assets/Server/Item/Block/Blocks/HytaleModdingManual/Block_Crystal_Glow.json
```

Para el flujo con modelo personalizado, el bloque debe apuntar al `.blockymodel` exportado y a la textura:

```json
{
  "Material": "Solid",
  "DrawType": "Model",
  "Opacity": "Transparent",
  "VariantRotation": "NESW",
  "CustomModel": "Blocks/HytaleModdingManual/Crystal_Glow.blockymodel",
  "CustomModelTexture": [
    {
      "Texture": "BlockTextures/HytaleModdingManual/Crystal_Glow.png",
      "Weight": 1
    }
  ],
  "HitboxType": "Full",
  "Gathering": {
    "Breaking": {
      "GatherType": "Rocks",
      "ItemId": "Block_Crystal_Glow"
    }
  },
  "Light": {
    "Color": "#88ccff",
    "Level": 14
  },
  "BlockSoundSetId": "Crystal",
  "ParticleColor": "#88ccff"
}
```

Notas:

- `DrawType: "Model"` le dice a Hytale que use el modelo exportado en vez de un cubo por defecto
- `CustomModel` apunta al `.blockymodel`
- `CustomModelTexture` apunta a la textura usada por ese modelo
- `Gathering.Breaking.ItemId` hace que el bloque se suelte a sí mismo al romperse

## Paso 4: Registrar el bloque en un BlockTypeList

Crea el archivo de lista en:

```text
Assets/Server/BlockTypeList/HytaleModdingManual_Blocks.json
```

```json
{
  "Blocks": [
    "Block_Crystal_Glow"
  ]
}
```

Hytale combina automáticamente las listas de bloques de los mods. No necesitas editar ningún archivo vanilla.

## Paso 5: Crear la definición del objeto

La definición del objeto hace que el bloque aparezca en el inventario y le dice al juego cómo colocarlo.

Crea:

```text
Assets/Server/Item/Items/HytaleModdingManual/Block_Crystal_Glow.json
```

```json
{
  "TranslationProperties": {
    "Name": "server.items.Block_Crystal_Glow.name",
    "Description": "server.items.Block_Crystal_Glow.description"
  },
  "Interactions": {
    "Primary": "Block_Primary",
    "Secondary": "Block_Secondary"
  },
  "Quality": "Uncommon",
  "Icon": "Icons/ItemsGenerated/Block_Crystal_Glow.png",
  "PlayerAnimationsId": "Block",
  "BlockType": {
    "Material": "Solid",
    "DrawType": "Model",
    "Opacity": "Transparent",
    "VariantRotation": "NESW",
    "CustomModel": "Blocks/HytaleModdingManual/Crystal_Glow.blockymodel",
    "CustomModelTexture": [
      {
        "Texture": "BlockTextures/HytaleModdingManual/Crystal_Glow.png",
        "Weight": 1
      }
    ],
    "HitboxType": "Full",
    "Flags": {},
    "Gathering": {
      "Breaking": {
        "GatherType": "Rocks",
        "ItemId": "Block_Crystal_Glow"
      }
    },
    "Light": {
      "Color": "#88ccff",
      "Level": 14
    },
    "BlockParticleSetId": "Stone",
    "BlockSoundSetId": "Crystal",
    "ParticleColor": "#88ccff"
  },
  "MaxStack": 64,
  "IconProperties": {
    "Scale": 0.58823,
    "Rotation": [22.5, 45, 22.5],
    "Translation": [0, -13.5]
  }
}
```

Esta es la diferencia principal frente a un tutorial simple de “cubo texturizado”: el objeto y el bloque standalone apuntan al mismo modelo exportado y a la misma textura.

## Paso 6: Añadir localización

Crea un archivo de idioma para cada locale que quieras soportar:

```text
Assets/Server/Languages/en-US/server.lang
Assets/Server/Languages/pt-BR/server.lang
Assets/Server/Languages/es/server.lang
```

Ejemplo:

```text
items.Block_Crystal_Glow.name = Glowing Crystal Block
items.Block_Crystal_Glow.description = A crystal block that radiates soft blue light.
```

Y en el JSON del objeto, mantén las claves así:

```json
{
  "TranslationProperties": {
    "Name": "server.items.Block_Crystal_Glow.name",
    "Description": "server.items.Block_Crystal_Glow.description"
  }
}
```

## Paso 7: Empaquetar el mod

Para runtime, la carpeta del mod debe quedar plana:

```text
CreateACustomBlock/
  Common/
  Server/
  manifest.json
```

En este proyecto práctico, la salida empaquetada vive en:

```text
dist/CreateACustomBlock
```

Esa es la carpeta que debes copiar al directorio de mods de Hytale.

## Paso 8: Probar en el juego

1. Copia `dist/CreateACustomBlock` a la carpeta de mods de Hytale.
2. Inicia el juego o recarga el entorno de mods.
3. Genera el objeto `Block_Crystal_Glow`.
4. Coloca el bloque en el mundo.
5. Confirma:
   - el modelo personalizado del cristal aparece correctamente
   - el bloque emite luz
   - se usa el set de sonidos de cristal
   - el bloque se suelta a sí mismo al romperse

### Resultado final

Añade una captura real dentro del juego en:

```text
../tutorials/hytale-guide-create-a-block/qa/screenshots/create-a-block/final-result.png
```

Leyenda sugerida:

> Bloque de cristal personalizado colocado en el juego con el modelo exportado desde Blockbench, la textura final y la emisión de luz.

## Problemas comunes

| Problema | Causa | Solución |
|---|---|---|
| El bloque aparece como un cubo | `DrawType` o `CustomModel` es incorrecto, o el `.blockymodel` falló al parsearse | Reexporta el modelo y verifica `DrawType: "Model"` |
| El mod falla con un error de parent | El JSON del bloque tiene un campo `Parent` accidental | Elimina la herencia inválida |
| Falta el icono | La ruta de `Icon` es incorrecta | Usa una ruta válida bajo `Icons/Items` o `Icons/ItemsGenerated` |
| La textura del bloque se ve mal | Los UVs o la ruta de la textura son incorrectos | Revisa los UVs en Blockbench y `CustomModelTexture` |
| El nombre aparece como una clave en vez de texto | La ruta o el formato de la localización es incorrecto | Verifica `Server/Languages/<locale>/server.lang` y las claves `server.items.*` en el JSON |

## Conjunto completo de archivos

```text
manifest.json
Assets/Common/Blocks/HytaleModdingManual/Crystal_Glow.blockymodel
Assets/Common/BlockTextures/HytaleModdingManual/Crystal_Glow.png
Assets/Common/Icons/ItemsGenerated/Block_Crystal_Glow.png
Assets/Server/BlockTypeList/HytaleModdingManual_Blocks.json
Assets/Server/Item/Block/Blocks/HytaleModdingManual/Block_Crystal_Glow.json
Assets/Server/Item/Items/HytaleModdingManual/Block_Crystal_Glow.json
Assets/Server/Languages/en-US/server.lang
source-assets/blockbench/Crystal_Glow.bbmodel
```

## Siguientes pasos

- [Crear un objeto personalizado](/hytale-modding-docs/tutorials/beginner/create-an-item)
- [Crear un NPC personalizado](/hytale-modding-docs/tutorials/beginner/create-an-npc)
- [Conceptos básicos de JSON](/hytale-modding-docs/getting-started/json-basics)
