# DevSpire Nexus Website Integration Guide

This document defines the integration interface and data contract between the canonical **DevSpire Nexus Registry** and the user-facing **DevSpire Nexus Website** ([`DevSpire-Nexus`](https://github.com/kumaradoss16/Devspire-Nexus)).

---

## 1. System Boundary Principle

The **Registry** owns canonical data, schemas, and verification.  
The **Website** owns user interface rendering, search UI, responsive cards, and client-side personal collections (`localStorage`).

```
┌─────────────────────────────────────────────────────────────┐
│                 DevSpire-Nexus-Registry                     │
│               (Authoritative Data Engine)                   │
└──────────────────────────────┬──────────────────────────────┘
                               │
            Static API Endpoints (api/v1/*.json)
                               v
┌─────────────────────────────────────────────────────────────┐
│                     DevSpire-Nexus                          │
│               (Consumer & Web Frontend)                     │
│                                                             │
│   • Consumes static API endpoints or bundled fallback       │
│   • Renders reactive card grids & modals                    │
│   • Provides interactive Quick Start terminal & tabs        │
│   • Manages user personal bookmarks in browser storage      │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Consuming Static API Endpoints

Web applications and downstream services can consume the immutable static JSON API artifacts:

| Endpoint | Content | Size | Records |
|---|---|---|---|
| `api/v1/tools.json` | Canonical AI Applications & Software | ~604 KB | 403 |
| `api/v1/models.json` | Foundation Models & Parameters | ~501 KB | 300 |
| `api/v1/developer-resources.json` | Engineering SDKs & Quick Starts | ~692 KB | 300 |
| `api/v1/categories.json` | Distinct taxonomy categories | ~3 KB | 38 |
| `api/v1/stats.json` | Registry-wide metrics & distributions | ~2 KB | — |
| `api/v1/catalog.json` | Release manifest with SHA-256 hashes | ~1 KB | — |

### Example JavaScript Ingestion:
```javascript
async function loadDeveloperResources() {
  const url = 'https://raw.githubusercontent.com/kumaradoss16/DevSpire-Nexus-Registry/main/api/v1/developer-resources.json';
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Failed to load registry: ${response.status}`);
  }
  const payload = await response.json();
  console.log(`Loaded ${payload.items.length} canonical developer resources.`);
  return payload.items;
}
```

---

## 3. Data Refresh & Synchronization Workflow

When metadata in the Registry is updated:
1. Re-run `python scripts/generate_api.py` to produce deterministic endpoints.
2. In the `DevSpire-Nexus` repository:
   - Synchronize the new JSON files into `api/`.
   - Update `data/developer-resources.js`, `data/ai-tools.js`, or `data/ai-models.js` if deploying for offline `file:///` local browsing environments.
3. Execute `.qa/qa-dev.js` and `.qa/qa-quickstart.js` to ensure 0 frontend regressions.
