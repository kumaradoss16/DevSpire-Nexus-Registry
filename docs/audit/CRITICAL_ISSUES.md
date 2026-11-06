# DevSpire Nexus Registry — Critical Issues Register

**Audit Date:** November 6, 2026  
**Status:** Open / Pending Approval Gate 0  
**Repository:** `https://github.com/kumaradoss16/DevSpire-Nexus-Registry`

---

## Issue Summary Matrix

| Issue ID | Severity | Category | Component | Description |
|---|---|---|---|---|
| **ISSUE-001** | **CRITICAL** | Distribution | `pyproject.toml`, `client.py` | Wheel package does not bundle canonical datasets; external SDK installs return 0 records |
| **ISSUE-002** | **HIGH** | Legal / Licensing | `LICENSE`, root | Undifferentiated MIT license covers dataset without trademark and factual curation terms |
| **ISSUE-003** | **HIGH** | API / Build | `scripts/generate_api.py` | Volatile wall-clock timestamps in endpoints break deterministic, bit-for-bit reproducible builds |
| **ISSUE-004** | **MEDIUM** | Data Quality | `datasets/*.json`, `validator.py` | Inconsistent evidence source labeling and absence of structured source taxonomy |
| **ISSUE-005** | **MEDIUM** | Governance | `.github/ISSUE_TEMPLATE/` | Missing structured data correction / re-verification template |
| **ISSUE-006** | **MEDIUM** | CI/CD | `.github/workflows/` | CI does not test package wheel build or static API artifact drift |
| **ISSUE-007** | **LOW** | Documentation | `docs/` | Missing external website integration guide and detailed verification guide |

---

## Detailed Issue Specifications

### ISSUE-001: Wheel Package Does Not Bundle Canonical Datasets
- **Severity:** **CRITICAL**
- **Affected Files:** `pyproject.toml`, `src/nexus_registry/client.py`, `src/nexus_registry/validator.py`
- **Evidence:** Running `pip wheel --no-deps -w dist .` and inspecting `nexus_registry-1.0.0-py3-none-any.whl` reveals only Python modules in `src/`. No JSON files are packaged. Testing `RegistryClient(root_dir='C:/Temp')` yields 0 records.
- **Impact:** Any external developer or agent running `pip install nexus-registry` cannot use the SDK or CLI unless they also clone the full Git repository.
- **Recommended Remediation:**
  1. Package canonical datasets and schemas inside `src/nexus_registry/data/` (or configure `package_data` inclusion in `pyproject.toml`).
  2. Update `RegistryClient` and `RegistryValidator` to load from package resources via `importlib.resources` by default, with automatic fallback to repository root if running from a git checkout.
- **Dependencies:** None.
- **Acceptance Criteria:** `pip install <wheel>` in a clean environment enables `RegistryClient().get("langchain")` and `nexus-registry stats` to return all 1,003 records.
- **Validation Method:** Build wheel, install in isolated virtual environment, run automated client test.

---

### ISSUE-002: Undifferentiated Licensing Architecture
- **Severity:** **HIGH**
- **Affected Files:** `LICENSE`, root directory
- **Evidence:** Root `LICENSE` is pure MIT, which applies to code. The dataset contains factual metadata and descriptions of third-party commercial/open-source tools (e.g. OpenAI, Anthropic, Meta).
- **Impact:** Legal ambiguity for corporate consumers regarding database rights, redistribution of curated metadata, and trademark fair-use.
- **Recommended Remediation:**
  1. Establish dual-licensing: Code under MIT; Dataset under Open Data Commons Attribution (ODC-By v1.0) or CC-BY 4.0.
  2. Create `DATA_LICENSE.md`, `ATTRIBUTION.md`, `THIRD_PARTY_CONTENT.md`, and `docs/licensing-policy.md` explicitly defining fair-use trademark boundaries.
- **Dependencies:** None.
- **Acceptance Criteria:** Code and data licenses are clearly partitioned; no ambiguous copyright claims over third-party trademarks.
- **Validation Method:** Legal documentation review against open data governance standards.

---

