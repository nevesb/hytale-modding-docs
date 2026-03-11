---
title: Crear un objeto personalizado (arma)
description: Tutorial paso a paso para agregar un arma personalizada a Hytale, incluyendo el JSON de definición del objeto, una receta de fabricación y claves de traducción.
---

## Objetivo

Agregar una daga personalizada llamada **Thornwood Dagger** al juego. Crearás el JSON de definición del objeto con valores de daño y una receta de fabricación, agregarás claves de traducción para el nombre y la descripción, y la probarás en el juego.

## Requisitos previos

- Una carpeta de mod con un `manifest.json` válido (consulta [Configura tu entorno de desarrollo](/hytale-modding-docs/tutorials/beginner/setup-dev-environment))
- Blockbench instalado para crear el modelo 3D (opcional — puedes referenciar un modelo del juego base para comenzar)
- Familiaridad con JSON (consulta [Conceptos básicos de JSON](/hytale-modding-docs/getting-started/json-basics))

---

## Paso 1: Crear el modelo del objeto en Blockbench

Hytale usa el formato `.blockymodel` para los modelos 3D de objetos. Si aún no tienes Blockbench configurado, omite este paso y referencia un modelo existente del juego base para hacer funcionar tu objeto primero, y luego reemplázalo después.

Los modelos de dagas del juego base se encuentran en rutas como:

```
Items/Weapons/Dagger/Bronze.blockymodel
Items/Weapons/Dagger/Bronze_Texture.png
```

Para tu objeto personalizado, crea y exporta:

```
YourMod/Assets/Common/Models/Items/Weapons/Dagger/Thornwood.blockymodel
YourMod/Assets/Common/Models/Items/Weapons/Dagger/Thornwood_Texture.png
```

**Consejos para Blockbench:**
- Mantén el modelo centrado en el origen — Hytale usa el punto de pivote para el posicionamiento en la mano
- Exporta como **Hytale Blocky Model** usando el plugin de Hytale (consulta [Configura tu entorno de desarrollo](/hytale-modding-docs/tutorials/beginner/setup-dev-environment))
- El archivo de textura debe ser un PNG y sus dimensiones deben ser potencia de dos (por ejemplo, 16x16, 32x32, 64x64)

---

## Paso 2: Crear el JSON de definición del objeto

Las definiciones de objetos tipo arma siguen el patrón establecido por los archivos en `Assets/Server/Item/Items/Weapon/`. El archivo de dagas de bronce (`Weapon_Daggers_Bronze.json`) muestra la estructura: una plantilla `Parent` maneja el comportamiento compartido mientras que el archivo hijo sobrescribe los valores de daño, rutas de modelo, calidad y claves de traducción.

Crea:

```
YourMod/Assets/Server/Item/Items/MyMod/Weapon_Daggers_Thornwood.json
```

```json
{
  "Parent": "Template_Weapon_Daggers",
  "TranslationProperties": {
    "Name": "server.items.Weapon_Daggers_Thornwood.name",
    "Description": "server.items.Weapon_Daggers_Thornwood.description"
  },
  "Model": "Items/Weapons/Dagger/Thornwood.blockymodel",
  "Texture": "Items/Weapons/Dagger/Thornwood_Texture.png",
  "Icon": "Icons/MyMod/Weapon_Daggers_Thornwood.png",
  "Quality": "Uncommon",
  "ItemLevel": 20,
  "MaxDurability": 80,
  "DurabilityLossOnHit": 0.5,
  "Tags": {
    "Type": ["Weapon"],
    "Family": ["Daggers"]
  },
  "InteractionVars": {
    "Swing_Left_Damage": {
      "Interactions": [
        {
          "Parent": "Weapon_Daggers_Primary_Swing_Left_Damage",
          "DamageCalculator": {
            "BaseDamage": {
              "Physical": 4
            }
          },
          "DamageEffects": {
            "WorldSoundEventId": "SFX_Daggers_T2_Slash_Impact",
            "LocalSoundEventId": "SFX_Daggers_T2_Slash_Impact"
          }
        }
      ]
    },
    "Swing_Right_Damage": {
      "Interactions": [
        {
          "Parent": "Weapon_Daggers_Primary_Swing_Right_Damage",
          "DamageCalculator": {
            "BaseDamage": {
              "Physical": 4
            }
          },
          "DamageEffects": {
            "WorldSoundEventId": "SFX_Daggers_T2_Slash_Impact",
            "LocalSoundEventId": "SFX_Daggers_T2_Slash_Impact"
          }
        }
      ]
    },
    "Stab_Left_Damage": {
      "Interactions": [
        {
          "Parent": "Weapon_Daggers_Primary_Stab_Left_Damage",
          "DamageCalculator": {
            "BaseDamage": {
              "Physical": 9
            }
          },
          "DamageEffects": {
            "WorldSoundEventId": "SFX_Daggers_T2_Slash_Impact",
            "LocalSoundEventId": "SFX_Daggers_T2_Slash_Impact"
          }
        }
      ]
    },
    "Stab_Right_Damage": {
      "Interactions": [
        {
          "Parent": "Weapon_Daggers_Primary_Stab_Right_Damage",
          "DamageCalculator": {
            "BaseDamage": {
              "Physical": 12
            }
          },
          "DamageEffects": {
            "WorldSoundEventId": "SFX_Daggers_T2_Slash_Impact",
            "LocalSoundEventId": "SFX_Daggers_T2_Slash_Impact"
          }
        }
      ]
    }
  }
}
```

