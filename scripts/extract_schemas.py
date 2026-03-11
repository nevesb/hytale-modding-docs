#!/usr/bin/env python3
"""
Extract JSON schemas from Hytale game assets.

Walks Assets/Server/ directories, reads all JSON files per category,
and produces JSON Schema 2020-12 files in schemas/.

Usage:
    python scripts/extract_schemas.py [--assets-dir PATH] [--output-dir PATH]
"""

import json
import os
import sys
import argparse
from pathlib import Path
from collections import defaultdict


def infer_json_type(value):
    """Map Python types to JSON Schema types."""
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    if value is None:
        return "null"
    return "string"


def merge_types(existing_type, new_type):
    """Merge two type specifications, producing oneOf if different."""
    if existing_type is None:
        return new_type
    if existing_type == new_type:
        return existing_type

    existing_set = set(existing_type) if isinstance(existing_type, list) else {existing_type}
    new_set = {new_type}
    merged = sorted(existing_set | new_set)
    return merged if len(merged) > 1 else merged[0]


class SchemaExtractor:
    def __init__(self, assets_dir, output_dir):
        self.assets_dir = Path(assets_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def read_json_files(self, directory):
        """Recursively read all JSON files in a directory."""
        files = []
        dir_path = self.assets_dir / directory
        if not dir_path.exists():
            print(f"  Warning: {dir_path} does not exist, skipping")
            return files

        for root, _, filenames in os.walk(dir_path):
            for fname in filenames:
                if fname.endswith(".json"):
                    fpath = Path(root) / fname
                    try:
                        with open(fpath, "r", encoding="utf-8-sig") as f:
                            data = json.load(f)
                        files.append({"path": str(fpath), "name": fname, "data": data})
                    except (json.JSONDecodeError, UnicodeDecodeError) as e:
                        print(f"  Warning: Could not parse {fpath}: {e}")
        return files

    def analyze_fields(self, files):
        """Analyze all files to build a union schema of observed fields."""
        field_info = {}
        total_files = len(files)

        for file_entry in files:
            data = file_entry["data"]
            if not isinstance(data, dict):
                continue
            self._analyze_object(data, field_info, total_files, file_entry["name"])

        return field_info

    def _analyze_object(self, obj, field_info, total_files, source_name, prefix=""):
        """Recursively analyze an object's fields."""
        for key, value in obj.items():
            full_key = f"{prefix}{key}" if not prefix else f"{prefix}.{key}"

            if full_key not in field_info:
                field_info[full_key] = {
                    "type": None,
                    "count": 0,
                    "examples": [],
                    "min_val": None,
                    "max_val": None,
                }

            info = field_info[full_key]
            json_type = infer_json_type(value)
            info["type"] = merge_types(info["type"], json_type)
            info["count"] += 1

            # Track example values (keep up to 3 unique)
            if json_type in ("string", "integer", "number", "boolean"):
                if value not in info["examples"] and len(info["examples"]) < 3:
                    info["examples"].append(value)

            # Track numeric ranges
            if json_type in ("integer", "number"):
                if info["min_val"] is None or value < info["min_val"]:
                    info["min_val"] = value
                if info["max_val"] is None or value > info["max_val"]:
                    info["max_val"] = value

        return field_info

    def build_json_schema(self, category_name, description, field_info, total_files):
        """Build a JSON Schema 2020-12 from analyzed field info."""
        properties = {}
        required = []

        for field_key, info in sorted(field_info.items()):
            # Only include top-level fields
            if "." in field_key:
                continue

            prop = {}
            field_type = info["type"]

            if isinstance(field_type, list):
                prop["oneOf"] = [{"type": t} for t in field_type]
            else:
                prop["type"] = field_type or "string"

            if info["examples"]:
                example_vals = info["examples"][:3]
                if len(example_vals) <= 5 and all(isinstance(v, str) for v in example_vals):
                    prop["examples"] = example_vals

            if info["min_val"] is not None:
                prop["minimum"] = info["min_val"]
            if info["max_val"] is not None:
                prop["maximum"] = info["max_val"]

            properties[field_key] = prop

            # If field appears in >80% of files, consider it required
            if total_files > 0 and (info["count"] / total_files) > 0.8:
                required.append(field_key)

        schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": category_name,
            "description": description,
            "type": "object",
            "properties": properties,
        }

        if required:
            schema["required"] = sorted(required)

        return schema

    def extract_category(self, directory, schema_name, description):
        """Extract schema for a single asset category."""
        print(f"Processing: {directory}")
        files = self.read_json_files(directory)

        if not files:
            print(f"  No JSON files found in {directory}")
            return None

        print(f"  Found {len(files)} JSON files")
        field_info = self.analyze_fields(files)
        schema = self.build_json_schema(schema_name, description, field_info, len(files))

        output_path = self.output_dir / f"{schema_name}.schema.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(schema, f, indent=2, ensure_ascii=False)

        print(f"  Generated: {output_path} ({len(schema.get('properties', {}))} properties)")
        return schema

    def extract_all(self):
        """Extract schemas for all known asset categories."""
        categories = [
            ("Server/NPC/Roles", "npc-roles", "NPC role definitions — behavior, stats, AI, and appearance"),
            ("Server/NPC/Spawn", "npc-spawn", "NPC spawn rules — where, when, and how NPCs appear"),
            ("Server/NPC/Attitude", "npc-attitude", "NPC attitude definitions toward players and other entities"),
            ("Server/NPC/DecisionMaking", "npc-decision-making", "AI condition evaluators for NPC behavior"),
            ("Server/NPC/Balancing", "npc-balancing", "Combat AI behavior trees and action evaluators"),
            ("Server/NPC/Groups", "npc-groups", "NPC groupings for spawn and interaction rules"),
            ("Server/NPC/Flocks", "npc-flocks", "Flock behavior patterns"),
            ("Server/Item/Items", "item-definition", "Item definitions — stats, recipes, icons, interactions"),
            ("Server/Item/Block", "block-definition", "Block type definitions — textures, materials, light"),
            ("Server/Item/Recipes", "recipe", "Crafting recipes — inputs, outputs, bench requirements"),
            ("Server/Item/Category", "item-category", "Item category hierarchy for inventory UI"),
            ("Server/Item/Qualities", "quality", "Item quality/rarity tiers"),
            ("Server/Item/Interactions", "item-interaction", "Item and block interaction chains"),
            ("Server/Item/Groups", "item-groups", "Item groupings"),
            ("Server/Item/ResourceTypes", "resource-types", "Resource type definitions"),
            ("Server/Drops", "drop-table", "Loot table definitions with weighted containers"),
            ("Server/Projectiles", "projectile", "Simple projectile definitions"),
            ("Server/ProjectileConfigs", "projectile-config", "Advanced projectile configurations with physics and interactions"),
            ("Server/Entity/Damage", "damage-type", "Damage type hierarchy"),
            ("Server/Models", "model-definition", "Server-side model definitions — hitboxes, animations, camera"),
            ("Server/BarterShops", "barter-shop", "NPC shop inventories with fixed and pool trade slots"),
            ("Server/Farming", "farming", "Farm configurations — coops, growth modifiers"),
            ("Server/Environments", "environment", "Biome environment configurations"),
            ("Server/Weathers", "weather", "Weather visual definitions — sky, fog, clouds, sun, moon"),
            ("Server/GameplayConfigs", "gameplay-config", "Core game settings — death, durability, stamina, day/night"),
            ("Server/HytaleGenerator", "world-generation", "World generation rules and assignments"),
            ("Server/World", "world-mask", "World noise mask configurations"),
            ("Server/Camera", "camera-effect", "Camera effect definitions"),
            ("Server/BlockTypeList", "block-type-list", "Block type collections"),
            ("Server/PortalTypes", "portal-type", "Portal configurations linking to instances"),
            ("Server/Particles", "particle", "Particle effect definitions"),
            ("Server/TagPatterns", "tag-pattern", "Logical tag matching patterns"),
            ("Server/ResponseCurves", "response-curve", "Mathematical curves for AI and gameplay"),
            ("Server/Instances", "instance", "Instance data configurations"),
            ("Server/Objective", "objective", "Quest objective definitions"),
            ("Server/MacroCommands", "macro-command", "Command macro definitions"),
        ]

        results = {}
        for directory, schema_name, description in categories:
            schema = self.extract_category(directory, schema_name, description)
            if schema:
                results[schema_name] = schema

        print(f"\nDone! Generated {len(results)} schemas in {self.output_dir}")
        return results


def main():
    parser = argparse.ArgumentParser(description="Extract JSON schemas from Hytale assets")
    parser.add_argument(
        "--assets-dir",
        default="Assets",
        help="Path to the Assets directory (default: Assets)",
    )
    parser.add_argument(
        "--output-dir",
        default="schemas",
        help="Path to output schemas directory (default: schemas)",
    )
    args = parser.parse_args()

    extractor = SchemaExtractor(args.assets_dir, args.output_dir)
    extractor.extract_all()


if __name__ == "__main__":
    main()
