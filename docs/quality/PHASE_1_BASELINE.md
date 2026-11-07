# DevSpire Nexus Registry — Phase 1 Quality Baseline Report

**Baseline Date:** 2026-11-07  
**Auditor:** Principal Data Quality Architect & Data Governance Specialist  
**Phase:** Phase 1 — Data Quality and Verification Infrastructure  
**Repository:** `https://github.com/kumaradoss16/DevSpire-Nexus-Registry.git`  

---

## 1. Executive Baseline Summary

This report establishes the pre-implementation data quality baseline for the **DevSpire Nexus Registry** prior to deploying the automated Phase 1 Data Quality and Verification Infrastructure.

| Baseline Metric | AI Tools | AI Models | Developer Resources | Catalog Total | Status |
|:---|---:|---:|---:|---:|:---|
| **Total Canonical Records** | 403 | 300 | 300 | **1,003** | Verified |
| **Schema-Valid Records** | 403 | 300 | 300 | **1,003 (100%)** | Verified |
| **Schema Validation Errors** | 0 | 0 | 0 | **0** | Clean |
| **Duplicate Identifiers** | 0 | 0 | 0 | **0** | Clean |
| **Duplicate Slugs** | 0 | 0 | 0 | **0** | Clean |
| **Cross-Registry ID Collisions** | 0 | 0 | 0 | **0** | Clean |
| **Unique Normalized URLs** | 401 | 277 | 288 | **966** | Analyzed |
| **Shared URL Destinations** | 1 destination | 14 destinations | 11 destinations | **26 destinations** | Classifying |
| **Verified Status Count** | 403 (100%) | 300 (100%) | 300 (100%) | **1,003 (100%)** | Baseline |
| **Total Evidence Citations** | 546 | 616 | 578 | **1,740** | Documented |
| **Average Citations / Record** | 1.35 | 2.05 | 1.93 | **1.73** | Documented |
| **Automated Unit Tests** | — | — | — | **30 Passing** | Verified |

---

## 2. Dataset-by-Dataset Inventory & Health

### 2.1 AI Tools (`datasets/ai-tools.json`)
- **Record Count:** 403
- **File Size:** 623,149 bytes
- **Mandatory Field Completeness:** 100% across `id`, `name`, `description`, `category`, `resource_type`, `official_url`, `pricing`, `tags`, `verified`, `status`, `evidence`, `canonical_id`.
- **Nullable / Optional Attributes:**
  - `license`: 240 specified, 163 `null` (Proprietary / closed commercial SaaS tools).
  - `signup_required`: 382 specified, 21 `null`.
  - `icon`: 395 specified, 8 `null` (Falling back to default frontend icons).
  - `platform`: 355 specified, 48 `null`.

### 2.2 AI Models (`datasets/ai-models.json`)
- **Record Count:** 300
- **File Size:** 517,338 bytes
- **Mandatory Field Completeness:** 100% across required contract attributes.
- **Nullable / Optional Attributes:**
  - `params`: 188 specified, 112 `null` (Closed API models such as GPT-4o, Claude 3.5 Sonnet do not disclose parameter scale).
  - `context_k`: 265 integer values, 35 `null` (Represented in text `context` field).
  - `moe`: 300 specified boolean flags (100% complete).
  - `open_weights`: 300 specified boolean flags (100% complete).

### 2.3 Developer Resources (`datasets/developer-resources.json`)
- **Record Count:** 300
- **File Size:** 711,332 bytes
- **Mandatory Field Completeness:** 100% across required contract attributes.
- **Nullable / Optional Attributes:**
  - `repository_url`: 245 specified, 55 `null` (52 proprietary cloud APIs + 3 open-source records flagged in AUD-004 where repository link was in evidence).
  - `developer_quick_start`: 32 enriched records with verified installation commands and code examples.

---

## 3. Identity and URL Integrity Baseline

### 3.1 Identifier Uniqueness
- **Within-Registry Duplicate IDs:** 0
- **Within-Registry Duplicate Slugs:** 0
- **Cross-Registry ID Collisions:** 0 (Disjoint identifier sets across all 3 registries).

### 3.2 URL Normalization & Shared Destinations Audit
A full URL normalization scan across all 1,003 records identified **26 shared destination URLs** mapped to 59 distinct records:

```text
Classification Breakdown:
1. Shared Legitimate Monorepo / Vendor Destinations (19 URLs, 45 records):
   - https://qodo.ai: Qodo vendor site hosting 3 distinct products ('qodo', 'pr-agent', 'codiumate')
   - https://ai.google.dev/gemini-api/docs/models/gemini: Documentation hub for 4 Gemini model records
   - https://github.com/openai/whisper: Monorepo containing 3 distinct Whisper checkpoint sizes
   - https://github.com/Dao-AILab/flash-attention: Repository for FlashAttention 1, 2, 3 and Flash-Decoding
   - https://github.com/mosaicml/llm-foundry: Cross-registry monorepo ('mpt-7b', 'mpt-30b', 'llm-foundry')
   - https://modelcontextprotocol.io: Specification vs SDK ('mcp-spec', 'mcp-sdk')

2. Probable Duplicates Flagged for Editorial Review (7 URLs, 14 records):
   - https://cohere.com/rerank: 'cohere-rerank-3' vs 'cohere-rerank-v3' (Cohere Rerank 3)
   - https://huggingface.co/THUDM/CogVideoX-5b: 'cogvideox' vs 'cogvideox-5b' (CogVideoX 5B)
   - https://github.com/triton-inference-server/tensorrt_llm_backend: 'tensorrt-llm-triton' vs 'tensorrt-llm-backend'
   - https://github.com/NVIDIA/cutlass: 'cutlass' vs 'nvidia-cutlass'
   - https://github.com/triton-inference-server/client: 'triton-client' vs 'triton-inference-client'
   - https://github.com/huggingface/safetensors: 'safetensors' vs 'huggingface-safetensors'
   - https://github.com/huggingface/tokenizers: 'tokenizers' vs 'huggingface-tokenizers'
```

*Policy Note: Under Phase 1 safety rules, these probable duplicates will NOT be merged or deleted automatically, preserving all existing IDs and consumer references while documenting resolution recommendations.*

---

## 4. Evidence and Provenance Baseline

- **Verification Status Distribution:** 1,003 records (100%) marked `status: "verified"`.
- **Verification Dates:** `2026-11-03` (948 records, 94.5%) and `2026-11-04` (55 records, 5.5%).
- **Evidence Citation Count Distribution:**
  - 1 citation: 377 records (37.59%)
  - 2 citations: 515 records (51.35%)
  - 3 citations: 111 records (11.07%)
  - Total: 1,740 citations (Average: 1.73 citations per record)
- **Evidence Archetypes:**
  - Official Website: 841 links (48.33%)
  - Source Repository: 368 links (21.15%)
  - Official Documentation: 242 links (13.91%)
  - Model Card / Weights: 148 links (8.51%)
  - Package Registry: 64 links (3.68%)
  - Official Announcement: 42 links (2.41%)
  - Research Paper: 35 links (2.01%)

---

## 5. Existing Tests & Verification Baseline

- **Automated Test Modules:** 7 test files in `tests/`
- **Total Tests:** 30 unit tests running in 0.54 seconds.
- **Pass Rate:** 100% (30 passed, 0 failed, 0 errors).
- **Packaging:** Standalone wheel (`nexus_registry-1.0.0-py3-none-any.whl`, 275 KB) tested and verified loading 1,003 records offline in isolated environment.
