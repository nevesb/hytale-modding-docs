---
title: Tipos de portal
description: Referencia para las definiciones de tipos de portal en Hytale, que configuran la instancia de destino, descripción de UI, pantalla de carga y reglas de juego para portales del mundo.
---

## Descripción general

Los archivos de tipo de portal definen la configuración para portales que transportan jugadores entre el mundo abierto y contenido instanciado. Cada archivo especifica a qué instancia conduce el portal, el nombre visible y texto descriptivo mostrado en la pantalla de carga, un color temático, arte de presentación y consejos de juego. Una bandera opcional `VoidInvasionEnabled` controla si los eventos de invasión del vacío pueden ocurrir dentro del destino del portal.

## Ubicación de archivos

```
Assets/Server/PortalTypes/
  Hederas_Lair.json
  Henges.json
  Jungles.json
  Taiga.json
  Windsurf_Valley.json
```

## Esquema

### Nivel superior

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `InstanceId` | `string` | Sí | — | ID de la instancia de destino. Debe coincidir con un nombre de directorio de instancia bajo `Assets/Server/Instances/`. |
| `Description` | `Description` | Sí | — | Metadatos de UI mostrados en la pantalla de carga y tooltip del portal. |
| `VoidInvasionEnabled` | `boolean` | No | `false` | Si los eventos de invasión del vacío pueden activarse dentro de la instancia de destino de este portal. |

### Description

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `DisplayName` | `string` | Sí | — | Clave de localización para el nombre visible del portal (ej. `"server.portals.hederas_lair"`). |
| `FlavorText` | `string` | Sí | — | Clave de localización para el texto descriptivo mostrado debajo del título. |
| `ThemeColor` | `string` | Sí | — | Color hexadecimal (con alfa opcional) usado para el acento de la pantalla de carga y elementos de UI. |
| `SplashImage` | `string` | No | `"DefaultArtwork.png"` | Nombre de archivo del arte de presentación mostrado durante la carga. |
| `Tips` | `string[]` | No | `[]` | Arreglo de claves de localización para consejos de juego mostrados en la pantalla de carga. |

## Ejemplos

**Guarida de Hedera** (`Assets/Server/PortalTypes/Hederas_Lair.json`):

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

**Valle Windsurf** (`Assets/Server/PortalTypes/Windsurf_Valley.json`):

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

## Páginas relacionadas

- [Instancias](/hytale-modding-docs/reference/game-configuration/instances) — definiciones de instancia a las que se conectan los portales
- [Configuraciones de juego](/hytale-modding-docs/reference/game-configuration/gameplay-configs) — reglas de juego aplicadas dentro de los destinos de portal
- [Ambientes](/hytale-modding-docs/reference/world-and-environment/environments) — archivos de ambiente usados dentro de instancias de portal
