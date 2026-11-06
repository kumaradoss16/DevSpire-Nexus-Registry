#!/usr/bin/env python3
"""
Generate deterministic, static API endpoints for DevSpire Nexus Registry.

Produces in api/v1/:
  - tools.json (deterministic)
  - models.json (deterministic)
  - developer-resources.json (deterministic)
  - categories.json (deterministic)
  - stats.json (deterministic)
  - catalog.json (with build metadata, record counts, and SHA256 checksums)
"""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

REGISTRY_ROOT = Path(__file__).resolve().parent.parent
DATASETS_DIR = REGISTRY_ROOT / "datasets"
API_V1_DIR = REGISTRY_ROOT / "api" / "v1"


def compute_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json_deterministic(path: Path, obj: dict | list) -> tuple[int, str]:
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    data = serialized.encode("utf-8")
    path.write_bytes(data)
    return len(data), compute_sha256(data)


def main():
    print("=== Generating Static API v1 Artifacts ===")

    # 1. Load canonical datasets
    tools_doc = json.loads((DATASETS_DIR / "ai-tools.json").read_text(encoding="utf-8"))
    models_doc = json.loads((DATASETS_DIR / "ai-models.json").read_text(encoding="utf-8"))
    dev_doc = json.loads((DATASETS_DIR / "developer-resources.json").read_text(encoding="utf-8"))

    tools = tools_doc.get("records") or tools_doc.get("items") or (tools_doc if isinstance(tools_doc, list) else [])
    models = models_doc.get("records") or models_doc.get("items") or (models_doc if isinstance(models_doc, list) else [])
    dev_resources = dev_doc.get("records") or dev_doc.get("items") or (dev_doc if isinstance(dev_doc, list) else [])

    manifest_artifacts = {}

    # 2. Write individual registry endpoints (deterministic metadata)
    for name, items in [
        ("tools.json", tools),
        ("models.json", models),
        ("developer-resources.json", dev_resources),
    ]:
        payload = {
            "_meta": {
                "schema_version": "1.0.0",
                "api_version": "v1",
                "count": len(items),
                "documentation": "https://github.com/kumaradoss16/DevSpire-Nexus-Registry#readme",
            },
            "items": items,
        }
        dest = API_V1_DIR / name
        size, sha = write_json_deterministic(dest, payload)
        manifest_artifacts[name] = {
            "path": f"api/v1/{name}",
            "records": len(items),
            "size_bytes": size,
            "sha256": sha,
        }
        print(f"  [OK] {name}: {len(items)} records, {size} bytes, sha256={sha[:12]}...")

    # 3. Write categories.json (deterministic metadata)
    categories_by_registry = {}
    for reg_name, items in [
        ("ai-tools", tools),
        ("ai-models", models),
        ("developer-resources", dev_resources),
    ]:
        cat_counts = {}
        for it in items:
            cat = it.get("category", "Uncategorized")
            cat_counts[cat] = cat_counts.get(cat, 0) + 1
        categories_by_registry[reg_name] = sorted(
            [{"name": k, "count": v} for k, v in cat_counts.items()],
            key=lambda x: (-x["count"], x["name"]),
        )

    categories_payload = {
        "_meta": {
            "schema_version": "1.0.0",
            "api_version": "v1",
        },
        "registries": categories_by_registry,
    }
    cat_size, cat_sha = write_json_deterministic(API_V1_DIR / "categories.json", categories_payload)
    manifest_artifacts["categories.json"] = {
        "path": "api/v1/categories.json",
        "size_bytes": cat_size,
        "sha256": cat_sha,
    }
    print(f"  [OK] categories.json: {cat_size} bytes, sha256={cat_sha[:12]}...")

    # 4. Write stats.json (deterministic metadata)
    all_items = tools + models + dev_resources
    verified_count = sum(1 for x in all_items if x.get("verified"))
    qs_count = sum(1 for x in dev_resources if (x.get("developer_quick_start") or {}).get("available"))
    pricing_dist = {}
    license_dist = {}
    for x in all_items:
        p = str(x.get("pricing") or "Unknown")
        pricing_dist[p] = pricing_dist.get(p, 0) + 1
        lic = str(x.get("license") or "Unknown")
        license_dist[lic] = license_dist.get(lic, 0) + 1

    stats_payload = {
        "_meta": {
            "schema_version": "1.0.0",
            "api_version": "v1",
        },
        "totals": {
            "all_resources": len(all_items),
            "ai_tools": len(tools),
            "ai_models": len(models),
            "developer_resources": len(dev_resources),
            "verified_resources": verified_count,
            "verified_percentage": round((verified_count / len(all_items)) * 100, 2),
            "developer_quick_starts_verified": qs_count,
        },
        "distribution": {
            "license": license_dist,
            "pricing": pricing_dist,
        },
    }
    stats_size, stats_sha = write_json_deterministic(API_V1_DIR / "stats.json", stats_payload)
    manifest_artifacts["stats.json"] = {
        "path": "api/v1/stats.json",
        "size_bytes": stats_size,
        "sha256": stats_sha,
    }
    print(f"  [OK] stats.json: {stats_size} bytes, sha256={stats_sha[:12]}...")

    # 5. Write catalog.json manifest (contains volatile build time and artifact checksums)
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    catalog_payload = {
        "_meta": {
            "name": "DevSpire Nexus Registry Catalog",
            "version": "1.0.0",
            "api_version": "v1",
            "brand": "DevSpireHub.com",
            "generated_at": now_iso,
            "total_resources": len(all_items),
            "endpoints": manifest_artifacts,
        }
    }
    cat_manifest_size, cat_manifest_sha = write_json_deterministic(API_V1_DIR / "catalog.json", catalog_payload)
    print(f"  [OK] catalog.json: {cat_manifest_size} bytes, sha256={cat_manifest_sha[:12]}...")
    print("=== API Generation Complete ===")


if __name__ == "__main__":
    main()
