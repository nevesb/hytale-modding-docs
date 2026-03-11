---
title: Configuración del servidor
description: Cómo configurar un servidor local de Hytale para probar mods.
---

## Configurar un servidor de pruebas

Para probar tus mods, necesitas un servidor local de Hytale ejecutándose con tu mod cargado.

### Paso 1: Localizar el servidor

El ejecutable del servidor de Hytale se incluye con la instalación del juego. Busca los archivos del servidor en el directorio de instalación de Hytale.

### Paso 2: Configurar los mods

Coloca la carpeta de tu mod en el directorio de mods del servidor. El servidor lee las carpetas de mods y carga su `manifest.json` al iniciar.

### Paso 3: Iniciar y probar

Inicia el servidor y conéctate a `localhost` desde el cliente del juego. Los cambios en los archivos de configuración JSON generalmente requieren reiniciar el servidor para que surtan efecto.

## Recarga en caliente

Algunos cambios de assets (texturas, modelos) pueden aplicarse sin un reinicio completo, pero los cambios en JSON del lado del servidor (roles de NPCs, definiciones de objetos, reglas de aparición) siempre requieren un reinicio.

## Solución de problemas

- **El mod no se carga**: Verifica que `manifest.json` exista en la raíz del mod con los campos `Group` y `Name` válidos
- **Errores de parseo de JSON**: Valida tus archivos JSON — los problemas comunes incluyen comas finales y comillas faltantes
- **Assets no encontrados**: Verifica que las rutas de archivos coincidan exactamente (distingue mayúsculas de minúsculas en algunos sistemas)
