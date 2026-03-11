---
title: Custom UI
description: Referencia de la UI controlada por el servidor en Hytale, cubriendo assets `.ui`, HUDs, paginas, paginas interactivas y el flujo en Java usado para actualizarlas.
---

## Descripcion general

La UI moddable de Hytale es la **Custom UI controlada por el servidor**, no la interfaz nativa del cliente. Segun la documentacion oficial reflejada por Hytale Modding, la UI predeterminada del cliente, como inventario, crafting, menus y el HUD base, no es moddable. Lo que si puedes crear es:

- **Custom Pages** — overlays interactivos a pantalla completa
- **Custom HUDs** — overlays persistentes dibujados durante la jugabilidad

Estas interfaces dependen de plugins Java del servidor y de archivos `.ui` incluidos en el asset pack.

## Que es y que no es moddable

### UI del cliente (no moddable)

El sitio de referencia lista explicitamente los siguientes elementos como parte de la UI integrada del cliente:

- Menu principal y configuracion
- Creacion de personaje
- HUD predeterminado
- Inventario y pantallas de crafting
- Herramientas de desarrollo

Estos elementos forman parte del cliente del juego y no estan pensados para ser reemplazados directamente por mods.

### UI en juego (moddable)

Los plugins del servidor pueden mostrar:

| Tipo de UI | Finalidad | Modelo de interaccion |
|------------|------------|-----------------------|
| `CustomUIHud` | Overlay persistente, rastreador de quests, panel de estado, informacion del servidor | Solo visualizacion |
| `CustomUIPage` | Pantalla completa sin entrada del usuario | Pagina no interactiva |
| `InteractiveCustomUIPage<T>` | Dialogos, tiendas, menus, formularios | Interactiva; los eventos vuelven a Java |

## Ubicacion de archivos

Las guias de plugins de la comunidad colocan los assets de Custom UI en:

```text
resources/Common/UI/Custom/
  MyHud.ui
  MyShop.ui
  Common.ui
  MyBackground.png
```

Asegurate tambien de que tu `manifest.json` incluya:

```json
{
  "IncludesAssetPack": true
}
```

## Arquitectura central

La documentacion oficial de Custom UI describe un flujo orientado a comandos:

1. Java construye comandos de UI con `UICommandBuilder`
2. El cliente carga el markup `.ui` y renderiza los elementos
3. El jugador interactua con la UI
4. Los eventos regresan a Java
5. Tu plugin procesa los datos y envia actualizaciones de vuelta

Por eso, Custom UI pertenece a la capa de **Java/plugin** y no a la capa de JSON puro usada para objetos, NPCs, recetas y contenido similar.

## Fundamentos de markup `.ui`

La UI moddable actual de Hytale usa archivos `.ui`. La guia de la comunidad indica que este formato es el que se usa hoy en el juego, aunque se ha hablado de una futura transicion a NoesisGUI.

Conceptos basicos:

- La UI se define de forma declarativa en archivos `.ui`
- Los elementos se acceden por IDs como `#MyButton`
- Java actualiza propiedades mediante selectores como `#MyLabel.TextSpans`
- Variables y estilos compartidos pueden importarse desde archivos como `Common.ui`

Ejemplo minimo:

```text
$Common = "Common.ui";

Group {
  Label #Title {
    Text: "Hello";
  }
}
```

## Flujo de HUD

Para un overlay persistente, hereda `CustomUIHud` y haz append de un archivo `.ui` en `build()`:

```java
@Override
public void build(UICommandBuilder uiCommandBuilder) {
  uiCommandBuilder.append("MyHud.ui");
}
```

Muestralo u ocultalo mediante el HUD manager del jugador:

- `player.getHudManager().setCustomHud(...)`
- `player.getHudManager().hideHudComponents(...)`

### Multiples HUDs

La guia de plugins de Hytale Modding **no** documenta una API oficial llamada `MultipleUI`. Lo que si menciona es un helper de comunidad llamado **MultipleHUD** para mostrar mas de un HUD personalizado al mismo tiempo. Tratalo como una utilidad opcional de la comunidad, no como una capacidad nativa garantizada del motor.

## Flujo de pagina interactiva

Usa `InteractiveCustomUIPage<T>` cuando el jugador necesite escribir, hacer clic o enviar datos de vuelta al servidor.

Piezas tipicas:

1. Un archivo `.ui` con IDs de elementos
2. Una clase de datos con `BuilderCodec<T>`
3. Bindings de eventos creados en `build(...)`
4. `handleDataEvent(...)` para procesar la entrada
5. `sendUpdate()` despues de manejar el input

Patron de binding:

```java
uiCommandBuilder.append("MyUI.ui");
uiEventBuilder.addEventBinding(
  CustomUIEventBindingType.ValueChanged,
  "#MyInput",
  EventData.of("@MyInput", "#MyInput.Value"),
  false
);
```

Comportamiento importante destacado por la guia de la comunidad: despues de recibir input, debes cambiar a otra UI o llamar a `sendUpdate()`, de lo contrario el cliente puede quedarse atascado mostrando un estado de carga.

## Cuando usar Custom UI

Usa Custom UI cuando los sistemas nativos basados en JSON no sean suficientes, por ejemplo:

- Tiendas personalizadas con validacion del lado del servidor
- Arboles de dialogo y paneles administrativos
- Formularios, cajas de busqueda o filtros
- HUDs de quests
- Paneles de estado ligados al estado de un plugin

No recurras primero a Custom UI si ya existe un sistema nativo que resuelva el problema, como:

- Pestanas de crafting de bancadas
- UI de intercambio de barter shops
- Tarjetas de descubrimiento de instancias
- Descripciones de carga de portales

Esos casos ya estan cubiertos por data assets existentes.

## Errores comunes

- Archivo `.ui` no encontrado: la ruta no coincide con `resources/Common/UI/Custom/...`
- Asset pack deshabilitado: falta `"IncludesAssetPack": true`
- Pantalla atascada en carga: la pagina interactiva proceso input pero no llamo a `sendUpdate()`
- Esperar reemplazar inventario o hotbar: esos pertenecen a la UI integrada del cliente

## Paginas relacionadas

- [Plugins Java del servidor](/hytale-modding-docs/es/getting-started/java-server-plugins) — cuando Java es obligatorio
- [Estructura del proyecto](/hytale-modding-docs/es/getting-started/project-structure) — layouts `Assets/...` versus `resources/...`
- [Instances](/hytale-modding-docs/es/reference/game-configuration/instances) — discovery UI nativa para tarjetas de instancia
- [Claves de localizacion](/hytale-modding-docs/es/reference/concepts/localization-keys) — traduccion de labels y texto de UI
