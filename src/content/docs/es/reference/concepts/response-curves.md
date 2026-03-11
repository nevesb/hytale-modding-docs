---
title: Curvas de respuesta
description: Curvas matemáticas utilizadas por los sistemas de IA y jugabilidad de Hytale para el mapeo de valores.
---

## Descripción general

Las curvas de respuesta mapean valores de entrada a valores de salida usando funciones matemáticas. Se usan principalmente en la toma de decisiones de la IA de NPCs para evaluar condiciones como porcentaje de salud, distancia al objetivo y nivel de amenaza.

## Ubicación de archivos

`Server/ResponseCurves/*.json`

## Esquema

| Field | Type | Required | Descripción |
|-------|------|----------|-------------|
| `Type` | string | Sí | Tipo de curva: `Exponential`, `Linear`, `Logistic`, `Constant` |
| `Slope` | number | No | Pendiente de la curva |
| `Exponent` | number | No | Potencia para curvas exponenciales |
| `XRange` | object | No | Rango de entrada con `Min` y `Max` |

## Tipos de curvas

### Linear
La salida cambia proporcionalmente con la entrada.
```json
{ "Type": "Linear", "Slope": 1.0, "XRange": { "Min": 0, "Max": 1 } }
```

### Exponential
La salida se acelera o desacelera según el exponente.
```json
{ "Type": "Exponential", "Exponent": 2.0, "Slope": 1.0, "XRange": { "Min": 0, "Max": 1 } }
```

### Logistic
Curva en forma de S — lenta en los extremos, pronunciada en el medio.
```json
{ "Type": "Logistic", "Slope": 10.0, "XRange": { "Min": 0, "Max": 1 } }
```

## Uso en la IA

Las curvas de respuesta convierten valores crudos de sensores en puntuaciones de utilidad para la toma de decisiones del NPC:

```json
{
  "Type": "OwnStatPercent",
  "Stat": "Health",
  "Curve": "Linear"
}
```

Cuando un NPC tiene 30% de salud, la curva Linear produce 0.3. El sistema de IA usa esta puntuación para ponderar acciones como huir vs. pelear.

## Páginas relacionadas

- [Toma de decisiones del NPC](/hytale-modding-docs/reference/npc-system/npc-decision-making/) — donde se usan las curvas
- [Balanceo de combate de NPCs](/hytale-modding-docs/reference/npc-system/npc-combat-balancing/) — árboles de comportamiento de IA
