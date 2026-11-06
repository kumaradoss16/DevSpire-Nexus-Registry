# Changelog

All notable changes to the DevSpire Nexus Registry will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-11-06

### Added
- **Canonical Datasets:**
  - `datasets/ai-tools.json`: 403 verified AI application records across 14 categories.
  - `datasets/ai-models.json`: 300 verified foundation & specialized AI model records across 12 categories.
  - `datasets/developer-resources.json`: 300 verified engineering resources across 12 categories.
- **Formal JSON Schema Specifications (Draft 2020-12):**
  - `schemas/common.schema.json`: Base resource contract, metadata, and verification provenance.
  - `schemas/ai-tool.schema.json`: AI application-specific contract.
  - `schemas/ai-model.schema.json`: AI model parameter, context window, and weights contract.
  - `schemas/developer-resource.schema.json`: Developer resource and Developer Quick Start contract.
- **Python CLI & Validator:**
  - `nexus-registry` CLI supporting offline validation, query search, resource inspect, and quickstart lookup.
  - Standalone validation engine checking IDs, URLs, schemas, category consistency, and quickstart contracts.
- **Static JSON API (v1):**
  - Static machine-readable distribution at `api/v1/*.json` with deterministic SHA256 catalog manifest.
- **Python SDK (`nexus_registry`):**
  - Zero-dependency client library for loading and querying offline registry datasets.
- **CI/CD Automation:**
  - Automated pull request dataset validation, CLI tests, and bounded link verification workflows.
