# DevSpire Nexus Registry — Editorial Review Procedure

**Procedure Version:** 1.0.0  
**Effective Date:** 2026-11-07  
**Scope:** Step-by-step workflow for onboarding new resources, verifying evidence, and auditing status transitions.

---

## 1. New Resource Review Workflow

```text
[1. Ingestion]           Contributor opens PR or Issue using GitHub Form
        |
        v
[2. Identity Check]      nexus-registry quality duplicates
                         - Verify slug is lowercase kebab-case
                         - Ensure zero ID collisions
        |
        v
[3. Schema Check]        nexus-registry quality validate
                         - Ensure all mandatory fields present
                         - Check string lengths and URL syntax
        |
        v
[4. Evidence Review]     nexus-registry quality evidence
                         - Verify at least 1 primary source link
                         - Check domain ownership matches provider
        |
        v
[5. Semantic Sanity]     Maintainer checks description accuracy:
                         - Concise, factual summary
                         - Correct category classification
                         - Accurate pricing class (free, freemium, paid, open_source)
        |
        v
[6. Approval & Merge]    PR merged -> CI generates static API & catalog manifest
```

---

## 2. Review Record & Audit Trail

For significant status changes, maintainers must record an audit entry in the git commit message or PR description:

- **Resource Identifier:** (e.g. `langchain`)
- **Previous Status:** (e.g. `unverified`)
- **New Status:** (e.g. `verified`)
- **Reviewer Identity:** GitHub handle or automated CI process identity.
- **Review Date:** ISO-8601 Date (`YYYY-MM-DD`).
- **Evidence Sources Reviewed:** List of URLs audited.
- **Justification:** Concise rationale for status change.

---

## 3. Disputed or Conflicting Information

If an external vendor or community contributor flags a discrepancy in resource pricing, license, or capability:
1. An issue is opened using `.github/ISSUE_TEMPLATE/data_correction.yml`.
2. The record is flagged as `partially_verified` during triage if the dispute involves core claims.
3. Maintainers review publisher documentation to confirm facts.
4. Dataset is updated with supporting evidence and restored to `verified`.
