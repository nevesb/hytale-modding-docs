---
title: Project Structure
description: Complete breakdown of the Hytale mod folder structure.
---

## Server Directory

The `Server/` folder contains all server-side data definitions. The server reads these JSON files to define game behavior.

### NPC System

| Path | Purpose |
|------|---------|
| `Server/NPC/Roles/` | NPC behavior definitions — stats, AI, appearance |
| `Server/NPC/Spawn/` | Spawn rules — where, when, and how NPCs appear |
| `Server/NPC/Attitude/` | NPC attitude definitions toward players |
| `Server/NPC/DecisionMaking/` | AI condition evaluators |
| `Server/NPC/Balancing/` | Combat AI behavior trees |
| `Server/NPC/Groups/` | NPC groupings for spawn/interaction rules |
| `Server/NPC/Flocks/` | Flock behavior patterns |

### Item System

| Path | Purpose |
|------|---------|
| `Server/Item/Items/` | Item definitions — stats, recipes, icons |
| `Server/Item/Block/` | Block type definitions — textures, materials |
| `Server/Item/Recipes/` | Crafting recipes |
| `Server/Item/Category/` | Item category hierarchy for inventory UI |
| `Server/Item/Qualities/` | Rarity tiers (Common, Uncommon, Rare, Epic) |
| `Server/Item/Interactions/` | Block/item interaction chains |
| `Server/Item/Groups/` | Item groupings |
| `Server/Item/ResourceTypes/` | Resource type definitions |

### World & Combat

| Path | Purpose |
|------|---------|
| `Server/Models/` | Server-side model definitions — hitboxes, animations |
| `Server/Drops/` | Loot table definitions |
| `Server/Projectiles/` | Simple projectile definitions |
| `Server/ProjectileConfigs/` | Advanced projectile configurations |
| `Server/Entity/` | Entity properties — damage types, stats, effects |
| `Server/Environments/` | Biome environment configurations |
| `Server/Weathers/` | Weather visual definitions |
| `Server/HytaleGenerator/` | World generation rules |
| `Server/BarterShops/` | NPC shop inventories |
| `Server/Farming/` | Farm and coop configurations |
| `Server/GameplayConfigs/` | Core game settings |

## Common Directory

The `Common/` folder contains client-side assets rendered by the game client.

| Path | Purpose |
|------|---------|
| `Common/Blocks/` | Block models (`.blockymodel`), animations (`.blockyanim`), textures |
| `Common/Characters/` | Player character models and animations |
| `Common/Items/` | Item models and textures |
| `Common/NPC/` | NPC client-side models and animations |
| `Common/Icons/` | UI icons for items and abilities |
| `Common/Sounds/` | Sound effects |
| `Common/Music/` | Music tracks |
| `Common/Particles/` | Particle effect definitions |
| `Common/UI/` | UI layout definitions |
| `Common/BlockTextures/` | Block face textures |

## Notes About Modern Plugin Workflows

If you are building **Java server plugins with asset packs**, community guides often describe the asset side of the plugin under `resources/Common/...` and `resources/Server/...`. The extracted vanilla assets documented in this manual still use the `Assets/...` structure, so you should translate paths based on the workflow you are following.

- For server JSON extracted from the game, keep using the `Assets/Server/...` references documented here.
- For plugin-packaged UI, look for `.ui` files under `resources/Common/UI/Custom`.
- For plugin projects that ship custom art, make sure `manifest.json` enables `"IncludesAssetPack": true`.

## Related Pages

- [Custom UI](/hytale-modding-docs/reference/game-configuration/custom-ui) — server-controlled pages, HUDs, `.ui` files, and event flow
- [Java Server Plugins](/hytale-modding-docs/getting-started/java-server-plugins) — when to use Java instead of JSON-only content
