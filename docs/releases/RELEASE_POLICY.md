# DevSpire Nexus Registry — Release Policy & Governance

**Policy Version:** 1.0.0  
**Effective Date:** 2026-11-07  
**Scope:** Tagging rules, release immutability, artifact distribution, and cadence.

---

## 1. Release Philosophy & Immutability

DevSpire Nexus Registry enforces strict immutability for all published releases:

1. **Git Tag Immutability:** Every formal release is anchored to an immutable, cryptographically signed Git tag (e.g. `v1.0.0`). Tags are never moved, deleted, or reassigned.
2. **Artifact Determinism:** Release assets attached to GitHub Releases and published on static CDNs are generated deterministically. Their cryptographic SHA-256 hashes must match the commit build manifest.
3. **No Silent Overwrites:** Once a release snapshot (e.g. `/releases/v1.0.0/` or a Git tag) is published, its contents cannot be altered. Corrections require a new patch release (e.g. `v1.0.1`).

---

## 2. Release Versioning Scheme

Releases follow Semantic Versioning (`MAJOR.MINOR.PATCH`):

- **MAJOR (vX.0.0):** Breaking schema changes, removed fields, or backward-incompatible API changes.
- **MINOR (v1.X.0):** Additive schema additions, new resource categories, or new SDK features.
- **PATCH (v1.0.X):** Data corrections, link fixes, documentation enhancements, and internal bug fixes.

---

## 3. Release Artifacts & Distribution Channels

Each release publishes the following artifacts:

| Artifact | Format | Distribution Channel | Integrity Verification |
|:---|:---|:---|:---|
| **Python Wheel** | `.whl` (PEP 427) | PyPI (`pip install nexus-registry`) | SHA-256 / PyPI provenance |
| **Source Tarball** | `.tar.gz` (sdist) | PyPI & GitHub Release Asset | SHA-256 checksum |
| **Static API Snapshot**| `api/v1/*.json` | CDN / GitHub Pages | `api/v1/catalog.json` hashes |
| **Release Archive** | `.zip` / `.tar.gz` | GitHub Releases (`tags/v1.0.0`) | Git commit tree SHA |

---

## 4. Release Cadence

- **Regular Minor / Patch Releases:** Bi-weekly or monthly based on verified community contributions.
- **Critical Data Hotfixes:** Published as patch releases within 24 hours of verifying a critical link or licensing defect.
- **Major Releases:** Scheduled with a minimum of 6 months advance notice and public deprecation windows.
