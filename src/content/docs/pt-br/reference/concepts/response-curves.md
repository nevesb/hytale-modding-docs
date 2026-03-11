---
title: Curvas de Resposta
description: Curvas matematicas usadas pela IA e sistemas de gameplay do Hytale para mapeamento de valores.
---

## Visao Geral

Curvas de resposta mapeiam valores de entrada para valores de saida usando funcoes matematicas. Elas sao usadas principalmente na tomada de decisao da IA de NPCs para avaliar condicoes como porcentagem de vida, distancia ate o alvo e nivel de ameaca.

## Localizacao dos Arquivos

`Server/ResponseCurves/*.json`

## Schema

| Field | Type | Required | Descricao |
|-------|------|----------|-----------|
| `Type` | string | Sim | Tipo da curva: `Exponential`, `Linear`, `Logistic`, `Constant` |
| `Slope` | number | Nao | Inclinacao da curva |
| `Exponent` | number | Nao | Potencia para curvas exponenciais |
| `XRange` | object | Nao | Faixa de entrada com `Min` e `Max` |

## Tipos de Curva

### Linear
A saida muda proporcionalmente com a entrada.
```json
{ "Type": "Linear", "Slope": 1.0, "XRange": { "Min": 0, "Max": 1 } }
```

### Exponential
A saida acelera ou desacelera com base no expoente.
```json
{ "Type": "Exponential", "Exponent": 2.0, "Slope": 1.0, "XRange": { "Min": 0, "Max": 1 } }
```

### Logistic
Curva em formato S — lenta nos extremos, inclinada no meio.
```json
{ "Type": "Logistic", "Slope": 10.0, "XRange": { "Min": 0, "Max": 1 } }
```

## Uso na IA

Curvas de resposta convertem valores brutos dos sensores em pontuacoes de utilidade para a tomada de decisao dos NPCs:

```json
{
  "Type": "OwnStatPercent",
  "Stat": "Health",
  "Curve": "Linear"
}
```

Quando um NPC tem 30% de vida, a curva Linear retorna 0.3. O sistema de IA usa essa pontuacao para ponderar acoes como fugir versus lutar.

## Paginas Relacionadas

- [NPC Decision Making](/hytale-modding-docs/reference/npc-system/npc-decision-making/) — onde as curvas sao usadas
- [NPC Combat Balancing](/hytale-modding-docs/reference/npc-system/npc-combat-balancing/) — arvores de comportamento da IA
