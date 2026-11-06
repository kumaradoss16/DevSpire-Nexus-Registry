# DevSpire Nexus Registry

[![CI Validation](https://github.com/kumaradoss16/DevSpire-Nexus-Registry/actions/workflows/validate.yml/badge.svg)](https://github.com/kumaradoss16/DevSpire-Nexus-Registry/actions)
[![Test Suite](https://github.com/kumaradoss16/DevSpire-Nexus-Registry/actions/workflows/tests.yml/badge.svg)](https://github.com/kumaradoss16/DevSpire-Nexus-Registry/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Resources](https://img.shields.io/badge/Total%20Resources-1%2C003-brightgreen.svg)](#datasets-summary)
[![JSON Schema](https://img.shields.io/badge/JSON%20Schema-Draft%202020--12-orange.svg)](schemas/)

> **The canonical, evidence-backed open data registry of verified AI Tools, AI Models, and Developer Resources.**  
> Official catalog backing the [DevSpire Nexus](https://github.com/kumaradoss16/Devspire-Nexus) intelligence directory.  
> Parent Brand: **[DevSpireHub.com](https://devspirehub.com)** · *Discover. Connect. Build.*

---

## 🏛️ System Architecture

DevSpire Nexus operates under a strict two-repository architecture:

1. **[DevSpire-Nexus](https://github.com/kumaradoss16/Devspire-Nexus)**: The user-facing web application (vanilla HTML/CSS/JS, static directory UI, interactive search, client-side bookmarks, and terminal).
2. **`DevSpire-Nexus-Registry` (This Repository)**: The authoritative open-source data engine, housing canonical datasets, Draft 2020-12 JSON Schemas, automated validators, the `nexus-registry` CLI, and versioned static API artifacts.

```
┌────────────────────────────────────────────────────────┐
│              DevSpire-Nexus-Registry                    │
│   (Canonical Data · Schemas · CLI · Python SDK · API)  │
└──────────────────────────┬─────────────────────────────┘
                           │ Consumes static API / JSON
                           ▼
┌────────────────────────────────────────────────────────┐
│                   DevSpire-Nexus                        │
│   (Web Frontend · Search UI · Personal Collections)     │
└────────────────────────────────────────────────────────┘
```

---

## 📊 Datasets Summary

All records are validated against formal JSON Schemas and primary source evidence:

| Registry | File | Count | Categories | Key Features |
|---|---|---|---|---|
| **AI Tools** | [`datasets/ai-tools.json`](datasets/ai-tools.json) | **403** | 14 | Platform, hosting, pricing class, verified icon assets |
| **AI Models** | [`datasets/ai-models.json`](datasets/ai-models.json) | **300** | 12 | Weights (open/closed), context windows, parameter sizes, modalities |
| **Developer Resources** | [`datasets/developer-resources.json`](datasets/developer-resources.json) | **300** | 12 | 32 verified Developer Quick Starts, repos, docs, SDKs |
| **Global Total** | - | **1,003** | 38 | 100% unique slug identifiers across all registries |

---

## 🚀 Quick Start: Python CLI

Install the registry toolkit locally:

```bash
git clone https://github.com/kumaradoss16/DevSpire-Nexus-Registry.git
cd DevSpire-Nexus-Registry
pip install -e .
```

### Validate datasets:
```bash
nexus-registry validate
```

### Search the catalog:
```bash
nexus-registry search "ollama"
nexus-registry search "vector database" --registry developer
```

### Inspect resource details & evidence:
```bash
nexus-registry info langchain
nexus-registry info gpt-4o
```

### Fetch verified Developer Quick Start reference:
```bash
nexus-registry quickstart langchain
```

### View catalog statistics:
```bash
nexus-registry stats
```

---

## 🐍 Python SDK Client

Embed or query registry datasets in Python applications without external network dependencies:

```python
from nexus_registry import RegistryClient

client = RegistryClient()

# Retrieve a single resource by slug
resource = client.get("langchain")
print(f"Name: {resource['name']} | License: {resource['license']}")

# Search by keyword
results = client.search("retrieval augmented generation", limit=5)
for r in results:
    print(f"- {r['name']} ({r['id']})")

# Fetch verified Quick Start instructions
qs = client.get_quickstart("qdrant")
if qs and qs["available"]:
    print(f"Package: {qs['package_name']}")
    for cmd in qs["installation"]:
        print(f"  [{cmd['pm']}]: {cmd['command']}")
```

---

## 🌐 Static JSON API (v1)

Deterministic static JSON endpoints are compiled into `api/v1/`:

- [`api/v1/tools.json`](api/v1/tools.json) - 403 AI Tools
- [`api/v1/models.json`](api/v1/models.json) - 300 AI Models
- [`api/v1/developer-resources.json`](api/v1/developer-resources.json) - 300 Developer Resources
- [`api/v1/categories.json`](api/v1/categories.json) - Taxonomy breakdown
- [`api/v1/stats.json`](api/v1/stats.json) - Registry-wide counts and distributions
- [`api/v1/catalog.json`](api/v1/catalog.json) - SHA256 integrity manifest

Re-generate static endpoints deterministically:
```bash
python scripts/generate_api.py
```

---

## 🧪 Testing

Run the automated test suite (26 unit tests):

```bash
python -m unittest discover -s tests
```

---

## 🤝 Contributing

Contributions are warmly welcomed! Please read our [Governance Guide](docs/governance.md) and [Verification Policy](docs/verification-policy.md) before submitting.

1. Fork this repository.
2. Create your branch (`git checkout -b submission/my-resource`).
3. Ensure all tests and schema checks pass (`nexus-registry validate`).
4. Submit a Pull Request following our [PR Template](.github/PULL_REQUEST_TEMPLATE.md).

---

## 📄 License

This repository is licensed under the [MIT License](LICENSE).
Datasets are curated under evidence-oriented, fair-use informational guidelines.
