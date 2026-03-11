---
title: Crear un Arma de Proyectil
description: Tutorial paso a paso para crear un arma de proyectil con definiciones de proyectiles, configs de proyectiles y cadenas de interacción.
---

## Objetivo

Crear un **Bastón de Escarcha** personalizado que dispare proyectiles de rayo de hielo. Definirás la entidad del proyectil, crearás un config de proyectil que controle la física de lanzamiento e interacciones de impacto, y conectarás todo a través de la cadena de interacción del arma.

## Lo que Aprenderás

- Cómo las definiciones de proyectiles controlan apariencia, física y daño
- Cómo los configs de proyectiles conectan armas con proyectiles mediante configuraciones de lanzamiento
- Cómo la cadena de interacción dispara proyectiles al usar el arma
- Cómo las interacciones de impacto y fallo manejan efectos de impacto

## Requisitos Previos

- Una carpeta de mod con un `manifest.json` válido (ver [Configura tu Entorno de Desarrollo](/es/hytale-modding-docs/tutorials/beginner/setup-dev-environment))
- Familiaridad con definiciones de objetos (ver [Crear un Objeto Personalizado](/es/hytale-modding-docs/tutorials/beginner/create-an-item))

---

## Descripción General del Sistema de Proyectiles

El sistema de proyectiles de Hytale tiene tres capas:

1. **Definición de Proyectil** (`Assets/Server/Projectiles/`) -- define la entidad del proyectil en sí: apariencia, física, daño y efectos
2. **Config de Proyectil** (`Assets/Server/ProjectileConfigs/`) -- conecta un arma a un proyectil con fuerza de lanzamiento, sonidos y cadenas de interacción para impacto/fallo
3. **Objeto Arma** -- referencia el config de proyectil a través de su cadena de interacción

```
Objeto Arma
  └─ referencia → Config de Proyectil
                     └─ referencia → Definición de Proyectil
```

---

## Paso 1: Crear la Definición del Proyectil

Las definiciones de proyectiles describen el proyectil físico que viaja por el mundo. Los archivos vanilla `Ice_Bolt.json` y `Arrow_FullCharge.json` son buenos puntos de referencia.

Crea:

```
YourMod/Assets/Server/Projectiles/Frost_Bolt.json
```

```json
{
  "Appearance": "Ice_Bolt",
  "Radius": 0.2,
  "Height": 0.2,
  "SticksVertically": true,
  "MuzzleVelocity": 45,
  "TerminalVelocity": 50,
  "Gravity": 5,
  "Bounciness": 0,
  "ImpactSlowdown": 0,
  "TimeToLive": 15,
  "Damage": 18,
  "DeadTimeMiss": 0,
  "DeathEffectsOnHit": true,
  "HorizontalCenterShot": 0.15,
  "VerticalCenterShot": 0.1,
  "DepthShot": 1.5,
  "PitchAdjustShot": true,
  "HitParticles": {
    "SystemId": "Impact_Ice"
  },
  "DeathParticles": {
    "SystemId": "Impact_Ice"
  },
  "HitSoundEventId": "SFX_Ice_Break",
  "MissSoundEventId": "SFX_Ice_Break",
  "DeathSoundEventId": "SFX_Ice_Break"
}
```

### Campos del proyectil explicados

| Campo | Propósito |
|-------|-----------|
| `Appearance` | El modelo visual del proyectil. Debe coincidir con un nombre de apariencia de proyectil conocido |
| `Radius` / `Height` | Dimensiones de la hitbox de colisión del proyectil |
| `MuzzleVelocity` | Velocidad inicial de lanzamiento (unidades por segundo) |
| `TerminalVelocity` | Velocidad máxima que el proyectil puede alcanzar |
| `Gravity` | Aceleración descendente. Valores más bajos = trayectoria más plana. Las flechas usan 10, los rayos de hielo usan 3-5 |
| `Bounciness` | Cuánto rebota el proyectil al impactar. `0` = sin rebote |
| `ImpactSlowdown` | Reducción de velocidad al impactar. `0` = el proyectil se detiene |
| `TimeToLive` | Segundos antes de que el proyectil desaparezca si no impacta nada |
| `Damage` | Daño base infligido al impactar |
| `SticksVertically` | Si es `true`, el proyectil se incrusta en superficies al fallar |
| `DeadTimeMiss` | Segundos que el proyectil persiste después de fallar. `0` = desaparece inmediatamente |
| `DeathEffectsOnHit` | Si es `true`, las partículas de muerte se reproducen al impactar además de al expirar naturalmente |
| `HorizontalCenterShot` / `VerticalCenterShot` | Dispersión de precisión. Valores más bajos = más preciso. `0` = perfectamente centrado |
| `DepthShot` | Desplazamiento frontal desde el personaje cuando el proyectil aparece |
| `PitchAdjustShot` | Si es `true`, el ángulo inicial del proyectil coincide con la inclinación de puntería del jugador |
| `HitParticles` / `DeathParticles` | IDs del sistema de efectos de partículas reproducidos al impactar o morir |
| `HitSoundEventId` / `MissSoundEventId` | Eventos de sonido para impacto y fallo |

