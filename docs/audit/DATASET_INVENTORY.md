# DevSpire Nexus Registry — Dataset Inventory

**Audit Date:** 2026-11-07  
**Auditor:** DevSpire Nexus Data Governance Specialist & QA Engineer  
**Scope:** Factual structural and metric inventory of canonical datasets in `datasets/`.  

---

## 1. Global Dataset Summary

| Dataset File | Resource Registry | File Size (Bytes) | Record Count | Categories | Status |
|:---|:---|:---|:---|:---|:---|
| `datasets/ai-tools.json` | AI Tools | 623,149 | 403 | 14 | 100% Validated |
| `datasets/ai-models.json` | AI Models | 517,338 | 300 | 12 | 100% Validated |
| `datasets/developer-resources.json` | Developer Resources | 711,332 | 300 | 12 | 100% Validated |
| **Total Canonical Inventory** | **3 Registries** | **1,851,819** | **1,003** | **38 Unique** | **0 Errors, 0 Collisions** |

---

## 2. Dataset Top-Level Structure

Every canonical dataset adheres to a standardized root envelope:

```json
{
  "_meta": {
    "registry": "ai-tools",
    "label": "AI Tools",
    "schema_version": "1.0.0",
    "dataset_version": "1.0.0",
    "last_migrated": "2026-11-06",
    "total_records": 403,
    "category_count": 14,
    "categories": [...]
  },
  "records": [...]
}
```

---

## 3. Dataset 1: AI Tools (`datasets/ai-tools.json`)

- **Total Records:** 403
- **File Size:** 623,149 bytes
- **Resource Type:** `AI Tool` (403 records, 100%)
- **Identifier Pattern:** `^[a-z0-9]+(-[a-z0-9]+)*$` (e.g. `chatgpt`, `midjourney`, `cursor`)
- **Canonical ID Pattern:** `ai_tool:{id}` (403 records, 100%)
- **Duplicate Identifiers:** 0
- **Missing Required Fields:** 0
- **Missing Official URLs:** 0 (100% HTTPS)

### Category Distribution (14 Categories)

| Category Name | Record Count | Percentage of Tools |
|:---|:---|:---|
| Business & Enterprise | 99 | 24.57% |
| Coding & Development | 53 | 13.15% |
| Image & Design | 42 | 10.42% |
| Audio & Speech | 35 | 8.68% |
| Search & Research | 31 | 7.69% |
| Video | 31 | 7.69% |
| Infrastructure & Security | 30 | 7.44% |
| Productivity | 25 | 6.20% |
| Meetings & Communication | 14 | 3.47% |
| Data & Analytics | 13 | 3.23% |
| Writing & Content | 13 | 3.23% |
| Assistants & Chatbots | 6 | 1.49% |
| Industry & Specialized | 6 | 1.49% |
| Agents & Automation | 5 | 1.24% |
| **Total** | **403** | **100.00%** |

### Field Structure & Nullability (AI Tools)

| Field Name | Type | Presence in Records | Nullable / Optional | Description |
|:---|:---|:---|:---|:---|
| `id` | `string` | 403 / 403 | Required | Canonical lowercase slug identifier |
| `name` | `string` | 403 / 403 | Required | Human-readable product name |
| `description` | `string` | 403 / 403 | Required | Capability summary (10–1000 chars) |
| `category` | `string` | 403 / 403 | Required | Standardized taxonomy category |
| `source_category` | `string` | 403 / 403 | Optional | Upstream catalog categorization |
| `resource_type` | `string` | 403 / 403 | Required | Must be `"AI Tool"` |
| `official_url` | `string` | 403 / 403 | Required | Valid HTTPS link to official site |
| `pricing` | `string` | 403 / 403 | Required | Human-readable pricing tier description |
| `pricing_class` | `string` | 403 / 403 | Required | Standard enum (`free`, `freemium`, `paid`, `open_source`) |
| `license` | `string | null` | 403 / 403 | Nullable | Open-source or proprietary software license |
| `open_source` | `boolean` | 403 / 403 | Optional | Boolean flag |
| `self_hostable` | `boolean` | 403 / 403 | Optional | Boolean flag |
| `signup_required` | `boolean | null`| 403 / 403 | Nullable | Indicates if account registration is needed |
| `tags` | `array[string]`| 403 / 403 | Required | Search and indexing keywords |
| `icon` | `string | null` | 403 / 403 | Nullable | Resource visual icon identifier or URL |
| `verified` | `string` | 403 / 403 | Required | Date stamp (`YYYY-MM-DD`) |
| `status` | `string` | 403 / 403 | Required | Enum (`verified`, `active`, `deprecated`) |
| `evidence` | `array[list]` | 403 / 403 | Required | Array of `[label, url]` citation tuples |
| `canonical_id` | `string` | 403 / 403 | Required | Globally unique identifier `ai_tool:{id}` |
| `provider` | `string` | 403 / 403 | Optional | Organization or corporation behind tool |
| `platform` | `string | null` | 403 / 403 | Nullable | Deployment platforms (Web, iOS, Desktop) |

---

## 4. Dataset 2: AI Models (`datasets/ai-models.json`)

