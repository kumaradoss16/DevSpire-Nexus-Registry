"""
Developer Experience (DX) and Consumer Acceptance Tests for DevSpire Nexus Registry.
Validates the complete external developer consumption journey across Static API and Python SDK.
"""

import json
import unittest
from pathlib import Path

from nexus_registry import RegistryClient

REPO_ROOT = Path(__file__).resolve().parent.parent
API_V1_DIR = REPO_ROOT / "api" / "v1"


class TestStaticAPIEndpoints(unittest.TestCase):
    """Acceptance tests for static JSON API endpoints."""

    def test_all_documented_endpoints_exist(self):
        expected_endpoints = [
            "tools.json",
            "models.json",
            "developer-resources.json",
            "categories.json",
            "stats.json",
            "catalog.json",
            "schemas/tools.schema.json",
            "schemas/models.schema.json",
            "schemas/developer-resources.schema.json",
            "schemas/common.schema.json",
        ]
        for ep in expected_endpoints:
            p = API_V1_DIR / ep
            self.assertTrue(p.exists(), f"Documented API endpoint missing: {ep}")

    def test_record_counts_and_envelope(self):
        files = {
            "tools.json": 403,
            "models.json": 300,
            "developer-resources.json": 300,
        }
        for fn, expected_count in files.items():
            data = json.loads((API_V1_DIR / fn).read_text(encoding="utf-8"))
            self.assertIn("_meta", data)
            self.assertIn("items", data)
            self.assertEqual(data["_meta"]["api_version"], "v1")
            self.assertEqual(data["_meta"]["count"], expected_count)
            self.assertEqual(len(data["items"]), expected_count)

    def test_catalog_manifest_consistency(self):
        cat = json.loads((API_V1_DIR / "catalog.json").read_text(encoding="utf-8"))
        meta = cat.get("_meta", {})
        self.assertEqual(meta.get("api_version"), "v1")
        self.assertEqual(meta.get("version"), "1.0.0")
        self.assertEqual(meta.get("total_resources"), 1003)
        self.assertIn("endpoints", meta)
        self.assertIn("schemas", meta)


class TestSDKDeveloperExperience(unittest.TestCase):
    """Acceptance tests for Python SDK public interface."""

    def setUp(self):
        self.client = RegistryClient()

    def test_client_initialization_and_counts(self):
        self.assertEqual(len(self.client.get_tools()), 403)
        self.assertEqual(len(self.client.get_models()), 300)
        self.assertEqual(len(self.client.get_developer_resources()), 300)

    def test_get_resource_case_insensitivity(self):
        # Lookups should succeed regardless of case
        rec_lower = self.client.get("langchain")
        rec_upper = self.client.get("LANGCHAIN")
        rec_title = self.client.get("LangChain")

        self.assertIsNotNone(rec_lower)
        self.assertEqual(rec_lower, rec_upper)
        self.assertEqual(rec_lower, rec_title)
        self.assertEqual(rec_lower["name"], "LangChain")

    def test_get_missing_resource_returns_none(self):
        res = self.client.get("non-existent-xyz-slug")
        self.assertIsNone(res)

    def test_search_and_limits(self):
        results = self.client.search("inference", limit=3)
        self.assertLessEqual(len(results), 3)
        self.assertGreater(len(results), 0)

    def test_quickstart_retrieval(self):
        qs = self.client.get_quickstart("langchain")
        self.assertIsNotNone(qs)
        self.assertTrue(qs.get("available"))
        self.assertIn("installation", qs)

    def test_stats_metrics(self):
        st = self.client.stats()
        self.assertEqual(st["total_resources"], 1003)
        self.assertEqual(st["tools_count"], 403)
        self.assertEqual(st["models_count"], 300)
        self.assertEqual(st["developer_resources_count"], 300)


if __name__ == "__main__":
    unittest.main()
