import os
import unittest
from pathlib import Path

from nexus_registry import RegistryClient, RegistryValidator


class TestStandaloneLoading(unittest.TestCase):
    def test_client_loads_bundled_datasets_with_dummy_root(self):
        # Even with a foreign directory that has no datasets, client falls back to bundled package data
        client = RegistryClient(root_dir=Path("C:/DummyNonExistentDir12345"))
        self.assertEqual(len(client.get_tools()), 403)
        self.assertEqual(len(client.get_models()), 300)
        self.assertEqual(len(client.get_developer_resources()), 300)

        # Quickstart works from bundled package data
        qs = client.get_quickstart("langchain")
        self.assertIsNotNone(qs)
        self.assertEqual(qs.get("package_name"), "langchain")

    def test_validator_loads_bundled_schemas(self):
        validator = RegistryValidator(root_dir=Path("C:/DummyNonExistentDir12345"))
        self.assertTrue((validator.schemas_dir / "common.schema.json").exists())
        self.assertTrue((validator.datasets_dir / "ai-tools.json").exists())


if __name__ == "__main__":
    unittest.main()
