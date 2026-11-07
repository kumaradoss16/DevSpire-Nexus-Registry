"""
Unit tests for schema compatibility checker.
Verifies detection of breaking changes vs backward-compatible schema modifications.
"""

import unittest
from nexus_registry.quality import (
    CompatibilityChecker,
    CompatibilityChangeType,
)


class TestCompatibilityChecker(unittest.TestCase):
    def setUp(self):
        self.checker = CompatibilityChecker()
        self.base_schema = {
            "type": "object",
            "required": ["id", "name"],
            "properties": {
                "id": {"type": "string"},
                "name": {"type": "string"},
                "pricing": {"type": "string"},
                "status": {"type": "string", "enum": ["verified", "unverified"]},
            }
        }

    def test_identical_schemas_are_compatible(self):
        report = self.checker.compare_schemas(self.base_schema, self.base_schema)
        self.assertTrue(report.is_backward_compatible)
        self.assertEqual(len(report.breaking_changes), 0)

    def test_removed_property_is_breaking(self):
        new_schema = {
            "type": "object",
            "required": ["id", "name"],
            "properties": {
                "id": {"type": "string"},
                "name": {"type": "string"},
                # "pricing" removed!
                "status": {"type": "string", "enum": ["verified", "unverified"]},
            }
        }
        report = self.checker.compare_schemas(self.base_schema, new_schema)
        self.assertFalse(report.is_backward_compatible)
        self.assertEqual(len(report.breaking_changes), 1)
        self.assertEqual(report.breaking_changes[0].field_name, "pricing")

    def test_added_optional_property_is_backward_compatible(self):
        new_schema = {
            "type": "object",
            "required": ["id", "name"],
            "properties": {
                "id": {"type": "string"},
                "name": {"type": "string"},
                "pricing": {"type": "string"},
                "status": {"type": "string", "enum": ["verified", "unverified"]},
                "tags": {"type": "array", "items": {"type": "string"}},  # Added optional
            }
        }
        report = self.checker.compare_schemas(self.base_schema, new_schema)
        self.assertTrue(report.is_backward_compatible)
        self.assertEqual(len(report.compatible_changes), 1)
        self.assertEqual(report.compatible_changes[0].field_name, "tags")

    def test_newly_required_property_is_breaking(self):
        new_schema = {
            "type": "object",
            "required": ["id", "name", "pricing"],  # pricing now required!
            "properties": {
                "id": {"type": "string"},
                "name": {"type": "string"},
                "pricing": {"type": "string"},
                "status": {"type": "string", "enum": ["verified", "unverified"]},
            }
        }
        report = self.checker.compare_schemas(self.base_schema, new_schema)
        self.assertFalse(report.is_backward_compatible)
        self.assertEqual(len(report.breaking_changes), 1)
        self.assertEqual(report.breaking_changes[0].field_name, "pricing")

    def test_changed_type_is_breaking(self):
        new_schema = {
            "type": "object",
            "required": ["id", "name"],
            "properties": {
                "id": {"type": "string"},
                "name": {"type": "string"},
                "pricing": {"type": "number"},  # changed from string to number!
                "status": {"type": "string", "enum": ["verified", "unverified"]},
            }
        }
        report = self.checker.compare_schemas(self.base_schema, new_schema)
        self.assertFalse(report.is_backward_compatible)
        self.assertEqual(len(report.breaking_changes), 1)
        self.assertEqual(report.breaking_changes[0].field_name, "pricing")

    def test_removed_enum_value_is_breaking(self):
        new_schema = {
            "type": "object",
            "required": ["id", "name"],
            "properties": {
                "id": {"type": "string"},
                "name": {"type": "string"},
                "pricing": {"type": "string"},
                "status": {"type": "string", "enum": ["verified"]},  # "unverified" removed!
            }
        }
        report = self.checker.compare_schemas(self.base_schema, new_schema)
        self.assertFalse(report.is_backward_compatible)
        self.assertEqual(len(report.breaking_changes), 1)
        self.assertEqual(report.breaking_changes[0].field_name, "status")


if __name__ == "__main__":
    unittest.main()
