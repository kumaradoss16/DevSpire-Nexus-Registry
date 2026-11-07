"""
Verification status lifecycle engine and audit framework for DevSpire Nexus Registry.
Enforces transition policies, evidence sufficiency, and audit trail consistency.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Set

from .evidence_auditor import EvidenceAuditor, EvidenceArchetype


class VerificationStatus(str, Enum):
    VERIFIED = "verified"
    PARTIALLY_VERIFIED = "partially_verified"
    UNVERIFIED = "unverified"
    DEPRECATED = "deprecated"


@dataclass
class VerificationViolation:
    record_id: str
    registry: str
    current_status: str
    violation_type: str
    message: str
    recommended_status: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "record_id": self.record_id,
            "registry": self.registry,
            "current_status": self.current_status,
            "violation_type": self.violation_type,
            "message": self.message,
            "recommended_status": self.recommended_status,
        }


@dataclass
class VerificationReport:
    registry: str
    total_records: int = 0
    status_counts: Dict[str, int] = field(default_factory=dict)
    violations: List[VerificationViolation] = field(default_factory=list)
    compliant_records: int = 0

    @property
    def integrity_percentage(self) -> float:
        if self.total_records == 0:
            return 100.0
        return round((self.compliant_records / self.total_records) * 100.0, 2)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "registry": self.registry,
            "total_records": self.total_records,
            "compliant_records": self.compliant_records,
            "integrity_percentage": self.integrity_percentage,
            "status_counts": self.status_counts,
            "violation_count": len(self.violations),
            "violations": [v.to_dict() for v in self.violations],
        }


class VerificationEngine:
    """Manages verification status assignments, transitions, and policy compliance."""

    ALLOWED_TRANSITIONS = {
        VerificationStatus.UNVERIFIED: {VerificationStatus.PARTIALLY_VERIFIED, VerificationStatus.VERIFIED, VerificationStatus.DEPRECATED},
        VerificationStatus.PARTIALLY_VERIFIED: {VerificationStatus.VERIFIED, VerificationStatus.UNVERIFIED, VerificationStatus.DEPRECATED},
        VerificationStatus.VERIFIED: {VerificationStatus.PARTIALLY_VERIFIED, VerificationStatus.UNVERIFIED, VerificationStatus.DEPRECATED},
        VerificationStatus.DEPRECATED: {VerificationStatus.UNVERIFIED},  # Permitted reactivation with new review
    }

    def __init__(self, evidence_auditor: Optional[EvidenceAuditor] = None):
        self.evidence_auditor = evidence_auditor or EvidenceAuditor()

    def audit_record_status(self, record: Dict[str, Any], registry: str) -> List[VerificationViolation]:
        """Audit whether a record's assigned status satisfies verification standards."""
        violations: List[VerificationViolation] = []
        rec_id = str(record.get("id", "UNKNOWN"))
        status = record.get("status", "unverified")
        ver_date = record.get("verified")

        ev_audit = self.evidence_auditor.audit_record_evidence(record, registry)

        if status == VerificationStatus.VERIFIED.value:
            # 1. Must have evidence
            if ev_audit.total_links == 0:
                violations.append(VerificationViolation(
                    record_id=rec_id, registry=registry, current_status=status,
                    violation_type="MISSING_EVIDENCE",
                    message="Record is marked 'verified' but has no evidence citations.",
                    recommended_status=VerificationStatus.UNVERIFIED.value
                ))
            # 2. Must have at least one primary source link
            elif ev_audit.primary_links == 0:
                violations.append(VerificationViolation(
                    record_id=rec_id, registry=registry, current_status=status,
                    violation_type="INSUFFICIENT_PRIMARY_EVIDENCE",
                    message="Record contains only secondary/community sources without primary evidence.",
                    recommended_status=VerificationStatus.PARTIALLY_VERIFIED.value
                ))

            # 3. Must have a verification date
            if not ver_date:
                violations.append(VerificationViolation(
                    record_id=rec_id, registry=registry, current_status=status,
                    violation_type="MISSING_VERIFICATION_DATE",
                    message="Record is marked 'verified' but has no verification timestamp.",
                    recommended_status=VerificationStatus.PARTIALLY_VERIFIED.value
                ))

        elif status == VerificationStatus.DEPRECATED.value:
            # Deprecated records should not be presented as actively verified
            pass

        return violations

    def audit_registry(self, records: List[Dict[str, Any]], registry: str) -> VerificationReport:
        """Audit verification status consistency across an entire registry dataset."""
        report = VerificationReport(registry=registry, total_records=len(records))

        for r in records:
            st = str(r.get("status", "unverified"))
            report.status_counts[st] = report.status_counts.get(st, 0) + 1

            violations = self.audit_record_status(r, registry)
            if violations:
                report.violations.extend(violations)
            else:
                report.compliant_records += 1

        return report

    def can_transition(self, current: VerificationStatus, target: VerificationStatus) -> bool:
        """Validate if a proposed status transition conforms to policy."""
        if current == target:
            return True
        return target in self.ALLOWED_TRANSITIONS.get(current, set())
