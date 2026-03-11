---
title: Java Server Plugins
description: When Hytale mods need Java logic, what plugins are good for, and where JSON data assets are still the better fit.
---

## Short Answer

Use Java when your mod needs **runtime logic** that data assets alone cannot express.

If you are only defining content the engine already understands, stay in JSON. If you need to react to events, manage state, open custom UI, intercept inputs, or create new gameplay behavior, that is where Java server plugins apply.

## What JSON Already Handles Well

The extracted game assets show that a lot of Hytale content is data-driven already:

- Items and blocks
- NPC roles, spawn rules, groups, and attitudes
- Recipes, benches, drop tables, and barter shops
- Damage types, stats, projectiles, and effects
- Environments, weather, instances, and world-generation data

For those systems, start with JSON first. It is simpler, easier to validate, and closer to how vanilla content is authored.

## When Java Is the Right Tool

Based on the Hytale Modding reference, Java server plugins are the right layer for:

| Use Java for... | Why JSON is not enough |
|-----------------|------------------------|
| Commands | Commands are runtime actions handled by plugin code |
| Event listeners | You need to react when players join, click, move, fight, or trigger systems |
| Custom UI | UI pages and HUDs are driven by Java plus `.ui` assets |
| Persistent custom state | Plugin-managed data lives beyond a single static JSON file |
| Input interception / keybind-like behavior | This is handled by server code and packet/input hooks |
| Advanced instance orchestration | Spawning, loading, and routing players between instances is plugin logic |
| New gameplay systems | If the engine has no existing JSON schema for the feature, you need code |

## A Practical Decision Rule

Ask this in order:

1. Does vanilla Hytale already have a JSON schema for the thing I want?
2. Can I express the full behavior with existing fields, references, and templates?
3. Do I need to react to player actions or server events at runtime?
4. Do I need a custom UI or custom state machine?

If the answer is "yes" to the first two and "no" to the last two, stay in JSON.

If the answer is "no" to the first two or "yes" to either runtime question, use Java.

## Common Examples

### JSON-first examples

- A new ore block with drops and crafting recipes
- A passive NPC with spawn rules and a loot table
- A new projectile item using existing projectile config fields
- A portal that sends players to an existing instance

### Java-required examples

- A `/home` command with per-player saved locations
- A dungeon queue system with matchmaking and instance rotation
- A custom shop page with filters, pagination, and validation
- A hotbar ability bound to special server-side logic
- A quest tracker HUD that updates from live plugin state

## Singleplayer Still Counts

The Hytale Modding reference also notes that "server plugins" still apply to singleplayer, because singleplayer runs a local server instance. So Java logic is not only for large multiplayer servers.

## Accuracy Notes

The broader Java plugin API is still not fully documented officially. The Hytale Modding site itself describes some Java modding knowledge as established information and some as community guide material. That means:

- Use Java for the categories above with confidence
- Avoid assuming undocumented APIs exist unless you can verify them
- Prefer JSON when a built-in schema already exists

## Related Pages

- [Custom UI](/hytale-modding-docs/reference/game-configuration/custom-ui) — one of the clearest cases where Java is required
- [Project Structure](/hytale-modding-docs/getting-started/project-structure) — where JSON assets live versus plugin resources
- [JSON Basics](/hytale-modding-docs/getting-started/json-basics) — how far the data-driven layer goes before you need code