### Campos clave explicados

| Campo | Propósito |
|-------|-----------|
| `Parent` | Hereda todas las animaciones de ataque, interacciones y estadísticas base de la plantilla |
| `TranslationProperties` | Claves resueltas desde tu archivo `.lang` para el nombre del objeto y el tooltip |
| `Model` | Ruta al archivo `.blockymodel` |
| `Texture` | Ruta al PNG de textura del modelo |
| `Icon` | PNG del ícono del espacio de inventario |
| `Quality` | Nivel de rareza — controla el color del borde y la partícula de drop. Valores válidos: `Junk`, `Common`, `Uncommon`, `Rare`, `Epic`, `Legendary` |
| `ItemLevel` | Determina el nivel de progresión; afecta la ponderación en tablas de botín |
| `MaxDurability` | Cuántos golpes antes de que el objeto se rompa |
| `DurabilityLossOnHit` | Durabilidad restada por golpe (soporta decimales) |
| `InteractionVars` | Sobrescribe valores de daño de ataques específicos de la plantilla padre |

### Calculador de daño

Cada entrada de `InteractionVars` sobrescribe una fase de ataque. `BaseDamage` recibe una clave de tipo de daño:

| Tipo de daño | Descripción |
|-------------|-------------|
| `Physical` | Daño cuerpo a cuerpo estándar |
| `Fire` | Daño elemental de fuego |
| `Poison` | Aplica un efecto de daño con el tiempo |
| `Ice` | Daño de hielo |

Puedes combinar tipos en un solo golpe:

```json
"BaseDamage": {
  "Physical": 4,
  "Poison": 2
}
```

---

## Paso 3: Agregar una receta de fabricación

Las recetas pueden definirse en línea dentro del JSON del objeto (como se ve en `Food_Bread.json`) o en un archivo de receta separado. La forma en línea es más simple para objetos únicos. Agrega un bloque `Recipe` a tu definición de objeto:

