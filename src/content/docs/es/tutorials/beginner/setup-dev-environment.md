---
title: Configura tu entorno de desarrollo
description: Instala las herramientas requeridas y crea una estructura de mod mínima funcional para comenzar a crear mods de Hytale.
---

## Objetivo

Instalar las herramientas que necesitas, crear una carpeta de mod con un `manifest.json` válido y cargar un mod de prueba mínimo en el juego. Al finalizar tendrás una base funcional sobre la cual construir todos los tutoriales siguientes.

## Requisitos previos

- Hytale instalado (el cliente del juego o una compilación de servidor local)
- Acceso de administrador o escritura al directorio de mods del juego
- Conexión a internet para descargar herramientas

---

## Paso 1: Instalar las herramientas requeridas

Necesitas tres herramientas para trabajar con mods de Hytale de manera eficiente.

### Hytale (cliente del juego o servidor)

El juego es necesario para cargar y probar mods. Los mods se cargan desde una carpeta `mods/` en el directorio de datos del juego — la ruta exacta aparece en la configuración del launcher.

### Visual Studio Code

VS Code es el editor recomendado para archivos JSON de Hytale. Proporciona resaltado de sintaxis, detección de errores y validación de esquemas JSON.

Descárgalo en: **https://code.visualstudio.com/**

Después de instalarlo, agrega las siguientes extensiones desde el panel de Extensiones de VS Code (`Ctrl+Shift+X`):

| Extensión | Propósito |
|-----------|-----------|
| **JSON** (integrado) | Resaltado de sintaxis y coincidencia de corchetes |
| **Error Lens** | Muestra errores de validación JSON en línea |
| **Prettier** | Formatea automáticamente el JSON al guardar para mantener la estructura consistente |

### Blockbench

Blockbench es la herramienta de modelado 3D usada para crear archivos `.blockymodel` para objetos, NPCs y decoraciones. El plugin de Hytale agrega soporte de exportación para el formato nativo de Hytale.

Descárgalo en: **https://www.blockbench.net/**

Después de instalar Blockbench:

1. Abre Blockbench
2. Ve a **File > Plugins**
3. Busca `Hytale`
4. Instala el plugin **Hytale Exporter**
5. Reinicia Blockbench

El plugin agrega la opción de exportación **Hytale Blocky Model** bajo **File > Export**.

---

## Paso 2: Crear la estructura de carpetas del mod

Cada mod de Hytale es una carpeta con un `manifest.json` en su raíz. El nombre de la carpeta se convierte en el identificador interno de tu mod — usa solo letras, números y guiones bajos.

Crea la siguiente estructura de carpetas:

```
MyMod/
  manifest.json
  Assets/
    Common/
      BlockTextures/
        MyMod/
      Models/
        Items/
        NPCs/
    Server/
      Item/
        Block/
          Blocks/
            MyMod/
        Items/
          MyMod/
        Recipes/
          MyMod/
      NPC/
        Roles/
          MyMod/
        Spawn/
          World/
      Drops/
        NPCs/
          MyMod/
      BlockTypeList/
    Languages/
```

No necesitas todas las carpetas de inmediato — créalas a medida que agregues contenido. Lo mínimo requerido es `manifest.json` y la carpeta `Assets/`.

---

## Paso 3: Crear manifest.json

El archivo `manifest.json` identifica tu mod ante el juego. El motor lo lee al iniciar para registrar el mod y sus rutas de assets.

Crea `MyMod/manifest.json`:

```json
{
  "Group": "MyMod",
  "Name": "My First Hytale Mod"
}
```

| Campo | Propósito |
|-------|-----------|
| `Group` | Namespace interno de tu mod. Se usa para evitar conflictos de nombres con otros mods. Haz que coincida con el nombre de tu carpeta |
| `Name` | Nombre visible en la lista de mods |

Compara con el `manifest.json` del juego base en `Assets/manifest.json`:

```json
{
  "Group": "Hytale",
  "Name": "Hytale"
}
```

Tu valor de `Group` debe ser único — evita usar `Hytale` o nombres genéricos como `Mod` que podrían entrar en conflicto con otros mods.

---

## Paso 4: Configurar VS Code para edición de JSON

Abre la carpeta de tu mod en VS Code:

```
File > Open Folder > selecciona MyMod/
```

### Configurar formato automático al guardar

