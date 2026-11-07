"""
Metadata completeness and schema field auditor for DevSpire Nexus Registry.
Classifies missing attributes by severity (Critical, High, Medium, Low).
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set


class MetadataSeverity(str, Enum):
    CRITICAL = "critical"  # Prevents identification, routing or validation
    HIGH = "high"          # Materially reduces trust, utility or searchability
    MEDIUM = "medium"      # Useful operational metadata is omitted
    LOW = "low"            # Optional aesthetic or minor enrichment


@dataclass
class MissingFieldFinding:
    registry: str
    record_id: str
    field_name: str
    severity: MetadataSeverity
    reason: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "registry": self.registry,
            "record_id": self.record_id,
            "field_name": self.field_name,
            "severity": self.severity.value,
            "reason": self.reason,
        }


@dataclass
class MetadataCompletenessReport:
    registry: str
    total_records: int = 0
    total_fields_evaluated: int = 0
    missing_critical: int = 0
    missing_high: int = 0
    missing_medium: int = 0
    missing_low: int = 0
    findings: List[MissingFieldFinding] = field(default_factory=list)
    completeness_percentage: float = 100.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "registry": self.registry,
            "total_records": self.total_records,
            "completeness_percentage": round(self.completeness_percentage, 2),
            "missing_critical": self.missing_critical,
            "missing_high": self.missing_high,
            "missing_medium": self.missing_medium,
            "missing_low": self.missing_low,
            "findings_count": len(self.findings),
            "findings": [f.to_dict() for f in self.findings],
        }


class MetadataAuditor:
    """Audits record metadata completeness against registry-specific expectations."""

    COMMON_CRITICAL = {
        "id", "name", "official_url", "category", "resource_type",
        "pricing", "verified", "status", "evidence", "canonical_id"
    }

    COMMON_HIGH = {
        "description", "tags"
    }

    def audit_record(self, record: Dict[str, Any], registry: str) -> List[MissingFieldFinding]:
        """Audit a single record for missing attributes across severity tiers."""
        findings: List[MissingFieldFinding] = []
        rec_id = str(record.get("id", "UNKNOWN"))

        # 1. Critical common fields
        for field in self.COMMON_CRITICAL:
            val = record.get(field)
            if val is None or val == "":
                findings.append(MissingFieldFinding(
                    registry=registry,
                    record_id=rec_id,
                    field_name=field,
                    severity=MetadataSeverity.CRITICAL,
                    reason=f"Mandatory common identity/contract field '{field}' is missing or empty."
                ))

        # 2. High common fields
        for field in self.COMMON_HIGH:
            val = record.get(field)
            if val is None or (isinstance(val, list) and len(val) == 0):
                findings.append(MissingFieldFinding(
                    registry=registry,
                    record_id=rec_id,
                    field_name=field,
                    severity=MetadataSeverity.HIGH,
                    reason=f"Core discovery field '{field}' is missing or empty."
                ))

        # 3. Registry-specific requirements
        if registry == "ai-tools":
            # Medium
            if record.get("pricing_class") is None:
                findings.append(MissingFieldFinding(
                    registry=registry, record_id=rec_id, field_name="pricing_class",
                    severity=MetadataSeverity.MEDIUM, reason="Normalized pricing_class is missing."
                ))
            if record.get("signup_required") is None:
                findings.append(MissingFieldFinding(
                    registry=registry, record_id=rec_id, field_name="signup_required",
                    severity=MetadataSeverity.MEDIUM, reason="signup_required flag is unspecified (null)."
                ))
            # Low
            if record.get("icon") is None:
                findings.append(MissingFieldFinding(
                    registry=registry, record_id=rec_id, field_name="icon",
                    severity=MetadataSeverity.LOW, reason="Resource visual icon is null."
                ))

        elif registry == "ai-models":
            # High
            if not record.get("modalities"):
                findings.append(MissingFieldFinding(
                    registry=registry, record_id=rec_id, field_name="modalities",
                    severity=MetadataSeverity.HIGH, reason="Model input/output modalities list is empty or null."
                ))
            # Medium
            if record.get("open_weights") is None:
                findings.append(MissingFieldFinding(
                    registry=registry, record_id=rec_id, field_name="open_weights",
                    severity=MetadataSeverity.MEDIUM, reason="open_weights boolean flag is unspecified."
                ))
            if record.get("publisher") is None and record.get("provider") is None:
                findings.append(MissingFieldFinding(
                    registry=registry, record_id=rec_id, field_name="publisher",
                    severity=MetadataSeverity.MEDIUM, reason="Model publisher / provider is null."
                ))
            # Low
            if record.get("context_k") is None and record.get("context") is None:
                findings.append(MissingFieldFinding(
                    registry=registry, record_id=rec_id, field_name="context_k",
                    severity=MetadataSeverity.LOW, reason="Quantitative context window token limit is unspecified."
                ))

        elif registry == "developer-resources":
            # High: Open source packages should have a license
            if record.get("open_source") is True and record.get("license") is None:
                findings.append(MissingFieldFinding(
                    registry=registry, record_id=rec_id, field_name="license",
                    severity=MetadataSeverity.HIGH, reason="Resource marked open_source=true but license is null."
                ))
            # Medium: Open source packages should specify repository_url
            if record.get("open_source") is True and record.get("repository_url") is None:
                findings.append(MissingFieldFinding(
                    registry=registry, record_id=rec_id, field_name="repository_url",
                    severity=MetadataSeverity.MEDIUM, reason="Open-source resource lacks top-level repository_url."
                ))
            # Low: Quick start
            if not record.get("developer_quick_start"):
                findings.append(MissingFieldFinding(
                    registry=registry, record_id=rec_id, field_name="developer_quick_start",
                    severity=MetadataSeverity.LOW, reason="Developer quick-start guide is not yet documented."
                ))

        return findings

    def audit_registry(self, records: List[Dict[str, Any]], registry: str) -> MetadataCompletenessReport:
        """Audit an entire registry dataset and calculate completeness percentage."""
        report = MetadataCompletenessReport(registry=registry, total_records=len(records))
        if not records:
            return report

        all_findings = []
        for r in records:
            findings = self.audit_record(r, registry)
            all_findings.extend(findings)
            for f in findings:
                if f.severity == MetadataSeverity.CRITICAL:
                    report.missing_critical += 1
                elif f.severity == MetadataSeverity.HIGH:
                    report.missing_high += 1
                elif f.severity == MetadataSeverity.MEDIUM:
                    report.missing_medium += 1
                elif f.severity == MetadataSeverity.LOW:
                    report.missing_low += 1

        report.findings = all_findings

        # Score calculation: 100 - penalties
        # Critical = -1.0 per record missing, High = -0.2, Medium = -0.05, Low = -0.01
        penalty = (
            (report.missing_critical * 2.0) +
            (report.missing_high * 0.2) +
            (report.missing_medium * 0.05) +
            (report.missing_low * 0.01)
        )
        max_possible = len(records) * 1.0
        score = max(0.0, 100.0 - (penalty / max_possible * 100.0 if max_possible else 0.0))
        report.completeness_percentage = min(100.0, score)

        return report
