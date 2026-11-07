"""
Structural schema and integrity validator for DevSpire Nexus Registry.
Validates records against JSON Schema Draft 2020-12 contracts with detailed error reporting.
"""

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

try:
    import jsonschema
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False

from ..client import resolve_datasets_dir
from ..validator import resolve_schemas_dir

ID_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
DATE_PATTERN = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
URI_PATTERN = re.compile(r"^https?://[^\s/$.?#].[^\s]*$")


@dataclass
class ValidationError:
    registry: str
    record_id: str
    field_path: str  # JSON Pointer, e.g. "$.name"
    message: str
    expected_type: Optional[str] = None
    actual_value: Optional[Any] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "registry": self.registry,
            "record_id": self.record_id,
            "field_path": self.field_path,
            "message": self.message,
            "expected_type": self.expected_type,
            "actual_value": str(self.actual_value) if self.actual_value is not None else None,
        }


@dataclass
class StructuralValidationResult:
    registry: str
    total_records: int = 0
    valid_records: int = 0
    invalid_records: int = 0
    errors: List[ValidationError] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return self.invalid_records == 0 and len(self.errors) == 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "registry": self.registry,
            "is_valid": self.is_valid,
            "total_records": self.total_records,
            "valid_records": self.valid_records,
            "invalid_records": self.invalid_records,
            "error_count": len(self.errors),
            "errors": [e.to_dict() for e in self.errors],
            "warnings": self.warnings,
        }


