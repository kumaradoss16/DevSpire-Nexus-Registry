# DevSpire Nexus Registry — Evidence Standards

**Standards Version:** 1.0.0  
**Effective Date:** 2026-11-07  
**Scope:** Canonical classification of external citations into 7 evidence archetypes and primary vs. secondary source hierarchy.

---

## 1. Evidence Archetype Taxonomy

DevSpire Nexus Registry classifies all external citations into seven canonical archetypes:

| Archetype Identifier | Primary Domain Examples | Authority Level | Role in Verification |
|:---|:---|:---|:---|
| `official_website` | `vendor.com`, `product.ai` | Primary | Establishes publisher identity and commercial domain ownership. |
| `official_documentation`| `docs.*`, `platform.*` | Primary | Validates API schemas, feature scope, and technical architecture. |
| `source_repository` | `github.com/*`, `gitlab.com/*` | Primary | Verifies open-source codebase, license files, and release commits. |
| `package_registry` | `pypi.org/*`, `npmjs.com/*` | Primary | Validates package naming, installation commands, and version tags. |
| `model_card` | `huggingface.co/*` | Primary | Validates model weights, parameter scales, and evaluation data. |
| `announcement` | `blog.*`, `/news/` | Primary | Confirms corporate release milestones and official launch dates. |
| `research_paper` | `arxiv.org/*`, `openreview.net`| Primary | Validates algorithmic innovations and academic benchmark claims. |
| `secondary_source` | Technical blogs, tutorials | Secondary | Corroborating signals; cannot substitute for primary source. |
| `community_source` | Reddit, Discord, Forums | Secondary | Discovery signal only; cannot be used as sole proof of claims. |

---

## 2. Evidence Tuple Format

In canonical datasets, evidence is stored as an array of 2-element tuples:

```json
"evidence": [
  ["Official website", "https://ollama.com/"],
  ["GitHub Repository", "https://github.com/ollama/ollama"],
  ["Ollama Blog", "https://ollama.com/blog/windows-preview"]
]
```

- Element 0 (`label`): Human-readable descriptive name or source classification.
- Element 1 (`url`): Valid, fully-qualified HTTP/HTTPS URL conforming to RFC 3986.

---

## 3. Evidence Quality Rules

1. **Relevance:** The URL must point directly to information concerning the indexed resource.
2. **Persistence:** Prefer canonical documentation URLs over transient marketing redirect links.
3. **Primary Source Requirement:** A record marked `verified` must have at least one primary source citation. Secondary sources alone are insufficient.
