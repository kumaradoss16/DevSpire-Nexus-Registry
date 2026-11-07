# DevSpire Nexus Registry — Compatibility Policy

**Policy Version:** 1.0.0  
**Effective Date:** 2026-11-07  
**Scope:** Public API stability, SDK interfaces, dataset guarantees, and version demarcation.

---

## 1. Distinct Version Tracks

DevSpire Nexus Registry enforces four independent, non-interchangeable version tracks to prevent consumer confusion:

| Version Track | Current Value | Target Interface | Governed Artifacts | Breaking Change Example |
|:---|:---|:---|:---|:---|
| **API Contract Version** | `v1` | URL / HTTP Namespace | `/api/v1/*.json` endpoints | Changing URL structure, envelope shape |
| **Schema Version** | `1.0.0` | Data Schema Standards | `schemas/*.schema.json` | Renaming `official_url` to `url` |
| **Dataset Release Version** | `1.0.0` | Content Snapshot | `datasets/*.json` records | Major editorial reclassification |
| **Python Package Version** | `1.0.0` | PyPI Distribution | `pip install nexus-registry`| Removing public `client.get()` method |

---

## 2. Backward Compatibility Guarantees

### 2.1 Static API Guarantees
- **Endpoint Permanence:** Documented URLs in `/api/v1/` will never be removed or return 404 within API major version 1.
- **Envelope Stability:** The top-level `_meta` and `records` envelope keys will remain unchanged.
- **Identifier Retention:** A published `id` will never be reassigned or deleted.
- **Additive Evolution:** New fields added in minor schema releases will be optional; consumers ignoring unrecognized fields will not break.

### 2.2 Python SDK Guarantees
- **Method Stability:** All methods documented in `docs/sdk/API_REFERENCE.md` (`get()`, `search()`, `get_tools()`, `get_models()`, `get_developer_resources()`, `get_quickstart()`, `stats()`, `categories()`) are stable.
- **Offline Reliability:** The SDK will always support zero-network operation with bundled package data.
- **Type Annotations:** Public method signatures will adhere strictly to standard Python type hints.

---

## 3. What Constitutes a Breaking Change

The following changes are classified as **Breaking Changes** requiring a Major version increment:

1. **Schema Breaking Changes:**
   - Removing any property from a canonical record.
   - Changing the data type of an existing property (e.g. integer to string).
   - Making a previously optional property mandatory.
   - Removing an existing value from an enumeration.
   - Tightening a string length constraint or regex pattern such that previously valid records fail.
2. **SDK Breaking Changes:**
   - Removing or renaming any public method in `RegistryClient`.
   - Adding mandatory positional arguments to existing methods without defaults.
   - Altering the return type structure of public methods.
   - Raising new unhandled exception classes on standard lookups.

---

## 4. Deprecation Timeline & Notice

- For any planned breaking change to public API contracts, a minimum **6-month deprecation period** will be observed.
- Deprecation warnings will be surfaced in API response headers (e.g. `Sunset`, `Deprecation`) and SDK release notes.
