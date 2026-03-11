---
title: Estructura del proyecto
description: Desglose completo de la estructura de carpetas de un mod de Hytale.
---

## Directorio Server

La carpeta `Server/` contiene todas las definiciones de datos del lado del servidor. El servidor lee estos archivos JSON para definir el comportamiento del juego.

### Sistema de NPCs

| Ruta | Propósito |
|------|-----------|
| `Server/NPC/Roles/` | Definiciones de comportamiento de NPCs — estadísticas, IA, apariencia |
| `Server/NPC/Spawn/` | Reglas de aparición — dónde, cuándo y cómo aparecen los NPCs |
| `Server/NPC/Attitude/` | Definiciones de actitud de NPCs hacia los jugadores |
| `Server/NPC/DecisionMaking/` | Evaluadores de condiciones de IA |
| `Server/NPC/Balancing/` | Árboles de comportamiento de IA de combate |
| `Server/NPC/Groups/` | Agrupaciones de NPCs para reglas de aparición e interacción |
| `Server/NPC/Flocks/` | Patrones de comportamiento de manada |

### Sistema de objetos

| Ruta | Propósito |
|------|-----------|
| `Server/Item/Items/` | Definiciones de objetos — estadísticas, recetas, íconos |
| `Server/Item/Block/` | Definiciones de tipos de bloques — texturas, materiales |
| `Server/Item/Recipes/` | Recetas de fabricación |
| `Server/Item/Category/` | Jerarquía de categorías de objetos para la interfaz de inventario |
| `Server/Item/Qualities/` | Niveles de rareza (Común, Poco común, Raro, Épico) |
| `Server/Item/Interactions/` | Cadenas de interacción de bloques/objetos |
| `Server/Item/Groups/` | Agrupaciones de objetos |
| `Server/Item/ResourceTypes/` | Definiciones de tipos de recursos |

### Mundo y combate

| Ruta | Propósito |
|------|-----------|
| `Server/Models/` | Definiciones de modelos del lado del servidor — hitboxes, animaciones |
| `Server/Drops/` | Definiciones de tablas de botín |
| `Server/Projectiles/` | Definiciones simples de proyectiles |
| `Server/ProjectileConfigs/` | Configuraciones avanzadas de proyectiles |
| `Server/Entity/` | Propiedades de entidades — tipos de daño, estadísticas, efectos |
| `Server/Environments/` | Configuraciones de entorno de biomas |
| `Server/Weathers/` | Definiciones visuales del clima |
| `Server/HytaleGenerator/` | Reglas de generación del mundo |
| `Server/BarterShops/` | Inventarios de tiendas de NPCs |
| `Server/Farming/` | Configuraciones de granjas y corrales |
| `Server/GameplayConfigs/` | Configuraciones principales del juego |

## Directorio Common

La carpeta `Common/` contiene los assets del lado del cliente que son renderizados por el cliente del juego.

| Ruta | Propósito |
|------|-----------|
| `Common/Blocks/` | Modelos de bloques (`.blockymodel`), animaciones (`.blockyanim`), texturas |
| `Common/Characters/` | Modelos y animaciones de personajes jugadores |
| `Common/Items/` | Modelos y texturas de objetos |
| `Common/NPC/` | Modelos y animaciones del lado del cliente para NPCs |
| `Common/Icons/` | Íconos de interfaz para objetos y habilidades |
| `Common/Sounds/` | Efectos de sonido |
| `Common/Music/` | Pistas de música |
| `Common/Particles/` | Definiciones de efectos de partículas |
| `Common/UI/` | Definiciones de diseño de interfaz de usuario |
| `Common/BlockTextures/` | Texturas de las caras de los bloques |
