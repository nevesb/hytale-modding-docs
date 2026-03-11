---
title: Fundamentos de JSON
description: Como o Hytale usa JSON para configuração do jogo e modding.
---

## JSON no Hytale

Cada elemento de conteúdo do jogo no Hytale — de NPCs a itens e geração de mundo — é definido em arquivos JSON. Entender os padrões comuns vai ajudar você a criar mods de forma eficiente.

## Padrões Comuns

### Herança de Templates

A maioria dos arquivos JSON suporta herança de um template usando `Parent` ou `Reference`:

```json
{
  "Reference": "Template_Beasts_Passive_Critter",
  "Modify": {
    "Appearance": "Chicken",
    "MaxHealth": 10,
    "DropList": "Drop_Chicken"
  }
}
```

O `Reference` aponta para um arquivo de template, e o `Modify` sobrescreve campos específicos. Isso evita duplicar configurações comuns entre entidades semelhantes.

### Valores Calculados

Alguns campos suportam valores calculados que referenciam parâmetros:

```json
{
  "Parameters": {
    "BaseHealth": {
      "Value": 100,
      "Description": "Base health for this NPC"
    }
  },
  "MaxHealth": {
    "Compute": "BaseHealth * 1.5"
  }
}
```

### Seleção por Peso

Drops, spawns e lojas usam um sistema de pesos para seleção aleatória:

```json
{
  "Container": {
    "Type": "Choice",
    "Containers": [
      { "Weight": 70, "Item": { "ItemId": "Coin_Gold" } },
      { "Weight": 25, "Item": { "ItemId": "Gem_Ruby" } },
      { "Weight": 5, "Item": { "ItemId": "Sword_Legendary" } }
    ]
  }
}
```

Peso maior = probabilidade maior. O total não precisa ser igual a 100 — os pesos são relativos.

### Encadeamento de Interações

Comportamentos complexos são construídos encadeando interações com o campo `Next`:

```json
{
  "Type": "Condition",
  "RequiredGameMode": "Adventure",
  "Next": {
    "Type": "ApplyEffect",
    "EffectId": "Poison",
    "Next": {
      "Type": "Damage",
      "DamageCalculator": {
        "BaseDamage": { "Poison": 5 }
      }
    }
  }
}
```

Cada interação dispara a próxima em sequência, criando comportamentos de gameplay complexos.

### Chaves de Tradução

Textos visíveis para o jogador utilizam chaves de localização:

```json
{
  "TranslationProperties": {
    "Name": "server.items.sword_iron.name",
    "Description": "server.items.sword_iron.description"
  }
}
```

O texto real é definido nos arquivos de idioma (`Languages/en-US.lang`):
```
server.items.sword_iron.name=Iron Sword
server.items.sword_iron.description=A sturdy blade forged from iron.
```

## Validação de Arquivos

O Hytale valida os arquivos JSON na inicialização do servidor. Erros comuns:
- **Vírgulas no final** — JSON não permite vírgulas após o último elemento
- **Referências ausentes** — `Parent` ou `Reference` apontando para templates inexistentes
- **Tipos de campo inválidos** — String onde era esperado um número, ou vice-versa
- **Campos obrigatórios ausentes** — Alguns campos são obrigatórios dependendo do tipo de entidade