Crea `.vscode/settings.json` dentro de la carpeta de tu mod:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "[json]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "files.associations": {
    "*.lang": "properties"
  }
}
```

Esto asegura que tu JSON siempre tenga un formato válido — las comas finales y los errores de sintaxis se detectan antes de que intentes cargar el mod.

### Activar sugerencias de validación JSON

El servidor de lenguaje JSON integrado de VS Code marca errores de sintaxis en línea. Cuando abres un archivo `.json`:

- Los subrayados rojos indican errores de sintaxis (comas faltantes, corchetes sin cerrar)
- Los subrayados amarillos de Error Lens indican advertencias

**Consejo:** El JSON de Hytale usa un superconjunto de JSON estándar en algunos casos — los nombres de campo y los valores de cadena distinguen entre mayúsculas y minúsculas. El motor rechazará `"material": "solid"` pero aceptará `"Material": "Solid"`.

---

## Paso 5: Configurar Blockbench para Hytale

Después de instalar el plugin Hytale Exporter:

1. Abre Blockbench
2. Crea un nuevo modelo: **File > New > Hytale Blocky Model**
3. Construye tu modelo usando cubos y grupos de huesos
4. Establece la textura en el panel **Textures** del lado derecho
5. Exporta con **File > Export > Export Hytale Blocky Model**

### Convenciones de modelo

| Convención | Detalle |
|------------|---------|
| Escala | 1 unidad de Blockbench = 1/16 de un bloque de Hytale |
| Punto de pivote | Centra el modelo en `[0, 0, 0]` para el posicionamiento correcto en la mano |
| Tamaño de textura | Solo potencias de dos: 16x16, 32x32, 64x64, 128x128 |
| Nombres de huesos | Sigue los patrones de nombres del juego base (`Root`, `Body`, `Head`) para compatibilidad con animaciones |
| Formato de archivo | Exporta como `.blockymodel`; las texturas se exportan por separado como `.png` |

---

## Paso 6: Crear un mod de prueba mínimo

Con tu estructura de carpetas y manifest en su lugar, agrega un solo bloque para verificar que todo el proceso funciona de principio a fin.

Crea `MyMod/Assets/Server/Item/Block/Blocks/MyMod/Block_Test.json`:

```json
{
  "Textures": [
    {
      "All": "Blocks/_Debug/Texture.png"
    }
  ],
  "Material": "Solid"
}
```

Esto referencia la textura de depuración del juego base para que no necesites crear arte todavía.

Crea `MyMod/Assets/Server/BlockTypeList/MyMod_Blocks.json`:

```json
{
  "Blocks": [
    "Block_Test"
  ]
}
```

Crea `MyMod/Assets/Server/Item/Items/MyMod/Block_Test.json`:

```json
{
  "TranslationProperties": {
    "Name": "server.items.Block_Test.name"
  },
  "Quality": "Common",
  "Icon": "Icons/Items/Block_Rock_Grey.png",
  "BlockType": {
    "Material": "Solid",
    "DrawType": "Block",
    "Opacity": "Opaque"
  },
  "MaxStack": 64
}
```

Crea `MyMod/Assets/Languages/en-US.lang`:

```
server.items.Block_Test.name=Test Block
```

Tu estructura de mod mínima final:

```
MyMod/
  manifest.json
  Assets/
    Server/
      Item/
        Block/
          Blocks/
            MyMod/
              Block_Test.json
        Items/
          MyMod/
            Block_Test.json
      BlockTypeList/
        MyMod_Blocks.json
    Languages/
      en-US.lang
```

---

## Paso 7: Cargar y probar el mod

1. Copia tu carpeta `MyMod/` en el directorio `mods/` del juego. La ruta varía según la instalación — revisa el launcher o la configuración del servidor para la ubicación exacta.
2. Inicia el juego o el servidor.
3. Observa el log de inicio en busca de líneas que referencien los archivos de tu mod. Los errores siempre incluyen la ruta del archivo y el nombre del campo problemático.
4. Una vez cargado, usa la consola de desarrollador del juego o el generador de objetos para darte `Block_Test`.
5. Coloca el bloque y confirma que se renderiza con la textura de depuración.

### Lectura de errores de inicio

| Patrón del log | Significado |
|----------------|------------|
| `Loaded mod: MyMod` | Manifest encontrado y leído exitosamente |
| `Unknown block id: Block_Test` | El bloque no está registrado en ningún BlockTypeList |
| `Texture not found: Blocks/_Debug/Texture.png` | Error en la ruta o los assets del juego base no se están cargando |
| `JSON parse error in Block_Test.json` | Error de sintaxis — abre en VS Code para encontrar el subrayado rojo |

---

## Archivos completos

### `MyMod/manifest.json`
```json
{
  "Group": "MyMod",
  "Name": "My First Hytale Mod"
}
```

### `MyMod/.vscode/settings.json`
```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "[json]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "files.associations": {
    "*.lang": "properties"
  }
}
```

### `MyMod/Assets/Server/Item/Block/Blocks/MyMod/Block_Test.json`
```json
{
  "Textures": [
    {
      "All": "Blocks/_Debug/Texture.png"
    }
  ],
  "Material": "Solid"
}
```

### `MyMod/Assets/Server/BlockTypeList/MyMod_Blocks.json`
```json
{
  "Blocks": [
    "Block_Test"
  ]
}
```

### `MyMod/Assets/Server/Item/Items/MyMod/Block_Test.json`
```json
{
  "TranslationProperties": {
    "Name": "server.items.Block_Test.name"
  },
  "Quality": "Common",
  "Icon": "Icons/Items/Block_Rock_Grey.png",
  "BlockType": {
    "Material": "Solid",
    "DrawType": "Block",
    "Opacity": "Opaque"
  },
  "MaxStack": 64
}
```

### `MyMod/Assets/Languages/en-US.lang`
```
server.items.Block_Test.name=Test Block
```

---

## Siguientes pasos

- [Crear un bloque personalizado](/hytale-modding-docs/tutorials/beginner/create-a-block) — construye un bloque brillante completo con textura, receta y definición de objeto
- [Crear un objeto personalizado](/hytale-modding-docs/tutorials/beginner/create-an-item) — agrega un arma fabricable con estadísticas de daño
- [Crear un NPC personalizado](/hytale-modding-docs/tutorials/beginner/create-an-npc) — genera una criatura pasiva con tabla de botín
- [Conceptos básicos de JSON](/hytale-modding-docs/getting-started/json-basics) — referencia más detallada sobre herencia de plantillas y validación
