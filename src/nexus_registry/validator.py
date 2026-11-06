"""
DevSpire Nexus Registry — Validator Engine
Strict offline validation of resource datasets, data contracts, and Quick Start metadata.
Zero network access, zero arbitrary code execution.
"""

import importlib.resources
import json
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from urllib.parse import urlparse

from .client import resolve_datasets_dir


def resolve_schemas_dir(custom_root: Optional[Path] = None) -> Path:
    """Resolve the canonical schemas directory across environments."""
    if custom_root is not None:
        p = Path(custom_root)
        if (p / "schemas").exists() and (p / "schemas" / "common.schema.json").exists():
            return p / "schemas"
        if (p / "common.schema.json").exists():
            return p

    # 1. Local checkout in repo
    local_repo = Path(__file__).resolve().parent.parent.parent / "schemas"
    if local_repo.exists() and (local_repo / "common.schema.json").exists():
        return local_repo

    # 2. Bundled package data
    try:
        pkg_data = Path(str(importlib.resources.files("nexus_registry").joinpath("data", "schemas")))
        if pkg_data.exists() and (pkg_data / "common.schema.json").exists():
            return pkg_data
    except Exception:
        pass

    # 3. Local relative data directory
    local_data = Path(__file__).resolve().parent / "data" / "schemas"
    if local_data.exists() and (local_data / "common.schema.json").exists():
        return local_data

    return local_repo


class Severity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


@dataclass
class ValidationIssue:
    severity: Severity
    registry: str
    resource_id: Optional[str]
    field: Optional[str]
    message: str


@dataclass
class ValidationReport:
    total_records: int = 0
    valid_records: int = 0
    registry_counts: Dict[str, int] = field(default_factory=dict)
    issues: List[ValidationIssue] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return not any(i.severity == Severity.ERROR for i in self.issues)

    @property
    def error_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == Severity.ERROR)

    @property
    def warning_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == Severity.WARNING)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "total_records": self.total_records,
            "valid_records": self.valid_records,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "registry_counts": self.registry_counts,
            "issues": [
                {
                    "severity": i.severity.value,
                    "registry": i.registry,
                    "resource_id": i.resource_id,
                    "field": i.field,
                    "message": i.message
                }
                for i in self.issues
            ]
        }

    def render_text(self) -> str:
        lines = []
        lines.append("==================================================")
        lines.append("       DevSpire Nexus Registry Validation Report   ")
        lines.append("==================================================")
        lines.append(f"Total Resources Checked: {self.total_records}")
        lines.append(f"Registries: {', '.join(f'{k} ({v})' for k, v in self.registry_counts.items())}")
        lines.append(f"Status: {'PASS [OK]' if self.is_valid else 'FAIL [ERRORS DETECTED]'}")
        lines.append(f"Errors: {self.error_count}  |  Warnings: {self.warning_count}")
        lines.append("--------------------------------------------------")

        if not self.issues:
            lines.append("All datasets comply 100% with schema contracts.")
        else:
            for issue in self.issues:
                prefix = f"[{issue.severity.value}] ({issue.registry}"
                if issue.resource_id:
                    prefix += f":{issue.resource_id}"
                prefix += ")"
                if issue.field:
                    prefix += f" Field '{issue.field}':"
                lines.append(f"{prefix} {issue.message}")

        lines.append("==================================================")
        return "\n".join(lines)


