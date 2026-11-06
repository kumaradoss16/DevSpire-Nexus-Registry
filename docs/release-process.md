# DevSpire Nexus Registry — Release & Versioning Process

This document defines the formal release procedure for publishing updates to the DevSpire Nexus Registry.

---

## 1. Versioning Architecture

The Registry follows Semantic Versioning (**SemVer 2.0.0**):

- **Major (`X.0.0`):** Breaking schema changes (e.g. removing required fields, altering existing slug ID syntax).
- **Minor (`1.X.0`):** New non-breaking fields, additional resource records, or new CLI commands.
- **Patch (`1.0.X`):** Metadata corrections, URL updates, documentation fixes, or dependency security patches.

---

## 2. Release Preparation Checklist

Before creating a release tag:

1. **Dataset Integrity Check:**
   ```bash
   nexus-registry validate
   ```
   Must report `PASS [OK] Errors: 0`.

2. **Automated Test Suite:**
   ```bash
   python -m unittest discover -s tests
   ```
   All unit and reproducibility tests must pass.

3. **Deterministic API Compilation:**
   ```bash
   python scripts/generate_api.py
   ```
   Verify manifest checksums match generated artifacts.

4. **Package Build Verification:**
   ```bash
   pip wheel --no-deps -w dist .
   ```
   Confirm wheel bundles `src/nexus_registry/data/`.

5. **Changelog Update:**
   Document all new additions, updates, and fixes in [`CHANGELOG.md`](../CHANGELOG.md).

---

## 3. Tagging & Publishing

Once approved by maintainers:
```bash
git tag -a v1.0.0 -m "Release v1.0.0: Canonical DevSpire Nexus Registry"
git push origin v1.0.0
```

GitHub Actions automatically builds distributions and publishes release artifacts.
