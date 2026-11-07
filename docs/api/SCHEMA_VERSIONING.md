# DevSpire Nexus Registry — Schema Versioning Specification

**Specification Version:** 1.0.0  
**Effective Date:** 2026-11-07  
**Schema Metaschema:** JSON Schema Draft 2020-12  
**Scope:** Representation, inheritance, evolution, and semantic versioning of registry JSON schemas.

---

## 1. Schema Version Representation

All JSON Schemas declared in `schemas/` and published in `api/v1/schemas/` adhere to Semantic Versioning (SemVer 2.0.0):

- **Format:** `MAJOR.MINOR.PATCH` (e.g. `1.0.0`)
- **Metadata Declaration:** Stored in the `$id` URI and the schema's root description:
  - Canonical `$id`: `https://devspirehub.com/schemas/v1/common.schema.json`
  - Explicit release version tracked in dataset `_meta.schema_version`.

---

## 2. Semantic Rules for Schema Evolution

```
┌────────────────────────────────────────────────────────────────────────┐
│                        Schema Semantic Versioning                      │
├────────────────────┬───────────────────────────────────────────────────┤
│ MAJOR (X.0.0)      │ Breaking changes: removing properties, altering   │
│                    │ types, making optional fields required, narrowing  │
│                    │ allowed enum values, or regex constraints.        │
├────────────────────┼───────────────────────────────────────────────────┤
│ MINOR (1.X.0)      │ Backward-compatible additions: adding optional    │
│                    │ fields, introducing new non-breaking enum options, │
│                    │ or relaxing non-critical string length limits.    │
├────────────────────┼───────────────────────────────────────────────────┤
│ PATCH (1.0.X)      │ Backward-compatible corrections: clarifying       │
│                    │ descriptions, fixing regex typo bug, formatting.  │
└────────────────────┴───────────────────────────────────────────────────┘
```

---

## 3. Inheritance and Modular Schema Architecture

The registry avoids schema duplication through JSON Schema Draft 2020-12 `$defs` and `allOf` references:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://devspirehub.com/schemas/v1/ai-tool.schema.json",
  "title": "DevSpire Nexus AI Tool Record",
  "allOf": [
    { "$ref": "common.schema.json" },
    {
      "type": "object",
      "properties": {
        "resource_type": { "const": "AI Tool" },
        "pricing_class": {
          "type": "string",
          "enum": ["free", "freemium", "paid", "open_source", "usage_based", "commercial"]
        }
      }
    }
  ]
}
```

---

## 4. Migration & Deprecation Process

When a breaking schema change is required (e.g. moving from Schema v1 to v2):
1. **RFC & Deprecation Notice:** A formal proposal is published in GitHub discussions at least 60 days in advance.
2. **Dual-Publishing Window:** Both `v1` and `v2` endpoints remain active simultaneously during the deprecation period.
3. **Automated Migration Script:** A migration utility (`scripts/migrate_v1_to_v2.py`) is provided in the repository to transform legacy consumer data.
