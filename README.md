# Hytale Modding Docs

Comprehensive multilingual documentation for Hytale server modding. Every JSON configuration schema documented, with step-by-step tutorials and interactive flowcharts.

**Live site:** [nevesb.github.io/hytale-modding-docs](https://nevesb.github.io/hytale-modding-docs/)

---

## What's Inside

### Reference (53 pages)

Complete schema documentation for every JSON config file in Hytale's asset system:

| Section | Pages | Covers |
|---------|-------|--------|
| Concepts | 7 | Inheritance, weights, interaction chaining, tags, time schedules, response curves, localization |
| NPC System | 8 | Roles, templates, spawn rules, attitudes, decision making, combat balancing, groups, flocks |
| Item System | 7 | Items, blocks, categories, qualities, interactions, groups, resource types |
| Crafting System | 4 | Recipes, bench definitions, bench requirements, salvage |
| Combat & Projectiles | 5 | Projectiles, configs, damage types, entity stats, entity effects |
| Economy & Progression | 4 | Drop tables, barter shops, farming coops, farming modifiers |
| World & Environment | 5 | Environments, weather, world generation, world masks, portal types |
| Models & Visuals | 6 | Server models, animation sets, client models, client animations, particles, block textures |
| Game Configuration | 6 | Gameplay configs, camera effects, macro commands, block type lists, instances, objectives |

Each reference page includes:
- Field-by-field schema table (type, required, default, description)
- Real JSON examples extracted from game assets
- Mermaid flowcharts explaining system behavior
- Cross-links to related pages

### Tutorials (17 pages)

| Level | Tutorials |
|-------|-----------|
| Beginner (4) | Create a Block, Create an Item, Create an NPC, Setup Dev Environment |
| Intermediate (6) | Crafting Bench, NPC Spawning, Projectile Weapons, Trees & Saplings, Loot Tables, NPC Shops |
| Advanced (6) | Custom Dungeons, World Gen Mods, NPC AI Behavior Trees, Combat System, Farming & Coops, Mod Packaging |
| Showcase (1) | Dude VS Dungeon — full mod walkthrough |

### JSON Schemas (36 files)

Machine-readable [JSON Schema 2020-12](https://json-schema.org/) files in `schemas/`, extracted from real game assets using `scripts/extract_schemas.py`. Covers NPC roles, items, blocks, recipes, drops, projectiles, damage types, environments, weather, and more.

### LLM Index

`public/llm-index.json` provides a machine-readable index of all pages and schemas, designed for AI tools to consume the documentation programmatically.

---

## Languages

| Language | Coverage |
|----------|----------|
| English (EN-US) | Full — all pages |
| Español (ES) | Getting Started + Beginner Tutorials |
| Português BR (PT-BR) | Getting Started + Beginner Tutorials |

Non-translated pages fall back to English automatically.

---

## Tech Stack

- **[Astro](https://astro.build/)** + **[Starlight](https://starlight.astro.build/)** — static site generator with built-in i18n
- **[Pagefind](https://pagefind.app/)** — static search across all 3 locales
- **[Shiki](https://shiki.matsu.io/)** — syntax highlighting for JSON examples
- **[Mermaid](https://mermaid.js.org/)** — interactive flowcharts and diagrams
- **GitHub Actions** — automated deployment to GitHub Pages

---

## Development

### Prerequisites

- Node.js 20+
- npm

### Commands

```bash
npm install          # Install dependencies
npm run dev          # Start dev server at localhost:4321
npm run build        # Production build to dist/
npm run preview      # Preview production build
```

### Schema Extraction

Requires the extracted `Assets/` directory (not included in repo — ~3GB):

```bash
python scripts/extract_schemas.py      # Generate schemas/ from Assets/Server/
python scripts/generate_examples.py    # Extract sanitized JSON examples
```

### Project Structure

```
src/content/docs/              # Documentation pages (root = EN-US)
  ├── getting-started/         # 5 intro pages
  ├── reference/               # 53 schema reference pages
  ├── tutorials/               # 17 tutorials (beginner/intermediate/advanced/showcase)
  ├── es/                      # Spanish translations
  ├── pt-br/                   # Portuguese (BR) translations
  └── 404.md                   # Custom 404 page
schemas/                       # 36 generated JSON Schema 2020-12 files
scripts/                       # Python extraction scripts
public/llm-index.json          # Machine-readable page index
.github/workflows/deploy.yml   # GitHub Pages deployment
astro.config.mjs               # Starlight + i18n configuration
```

---

## Deployment

The site deploys automatically to GitHub Pages on every push to `main` via the workflow in `.github/workflows/deploy.yml`.

To enable: go to **Settings > Pages** in the repository and select **GitHub Actions** as the build source.

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add or edit pages in `src/content/docs/`
4. Run `npm run build` to verify zero errors
5. Submit a pull request

### Content Conventions

- **Reference pages**: Overview → File Location → Schema Table → JSON Example → Related Pages
- **Tutorials**: What You'll Learn → Prerequisites → Step-by-step → Testing → Related Pages
- **Schema tables**: Field | Type | Required | Default | Description
- **JSON examples**: Use real sanitized data from game assets
- **Internal links**: Use `/hytale-modding-docs/` prefix

### Adding Translations

- English pages go in `src/content/docs/` (root, NOT in `en/`)
- Spanish: `src/content/docs/es/`
- Portuguese BR: `src/content/docs/pt-br/`
- Keep JSON code examples unchanged — only translate prose text

---

## Acknowledgments

- Game assets and configuration schemas are from **Hytale** by Hypixel Studios
- Inspired by [AueSip's Hytale Modding Guide](https://www.youtube.com/@AueSip) YouTube series
- Built with [Astro Starlight](https://starlight.astro.build/)

---

## License

This project is documentation for educational purposes. Hytale and its assets are property of Hypixel Studios.
