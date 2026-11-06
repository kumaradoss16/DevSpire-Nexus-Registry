import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from nexus_registry.cli import main


class TestCLI(unittest.TestCase):
    def run_cli(self, args: list[str]) -> tuple[int, str]:
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = main(args, repo_root=REPO_ROOT)
        return code, buf.getvalue()

    def test_cli_version(self):
        code, out = self.run_cli(["version"])
        self.assertEqual(code, 0)
        self.assertIn("nexus-registry", out)

    def test_cli_stats(self):
        code, out = self.run_cli(["stats"])
        self.assertEqual(code, 0)
        self.assertIn("1,003", out)

    def test_cli_categories(self):
        code, out = self.run_cli(["categories"])
        self.assertEqual(code, 0)
        self.assertIn("Agent Frameworks", out)

    def test_cli_search(self):
        code, out = self.run_cli(["search", "ollama"])
        self.assertEqual(code, 0)
        self.assertIn("ollama", out)

    def test_cli_info(self):
        code, out = self.run_cli(["info", "chatgpt"])
        self.assertEqual(code, 0)
        self.assertIn("ChatGPT", out)

    def test_cli_quickstart(self):
        code, out = self.run_cli(["quickstart", "langchain"])
        self.assertEqual(code, 0)
        self.assertIn("LangChain", out)

    def test_cli_validate(self):
        code, out = self.run_cli(["validate"])
        self.assertEqual(code, 0)
        self.assertIn("PASS [OK]", out)


if __name__ == "__main__":
    unittest.main()
