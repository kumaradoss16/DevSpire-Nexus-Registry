# DevSpire Nexus Registry — Metadata Freshness Policy

**Policy Version:** 1.0.0  
**Effective Date:** 2026-11-07  
**Scope:** Review intervals, age categories, staleness detection, and scheduled auditing workflows.

---

## 1. Freshness Review Windows

Different metadata attributes decay at different rates. The registry enforces tiered review windows:

| Metadata Type | Review Window | Rationale |
|:---|:---|:---|
| **Commercial Pricing & Plans** | 90 days | SaaS products frequently revise seat prices, free tiers, and API rate limits. |
| **API Endpoints & SDK Packages** | 180 days | Frameworks release major semver updates and deprecate older client interfaces. |
| **General Architecture & Features** | 180 days | Core technical capabilities and model parameter counts remain relatively stable. |
| **Annual Full Catalog Sweep** | 365 days | Comprehensive re-verification of all records and publisher domains. |

---

## 2. Age Classification Model

Based on the elapsed calendar days between the `verified` timestamp and the current audit run:

| Age (Days) | Classification | Impact on Quality Score | Action Required |
|:---|:---|:---|:---|
| **0 – 90 days** | `FRESH` | 100% freshness credit | None; actively verified. |
| **91 – 180 days** | `CURRENT` | 90% freshness credit | Normal maintenance schedule. |
| **181 – 365 days** | `AGING` | 60% freshness credit | Candidate for review in next quarterly sweep. |
| **> 365 days** | `STALE` | 0% freshness credit | Flagged in `freshness-audit.json`; requires manual re-audit. |

---

## 3. Scheduled Automated Auditing

1. **Weekly Sample Probe:**
   - GitHub Action `.github/workflows/link-check.yml` samples 50 URLs every Sunday at 03:00 UTC.
   - Detects domain redirects, HTTP 404/410, and DNS failures before consumers are impacted.
2. **Quarterly Catalog Sweep:**
   - Evaluates all 1,003 records using `nexus-registry quality freshness`.
   - Generates freshness reports to guide editorial re-verification batches.
