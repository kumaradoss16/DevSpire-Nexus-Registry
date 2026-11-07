"""
Evidence source classifier and provenance auditor for DevSpire Nexus Registry.
Classifies external references into canonical archetypes and evaluates primary source sufficiency.
"""

import urllib.parse
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple


class EvidenceArchetype(str, Enum):
    OFFICIAL_WEBSITE = "official_website"
    OFFICIAL_DOCUMENTATION = "official_documentation"
    SOURCE_REPOSITORY = "source_repository"
    PACKAGE_REGISTRY = "package_registry"
    MODEL_CARD = "model_card"
    ANNOUNCEMENT = "announcement"
    RESEARCH_PAPER = "research_paper"
    SECONDARY_SOURCE = "secondary_source"
    COMMUNITY_SOURCE = "community_source"
    UNKNOWN = "unknown"


@dataclass
class ClassifiedEvidence:
    label: str
    url: str
    archetype: EvidenceArchetype
    is_primary: bool
    domain: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "label": self.label,
            "url": self.url,
            "archetype": self.archetype.value,
            "is_primary": self.is_primary,
            "domain": self.domain,
        }


@dataclass
class RecordEvidenceAudit:
    record_id: str
    registry: str
    total_links: int
    primary_links: int
    secondary_links: int
    archetypes: List[EvidenceArchetype]
    is_sufficient_for_verification: bool
    evidence_items: List[ClassifiedEvidence]
    issues: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "record_id": self.record_id,
            "registry": self.registry,
            "total_links": self.total_links,
            "primary_links": self.primary_links,
            "secondary_links": self.secondary_links,
            "archetypes": [a.value for a in self.archetypes],
            "is_sufficient_for_verification": self.is_sufficient_for_verification,
            "evidence_items": [e.to_dict() for e in self.evidence_items],
            "issues": self.issues,
        }


@dataclass
class EvidenceReport:
    registry: str
    total_records: int = 0
    records_with_evidence: int = 0
    records_with_zero_evidence: int = 0
    records_with_primary_evidence: int = 0
    archetype_distribution: Dict[str, int] = field(default_factory=dict)
    insufficient_evidence_records: List[str] = field(default_factory=list)
    record_audits: List[RecordEvidenceAudit] = field(default_factory=list)

    @property
    def coverage_percentage(self) -> float:
        if self.total_records == 0:
            return 100.0
        return round((self.records_with_evidence / self.total_records) * 100.0, 2)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "registry": self.registry,
            "total_records": self.total_records,
            "records_with_evidence": self.records_with_evidence,
            "records_with_zero_evidence": self.records_with_zero_evidence,
            "records_with_primary_evidence": self.records_with_primary_evidence,
            "coverage_percentage": self.coverage_percentage,
            "archetype_distribution": self.archetype_distribution,
            "insufficient_evidence_count": len(self.insufficient_evidence_records),
            "insufficient_evidence_records": self.insufficient_evidence_records,
        }


