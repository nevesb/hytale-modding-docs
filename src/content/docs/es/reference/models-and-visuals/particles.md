---
title: Particulas
description: Referencia para las definiciones de sistemas de particulas y spawners de particulas en Hytale, cubriendo efectos de particulas para bloques, combate, clima, NPCs y desplegables.
---

## Descripcion general

El sistema de particulas de Hytale utiliza dos tipos de archivos que trabajan juntos: los **sistemas de particulas** (`.particlesystem`) componen una o mas referencias de spawners en un efecto completo, y los **spawners de particulas** (`.particlespawner`) definen el comportamiento individual del emisor — tasa de emision, velocidad, tiempo de vida, textura, animacion de color, atractores y colision. Los archivos JSON de sistemas de particulas tambien pueden usar la extension `.json` para efectos complejos con multiples spawners. El motor los carga en tiempo de ejecucion para producir efectos visuales para interacciones de bloques, impactos de combate, clima, habilidades de NPCs y objetos desplegables.

## Ubicacion de archivos

```
Assets/Server/Particles/
  Block/
    Block_Top_Glow.particlesystem
    Block_Top_Glow_Alpha.particlespawner
    Clay/
      Block_Break_Clay.particlesystem
      Block_Hit_Clay.particlesystem
    Crystal/
    Stone/
    Wood/
  Combat/
  Deployables/
    Healing_Totem/
      Totem_Heal_Simple_Test.json
    Slowness_Totem/
  Drop/
  Dust_Sparkles_Fine.particlesystem
  Dust_Sparkles_Fine.particlespawner
  Explosion/
  Item/
  Memories/
  NPC/
  Projectile/
  Spell/
  Status_Effect/
  Weapon/
  Weather/
  _Example/
```

## Esquema

### Sistema de particulas (.particlesystem / .json)

| Campo | Tipo | Requerido | Predeterminado | Descripcion |
|-------|------|-----------|----------------|-------------|
| `Spawners` | `SpawnerRef[]` | Si | — | Arreglo de referencias a spawners que componen este efecto de particulas. |
| `LifeSpan` | `number` | No | — | Duracion total en segundos antes de que el sistema completo sea destruido. Omitir para efectos de duracion infinita. |
| `CullDistance` | `number` | No | — | Distancia en bloques mas alla de la cual el sistema de particulas no se renderiza. |
| `BoundingRadius` | `number` | No | — | Radio utilizado para el culling de frustum. |
| `IsImportant` | `boolean` | No | `false` | Cuando es `true`, el sistema nunca es eliminado por el presupuesto de particulas. |

### SpawnerRef

| Campo | Tipo | Requerido | Predeterminado | Descripcion |
|-------|------|-----------|----------------|-------------|
| `SpawnerId` | `string` | Si | — | ID del spawner de particulas a usar. Se resuelve a un archivo `.particlespawner` por nombre. |
| `PositionOffset` | `Vector3` | No | `{0,0,0}` | Desplazamiento de posicion desde el origen del sistema. Solo los ejes especificados se sobreescriben. |
| `FixedRotation` | `boolean` | No | `true` | Cuando es `false`, las particulas rotan con la entidad emisora. |
| `StartDelay` | `number` | No | `0` | Segundos a esperar antes de que este spawner comience a emitir. |
| `WaveDelay` | `MinMax` | No | — | Rango de retraso aleatorio entre ondas de emision. |

### Spawner de particulas (.particlespawner)

| Campo | Tipo | Requerido | Predeterminado | Descripcion |
|-------|------|-----------|----------------|-------------|
| `RenderMode` | `string` | No | — | Modo de renderizado: `"Erosion"`, `"Additive"`, `"AlphaBlend"`, etc. |
| `EmitOffset` | `Vector3MinMax` | No | — | Rango de desplazamiento aleatorio para la posicion de aparicion de particulas en cada eje. |
| `ParticleRotationInfluence` | `string` | No | — | Como se calcula la rotacion de particulas: `"Billboard"` (mira a la camara), `"Velocity"`, etc. |
| `LinearFiltering` | `boolean` | No | `false` | Usar filtrado bilineal de texturas en lugar de vecino mas cercano. |
| `LightInfluence` | `number` | No | `1.0` | Cuanto afecta la iluminacion de la escena al color de las particulas (0 = sin iluminacion, 1 = completamente iluminado). |
| `MaxConcurrentParticles` | `number` | No | `0` | Numero maximo de particulas vivas. `0` significa ilimitado. |
| `ParticleLifeSpan` | `MinMax` | No | — | Rango aleatorio para el tiempo de vida individual de particulas en segundos. |
| `ParticleRotateWithSpawner` | `boolean` | No | `false` | Si las particulas heredan la rotacion del spawner. |
| `SpawnRate` | `MinMax` | No | — | Milisegundos entre emisiones de particulas (aleatorio dentro del rango). |
| `InitialVelocity` | `VelocityConfig` | No | — | Velocidad inicial en coordenadas esfericas. |
| `Attractors` | `Attractor[]` | No | `[]` | Atractores puntuales que atraen particulas. |
| `Particle` | `ParticleConfig` | Si | — | Textura, keyframes de animacion y estado inicial. |
| `ParticleCollision` | `object` | No | — | Configuracion de colision para particulas que impactan bloques. |

