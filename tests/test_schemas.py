import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))
SCHEMAS_DIR = REPO_ROOT / "schemas"


class TestSchemas(unittest.TestCase):
    def test_schema_files_exist(self):
        expected = [
            "common.schema.json",
            "ai-tool.schema.json",
            "ai-model.schema.json",
            "developer-resource.schema.json",
        ]
        for name in expected:
            path = SCHEMAS_DIR / name
            self.assertTrue(path.exists(), f"Missing schema file: {name}")

    def test_schemas_are_valid_json(self):
        for path in SCHEMAS_DIR.glob("*.json"):
            with self.subTest(schema=path.name):
                content = json.loads(path.read_text(encoding="utf-8"))
                self.assertIn("$schema", content)
                self.assertIn("title", content)
                self.assertEqual(content["$schema"], "https://json-schema.org/draft/2020-12/schema")

    def test_common_schema_properties(self):
        common = json.loads((SCHEMAS_DIR / "common.schema.json").read_text(encoding="utf-8"))
        props = common.get("properties", {})
        self.assertIn("id", props)
        self.assertIn("name", props)
        self.assertIn("description", props)
        self.assertIn("official_url", props)
        self.assertIn("evidence", props)
        self.assertIn("canonical_id", props)

    def test_specialized_schemas_require_base(self):
        for name in ["ai-tool.schema.json", "ai-model.schema.json", "developer-resource.schema.json"]:
            schema = json.loads((SCHEMAS_DIR / name).read_text(encoding="utf-8"))
            self.assertIn("allOf", schema, f"Schema {name} should inherit from common schema via allOf")


if __name__ == "__main__":
    unittest.main()
