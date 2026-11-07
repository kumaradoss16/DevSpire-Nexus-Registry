"""
Unit tests for DevSpire Nexus Registry Phase 1 Data Quality & Verification Infrastructure.
Tests structural validation, identity integrity, evidence auditing, metadata/freshness,
scoring gates, and quality CLI subcommands.
"""

import json
import unittest
from pathlib import Path

from nexus_registry.quality import (
    StructuralValidator,
    ValidationError,
    UniquenessChecker,
    DuplicateClassification,
    URLAuditor,
    MetadataAuditor,
    MetadataSeverity,
    EvidenceAuditor,
    EvidenceArchetype,
    VerificationEngine,
    VerificationStatus,
    FreshnessChecker,
    FreshnessCategory,
    QualityScorer,
    QualityGrade,
    QualityReportGenerator,
)


class TestStructuralValidator(unittest.TestCase):
    """Test JSON Schema structural validation and error reporting."""

    def setUp(self):
        self.validator = StructuralValidator()

    def test_valid_record(self):
        valid_record = {
            "id": "sample-tool",
            "name": "Sample Tool",
            "description": "A fully valid sample AI tool for unit testing purposes.",
            "category": "Coding & Development",
            "resource_type": "AI Tool",
            "official_url": "https://sample.devspirehub.com/",
            "pricing": "Free",
            "pricing_class": "free",
            "license": "MIT",
            "tags": ["ai", "sample"],
            "verified": "2026-11-07",
            "status": "verified",
            "evidence": [["Official website", "https://sample.devspirehub.com/"]],
            "canonical_id": "ai_tool:sample-tool",
        }
        errors = self.validator.validate_record(valid_record, "ai-tools")
        self.assertEqual(len(errors), 0, f"Expected 0 errors, got: {errors}")

    def test_missing_required_field(self):
        bad_record = {
            "id": "missing-name",
            # missing "name"
            "description": "A sample tool missing its canonical name attribute.",
            "category": "Productivity",
            "resource_type": "AI Tool",
            "official_url": "https://sample.com",
            "pricing": "Free",
            "license": "MIT",
            "tags": ["sample"],
            "verified": "2026-11-07",
            "status": "verified",
            "evidence": [["Official Site", "https://sample.com"]],
            "canonical_id": "ai_tool:missing-name",
        }
        errors = self.validator.validate_record(bad_record, "ai-tools")
        paths = [e.field_path for e in errors]
        self.assertIn("$.name", paths)

    def test_invalid_id_pattern(self):
        bad_id_record = {
            "id": "Invalid_ID_Uppercase!",
            "name": "Bad ID",
            "description": "A sample tool with an invalid uppercase identifier.",
            "category": "Productivity",
            "resource_type": "AI Tool",
            "official_url": "https://sample.com",
            "pricing": "Free",
            "license": "MIT",
            "tags": ["sample"],
            "verified": "2026-11-07",
            "status": "verified",
            "evidence": [["Official Site", "https://sample.com"]],
            "canonical_id": "ai_tool:Invalid_ID_Uppercase!",
        }
        errors = self.validator.validate_record(bad_id_record, "ai-tools")
        paths = [e.field_path for e in errors]
        self.assertIn("$.id", paths)

    def test_invalid_enum_status(self):
        bad_status_record = {
            "id": "bad-status",
            "name": "Bad Status",
            "description": "A sample tool with an unsupported verification status.",
            "category": "Productivity",
            "resource_type": "AI Tool",
            "official_url": "https://sample.com",
            "pricing": "Free",
            "license": "MIT",
            "tags": ["sample"],
            "verified": "2026-11-07",
            "status": "SUPER_VERIFIED",
            "evidence": [["Official Site", "https://sample.com"]],
            "canonical_id": "ai_tool:bad-status",
        }
        errors = self.validator.validate_record(bad_status_record, "ai-tools")
        paths = [e.field_path for e in errors]
        self.assertIn("$.status", paths)