- **Total Records:** 300
- **File Size:** 517,338 bytes
- **Resource Type:** `AI Model` (300 records, 100%)
- **Identifier Pattern:** `^[a-z0-9]+(-[a-z0-9]+)*$` (e.g. `gpt-4o`, `claude-3-5-sonnet`, `llama-3-3-70b-instruct`)
- **Canonical ID Pattern:** `ai_model:{id}` (300 records, 100%)
- **Duplicate Identifiers:** 0
- **Missing Required Fields:** 0
- **Missing Official URLs:** 0 (100% HTTPS)

### Category Distribution (12 Categories)

| Category Name | Record Count | Percentage of Models |
|:---|:---|:---|
| Large Language Models | 74 | 24.67% |
| Vision & Multimodal | 56 | 18.67% |
| Embeddings & Rerankers | 29 | 9.67% |
| Small / Edge Models | 26 | 8.67% |
| Audio & Speech | 24 | 8.00% |
| Coding Models | 23 | 7.67% |
| Image Generation | 17 | 5.67% |
| Reasoning & CoT | 15 | 5.00% |
| Specialized Models | 10 | 3.33% |
| 3D Generation | 9 | 3.00% |
| Robotics & Embodied | 9 | 3.00% |
| Video Generation | 8 | 2.67% |
| **Total** | **300** | **100.00%** |

### Field Structure & Model-Specific Attributes (AI Models)

| Field Name | Type | Presence in Records | Description |
|:---|:---|:---|:---|
| `family` | `string` | 300 / 300 | Model architecture lineage (e.g. `GPT-4`, `Claude 3.5`, `Llama 3`) |
| `modalities` | `array[string]`| 300 / 300 | Input/output formats (`text`, `image`, `audio`, `video`, `code`) |
| `params` | `string | null` | 300 / 300 | Parameter scale (e.g. `70B`, `8B`, `None` for proprietary API) |
| `context` | `string | null` | 300 / 300 | Context window label (e.g. `128K`, `200K`, `1M`) |
| `context_k` | `integer | null`| 300 / 300 | Quantitative context token limit in thousands (e.g. 128, 200, 1000) |
| `open_weights` | `boolean` | 300 / 300 | Indicates whether weights are publicly downloadable |
| `weights` | `string` | 300 / 300 | Weights distribution type (`Open Weights`, `Proprietary API`) |
| `moe` | `boolean` | 300 / 300 | Mixture-of-Experts architecture flag |
| `publisher` | `string` | 300 / 300 | Entity releasing the model (e.g. `OpenAI`, `Anthropic`, `Meta AI`) |

---

## 5. Dataset 3: Developer Resources (`datasets/developer-resources.json`)

- **Total Records:** 300
- **File Size:** 711,332 bytes
- **Identifier Pattern:** `^[a-z0-9]+(-[a-z0-9]+)*$` (e.g. `langchain`, `vllm`, `qdrant`, `ollama`)
- **Canonical ID Pattern:** `developer_resource:{id}` (300 records, 100%)
- **Duplicate Identifiers:** 0
- **Missing Required Fields:** 0
- **Missing Official URLs:** 0 (100% HTTPS)

### Category Distribution (12 Categories)

| Category Name | Record Count | Percentage of Resources |
|:---|:---|:---|
| Model Serving & Inference | 69 | 23.00% |
| Agent Frameworks | 40 | 13.33% |
| APIs, Gateways & Protocols | 35 | 11.67% |
| Developer Tooling & QA | 30 | 10.00% |
| Vector Databases & RAG | 29 | 9.67% |
| Evaluation & Observability | 28 | 9.33% |
| Fine-Tuning & Optimization | 19 | 6.33% |
| Local Runtimes | 14 | 4.67% |
| AI Security & Guardrails | 13 | 4.33% |
| Cloud & GPU Infrastructure | 13 | 4.33% |
| Data & Annotation | 7 | 2.33% |
| Robotics & Embodied AI | 3 | 1.00% |
| **Total** | **300** | **100.00%** |

### Resource Type Breakdown (Developer Resources)

| Resource Type | Count | Percentage |
|:---|:---|:---|
| Framework / SDK / Library | 95 | 31.67% |
| Developer Resource | 61 | 20.33% |
| Platform / Service | 58 | 19.33% |
| Inference Engine | 48 | 16.00% |
| Database / Index | 13 | 4.33% |
| Framework | 12 | 4.00% |
| SDK / Library | 8 | 2.67% |
| Desktop App / Runtime | 5 | 1.67% |
| **Total** | **300** | **100.00%** |

---

## 6. Verification and Evidence Distribution

Across all 1,003 records:
- **Status Value:** `verified` on 1,003 records (100%)
- **Verification Dates:** `2026-11-03` (948 records) and `2026-11-04` (55 records)
- **Evidence Citations:** Every record contains between 1 and 3 verified reference URLs.
  - 1 Evidence link: 377 records (37.59%)
  - 2 Evidence links: 515 records (51.35%)
  - 3 Evidence links: 111 records (11.07%)
  - Total Evidence Links: 1,740 valid external reference citations.
- **Cross-Registry ID Collisions:** 0 (Every identifier across all three datasets is globally disjoint).