class RegistryValidator:
    """Offline schema, integrity, and provenance validator."""

    SLUG_REGEX = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
    DATE_REGEX = re.compile(r"^\d{4}-\d{2}-\d{2}$")

    def __init__(self, root_dir: Optional[Path] = None, repo_root: Optional[Path] = None):
        if root_dir is None:
            root_dir = repo_root
        self.root_dir = Path(root_dir) if root_dir else Path(__file__).resolve().parent.parent.parent
        self.datasets_dir = resolve_datasets_dir(root_dir)
        self.schemas_dir = resolve_schemas_dir(root_dir)

    def validate_url(self, url: str) -> bool:
        if not url or not isinstance(url, str):
            return False
        try:
            parsed = urlparse(url)
            return parsed.scheme in ("http", "https") and bool(parsed.netloc)
        except Exception:
            return False

    def validate_record(self, r: Dict[str, Any], reg_key: str = "ai-tools") -> ValidationReport:
        """Validate a single resource record against schema rules."""
        report = ValidationReport()
        global_ids: Set[str] = set()
        self._validate_record(r, reg_key, global_ids, report)
        return report

    def validate_all(self, registry_filter: Optional[str] = None) -> ValidationReport:
        report = ValidationReport()
        global_ids: Set[str] = set()

        registry_files = {
            "ai-tools": "ai-tools.json",
            "ai-models": "ai-models.json",
            "developer-resources": "developer-resources.json"
        }

        if registry_filter:
            norm_filter = registry_filter.lower().replace("_", "-")
            if norm_filter in registry_files:
                registry_files = {norm_filter: registry_files[norm_filter]}
            else:
                report.issues.append(
                    ValidationIssue(
                        severity=Severity.ERROR,
                        registry="global",
                        resource_id=None,
                        field="registry",
                        message=f"Unknown registry filter '{registry_filter}'. Allowed: {list(registry_files.keys())}"
                    )
                )
                return report

        for reg_key, filename in registry_files.items():
            dataset_path = self.datasets_dir / filename
            if not dataset_path.exists():
                report.issues.append(
                    ValidationIssue(
                        severity=Severity.ERROR,
                        registry=reg_key,
                        resource_id=None,
                        field=None,
                        message=f"Dataset file missing: {dataset_path}"
                    )
                )
                continue

            try:
                with open(dataset_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as e:
                report.issues.append(
                    ValidationIssue(
                        severity=Severity.ERROR,
                        registry=reg_key,
                        resource_id=None,
                        field=None,
                        message=f"Invalid JSON syntax in {filename}: {str(e)}"
                    )
                )
                continue

            records = data.get("records", [])
            report.registry_counts[reg_key] = len(records)
            report.total_records += len(records)

            for rec in records:
                is_record_valid = self._validate_record(rec, reg_key, global_ids, report)
                if is_record_valid:
                    report.valid_records += 1

        return report

    def _validate_record(self, r: Dict[str, Any], reg_key: str, global_ids: Set[str], report: ValidationReport) -> bool:
        rec_id = r.get("id")
        initial_error_count = report.error_count

        # 1. ID Validation
        if not rec_id:
            report.issues.append(ValidationIssue(Severity.ERROR, reg_key, None, "id", "Record is missing required 'id'"))
            return False

        if not isinstance(rec_id, str) or not self.SLUG_REGEX.match(rec_id):
            report.issues.append(ValidationIssue(Severity.ERROR, reg_key, rec_id, "id", f"ID '{rec_id}' does not match slug pattern ^[a-z0-9]+(-[a-z0-9]+)*$"))

        if rec_id in global_ids:
            report.issues.append(ValidationIssue(Severity.ERROR, reg_key, rec_id, "id", f"Duplicate resource ID detected: '{rec_id}'"))
        else:
            global_ids.add(rec_id)

        # 2. Required Common Fields
        required_common = ["name", "description", "category", "official_url", "pricing", "status", "verified", "evidence"]
        for rf in required_common:
            val = r.get(rf)
            if val is None or val == "":
                report.issues.append(ValidationIssue(Severity.ERROR, reg_key, rec_id, rf, f"Missing required field '{rf}'"))

        # 3. URL Syntax
        for uf in ["official_url", "documentation_url", "repository_url", "api_url"]:
            u = r.get(uf)
            if u is not None and not self.validate_url(u):
                report.issues.append(ValidationIssue(Severity.ERROR, reg_key, rec_id, uf, f"Malformed URL: '{u}'"))

        # 4. Verified Timestamp format
        verified_date = r.get("verified")
        if verified_date and not self.DATE_REGEX.match(str(verified_date)):
            report.issues.append(ValidationIssue(Severity.ERROR, reg_key, rec_id, "verified", f"Invalid verification date format: '{verified_date}'. Expected YYYY-MM-DD"))

        # 5. Evidence provenance
        evidence = r.get("evidence")
        if evidence is not None:
            if not isinstance(evidence, list) or len(evidence) == 0:
                report.issues.append(ValidationIssue(Severity.WARNING, reg_key, rec_id, "evidence", "Evidence list is empty. Primary sources required for verified status."))
            else:
                for item in evidence:
                    if not isinstance(item, list) or len(item) != 2:
                        report.issues.append(ValidationIssue(Severity.ERROR, reg_key, rec_id, "evidence", f"Evidence entry must be [label, url] pair: {item}"))
                    elif not self.validate_url(item[1]):
                        report.issues.append(ValidationIssue(Severity.ERROR, reg_key, rec_id, "evidence", f"Evidence URL is invalid: '{item[1]}'"))

        # 6. Domain-specific checks
        if reg_key == "ai-tools":
            if not r.get("org") and not r.get("provider"):
                report.issues.append(ValidationIssue(Severity.ERROR, reg_key, rec_id, "org", "AI Tool missing required developer organization 'org' or 'provider'"))

        elif reg_key == "ai-models":
            for mf in ["publisher", "family", "weights", "modalities"]:
                if not r.get(mf):
                    report.issues.append(ValidationIssue(Severity.ERROR, reg_key, rec_id, mf, f"AI Model missing required field '{mf}'"))

        elif reg_key == "developer-resources":
            if not r.get("resource_subtype"):
                report.issues.append(ValidationIssue(Severity.ERROR, reg_key, rec_id, "resource_subtype", "Developer resource missing 'resource_subtype'"))

            qs = r.get("developer_quick_start")
            if not qs or not isinstance(qs, dict):
                report.issues.append(ValidationIssue(Severity.ERROR, reg_key, rec_id, "developer_quick_start", "Developer resource missing 'developer_quick_start' object"))
            else:
                if "available" not in qs:
                    report.issues.append(ValidationIssue(Severity.ERROR, reg_key, rec_id, "developer_quick_start.available", "Quick start missing 'available' boolean"))
                elif qs["available"]:
                    if not qs.get("package_name"):
                        report.issues.append(ValidationIssue(Severity.WARNING, reg_key, rec_id, "developer_quick_start.package_name", "Verified quick start has no package_name"))
                    if not qs.get("installation") or not isinstance(qs["installation"], list):
                        report.issues.append(ValidationIssue(Severity.ERROR, reg_key, rec_id, "developer_quick_start.installation", "Verified quick start requires installation commands list"))
                    if not qs.get("examples") or not isinstance(qs["examples"], list):
                        report.issues.append(ValidationIssue(Severity.ERROR, reg_key, rec_id, "developer_quick_start.examples", "Verified quick start requires usage examples list"))

        return report.error_count == initial_error_count
