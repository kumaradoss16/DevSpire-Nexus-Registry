# DevSpire Nexus Registry — Prioritized Remediation Plan

**Document Version:** 1.0.0  
**Audit Date:** November 6, 2026  
**Status:** Submitted for Approval Gate 0  
**Target Repository:** `https://github.com/kumaradoss16/DevSpire-Nexus-Registry.git`

---

## 1. Prioritization Strategy

Remediation follows a strict dependency order: **Data & Distribution Integrity First -> Governance & Legal Clarity -> Automation & Quality Gates -> Documentation & Onboarding**.

| Priority | Phase | Focus Area | Impact |
|---|---|---|---|
| **P0** | **Phase 1** | Packaging & Standalone SDK Distribution | Fix ISSUE-001 (bundle datasets in wheel) |
| **P0** | **Phase 2** | Deterministic API & Reproducible Hashing | Fix ISSUE-003 (stable hashes, decouple build metadata) |
| **P0** | **Phase 3** | Legal & Licensing Clarity | Fix ISSUE-002 (dual code/data licensing, trademarks) |
| **P1** | **Phase 4** | Data Quality, Taxonomy & Evidence | Fix ISSUE-004 (evidence source taxonomy & semantic audit) |
| **P1** | **Phase 5** | CI/CD Quality Gates & Drift Detection | Fix ISSUE-006 (package build & API sync checks) |
| **P1** | **Phase 6** | Contribution Governance & Templates | Fix ISSUE-005 (data correction & verification guide) |
| **P2** | **Phase 7** | Auxiliary Developer Documentation | Fix ISSUE-007 (website integration, onboarding) |
| **P2** | **Phase 8** | Final Verification & Readiness Classification | Complete Phase 11 audit cycle |

---

## 2. Phase-by-Phase Remediation Roadmap

### Phase 1: Package Bundling & Standalone SDK Execution (ISSUE-001)
- **Goal:** Enable `RegistryClient` and `nexus-registry` to work out-of-the-box when installed from PyPI/wheel without a cloned repository.
- **Actions:**
  1. Add dataset and schema assets into `src/nexus_registry/data/`.
  2. Configure `pyproject.toml` with `[tool.setuptools.package-data]` to bundle `*.json`.
  3. Refactor `client.py` and `validator.py` to use `importlib.resources` to load embedded data by default, with local path overrides.
  4. Add integration test `tests/test_standalone_client.py` asserting full catalog retrieval outside repo directory.
- **Deliverable:** Functional wheel containing all 1,003 records and 4 JSON schemas.

### Phase 2: Deterministic Static API Generation (ISSUE-003)
- **Goal:** Bit-for-bit reproducible static API artifacts with stable SHA-256 checksums.
- **Actions:**
  1. Refactor `scripts/generate_api.py` to remove volatile wall-clock `now_iso` from `tools.json`, `models.json`, `developer-resources.json`, `categories.json`, and `stats.json`.
  2. Use dataset release timestamps (`last_migrated`) in data endpoints.
  3. Confine build generation timestamps exclusively to `api/v1/catalog.json`.
  4. Add unit test `tests/test_api_reproducibility.py` running generator twice and asserting identical SHA-256 hashes.
- **Deliverable:** Reproducible static API artifacts.

### Phase 3: Legal & Licensing Architecture (ISSUE-002)
- **Goal:** Establish crystal-clear legal rights for code, factual metadata, and third-party trademarks.
- **Actions:**
  1. Retain MIT for code in `LICENSE`.
  2. Create `DATA_LICENSE.md` licensing curated dataset records under Open Data Commons Attribution License (ODC-By v1.0).
  3. Create `ATTRIBUTION.md` detailing attribution requirements for downstream consumers.
  4. Create `THIRD_PARTY_CONTENT.md` clarifying that third-party product names, logos, and trademarks belong to their respective owners.
  5. Create `docs/licensing-policy.md`.
  6. Update `README.md` to clearly partition code, data, and trademark terms.
- **Deliverable:** Complete, legally vetted open-source licensing framework.

### Phase 4: Evidence Source Taxonomy & Semantic Quality (ISSUE-004)
- **Goal:** Standardize evidence provenance across all 1,003 records.
- **Actions:**
  1. Define recognized evidence source types (`official_website`, `official_docs`, `source_repository`, `package_registry`, `model_card`, `research_paper`, `announcement`).
  2. Add semantic validation in `validator.py` with categorized warning and error reporting.
  3. Generate machine-readable `reports/data-quality-report.json` and human-readable `reports/data-quality-report.md`.
- **Deliverable:** Clean evidence taxonomy and automated data quality reporting.

### Phase 5: CI/CD Pipeline Hardening (ISSUE-006)
- **Goal:** Prevent API drift and enforce package build integrity on every PR.
- **Actions:**
  1. Update `.github/workflows/validate.yml` to:
     - Run `nexus-registry validate`.
     - Run `python scripts/generate_api.py` and execute `git diff --exit-code api/v1/` to block uncommitted API drift.
     - Test building the wheel (`pip wheel --no-deps .`).
     - Test running client in an isolated clean environment.
  2. Set least-privilege workflow permissions (`contents: read`).
- **Deliverable:** Production-grade CI quality gate.

### Phase 6: Contribution Governance (ISSUE-005)
- **Goal:** Transparent, low-friction community contribution process.
- **Actions:**
  1. Create `.github/ISSUE_TEMPLATE/data_correction.yml`.
  2. Author `CONTRIBUTING.md`, `docs/contribution-guide.md`, `docs/adding-a-resource.md`, and `docs/verification-guide.md`.
- **Deliverable:** Complete community contribution infrastructure.

### Phase 7: Auxiliary Developer Guides (ISSUE-007)
- **Goal:** Seamless developer onboarding.
- **Actions:**
  1. Create `docs/website-integration.md` detailing how `DevSpire-Nexus` consumes the Registry.
  2. Create `docs/release-process.md` defining SemVer tagging, changelog updates, and release verification.
  3. Provide concrete JavaScript `fetch()` and Python SDK usage examples.
- **Deliverable:** Complete developer documentation suite.

### Phase 8: Final Verification & Production Readiness Classification
- **Goal:** Measure and certify production readiness.
- **Actions:**
  1. Execute full test suite, schema checks, drift tests, and wheel installs.
  2. Compile `docs/audit/FINAL_REMEDIATION_REPORT.md` with issue resolution matrix and readiness classification.
- **Deliverable:** Comprehensive Final Engineering Report.

---

## 3. Approval Gate 0 Checkpoint

Before proceeding with Phase 1 modifications, the findings and remediation roadmap are submitted to the repository owner for formal review and authorization.
