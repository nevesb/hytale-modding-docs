---
title: Modelos del cliente
description: Referencia para los archivos blockymodel del lado del cliente en Hytale, el formato binario de malla voxel utilizado para bloques, bancos de trabajo, muebles y otros objetos interactivos del mundo.
---

## Descripcion general

Los archivos de modelos del cliente (`.blockymodel`) definen la geometria de malla voxel para bloques, bancos de trabajo, muebles, puertas y otros objetos que tienen una forma visual no estandar. A diferencia de los bloques cubicos simples que solo usan texturas, los archivos blockymodel contienen un modelo voxel 3D completo con huesos nombrados para soporte de animacion. Son referenciados por las definiciones de bloques del servidor y por los archivos de modelos del servidor a traves del campo `Model`.

Estos son archivos binarios — no son JSON directamente editable por humanos. Son creados en la herramienta Hytale Model Maker y exportados al formato `.blockymodel`. Esta pagina documenta las convenciones de archivos, la estructura de directorios y como se integran con el pipeline de assets general.

## Ubicacion de archivos

```
Assets/Common/Blocks/
  Animations/           (archivos .blockyanim emparejados)
  Benches/
    Alchemy.blockymodel
    Anvil.blockymodel
    ArcaneTable.blockymodel
    Armor.blockymodel
    Bedroll.blockymodel
    Builder.blockymodel
    Campfire.blockymodel
    Carpenter.blockymodel
    Cooking.blockymodel
    Farming.blockymodel
    Furnace.blockymodel
    ...
  Chests/
  Coffins/
  Containers/
  Doors/
  Fences/
  Furniture/
  Lights/
  Signs/
  Stairs/
  Trapdoors/
  Walls/
```

## Convenciones de nomenclatura

| Patron | Ejemplo | Descripcion |
|--------|---------|-------------|
| `{Objeto}.blockymodel` | `Anvil.blockymodel` | Modelo base para un objeto de variante unica. |
| `{Objeto}_{Variante}.blockymodel` | `Campfire_Cooking.blockymodel` | Modelo variante (por ejemplo, diferente estado del mismo bloque). |
| `{Categoria}_{Material}.blockymodel` | `Door_Wood.blockymodel` | Variante de material dentro de una categoria. |

## Puntos de integracion

### Referenciado por definiciones de bloques del servidor

Los archivos JSON de tipos de bloques referencian rutas de blockymodel para sobreescribir la forma cubica predeterminada:

```json
{
  "Model": "Blocks/Benches/Anvil.blockymodel"
}
```

### Referenciado por definiciones de modelos del servidor

Los archivos de modelos del servidor para NPCs y entidades usan el mismo formato:

```json
{
  "Model": "NPC/Beast/Bear_Grizzly/Models/Model.blockymodel"
}
```

### Emparejado con animaciones

Muchos archivos blockymodel tienen archivos `.blockyanim` correspondientes en el directorio `Animations/`. Los nombres de huesos definidos en el modelo deben coincidir con los referenciados por los clips de animacion.

## Estructura de huesos

Los archivos blockymodel contienen huesos nombrados que sirven como puntos de articulacion. Nombres de huesos comunes observados en modelos de bloques:

| Hueso | Usado en | Proposito |
|-------|----------|-----------|
| `Lid` | Cofres, Ataudes | Tapa con bisagra para animacion de abrir/cerrar |
| `Door` | Puertas | Panel de puerta giratorio o deslizante |
| `Flame` | Velas, Fogatas | Elemento de llama animado |
| `Trapdoor` | Trampillas | Panel de trampilla con bisagra |

## Flujo de trabajo de ejemplo

1. Crear un modelo voxel en Model Maker con huesos nombrados
2. Exportar como `.blockymodel` a `Assets/Common/Blocks/{Categoria}/`
3. Crear archivos `.blockyanim` correspondientes en `Assets/Common/Blocks/Animations/{Categoria}/`
4. Referenciar la ruta del modelo en la definicion del tipo de bloque del servidor
5. Configurar los conjuntos de animacion si el bloque tiene estados interactivos

## Paginas relacionadas

- [Animaciones del cliente](/hytale-modding-docs/reference/models-and-visuals/client-animations) — clips de animacion `.blockyanim` emparejados con modelos de bloques
- [Modelos del servidor](/hytale-modding-docs/reference/models-and-visuals/server-models) — definiciones de modelos del servidor que referencian rutas `.blockymodel`
- [Texturas de bloques](/hytale-modding-docs/reference/models-and-visuals/block-textures) — convenciones de texturas para bloques cubicos estandar
