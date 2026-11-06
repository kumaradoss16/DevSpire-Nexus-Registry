import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from nexus_registry.validator import RegistryValidator


class TestValidator(unittest.TestCase):
    def setUp(self):
        self.validator = RegistryValidator(repo_root=REPO_ROOT)

    def test_canonical_datasets_pass_validation(self):
        res = self.validator.validate_all()
        self.assertTrue(
            res.is_valid,
            f"Canonical datasets failed validation: {[i.message for i in res.issues if i.severity.value == 'ERROR'][:5]}",
        )
        self.assertEqual(res.total_records, 1003)

    def test_catches_invalid_slug(self):
        invalid_rec = {
            "id": "INVALID_SLUG!!",
            "name": "Test Tool",
            "description": "Valid description of at least twenty characters.",
            "category": "Coding & Development",
            "resource_type": "AI Tool",
            "official_url": "https://example.com",
            "pricing": "Free",
            "license": "MIT",
        }
        res = self.validator.validate_record(invalid_rec, "ai-tools")
        self.assertFalse(res.is_valid)
        self.assertTrue(any("slug pattern" in issue.message for issue in res.issues))

    def test_catches_missing_required_fields(self):
        invalid_rec = {
            "id": "test-tool",
            "name": "Test Tool",
        }
        res = self.validator.validate_record(invalid_rec, "ai-tools")
        self.assertFalse(res.is_valid)
        missing_fields = [issue.field for issue in res.issues]
        self.assertIn("description", missing_fields)
        self.assertIn("category", missing_fields)
        self.assertIn("official_url", missing_fields)

    def test_catches_invalid_url_protocol(self):
        invalid_rec = {
            "id": "test-tool",
            "name": "Test Tool",
            "description": "Valid description of at least twenty characters.",
            "category": "Coding & Development",
            "resource_type": "AI Tool",
            "official_url": "ftp://example.com",
            "pricing": "Free",
            "license": "MIT",
        }
        res = self.validator.validate_record(invalid_rec, "ai-tools")
        self.assertFalse(res.is_valid)
        self.assertTrue(any("Malformed URL" in issue.message for issue in res.issues))


if __name__ == "__main__":
    unittest.main()
