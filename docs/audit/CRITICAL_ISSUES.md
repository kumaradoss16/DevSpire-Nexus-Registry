# DevSpire Nexus Registry — Master Critical Issues Register

**Audit Date:** 2026-11-07  
**Auditor:** DevSpire Nexus Audit & Remediation Specialist Team  
**Scope:** Consolidated register of all identified weaknesses, operational gaps, and architectural issues.  

---

## 1. Master Issue Register

| ID | Area | Finding / Weakness | Severity | Evidence | Impact | Recommended Remediation |
|:---|:---|:---|:---|:---|:---|:---|
| **AUD-001** | **SDK Distribution** | Standalone wheel distribution previously omitted canonical datasets. *(Resolved in Phase 1; monitored)* | **High** *(Remediated)* | `pyproject.toml`, `src/nexus_registry/data/` | External `pip install` users could not access records without cloning git repo. | Maintain embedded package data in `src/nexus_registry/data/` and verify in CI. |
| **AUD-002** | **CI/CD Security** | `.github/workflows/link-check.yml` lacks explicit least-privilege permissions and uses unpinned dependency. | **Medium** | `.github/workflows/link-check.yml:18` (`pip install requests`) | Workflow runs with ambient GitHub token permissions; susceptible to unpinned dependency breakages. | Add `permissions: contents: read` and pin `pip install requests==2.32.3`. |
| **AUD-003** | **API Reproducibility** | Volatile wall-clock build timestamps in data endpoints previously caused SHA-256 drift. *(Resolved in Phase 2; monitored)* | **High** *(Remediated)* | `scripts/generate_api.py`, `tests/test_api_reproducibility.py` | Repeated builds produced checksum mismatches. | Isolate all generation timestamps strictly to `catalog.json` manifest. |
| **AUD-004** | **Data Quality** | 3 open-source developer resources have null top-level `repository_url` despite having GitHub links in `evidence`. | **Low** | `datasets/developer-resources.json` (`whisper-cpp-api`, `llama-cpp-server`, `fastembed-gpu`) | Consumers querying `repository_url` receive `null` instead of direct repository link. | Backport GitHub links from evidence array into `repository_url` in Phase 2. |
| **AUD-005** | **Schema Evolution** | Schemas do not enforce `additionalProperties: false` or conditional `if/then` rules for open-source licenses. | **Medium** | `schemas/common.schema.json`, `schemas/ai-tool.schema.json` | Contributor typos in field names could pass validation; open-source records can have null licenses. | Add `additionalProperties: false` and `if/then` constraints in Schema v1.1.0. |
| **AUD-006** | **Data Governance** | Static verification timestamps (`2026-11-03`) risk staleness over time without periodic full-pass sweeps. | **Medium** | `datasets/*.json` (`verified: "2026-11-03"`) | External sites change pricing or redirect over time without automated flagging. | Establish a quarterly full-pass verification scan alongside the weekly sample checker. |
| **AUD-007** | **Test Infrastructure** | Test runner relies on standard `unittest`; `coverage` tool is not configured in default environment. | **Low** | CLI test run: `No module named coverage` | Code coverage percentages cannot be formally measured in local terminal without dev dependencies. | Add `coverage run -m unittest` script and documented dev setup in `docs/release-process.md`. |
| **AUD-008** | **Search Backend** | In-memory substring scoring is $O(N)$ across all records. | **Informational** | `src/nexus_registry/client.py:165` (`search()`) | High performance for 1,003 records (< 2ms), but will scale linearly as datasets grow beyond 20,000. | Plan optional SQLite FTS5 index generation for future large-scale releases. |

---

## 2. Issues Grouped by Severity

### Critical Severity (0 Issues)
- **None.** No critical security exploits, active data corruption bugs, hardcoded secrets, or breaking crashes exist in the codebase.

### High Severity (2 Issues — Both Successfully Remediated)
- **AUD-001 (SDK Packaging):** Previously, installing `nexus-registry` from PyPI outside git would fail to find `datasets/`. Fixed by embedding canonical data into `src/nexus_registry/data/` with `importlib.resources`.
- **AUD-003 (Deterministic API Hashes):** Previously, volatile timestamps broke reproducible SHA-256 hashes. Fixed by removing timestamps from data endpoints and isolating them strictly to `catalog.json`.

### Medium Severity (3 Active Issues)
- **AUD-002 (CI Link-Check Permissions & Pinning):** `.github/workflows/link-check.yml` needs `permissions: contents: read` and pinned `requests`.
- **AUD-005 (Schema Strictness):** Absence of `additionalProperties: false` leaves room for unnoticed contributor typos.
- **AUD-006 (Periodic Verification Maintenance):** Static timestamps need scheduled automated refresh workflows.

### Low Severity (2 Active Issues)
- **AUD-004 (Missing Top-Level Repository URLs):** 3 developer resources should have their GitHub evidence links backported to `repository_url`.
- **AUD-007 (Local Coverage Tooling):** Configure a standardized `dev` environment script for local coverage reporting.

### Informational (1 Issue)
- **AUD-008 (Search Scalability):** Documented roadmap for SQLite FTS5 backend when dataset exceeds 20,000 records.
