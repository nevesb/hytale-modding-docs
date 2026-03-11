---
title: Plugins Java del servidor
description: Cuando los mods de Hytale necesitan logica en Java, para que sirven los plugins y donde los data assets en JSON siguen siendo la mejor opcion.
---

## Respuesta corta

Usa Java cuando tu mod necesite **logica en tiempo de ejecucion** que los data assets por si solos no puedan expresar.

Si solo estas definiendo contenido que el motor ya entiende, quedate en JSON. Si necesitas reaccionar a eventos, gestionar estado, abrir UI personalizada, interceptar inputs o crear comportamiento nuevo de gameplay, ahi es donde entran los plugins Java del servidor.

## Lo que JSON ya resuelve bien

Los assets extraidos del juego muestran que mucho contenido de Hytale ya esta orientado a datos:

- Objetos y bloques
- Roles, reglas de aparicion, grupos y actitudes de NPC
- Recetas, bancadas, tablas de botin y barter shops
- Tipos de dano, estadisticas, proyectiles y efectos
- Environments, clima, instances y datos de generacion del mundo

Para esos sistemas, empieza por JSON. Es mas simple, mas facil de validar y esta mas cerca de como se estructura el contenido vanilla.

## Cuando Java es la herramienta correcta

Segun la referencia de Hytale Modding, los plugins Java del servidor son la capa adecuada para:

| Usa Java para... | Por que JSON no alcanza |
|------------------|-------------------------|
| Comandos | Los comandos son acciones en runtime manejadas por codigo de plugin |
| Listeners de eventos | Necesitas reaccionar cuando jugadores entran, hacen clic, se mueven, combaten o activan sistemas |
| Custom UI | Las paginas y HUDs personalizadas dependen de Java y assets `.ui` |
| Estado persistente personalizado | Los datos gestionados por el plugin van mas alla de un JSON estatico |
| Intercepcion de input / comportamiento tipo keybind | Esto se maneja con codigo del servidor y hooks de input |
| Orquestacion avanzada de instances | Spawnear, cargar y mover jugadores entre instances es logica de plugin |
| Nuevos sistemas de gameplay | Si el motor no tiene un schema JSON existente para la caracteristica, necesitas codigo |

## Regla practica de decision

Preguntate esto en orden:

1. ¿Hytale vanilla ya tiene un schema JSON para lo que quiero hacer?
2. ¿Puedo expresar todo el comportamiento con los campos, referencias y templates existentes?
3. ¿Necesito reaccionar a acciones del jugador o eventos del servidor en runtime?
4. ¿Necesito una UI personalizada o una maquina de estados personalizada?

Si la respuesta es "si" para las dos primeras y "no" para las dos ultimas, quedate en JSON.

Si la respuesta es "no" para las dos primeras o "si" para cualquiera de las preguntas de runtime, usa Java.

## Ejemplos comunes

### Ejemplos para JSON primero

- Un nuevo mineral con drops y recetas de crafting
- Un NPC pasivo con reglas de aparicion y tabla de botin
- Un objeto de proyectil usando campos existentes de projectile config
- Un portal que envia al jugador a una instance existente

### Ejemplos que requieren Java

- Un comando `/home` con ubicaciones guardadas por jugador
- Un sistema de cola para dungeons con matchmaking y rotacion de instances
- Una pagina de tienda personalizada con filtros, paginacion y validacion
- Una habilidad de hotbar ligada a logica especial del servidor
- Un HUD de quest que se actualiza con estado vivo del plugin

## Singleplayer tambien cuenta

La referencia de Hytale Modding tambien indica que los "server plugins" siguen aplicando en singleplayer, porque el modo solo ejecuta una instancia local del servidor. Asi que la logica en Java no sirve solo para grandes servidores multijugador.

## Notas de precision

La API mas amplia de plugins Java todavia no esta completamente documentada de forma oficial. El propio sitio Hytale Modding trata parte del conocimiento sobre Java como informacion establecida y parte como guias de comunidad. Eso significa:

- Usa Java para las categorias anteriores con confianza
- Evita asumir que existen APIs no documentadas sin verificarlo
- Prefiere JSON cuando ya exista un schema nativo para el sistema

## Paginas relacionadas

- [Custom UI](/hytale-modding-docs/es/reference/game-configuration/custom-ui) — uno de los casos mas claros donde Java es obligatorio
- [Estructura del proyecto](/hytale-modding-docs/es/getting-started/project-structure) — donde viven los assets JSON frente a los recursos de plugin
- [Fundamentos de JSON](/hytale-modding-docs/es/getting-started/json-basics) — hasta donde llega la capa orientada a datos antes de necesitar codigo
