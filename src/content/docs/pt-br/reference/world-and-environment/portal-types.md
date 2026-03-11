---
title: Tipos de Portal
description: Referência para definições de tipos de portal no Hytale, que configuram a instância de destino, descrição na UI, tela de carregamento e regras de gameplay para portais do mundo.
---

## Visão Geral

Arquivos de tipo de portal definem a configuração para portais que transportam jogadores entre o overworld e conteúdo instanciado. Cada arquivo especifica qual instância o portal leva, o nome de exibição e texto descritivo mostrado na tela de carregamento, uma cor temática, arte de splash e dicas de gameplay. Um flag opcional `VoidInvasionEnabled` controla se eventos de invasão void podem ocorrer dentro do destino do portal.

## Localização dos Arquivos

```
Assets/Server/PortalTypes/
  Hederas_Lair.json
  Henges.json
  Jungles.json
  Taiga.json
  Windsurf_Valley.json
```

## Schema

### Nível superior

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `InstanceId` | `string` | Sim | — | ID da instância de destino. Deve corresponder a um nome de diretório de instância em `Assets/Server/Instances/`. |
| `Description` | `Description` | Sim | — | Metadados da UI exibidos na tela de carregamento e tooltip do portal. |
| `VoidInvasionEnabled` | `boolean` | Não | `false` | Se eventos de invasão void podem ocorrer dentro da instância de destino deste portal. |

### Description

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `DisplayName` | `string` | Sim | — | Chave de localização para o nome de exibição do portal (ex: `"server.portals.hederas_lair"`). |
| `FlavorText` | `string` | Sim | — | Chave de localização para o texto descritivo mostrado abaixo do título. |
| `ThemeColor` | `string` | Sim | — | Cor hexadecimal (com alfa opcional) usada para o destaque da tela de carregamento e elementos da UI. |
| `SplashImage` | `string` | Não | `"DefaultArtwork.png"` | Nome do arquivo de arte splash exibido durante o carregamento. |
| `Tips` | `string[]` | Não | `[]` | Array de chaves de localização para dicas de gameplay mostradas na tela de carregamento. |

## Exemplos

**Hedera's Lair** (`Assets/Server/PortalTypes/Hederas_Lair.json`):

```json
{
  "InstanceId": "Portals_Hedera",
  "Description": {
    "DisplayName": "server.portals.hederas_lair",
    "FlavorText": "server.portals.hederas_lair.description",
    "ThemeColor": "#23970cec",
    "SplashImage": "DefaultArtwork.png",
    "Tips": [
      "server.portals.hederas_lair.tip1",
      "server.portals.hederas_lair.tip2"
    ]
  },
  "VoidInvasionEnabled": true
}
```

**Windsurf Valley** (`Assets/Server/PortalTypes/Windsurf_Valley.json`):

```json
{
  "InstanceId": "Portals_Oasis",
  "Description": {
    "DisplayName": "server.portals.oasis",
    "FlavorText": "server.portals.oasis.description",
    "ThemeColor": "#f3b33cec",
    "SplashImage": "DefaultArtwork.png",
    "Tips": [
      "server.portals.windsurf_valley.tip1"
    ]
  }
}
```

## Páginas Relacionadas

- [Instâncias](/hytale-modding-docs/reference/game-configuration/instances) — definições de instância às quais os portais se conectam
- [Configs de Gameplay](/hytale-modding-docs/reference/game-configuration/gameplay-configs) — regras de gameplay aplicadas dentro dos destinos de portal
- [Ambientes](/hytale-modding-docs/reference/world-and-environment/environments) — arquivos de ambiente usados dentro de instâncias de portal
