"""
DevSpire Nexus Registry — Python SDK Client
Lightweight, zero-dependency offline client for querying and embedding
DevSpire Nexus Registry resources into applications and pipelines.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any


class RegistryClient:
    """Client for querying local DevSpire Nexus Registry datasets."""

    def __init__(self, root_dir: Optional[Path] = None, repo_root: Optional[Path] = None):
        if root_dir is None:
            root_dir = repo_root
        if root_dir is None:
            self.root_dir = Path(__file__).resolve().parent.parent.parent
        else:
            self.root_dir = Path(root_dir)

        self.datasets_dir = self.root_dir / "datasets"
        self._cache: Dict[str, List[Dict[str, Any]]] = {}
        self._index: Dict[str, Dict[str, Any]] = {}
        self._loaded = False

    def _ensure_loaded(self):
        if self._loaded:
            return

        registry_map = {
            "tools": self.datasets_dir / "ai-tools.json",
            "models": self.datasets_dir / "ai-models.json",
            "developer": self.datasets_dir / "developer-resources.json"
        }

        for reg_key, p in registry_map.items():
            if p.exists():
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    records = data.get("records", [])
                    self._cache[reg_key] = records
                    for r in records:
                        rec_id = r.get("id")
                        if rec_id:
                            # Attach normalized registry key
                            reg_full = "ai-tools" if reg_key == "tools" else ("ai-models" if reg_key == "models" else "developer-resources")
                            r_copy = dict(r)
                            r_copy["_registry"] = reg_full
                            self._index[rec_id.lower()] = {
                                "registry": reg_full,
                                "record": r_copy
                            }

        self._loaded = True

    def get_tools(self) -> List[Dict[str, Any]]:
        """Return all AI Tools."""
        self._ensure_loaded()
        return self._cache.get("tools", [])

    def get_models(self) -> List[Dict[str, Any]]:
        """Return all AI Models."""
        self._ensure_loaded()
        return self._cache.get("models", [])

    def get_developer_resources(self) -> List[Dict[str, Any]]:
        """Return all Developer Resources."""
        self._ensure_loaded()
        return self._cache.get("developer", [])

    def get(self, resource_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a single resource record by ID across all registries."""
        self._ensure_loaded()
        item = self._index.get(resource_id.strip().lower())
        return item["record"] if item else None

    def get_resource(self, resource_id: str) -> Optional[Dict[str, Any]]:
        """Alias for get()."""
        return self.get(resource_id)

    def get_quickstart(self, resource_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve the Quick Start reference for a developer resource."""
        res = self.get(resource_id)
        if not res:
            return None
        return res.get("developer_quick_start")

    def search(
        self,
        query: str,
        registry: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Search records by keyword across name, description, category, and tags."""
        self._ensure_loaded()
        q = query.strip().lower()

        active_registries = [registry] if registry and registry in self._cache else list(self._cache.keys())
        results = []

        for reg in active_registries:
            for r in self._cache.get(reg, []):
                if category and r.get("category", "").lower() != category.lower():
                    continue

                haystack = " ".join([
                    str(r.get("name", "")),
                    str(r.get("description", "")),
                    str(r.get("category", "")),
                    str(r.get("resource_type", "")),
                    " ".join(r.get("tags", []))
                ]).lower()

                if q in haystack:
                    results.append(r)
                    if len(results) >= limit:
                        return results

        return results

    def list_categories(self, registry: Optional[str] = None) -> List[str]:
        """List distinct categories within a registry or across all registries."""
        self._ensure_loaded()
        cats = set()
        active = [registry] if registry and registry in self._cache else list(self._cache.keys())
        for reg in active:
            for r in self._cache.get(reg, []):
                c = r.get("category")
                if c:
                    cats.add(c)
        return sorted(list(cats))

    def categories(self) -> Dict[str, List[str]]:
        """Return categorized lists for all registries."""
        return {
            "ai-tools": self.list_categories("tools"),
            "ai-models": self.list_categories("models"),
            "developer-resources": self.list_categories("developer")
        }

    def stats(self) -> Dict[str, Any]:
        """Return catalog record counts, category counts, and verification totals."""
        self._ensure_loaded()
        tools_recs = self._cache.get("tools", [])
        models_recs = self._cache.get("models", [])
        dev_recs = self._cache.get("developer", [])

        qs_available = sum(1 for r in dev_recs if (r.get("developer_quick_start") or {}).get("available"))

        out = {
            "total_resources": len(self._index),
            "tools_count": len(tools_recs),
            "models_count": len(models_recs),
            "developer_resources_count": len(dev_recs),
            "quickstarts_available": qs_available,
            "registries": {}
        }
        for reg, recs in self._cache.items():
            cats = set(r.get("category") for r in recs if r.get("category"))
            verified = sum(1 for r in recs if r.get("status") == "verified")
            out["registries"][reg] = {
                "count": len(recs),
                "categories": len(cats),
                "verified": verified
            }
        return out