### VelocityConfig

| Campo | Tipo | Requerido | Predeterminado | Descripcion |
|-------|------|-----------|----------------|-------------|
| `Yaw` | `MinMax` | No | — | Rango aleatorio de angulo de guiñada en grados. |
| `Pitch` | `MinMax` | No | — | Rango aleatorio de angulo de cabeceo en grados. |
| `Speed` | `MinMax` | No | — | Rango aleatorio de velocidad en bloques por segundo. |

### Attractor

| Campo | Tipo | Requerido | Predeterminado | Descripcion |
|-------|------|-----------|----------------|-------------|
| `Position` | `Vector3` | Si | — | Posicion del atractor relativa al spawner. |
| `RadialAxis` | `Vector3` | No | — | Eje para la aceleracion radial. |
| `Radius` | `number` | No | `0` | Radio de influencia del atractor. |
| `RadialAcceleration` | `number` | No | `0` | Fuerza radial hacia adentro (negativa) o hacia afuera (positiva). |
| `RadialTangentAcceleration` | `number` | No | `0` | Fuerza tangencial perpendicular a la direccion radial. |
| `LinearAcceleration` | `Vector3` | No | — | Aceleracion lineal constante (por ejemplo, gravedad). |

### ParticleConfig

| Campo | Tipo | Requerido | Predeterminado | Descripcion |
|-------|------|-----------|----------------|-------------|
| `Texture` | `string` | Si | — | Ruta a la imagen de textura de la particula. |
| `FrameSize` | `{ Width, Height }` | No | — | Tamaño de un fotograma individual en una textura de hoja de sprites. |
| `ScaleRatioConstraint` | `string` | No | — | `"OneToOne"` bloquea la escala X e Y juntas. |
| `Animation` | `object` | No | — | Mapa de keyframes donde las claves son porcentajes del tiempo de vida (`"0"`, `"50"`, `"100"`). |
| `InitialAnimationFrame` | `object` | No | — | Valores iniciales para rotacion, escala, opacidad e indice de fotograma. |

### Keyframe de animacion

Cada clave en el objeto `Animation` es un porcentaje del tiempo de vida (0-100). Valores en cada keyframe:

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| `FrameIndex` | `MinMax` | Rango de indice de fotograma de la hoja de sprites. |
| `Scale` | `{ X: MinMax, Y: MinMax }` | Escala en este punto de la vida de la particula. |
| `Rotation` | `{ X: MinMax, Y: MinMax, Z: MinMax }` | Rotacion en grados. |
| `Opacity` | `number` | Opacidad de 0 (invisible) a 1 (completamente opaco). |
| `Color` | `string` | Tinte de color hexadecimal en este keyframe. |

### MinMax

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| `Min` | `number` | Valor minimo del rango aleatorio. |
| `Max` | `number` | Valor maximo del rango aleatorio. |

## Ejemplos

**Sistema de particulas simple** (`Assets/Server/Particles/Dust_Sparkles_Fine.particlesystem`):

```json
{
  "Spawners": [
    {
      "SpawnerId": "Dust_Sparkles_Fine",
      "FixedRotation": true,
      "WaveDelay": { "Min": 4, "Max": 36 }
    },
    { "SpawnerId": "Dust_Sparkles_Fine" },
    { "SpawnerId": "Dust_Sparkles_Fine" }
  ],
  "CullDistance": 30
}
```

**Efecto multi-spawner con retrasos** (`Assets/Server/Particles/Deployables/Healing_Totem/Totem_Heal_Simple_Test.json`):

```json
{
  "Spawners": [
    { "SpawnerId": "Totem_Heal_Ground_Line",      "PositionOffset": { "Z": 0 }, "FixedRotation": false, "StartDelay": 1.2 },
    { "SpawnerId": "Totem_Heal_Uhr",              "PositionOffset": { "Y": 0.1 }, "StartDelay": 0.8 },
    { "SpawnerId": "Totem_Heal_Ground_Constant",   "PositionOffset": { "Z": 0 }, "FixedRotation": false, "StartDelay": 0.5 },
    { "SpawnerId": "Totem_Heal_Sparks_Constant",   "PositionOffset": { "Y": 0.5 }, "StartDelay": 0.5 }
  ],
  "LifeSpan": 9,
  "CullDistance": 100
}
```

## Paginas relacionadas

- [Modelos del servidor](/hytale-modding-docs/reference/models-and-visuals/server-models) — modelos de entidades que pueden emitir sistemas de particulas
- [Efectos de camara](/hytale-modding-docs/reference/game-configuration/camera-effects) — efectos visuales activados junto con particulas durante el combate
- [Sistema de clima](/hytale-modding-docs/reference/world-and-environment/weather-system) — particulas de clima para lluvia, nieve y polvo
