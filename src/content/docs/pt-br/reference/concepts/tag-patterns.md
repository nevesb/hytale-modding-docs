---
title: Padroes de Tags
description: Sistema logico de correspondencia de tags usado em toda a configuracao do Hytale.
---

## Visao Geral

Os padroes de tags fornecem um sistema de logica booleana para corresponder conteudo com tags. Eles usam operadores como `And`, `Or`, `Not` e `Equals` para criar regras complexas de correspondencia para ambientes, blocos, NPCs e outras entidades com tags.

## Localizacao dos Arquivos

`Server/TagPatterns/*.json`

## Operadores

| Operador | Proposito | Campos |
|----------|-----------|--------|
| `Equals` | Corresponde a uma unica tag | `Tag` |
| `Or` | Corresponde a qualquer um dos padroes | `Patterns` (array) |
| `And` | Corresponde a todos os padroes | `Patterns` (array) |
| `Not` | Inverte um padrao | `Pattern` (unico) |

## Exemplos

### Correspondencia OR simples

```json
{
  "Op": "Or",
  "Patterns": [
    { "Op": "Equals", "Tag": "Bush" },
    { "Op": "Equals", "Tag": "Seed" }
  ]
}
```

Corresponde a qualquer bloco com a tag `Bush` ou `Seed`.

### AND + NOT complexo

```json
{
  "Op": "And",
  "Patterns": [
    { "Op": "Equals", "Tag": "Caves" },
    {
      "Op": "Not",
      "Pattern": {
        "Op": "Or",
        "Patterns": [
          { "Op": "Equals", "Tag": "Volcanic" },
          { "Op": "Equals", "Tag": "Spiders" },
          { "Op": "Equals", "Tag": "Dungeons" }
        ]
      }
    }
  ]
}
```

Corresponde a ambientes com a tag `Caves` mas NAO `Volcanic`, `Spiders` ou `Dungeons`.

## Onde as Tags Sao Usadas

- **Audio de ambiente** — seleciona sons ambientes com base nas tags do ambiente
- **Spawn de NPCs** — restringe spawns a biomas com tags especificas
- **Interacoes de blocos** — corresponde tipos de blocos por grupos de tags

## Paginas Relacionadas

- [Environments](/hytale-modding-docs/reference/world-and-environment/environments/) — uso de tags de ambiente
- [NPC Spawn Rules](/hytale-modding-docs/reference/npc-system/npc-spawn-rules/) — filtragem de spawn por tags
