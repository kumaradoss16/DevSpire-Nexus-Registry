#!/usr/bin/env python3
"""
DevSpire Nexus Registry CLI
Command-line interface for validating, querying, inspecting, and retrieving
developer quick starts from the DevSpire Nexus Registry.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Optional

from .validator import RegistryValidator
from .client import RegistryClient
from . import __version__


def cmd_validate(args) -> int:
    validator = RegistryValidator(root_dir=args.root)
    report = validator.validate_all(registry_filter=args.registry)

    if args.json:
        print(json.dumps(report.to_dict(), indent=2))
    else:
        print(report.render_text())

    return 0 if report.is_valid else 1


def cmd_search(args) -> int:
    client = RegistryClient(root_dir=args.root)
    results = client.search(
        query=args.query,
        registry=args.registry,
        category=args.category,
        limit=args.limit
    )

    if not results:
        print(f"No resources found matching '{args.query}'.")
        return 0

    print(f"\nFound {len(results)} resource(s) matching '{args.query}':\n")
    for r in results:
        reg = r.get("canonical_id", "").split(":")[0] if r.get("canonical_id") else "resource"
        print(f"• [{reg}] {r.get('name')} ({r.get('id')})")
        print(f"  Category: {r.get('category')} | License: {r.get('license', 'N/A')}")
        print(f"  URL:      {r.get('official_url')}")
        print(f"  Summary:  {r.get('description', '')[:120]}...\n")
    return 0


def cmd_info(args) -> int:
    client = RegistryClient(root_dir=args.root)
    res = client.get(args.id)

    if not res:
        print(f"Error: Resource '{args.id}' not found in registry.", file=sys.stderr)
        return 1

    print("=" * 60)
    print(f"{res.get('name')} [{res.get('category')}]")
    print("=" * 60)
    print(f"ID:           {res.get('id')}")
    print(f"Canonical ID: {res.get('canonical_id')}")
    print(f"Type:         {res.get('resource_type')}")
    print(f"URL:          {res.get('official_url')}")
    print(f"Pricing:      {res.get('pricing')} ({res.get('license', 'N/A')})")
    print(f"Status:       {res.get('status')} (Verified: {res.get('verified')})")
    print(f"Description:\n  {res.get('description')}\n")

    if res.get("tags"):
        print(f"Tags:         {', '.join(res.get('tags', []))}")

    if res.get("evidence"):
        print("\nPrimary Evidence Sources:")
        for label, url in res.get("evidence", []):
            print(f"  • {label}: {url}")

    if res.get("developer_quick_start") and res["developer_quick_start"].get("available"):
        qs = res["developer_quick_start"]
        print(f"\nDeveloper Quick Start Available! (Package: {qs.get('package_name', 'N/A')})")
        print(f"Run 'nexus-registry quickstart {res.get('id')}' to view commands.")

    return 0


def cmd_quickstart(args) -> int:
    client = RegistryClient(root_dir=args.root)
    qs = client.get_quickstart(args.id)

    if not qs or not qs.get("available"):
        print(f"Resource '{args.id}' does not have a verified Developer Quick Start guide.", file=sys.stderr)
        print("Submit a verified guide via GitHub pull request.", file=sys.stderr)
        return 1

    res = client.get(args.id)
    res_name = res.get("name", args.id) if res else args.id

    print("=" * 60)
    print(f"Developer Quick Start: {res_name} (Package: {qs.get('package_name')})")
    print("=" * 60)

    if qs.get("installation"):
        print("\nInstallation:")
        for inst in qs["installation"]:
            print(f"  [{inst.get('pm')}]: {inst.get('command')}")

    doc = qs.get("documentation")
    if doc:
        print(f"\nOfficial Documentation:\n  {doc.get('url')} ({doc.get('title')})")

    gh = qs.get("github")
    if gh:
        print(f"GitHub Repository:\n  {gh.get('url')}")

    if qs.get("supported_languages"):
        langs = [l.get("language") for l in qs["supported_languages"]]
        print(f"Supported Languages:\n  {', '.join(langs)}")

    if qs.get("examples"):
        ex = qs["examples"][0]
        print(f"\nBasic Usage Example ({ex.get('label', 'Example')}):")
        print("-" * 60)
        print(ex.get("code"))
        print("-" * 60)
        if ex.get("expected_output"):
            print("Expected Output:")
            print(ex.get("expected_output"))

    return 0


def cmd_categories(args) -> int:
    client = RegistryClient(root_dir=args.root)
    cats = client.list_categories(registry=args.registry)

    reg_label = f"[{args.registry}]" if args.registry else "[All Registries]"
    print(f"\nTaxonomy Categories {reg_label} ({len(cats)} total):\n")
    for c in cats:
        print(f"  • {c}")
    return 0


def cmd_stats(args) -> int:
    client = RegistryClient(root_dir=args.root)
    st = client.stats()

    print("=" * 50)
    print("       DevSpire Nexus Registry Metrics            ")
    print("=" * 50)
    print(f"Total Canonical Resources: {st['total_resources']:,}")
    print(f"AI Tools:                 {st['tools_count']:,}")
    print(f"AI Models:                {st['models_count']:,}")
    print(f"Developer Resources:      {st['developer_resources_count']:,}")
    print(f"Verified Quick Starts:    {st['quickstarts_available']}")
    print("-" * 50)
    for reg, data in st["registries"].items():
        print(f"Registry: {reg:<22} Count: {data['count']:<5} Categories: {data['categories']}")
    print("=" * 50)
    return 0


def main(args: Optional[List[str]] = None, root_dir: Optional[Path] = None, repo_root: Optional[Path] = None) -> int:
    if root_dir is None:
        root_dir = repo_root

    parser = argparse.ArgumentParser(
        prog="nexus-registry",
        description="DevSpire Nexus Registry CLI — Discover, validate, and inspect canonical AI tools, models, and developer resources."
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--root", type=Path, default=root_dir, help="Root path to registry repository containing datasets/.")

    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # validate
    p_val = subparsers.add_parser("validate", help="Validate datasets against schemas and integrity constraints.")
    p_val.add_argument("--registry", choices=["ai-tools", "ai-models", "developer-resources"], help="Validate specific registry.")
    p_val.add_argument("--json", action="store_true", help="Output machine-readable JSON report.")
    p_val.set_defaults(func=cmd_validate)

    # search
    p_search = subparsers.add_parser("search", help="Search resources by query keyword.")
    p_search.add_argument("query", help="Search term (name, category, description, tags).")
    p_search.add_argument("--registry", choices=["tools", "models", "developer"], help="Filter by registry.")
    p_search.add_argument("--category", help="Filter by exact category.")
    p_search.add_argument("--limit", type=int, default=15, help="Maximum results to return.")
    p_search.set_defaults(func=cmd_search)

    # info
    p_info = subparsers.add_parser("info", help="Inspect detailed metadata for a resource ID.")
    p_info.add_argument("id", help="Resource slug ID (e.g. langchain, ollama, gpt-4o).")
    p_info.set_defaults(func=cmd_info)

    # quickstart
    p_qs = subparsers.add_parser("quickstart", help="Print verified Quick Start installation and usage example.")
    p_qs.add_argument("id", help="Developer resource ID (e.g. langchain, qdrant, vllm).")
    p_qs.set_defaults(func=cmd_quickstart)

    # categories
    p_cats = subparsers.add_parser("categories", help="List distinct taxonomy categories.")
    p_cats.add_argument("--registry", choices=["tools", "models", "developer"], help="Filter by registry.")
    p_cats.set_defaults(func=cmd_categories)

    # stats
    p_stats = subparsers.add_parser("stats", help="Display dataset record counts and verification metrics.")
    p_stats.set_defaults(func=cmd_stats)

    # version
    p_ver = subparsers.add_parser("version", help="Print version number.")
    p_ver.set_defaults(func=lambda _: (print(f"nexus-registry {__version__}") or 0))

    parsed = parser.parse_args(args)
    if parsed.root is None and root_dir is not None:
        parsed.root = root_dir

    if hasattr(parsed, "func"):
        return parsed.func(parsed)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
