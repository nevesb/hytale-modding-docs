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
| Resolucion | 16x16 pixeles (estandar) | Todas las texturas de bloques usan la misma resolucion para el empaquetado en atlas. |
| Transparencia | Soportada | El canal alfa permite bloques parcialmente transparentes (vidrio, hojas). |
| Espacio de color | sRGB | Espacio de color estandar; el motor maneja la conversion lineal. |

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
