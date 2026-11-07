# DevSpire Nexus Registry — Python SDK

The official Python client library for querying, searching, filtering, and embedding canonical AI Tools, AI Models, and Developer Resources into applications, agent frameworks, and evaluation pipelines.

---

## Key Features

- **Zero Runtime Dependencies:** Built strictly on the Python standard library. No dependency conflicts.
- **Offline Capable:** Automatically embeds and queries canonical datasets bundled inside the package.
- **Instant Latency:** In-memory lookups resolve in $< 1\text{ ms}$; full catalog loads in $< 15\text{ ms}$.
- **Comprehensive API:** Simple methods for $O(1)$ ID lookups, multi-keyword search, category filtering, and Quick Start command extraction.

---

## Quick Start

```python
from nexus_registry import RegistryClient

# 1. Initialize client (zero configuration needed)
client = RegistryClient()

# 2. Lookup a resource by ID or slug (case-insensitive)
resource = client.get("langchain")
if resource:
    print(f"Name:    {resource['name']}")
    print(f"Category:{resource['category']}")
    print(f"URL:     {resource['official_url']}")
    print(f"Status:  {resource['status']}")

# 3. Search across all registries
results = client.search("inference", limit=5)
for r in results:
    print(f"• {r['name']} ({r['id']}) - {r['official_url']}")

# 4. Filter by registry
models = client.get_models()
print(f"Total Models Available: {len(models)}")
```

---

## Detailed Documentation

- [Installation & Build Guide](file:///H:/DevSpire-Nexus-Registry/docs/sdk/INSTALLATION.md)
- [Complete Python SDK API Reference](file:///H:/DevSpire-Nexus-Registry/docs/sdk/API_REFERENCE.md)
- [Static JSON API Documentation](file:///H:/DevSpire-Nexus-Registry/docs/api/STATIC_API.md)
