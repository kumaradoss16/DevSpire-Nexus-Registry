# DevSpire Nexus Registry — Licensing & Governance Policy

This document defines the formal legal architecture governing the DevSpire Nexus Registry codebase, datasets, and community contributions.

---

## 1. Dual-License Architecture

To ensure maximum legal certainty for both software engineers and data consumers, the project maintains an explicit separation between code and curated data:

```
┌─────────────────────────────────────────────────────────────┐
│                 DevSpire Nexus Registry                     │
├──────────────────────────────┬──────────────────────────────┤
│         Software Code        │         Curated Data         │
│   • Python SDK (nexus_reg)   │   • datasets/*.json          │
│   • nexus-registry CLI       │   • api/v1/*.json            │
│   • Validator Engine         │   • catalog.json             │
│   • Build Scripts            │                              │
├──────────────────────────────┼──────────────────────────────┤
│          MIT License         │      ODC-By 1.0 License      │
│     (Permissive Software)    │     (Open Data Commons)      │
└──────────────────────────────┴──────────────────────────────┘
```

### 1.1 Software License (MIT)
All executable source code, CLI utilities, test harnesses, and build automations located in `src/`, `scripts/`, and `tests/` are distributed under the terms of the **MIT License** ([`LICENSE`](../LICENSE)).

### 1.2 Dataset License (ODC-By 1.0)
All curated JSON datasets located in `datasets/`, static endpoints in `api/v1/`, and schema definitions in `schemas/` are distributed under the **Open Data Commons Attribution License (ODC-By v1.0)** ([`DATA_LICENSE.md`](../DATA_LICENSE.md)).

---

## 2. Nominative Trademark Fair Use

Names, trade dress, and brand assets of cataloged tools and models are protected trademarks of their respective owners. Refer to [`THIRD_PARTY_CONTENT.md`](../THIRD_PARTY_CONTENT.md) for detailed nominative fair-use guidelines.

---

## 3. Contribution Inbound/Outbound Terms

By submitting a Pull Request containing code or resource metadata to this repository, contributors agree that:
1. Code contributions will be licensed under the MIT License.
2. Resource metadata contributions will be licensed under the ODC-By v1.0 License.
3. All submitted metadata and documentation URLs represent publicly available primary sources without proprietary trade secret restrictions.
