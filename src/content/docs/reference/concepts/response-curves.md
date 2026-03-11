---
title: Response Curves
description: Mathematical curves used by Hytale's AI and gameplay systems for value mapping.
---

## Overview

Response curves map input values to output values using mathematical functions. They're used primarily in NPC AI decision-making to evaluate conditions like health percentage, distance to target, and threat level.

## File Location

`Server/ResponseCurves/*.json`

## Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `Type` | string | Yes | Curve type: `Exponential`, `Linear`, `Logistic`, `Constant` |
| `Slope` | number | No | Steepness of the curve |
| `Exponent` | number | No | Power for exponential curves |
| `XRange` | object | No | Input range with `Min` and `Max` |

## Curve Types

### Linear
Output changes proportionally with input.
```json
{ "Type": "Linear", "Slope": 1.0, "XRange": { "Min": 0, "Max": 1 } }
```

### Exponential
Output accelerates or decelerates based on exponent.
```json
{ "Type": "Exponential", "Exponent": 2.0, "Slope": 1.0, "XRange": { "Min": 0, "Max": 1 } }
```

### Logistic
S-shaped curve — slow at extremes, steep in the middle.
```json
{ "Type": "Logistic", "Slope": 10.0, "XRange": { "Min": 0, "Max": 1 } }
```

## Usage in AI

Response curves convert raw sensor values into utility scores for NPC decision-making:

```json
{
  "Type": "OwnStatPercent",
  "Stat": "Health",
  "Curve": "Linear"
}
```

When an NPC has 30% health, the Linear curve outputs 0.3. The AI system uses this score to weight actions like fleeing vs. fighting.

## Related Pages

- [NPC Decision Making](/hytale-modding-docs/reference/npc-system/npc-decision-making/) — where curves are used
- [NPC Combat Balancing](/hytale-modding-docs/reference/npc-system/npc-combat-balancing/) — AI behavior trees
