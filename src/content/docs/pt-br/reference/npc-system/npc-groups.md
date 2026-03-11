---
title: Grupos de NPC
description: Arquivos de definicao de grupo que coletam IDs de roles de NPC em conjuntos nomeados usados por tabelas de spawn, consultas de atitude e volumes de supressao.
---

## Visao Geral

Arquivos de Grupo de NPC definem colecoes nomeadas de IDs de role. Um grupo da um nome unico a um conjunto de roles para que regras de spawn, tabelas de atitude e volumes de supressao possam se referir ao conjunto inteiro sem listar cada role individualmente. IDs de role suportam um sufixo curinga `*` para corresponder a todos os roles cujo nome comeca com um determinado prefixo.

## Localizacao dos Arquivos

`Assets/Server/NPC/Groups/**/*.json`

Os grupos sao organizados em subdiretorios que espelham a arvore `Roles/` (ex: `Groups/Creature/Livestock/Chicken.json` para o grupo de bando de Chicken, `Groups/Birds.json` para todos os passaros).

## Schema

| Field | Type | Required | Default | Descricao |
|-------|------|----------|---------|-----------|
| `IncludeRoles` | string[] | Sim | — | Lista de IDs de role a incluir neste grupo. Suporta sufixo curinga `*` (ex: `"Trilobite*"` corresponde a todos os roles cujo ID comeca com `"Trilobite"`). |

## Correspondencia por Curinga

Um `*` no final de um ID de role corresponde a todos os roles com aquele prefixo. Isso e util para familias de variantes:

```json
{ "IncludeRoles": ["Trilobite*", "Jellyfish*", "Tang*"] }
```

Isso corresponde a `Trilobite`, `Trilobite_Small`, `Jellyfish_Blue`, etc. sem listar cada variante explicitamente.

## Exemplos

### Grupo de passaros

```json
{
  "IncludeRoles": [
    "Bluebird",
    "Crow",
    "Finch_Green",
    "Owl_Brown",
    "Owl_Snow",
    "Parrot",
    "Pigeon",
    "Raven",
    "Sparrow",
    "Woodpecker",
    "Duck",
    "Archaeopteryx",
    "Hawk",
    "Pterodactyl",
    "Vulture"
  ]
}
```

### Grupo aquatico (com curingas)

```json
{
  "IncludeRoles": [
    "Eel_Moray",
    "Shark_Hammerhead",
    "Shellfish_Lava",
    "Trilobite*",
    "Whale_Humpback",
    "Bluegill",
    "Frostgill",
    "Minnow",
    "Pike",
    "Piranha_Black",
    "Piranha",
    "Salmon",
    "Snapjaw",
    "Trout_Rainbow",
    "Clownfish",
    "Jellyfish*",
    "Pufferfish",
    "Tang*"
  ]
}
```

### Grupo de especie unica (bando de Chicken)

```json
{
  "IncludeRoles": [
    "Chicken",
    "Chicken_Chick"
  ]
}
```

## Como os Grupos Sao Usados

- **Regras de spawn** referenciam IDs de grupo no campo `Flock` de uma entrada de spawn de NPC para definir quais roles podem aparecer juntos.
- **Arquivos de atitude** referenciam IDs de grupo no objeto `Groups` para definir como um tipo de NPC se sente em relacao a uma categoria inteira (ex: todos os `"Predators"` sao `"Hostile"` para animais presa).
- **Volumes de supressao** referenciam IDs de grupo em `SuppressedGroups` para impedir que uma categoria de NPCs spawne em uma area.

## Paginas Relacionadas

- [NPC Roles](/hytale-modding-docs/reference/npc-system/npc-roles) — Arquivos de role individuais listados dentro dos grupos
- [NPC Spawn Rules](/hytale-modding-docs/reference/npc-system/npc-spawn-rules) — Arquivos de spawn que referenciam IDs de grupo via `Flock` e `SuppressedGroups`
- [NPC Attitudes](/hytale-modding-docs/reference/npc-system/npc-attitudes) — Arquivos de atitude que referenciam IDs de grupo para definicoes de relacionamento