class TestUniquenessChecker(unittest.TestCase):
    """Test identity uniqueness, URL normalization, and duplicate classification."""

    def setUp(self):
        self.checker = UniquenessChecker()

    def test_url_normalization(self):
        raw_url = "https://WWW.Example.com:443/products/ai/?utm_source=twitter&ref=123#overview"
        normalized = self.checker.normalize_url(raw_url)
        self.assertEqual(normalized, "https://example.com/products/ai")

    def test_duplicate_id_detection(self):
        datasets = {
            "ai-tools": [
                {"id": "duplicate-tool", "name": "Tool A", "official_url": "https://a.com"},
                {"id": "duplicate-tool", "name": "Tool B", "official_url": "https://b.com"},
            ],
            "ai-models": []
        }
        rep = self.checker.audit(datasets)
        self.assertTrue(rep.has_identity_conflicts)
        self.assertEqual(len(rep.duplicate_ids), 1)
        self.assertEqual(rep.duplicate_ids[0]["id"], "duplicate-tool")

    def test_cross_registry_collision(self):
        datasets = {
            "ai-tools": [{"id": "collision-id", "name": "Tool", "official_url": "https://t.com"}],
            "ai-models": [{"id": "collision-id", "name": "Model", "official_url": "https://m.com"}],
        }
        rep = self.checker.audit(datasets)
        self.assertTrue(rep.has_identity_conflicts)
        self.assertEqual(len(rep.cross_registry_id_collisions), 1)

    def test_probable_duplicate_classification(self):
        datasets = {
            "ai-models": [
                {"id": "cohere-rerank-3", "name": "Cohere Rerank 3", "official_url": "https://cohere.com/rerank"},
                {"id": "cohere-rerank-v3", "name": "Cohere Rerank 3", "official_url": "https://cohere.com/rerank"},
            ]
        }
        rep = self.checker.audit(datasets)
        self.assertEqual(len(rep.url_findings), 1)
        finding = rep.url_findings[0]
        self.assertEqual(finding.classification, DuplicateClassification.PROBABLE_DUPLICATE)


class TestEvidenceAuditor(unittest.TestCase):
    """Test classification of evidence into canonical archetypes."""

    def setUp(self):
        self.auditor = EvidenceAuditor()

    def test_classify_archetypes(self):
        cases = [
            ("GitHub Repo", "https://github.com/langchain-ai/langchain", EvidenceArchetype.SOURCE_REPOSITORY, True),
            ("Official Docs", "https://docs.anthropic.com/claude", EvidenceArchetype.OFFICIAL_DOCUMENTATION, True),
            ("PyPI Package", "https://pypi.org/project/vllm/", EvidenceArchetype.PACKAGE_REGISTRY, True),
            ("Hugging Face Model Card", "https://huggingface.co/meta-llama/Llama-3-8B", EvidenceArchetype.MODEL_CARD, True),
            ("ArXiv Preprint", "https://arxiv.org/abs/2303.08774", EvidenceArchetype.RESEARCH_PAPER, True),
            ("Reddit Discussion", "https://reddit.com/r/MachineLearning/comments/xyz", EvidenceArchetype.COMMUNITY_SOURCE, False),
        ]
        for label, url, expected_arch, expected_prim in cases:
            arch, is_prim, _ = self.auditor.classify_source(label, url)
            self.assertEqual(arch, expected_arch, f"Failed for {url}")
            self.assertEqual(is_prim, expected_prim, f"Primary mismatch for {url}")

    def test_insufficient_evidence_for_verified(self):
        record = {
            "id": "unverified-tool",
            "status": "verified",
            "evidence": [["Reddit Thread", "https://reddit.com/r/ai/sample"]]
        }
        audit = self.auditor.audit_record_evidence(record, "ai-tools")
        self.assertFalse(audit.is_sufficient_for_verification)
        self.assertIn("Record is marked 'verified' but lacks at least one primary source citation.", audit.issues)