---

## Paso 2: Crear el Config de Proyectil

El config de proyectil conecta un arma a un proyectil. Especifica fuerza de lanzamiento, sobrescrituras de física, sonidos y la cadena de interacción que se ejecuta al impactar o fallar. Los configs se encuentran en `Assets/Server/ProjectileConfigs/`.

Crea:

```
YourMod/Assets/Server/ProjectileConfigs/Weapons/Staff/Projectile_Config_Frost_Staff.json
```

```json
{
  "Model": "Ice_Bolt",
  "LaunchForce": 20,
  "Physics": {
    "Type": "Standard",
    "Gravity": 5,
    "TerminalVelocityAir": 50,
    "TerminalVelocityWater": 15,
    "RotationMode": "VelocityDamped",
    "Bounciness": 0.0,
    "SticksVertically": true
  },
  "LaunchLocalSoundEventId": "SFX_Staff_Shoot_Local",
  "LaunchWorldSoundEventId": "SFX_Staff_Shoot",
  "Interactions": {
    "ProjectileHit": {
      "Interactions": [
        {
          "Type": "Replace",
          "Var": "Primary_Shoot_Damage",
          "DefaultValue": {
            "Interactions": [
              "Weapon_Staff_Frost_Damage"
            ]
          }
        },
        {
          "Type": "Replace",
          "Var": "Primary_Shoot_Impact",
          "DefaultValue": {
            "Interactions": [
              "Common_Projectile_Impact_Effects"
            ]
          }
        },
        "Common_Projectile_Despawn"
      ]
    },
    "ProjectileMiss": {
      "Interactions": [
        {
          "Type": "Replace",
          "Var": "Primary_Shoot_Miss",
          "DefaultValue": {
            "Interactions": [
              "Common_Projectile_Miss"
            ]
          }
        },
        "Common_Projectile_Despawn"
      ]
    }
  }
}
```

### Campos del config de proyectil

| Campo | Propósito |
|-------|-----------|
| `Model` | El modelo de apariencia del proyectil a usar |
| `LaunchForce` | Fuerza aplicada al disparar. Mayor = velocidad inicial más rápida |
| `Physics.Type` | Tipo de simulación física. `"Standard"` es el predeterminado |
| `Physics.Gravity` | Sobrescritura de gravedad para el config (sobrescribe el valor de la definición del proyectil) |
| `Physics.TerminalVelocityAir` / `TerminalVelocityWater` | Velocidad máxima en aire y agua |
| `Physics.RotationMode` | Cómo rota el proyectil en vuelo. `"VelocityDamped"` hace que mire en la dirección de viaje |
| `Interactions.ProjectileHit` | Cadena de interacción ejecutada cuando el proyectil impacta una entidad |
| `Interactions.ProjectileMiss` | Cadena de interacción ejecutada cuando el proyectil impacta terreno o expira |

### Estructura de la cadena de interacción

El objeto `Interactions` usa un patrón de reemplazo de variables. Cada entrada con `"Type": "Replace"` define una variable nombrada (`Var`) con un `DefaultValue` que contiene referencias de interacción. Esto permite que las plantillas sobrescriban partes específicas de la cadena. Las entradas de cadena (como `"Common_Projectile_Despawn"`) referencian archivos de interacción compartidos.

---

## Paso 3: Crear el Objeto Arma

El objeto arma referencia el config de proyectil a través de su configuración de interacción. Crea la definición del objeto bastón:

```
YourMod/Assets/Server/Item/Items/Weapon/Weapon_Staff_Frost.json
```

