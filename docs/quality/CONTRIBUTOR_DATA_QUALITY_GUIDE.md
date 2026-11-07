# DevSpire Nexus Registry — Contributor Data Quality Guide

**Guide Version:** 1.0.0  
**Effective Date:** 2026-11-07  
**Scope:** Instructions for open-source contributors submitting new resources or correcting existing entries.

---

## 1. Contributor Checklist

Before submitting a Pull Request to add or update records:

1. [ ] **ID Format:** Slug must be lowercase kebab-case (`my-ai-tool`).
2. [ ] **Required Fields:** Include `id`, `name`, `description`, `category`, `resource_type`, `official_url`, `pricing`, `tags`, `verified`, `status`, `evidence`, `canonical_id`.
3. [ ] **Evidence Link:** Provide at least one valid primary source URL (official site, documentation, repository, or model card).
4. [ ] **Local Validation:** Run `nexus-registry quality validate` and ensure 0 errors.
5. [ ] **Identity Check:** Run `nexus-registry quality duplicates` and confirm no ID collisions.

---

## 2. Local Quality Commands for Contributors

```bash
# 1. Validate your changes against JSON Schema contracts
nexus-registry quality validate

# 2. Check for duplicate IDs or shared URLs
nexus-registry quality duplicates

# 3. View the full quality scorecard
nexus-registry quality check
```

---

## 3. Resolving Common Validation Errors

| Validation Error | Cause | Resolution |
|:---|:---|:---|
| `$.name: Required property missing` | Mandatory property omitted. | Add `"name": "Canonical Product Name"` to record. |
| `$.id: Identifier must be lowercase...` | Uppercase, underscore or spaces. | Convert to kebab-case: `my_tool` -> `my-tool`. |
| `$.official_url: Must be a valid URI` | Missing protocol or malformed. | Ensure URL starts with `https://` or `http://`. |
| `$.status: Value must be one of...` | Invalid status string. | Use `"verified"`, `"partially_verified"`, or `"unverified"`. |
