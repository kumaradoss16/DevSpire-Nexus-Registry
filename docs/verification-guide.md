# DevSpire Nexus Registry — Verification Guide

This guide establishes the verification criteria and standards for maintainers and community contributors.

---

## 1. Verification Hierarchy

Records must satisfy minimum evidence thresholds to achieve `verified` status:

| Threshold | Required Primary Sources | Allowed Sources |
|---|---|---|
| **Tier 1 (High Confidence)** | 2+ Authoritative Sources | Official documentation + source code repository OR model card |
| **Tier 2 (Standard Verified)** | 1 Official Primary Source | Official homepage OR official publisher documentation |
| **Partially Verified** | Third-party corroboration | Public package index or verified community port |
| **Deprecated** | Discontinuation notice | Vendor sunset post, archived repository, or CVE advisory |

---

## 2. Unacceptable Sources

The following sources **do not qualify** as authoritative evidence:
- Aggregator directories and SEO affiliate lists.
- Anonymous social media posts or speculative rumors.
- Unattributed blog reposts or AI summary scrapers.

---

## 3. Review Frequency

- **Rapidly evolving tools & models:** Re-verified every **90 days**.
- **Stable developer frameworks:** Re-verified every **180 days**.
- **Stale Threshold:** Records exceeding 180 days without review trigger automated quality warnings.