```json
{
  "TranslationProperties": {
    "Name": "server.items.Weapon_Staff_Frost.name",
    "Description": "server.items.Weapon_Staff_Frost.description"
  },
  "Icon": "Icons/MyMod/Weapon_Staff_Frost.png",
  "Quality": "Rare",
  "MaxStack": 1,
  "ItemLevel": 5,
  "Interactions": {
    "Primary": "Staff_Frost_Primary_Shoot",
    "Secondary": "Staff_Frost_Secondary_Block"
  },
  "ProjectileConfig": "Projectile_Config_Frost_Staff",
  "Recipe": {
    "TimeSeconds": 8,
    "Input": [
      {
        "ItemId": "Ingredient_Bar_Iron",
        "Quantity": 5
      },
      {
        "ItemId": "Ingredient_Ice_Essence",
        "Quantity": 10
      },
      {
        "ItemId": "Ingredient_Crystal_Cyan",
        "Quantity": 3
      }
    ],
    "OutputQuantity": 1,
    "BenchRequirement": [
      {
        "Type": "Crafting",
        "Id": "Weapon_Bench",
        "Categories": [
          "Weapon_Bow"
        ]
      }
    ]
  },
  "PlayerAnimationsId": "Staff",
  "Tags": {
    "Type": [
      "Weapon"
    ],
    "Family": [
      "Staff"
    ]
  },
  "ItemSoundSetId": "ISS_Weapons_Staff"
}
```

### Campos clave del arma

| Campo | Propósito |
|-------|-----------|
| `Interactions.Primary` | El archivo de interacción activado con el ataque primario (clic izquierdo). Esta cadena de interacción finalmente dispara el proyectil |
| `Interactions.Secondary` | El archivo de interacción activado con la acción secundaria (clic derecho) |
| `ProjectileConfig` | Referencia el archivo de config de proyectil por nombre (sin `.json`). Esto es lo que conecta el arma con su proyectil |

---

## Paso 4: Agregar Claves de Traducción

```
YourMod/Assets/Languages/en-US.lang
```

```
server.items.Weapon_Staff_Frost.name=Frost Staff
server.items.Weapon_Staff_Frost.description=A staff that fires bolts of freezing ice.
```

---

## Paso 5: Probar en el Juego

1. Coloca la carpeta de tu mod en el directorio de mods del servidor.
2. Inicia el servidor y observa si hay errores sobre configs de proyectiles desconocidos o archivos de interacción faltantes.
3. Usa el spawner de objetos del desarrollador para darte `Weapon_Staff_Frost`.
4. Equipa el bastón y usa el ataque primario (clic izquierdo) para disparar el proyectil.
5. Verifica que el proyectil viaje con el arco correcto (gravedad), velocidad y apariencia.
6. Impacta un NPC y confirma que el daño se aplica y las partículas de impacto se reproducen.
7. Dispara al terreno y confirma que el sonido y partículas de fallo se reproducen.
8. Verifica que el proyectil desaparezca después de `TimeToLive` segundos si no impacta nada.

**Errores comunes y soluciones:**

| Error | Causa | Solución |
|-------|-------|----------|
| `Unknown projectile config` | Archivo de config no encontrado | Verifica la ruta del archivo bajo `ProjectileConfigs/` y que el nombre coincida con el valor de `ProjectileConfig` |
| El proyectil vuela directamente hacia arriba | `PitchAdjustShot` es false | Establece `"PitchAdjustShot": true` |
| El proyectil cae demasiado rápido | `Gravity` demasiado alto | Reduce la gravedad. Las flechas usan 10, los rayos mágicos usan 3-5 |
| Sin visual en el proyectil | `Appearance` incorrecto | Revisa `Assets/Server/Models/Projectiles/` para nombres de apariencia válidos |
| Sin daño al impactar | `Damage` es 0 o faltan interacciones | Establece `Damage` > 0 y verifica la cadena de interacción `ProjectileHit` |

---

## Próximos Pasos

- [Crear un Objeto Personalizado](/es/hytale-modding-docs/tutorials/beginner/create-an-item) -- entiende la estructura completa de definición de objetos
- [Crear un Banco de Crafteo](/es/hytale-modding-docs/tutorials/intermediate/create-a-crafting-bench) -- construye el banco donde los jugadores fabrican tu arma
- [Tablas de Botín Personalizadas](/es/hytale-modding-docs/tutorials/intermediate/custom-loot-tables) -- haz que tu arma dropee de enemigos