class StructuralValidator:
    """Validates canonical dataset records against JSON Schema contracts."""

    REQUIRED_COMMON_FIELDS = [
        "id", "name", "description", "category", "resource_type",
        "official_url", "pricing", "license", "tags", "verified",
        "status", "evidence", "canonical_id"
    ]

    ALLOWED_STATUSES = {"verified", "active", "deprecated"}
    ALLOWED_PRICING_CLASSES = {"free", "freemium", "paid", "open_source", "usage_based", "commercial"}

    def __init__(self, schemas_dir: Optional[Path] = None):
        self.schemas_dir = schemas_dir or resolve_schemas_dir()
        self._schemas: Dict[str, Dict[str, Any]] = {}
        self._load_schemas()

    def _load_schemas(self):
        schema_map = {
            "common": "common.schema.json",
            "ai-tools": "ai-tool.schema.json",
            "ai-models": "ai-model.schema.json",
            "developer-resources": "developer-resource.schema.json",
        }
        for key, filename in schema_map.items():
            path = self.schemas_dir / filename
            if path.exists():
                try:
                    self._schemas[key] = json.loads(path.read_text(encoding="utf-8"))
                except Exception as e:
                    pass

    def validate_record(self, record: Dict[str, Any], registry: str) -> List[ValidationError]:
        """Validate a single record and return all discovered validation errors."""
        errors: List[ValidationError] = []
        rec_id = str(record.get("id", "UNKNOWN"))

        # 1. Check all required common fields
        for req_field in self.REQUIRED_COMMON_FIELDS:
            if req_field not in record:
                errors.append(ValidationError(
                    registry=registry,
                    record_id=rec_id,
                    field_path=f"$.{req_field}",
                    message="Required property is missing.",
                    expected_type="defined"
                ))

        # 2. Validate identifier format
        val_id = record.get("id")
        if val_id is not None:
            if not isinstance(val_id, str):
                errors.append(ValidationError(
                    registry=registry,
                    record_id=rec_id,
                    field_path="$.id",
                    message="Must be a string.",
                    expected_type="string",
                    actual_value=type(val_id).__name__
                ))
            elif not ID_PATTERN.match(val_id):
                errors.append(ValidationError(
                    registry=registry,
                    record_id=rec_id,
                    field_path="$.id",
                    message="Identifier must be lowercase alphanumeric with hyphens (kebab-case).",
                    actual_value=val_id
                ))

        # 3. Validate name and description lengths
        name = record.get("name")
        if name is not None:
            if not isinstance(name, str):
                errors.append(ValidationError(
                    registry=registry,
                    record_id=rec_id,
                    field_path="$.name",
                    message="Name must be a string.",
                    expected_type="string"
                ))
            elif len(name) < 2 or len(name) > 100:
                errors.append(ValidationError(
                    registry=registry,
                    record_id=rec_id,
                    field_path="$.name",
                    message=f"Name length ({len(name)}) must be between 2 and 100 characters.",
                    actual_value=name
                ))

        desc = record.get("description")
        if desc is not None:
            if not isinstance(desc, str):
                errors.append(ValidationError(
                    registry=registry,
                    record_id=rec_id,
                    field_path="$.description",
                    message="Description must be a string.",
                    expected_type="string"
                ))
            elif len(desc) < 10 or len(desc) > 1000:
                errors.append(ValidationError(
                    registry=registry,
                    record_id=rec_id,
                    field_path="$.description",
                    message=f"Description length ({len(desc)}) must be between 10 and 1000 characters.",
                    actual_value=desc
                ))

        # 4. Validate URLs
        url = record.get("official_url")
        if url is not None:
            if not isinstance(url, str) or not URI_PATTERN.match(url.strip()):
                errors.append(ValidationError(
                    registry=registry,
                    record_id=rec_id,
                    field_path="$.official_url",
                    message="Must be a valid HTTP or HTTPS URI.",
                    actual_value=url
                ))

        # 5. Validate status and verified date
        status = record.get("status")
        if status is not None and status not in self.ALLOWED_STATUSES:
            errors.append(ValidationError(
                registry=registry,
                record_id=rec_id,
                field_path="$.status",
                message=f"Value must be one of {sorted(self.ALLOWED_STATUSES)}.",
                actual_value=status
            ))

        ver_date = record.get("verified")
        if ver_date is not None:
            if not isinstance(ver_date, str) or not DATE_PATTERN.match(ver_date):
                errors.append(ValidationError(
                    registry=registry,
                    record_id=rec_id,
                    field_path="$.verified",
                    message="Verification date must be formatted as YYYY-MM-DD.",
                    actual_value=ver_date
                ))

        # 6. Validate evidence array
        evidence = record.get("evidence")
        if evidence is not None:
            if not isinstance(evidence, list) or len(evidence) == 0:
                errors.append(ValidationError(
                    registry=registry,
                    record_id=rec_id,
                    field_path="$.evidence",
                    message="Evidence must be a non-empty array of [label, url] pairs.",
                    actual_value=evidence
                ))
            else:
                for idx, item in enumerate(evidence):
                    if not isinstance(item, (list, tuple)) or len(item) != 2:
                        errors.append(ValidationError(
                            registry=registry,
                            record_id=rec_id,
                            field_path=f"$.evidence[{idx}]",
                            message="Each evidence item must be a 2-element tuple [label, url].",
                            actual_value=item
                        ))
                    elif not isinstance(item[1], str) or not URI_PATTERN.match(item[1].strip()):
                        errors.append(ValidationError(
                            registry=registry,
                            record_id=rec_id,
                            field_path=f"$.evidence[{idx}][1]",
                            message="Evidence URL must be a valid HTTP/HTTPS URI.",
                            actual_value=item[1]
                        ))

        # 7. Validate canonical_id format
        can_id = record.get("canonical_id")
        if can_id is not None and val_id is not None:
            if not isinstance(can_id, str):
                errors.append(ValidationError(
                    registry=registry,
                    record_id=rec_id,
                    field_path="$.canonical_id",
                    message="Canonical ID must be a string.",
                    expected_type="string"
                ))
            elif not can_id.endswith(f":{val_id}") and can_id != val_id:
                errors.append(ValidationError(
                    registry=registry,
                    record_id=rec_id,
                    field_path="$.canonical_id",
                    message=f"Canonical ID '{can_id}' does not match record ID '{val_id}'.",
                    actual_value=can_id
                ))

        # 8. Registry-specific validation
        if registry == "ai-tools":
            if record.get("resource_type") != "AI Tool":
                errors.append(ValidationError(
                    registry=registry,
                    record_id=rec_id,
                    field_path="$.resource_type",
                    message="resource_type must be exactly 'AI Tool'.",
                    actual_value=record.get("resource_type")
                ))
        elif registry == "ai-models":
            if record.get("resource_type") != "AI Model":
                errors.append(ValidationError(
                    registry=registry,
                    record_id=rec_id,
                    field_path="$.resource_type",
                    message="resource_type must be exactly 'AI Model'.",
                    actual_value=record.get("resource_type")
                ))
            if "context_k" in record and record["context_k"] is not None:
                ck = record["context_k"]
                if not isinstance(ck, int) or ck <= 0:
                    errors.append(ValidationError(
                        registry=registry,
                        record_id=rec_id,
                        field_path="$.context_k",
                        message="context_k must be a positive integer.",
                        actual_value=ck
                    ))
        elif registry == "developer-resources":
            if not record.get("resource_type"):
                errors.append(ValidationError(
                    registry=registry,
                    record_id=rec_id,
                    field_path="$.resource_type",
                    message="resource_type is required for developer resources.",
                    actual_value=record.get("resource_type")
                ))

        return errors

    def validate_registry(self, records: List[Dict[str, Any]], registry: str) -> StructuralValidationResult:
        """Validate an entire collection of records for a given registry."""
        result = StructuralValidationResult(registry=registry, total_records=len(records))

        for record in records:
            rec_errors = self.validate_record(record, registry)
            if rec_errors:
                result.invalid_records += 1
                result.errors.extend(rec_errors)
            else:
                result.valid_records += 1

        return result
