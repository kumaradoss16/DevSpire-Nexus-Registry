#!/usr/bin/env python3
"""
DevSpire Nexus Registry — Canonical Data Migration Script
Extracts, transforms, and validates 1,003 resource records from the
DevSpire Nexus source datasets into canonical, version-controlled registry datasets.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

SOURCE_ROOT = Path("H:/Devspirehub AI")
TARGET_ROOT = Path(__file__).resolve().parent.parent

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def clean_record(rec, registry_type):
    # Ensure stable ordering of dictionary keys for deterministic diffs
    ordered = {}
    
    # Common keys
    common_keys = [
        "id", "name", "description", "category", "source_category",
        "resource_type", "official_url", "pricing", "pricing_class",
        "license", "license_short", "open_source", "self_hostable",
        "signup_required", "tags", "icon", "verified", "status",
        "notes", "evidence", "domain", "provider", "local_execution", "canonical_id"
    ]
    
    for k in common_keys:
        if k in rec:
            ordered[k] = rec[k]
            
    # Registry-specific additions
    if registry_type == "ai-tools":
        tool_keys = ["org", "platform", "hosting", "initials"]
        for k in tool_keys:
            if k in rec:
                ordered[k] = rec[k]
        if not ordered.get("org") and ordered.get("provider"):
            ordered["org"] = ordered["provider"]
                
    elif registry_type == "ai-models":
        model_keys = [
            "publisher", "family", "weights", "open_weights", "license_group",
            "params", "context", "context_k", "moe", "modalities"
        ]
        for k in model_keys:
            if k in rec:
                ordered[k] = rec[k]

        if not ordered.get("weights"):
            if ordered.get("open_weights") is True or ordered.get("open_source") is True:
                ordered["weights"] = "open"
            else:
                ordered["weights"] = "closed"

        if not ordered.get("modalities"):
            cat = rec.get("category", "")
            if "Vision" in cat or "Multimodal" in cat:
                ordered["modalities"] = ["Vision", "Text"]
            elif "Image" in cat:
                ordered["modalities"] = ["Image"]
            elif "Audio" in cat or "Speech" in cat:
                ordered["modalities"] = ["Audio"]
            elif "Video" in cat:
                ordered["modalities"] = ["Video"]
            elif "Embedding" in cat:
                ordered["modalities"] = ["Embeddings"]
            elif "3D" in cat:
                ordered["modalities"] = ["3D"]
            else:
                ordered["modalities"] = ["Text"]
                
    elif registry_type == "developer-resources":
        dev_keys = [
            "resource_subtype", "documentation_url", "repository_url",
            "api_url", "hosting", "programming_languages", "integrations",
            "developer_quick_start"
        ]
        for k in dev_keys:
            if k in rec:
                ordered[k] = rec[k]

    # Include any remaining keys deterministically
    for k in sorted(rec.keys()):
        if k not in ordered:
            ordered[k] = rec[k]
            
    return ordered

def run_migration():
    print("=== Starting DevSpire Nexus Registry Data Migration ===")
    
    # 1. AI Tools
    tools_source_path = SOURCE_ROOT / "api/tools.json"
    print(f"Reading AI Tools from: {tools_source_path}")
    tools_data = load_json(tools_source_path)
    raw_tools = tools_data.get("records", tools_data) if isinstance(tools_data, dict) else tools_data
    migrated_tools = [clean_record(r, "ai-tools") for r in raw_tools]
    
    # 2. AI Models
    models_source_path = SOURCE_ROOT / "api/models.json"
    print(f"Reading AI Models from: {models_source_path}")
    models_data = load_json(models_source_path)
    raw_models = models_data.get("records", models_data) if isinstance(models_data, dict) else models_data
    migrated_models = [clean_record(r, "ai-models") for r in raw_models]
    
    # 3. Developer Resources
    dev_source_path = SOURCE_ROOT / "api/developer-resources.json"
    print(f"Reading Developer Resources from: {dev_source_path}")
    dev_data = load_json(dev_source_path)
    raw_dev = dev_data.get("records", dev_data) if isinstance(dev_data, dict) else dev_data
    migrated_dev = [clean_record(r, "developer-resources") for r in raw_dev]
    
    now_iso = datetime.now().strftime("%Y-%m-%d")
    
    def write_canonical(filename, records, reg_key, label):
        cats = sorted(list(set(r.get("category") for r in records if r.get("category"))))
        payload = {
            "_meta": {
                "registry": reg_key,
                "label": label,
                "schema_version": "1.0.0",
                "dataset_version": "1.0.0",
                "last_migrated": now_iso,
                "total_records": len(records),
                "category_count": len(cats),
                "categories": cats
            },
            "records": records
        }
        target_path = TARGET_ROOT / "datasets" / filename
        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
        print(f"-> Wrote {len(records)} records to {target_path}")
        return payload["_meta"]
        
    tools_meta = write_canonical("ai-tools.json", migrated_tools, "ai-tools", "AI Tools")
    models_meta = write_canonical("ai-models.json", migrated_models, "ai-models", "AI Models")
    dev_meta = write_canonical("developer-resources.json", migrated_dev, "developer-resources", "Developer Resources")
    
    total = len(migrated_tools) + len(migrated_models) + len(migrated_dev)
    print(f"\nMigration Complete! Total canonical records: {total}")
    assert total == 1003, f"Expected 1,003 records, got {total}"
    assert len(set(r["id"] for r in migrated_tools)) == 403, "Duplicate ID in tools"
    assert len(set(r["id"] for r in migrated_models)) == 300, "Duplicate ID in models"
    assert len(set(r["id"] for r in migrated_dev)) == 300, "Duplicate ID in dev resources"
    print("All ID uniqueness assertions passed (100% unique IDs across all registries).")

if __name__ == "__main__":
    run_migration()