```json
{
  "Parent": "Template_Weapon_Daggers",
  "TranslationProperties": {
    "Name": "server.items.Weapon_Daggers_Thornwood.name",
    "Description": "server.items.Weapon_Daggers_Thornwood.description"
  },
  "Model": "Items/Weapons/Dagger/Thornwood.blockymodel",
  "Texture": "Items/Weapons/Dagger/Thornwood_Texture.png",
  "Icon": "Icons/MyMod/Weapon_Daggers_Thornwood.png",
  "Quality": "Uncommon",
  "ItemLevel": 20,
  "MaxDurability": 80,
  "DurabilityLossOnHit": 0.5,
  "Tags": {
    "Type": ["Weapon"],
    "Family": ["Daggers"]
  },
  "Recipe": {
    "Input": [
      {
        "ResourceTypeId": "Wood_Trunk",
        "Quantity": 3
      },
      {
        "ItemId": "Ingredient_Fibre",
        "Quantity": 2
      },
      {
        "ItemId": "Ingredient_Bar_Copper",
        "Quantity": 1
      }
    ],
    "Output": [
      {
        "ItemId": "Weapon_Daggers_Thornwood"
      }
    ],
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Categories": ["Weapon_Daggers"],
        "Id": "Weapon_Bench"
      }
    ],
    "TimeSeconds": 4
  },
  "InteractionVars": {
    "Swing_Left_Damage": {
      "Interactions": [
        {
          "Parent": "Weapon_Daggers_Primary_Swing_Left_Damage",
          "DamageCalculator": {
            "BaseDamage": {
              "Physical": 4
            }
          },
          "DamageEffects": {
            "WorldSoundEventId": "SFX_Daggers_T2_Slash_Impact",
            "LocalSoundEventId": "SFX_Daggers_T2_Slash_Impact"
          }
        }
      ]
    },
    "Swing_Right_Damage": {
      "Interactions": [
        {
          "Parent": "Weapon_Daggers_Primary_Swing_Right_Damage",
          "DamageCalculator": {
            "BaseDamage": {
              "Physical": 4
            }
          },
          "DamageEffects": {
            "WorldSoundEventId": "SFX_Daggers_T2_Slash_Impact",
            "LocalSoundEventId": "SFX_Daggers_T2_Slash_Impact"
          }
        }
      ]
    },
    "Stab_Left_Damage": {
      "Interactions": [
        {
          "Parent": "Weapon_Daggers_Primary_Stab_Left_Damage",
          "DamageCalculator": {
            "BaseDamage": {
              "Physical": 9
            }
          },
          "DamageEffects": {
            "WorldSoundEventId": "SFX_Daggers_T2_Slash_Impact",
            "LocalSoundEventId": "SFX_Daggers_T2_Slash_Impact"
          }
        }
      ]
    },
    "Stab_Right_Damage": {
      "Interactions": [
        {
          "Parent": "Weapon_Daggers_Primary_Stab_Right_Damage",
          "DamageCalculator": {
            "BaseDamage": {
              "Physical": 12
            }
          },
          "DamageEffects": {
            "WorldSoundEventId": "SFX_Daggers_T2_Slash_Impact",
            "LocalSoundEventId": "SFX_Daggers_T2_Slash_Impact"
          }
        }
      ]
    }
  }
}
```

### Campos de receta

| Campo | Propósito |
|-------|-----------|
| `Input` | Lista de ingredientes requeridos. Usa `ItemId` para un objeto específico, o `ResourceTypeId` para una categoría de recurso (por ejemplo, cualquier tronco de madera cuenta como `Wood_Trunk`) |
| `Output` | Lo que el jugador recibe. Omitir `Quantity` usa el valor predeterminado de 1 |
| `BenchRequirement` | Qué estación de fabricación se necesita. `Id` es el identificador del banco; `Categories` filtra en qué pestaña del banco aparece |
| `TimeSeconds` | Cuánto tiempo tarda la fabricación |
| `KnowledgeRequired` | Establece `true` si la receta debe aprenderse de un pergamino antes de aparecer |

---

## Paso 4: Agregar claves de traducción

Crea o agrega a tu archivo de idioma del mod:

```
YourMod/Assets/Languages/en-US.lang
```

```
server.items.Weapon_Daggers_Thornwood.name=Thornwood Dagger
server.items.Weapon_Daggers_Thornwood.description=A light blade carved from thornwood. Fast and precise.
```

El formato de clave de traducción usado en todo el juego base: `server.items.<ItemId>.name` y `server.items.<ItemId>.description`. Sigue este patrón exactamente — el motor distingue entre mayúsculas y minúsculas.

---

## Paso 5: Probar en el juego

1. Copia la carpeta de tu mod en el directorio de mods del servidor.
2. Inicia el servidor y revisa la consola en busca de errores que referencien tu archivo de objeto.
3. Usa el generador de objetos del modo desarrollador para darte `Weapon_Daggers_Thornwood`.
4. Confirma que el modelo, la textura, el ícono y el nombre se muestren correctamente.
5. Ataca un muñeco de entrenamiento o una criatura para verificar que los números de daño coincidan con tus valores de `BaseDamage`.
6. Revisa la lista de recetas del banco de armas para encontrar tu objeto.

**Errores comunes y soluciones:**

| Error | Causa | Solución |
|-------|-------|----------|
| `Unknown parent: Template_Weapon_Daggers` | Plantilla no cargada | Asegúrate de que los assets del juego base estén presentes |
| El modelo aparece como cubo predeterminado | Ruta de `.blockymodel` incorrecta | Verifica la ruta en `Model` |
| La receta no aparece en el banco | `BenchRequirement.Id` incorrecto | Usa `Weapon_Bench` exactamente |
| El nombre muestra la clave cruda | Entrada `.lang` faltante | Agrega la clave a `en-US.lang` |

