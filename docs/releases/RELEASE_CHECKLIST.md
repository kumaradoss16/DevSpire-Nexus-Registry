# DevSpire Nexus Registry — Release Checklist

**Checklist Version:** 1.0.0  
**Effective Date:** 2026-11-07  
**Scope:** Mandatory steps for Release Engineers before publishing any version tag.

---

## Pre-Release Verification Checklist

Execute every step in an isolated development environment:

### 1. Data Integrity & Validation Gates
- [ ] Run complete schema validation:
  ```bash
  python -m nexus_registry.cli validate
  ```
  *Requirement: PASS [OK] with 0 errors and 0 warnings.*
- [ ] Run full data quality scorecard:
  ```bash
  python -m nexus_registry.cli quality check
  ```
  *Requirement: Release Readiness = READY, Structural Gate = PASSED, Score >= 95.0.*
- [ ] Check identity uniqueness:
  ```bash
  python -m nexus_registry.cli quality duplicates
  ```
  *Requirement: 0 duplicate IDs, 0 cross-registry collisions.*

### 2. Static API Determinism & Schemas
- [ ] Regenerate static API artifacts:
  ```bash
  python scripts/generate_api.py
  ```
- [ ] Verify zero drift against committed files:
  ```bash
  git diff --exit-code api/v1/
  ```
- [ ] Validate manifest checksums in `api/v1/catalog.json`:
  ```bash
  python -m unittest discover -s tests -p "test_api_reproducibility.py"
  ```

### 3. Automated Test Suite
- [ ] Run the complete unit and integration test suite:
  ```bash
  python -m unittest discover -s tests -v
  ```
  *Requirement: 100% of tests pass.*

### 4. Package Build & Smoke Test
- [ ] Build source distribution and binary wheel:
  ```bash
  python -m pip install wheel build
  python -m build
  ```
- [ ] Verify wheel contents include bundled datasets:
  ```bash
  tar -ztvf dist/*.tar.gz || unzip -l dist/*.whl
  ```
- [ ] Test standalone installation in an isolated directory outside the repository:
  ```bash
  python -m unittest tests/test_standalone.py
  ```

### 5. Documentation & Changelog
- [ ] Update `CHANGELOG.md` with release notes, new resources, and bug fixes.
- [ ] Verify that version number in `pyproject.toml` and `src/nexus_registry/__init__.py` match target release version.

### 6. Git Tagging & Release Publication
- [ ] Create annotated Git tag:
  ```bash
  git tag -a v1.0.0 -m "Release v1.0.0: DevSpire Nexus Registry"
  ```
- [ ] Push tag to remote:
  ```bash
  git push origin v1.0.0
  ```
- [ ] Create GitHub Release attaching build artifacts (`.whl`, `.tar.gz`, `catalog.json`).
- [ ] Publish package to PyPI via Trusted Publishing.
