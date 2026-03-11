---
title: Chaves de Localizacao
description: Como o Hytale lida com traducao de texto usando arquivos de idioma chave-valor.
---

## Visao Geral

Todo texto visivel ao jogador no Hytale usa chaves de traducao em vez de strings fixas no codigo. Isso permite suporte a multiplos idiomas. As chaves sao definidas em arquivos `.lang` dentro dos diretorios `Languages/`.

## Localizacao dos Arquivos

- `Server/Languages/*.lang` — Strings do lado do servidor (nomes de itens, nomes de NPCs, texto de quests)
- `Common/Languages/*.lang` — Strings do lado do cliente (rotulos de UI, tooltips, menus)

## Formato do Arquivo de Idioma

Arquivos de idioma usam um formato simples `chave=valor`, uma entrada por linha:

```
server.items.sword_iron.name=Iron Sword
server.items.sword_iron.description=A sturdy blade forged from iron.
server.npc.chicken.name=Chicken
server.npc.bear_grizzly.name=Grizzly Bear
```

## Usando Chaves de Traducao

### Em Definicoes de Itens

```json
{
  "TranslationProperties": {
    "Name": "server.items.sword_iron.name",
    "Description": "server.items.sword_iron.description"
  }
}
```

### Em Roles de NPCs

```json
{
  "Modify": {
    "NameTranslationKey": "server.npc.chicken.name"
  }
}
```

### Em Tipos de Portal

```json
{
  "Description": {
    "DisplayName": "server.portals.dungeon_entrance.name",
    "FlavorText": "server.portals.dungeon_entrance.flavor",
    "Tips": [
      "server.portals.dungeon_entrance.tip1",
      "server.portals.dungeon_entrance.tip2"
    ]
  }
}
```

## Convencoes de Nomenclatura de Chaves

| Padrao | Usado Para |
|--------|------------|
| `server.items.{id}.name` | Nomes de exibicao de itens |
| `server.items.{id}.description` | Descricoes de itens |
| `server.npc.{id}.name` | Nomes de exibicao de NPCs |
| `server.blocks.{id}.name` | Nomes de exibicao de blocos |
| `server.portals.{id}.*` | Texto de UI de portais |
| `server.quests.{id}.*` | Texto de quests |

## Adicionando Traducoes para Mods

Crie um arquivo de idioma no diretorio `Server/Languages/` do seu mod:

```
mymod.items.magic_staff.name=Magic Staff
mymod.items.magic_staff.description=A staff imbued with arcane power.
```

Use um prefixo unico (o nome do seu mod) para evitar conflitos com as chaves do jogo base.

## Paginas Relacionadas

- [Item Definitions](/hytale-modding-docs/reference/item-system/item-definitions/) — uso de TranslationProperties
- [NPC Roles](/hytale-modding-docs/reference/npc-system/npc-roles/) — NameTranslationKey
