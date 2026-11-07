"""
Schema compatibility checker for DevSpire Nexus Registry.
Compares proposed schema revisions against baseline schemas to detect breaking changes.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set


class CompatibilityChangeType(str, Enum):
    BREAKING = "breaking"
    BACKWARD_COMPATIBLE = "backward_compatible"
    INFORMATIONAL = "informational"


@dataclass
class SchemaChange:
    field_name: str
    change_type: CompatibilityChangeType
    description: str
    old_value: Optional[Any] = None
    new_value: Optional[Any] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "field_name": self.field_name,
            "change_type": self.change_type.value,
            "description": self.description,
            "old_value": self.old_value,
            "new_value": self.new_value,
        }


@dataclass
class CompatibilityReport:
    is_backward_compatible: bool = True
    breaking_changes: List[SchemaChange] = field(default_factory=list)
    compatible_changes: List[SchemaChange] = field(default_factory=list)
    informational_changes: List[SchemaChange] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_backward_compatible": self.is_backward_compatible,
            "breaking_count": len(self.breaking_changes),
            "breaking_changes": [c.to_dict() for c in self.breaking_changes],
            "compatible_count": len(self.compatible_changes),
            "compatible_changes": [c.to_dict() for c in self.compatible_changes],
            "informational_count": len(self.informational_changes),
            "informational_changes": [c.to_dict() for c in self.informational_changes],
        }


class CompatibilityChecker:
    """Detects breaking contract modifications between two schema definitions."""

    def compare_schemas(self, old_schema: Dict[str, Any], new_schema: Dict[str, Any]) -> CompatibilityReport:
        """Compare baseline schema against proposed new schema."""
        report = CompatibilityReport()

        old_props = old_schema.get("properties", {})
        new_props = new_schema.get("properties", {})

        old_required = set(old_schema.get("required", []))
        new_required = set(new_schema.get("required", []))

        # 1. Detect removed properties (Breaking)
        for prop_name in old_props:
            if prop_name not in new_props:
                change = SchemaChange(
                    field_name=prop_name,
                    change_type=CompatibilityChangeType.BREAKING,
                    description=f"Property '{prop_name}' was removed from the schema.",
                    old_value=old_props[prop_name]
                )
                report.breaking_changes.append(change)
                report.is_backward_compatible = False

        # 2. Detect added properties
        for prop_name in new_props:
            if prop_name not in old_props:
                if prop_name in new_required:
                    # Newly required property is breaking for existing data
                    change = SchemaChange(
                        field_name=prop_name,
                        change_type=CompatibilityChangeType.BREAKING,
                        description=f"Newly added property '{prop_name}' is marked required.",
                        new_value=new_props[prop_name]
                    )
                    report.breaking_changes.append(change)
                    report.is_backward_compatible = False
                else:
                    change = SchemaChange(
                        field_name=prop_name,
                        change_type=CompatibilityChangeType.BACKWARD_COMPATIBLE,
                        description=f"Optional property '{prop_name}' was added.",
                        new_value=new_props[prop_name]
                    )
                    report.compatible_changes.append(change)

        # 3. Detect newly required existing properties (Breaking)
        for prop_name in new_required - old_required:
            if prop_name in old_props:
                change = SchemaChange(
                    field_name=prop_name,
                    change_type=CompatibilityChangeType.BREAKING,
                    description=f"Previously optional property '{prop_name}' is now required.",
                )
                report.breaking_changes.append(change)
                report.is_backward_compatible = False

        # 4. Check shared property changes (type changes, enum removals)
        for prop_name in old_props:
            if prop_name in new_props:
                old_p = old_props[prop_name]
                new_p = new_props[prop_name]

                # Check type change
                old_type = old_p.get("type")
                new_type = new_p.get("type")
                if old_type and new_type and old_type != new_type:
                    change = SchemaChange(
                        field_name=prop_name,
                        change_type=CompatibilityChangeType.BREAKING,
                        description=f"Property '{prop_name}' changed type from '{old_type}' to '{new_type}'.",
                        old_value=old_type,
                        new_value=new_type
                    )
                    report.breaking_changes.append(change)
                    report.is_backward_compatible = False

                # Check enum removals
                old_enum = set(old_p.get("enum", []))
                new_enum = set(new_p.get("enum", []))
                if old_enum and new_enum:
                    removed_enums = old_enum - new_enum
                    if removed_enums:
                        change = SchemaChange(
                            field_name=prop_name,
                            change_type=CompatibilityChangeType.BREAKING,
                            description=f"Property '{prop_name}' removed allowed enum values: {sorted(removed_enums)}",
                            old_value=list(old_enum),
                            new_value=list(new_enum)
                        )
                        report.breaking_changes.append(change)
                        report.is_backward_compatible = False
                    added_enums = new_enum - old_enum
                    if added_enums:
                        change = SchemaChange(
                            field_name=prop_name,
                            change_type=CompatibilityChangeType.BACKWARD_COMPATIBLE,
                            description=f"Property '{prop_name}' added new allowed enum values: {sorted(added_enums)}",
                            old_value=list(old_enum),
                            new_value=list(new_enum)
                        )
                        report.compatible_changes.append(change)

        return report
