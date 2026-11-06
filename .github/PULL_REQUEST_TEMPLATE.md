## Description
Briefly describe the change proposed in this PR.

## Type of Change
- [ ] New resource submission
- [ ] Existing resource metadata update / re-verification
- [ ] Developer Quick Start guide addition
- [ ] Bug fix in Python CLI or SDK
- [ ] Documentation improvement
- [ ] Schema or tooling refinement

## Checklist
- [ ] Added or modified records follow kebab-case slug ID convention (`^[a-z0-9]+(-[a-z0-9]+)*$`).
- [ ] Primary source evidence URLs are provided in the `evidence` field.
- [ ] Resource `official_url` is accessible and uses `https://`.
- [ ] Ran `python -m nexus_registry.cli validate` and confirmed 0 errors.
- [ ] Ran `python -m unittest discover -s tests` and confirmed all tests pass.
- [ ] Generated deterministic API endpoints via `python scripts/generate_api.py`.
