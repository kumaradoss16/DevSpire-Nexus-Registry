import hashlib
import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
API_V1_DIR = REPO_ROOT / "api" / "v1"


class TestAPIReproducibility(unittest.TestCase):
    def test_catalog_manifest_checksums_match_files(self):
        catalog_path = API_V1_DIR / "catalog.json"
        self.assertTrue(catalog_path.exists(), "catalog.json missing")

        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        endpoints = catalog.get("_meta", {}).get("endpoints", {})

        for name, meta in endpoints.items():
            file_path = REPO_ROOT / meta["path"]
            self.assertTrue(file_path.exists(), f"Artifact {name} does not exist at {file_path}")

            content_bytes = file_path.read_bytes()
            computed_sha = hashlib.sha256(content_bytes).hexdigest()
            self.assertEqual(
                computed_sha,
                meta["sha256"],
                f"Checksum mismatch for {name}: catalog says {meta['sha256']}, file hash is {computed_sha}"
            )
            self.assertEqual(len(content_bytes), meta["size_bytes"], f"Size mismatch for {name}")

    def test_deterministic_meta_no_volatile_clock_in_data_files(self):
        for name in ["tools.json", "models.json", "developer-resources.json", "categories.json", "stats.json"]:
            path = API_V1_DIR / name
            data = json.loads(path.read_text(encoding="utf-8"))
            meta = data.get("_meta", {})
            self.assertNotIn(
                "generated_at",
                meta,
                f"Volatile timestamp 'generated_at' should not be present in data artifact {name}"
            )


if __name__ == "__main__":
    unittest.main()
