import json
import re
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))
DATASETS_DIR = REPO_ROOT / "datasets"

SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class TestDatasets(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tools_file = DATASETS_DIR / "ai-tools.json"
        cls.models_file = DATASETS_DIR / "ai-models.json"
        cls.dev_file = DATASETS_DIR / "developer-resources.json"

        cls.tools_doc = json.loads(cls.tools_file.read_text(encoding="utf-8"))
        cls.models_doc = json.loads(cls.models_file.read_text(encoding="utf-8"))
        cls.dev_doc = json.loads(cls.dev_file.read_text(encoding="utf-8"))

        cls.tools = cls.tools_doc.get("records", [])
        cls.models = cls.models_doc.get("records", [])
        cls.dev_resources = cls.dev_doc.get("records", [])

    def test_record_counts(self):
        self.assertEqual(len(self.tools), 403, "Expected 403 AI Tools")
        self.assertEqual(len(self.models), 300, "Expected 300 AI Models")
        self.assertEqual(len(self.dev_resources), 300, "Expected 300 Developer Resources")

    def test_global_id_uniqueness(self):
        seen = {}
        all_registries = [
            ("ai-tools", self.tools),
            ("ai-models", self.models),
            ("developer-resources", self.dev_resources),
        ]
        for reg_name, items in all_registries:
            for item in items:
                rid = item.get("id")
                self.assertTrue(rid, f"Resource in {reg_name} has missing or empty id")
                self.assertNotIn(
                    rid,
                    seen,
                    f"Duplicate ID '{rid}' detected in {reg_name} (first seen in {seen.get(rid)})",
                )
                seen[rid] = reg_name
        self.assertEqual(len(seen), 1003, "Expected 1,003 unique resource IDs globally")

    def test_slug_format(self):
        for reg_name, items in [
            ("ai-tools", self.tools),
            ("ai-models", self.models),
            ("developer-resources", self.dev_resources),
        ]:
            for item in items:
                rid = str(item["id"])
                self.assertTrue(
                    SLUG_PATTERN.match(rid),
                    f"ID '{rid}' in {reg_name} does not match kebab-case slug pattern",
                )

    def test_required_common_fields(self):
        required_non_null = ["id", "name", "description", "category", "official_url", "pricing"]
        for reg_name, items in [
            ("ai-tools", self.tools),
            ("ai-models", self.models),
            ("developer-resources", self.dev_resources),
        ]:
            for item in items:
                for req in required_non_null:
                    self.assertIn(req, item, f"Resource '{item.get('id')}' in {reg_name} missing '{req}'")
                    val = item[req]
                    self.assertIsNotNone(val, f"Resource '{item.get('id')}' in {reg_name} has null '{req}'")
                self.assertIn("license", item, f"Resource '{item.get('id')}' missing 'license' key")

    def test_https_urls(self):
        for reg_name, items in [
            ("ai-tools", self.tools),
            ("ai-models", self.models),
            ("developer-resources", self.dev_resources),
        ]:
            for item in items:
                url = item.get("official_url", "")
                self.assertTrue(
                    url.startswith("https://") or url.startswith("http://"),
                    f"Resource '{item.get('id')}' has invalid URL protocol: {url}",
                )

    def test_quickstart_contract(self):
        available_count = 0
        for r in self.dev_resources:
            qs = r.get("developer_quick_start")
            self.assertIsNotNone(qs, f"Developer resource '{r['id']}' missing developer_quick_start block")
            if qs.get("available"):
                available_count += 1
                self.assertTrue(qs.get("package_name"), f"Quickstart for '{r['id']}' missing package_name")
                self.assertTrue(qs.get("installation"), f"Quickstart for '{r['id']}' missing installation commands")
                self.assertTrue(qs.get("documentation"), f"Quickstart for '{r['id']}' missing documentation")
                self.assertTrue(qs.get("examples"), f"Quickstart for '{r['id']}' missing examples")
                for ex in qs["examples"]:
                    self.assertTrue(ex.get("code"), f"Example for '{r['id']}' missing code")
                    self.assertTrue(ex.get("title"), f"Example for '{r['id']}' missing title")
        self.assertEqual(available_count, 32, "Expected exactly 32 verified Developer Quick Starts")


if __name__ == "__main__":
    unittest.main()
