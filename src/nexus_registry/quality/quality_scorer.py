"""
Data quality scoring engine for DevSpire Nexus Registry.
Calculates a transparent, multi-dimensional, versioned quality score with a strict structural gate.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


class QualityGrade(str, Enum):
    EXCELLENT = "Excellent"          # 95 - 100
    GOOD = "Good"                    # 85 - 94
    NEEDS_IMPROVEMENT = "Needs Improvement"  # 70 - 84
    POOR = "Poor"                    # 50 - 69
    CRITICAL = "Critical"            # < 50


@dataclass
class ScoreDimension:
    name: str
    weight: float
    raw_score: float      # 0.0 to 100.0
    weighted_score: float # (raw_score * weight)
    metric_summary: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "weight": self.weight,
            "raw_score": round(self.raw_score, 2),
            "weighted_score": round(self.weighted_score, 2),
            "metric_summary": self.metric_summary,
        }


@dataclass
class QualityScoreReport:
    registry: str
    total_records: int
    overall_score: float
    grade: QualityGrade
    is_release_ready: bool
    structural_gate_passed: bool
    methodology_version: str = "1.0.0"
    assessed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    dimensions: List[ScoreDimension] = field(default_factory=list)
    blocking_issues: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "registry": self.registry,
            "methodology_version": self.methodology_version,
            "assessed_at": self.assessed_at,
            "total_records": self.total_records,
            "overall_score": round(self.overall_score, 2),
            "grade": self.grade.value,
            "is_release_ready": self.is_release_ready,
            "structural_gate_passed": self.structural_gate_passed,
            "dimensions": {d.name: d.to_dict() for d in self.dimensions},
            "blocking_issues": self.blocking_issues,
            "warnings": self.warnings,
        }


class QualityScorer:
    """Calculates standardized, multi-dimensional quality scores across registries."""

    METHODOLOGY_VERSION = "1.0.0"

    DEFAULT_WEIGHTS = {
        "structural_validity": 0.20,
        "identity_integrity": 0.15,
        "url_integrity": 0.10,
        "metadata_completeness": 0.15,
        "evidence_coverage": 0.15,
        "verification_integrity": 0.15,
        "freshness": 0.10,
    }

    def __init__(self, weights: Optional[Dict[str, float]] = None):
        self.weights = weights or self.DEFAULT_WEIGHTS

    @classmethod
    def classify_grade(cls, score: float) -> QualityGrade:
        """Map a numeric score (0-100) to a qualitative operational grade."""
        if score >= 95.0:
            return QualityGrade.EXCELLENT
        elif score >= 85.0:
            return QualityGrade.GOOD
        elif score >= 70.0:
            return QualityGrade.NEEDS_IMPROVEMENT
        elif score >= 50.0:
            return QualityGrade.POOR
        return QualityGrade.CRITICAL

    def calculate_score(
        self,
        registry: str,
        total_records: int,
        structural_valid_pct: float,
        identity_integrity_pct: float,
        url_integrity_pct: float,
        metadata_completeness_pct: float,
        evidence_coverage_pct: float,
        verification_integrity_pct: float,
        freshness_pct: float,
        invalid_record_count: int = 0,
        duplicate_id_count: int = 0
    ) -> QualityScoreReport:
        """Compute the weighted composite score and evaluate structural release gates."""
        blocking_issues: List[str] = []
        warnings: List[str] = []

        # 1. Evaluate Critical Structural Gate
        structural_gate_passed = (invalid_record_count == 0) and (structural_valid_pct == 100.0)
        if not structural_gate_passed:
            blocking_issues.append(
                f"STRUCTURAL GATE FAILED: {invalid_record_count} record(s) violate JSON Schema contracts."
            )

        # 2. Evaluate Identity Gate
        if duplicate_id_count > 0:
            blocking_issues.append(
                f"IDENTITY GATE FAILED: {duplicate_id_count} duplicate identifier(s) detected."
            )

        # 3. Calculate dimension scores
        raw_scores = {
            "structural_validity": (structural_valid_pct if structural_gate_passed else 0.0),
            "identity_integrity": identity_integrity_pct,
            "url_integrity": url_integrity_pct,
            "metadata_completeness": metadata_completeness_pct,
            "evidence_coverage": evidence_coverage_pct,
            "verification_integrity": verification_integrity_pct,
            "freshness": freshness_pct,
        }

        dimensions: List[ScoreDimension] = []
        total_weighted = 0.0

        summaries = {
            "structural_validity": f"{structural_valid_pct:.1f}% records valid ({total_records - invalid_record_count}/{total_records})",
            "identity_integrity": f"{identity_integrity_pct:.1f}% unique identities ({duplicate_id_count} duplicate IDs)",
            "url_integrity": f"{url_integrity_pct:.1f}% valid URLs",
            "metadata_completeness": f"{metadata_completeness_pct:.1f}% completeness index",
            "evidence_coverage": f"{evidence_coverage_pct:.1f}% evidence coverage",
            "verification_integrity": f"{verification_integrity_pct:.1f}% status consistency",
            "freshness": f"{freshness_pct:.1f}% verification freshness index",
        }

        for dim_name, weight in self.weights.items():
            raw = raw_scores.get(dim_name, 0.0)
            weighted = raw * weight
            total_weighted += weighted
            dimensions.append(ScoreDimension(
                name=dim_name,
                weight=weight,
                raw_score=raw,
                weighted_score=weighted,
                metric_summary=summaries.get(dim_name, "")
            ))

        final_score = round(total_weighted, 2)
        grade = self.classify_grade(final_score)

        # Release readiness requirement: No blocking issues and grade is Good or Excellent
        is_release_ready = structural_gate_passed and (len(blocking_issues) == 0) and (final_score >= 85.0)

        return QualityScoreReport(
            registry=registry,
            total_records=total_records,
            overall_score=final_score,
            grade=grade,
            is_release_ready=is_release_ready,
            structural_gate_passed=structural_gate_passed,
            methodology_version=self.METHODOLOGY_VERSION,
            dimensions=dimensions,
            blocking_issues=blocking_issues,
            warnings=warnings,
        )