### ISSUE-003: Volatile Timestamps Prevent Deterministic API Builds
- **Severity:** **HIGH**
- **Affected Files:** `scripts/generate_api.py`, `api/v1/*.json`
- **Evidence:** `generate_api.py` inserts `now_iso = datetime.now(...)` into `tools.json`, `models.json`, etc. Running the generator without dataset changes alters SHA-256 hashes on every run.
- **Impact:** Breaks reproducible builds; causes unnecessary git diff churn; invalidates downstream client caching.
- **Recommended Remediation:**
  1. Use deterministic metadata in data endpoints (e.g., dataset version `1.0.0` or git commit/migration date).
  2. Confine wall-clock build timestamps exclusively to the top-level `catalog.json` manifest.
- **Dependencies:** None.
- **Acceptance Criteria:** Consecutive runs of `generate_api.py` without data changes produce identical SHA-256 hashes for all data endpoints.
- **Validation Method:** Run `generate_api.py` twice and assert byte-for-byte hash equality.

---

### ISSUE-004: Inconsistent Evidence Source Labeling
- **Severity:** **MEDIUM**
- **Affected Files:** `datasets/*.json`, `schemas/common.schema.json`, `src/nexus_registry/validator.py`
- **Evidence:** Evidence source labels vary between `"Official website"`, `"Verified link"`, `"github.com"`, and `"Hugging Face Model Card"` without a formalized source type taxonomy.
- **Impact:** External API consumers cannot programmatically filter records by evidence type (e.g., filter models verified by official model cards vs blog posts).
- **Recommended Remediation:**
  1. Define a standardized evidence source schema with `source_type` enum (`official_website`, `official_docs`, `source_repository`, `package_registry`, `model_card`, `research_paper`, `announcement`).
  2. Implement semantic validation in `validator.py` for evidence tuples.
- **Dependencies:** Schema update.
- **Acceptance Criteria:** Every record's evidence sources map to a recognized taxonomy.
- **Validation Method:** `nexus-registry validate` verifies evidence types.

---

### ISSUE-005: Missing Structured Data Correction Issue Template
- **Severity:** **MEDIUM**
- **Affected Files:** `.github/ISSUE_TEMPLATE/`
- **Evidence:** Issue templates exist for new resource submissions and bugs, but lacks a dedicated template for community data corrections (e.g., pricing change, URL redirect, new model context window).
- **Impact:** Community contributions for metadata fixes lack structured triage.
- **Recommended Remediation:** Create `.github/ISSUE_TEMPLATE/data_correction.yml`.
- **Dependencies:** None.
- **Acceptance Criteria:** GitHub issue template offers structured dropdowns and evidence requirements for reporting data corrections.
- **Validation Method:** YAML linting and GitHub Issue forms parser verification.

---

### ISSUE-006: CI Does Not Verify Package Build or API Drift
- **Severity:** **MEDIUM**
- **Affected Files:** `.github/workflows/validate.yml`, `.github/workflows/tests.yml`
- **Evidence:** Current CI workflows test unit tests and validate datasets, but do not check whether `api/v1/*.json` has drifted out of sync with `datasets/*.json`, nor do they test building the wheel package.
- **Impact:** A pull request modifying `datasets/` could be merged without updating `api/v1/`, breaking API consumers.
- **Recommended Remediation:** Add build and drift verification steps in CI.
- **Dependencies:** `scripts/generate_api.py`.
- **Acceptance Criteria:** CI fails if `git diff --exit-code api/v1/` detects uncommitted API drift.
- **Validation Method:** CI workflow simulation in test harness.

---

### ISSUE-007: Missing Auxiliary Documentation Guides
- **Severity:** **LOW**
- **Affected Files:** `docs/`
- **Evidence:** `docs/` currently has `architecture.md`, `cli-reference.md`, `data-model.md`, `governance.md`, `schema-versioning.md`, `verification-policy.md`, but lacks specific developer onboarding guides: `website-integration.md`, `contribution-guide.md`, `adding-a-resource.md`, `release-process.md`.
- **Impact:** External developers must deduce integration procedures from general docs.
- **Recommended Remediation:** Author comprehensive guides for each workflow.
- **Dependencies:** None.
- **Acceptance Criteria:** All guides exist, are cross-referenced, and contain complete instructions.
- **Validation Method:** Markdown and link verification.
