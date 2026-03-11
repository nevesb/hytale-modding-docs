---
title: Animaciones del cliente
description: Referencia para los archivos de animacion blockyanim en Hytale, el formato binario de clips de animacion utilizado por modelos de bloques y modelos de entidades para animacion por huesos con keyframes.
---

## Descripcion general

Los archivos de animacion del cliente (`.blockyanim`) contienen datos de animacion por huesos con keyframes para modelos voxel. Animan los huesos nombrados definidos en archivos `.blockymodel` para producir movimiento como puertas abriendose, tapas de cofres levantandose, llamas de velas parpadeando y fuego ardiendo. Al igual que los archivos blockymodel, estos son assets binarios creados en la herramienta Hytale Model Maker — no son directamente editables por humanos.

Las definiciones de modelos del servidor referencian archivos blockyanim dentro de sus `AnimationSets`. Las animaciones especificas de bloques se encuentran junto a sus modelos en el arbol de directorios `Blocks/Animations/`.

## Ubicacion de archivos

```
Assets/Common/Blocks/Animations/
  Candle/
    Candle_Burn.blockyanim
  Chest/
    Chest_Close.blockyanim
    Chest_Open.blockyanim
  Coffin/
    Coffin_Close.blockyanim
    Coffin_Open.blockyanim
  Door/
    Door_Close_In.blockyanim
    Door_Close_Out.blockyanim
    Door_Open_In.blockyanim
    Door_Open_Out.blockyanim
    Door_Open_Slide_In.blockyanim
    Door_Open_Slide_Out.blockyanim
  Fire/
    Fire_Burn.blockyanim
    Fire_Small_Burn.blockyanim
  Light/
    Light_Off.blockyanim
    Light_On.blockyanim
  Trapdoor/
    ...
```

Las animaciones de entidades se encuentran en una ruta separada:

```
Assets/Common/Characters/Animations/
  Damage/
    Default/
      Hurt.blockyanim
      Hurt2.blockyanim
  ...

Assets/Common/NPC/
  Beast/
    Bear_Grizzly/
      Animations/
        Default/
          Idle.blockyanim
          Run.blockyanim
        Damage/
          Death.blockyanim
  ...
```

## Convenciones de nomenclatura

| Patron | Ejemplo | Descripcion |
|--------|---------|-------------|
| `{Objeto}_{Accion}.blockyanim` | `Chest_Open.blockyanim` | Animacion de accion principal para un objeto. |
| `{Objeto}_{Accion}_{Direccion}.blockyanim` | `Door_Open_In.blockyanim` | Variante direccional de una accion. |
| `{Accion}.blockyanim` | `Idle.blockyanim` | Animacion de entidad nombrada por estado. |
| `{Accion}{N}.blockyanim` | `Hurt2.blockyanim` | Variante numerada para seleccion aleatoria. |

## Emparejamiento de animaciones

Cada archivo blockyanim apunta a huesos definidos en un blockymodel especifico. El sistema de animacion empareja por nombre de hueso, por lo tanto:

- Los nombres de huesos en la animacion **deben** coincidir exactamente con los del modelo destino.
- Una sola animacion puede compartirse entre multiples modelos si definen los mismos nombres de huesos.
- Los huesos faltantes se ignoran silenciosamente; los huesos extra en el modelo permanecen estaticos.

## Como se referencian las animaciones

### En AnimationSets de modelos del servidor

```json
{
  "AnimationSets": {
    "Idle": {
      "Animations": [
        {
          "Animation": "NPC/Beast/Bear_Grizzly/Animations/Default/Idle.blockyanim",
          "Speed": 0.6
        }
      ]
    }
  }
}
```

### En definiciones de tipos de bloques

Los tipos de bloques con estados interactivos referencian animaciones para sus transiciones de estado (por ejemplo, abrir/cerrar):

```json
{
  "OpenAnimation": "Blocks/Animations/Chest/Chest_Open.blockyanim",
  "CloseAnimation": "Blocks/Animations/Chest/Chest_Close.blockyanim"
}
```

## Categorias comunes de animaciones de bloques

| Categoria | Animaciones | Descripcion |
|-----------|------------|-------------|
| Cofre | `Chest_Open`, `Chest_Close` | Animacion de bisagra de tapa para todos los tipos de cofres |
| Ataud | `Coffin_Open`, `Coffin_Close` | Animacion de deslizamiento de tapa para bloques de ataud |
| Puerta | `Door_Open_In/Out`, `Door_Close_In/Out`, `Door_Open_Slide_In/Out` | Variantes de giro y deslizamiento para puertas |
| Vela | `Candle_Burn` | Parpadeo de llama en bucle |
| Fuego | `Fire_Burn`, `Fire_Small_Burn` | Animaciones de fuego en bucle a dos escalas |
| Luz | `Light_On`, `Light_Off` | Animaciones de alternancia para bloques emisores de luz |

## Paginas relacionadas

- [Modelos del cliente](/hytale-modding-docs/reference/models-and-visuals/client-models) — archivos de malla `.blockymodel` que definen los huesos animados por estos clips
- [Conjuntos de animacion](/hytale-modding-docs/reference/models-and-visuals/animation-sets) — como los clips de animacion se agrupan en conjuntos nombrados
- [Modelos del servidor](/hytale-modding-docs/reference/models-and-visuals/server-models) — definiciones de modelos del servidor que conectan animaciones a estados de entidades
