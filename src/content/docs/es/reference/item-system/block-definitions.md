---
title: Definiciones de Bloques
description: Referencia de los archivos JSON de definición de bloques en Hytale, cubriendo texturas, materiales, luz y tipos de renderizado para bloques del mundo.
---

## Descripción General

Las definiciones de bloques describen las propiedades visuales y físicas de los bloques colocados en el mundo. La mayoría de los datos de bloque se encuentran dentro del objeto `BlockType` de un archivo de definición de objeto, pero existen archivos de bloque independientes para fluidos, efectos de fluidos y calcomanías de rotura. Las texturas pueden especificarse por cara o como un atajo único `All`, con valores `Weight` opcionales para variantes aleatorias.

## Ubicación del Archivo

Los datos de bloque se almacenan en dos lugares:

- **Bloques integrados en objetos** (rocas, madera, tierra, etc.): Objeto `BlockType` dentro de `Assets/Server/Item/Items/<Category>/<ItemId>.json`
- **Archivos de bloque independientes** (fluidos, calcomanías, efectos de fluidos): `Assets/Server/Item/Block/<Subcategory>/<BlockId>.json`

Subcategorías bajo `Assets/Server/Item/Block/`:
```
Block/Fluids/          — Bloques de fluido (Lava, Agua, Slime, Veneno, Fuego)
Block/BreakingDecals/  — Superposiciones de grietas de animación de rotura
Block/FluidFX/         — Configuraciones de efectos visuales de fluidos
Block/Hitboxes/        — Definiciones de formas de hitbox personalizadas
Block/Blocks/_Debug/   — Bloques de prueba solo para depuración
```

## Esquema

### Campos del Objeto de Textura

Cada entrada en el arreglo `Textures` define una variante de textura. Múltiples entradas con valores `Weight` permiten la selección aleatoria de texturas.

| Campo | Tipo | Requerido | Por Defecto | Descripción |
|-------|------|-----------|-------------|-------------|
| `All` | string | No | — | Ruta de textura aplicada a las seis caras del bloque. |
| `Sides` | string | No | — | Textura aplicada a las cuatro caras laterales (Norte, Sur, Este, Oeste). |
| `UpDown` | string | No | — | Textura aplicada a las caras superior e inferior. |
| `Top` | string | No | — | Textura aplicada solo a la cara superior. |
| `Bottom` | string | No | — | Textura aplicada solo a la cara inferior. |
| `North` | string | No | — | Textura aplicada solo a la cara norte. |
| `South` | string | No | — | Textura aplicada solo a la cara sur. |
| `East` | string | No | — | Textura aplicada solo a la cara este. |
| `West` | string | No | — | Textura aplicada solo a la cara oeste. |
| `Weight` | number | No | `1` | Peso de probabilidad relativa para esta variante cuando hay múltiples entradas de textura presentes. |

### Campos de BlockType / Nivel de Bloque

| Campo | Tipo | Requerido | Por Defecto | Descripción |
|-------|------|-----------|-------------|-------------|
| `Textures` | object[] | No | — | Arreglo de objetos de variantes de textura (ver arriba). |
| `Material` | string | No | — | Categoría de material físico. Valores: `Solid`, `Fluid`, `Empty`, `Plant`. Controla el comportamiento de colisión e interacción. |
| `DrawType` | string | No | — | Modo de renderizado. Valores comunes: `Model` (malla personalizada), `Block` (cubo estándar), `Plant` (follaje tipo billboard). |
| `Opacity` | string | No | — | Nivel de transparencia. Valores: `Opaque`, `Semitransparent`, `Transparent`. |
| `Light` | object | No | — | Configuración de emisión de luz. Contiene `Color` (cadena hexadecimal, ej. `"#e90"`) y opcionalmente `Level` (número). |
| `ParticleColor` | string | No | — | Color hexadecimal para los efectos de partículas de rotura de bloque (ej. `"#58ad9b"`). |
| `CustomModel` | string | No | — | Ruta a un archivo `.blockymodel` usado en lugar de una malla de cubo estándar. |
| `CustomModelTexture` | object[] | No | — | Arreglo de `{ "Texture": "<ruta>", "Weight": <número> }` para variantes de textura de modelo personalizado. |
| `CustomModelScale` | number | No | `1.0` | Multiplicador de escala para el modelo personalizado. |
| `HitboxType` | string | No | — | ID de una definición de hitbox de `Block/Hitboxes/`. |
| `RandomRotation` | string | No | — | Aleatorización de rotación al colocarse. Ejemplo: `"YawStep1"`. |
| `BlockParticleSetId` | string | No | — | Conjunto de partículas usado para partículas ambientales del bloque (ej. `"Lava"`, `"Dust"`). |
| `BlockSoundSetId` | string | No | — | ID del conjunto de sonidos para los sonidos de interacción con bloques. |
| `Gathering` | object | No | — | Configuración de cosecha. Los objetos hijos `Harvest`, `Soft` y `Breaking` aceptan cada uno una cadena `GatherType`. |
| `Aliases` | string[] | No | — | IDs de cadena alternativos para este bloque, usados por comandos y generación de mundo. |

