# DevSpire Nexus Registry — Python SDK API Reference

**Package:** `nexus-registry`  
**Module:** `nexus_registry.client`  
**Class:** `RegistryClient`

---

## Constructor

### `RegistryClient(root_dir=None, repo_root=None)`

Initializes the client and resolves canonical dataset files using a robust 3-tier fallback pipeline:
1. User-supplied custom root directory (`root_dir`).
2. Active local Git repository clone (`../../datasets/`).
3. Packaged data bundled within the wheel via `importlib.resources`.

```python
from nexus_registry import RegistryClient

# Default initialization (recommended)
client = RegistryClient()

# Custom datasets directory
client = RegistryClient(root_dir="/path/to/custom/datasets")
```

---

## Retrieval Methods

### `client.get(resource_id: str) -> Optional[Dict[str, Any]]`
Retrieves a single canonical resource record by ID across all three registries. Lookups are case-insensitive and normalized. Returns `None` if the resource does not exist.

### `client.get_resource(resource_id: str) -> Optional[Dict[str, Any]]`
Exact alias for `get()`.

### `client.get_tools() -> List[Dict[str, Any]]`
Returns all 403 AI Tool records.

### `client.get_models() -> List[Dict[str, Any]]`
Returns all 300 AI Model records.

### `client.get_developer_resources() -> List[Dict[str, Any]]`
Returns all 300 Developer Resource records.

### `client.get_quickstart(resource_id: str) -> Optional[Dict[str, Any]]`
Retrieves the verified Quick Start instructions for a developer resource (e.g. `pip`, `npm`, `uv` installation commands and tested code snippets). Returns `None` if no guide is available.

---

## Search & Filtering

### `client.search(query: str, registry=None, category=None, limit=20) -> List[Dict[str, Any]]`
Searches across resource titles, descriptions, categories, and tags.

- `query` (`str`): Search keywords.
- `registry` (`str | None`): Optional filter (`"tools"`, `"models"`, `"developer"`).
- `category` (`str | None`): Optional exact category name match.
- `limit` (`int`): Maximum results to return (default: `20`).

### `client.list_categories(registry=None) -> List[str]`
Returns a sorted list of unique category names within a specified registry or across all registries.

### `client.categories() -> Dict[str, List[str]]`
Returns a dictionary mapping each registry to its list of taxonomy categories.

### `client.stats() -> Dict[str, Any]`
Returns real-time aggregate metrics including total resources, per-registry counts, verified counts, and category counts.
