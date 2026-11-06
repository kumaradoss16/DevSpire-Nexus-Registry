# DevSpire Nexus Registry

[![CI Validation](https://github.com/kumaradoss16/DevSpire-Nexus-Registry/actions/workflows/validate.yml/badge.svg)](https://github.com/kumaradoss16/DevSpire-Nexus-Registry/actions)
[![Test Suite](https://github.com/kumaradoss16/DevSpire-Nexus-Registry/actions/workflows/tests.yml/badge.svg)](https://github.com/kumaradoss16/DevSpire-Nexus-Registry/actions)
[![Code License: MIT](https://img.shields.io/badge/Code%20License-MIT-blue.svg)](LICENSE)
[![Data License: ODC--By](https://img.shields.io/badge/Data%20License-ODC--By%201.0-brightgreen.svg)](DATA_LICENSE.md)
[![JSON Schema](https://img.shields.io/badge/JSON%20Schema-Draft%202020--12-orange.svg)](schemas/)

> **The canonical, evidence-backed open data registry of verified AI Tools, AI Models, and Developer Resources.**  
> Authoritative data engine backing the [DevSpire Nexus](https://github.com/kumaradoss16/Devspire-Nexus) intelligence directory.  
> Parent Brand: **[DevSpireHub.com](https://devspirehub.com)** · *Discover. Connect. Build.*

---

## 🏛️ System Architecture

DevSpire Nexus operates under a strict two-repository architecture:

1. **[DevSpire-Nexus](https://github.com/kumaradoss16/Devspire-Nexus)**: The user-facing web application (vanilla HTML5/Tailwind/JS, static directory UI, interactive search, client-side bookmarks, and terminal).
2. **`DevSpire-Nexus-Registry` (This Repository)**: The authoritative open-source data engine, housing canonical datasets, Draft 2020-12 JSON Schemas, automated validators, the `nexus-registry` CLI, bundled Python SDK, and versioned static API artifacts.

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

Install the registry toolkit locally or in your project environment:

```bash
# Clone and install in editable mode
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

# Automatically loads bundled datasets across any environment
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

Deterministic, reproducible static JSON endpoints are compiled into `api/v1/`:

- [`api/v1/tools.json`](api/v1/tools.json) - 403 AI Tools
- [`api/v1/models.json`](api/v1/models.json) - 300 AI Models
- [`api/v1/developer-resources.json`](api/v1/developer-resources.json) - 300 Developer Resources
- [`api/v1/categories.json`](api/v1/categories.json) - Taxonomy breakdown
- [`api/v1/stats.json`](api/v1/stats.json) - Registry-wide counts and distributions
- [`api/v1/catalog.json`](api/v1/catalog.json) - SHA-256 integrity manifest

Re-generate static endpoints deterministically:
```bash
python scripts/generate_api.py
```

---

## 🧪 Testing

Run the automated test suite (30 unit tests covering schemas, datasets, validator, CLI, client, standalone loading, and reproducible API hashing):

```bash
python -m unittest discover -s tests
```

---

## 📚 Documentation

- [Architecture & System Boundaries](docs/architecture.md)
- [Website Integration Guide](docs/website-integration.md)
- [Data Model & Schemas](docs/data-model.md)
- [Verification & Governance Policy](docs/verification-policy.md)
- [Verification Guide](docs/verification-guide.md)
- [Adding a Resource](docs/adding-a-resource.md)
- [CLI Reference](docs/cli-reference.md)
- [Licensing Policy](docs/licensing-policy.md)
- [Release Process](docs/release-process.md)
- [Technical Audit Reports](docs/audit/)

---

## 🤝 Contributing

Contributions are warmly welcomed! Please read our [Contributing Guide](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md).

- Propose a new resource: [Resource Submission Form](.github/ISSUE_TEMPLATE/resource_submission.yml)
- Report outdated metadata: [Data Correction Form](.github/ISSUE_TEMPLATE/data_correction.yml)

---

## 📄 Licensing & Trademarks

- **Software Code:** Licensed under the [MIT License](LICENSE).
- **Curated Datasets:** Licensed under the [Open Data Commons Attribution License (ODC-By v1.0)](DATA_LICENSE.md).
- **Attribution:** See [ATTRIBUTION.md](ATTRIBUTION.md) for citation and usage instructions.
- **Third-Party Content & Trademarks:** See [THIRD_PARTY_CONTENT.md](THIRD_PARTY_CONTENT.md).
