# Schema Versioning & Evolution Policy

The DevSpire Nexus Registry adheres to [Semantic Versioning 2.0.0](https://semver.org/).

## Version Identifier Format

- **Schema URI:** `https://devspirehub.com/schemas/<domain>.schema.json`
- **Release Version:** `MAJOR.MINOR.PATCH` (e.g. `1.0.0`)
- **Dataset Metadata:** Each dataset file embeds `_meta.schema_version` and `_meta.dataset_version`.

## Compatibility Rules

1. **PATCH Releases (`1.0.x`):**
   - Adding or updating resource records.
   - Correcting documentation, typos, or verification evidence.
   - Non-breaking validation performance improvements.
2. **MINOR Releases (`1.x.0`):**
   - Adding optional fields to the schema.
   - Introducing new supported package managers or modalities.
   - Adding new CLI read-only subcommands.
   - Existing consumers and scripts remain 100% backward-compatible.
3. **MAJOR Releases (`x.0.0`):**
   - Renaming or removing existing fields.
   - Changing required property constraints.
   - Modifying ID format or namespacing conventions.
   - Deprecation notices must be provided at least one minor release prior.
