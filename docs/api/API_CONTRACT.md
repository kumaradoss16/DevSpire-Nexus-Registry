# DevSpire Nexus Registry — Public API Contract Specification

**Contract Version:** 1.0.0 (API v1)  
**Effective Date:** 2026-11-07  
**Schema Standard:** JSON Schema Draft 2020-12  
**Scope:** Canonical contracts, data structures, guarantees, and nullability semantics for external consumers.

---

## 1. Canonical Registry Endpoints

The static JSON API exposes three primary resource datasets and two utility datasets under the `/api/v1/` namespace:

| Endpoint Path | Canonical Resource Type | Entity Schema | Record Count |
|:---|:---|:---|---:|
| `/api/v1/tools.json` | End-user AI Applications | `schemas/ai-tool.schema.json` | 403 |
| `/api/v1/models.json` | Foundation & Specialized Models | `schemas/ai-model.schema.json` | 300 |
| `/api/v1/developer-resources.json` | Frameworks, SDKs, Runtimes, APIs | `schemas/developer-resource.schema.json` | 300 |
| `/api/v1/categories.json` | Distinct Taxonomy Categories | `schemas/common.schema.json` | 38 |
| `/api/v1/stats.json` | Aggregate Metrics & Counts | Internal summary structure | Global |
| `/api/v1/catalog.json` | Cryptographic Manifest & Checksums | `schemas/common.schema.json` | Manifest |

---

## 2. Global Record Envelope & Metadata

Every primary registry endpoint returns an envelope containing metadata and the canonical `records` array:

```json
{
  "_meta": {
    "api_version": "v1",
    "schema_version": "1.0.0",
    "registry": "ai-tools",
    "total_records": 403,
    "license": "ODC-By 1.0",
    "documentation": "https://github.com/kumaradoss16/DevSpire-Nexus-Registry#readme"
  },
  "records": [ ... ]
}
```

---

## 3. Base Contract Properties (Common to All Resources)

Every canonical record in any registry implements the base contract defined in `schemas/common.schema.json`:

| Field Name | Type | Constraint / Format | Mandatory? | Description |
|:---|:---|:---|:---:|:---|
| `id` | `string` | Regex `^[a-z0-9]+(-[a-z0-9]+)*$` | **Yes** | Unique, immutable, lowercase slug identifier. |
| `name` | `string` | 2 to 100 characters | **Yes** | Canonical product or resource title. |
| `description` | `string` | 10 to 1000 characters | **Yes** | Technical capability summary. |
| `category` | `string` | Whitelisted in `_meta.categories` | **Yes** | Standardized taxonomy category. |
| `resource_type` | `string` | `"AI Tool"`, `"AI Model"`, etc. | **Yes** | Primary entity classification. |
| `official_url` | `string` | RFC 3986 URI (`https://...`) | **Yes** | Authoritative destination URL. |
| `pricing` | `string` | Free text label | **Yes** | Human-readable pricing summary. |
| `license` | `string \| null`| Standard identifier or `null` | **Yes** | Software license (e.g. `"MIT"`, `"Proprietary"`). |
| `tags` | `array[string]`| 1 to 20 keywords | **Yes** | Search and indexing tags. |
| `verified` | `string` | ISO-8601 Date (`YYYY-MM-DD`) | **Yes** | Verification date timestamp. |
| `status` | `string` | Enum: `verified`, `partially_verified`, `unverified`, `deprecated` | **Yes** | Editorial verification lifecycle status. |
| `evidence` | `array[tuple]` | Min 1 element: `[label, url]` | **Yes** | Traceable external verification citations. |
| `canonical_id` | `string` | Pattern `{prefix}:{id}` | **Yes** | Globally unique identifier (e.g. `ai_tool:chatgpt`). |

---

## 4. Registry-Specific Contract Extensions

### 4.1 AI Tools (`ai-tools.json`)
- `pricing_class` (`string`, required): Enum: `free`, `freemium`, `paid`, `open_source`, `usage_based`, `commercial`.
- `signup_required` (`boolean | null`, optional): Indicates if registration is required to use.
- `platform` (`string | null`, optional): Target environments (e.g. `"Web, iOS, Desktop"`).
- `icon` (`string | null`, optional): Frontend visual icon identifier.

### 4.2 AI Models (`ai-models.json`)
- `family` (`string`, required): Model architecture lineage (e.g. `"GPT-4"`, `"Llama 3"`).
- `modalities` (`array[string]`, required): Input/output formats (e.g. `["Text", "Image"]`).
- `params` (`string | null`, optional): Parameter scale (e.g. `"70B"`, `"8B"`, or `null` for closed APIs).
- `context` (`string | null`, optional): Context window label (e.g. `"128K"`).
- `context_k` (`integer | null`, optional): Quantitative token limit in thousands (e.g. `128`).
- `open_weights` (`boolean`, required): Indicates whether weights are publicly downloadable.
- `weights` (`string`, required): Weights availability type (e.g. `"Open Weights"`, `"Proprietary API"`).
- `moe` (`boolean`, required): Mixture-of-Experts architecture flag.

### 4.3 Developer Resources (`developer-resources.json`)
- `resource_subtype` (`string`, optional): Specific subtype (e.g. `"Framework"`, `"Inference Engine"`).
- `repository_url` (`string | null`, optional): Official GitHub/GitLab source repository link.
- `documentation_url` (`string | null`, optional): Official technical documentation portal link.
- `developer_quick_start` (`object | null`, optional): Verified quick-start guide containing:
  - `available` (`boolean`): Availability flag.
  - `package_name` (`string`): Package manager name.
  - `installation` (`array[object]`): Commands for `pip`, `uv`, `npm`, `pnpm`.
  - `examples` (`array[object]`): Tested code snippet, label, and expected output.

---

## 5. Representation of Null, Unknown, and Deprecated States

1. **Unknown / Not Disclosed:** Represented strictly as JSON `null`. Consumers should not assume `null` implies false or free.
2. **Empty Arrays:** Used only when an attribute is applicable but empty (e.g. `"tags": []`).
3. **Deprecated Resources:** Resources discontinued or replaced by upstream publishers are marked `status: "deprecated"`. They remain accessible at their original IDs to prevent broken links in external systems.

---

## 6. Identifier Stability Guarantees

- **Immutability:** Once published in a release, an `id` or `canonical_id` will **never be renamed or reassigned** to another resource.
- **Persistence:** Deprecated resources are retained with `status: "deprecated"` rather than deleted.
- **Case Sensitivity:** Identifiers are strictly lowercase alphanumeric strings with hyphens. Queries to the SDK are normalized automatically.