class EvidenceAuditor:
    """Classifies external evidence and checks whether claims are traceable to primary sources."""

    PRIMARY_ARCHETYPES = {
        EvidenceArchetype.OFFICIAL_WEBSITE,
        EvidenceArchetype.OFFICIAL_DOCUMENTATION,
        EvidenceArchetype.SOURCE_REPOSITORY,
        EvidenceArchetype.PACKAGE_REGISTRY,
        EvidenceArchetype.MODEL_CARD,
        EvidenceArchetype.ANNOUNCEMENT,
        EvidenceArchetype.RESEARCH_PAPER,
    }

    @classmethod
    def classify_source(cls, label: str, url: str) -> Tuple[EvidenceArchetype, bool, str]:
        """Classify an evidence link into an archetype and primary/secondary flag."""
        domain = ""
        try:
            domain = urllib.parse.urlparse(url).netloc.lower()
        except Exception:
            pass

        label_lower = (label or "").lower()
        url_lower = (url or "").lower()

        # 1. Model Card
        if "huggingface.co" in domain or "civitai.com" in domain or "model card" in label_lower:
            return EvidenceArchetype.MODEL_CARD, True, domain

        # 2. Source Repository
        if "github.com" in domain or "gitlab.com" in domain or "codeberg.org" in domain:
            return EvidenceArchetype.SOURCE_REPOSITORY, True, domain

        # 3. Package Registry
        if any(p in domain for p in ["pypi.org", "npmjs.com", "crates.io", "pkg.go.dev", "packagist.org"]):
            return EvidenceArchetype.PACKAGE_REGISTRY, True, domain

        # 4. Research Paper
        if "arxiv.org" in domain or "openreview.net" in domain or "biorxiv.org" in domain or "paper" in label_lower:
            return EvidenceArchetype.RESEARCH_PAPER, True, domain

        # 5. Documentation
        if (
            "docs." in domain or "platform.openai.com/docs" in url_lower or
            "/docs" in url_lower or "documentation" in label_lower or
            "readthedocs.io" in domain or "gitbook.io" in domain or
            "developers." in domain or "developer." in domain
        ):
            return EvidenceArchetype.OFFICIAL_DOCUMENTATION, True, domain

        # 6. Official Announcement
        if "/blog" in url_lower or "/news" in url_lower or "announcement" in label_lower or "release" in label_lower:
            return EvidenceArchetype.ANNOUNCEMENT, True, domain

        # 7. Community Source
        if any(c in domain for c in ["reddit.com", "news.ycombinator.com", "discord.gg", "x.com", "twitter.com"]):
            return EvidenceArchetype.COMMUNITY_SOURCE, False, domain

        # 8. Official Website / Portal (default primary for publisher domains)
        if label_lower in ("official website", "website", "verified link", "home") or domain:
            return EvidenceArchetype.OFFICIAL_WEBSITE, True, domain

        return EvidenceArchetype.UNKNOWN, False, domain

    def audit_record_evidence(self, record: Dict[str, Any], registry: str) -> RecordEvidenceAudit:
        """Audit the evidence links for a single record."""
        rec_id = str(record.get("id", "UNKNOWN"))
        raw_evidence = record.get("evidence", [])
        classified_items: List[ClassifiedEvidence] = []
        archetypes: List[EvidenceArchetype] = []
        issues: List[str] = []

        primary_count = 0
        secondary_count = 0

        if not isinstance(raw_evidence, list) or len(raw_evidence) == 0:
            issues.append("Record contains no evidence citations.")
        else:
            for item in raw_evidence:
                if isinstance(item, (list, tuple)) and len(item) == 2:
                    lbl, link = str(item[0]), str(item[1])
                    arch, is_prim, dom = self.classify_source(lbl, link)
                    classified = ClassifiedEvidence(
                        label=lbl, url=link, archetype=arch, is_primary=is_prim, domain=dom
                    )
                    classified_items.append(classified)
                    archetypes.append(arch)
                    if is_prim:
                        primary_count += 1
                    else:
                        secondary_count += 1
                else:
                    issues.append(f"Malformed evidence tuple: {item}")

        # Verification sufficiency requirement: At least 1 primary source citation
        is_sufficient = (primary_count >= 1) and (len(issues) == 0)
        if not is_sufficient and record.get("status") == "verified":
            issues.append("Record is marked 'verified' but lacks at least one primary source citation.")

        return RecordEvidenceAudit(
            record_id=rec_id,
            registry=registry,
            total_links=len(classified_items),
            primary_links=primary_count,
            secondary_links=secondary_count,
            archetypes=archetypes,
            is_sufficient_for_verification=is_sufficient,
            evidence_items=classified_items,
            issues=issues,
        )

    def audit_registry(self, records: List[Dict[str, Any]], registry: str) -> EvidenceReport:
        """Audit all evidence across an entire registry dataset."""
        report = EvidenceReport(registry=registry, total_records=len(records))

        for r in records:
            audit = self.audit_record_evidence(r, registry)
            report.record_audits.append(audit)

            if audit.total_links > 0:
                report.records_with_evidence += 1
            else:
                report.records_with_zero_evidence += 1

            if audit.primary_links > 0:
                report.records_with_primary_evidence += 1

            for arch in audit.archetypes:
                val = arch.value
                report.archetype_distribution[val] = report.archetype_distribution.get(val, 0) + 1

            if not audit.is_sufficient_for_verification:
                report.insufficient_evidence_records.append(audit.record_id)

        return report
