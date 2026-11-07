# DevSpire Nexus Registry — Dataset Integrity Rules

**Specification Version:** 1.0.0  
**Effective Date:** 2026-11-07  
**Scope:** Strict structural and relational rules governing canonical JSON records.

---

## 1. Identity & Naming Rules

1. **Identifier Format:** `id` must be lowercase alphanumeric string with optional hyphens (`^[a-z0-9]+(-[a-z0-9]+)*$`).
2. **Global Uniqueness:** No two records may share the same `id` anywhere within the entire catalog, across all three registries.
3. **Canonical ID Alignment:** `canonical_id` must match the pattern `{registry_prefix}:{id}`:
   - AI Tools: `ai_tool:{id}`
   - AI Models: `ai_model:{id}` (or `model:{id}`)
   - Developer Resources: `developer_resource:{id}`

---

## 2. Text & Description Constraints

1. **Resource Name:** `minLength: 2`, `maxLength: 100`. Must reflect canonical product or package branding.
2. **Description:** `minLength: 10`, `maxLength: 1000`. Must be a concise technical summary of capabilities, target audience, and architecture. Marketing hyperbole (e.g. *"The best tool on the planet"*) is prohibited.
3. **Tags:** Array of 1 to 20 lowercase or title-cased keyword strings.

---

## 3. URL and Protocol Rules

1. **Protocol:** All `official_url`, `repository_url`, `documentation_url`, and `evidence` URLs must use valid `https://` or `http://` schemes. HTTPS is strongly preferred.
2. **Canonical Destination:** Avoid shorteners (`bit.ly`, `t.co`) or tracking links (`utm_*`).

---

## 4. Category Whitelisting

1. Each record's `category` must exactly match one of the predefined categories declared in the dataset's `_meta.categories` array.
2. New categories require a schema update and documentation review.
