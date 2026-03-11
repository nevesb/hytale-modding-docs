---
title: Partículas
description: Referência para definições de sistema de partículas e emissores de partículas no Hytale, cobrindo efeitos de partículas para blocos, combate, clima, NPCs e implantáveis.
---

## Visão Geral

O sistema de partículas do Hytale usa dois tipos de arquivo que trabalham juntos: **sistemas de partículas** (`.particlesystem`) compõem uma ou mais referências de emissores em um efeito completo, e **emissores de partículas** (`.particlespawner`) definem o comportamento individual do emissor — taxa de emissão, velocidade, tempo de vida, textura, animação de cor, atratores e colisão. Arquivos JSON de sistema de partículas também podem usar a extensão `.json` para efeitos complexos com múltiplos emissores. O motor carrega estes em tempo de execução para produzir efeitos visuais para interações de bloco, acertos de combate, clima, habilidades de NPC e objetos implantáveis.

## Localização dos Arquivos

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

### Sistema de Partículas (.particlesystem / .json)

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `Spawners` | `SpawnerRef[]` | Sim | — | Array de referências de emissores que compõem este efeito de partículas. |
| `LifeSpan` | `number` | Não | — | Duração total em segundos antes que o sistema inteiro seja destruído. Omita para efeitos de duração infinita. |
| `CullDistance` | `number` | Não | — | Distância em blocos além da qual o sistema de partículas não é renderizado. |
| `BoundingRadius` | `number` | Não | — | Raio usado para culling por frustum. |
| `IsImportant` | `boolean` | Não | `false` | Quando `true`, o sistema nunca é descartado pelo orçamento de partículas. |

### SpawnerRef

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `SpawnerId` | `string` | Sim | — | ID do emissor de partículas a ser usado. Resolve para um arquivo `.particlespawner` pelo nome. |
| `PositionOffset` | `Vector3` | Não | `{0,0,0}` | Deslocamento de posição a partir da origem do sistema. Apenas os eixos especificados são sobrescritos. |
| `FixedRotation` | `boolean` | Não | `true` | Quando `false`, as partículas rotacionam com a entidade emissora. |
| `StartDelay` | `number` | Não | `0` | Segundos a esperar antes que este emissor comece a emitir. |
| `WaveDelay` | `MinMax` | Não | — | Intervalo de atraso aleatório entre ondas de emissão. |

### Emissor de Partículas (.particlespawner)

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `RenderMode` | `string` | Não | — | Modo de renderização: `"Erosion"`, `"Additive"`, `"AlphaBlend"`, etc. |
| `EmitOffset` | `Vector3MinMax` | Não | — | Intervalo de deslocamento aleatório para posição de spawn de partículas em cada eixo. |
| `ParticleRotationInfluence` | `string` | Não | — | Como a rotação da partícula é calculada: `"Billboard"` (voltada para a câmera), `"Velocity"`, etc. |
| `LinearFiltering` | `boolean` | Não | `false` | Usar filtragem bilinear de textura em vez de vizinho mais próximo. |
| `LightInfluence` | `number` | Não | `1.0` | Quanto a iluminação da cena afeta a cor da partícula (0 = sem iluminação, 1 = totalmente iluminada). |
| `MaxConcurrentParticles` | `number` | Não | `0` | Número máximo de partículas vivas. `0` significa ilimitado. |
| `ParticleLifeSpan` | `MinMax` | Não | — | Intervalo aleatório para tempo de vida individual da partícula em segundos. |
| `ParticleRotateWithSpawner` | `boolean` | Não | `false` | Se as partículas herdam a rotação do emissor. |
| `SpawnRate` | `MinMax` | Não | — | Milissegundos entre emissões de partículas (aleatório dentro do intervalo). |
| `InitialVelocity` | `VelocityConfig` | Não | — | Velocidade inicial em coordenadas esféricas. |
| `Attractors` | `Attractor[]` | Não | `[]` | Atratores pontuais que puxam partículas. |
| `Particle` | `ParticleConfig` | Sim | — | Textura, keyframes de animação e estado inicial. |
| `ParticleCollision` | `object` | Não | — | Configurações de colisão para partículas atingindo blocos. |

### VelocityConfig

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `Yaw` | `MinMax` | Não | — | Intervalo de ângulo yaw aleatório em graus. |
| `Pitch` | `MinMax` | Não | — | Intervalo de ângulo pitch aleatório em graus. |
| `Speed` | `MinMax` | Não | — | Intervalo de velocidade aleatória em blocos por segundo. |

### Attractor

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `Position` | `Vector3` | Sim | — | Posição do atrator relativa ao emissor. |
| `RadialAxis` | `Vector3` | Não | — | Eixo para aceleração radial. |
| `Radius` | `number` | Não | `0` | Raio de influência do atrator. |
| `RadialAcceleration` | `number` | Não | `0` | Força radial para dentro (negativa) ou para fora (positiva). |
| `RadialTangentAcceleration` | `number` | Não | `0` | Força tangencial perpendicular à direção radial. |
| `LinearAcceleration` | `Vector3` | Não | — | Aceleração linear constante (ex.: gravidade). |

### ParticleConfig

| Campo | Tipo | Obrigatório | Padrão | Descrição |
|-------|------|-------------|--------|-----------|
| `Texture` | `string` | Sim | — | Caminho para a imagem de textura da partícula. |
| `FrameSize` | `{ Width, Height }` | Não | — | Tamanho de um único quadro em uma textura de sprite sheet. |
| `ScaleRatioConstraint` | `string` | Não | — | `"OneToOne"` trava a escala X e Y juntas. |
| `Animation` | `object` | Não | — | Mapa de keyframes onde as chaves são porcentagens do tempo de vida (`"0"`, `"50"`, `"100"`). |
| `InitialAnimationFrame` | `object` | Não | — | Valores iniciais para rotação, escala, opacidade e índice de quadro. |

### Keyframe de Animação

Cada chave no objeto `Animation` é uma porcentagem do tempo de vida (0-100). Valores em cada keyframe:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `FrameIndex` | `MinMax` | Intervalo de índice de quadro do sprite sheet. |
| `Scale` | `{ X: MinMax, Y: MinMax }` | Escala neste ponto da vida da partícula. |
| `Rotation` | `{ X: MinMax, Y: MinMax, Z: MinMax }` | Rotação em graus. |
| `Opacity` | `number` | Opacidade de 0 (invisível) a 1 (totalmente opaco). |
| `Color` | `string` | Matiz de cor hexadecimal neste keyframe. |

### MinMax

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `Min` | `number` | Valor mínimo do intervalo aleatório. |
| `Max` | `number` | Valor máximo do intervalo aleatório. |

## Exemplos

**Sistema de partículas simples** (`Assets/Server/Particles/Dust_Sparkles_Fine.particlesystem`):

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

**Efeito com múltiplos emissores e atrasos** (`Assets/Server/Particles/Deployables/Healing_Totem/Totem_Heal_Simple_Test.json`):

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

## Páginas Relacionadas

- [Modelos de Servidor](/hytale-modding-docs/pt-br/reference/models-and-visuals/server-models) — modelos de entidade que podem emitir sistemas de partículas
- [Efeitos de Câmera](/hytale-modding-docs/pt-br/reference/game-configuration/camera-effects) — efeitos visuais disparados junto com partículas durante o combate
- [Sistema de Clima](/hytale-modding-docs/pt-br/reference/world-and-environment/weather-system) — partículas de clima para chuva, neve e poeira
