# DevSpire Nexus Registry Governance

The DevSpire Nexus Registry is maintained as a transparent, evidence-first catalog of AI software, foundation models, and developer infrastructure.

## Editorial Principles

1. **Evidence-First Requirement:**
   Every record must cite at least one primary source (official documentation, vendor announcement, repository, or package registry). Secondary blogs, affiliate links, and promotional reviews are prohibited.
2. **Deterministic Schemas:**
   All entries must strictly pass the JSON Schemas in `schemas/`.
3. **No Fabricated Benchmarks or Capabilities:**
   Performance metrics, pricing tiers, and licensing statements must match published specifications from the author or vendor.
4. **Honest Fallbacks:**
   When verified Quick Start guides or parameter sizes are unavailable, records must explicitly state unverified status rather than generating synthetic instructions.

## Contribution Workflow

1. Fork the repository.
2. Create a feature branch: `git checkout -b submission/<resource-slug>`.
3. Add or update the record in `datasets/<registry>.json`.
4. Validate compliance:
   ```bash
   python -m nexus_registry.cli validate
   python -m unittest discover -s tests
   python scripts/generate_api.py
   ```
5. Commit and submit a Pull Request using the PR template.
6. CI automated checks validate schemas and run unit tests.
