#!/usr/bin/env python3
"""
DevSpire Nexus Registry CLI
Command-line interface for validating, querying, inspecting, and retrieving
developer quick starts and auditing data quality from the DevSpire Nexus Registry.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Optional

from .validator import RegistryValidator
from .client import RegistryClient
from . import __version__
from .quality import (
    StructuralValidator,
    UniquenessChecker,
    URLAuditor,
    MetadataAuditor,
    EvidenceAuditor,
    VerificationEngine,
    FreshnessChecker,
    QualityScorer,
    QualityReportGenerator,
)


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


# ---------------------------------------------------------
# Phase 1: Quality CLI Commands
# ---------------------------------------------------------

def _get_quality_generator(args) -> QualityReportGenerator:
    return QualityReportGenerator(repo_root=args.root)


def cmd_quality_check(args) -> int:
    gen = _get_quality_generator(args)
    audit = gen.run_full_audit(check_network=args.network)

    if args.json:
        print(json.dumps(audit, indent=2))
        return 0 if audit["catalog_summary"]["is_release_ready"] else 1

    summary = audit["catalog_summary"]
    print("=" * 60)
    print("       DevSpire Nexus Registry Data Quality Scorecard      ")
    print("=" * 60)
    print(f"Total Records Audited:      {summary['total_records']:,}")
    print(f"Overall Quality Score:      {summary['overall_score']:.1f} / 100.0 ({summary['overall_grade']})")
    print(f"Structural Gate:            {'PASSED' if summary['structural_gate_passed'] else 'FAILED'}")
    print(f"Release Readiness:          {'READY' if summary['is_release_ready'] else 'BLOCKED'}")
    print("-" * 60)
    print("Dimension Scores:")
    for dim_name, dim in summary["dimensions"].items():
        print(f"  • {dim_name:<26} {dim['raw_score']:>5.1f}%  (Weight: {dim['weight']*100:.0f}%, Score: {dim['weighted_score']:>4.2f})")
    print("-" * 60)
    print("Registries:")
    for reg_name, reg_data in audit["registries"].items():
        sc = reg_data["score"]
        st = reg_data["structural"]
        print(f"  • {reg_name:<22} Score: {sc['overall_score']:>5.1f} ({sc['grade']:<9}) Valid: {st['valid_records']}/{st['total_records']}")
    print("=" * 60)

    return 0 if summary["is_release_ready"] else 1


def cmd_quality_validate(args) -> int:
    gen = _get_quality_generator(args)
    datasets = gen.load_datasets()

    target_registries = [args.registry] if args.registry else list(datasets.keys())
    all_valid = True

    print("=" * 60)
    print("       DevSpire Nexus Registry Structural Validation       ")
    print("=" * 60)

    for reg in target_registries:
        records = datasets.get(reg, [])
        res = gen.structural_validator.validate_registry(records, reg)
        status_label = "PASS" if res.is_valid else "FAIL"
        print(f"Registry: {reg:<22} Status: [{status_label}]  Valid: {res.valid_records}/{res.total_records}  Errors: {len(res.errors)}")
        if res.errors:
            all_valid = False
            for err in res.errors[:5]:
                print(f"   [!] Record '{err.record_id}' {err.field_path}: {err.message}")
            if len(res.errors) > 5:
                print(f"   ... and {len(res.errors) - 5} more error(s).")

    print("=" * 60)
    return 0 if all_valid else 1


def cmd_quality_duplicates(args) -> int:
    gen = _get_quality_generator(args)
    datasets = gen.load_datasets()
    rep = gen.uniqueness_checker.audit(datasets)

    if args.json:
        print(json.dumps(rep.to_dict(), indent=2))
        return 0 if not rep.has_identity_conflicts else 1

    print("=" * 60)
    print("       DevSpire Nexus Registry Identity & URL Audit       ")
    print("=" * 60)
    print(f"Total Records Audited:         {rep.total_records:,}")
    print(f"Duplicate Identifiers:         {len(rep.duplicate_ids)}")
    print(f"Cross-Registry Collisions:     {len(rep.cross_registry_id_collisions)}")
    print(f"Shared Destination URLs:       {len(rep.url_findings)}")
    print("-" * 60)

    if rep.duplicate_ids:
        print("Duplicate Identifiers:")
        for dup in rep.duplicate_ids:
            print(f"  [!] [{dup['registry']}] ID: {dup['id']} ('{dup['name']}')")

    if rep.url_findings:
        print("\nShared URL Findings:")
        for f in rep.url_findings:
            print(f"\n• URL: {f.normalized_url}")
            print(f"  Classification: {f.classification.value}")
            print(f"  Reason:         {f.reason}")
            print(f"  Recommendation: {f.recommended_action}")
            for r in f.records:
                print(f"    - [{r['registry']}] {r['id']} ({r['name']})")

    print("=" * 60)
    return 0 if not rep.has_identity_conflicts else 1


def cmd_quality_evidence(args) -> int:
    gen = _get_quality_generator(args)
    datasets = gen.load_datasets()

    target_registries = [args.registry] if args.registry else list(datasets.keys())

    print("=" * 60)
    print("       DevSpire Nexus Registry Evidence Source Audit       ")
    print("=" * 60)

    for reg in target_registries:
        records = datasets.get(reg, [])
        rep = gen.evidence_auditor.audit_registry(records, reg)
        print(f"\nRegistry: {reg} (Records: {rep.total_records})")
        print(f"  Coverage: {rep.coverage_percentage:.1f}% ({rep.records_with_evidence}/{rep.total_records})")
        print(f"  With Primary Evidence: {rep.records_with_primary_evidence}/{rep.total_records}")
        print("  Archetype Distribution:")
        for arch, count in sorted(rep.archetype_distribution.items(), key=lambda x: -x[1]):
            print(f"    • {arch:<24} {count:>4} citations")

    print("=" * 60)
    return 0


def cmd_quality_metadata(args) -> int:
    gen = _get_quality_generator(args)
    datasets = gen.load_datasets()

    target_registries = [args.registry] if args.registry else list(datasets.keys())

    print("=" * 60)
    print("       DevSpire Nexus Registry Metadata Completeness      ")
    print("=" * 60)

    for reg in target_registries:
        records = datasets.get(reg, [])
        rep = gen.metadata_auditor.audit_registry(records, reg)
        print(f"\nRegistry: {reg} (Records: {rep.total_records})")
        print(f"  Completeness Index: {rep.completeness_percentage:.1f}%")
        print(f"  Missing Critical:   {rep.missing_critical}")
        print(f"  Missing High:       {rep.missing_high}")
        print(f"  Missing Medium:     {rep.missing_medium}")
        print(f"  Missing Low:        {rep.missing_low}")

    print("=" * 60)
    return 0


def cmd_quality_freshness(args) -> int:
    gen = _get_quality_generator(args)
    datasets = gen.load_datasets()

    target_registries = [args.registry] if args.registry else list(datasets.keys())

    print("=" * 60)
    print("       DevSpire Nexus Registry Verification Freshness     ")
    print("=" * 60)

    for reg in target_registries:
        records = datasets.get(reg, [])
        rep = gen.freshness_checker.audit_registry(records, reg)
        print(f"\nRegistry: {reg} (Records: {rep.total_records})")
        print(f"  Freshness Index:   {rep.freshness_percentage:.1f}%")
        print(f"  Fresh (<= 90d):    {rep.fresh_count}")
        print(f"  Current (91-180d): {rep.current_count}")
        print(f"  Aging (181-365d):  {rep.aging_count}")
        print(f"  Stale (> 365d):    {rep.stale_count}")

    print("=" * 60)
    return 0


def cmd_quality_score(args) -> int:
    gen = _get_quality_generator(args)
    audit = gen.run_full_audit(check_network=False)
    summary = audit["catalog_summary"]

    if args.json:
        print(json.dumps(audit["global_score"], indent=2))
        return 0

    print("=" * 60)
    print(f"Overall Catalog Score: {summary['overall_score']:.1f} / 100.0 [{summary['overall_grade']}]")
    print("=" * 60)
    for dim_name, d in summary["dimensions"].items():
        print(f"  [{d['name']:<24}] Score: {d['raw_score']:>5.1f}%  Weight: {d['weight']*100:>2.0f}% -> {d['weighted_score']:>4.2f} pts")
    print("-" * 60)
    for reg, data in audit["registries"].items():
        sc = data["score"]
        print(f"  {reg:<26} {sc['overall_score']:>5.1f} / 100.0  [{sc['grade']}]")
    print("=" * 60)
    return 0


def cmd_quality_report(args) -> int:
    gen = _get_quality_generator(args)
    out_dir = gen.write_reports(check_network=args.network)
    print(f"Data quality reports successfully generated at:\n  {out_dir}")
    return 0


def cmd_quality_urls(args) -> int:
    gen = _get_quality_generator(args)
    datasets = gen.load_datasets()

    print(f"Auditing URLs (network checks = {'ENABLED' if args.network else 'DISABLED'})...")
    total_urls = 0
    valid_syntax = 0

    for reg, records in datasets.items():
        for r in records:
            res = gen.url_auditor.audit_record_urls(r, check_network=args.network, timeout=args.timeout)
            for ua in res:
                total_urls += 1
                if ua.is_syntactically_valid:
                    valid_syntax += 1

    print(f"Total URLs Checked:     {total_urls:,}")
    print(f"Syntactically Valid:   {valid_syntax:,} ({valid_syntax/total_urls*100:.1f}%)")
    return 0


# ---------------------------------------------------------
# Main Argument Parsing & Dispatch
# ---------------------------------------------------------

def main(args: Optional[List[str]] = None, root_dir: Optional[Path] = None, repo_root: Optional[Path] = None) -> int:
    if root_dir is None:
        root_dir = repo_root

    parser = argparse.ArgumentParser(
        prog="nexus-registry",
        description="DevSpire Nexus Registry CLI — Discover, validate, inspect, and audit canonical AI resources."
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

    # quality subcommand group
    p_qual = subparsers.add_parser("quality", help="Data quality, verification, and audit commands.")
    q_subparsers = p_qual.add_subparsers(dest="quality_command", help="Quality subcommands")

    # quality check
    pq_check = q_subparsers.add_parser("check", help="Run full multi-dimensional data quality audit.")
    pq_check.add_argument("--json", action="store_true", help="Output machine-readable JSON.")
    pq_check.add_argument("--network", action="store_true", help="Include bounded external network checks.")
    pq_check.set_defaults(func=cmd_quality_check)

    # quality validate
    pq_val = q_subparsers.add_parser("validate", help="Validate schemas with JSON Pointer error formatting.")
    pq_val.add_argument("--registry", choices=["ai-tools", "ai-models", "developer-resources"], help="Filter registry.")
    pq_val.set_defaults(func=cmd_quality_validate)

    # quality duplicates
    pq_dup = q_subparsers.add_parser("duplicates", help="Detect duplicate identifiers, slugs, and shared URLs.")
    pq_dup.add_argument("--json", action="store_true", help="Output JSON findings.")
    pq_dup.set_defaults(func=cmd_quality_duplicates)

    # quality evidence
    pq_ev = q_subparsers.add_parser("evidence", help="Audit evidence sources and archetype classifications.")
    pq_ev.add_argument("--registry", choices=["ai-tools", "ai-models", "developer-resources"], help="Filter registry.")
    pq_ev.set_defaults(func=cmd_quality_evidence)

    # quality metadata
    pq_meta = q_subparsers.add_parser("metadata", help="Audit metadata completeness and severity tiers.")
    pq_meta.add_argument("--registry", choices=["ai-tools", "ai-models", "developer-resources"], help="Filter registry.")
    pq_meta.set_defaults(func=cmd_quality_metadata)

    # quality freshness
    pq_fresh = q_subparsers.add_parser("freshness", help="Check verification date age against review windows.")
    pq_fresh.add_argument("--registry", choices=["ai-tools", "ai-models", "developer-resources"], help="Filter registry.")
    pq_fresh.set_defaults(func=cmd_quality_freshness)

    # quality score
    pq_score = q_subparsers.add_parser("score", help="Calculate and display 7-dimension quality score.")
    pq_score.add_argument("--json", action="store_true", help="Output JSON score report.")
    pq_score.set_defaults(func=cmd_quality_score)

    # quality report
    pq_rep = q_subparsers.add_parser("report", help="Generate quality reports in reports/quality/latest/.")
    pq_rep.add_argument("--network", action="store_true", help="Include bounded network checks.")
    pq_rep.set_defaults(func=cmd_quality_report)

    # quality urls
    pq_urls = q_subparsers.add_parser("urls", help="Audit URL syntax and optional network availability.")
    pq_urls.add_argument("--network", action="store_true", help="Execute live network probes.")
    pq_urls.add_argument("--timeout", type=int, default=10, help="Probe timeout in seconds.")
    pq_urls.set_defaults(func=cmd_quality_urls)

    parsed = parser.parse_args(args)
    if parsed.root is None and root_dir is not None:
        parsed.root = root_dir

    if hasattr(parsed, "func"):
        return parsed.func(parsed)
    else:
        if parsed.command == "quality":
            p_qual.print_help()
        else:
            parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
