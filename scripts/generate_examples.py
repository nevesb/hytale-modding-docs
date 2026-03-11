#!/usr/bin/env python3
"""
Generate sanitized example JSON files from Hytale game assets.

Picks representative files from each asset category and copies them
to the examples directory for use in documentation.

Usage:
    python scripts/generate_examples.py [--assets-dir PATH] [--output-dir PATH]
"""

import json
import os
import sys
import argparse
from pathlib import Path


def pick_representative_files(directory, max_files=2):
    """Pick representative JSON files from a directory — prefer smaller, complete files."""
    candidates = []

    for root, _, filenames in os.walk(directory):
        for fname in filenames:
            if not fname.endswith(".json"):
                continue
            # Skip template/core files — prefer concrete examples
            if "_Core" in root or "Template" in fname:
                continue

            fpath = Path(root) / fname
            try:
                size = fpath.stat().st_size
                candidates.append((fpath, size))
            except OSError:
                continue

    # Sort by size (prefer medium-sized files — not too small, not too large)
    candidates.sort(key=lambda x: abs(x[1] - 500))
    return [c[0] for c in candidates[:max_files]]


def sanitize_example(data, max_array_items=3):
    """Trim large arrays and deeply nested objects for documentation clarity."""
    if isinstance(data, dict):
        return {k: sanitize_example(v, max_array_items) for k, v in data.items()}
    if isinstance(data, list):
        trimmed = [sanitize_example(item, max_array_items) for item in data[:max_array_items]]
        if len(data) > max_array_items:
            trimmed.append(f"... ({len(data) - max_array_items} more items)")
        return trimmed
    return data


def main():
    parser = argparse.ArgumentParser(description="Generate example files from Hytale assets")
    parser.add_argument("--assets-dir", default="Assets", help="Path to Assets directory")
    parser.add_argument("--output-dir", default="examples", help="Path to output examples directory")
    args = parser.parse_args()

    assets_dir = Path(args.assets_dir)
    output_dir = Path(args.output_dir)

    categories = [
        ("Server/NPC/Roles", "npc-roles"),
        ("Server/NPC/Spawn", "npc-spawn"),
        ("Server/Item/Items", "item-definitions"),
        ("Server/Item/Block/Blocks", "block-definitions"),
        ("Server/Item/Recipes", "recipes"),
        ("Server/Drops", "drop-tables"),
        ("Server/Projectiles", "projectiles"),
        ("Server/ProjectileConfigs", "projectile-configs"),
        ("Server/Models", "models"),
        ("Server/BarterShops", "barter-shops"),
        ("Server/Farming", "farming"),
        ("Server/Environments", "environments"),
        ("Server/Weathers", "weathers"),
        ("Server/GameplayConfigs", "gameplay-configs"),
        ("Server/Entity/Damage", "damage-types"),
    ]

    total_generated = 0

    for subdir, category_name in categories:
        source = assets_dir / subdir
        if not source.exists():
            print(f"Skipping {subdir} (not found)")
            continue

        dest = output_dir / category_name
        dest.mkdir(parents=True, exist_ok=True)

        files = pick_representative_files(source)
        if not files:
            print(f"Skipping {subdir} (no suitable files)")
            continue

        for fpath in files:
            try:
                with open(fpath, "r", encoding="utf-8-sig") as f:
                    data = json.load(f)

                sanitized = sanitize_example(data)
                output_path = dest / fpath.name

                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(sanitized, f, indent=2, ensure_ascii=False)

                print(f"  {category_name}/{fpath.name}")
                total_generated += 1

            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                print(f"  Warning: Could not process {fpath}: {e}")

    print(f"\nDone! Generated {total_generated} example files in {output_dir}/")


if __name__ == "__main__":
    main()
