---
title: Resumen de assets
description: Comprende los tipos de assets y formatos de archivo de Hytale.
---

## Formatos de archivo

Hytale utiliza varios formatos de archivo personalizados junto con los estándar:

### Configuración JSON (`.json`)

El formato principal para todos los datos del juego. Se usa para:
- Definiciones de roles de NPCs
- Definiciones de objetos y bloques
- Recetas y tablas de botín
- Reglas de aparición y generación del mundo
- Definiciones de modelos (lado del servidor)
- Configuraciones de jugabilidad

### Modelo Blocky (`.blockymodel`)

El formato de modelo 3D de Hytale. Internamente basado en JSON, contiene:
- Geometría de cuboides (posición, tamaño, rotación)
- Mapeo UV a hojas de textura
- Jerarquía de huesos para animación
- Puntos de anclaje para equipamiento

Se crea y edita con **Blockbench** usando el plugin de Hytale.

### Animación Blocky (`.blockyanim`)

El formato de animación de Hytale. Basado en JSON, contiene:
- Datos de keyframes para huesos
- Canales de posición, rotación y escala
- Configuración de bucles y temporización

### Texturas (`.png`)

Imágenes PNG estándar usadas para:
- Caras de bloques (normalmente 16x16 o 32x32)
- Texturas de modelos (la resolución varía según la complejidad del modelo)
- Elementos de interfaz e íconos
- Efectos de partículas

Hytale utiliza texturas con estilo pixel art. Resoluciones comunes:
- **16x16** — Bloques simples y objetos pequeños
- **32x32** — Bloques detallados y equipamiento
- **64x64** — Modelos grandes o complejos

## Conceptos clave

### Namespace

Cada asset se identifica por el namespace de su mod: `Group:Name`. Por ejemplo, `Hytale:Sword_Iron` se refiere a la espada de hierro en el juego base.

### Herencia

Muchos archivos JSON soportan herencia mediante los campos `Parent` o `Reference`. Esto te permite crear nuevo contenido extendiendo definiciones existentes en lugar de escribir todo desde cero. Consulta [Herencia y plantillas](/hytale-modding-docs/reference/concepts/inheritance-and-templates/) para más detalles.

### Localización

Todo el texto visible para el jugador usa claves de traducción en lugar de cadenas de texto fijas. Las claves se definen en archivos `.lang` dentro de los directorios `Languages/`. Consulta [Claves de localización](/hytale-modding-docs/reference/concepts/localization-keys/) para conocer el formato.
