# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Hytale Modding Manual** — a multilingual (EN-US, ES, PT-BR) static documentation site hosted on GitHub Pages. Documents every JSON configuration schema from Hytale's extracted game assets to help mod creators build server mods.

Built with **Astro Starlight** (static site generator with built-in i18n, Pagefind search, Shiki syntax highlighting).

## Build Commands

```bash
npm run dev          # Start dev server at localhost:4321
npm run build        # Production build to dist/
npm run preview      # Preview production build
```

**Important**: On Windows MSYS/Git Bash, use `cmd //c "npx astro build 2>&1"` if `npm run build` can't find the astro command.

## Repository Structure

```
src/content/docs/           # Documentation pages (root = EN-US)
  ├── getting-started/      # 5 intro pages
  ├── reference/            # Schema reference (concepts, npc, items, crafting, combat, economy, world, models, game-config)
  ├── tutorials/            # Beginner / Intermediate / Advanced
  ├── es/                   # Spanish translations
  ├── pt-br/                # Portuguese (BR) translations
  └── 404.md                # Custom 404 page
schemas/                    # Generated JSON Schema 2020-12 files (36 schemas, committed)
scripts/
  ├── extract_schemas.py    # Generates schemas/ from Assets/Server/
  └── generate_examples.py  # Extracts sanitized examples from assets
public/
  └── llm-index.json        # Machine-readable page + schema index for LLMs
docs/                       # Legacy tutorials (kept for reference)
Assets/                     # Extracted game assets (~3GB, gitignored)
.github/workflows/deploy.yml  # GitHub Pages deployment (Node 20)
```

## i18n Architecture

- **Default locale**: `root` (English has no URL prefix)
- English pages go directly in `src/content/docs/` (NOT in `en/`)
- Spanish: `src/content/docs/es/`
- Portuguese BR: `src/content/docs/pt-br/`
- Sidebar translations configured in `astro.config.mjs`
- Non-translated pages fall back to English automatically

**Critical**: Never put English content in `src/content/docs/en/` — it must be at the root level because `defaultLocale: 'root'` is used.

## Astro Config

- `site`: `https://nevesb.github.io`
- `base`: `/hytale-modding-docs`
- Starlight 0.33.2 + Astro 5.6.1
- Overrides: `@astrojs/sitemap@3.6.1` and `zod@3.25.76` (prevents Zod v4 compatibility crash on 404 page)

## Schema Extraction

```bash
python scripts/extract_schemas.py   # Requires Assets/Server/ to be present
```

Walks `Assets/Server/` subdirectories, reads all JSON files per category, merges observed fields into union schemas (JSON Schema 2020-12). Output: `schemas/*.schema.json`.

## Hytale Asset Patterns

Key patterns found across asset JSON files:
- **Inheritance**: `Reference`/`Modify` (overlay on existing), `Parent` (inherit from template), `Inherits` (list of parents)
- **Computed values**: `Parameter`/`Compute` for dynamic stat calculation
- **Weighted selection**: `Weight` fields in drops, spawns, loot
- **Interaction chaining**: Sequential action definitions in item interactions
- **Translation keys**: `hytale.item.name.xxx` format referencing `.lang` files

## Content Conventions

- Reference pages: Overview → File Location → Schema Table → JSON Example → Related Pages
- Tutorials: What You'll Learn → Prerequisites → Step-by-step → Testing → Related Pages
- Schema tables use: Field | Type | Required | Default | Description
- JSON examples use real sanitized data from Assets/
- Internal links use `/hytale-modding-docs/` prefix
