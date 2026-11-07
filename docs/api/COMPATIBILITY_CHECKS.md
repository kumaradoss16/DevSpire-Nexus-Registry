# DevSpire Nexus Registry — Automated Compatibility Checks

**Specification Version:** 1.0.0  
**Effective Date:** 2026-11-07  
**Module:** `nexus_registry.quality.compatibility_checker`  
**Scope:** Automated detection of schema regressions, breaking field changes, and API drift.

---

## 1. Overview

To prevent accidental regressions for external applications consuming the DevSpire Nexus Registry, the test suite and CI pipeline include an automated **Compatibility Checker** (`CompatibilityChecker`).

The engine compares a proposed or updated schema against a committed baseline schema and categorizes every detected change:

| Classification | Definition | CI Gate Action | Example |
|:---|:---|:---:|:---|
| **BREAKING** | Any change that could cause existing valid data or consumers to fail. | **BLOCKED** | Removing a property, changing field type, removing an enum option, making an optional field required. |
| **BACKWARD_COMPATIBLE** | Safe additions that preserve existing consumer behavior. | **ALLOWED** | Adding an optional field, adding a new enum option. |
| **INFORMATIONAL** | Non-structural metadata changes. | **ALLOWED** | Updating schema descriptions or titles. |

---

## 2. Automated Compatibility Rules

1. **Property Removals:** Flagged as breaking. Existing clients depending on the field would receive undefined/null.
2. **Type Mutations:** Flagged as breaking (e.g. changing `context_k` from integer to string).
3. **Required Constraints:** Adding an existing property to the `required` array is breaking because historical records lacking the field become invalid.
4. **Enum Contractions:** Removing any allowed string from an `enum` is breaking.

---

## 3. Running Compatibility Checks Locally

```python
from nexus_registry.quality import CompatibilityChecker

checker = CompatibilityChecker()
report = checker.compare_schemas(old_schema, new_schema)

if not report.is_backward_compatible:
    print(f"Detected {len(report.breaking_changes)} breaking change(s)!")
    for change in report.breaking_changes:
        print(f"  • {change.field_name}: {change.description}")
```
