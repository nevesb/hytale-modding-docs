---
title: Custom UI
description: Reference for Hytale server-controlled UI, covering `.ui` assets, HUDs, pages, interactive pages, and the Java event flow used to update them.
---

## Overview

Hytale's moddable UI is **server-controlled Custom UI**, not the built-in client interface. According to the official documentation mirrored by Hytale Modding, the default client UI such as inventory, crafting, menus, and the base HUD is not moddable. What you can create is:

- **Custom Pages** — full-screen interactive overlays
- **Custom HUDs** — persistent overlays drawn during gameplay

These interfaces are driven by Java server plugins plus asset-pack files in `.ui` format.

## What Is and Is Not Moddable

### Client UI (not moddable)

The reference site explicitly lists the following as part of the built-in client UI:

- Main menu and settings
- Character creation
- Built-in HUD
- Inventory and crafting screens
- Development tools

These are part of the game client and are not intended to be replaced directly by mods.

### In-game UI (moddable)

Server-side plugins can show:

| UI type | Purpose | Interaction model |
|---------|---------|-------------------|
| `CustomUIHud` | Persistent overlay, quest tracker, status panel, server info | Display only |
| `CustomUIPage` | Full-screen screen without user input | Non-interactive page |
| `InteractiveCustomUIPage<T>` | Dialogs, shops, menus, forms | Interactive; events return to Java |

## File Location

Community plugin guides place Custom UI assets in:

```text
resources/Common/UI/Custom/
  MyHud.ui
  MyShop.ui
  Common.ui
  MyBackground.png
```

Also ensure your `manifest.json` includes:

```json
{
  "IncludesAssetPack": true
}
```

## Core Architecture

The official Custom UI docs describe a command-based flow:

1. Java builds UI commands with `UICommandBuilder`
2. The client loads `.ui` markup and renders elements
3. The player interacts with the UI
4. Events flow back to Java
5. Your plugin processes data and sends updates back

This is why Custom UI belongs in the **Java/plugin** layer rather than in the JSON data-only layer used for items, NPCs, recipes, and similar content.

## `.ui` Markup Basics

Hytale's current moddable UI uses `.ui` files. The community guide notes that this format is currently used in-game, even though a future move to NoesisGUI has been discussed.

Basic concepts:

- UI is defined declaratively in `.ui` files
- Elements are addressed by IDs such as `#MyButton`
- Java updates properties through selectors such as `#MyLabel.TextSpans`
- Shared variables and styles can be imported from files like `Common.ui`

Minimal example:

```text
$Common = "Common.ui";

Group {
  Label #Title {
    Text: "Hello";
  }
}
```

## HUD Workflow

For a persistent overlay, extend `CustomUIHud` and append a `.ui` file in `build()`:

```java
@Override
public void build(UICommandBuilder uiCommandBuilder) {
  uiCommandBuilder.append("MyHud.ui");
}
```

Show or hide it through the player's HUD manager:

- `player.getHudManager().setCustomHud(...)`
- `player.getHudManager().hideHudComponents(...)`

### Multiple HUDs

The Hytale Modding plugin guide does **not** document an official API called `MultipleUI`. What it does point to is a community helper named **MultipleHUD** for showing more than one custom HUD at once. Treat that as an optional community utility rather than a built-in engine feature.

## Interactive Page Workflow

Use `InteractiveCustomUIPage<T>` when the player must type, click, or otherwise send data back to the server.

Typical pieces:

1. A `.ui` file with element IDs
2. A data class with a `BuilderCodec<T>`
3. Event bindings created in `build(...)`
4. `handleDataEvent(...)` to process input
5. `sendUpdate()` after handling input

Example event binding pattern:

```java
uiCommandBuilder.append("MyUI.ui");
uiEventBuilder.addEventBinding(
  CustomUIEventBindingType.ValueChanged,
  "#MyInput",
  EventData.of("@MyInput", "#MyInput.Value"),
  false
);
```

Important behavior from the community guide: after receiving input, you must either switch to another UI or call `sendUpdate()`, otherwise the client may stay stuck showing a loading state.

## When To Use Custom UI

Use Custom UI when vanilla JSON-driven systems are not enough, for example:

- Custom shops with server-side validation
- Dialog trees and admin panels
- Custom forms, search boxes, or filters
- Quest HUD overlays
- Status panels tied to plugin state

Do **not** reach for Custom UI first if a built-in system already solves the problem, such as:

- Bench crafting tabs
- Barter shop trading UI
- Instance discovery cards
- Portal loading descriptions

Those are already supported by existing data assets.

## Common Pitfalls

- `.ui` file not found: path does not match `resources/Common/UI/Custom/...`
- Asset pack disabled: missing `"IncludesAssetPack": true`
- Waiting forever on loading: interactive page handled input but did not call `sendUpdate()`
- Expecting to replace the inventory or hotbar: those belong to the built-in client UI

## Related Pages

- [Java Server Plugins](/hytale-modding-docs/getting-started/java-server-plugins) — when Java is required
- [Project Structure](/hytale-modding-docs/getting-started/project-structure) — `Assets/...` versus `resources/...` layouts
- [Instances](/hytale-modding-docs/reference/game-configuration/instances) — built-in discovery UI for instance title cards
- [Localization Keys](/hytale-modding-docs/reference/concepts/localization-keys) — translating labels and UI text