### Campos Específicos de Fluidos

Estos campos aparecen en archivos de bloques de fluidos independientes bajo `Block/Fluids/`.

| Campo | Tipo | Requerido | Por Defecto | Descripción |
|-------|------|-----------|-------------|-------------|
| `MaxFluidLevel` | number | No | — | Entero de nivel máximo de fluido. Los bloques fuente típicamente usan `1`; los fluidos en movimiento usan `8`. |
| `Effect` | string[] | No | — | Lista de IDs de efecto aplicados cuando una entidad entra en este fluido (ej. `["Lava"]`). |
| `FluidFXId` | string | No | — | Referencia una configuración de efecto visual de fluido de `Block/FluidFX/`. |
| `Ticker` | object | No | — | Comportamiento de flujo del fluido. Contiene `CanDemote` (boolean), `SpreadFluid` (string), `FlowRate` (number), `SupportedBy` (string) y `Collisions` (objeto que mapea IDs de bloque a resultados de colocación). |
| `Interactions` | object | No | — | Cadenas de interacción a nivel de bloque (ej. efectos de colisión). Usa el mismo formato de cadena que las interacciones de objetos. |
| `Parent` | string | No | — | ID de un bloque padre del cual heredar campos. |

## Ejemplo

`Assets/Server/Item/Items/Rock/Rock_Aqua.json` (sección BlockType):

```json
{
  "TranslationProperties": {
    "Name": "server.items.Rock_Aqua.name"
  },
  "Icon": "Icons/ItemsGenerated/Rock_Aqua.png",
  "Parent": "Rock_Stone",
  "BlockType": {
    "Textures": [
      {
        "All": "BlockTextures/Rock_Aqua.png",
        "Weight": 1
      }
    ],
    "ParticleColor": "#58ad9b",
    "Gathering": {
      "Breaking": {
        "GatherType": "Rocks"
      }
    },
    "Aliases": [
      "aqua",
      "aqua00"
    ]
  }
}
```

`Assets/Server/Item/Block/Blocks/_Debug/Debug_Test_Block.json` (bloque independiente con luz):

```json
{
  "Textures": [
    {
      "All": "Blocks/_Debug/Texture.png"
    }
  ],
  "Material": "Solid",
  "Light": {
    "Color": "#f0f"
  }
}
```

`Assets/Server/Item/Block/Fluids/Lava_Source.json` (bloque de fluido):

```json
{
  "MaxFluidLevel": 1,
  "Effect": ["Lava"],
  "Opacity": "Transparent",
  "Textures": [
    {
      "Weight": 1,
      "All": "BlockTextures/Fluid_Lava.png"
    }
  ],
  "Light": {
    "Color": "#e90"
  },
  "Ticker": {
    "CanDemote": false,
    "SpreadFluid": "Lava",
    "FlowRate": 2.0,
    "Collisions": {
      "Water": {
        "BlockToPlace": "Rock_Stone_Cobble",
        "SoundEvent": "SFX_Flame_Break"
      }
    }
  }
}
```

## Páginas Relacionadas

- [Definiciones de Objetos](/hytale-modding-docs/reference/item-system/item-definitions) — Esquema completo de definición de objetos incluyendo BlockType
- [Grupos de Objetos](/hytale-modding-docs/reference/item-system/item-groups) — Conjuntos nombrados de IDs de bloque usados por recetas y sistemas
- [Interacciones de Objetos](/hytale-modding-docs/reference/item-system/item-interactions) — Cadenas de interacción usadas en disparadores de colisión de fluidos
