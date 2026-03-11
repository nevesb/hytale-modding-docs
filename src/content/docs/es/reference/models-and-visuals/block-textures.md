---
title: Texturas de bloques
description: Referencia para las convenciones de texturas de bloques en Hytale, cubriendo los patrones de nomenclatura, estructura de directorios y el sistema de texturas por cara utilizado por los bloques cubicos estandar.
---

## Descripcion general

Las texturas de bloques son imagenes PNG que definen la apariencia visual de los bloques cubicos estandar. A diferencia de los bloques basados en blockymodel que tienen geometria voxel 3D completa, los bloques estandar usan un conjunto de texturas de cara aplicadas a un cubo unitario. El motor resuelve las texturas por convencion de nomenclatura — un bloque llamado `Calcite` busca `Calcite.png`, `Calcite_Top.png`, `Calcite_Side.png`, etc. en el directorio `BlockTextures`. Todas las texturas usan una resolucion de pixeles consistente y se empaquetan en un atlas de texturas al cargar.

## Ubicacion de archivos

```
Assets/Common/BlockTextures/
  Bone_Side.png
  Bone_Top.png
  Calcite.png
  Calcite_Brick_Decorative.png
  Calcite_Brick_Decorative_Top.png
  Calcite_Brick_Ornate.png
  Calcite_Brick_Side.png
  Calcite_Brick_Smooth.png
  Calcite_Brick_Top.png
  Calcite_Cobble_Top.png
  Calcite_Top.png
  Chalk.png
  Clay_Black.png
  Clay_Blue.png
  Clay_Smooth_Black.png
  ...
```

## Convenciones de nomenclatura

### Texturas especificas por cara

El motor usa un sistema basado en sufijos para asignar texturas a caras especificas del cubo. Si no se encuentra una textura especifica para una cara, el motor recurre a la textura base.

| Sufijo | Caras aplicadas | Descripcion |
|--------|----------------|-------------|
| _(ninguno)_ | Todas las caras (respaldo) | Textura base usada para cualquier cara sin una sobreescritura especifica. |
| `_Top` | Superior (+Y) | Textura de la cara superior. Comun para bloques con apariencia diferente arriba/lados (por ejemplo, pasto, mineral). |
| `_Side` | Norte, Sur, Este, Oeste | Textura de cara lateral, usada cuando los lados difieren de la parte superior e inferior. |
| `_Bottom` | Inferior (-Y) | Textura de la cara inferior. Raramente necesaria; recurre a la base si esta ausente. |

### Orden de resolucion

Para un bloque llamado `Calcite_Brick`:

1. **Cara superior**: `Calcite_Brick_Top.png` -> `Calcite_Brick.png`
2. **Caras laterales**: `Calcite_Brick_Side.png` -> `Calcite_Brick.png`
3. **Cara inferior**: `Calcite_Brick_Bottom.png` -> `Calcite_Brick.png`

### Patrones de material y variante

| Patron | Ejemplo | Descripcion |
|--------|---------|-------------|
| `{Material}.png` | `Chalk.png` | Bloque uniforme simple — misma textura en todas las caras. |
| `{Material}_{Acabado}.png` | `Calcite_Brick_Smooth.png` | Variante procesada de un material base. |
| `{Material}_{Acabado}_{Cara}.png` | `Calcite_Brick_Decorative_Top.png` | Textura especifica por cara para una variante procesada. |
| `{Categoria}_{Color}.png` | `Clay_Blue.png` | Variante de color dentro de una categoria de material. |
| `{Categoria}_{Acabado}_{Color}.png` | `Clay_Smooth_Blue.png` | Variante de color de un acabado procesado. |

## Especificaciones de textura

| Propiedad | Valor | Descripcion |
|-----------|-------|-------------|
| Formato | PNG | Imagenes PNG RGBA estandar. |
| Densidad de pixeles | 32 px por cara de bloque | La referencia de Hytale Modding describe los bloques con un estandar de densidad de 32 px. |
| Transparencia | Soportada | El canal alfa permite bloques parcialmente transparentes (vidrio, hojas). |
| Espacio de color | sRGB | Espacio de color estandar; el motor maneja la conversion lineal. |

## Guia practico de tamanos

La referencia de Hytale Modding diferencia mejor la **densidad de pixeles** del tamano fijo del archivo. La regla mas segura es igualar la densidad del tipo de asset en lugar de forzar todas las texturas a la misma resolucion.

| Tipo de asset | Densidad recomendada | Ejemplos practicos | Observaciones |
|---------------|----------------------|--------------------|---------------|
| Bloques cubicos | 32 px por cara de bloque | `32x32` para una cara normal, `64x64` para una variante 2x manteniendo la misma densidad | Este es el estandar mejor documentado. |
| Modelos de jugador | 64 px de densidad | `64x64`, `128x128` | Los tamanos mayores son validos si mantienen la misma densidad visual. |
| Modelos de NPC / mob | 64 px de densidad | `64x64`, `128x128` | La guia externa describe los mobs como "probablemente tambien 64px"; tomalo como mejor practica actual, no como regla absoluta del motor. |
| Equipamiento / objetos sostenidos con modelo | 64 px de densidad | textura de espada `64x64`, textura de armadura `128x128` | Esto aplica a texturas de modelo, no a iconos de inventario. |
| Iconos de objeto / UI | Varia segun la direccion artistica de la UI | `32x32`, `64x64`, `128x128` | La referencia no define una densidad canonica unica para iconos, asi que manten consistencia dentro del mismo set visual. |

### Ejemplos

- Un bloque de piedra simple: una textura `32x32`, opcionalmente con variantes `_Top`, `_Side` y `_Bottom`.
- Una textura de peto de jugador: `64x64` o `128x128`, siempre que respete la densidad de 64 px del modelo del personaje.
- Una textura de NPC grande o jefe: `128x128` puede seguir siendo correcta si el modelo conserva la misma densidad visual que otros personajes de 64 px.
- Un icono de espada para inventario: mantenlo alineado con el resto del atlas de iconos; eso es una decision de UI, no la misma regla que bloques o personajes.

## Nota de precision

Una version anterior de este manual describia las texturas de bloques como "16x16 pixeles (estandar)". Eso era demasiado rigido frente a la referencia actual de Hytale Modding, que apunta a un estandar de **densidad de 32 px para bloques**.

## Categorias comunes de materiales

| Categoria | Ejemplos | Descripcion |
|-----------|----------|-------------|
| Suelo | `Soil_Grass.png`, `Soil_Dirt.png` | Bloques de superficie de terreno natural. |
| Piedra | `Stone.png`, `Stone_Mossy.png` | Roca subterranea y superficial. |
| Calcita | `Calcite.png`, `Calcite_Brick_Ornate.png` | Piedra de construccion de color claro con muchas variantes decorativas. |
| Arcilla | `Clay_Black.png` hasta `Clay_Purple.png` | Bloques de arcilla coloreados para construccion. |
| Mineral | Varios minerales por zona | Depositos minerales con texturas de cara distintas. |
| Madera | Varias especies de arboles | Texturas de corteza (lateral) y anillos (superior). |

## Paginas relacionadas

- [Modelos del cliente](/hytale-modding-docs/reference/models-and-visuals/client-models) — archivos `.blockymodel` para bloques con geometria no cubica
- [Listas de tipos de bloques](/hytale-modding-docs/reference/game-configuration/block-type-lists) — listas nombradas que agrupan tipos de bloques por categoria
