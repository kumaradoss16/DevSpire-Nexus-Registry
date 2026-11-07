# DevSpire Nexus Registry — Licensing & Legal Architecture Audit

**Audit Date:** 2026-11-07  
**Auditor:** Principal Software Architect & Open-Source Maintainer  
**Scope:** Intellectual property boundaries, open-source code licenses, data redistribution terms, and third-party trademark policies.  

---

## 1. Dual-License Architecture Overview

DevSpire Nexus Registry implements an explicit, industry-standard **Dual-Licensing Model** to separate software copyright from factual open-data redistribution rights:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   DevSpire Nexus Registry Licensing                    │
├───────────────────────────────────┬────────────────────────────────────┤
│           Source Code             │              Datasets              │
│       (Scripts, SDK, CLI)         │       (AI Tools, Models, Dev)      │
│                                   │                                    │
│        MIT License (OSI)          │       ODC-By v1.0 (Open Data)      │
│          `LICENSE`                │          `DATA_LICENSE.md`         │
└───────────────────────────────────┴────────────────────────────────────┘
```

---

## 2. Component Licensing Matrix

| Repository Artifact | Governing License File | License Standard | Permitted Rights | User Obligations |
|:---|:---|:---|:---|:---|
| **Python SDK (`src/`)** | `LICENSE` | MIT License | Commercial, modification, distribution, private use | Include copyright notice |
| **CLI Tooling (`nexus_registry/cli.py`)** | `LICENSE` | MIT License | Commercial, modification, distribution, private use | Include copyright notice |
| **Automation Scripts (`scripts/`)** | `LICENSE` | MIT License | Commercial, modification, distribution, private use | Include copyright notice |
| **Canonical Datasets (`datasets/*.json`)** | `DATA_LICENSE.md` | Open Data Commons Attribution (ODC-By v1.0) | Share, modify, create derivative databases, commercial use | Provide attribution credit |
| **Generated API Artifacts (`api/v1/*.json`)** | `DATA_LICENSE.md` | Open Data Commons Attribution (ODC-By v1.0) | Read, query, redistribute, embed in apps | Provide attribution credit |
| **Documentation (`docs/`, `*.md`)** | `LICENSE` / `ATTRIBUTION.md` | CC BY 4.0 / MIT | Reproduction, translation, publication | Retain authorship attribution |
| **Third-Party Product Metadata** | `THIRD_PARTY_CONTENT.md` | Nominative Fair Use | Informational reference & cataloging only | No trademark claim |

---

## 3. Third-Party Intellectual Property & Trademark Fair Use

### 3.1 Nominative Fair Use Boundaries

The registry documents and indexes commercial products, models, and open-source packages created by external organizations (e.g. OpenAI, Google, Anthropic, Meta, Microsoft, GitHub):

- **Policy Reference:** `THIRD_PARTY_CONTENT.md`
- **Legal Posture:** All company names, product titles, model names, and service marks referenced in canonical datasets are the property of their respective trademark holders.
- **Fair Use Criteria Met:**
  1. Names are used strictly to identify the actual product or service being cataloged.
  2. The registry does not assert ownership, affiliation, sponsorship, or endorsement by third-party trademark owners.
  3. No proprietary software binaries, model weights, training corpora, or protected codebases are hosted or redistributed inside this repository.

### 3.2 Logos and Brand Assets

- **Finding:** Canonical datasets store textual icon names (e.g. `icon: "brain"`, `icon: "terminal"`, `icon: "code"`) or public CDN URL references.
- **Assessment:** **Safe.** No proprietary trademarked SVG/PNG icon binaries are bundled in the git tree. All visual icons are resolved on the frontend using standard Lucide / FontAwesome icon identifiers or public third-party CDNs.

---

## 4. Citation and Attribution Requirements

In accordance with ODC-By v1.0, developers, researchers, and applications consuming registry datasets must provide attribution:

- **Attribution Specification:** Documented in `ATTRIBUTION.md`.
- **Machine-Readable Metadata:** Stored in `CITATION.cff` for academic research indexing.
- **Standard Citation Format:**
  > *"Data sourced from DevSpire Nexus Registry (https://devspirehub.com), licensed under ODC-By 1.0."*

---

## 5. Potential Legal Ambiguities & Maintainer Recommendations

1. **Clarification on Commercial Derivative Databases:**
   - Under ODC-By v1.0, downstream commercial apps may build proprietary products on top of the registry data, provided they give attribution.
   - *Recommendation:* Keep `DATA_LICENSE.md` prominently linked in README badges and package metadata so external companies understand their redistribution freedoms.
2. **DMCA Takedown and Correction Channel:**
   - `SECURITY.md` and `THIRD_PARTY_CONTENT.md` provide an explicit contact email (`oss@devspirehub.com` / `legal@devspirehub.com`) for trademark holders requesting corrections or metadata removal.
   - *Assessment:* Conforms to open-source standard operating procedures.
