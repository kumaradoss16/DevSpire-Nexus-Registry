# DevSpire Nexus Registry — Python Package Release Guide

**Release Specification:** PEP 517 / PEP 621  
**Build System:** `setuptools.build_meta`  
**Distribution Targets:** Wheel (`.whl`), Source Distribution (`.tar.gz`)

---

## 1. Package Metadata Verification (`pyproject.toml`)

Before building a release distribution, verify that `pyproject.toml` contains:
- Correct version number: `version = "1.0.0"`.
- License identifier: `license = { text = "MIT" }`.
- Package data inclusion:
  ```toml
  [tool.setuptools.package-data]
  "nexus_registry" = [
      "data/datasets/*.json",
      "data/schemas/*.json"
  ]
  ```

---

## 2. Building Release Distributions

In an isolated virtual environment, execute:

```bash
# Install build tooling
pip install build wheel

# Build both wheel and sdist
python -m build
```

This produces:
- `dist/nexus_registry-1.0.0-py3-none-any.whl` (~275 KB)
- `dist/nexus_registry-1.0.0.tar.gz`

---

## 3. Validating the Wheel Package

Ensure the binary wheel bundles the required dataset and schema JSON files:

```bash
# Inspect wheel archive contents
python -m zipfile -l dist/nexus_registry-1.0.0-py3-none-any.whl
```

Verify that `nexus_registry/data/datasets/ai-tools.json`, `ai-models.json`, and `developer-resources.json` are present.

---

## 4. PyPI Trusted Publishing

Publishing to PyPI is executed via GitHub Actions using OpenID Connect (OIDC) Trusted Publishing:
- Workflow: `.github/workflows/publish-pypi.yml`
- Trigger: Pushing a release tag `v*.*.*`
- No long-lived PyPI API tokens stored in repository secrets.
