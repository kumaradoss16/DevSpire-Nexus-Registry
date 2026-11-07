# DevSpire Nexus Registry — Quality Report Guide

**Guide Version:** 1.0.0  
**Effective Date:** 2026-11-07  
**Scope:** Understanding, interpreting, and generating quality report artifacts in `reports/quality/latest/`.

---

## 1. Directory Structure

Running `nexus-registry quality report` generates eleven standardized report files:

```
reports/quality/latest/
├── summary.json              # High-level metrics, release readiness, and gate status
├── summary.md                # Human-readable markdown table of scores and dimensions
├── ai-tools.json             # AI Tools registry quality results
├── ai-models.json            # AI Models registry quality results
├── developer-resources.json  # Developer Resources registry quality results
├── schema-errors.json        # Granular schema errors with JSON Pointer paths
├── duplicates.json           # Duplicate IDs, cross-collisions, and shared URLs
├── evidence-audit.json       # Evidence archetypes and coverage breakdowns
├── metadata-audit.json       # Completeness by severity (Critical, High, Medium, Low)
├── freshness-audit.json      # Verification age distribution and stale records
└── quality-score.json        # 7-dimension mathematical score report
```

---

## 2. Interpreting Key Reports

### 2.1 `summary.json`
Contains top-level indicators:
```json
{
  "total_records": 1003,
  "total_valid_records": 1003,
  "total_invalid_records": 0,
  "overall_score": 99.24,
  "overall_grade": "Excellent",
  "is_release_ready": true,
  "structural_gate_passed": true
}
```

### 2.2 `duplicates.json`
Separates shared legitimate URLs (vendor sites or monorepos) from probable duplicates (candidate variant slugs for review).

---

## 3. CLI Commands for Report Generation

```bash
# Generate full report suite locally
nexus-registry quality report

# Include optional live network health probes
nexus-registry quality report --network
```
