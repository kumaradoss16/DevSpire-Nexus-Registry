# Resource Verification & Provenance Policy

## 1. Principles

1. **Evidence-Based:** Every claim (open-source status, pricing, license, parameter scale, installation command) must be corroborated by direct primary-source links.
2. **Never Inferred:** Missing attributes are recorded as `null` or explicitly documented as unavailable. Attributes are never guessed or inferred from marketing copy.
3. **Traceable Timestamps:** Every verified record carries an ISO-8601 date timestamp (`verified`) documenting when evidence was last audited.

## 2. Verification Taxonomy

| State | Definition | Requirements |
| :--- | :--- | :--- |
| **`verified`** | Fully confirmed from primary source | ≥ 2 primary evidence links (official website, GitHub repo, model card, or package registry). |
| **`partially_verified`** | Core identity confirmed; advanced fields pending | Website confirmed; parameters or quick start awaiting maintainer review. |
| **`unverified`** | Community submission | Initial submission pending maintainer verification. |
| **`deprecated`** | Discontinued or superseded | Archived repository or official shutdown announcement cited in notes. |

## 3. Evidence Requirements

Acceptable primary sources:
- Official product domain / documentation site.
- Canonical GitHub / GitLab / Bitbucket repository.
- Hugging Face official model card or organization repository.
- PyPI, npm, crates.io, or Docker Hub official package listings.
- Publisher whitepaper or technical report.

Unacceptable sources:
- Aggregator websites or third-party affiliate directories.
- Unverified blog posts or secondary reviews.
- Social media commentary without official attribution.
