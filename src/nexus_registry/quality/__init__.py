"""
DevSpire Nexus Registry — Data Quality & Verification Infrastructure
Core package export module.
"""

from .structural_validator import StructuralValidator, StructuralValidationResult, ValidationError
from .uniqueness_checker import UniquenessChecker, UniquenessReport, DuplicateClassification
from .url_auditor import URLAuditor, URLAuditResult
from .metadata_auditor import MetadataAuditor, MetadataCompletenessReport, MetadataSeverity
from .evidence_auditor import EvidenceAuditor, EvidenceReport, EvidenceArchetype
from .verification_engine import VerificationEngine, VerificationReport, VerificationStatus
from .freshness_checker import FreshnessChecker, FreshnessReport, FreshnessCategory
from .quality_scorer import QualityScorer, QualityScoreReport, ScoreDimension, QualityGrade
from .report_generator import QualityReportGenerator
from .compatibility_checker import CompatibilityChecker, CompatibilityReport, SchemaChange, CompatibilityChangeType

__all__ = [
    "StructuralValidator",
    "StructuralValidationResult",
    "ValidationError",
    "UniquenessChecker",
    "UniquenessReport",
    "DuplicateClassification",
    "URLAuditor",
    "URLAuditResult",
    "MetadataAuditor",
    "MetadataCompletenessReport",
    "MetadataSeverity",
    "EvidenceAuditor",
    "EvidenceReport",
    "EvidenceArchetype",
    "VerificationEngine",
    "VerificationReport",
    "VerificationStatus",
    "FreshnessChecker",
    "FreshnessReport",
    "FreshnessCategory",
    "QualityScorer",
    "QualityScoreReport",
    "ScoreDimension",
    "QualityGrade",
    "QualityReportGenerator",
    "CompatibilityChecker",
    "CompatibilityReport",
    "SchemaChange",
    "CompatibilityChangeType",
]
