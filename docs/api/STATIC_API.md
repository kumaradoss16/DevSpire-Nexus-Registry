# DevSpire Nexus Registry — Static JSON API Guide

**API Version:** v1  
**Status:** Production Stable  
**License:** Open Data Commons Attribution (ODC-By v1.0)  
**Base URL:** `https://devspirehub.com/api/v1/` (or raw GitHub CDN / Pages)

---

## 1. Overview

The DevSpire Nexus Registry Static API provides versioned, machine-readable JSON files enabling applications, research pipelines, and AI agents to query the catalog without requiring server-side compute or Python environments.

All endpoints are hosted statically, delivering:
- **Infinite Scalability:** Zero backend server dependencies; 100% CDN cacheable.
- **Deterministic Hashing:** Bit-for-bit reproducible JSON with SHA-256 checksums.
- **Offline Capable:** Endpoints can be mirrored or downloaded for local disconnected operation.

---

## 2. Primary Endpoints Inventory

| Endpoint | HTTP Method | Size (Bytes) | Record Count | Description |
|:---|:---:|---:|---:|:---|
| [`/api/v1/tools.json`](file:///H:/DevSpire-Nexus-Registry/api/v1/tools.json) | `GET` | 604,764 | 403 | Canonical catalog of AI Tools and SaaS apps. |
| [`/api/v1/models.json`](file:///H:/DevSpire-Nexus-Registry/api/v1/models.json) | `GET` | 501,786 | 300 | Canonical catalog of AI Foundation and Edge Models. |
| [`/api/v1/developer-resources.json`](file:///H:/DevSpire-Nexus-Registry/api/v1/developer-resources.json) | `GET` | 692,303 | 300 | Canonical catalog of Frameworks, Libraries, Runtimes, and APIs. |
| [`/api/v1/categories.json`](file:///H:/DevSpire-Nexus-Registry/api/v1/categories.json) | `GET` | 3,058 | 38 | Taxonomy category counts across all three registries. |
| [`/api/v1/stats.json`](file:///H:/DevSpire-Nexus-Registry/api/v1/stats.json) | `GET` | 2,297 | Global | Aggregate metrics, verification percentages, and license distributions. |
| [`/api/v1/catalog.json`](file:///H:/DevSpire-Nexus-Registry/api/v1/catalog.json) | `GET` | 2,170 | Manifest | Cryptographic manifest with SHA-256 hashes and schema links. |

---

## 3. Schema Endpoints

Downstream validators can fetch the authoritative JSON Schemas directly:
- `/api/v1/schemas/tools.schema.json`
- `/api/v1/schemas/models.schema.json`
- `/api/v1/schemas/developer-resources.schema.json`
- `/api/v1/schemas/common.schema.json`

---

## 4. Response Structure Example (`tools.json`)

```json
{
  "_meta": {
    "api_version": "v1",
    "schema_version": "1.0.0",
    "count": 403,
    "documentation": "https://github.com/kumaradoss16/DevSpire-Nexus-Registry#readme"
  },
  "items": [
    {
      "id": "chatgpt",
      "canonical_id": "ai_tool:chatgpt",
      "name": "ChatGPT",
      "description": "Conversational AI assistant developed by OpenAI...",
      "category": "Assistants & Chatbots",
      "resource_type": "AI Tool",
      "official_url": "https://chatgpt.com/",
      "pricing": "Freemium",
      "pricing_class": "freemium",
      "license": null,
      "tags": ["chatbots", "assistant", "openai", "general-purpose"],
      "verified": "2026-11-03",
      "status": "verified",
      "evidence": [
        ["Verified link", "https://chatgpt.com/"],
        ["openai.com", "https://openai.com/chatgpt/pricing/"]
      ]
    }
  ]
}
```

---

## 5. Integrity Verification Workflow

Before consuming downloaded artifacts, verify file integrity against `catalog.json`:

```bash
# 1. Download catalog manifest and tools dataset
curl -s -O https://devspirehub.com/api/v1/catalog.json
curl -s -O https://devspirehub.com/api/v1/tools.json

# 2. Compute SHA-256 hash
sha256sum tools.json

# 3. Compare with catalog.json ["_meta"]["endpoints"]["tools.json"]["sha256"]
```
