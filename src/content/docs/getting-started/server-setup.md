---
title: Server Setup
description: How to set up a local Hytale server for mod testing.
---

## Setting Up a Test Server

To test your mods, you need a local Hytale server running with your mod loaded.

### Step 1: Locate the Server

The Hytale server executable is included with your game installation. Look for the server files in your Hytale installation directory.

### Step 2: Configure Mods

Place your mod folder in the server's mods directory. The server reads mod folders and loads their `manifest.json` on startup.

### Step 3: Launch and Test

Start the server and connect to `localhost` from the game client. Changes to JSON configuration files typically require a server restart to take effect.

## Hot Reload

Some asset changes (textures, models) may be picked up without a full restart, but server-side JSON changes (NPC roles, item definitions, spawn rules) always require a restart.

## Troubleshooting

- **Mod not loading**: Check that `manifest.json` exists at the mod root with valid `Group` and `Name` fields
- **JSON parse errors**: Validate your JSON files — common issues include trailing commas and missing quotes
- **Assets not found**: Verify file paths match exactly (case-sensitive on some systems)
