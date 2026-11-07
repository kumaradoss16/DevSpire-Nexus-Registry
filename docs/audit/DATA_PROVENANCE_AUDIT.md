# DevSpire Nexus Registry — Data Provenance & Verification Audit

**Audit Date:** 2026-11-07  
**Auditor:** DevSpire Nexus Data Governance Specialist & DevSecOps Engineer  
**Scope:** Verification metadata, evidence taxonomy, source lineage, and citation integrity across 1,003 records.  

---

## 1. Provenance Architecture Overview

In DevSpire Nexus Registry, provenance is modeled directly within each canonical record through three coordinated fields:

1. `status` (`string` enum): The editorial audit status (`verified`, `active`, `deprecated`).
2. `verified` (`string` ISO-8601 Date): The calendar date on which human or automated verification was performed.
3. `evidence` (`array[array[string, string]]`): Two-element tuples containing `[Source Label / Archetype, Authoritative Reference URL]`.

---

## 2. Evidence Taxonomy Breakdown

Using the automated audit engine (`scripts/generate_quality_report.py`), all 1,740 external evidence links across 1,003 records were classified into seven canonical evidence archetypes:

| Evidence Archetype | Primary Domain Types | Link Count | Share of Total | Audit Role & Authority |
|:---|:---|:---|:---|:---|
| **Official Website** | `company.com`, `product.ai`, `devspirehub.com` | 841 | 48.33% | Establishes primary vendor identity and official domain ownership. |
| **Source Repository** | `github.com/*`, `gitlab.com/*` | 368 | 21.15% | Verifies open-source codebase, commit activity, and license file integrity. |
| **Official Documentation** | `docs.*`, `platform.*`, `readthedocs.io` | 242 | 13.91% | Validates API schemas, SDK signatures, and technical architecture. |
| **Model Card / Weights** | `huggingface.co/*`, `civitai.com` | 148 | 8.51% | Confirms model weights availability, tokenizer details, and evaluation data. |
| **Package Registry** | `pypi.org/project/*`, `npmjs.com/package/*` | 64 | 3.68% | Validates pip/npm installation packages and version releases. |
| **Official Announcement** | `openai.com/news/*`, `anthropic.com/news/*` | 42 | 2.41% | Validates corporate product announcements and official release milestones. |
| **Research Paper / Preprint** | `arxiv.org/abs/*` | 35 | 2.01% | Confirms peer-reviewed academic lineage and benchmark methodology. |
| **Total Evidence Citations** | — | **1,740** | **100.00%** | Average: 1.73 citations per resource record |

---

## 3. Verification Timestamps & Audit Freshness

### 3.1 Verification Timestamp Distribution

| Verification Date | Record Count | Percentage |
|:---|:---|:---|
| `2026-11-03` | 948 | 94.52% |
| `2026-11-04` | 55 | 5.48% |
| **Total** | **1,003** | **100.00%** |

### 3.2 Audit Observation on Verification Dates

- **Finding:** All 1,003 records were verified or migrated within a 48-hour window (November 3–4, 2026).
- **Evaluation:** While the migration audit established initial baseline validity, relying solely on static historical verification dates introduces freshness decay risk over time as external URLs redirect, change pricing, or deprecate API versions.
- **Remediation Recommendation:**
  1. Maintain the weekly scheduled GitHub Action (`.github/workflows/link-check.yml`) to continuously test a 50-URL random sample.
  2. Implement a quarterly full-pass verification scan that updates `verified` timestamps only upon successful schema & HTTP 200 re-validation.

---

## 4. Evidence Sufficiency Assessment

To assess whether the evidence is sufficient to justify the `status: "verified"` tag, each registry was evaluated against strict proof criteria:

### 4.1 AI Tools (403 Records)
- **Proof Requirement:** Valid official product website + verified pricing/tier reference.
- **Assessment:** **Sufficient.** 143 records contain dual links (landing page + pricing page); 260 contain direct product landing page where pricing is visibly published.

### 4.2 AI Models (300 Records)
- **Proof Requirement:** Official documentation link OR Hugging Face model card OR ArXiv technical report.
- **Assessment:** **Sufficient.** 258 records (86%) contain 2 or 3 distinct citations (e.g., OpenAI docs + pricing, or Meta AI paper + HuggingFace weights).

### 4.3 Developer Resources (300 Records)
- **Proof Requirement:** Official documentation link AND/OR active GitHub/GitLab source repository.
- **Assessment:** **High Provenance.** 225 records (75%) contain 2 or 3 distinct citations linking directly to source repositories and technical docs.

---

## 5. Potential Provenance Risks & Recommendations

1. **Third-Party Domain Churn:**
   - Fast-moving AI startups occasionally rebrand, redirect domains, or shutter.
   - *Mitigation:* The link-checking CI workflow samples external endpoints to alert maintainers of HTTP 404/410 status codes before they impact consumer applications.
2. **Attribution Provenance:**
   - Provider organizations (`provider`, `publisher`, `org`) are tracked in text format.
   - *Recommendation:* Introduce standardized provider slugs (`provider_id: "openai"`, `provider_id: "meta"`) in Schema v1.1.0 to enable relational queries across products by the same author.
