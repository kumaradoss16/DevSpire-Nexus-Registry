import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from nexus_registry.client import RegistryClient


class TestClient(unittest.TestCase):
    def setUp(self):
        self.client = RegistryClient(repo_root=REPO_ROOT)

    def test_client_loads_datasets(self):
        tools = self.client.get_tools()
        models = self.client.get_models()
        dev = self.client.get_developer_resources()

        self.assertEqual(len(tools), 403)
        self.assertEqual(len(models), 300)
        self.assertEqual(len(dev), 300)

    def test_get_resource_by_id(self):
        chatgpt = self.client.get_resource("chatgpt")
        self.assertIsNotNone(chatgpt)
        self.assertEqual(chatgpt["name"], "ChatGPT")
        self.assertEqual(chatgpt["_registry"], "ai-tools")

        langchain = self.client.get_resource("langchain")
        self.assertIsNotNone(langchain)
        self.assertEqual(langchain["name"], "LangChain")
        self.assertEqual(langchain["_registry"], "developer-resources")

    def test_search_resources(self):
        results = self.client.search("python", limit=10)
        self.assertGreater(len(results), 0)
        self.assertLessEqual(len(results), 10)

    def test_get_quickstart(self):
        qs = self.client.get_quickstart("langchain")
        self.assertIsNotNone(qs)
        self.assertTrue(qs.get("available"))
        self.assertIn("installation", qs)
        self.assertIn("examples", qs)

    def test_categories_and_stats(self):
        cats = self.client.categories()
        self.assertIn("ai-tools", cats)
        self.assertIn("ai-models", cats)
        self.assertIn("developer-resources", cats)

        stats = self.client.stats()
        self.assertEqual(stats["total_resources"], 1003)
        self.assertEqual(stats["tools_count"], 403)
        self.assertEqual(stats["models_count"], 300)
        self.assertEqual(stats["developer_resources_count"], 300)
        self.assertEqual(stats["quickstarts_available"], 32)


if __name__ == "__main__":
    unittest.main()
