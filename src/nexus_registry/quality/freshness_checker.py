"""
Metadata and verification freshness checker for DevSpire Nexus Registry.
Tracks verification age against review policies and flags stale or aging records.
"""

from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


class FreshnessCategory(str, Enum):
    FRESH = "fresh"      # <= 90 days
    CURRENT = "current"  # 91 to 180 days
    AGING = "aging"      # 181 to 365 days
    STALE = "stale"      # > 365 days
    UNKNOWN = "unknown"  # unparseable or missing date


@dataclass
class RecordFreshnessFinding:
    record_id: str
    registry: str
    verified_date_str: str
    age_days: Optional[int]
    category: FreshnessCategory
    is_stale: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "record_id": self.record_id,
            "registry": self.registry,
            "verified_date": self.verified_date_str,
            "age_days": self.age_days,
            "category": self.category.value,
            "is_stale": self.is_stale,
        }


@dataclass
class FreshnessReport:
    registry: str
    total_records: int = 0
    fresh_count: int = 0
    current_count: int = 0
    aging_count: int = 0
    stale_count: int = 0
    unknown_count: int = 0
    freshness_percentage: float = 100.0
    findings: List[RecordFreshnessFinding] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "registry": self.registry,
            "total_records": self.total_records,
            "freshness_percentage": round(self.freshness_percentage, 2),
            "fresh_count": self.fresh_count,
            "current_count": self.current_count,
            "aging_count": self.aging_count,
            "stale_count": self.stale_count,
            "unknown_count": self.unknown_count,
            "stale_records": [f.record_id for f in self.findings if f.is_stale],
        }


class FreshnessChecker:
    """Evaluates record verification age against configured freshness thresholds."""

    FAST_MOVING_DAYS = 90
    STANDARD_DAYS = 180
    STALE_THRESHOLD_DAYS = 365

    def __init__(self, reference_date: Optional[date] = None):
        # Default to reference date or today
        self.reference_date = reference_date or date.today()

    def audit_record_freshness(self, record: Dict[str, Any], registry: str) -> RecordFreshnessFinding:
        """Audit the verification date age of a single record."""
        rec_id = str(record.get("id", "UNKNOWN"))
        raw_date = record.get("verified")

        if not raw_date or not isinstance(raw_date, str):
            return RecordFreshnessFinding(
                record_id=rec_id, registry=registry, verified_date_str="NONE",
                age_days=None, category=FreshnessCategory.UNKNOWN, is_stale=True
            )

        try:
            ver_d = datetime.strptime(raw_date.strip(), "%Y-%m-%d").date()
            age_days = (self.reference_date - ver_d).days
            # Guard against future dates
            if age_days < 0:
                age_days = 0

            if age_days <= self.FAST_MOVING_DAYS:
                cat = FreshnessCategory.FRESH
            elif age_days <= self.STANDARD_DAYS:
                cat = FreshnessCategory.CURRENT
            elif age_days <= self.STALE_THRESHOLD_DAYS:
                cat = FreshnessCategory.AGING
            else:
                cat = FreshnessCategory.STALE

            return RecordFreshnessFinding(
                record_id=rec_id,
                registry=registry,
                verified_date_str=raw_date,
                age_days=age_days,
                category=cat,
                is_stale=(cat == FreshnessCategory.STALE)
            )
        except Exception:
            return RecordFreshnessFinding(
                record_id=rec_id, registry=registry, verified_date_str=raw_date,
                age_days=None, category=FreshnessCategory.UNKNOWN, is_stale=True
            )

    def audit_registry(self, records: List[Dict[str, Any]], registry: str) -> FreshnessReport:
        """Audit freshness across an entire registry dataset."""
        report = FreshnessReport(registry=registry, total_records=len(records))

        for r in records:
            finding = self.audit_record_freshness(r, registry)
            report.findings.append(finding)

            if finding.category == FreshnessCategory.FRESH:
                report.fresh_count += 1
            elif finding.category == FreshnessCategory.CURRENT:
                report.current_count += 1
            elif finding.category == FreshnessCategory.AGING:
                report.aging_count += 1
            elif finding.category == FreshnessCategory.STALE:
                report.stale_count += 1
            else:
                report.unknown_count += 1

        if report.total_records > 0:
            # Score formula: (Fresh*1.0 + Current*0.9 + Aging*0.6 + Stale*0.0) / total * 100
            weighted_points = (
                (report.fresh_count * 1.0) +
                (report.current_count * 0.9) +
                (report.aging_count * 0.6)
            )
            report.freshness_percentage = round((weighted_points / report.total_records) * 100.0, 2)

        return report
