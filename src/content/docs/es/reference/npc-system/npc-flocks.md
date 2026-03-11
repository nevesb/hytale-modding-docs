---
title: Manadas de NPC
description: Definiciones de manadas que controlan cuántos NPCs aparecen juntos como grupo, con selección de tamaño ponderada.
---

## Descripción general

Los archivos de manadas definen el comportamiento de aparición grupal — cuántos NPCs aparecen juntos cuando se activa un evento de aparición. El sistema soporta dos modos: **Weighted** (selecciona aleatoriamente un tamaño de grupo de probabilidades ponderadas) y **Range** (elige un tamaño aleatorio dentro de un rango min/max). Las manadas son referenciadas por las reglas de aparición a través del campo `Flock`.

## Cómo funciona el tamaño de manada

```mermaid
flowchart TD;
    A[Spawn Event Triggers] --> B{Flock Type?};

    B -->|"Weighted"| C[Roll Weighted Sizes];
    B -->|"Range / Size array"| D["Pick Random<br>in Range"];

    C --> E["MinSize = 3<br>Weights: 60, 25, 15"];
    E --> F{Roll};
    F -->|"60%"| G[Spawn 3 NPCs];
    F -->|"25%"| H[Spawn 4 NPCs];
    F -->|"15%"| I[Spawn 5 NPCs];

    D --> J[Size: 2, 3];
    J --> K[Spawn 2-3 NPCs];

    G --> L["MaxGrowSize<br>Defined?"];
    H --> L;
    I --> L;
    K --> L;

    L -->|"Yes"| M["Group can grow<br>up to MaxGrowSize<br>over time"];
    L -->|"No"| N["Group stays<br>at spawned size"];

    style A fill:darkgreen,color:white;
    style G fill:steelblue,color:white;
    style H fill:steelblue,color:white;
    style I fill:steelblue,color:white;```

## Ubicación de archivos

```
Assets/Server/NPC/Flocks/
  Group_Small.json
  Group_Medium.json
  Group_Large.json
  Group_Tiny.json
  Pack_Small.json
  One_Or_Two.json
  Parent_And_Young_75_25.json
  EasterEgg_Pair.json
```

## Esquema

| Field | Type | Required | Default | Descripción |
|-------|------|----------|---------|-------------|
| `Type` | string | No | — | Modo de dimensionamiento. `"Weighted"` usa `MinSize` + `SizeWeights`. Omitir para modo de rango simple. |
| `MinSize` | integer | Sí* | — | Tamaño mínimo del grupo. Requerido para tipo `Weighted`. Tamaño inicial para el índice de peso 0. |
| `SizeWeights` | number[] | Sí* | — | Pesos relativos para cada tamaño comenzando en `MinSize`. Requerido para tipo `Weighted`. |
| `Size` | [number, number] | No | — | Rango simple min/max para el tamaño del grupo (alternativa a Weighted). |
| `MaxGrowSize` | integer | No | — | Tamaño máximo al que el grupo puede crecer con el tiempo (p.ej. a través de reproducción). |

### Cómo funcionan los SizeWeights

Para `MinSize: 3` y `SizeWeights: [60, 25, 15]`:

| Índice | Tamaño | Peso | Probabilidad |
|--------|--------|------|--------------|
| 0 | 3 (MinSize + 0) | 60 | 60% |
| 1 | 4 (MinSize + 1) | 25 | 25% |
| 2 | 5 (MinSize + 2) | 15 | 15% |

## Ejemplos

### Grupo pequeño (3-5 NPCs, ponderado)

```json
{
  "Type": "Weighted",
  "MinSize": 3,
  "SizeWeights": [60, 25, 15]
}
```

60% de probabilidad de 3, 25% de probabilidad de 4, 15% de probabilidad de 5.

### Grupo grande (5-7 NPCs, ponderado)

```json
{
  "Type": "Weighted",
  "MinSize": 5,
  "SizeWeights": [60, 20, 20]
}
```

### Padre y cría (1-2, con crecimiento)

```json
{
  "Type": "Weighted",
  "MinSize": 1,
  "SizeWeights": [75, 25],
  "MaxGrowSize": 8
}
```

75% de probabilidad de 1, 25% de probabilidad de 2. El grupo puede crecer hasta 8 con el tiempo.

### Rango simple (2-3 NPCs)

```json
{
  "Size": [2, 3]
}
```

Sin pesos — simplemente una selección aleatoria entre 2 y 3.

## Manadas disponibles

| ID de manada | Tipo | Tamaños | Notas |
|--------------|------|---------|-------|
| `Group_Tiny` | Weighted | 1-2 | Grupos muy pequeños |
| `Group_Small` | Weighted | 3-5 | Animales pasivos comunes |
| `Group_Medium` | Weighted | 4-6 | Manadas medianas |
| `Group_Large` | Weighted | 5-7 | Manadas grandes |
| `Pack_Small` | Range | 2-3 | Manadas de depredadores |
| `One_Or_Two` | Range | 1-2 | Solitario o en pareja |
| `Parent_And_Young_75_25` | Weighted | 1-2 | Parejas reproductoras, crece hasta 8 |
| `EasterEgg_Pair` | Range | 2 | Apariciones de easter egg |

## Páginas relacionadas

- [Reglas de aparición de NPCs](/hytale-modding-docs/reference/npc-system/npc-spawn-rules/) — Donde las manadas son referenciadas vía el campo `Flock`
- [Grupos de NPC](/hytale-modding-docs/reference/npc-system/npc-groups/) — Agrupación lógica de tipos de NPC
- [Sistema de pesos](/hytale-modding-docs/reference/concepts/weight-system/) — Cómo funciona la selección ponderada