---

## Archivos completos

### `YourMod/Assets/Server/Item/Items/MyMod/Weapon_Daggers_Thornwood.json`
```json
{
  "Parent": "Template_Weapon_Daggers",
  "TranslationProperties": {
    "Name": "server.items.Weapon_Daggers_Thornwood.name",
    "Description": "server.items.Weapon_Daggers_Thornwood.description"
  },
  "Model": "Items/Weapons/Dagger/Thornwood.blockymodel",
  "Texture": "Items/Weapons/Dagger/Thornwood_Texture.png",
  "Icon": "Icons/MyMod/Weapon_Daggers_Thornwood.png",
  "Quality": "Uncommon",
  "ItemLevel": 20,
  "MaxDurability": 80,
  "DurabilityLossOnHit": 0.5,
  "Tags": {
    "Type": ["Weapon"],
    "Family": ["Daggers"]
  },
  "Recipe": {
    "Input": [
      {
        "ResourceTypeId": "Wood_Trunk",
        "Quantity": 3
      },
      {
        "ItemId": "Ingredient_Fibre",
        "Quantity": 2
      },
      {
        "ItemId": "Ingredient_Bar_Copper",
        "Quantity": 1
      }
    ],
    "Output": [
      {
        "ItemId": "Weapon_Daggers_Thornwood"
      }
    ],
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Categories": ["Weapon_Daggers"],
        "Id": "Weapon_Bench"
      }
    ],
    "TimeSeconds": 4
  },
  "InteractionVars": {
    "Swing_Left_Damage": {
      "Interactions": [
        {
          "Parent": "Weapon_Daggers_Primary_Swing_Left_Damage",
          "DamageCalculator": {
            "BaseDamage": { "Physical": 4 }
          },
          "DamageEffects": {
            "WorldSoundEventId": "SFX_Daggers_T2_Slash_Impact",
            "LocalSoundEventId": "SFX_Daggers_T2_Slash_Impact"
          }
        }
      ]
    },
    "Swing_Right_Damage": {
      "Interactions": [
        {
          "Parent": "Weapon_Daggers_Primary_Swing_Right_Damage",
          "DamageCalculator": {
            "BaseDamage": { "Physical": 4 }
          },
          "DamageEffects": {
            "WorldSoundEventId": "SFX_Daggers_T2_Slash_Impact",
            "LocalSoundEventId": "SFX_Daggers_T2_Slash_Impact"
          }
        }
      ]
    },
    "Stab_Left_Damage": {
      "Interactions": [
        {
          "Parent": "Weapon_Daggers_Primary_Stab_Left_Damage",
          "DamageCalculator": {
            "BaseDamage": { "Physical": 9 }
          },
          "DamageEffects": {
            "WorldSoundEventId": "SFX_Daggers_T2_Slash_Impact",
            "LocalSoundEventId": "SFX_Daggers_T2_Slash_Impact"
          }
        }
      ]
    },
    "Stab_Right_Damage": {
      "Interactions": [
        {
          "Parent": "Weapon_Daggers_Primary_Stab_Right_Damage",
          "DamageCalculator": {
            "BaseDamage": { "Physical": 12 }
          },
          "DamageEffects": {
            "WorldSoundEventId": "SFX_Daggers_T2_Slash_Impact",
            "LocalSoundEventId": "SFX_Daggers_T2_Slash_Impact"
          }
        }
      ]
    }
  }
}
```

### `YourMod/Assets/Languages/en-US.lang`
```
server.items.Weapon_Daggers_Thornwood.name=Thornwood Dagger
server.items.Weapon_Daggers_Thornwood.description=A light blade carved from thornwood. Fast and precise.
```

---

## Siguientes pasos

- [Crear un bloque personalizado](/hytale-modding-docs/tutorials/beginner/create-a-block) — agrega un bloque colocable que se obtiene de NPCs
- [Crear un NPC personalizado](/hytale-modding-docs/tutorials/beginner/create-an-npc) — crea una criatura que suelte tu nueva arma
- [Conceptos básicos de JSON](/hytale-modding-docs/getting-started/json-basics) — referencia sobre herencia de plantillas y encadenamiento de interacciones