class TestMetadataAndFreshness(unittest.TestCase):
    """Test metadata completeness and freshness checking."""

    def test_metadata_completeness(self):
        auditor = MetadataAuditor()
        record = {
            "id": "sparse-tool",
            "name": "Sparse Tool",
            "official_url": "https://sparse.com",
            "category": "Coding & Development",
            "resource_type": "AI Tool",
            "pricing": "Free",
            "verified": "2026-11-07",
            "status": "verified",
            "evidence": [["Website", "https://sparse.com"]],
            "canonical_id": "ai_tool:sparse-tool",
            # missing description & tags (HIGH severity)
        }
        findings = auditor.audit_record(record, "ai-tools")
        fields = [f.field_name for f in findings]
        self.assertIn("description", fields)
        self.assertIn("tags", fields)

    def test_freshness_category(self):
        from datetime import date, timedelta
        today = date.today()
        checker = FreshnessChecker(reference_date=today)

        # 10 days old -> Fresh
        d_fresh = (today - timedelta(days=10)).isoformat()
        res_fresh = checker.audit_record_freshness({"id": "f", "verified": d_fresh}, "ai-tools")
        self.assertEqual(res_fresh.category, FreshnessCategory.FRESH)

        # 400 days old -> Stale
        d_stale = (today - timedelta(days=400)).isoformat()
        res_stale = checker.audit_record_freshness({"id": "s", "verified": d_stale}, "ai-tools")
        self.assertEqual(res_stale.category, FreshnessCategory.STALE)
        self.assertTrue(res_stale.is_stale)


class TestQualityScorer(unittest.TestCase):
    """Test quality score calculations and the critical structural gate."""

    def setUp(self):
        self.scorer = QualityScorer()

    def test_structural_gate_blocks_release(self):
        # 1 schema violation must block release readiness regardless of other scores
        rep = self.scorer.calculate_score(
            registry="ai-tools",
            total_records=100,
            structural_valid_pct=99.0,
            identity_integrity_pct=100.0,
            url_integrity_pct=100.0,
            metadata_completeness_pct=100.0,
            evidence_coverage_pct=100.0,
            verification_integrity_pct=100.0,
            freshness_pct=100.0,
            invalid_record_count=1,
            duplicate_id_count=0
        )
        self.assertFalse(rep.structural_gate_passed)
        self.assertFalse(rep.is_release_ready)
        self.assertTrue(any("STRUCTURAL GATE FAILED" in issue for issue in rep.blocking_issues))

    def test_perfect_score(self):
        rep = self.scorer.calculate_score(
            registry="ai-tools",
            total_records=100,
            structural_valid_pct=100.0,
            identity_integrity_pct=100.0,
            url_integrity_pct=100.0,
            metadata_completeness_pct=100.0,
            evidence_coverage_pct=100.0,
            verification_integrity_pct=100.0,
            freshness_pct=100.0,
            invalid_record_count=0,
            duplicate_id_count=0
        )
        self.assertTrue(rep.structural_gate_passed)
        self.assertTrue(rep.is_release_ready)
        self.assertEqual(rep.overall_score, 100.0)
        self.assertEqual(rep.grade, QualityGrade.EXCELLENT)


class TestReportGenerator(unittest.TestCase):
    """Test comprehensive report generator across real canonical datasets."""

    def test_full_audit_runs(self):
        gen = QualityReportGenerator()
        data = gen.run_full_audit(check_network=False)
        self.assertIn("catalog_summary", data)
        self.assertEqual(data["catalog_summary"]["total_records"], 1003)
        self.assertTrue(data["catalog_summary"]["structural_gate_passed"])
        self.assertTrue(data["catalog_summary"]["is_release_ready"])
        self.assertGreaterEqual(data["catalog_summary"]["overall_score"], 95.0)


if __name__ == "__main__":
    unittest.main()
