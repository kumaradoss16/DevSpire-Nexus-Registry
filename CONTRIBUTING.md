# Contributing to DevSpire Nexus Registry

Thank you for your interest in contributing to the **DevSpire Nexus Registry**!

We welcome community submissions of new AI tools, foundation models, developer infrastructure, as well as corrections, documentation improvements, and tooling enhancements.

---

## 1. Principles of Contribution

1. **Evidence-First Rule:** Every submitted or modified record must cite at least one authoritative primary source (official documentation, vendor announcement, repository, or package registry).
2. **Schema Conformance:** All records must strictly pass the JSON Schemas in `schemas/`.
3. **No Synthetic Benchmarks:** Performance claims, parameters, and pricing must reflect official publisher disclosures.
4. **Preserve Identifiers:** Existing kebab-case slug IDs must not be changed without a documented migration alias.

---

## 2. Ways to Contribute

- **Report Data Errors:** Open an issue using the [Data Correction Form](.github/ISSUE_TEMPLATE/data_correction.yml).
- **Propose a New Resource:** Open an issue via the [Resource Submission Form](.github/ISSUE_TEMPLATE/resource_submission.yml).
- **Submit a Pull Request:** Add a new resource, update an existing one, or contribute code directly via Git.

---

## 3. Pull Request Workflow

1. **Fork and Clone:**
   ```bash
   git clone https://github.com/<your-username>/DevSpire-Nexus-Registry.git
   cd DevSpire-Nexus-Registry
   ```

2. **Create a Topic Branch:**
   ```bash
   git checkout -b submission/my-resource
   ```

3. **Install Package in Editable Mode:**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Edit the Appropriate Dataset:**
   - AI Tools: `datasets/ai-tools.json`
   - AI Models: `datasets/ai-models.json`
   - Developer Resources: `datasets/developer-resources.json`

5. **Validate Locally:**
   ```bash
   # Validate schemas and integrity
   nexus-registry validate

   # Run automated test suite
   python -m unittest discover -s tests

   # Re-generate static API endpoints
   python scripts/generate_api.py
   ```

6. **Submit PR:**
   - Commit changes with clear, descriptive commit messages.
   - Push to your fork and submit a Pull Request using the [PR Template](.github/PULL_REQUEST_TEMPLATE.md).

---

## 4. Maintainer Review Process

1. **Automated Checks:** GitHub Actions runs `validate.yml` and `tests.yml`. Pull requests with failing tests or uncommitted API drift cannot be merged.
2. **Human Verification:** Maintainers verify that submitted evidence URLs genuinely correspond to the claimed capabilities.
3. **Merge & Release:** Approved records are merged into `main` and included in the next immutable API snapshot.
