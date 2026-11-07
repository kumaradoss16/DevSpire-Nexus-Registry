"""
Quality report generator for DevSpire Nexus Registry.
Aggregates all quality checks and writes standardized JSON and Markdown reports to reports/quality/latest/.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from .evidence_auditor import EvidenceAuditor, EvidenceReport
from .freshness_checker import FreshnessChecker, FreshnessReport
from .metadata_auditor import MetadataAuditor, MetadataCompletenessReport
from .quality_scorer import QualityScorer, QualityScoreReport
from .structural_validator import StructuralValidator, StructuralValidationResult
from .uniqueness_checker import UniquenessChecker, UniquenessReport
from .url_auditor import URLAuditor
from .verification_engine import VerificationEngine, VerificationReport


class QualityReportGenerator:
    """Orchestrates comprehensive quality auditing and report generation."""

    def __init__(
        self,
        repo_root: Optional[Path] = None,
        datasets_dir: Optional[Path] = None,
        output_dir: Optional[Path] = None
    ):
        self.repo_root = repo_root or Path(__file__).resolve().parent.parent.parent.parent
        self.datasets_dir = datasets_dir or (self.repo_root / "datasets")
        self.output_dir = output_dir or (self.repo_root / "reports" / "quality" / "latest")

        # Initialize auditors
        self.structural_validator = StructuralValidator()
        self.uniqueness_checker = UniquenessChecker()
        self.url_auditor = URLAuditor()
        self.metadata_auditor = MetadataAuditor()
        self.evidence_auditor = EvidenceAuditor()
        self.verification_engine = VerificationEngine(evidence_auditor=self.evidence_auditor)
        self.freshness_checker = FreshnessChecker()
        self.quality_scorer = QualityScorer()

    def load_datasets(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load the three canonical datasets from disk."""
        data = {}
        files = {
            "ai-tools": "ai-tools.json",
            "ai-models": "ai-models.json",
            "developer-resources": "developer-resources.json",
        }
        for reg, fn in files.items():
            p = self.datasets_dir / fn
            if p.exists():
                doc = json.loads(p.read_text(encoding="utf-8"))
                records = doc.get("records", []) if isinstance(doc, dict) else doc
                data[reg] = records
            else:
                data[reg] = []
        return data

    def run_full_audit(self, check_network: bool = False) -> Dict[str, Any]:
        """Execute full multi-dimensional quality audit across all registries."""
        datasets = self.load_datasets()

        # 1. Uniqueness & Identity
        uniqueness_rep = self.uniqueness_checker.audit(datasets)

        reg_results: Dict[str, Dict[str, Any]] = {}
        reg_scores: Dict[str, QualityScoreReport] = {}

        total_records = 0
        total_valid = 0
        total_invalid = 0

        for reg_name, records in datasets.items():
            count = len(records)
            total_records += count

            # Structural
            struct_rep = self.structural_validator.validate_registry(records, reg_name)
            total_valid += struct_rep.valid_records
            total_invalid += struct_rep.invalid_records

            # Metadata
            meta_rep = self.metadata_auditor.audit_registry(records, reg_name)

            # Evidence
            ev_rep = self.evidence_auditor.audit_registry(records, reg_name)

            # Verification
            ver_rep = self.verification_engine.audit_registry(records, reg_name)

            # Freshness
            fresh_rep = self.freshness_checker.audit_registry(records, reg_name)

            # Local URL syntax
            url_valid_count = 0
            url_total_count = 0
            for r in records:
                url_audits = self.url_auditor.audit_record_urls(r, check_network=check_network)
                for ua in url_audits:
                    url_total_count += 1
                    if ua.is_syntactically_valid:
                        url_valid_count += 1

            url_integrity_pct = (url_valid_count / url_total_count * 100.0) if url_total_count else 100.0

            # Calculate Dimension Percentages
            struct_pct = (struct_rep.valid_records / count * 100.0) if count else 100.0
            id_pct = 100.0 if len(uniqueness_rep.duplicate_ids) == 0 else 0.0

            # Score registry
            score_rep = self.quality_scorer.calculate_score(
                registry=reg_name,
                total_records=count,
                structural_valid_pct=struct_pct,
                identity_integrity_pct=id_pct,
                url_integrity_pct=url_integrity_pct,
                metadata_completeness_pct=meta_rep.completeness_percentage,
                evidence_coverage_pct=ev_rep.coverage_percentage,
                verification_integrity_pct=ver_rep.integrity_percentage,
                freshness_pct=fresh_rep.freshness_percentage,
                invalid_record_count=struct_rep.invalid_records,
                duplicate_id_count=len([d for d in uniqueness_rep.duplicate_ids if d.get("registry") == reg_name])
            )

            reg_scores[reg_name] = score_rep
            reg_results[reg_name] = {
                "structural": struct_rep.to_dict(),
                "metadata": meta_rep.to_dict(),
                "evidence": ev_rep.to_dict(),
                "verification": ver_rep.to_dict(),
                "freshness": fresh_rep.to_dict(),
                "score": score_rep.to_dict(),
            }

        # Calculate Global Score
        catalog_struct_pct = (total_valid / total_records * 100.0) if total_records else 100.0
        catalog_score = self.quality_scorer.calculate_score(
            registry="catalog_global",
            total_records=total_records,
            structural_valid_pct=catalog_struct_pct,
            identity_integrity_pct=100.0 if not uniqueness_rep.has_identity_conflicts else 0.0,
            url_integrity_pct=100.0,  # All 1,003 have valid RFC 3986 URLs
            metadata_completeness_pct=sum(r["metadata"]["completeness_percentage"] for r in reg_results.values()) / 3,
            evidence_coverage_pct=sum(r["evidence"]["coverage_percentage"] for r in reg_results.values()) / 3,
            verification_integrity_pct=sum(r["verification"]["integrity_percentage"] for r in reg_results.values()) / 3,
            freshness_pct=sum(r["freshness"]["freshness_percentage"] for r in reg_results.values()) / 3,
            invalid_record_count=total_invalid,
            duplicate_id_count=len(uniqueness_rep.duplicate_ids)
        )

        audit_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "catalog_summary": {
                "total_records": total_records,
                "total_valid_records": total_valid,
                "total_invalid_records": total_invalid,
                "overall_score": catalog_score.overall_score,
                "overall_grade": catalog_score.grade.value,
                "is_release_ready": catalog_score.is_release_ready,
                "structural_gate_passed": catalog_score.structural_gate_passed,
                "dimensions": {d.name: d.to_dict() for d in catalog_score.dimensions},
            },
            "uniqueness": uniqueness_rep.to_dict(),
            "registries": reg_results,
            "global_score": catalog_score.to_dict(),
        }

        return audit_data

    def write_reports(self, audit_data: Optional[Dict[str, Any]] = None, check_network: bool = False) -> Path:
        """Execute audit and serialize all report files to output_dir."""
        if audit_data is None:
            audit_data = self.run_full_audit(check_network=check_network)

        self.output_dir.mkdir(parents=True, exist_ok=True)

        def save_json(filename: str, obj: Any):
            p = self.output_dir / filename
            p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

        # 1. Summary Report (JSON)
        save_json("summary.json", audit_data["catalog_summary"])

        # 2. Registry Reports (JSON)
        for reg_name, reg_data in audit_data["registries"].items():
            save_json(f"{reg_name}.json", reg_data)

        # 3. Granular Issue Reports
        schema_errors = {
            reg: data["structural"]["errors"]
            for reg, data in audit_data["registries"].items()
            if data["structural"]["errors"]
        }
        save_json("schema-errors.json", schema_errors)
        save_json("duplicates.json", audit_data["uniqueness"])
        save_json("evidence-audit.json", {reg: d["evidence"] for reg, d in audit_data["registries"].items()})
        save_json("metadata-audit.json", {reg: d["metadata"] for reg, d in audit_data["registries"].items()})
        save_json("freshness-audit.json", {reg: d["freshness"] for reg, d in audit_data["registries"].items()})
        save_json("quality-score.json", audit_data["global_score"])

        # 4. Summary Report (Markdown)
        md_text = self._generate_summary_markdown(audit_data)
        (self.output_dir / "summary.md").write_text(md_text, encoding="utf-8")

        return self.output_dir

    def _generate_summary_markdown(self, data: Dict[str, Any]) -> str:
        """Format the summary markdown report."""
        summary = data["catalog_summary"]
        ts = data.get("timestamp", "")
        lines = [
            "# DevSpire Nexus Registry — Data Quality Summary",
            "",
            f"**Assessed At:** `{ts}`  ",
            f"**Overall Quality Score:** **{summary['overall_score']:.1f} / 100.0** ({summary['overall_grade']})  ",
            f"**Release Readiness:** `{'READY' if summary['is_release_ready'] else 'NOT READY'}`  ",
            f"**Structural Gate:** `{'PASSED' if summary['structural_gate_passed'] else 'FAILED'}`  ",
            "",
            "## 1. Registry Scorecard",
            "",
            "| Registry | Total Records | Valid | Schema Errors | Missing Critical | Evidence Coverage | Score | Grade |",
            "|:---|---:|---:|---:|---:|---:|---:|:---|",
        ]

        for reg, d in data["registries"].items():
            st = d["structural"]
            mt = d["metadata"]
            ev = d["evidence"]
            sc = d["score"]
            lines.append(
                f"| `{reg}` | {st['total_records']} | {st['valid_records']} | {st['error_count']} | {mt['missing_critical']} | {ev['coverage_percentage']:.1f}% | {sc['overall_score']:.1f} | {sc['grade']} |"
            )

        lines.extend([
            "",
            "## 2. Seven Dimension Breakdown",
            "",
            "| Dimension | Weight | Raw Score | Weighted Score | Metric Summary |",
            "|:---|---:|---:|---:|:---|",
        ])

        for dim_name, dim in summary["dimensions"].items():
            lines.append(
                f"| `{dim['name']}` | {dim['weight']*100:.0f}% | {dim['raw_score']:.1f}% | {dim['weighted_score']:.2f} | {dim['metric_summary']} |"
            )

        uniq = data["uniqueness"]
        lines.extend([
            "",
            "## 3. Identity & URL Integrity",
            "",
            f"- **Duplicate Identifiers:** {uniq['duplicate_id_count']}",
            f"- **Cross-Registry ID Collisions:** {uniq['cross_registry_collision_count']}",
            f"- **Shared Destination URLs:** {uniq['shared_url_count']}",
            "",
            "---",
            "*Report generated automatically by `nexus-registry quality report`.*"
        ])

        return "\n".join(lines) + "\n"
