# DevSpire Nexus Registry Data Model

This document defines the schema taxonomy and data contracts governing all canonical resource records in DevSpire Nexus Registry.

## Common Resource Contract

Every resource in any registry implements the base contract defined in `schemas/common.schema.json`.

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | `string` | **Yes** | Lowercase kebab-case slug: `^[a-z0-9]+(-[a-z0-9]+)*$` |
| `canonical_id` | `string` | **Yes** | Namespaced global identifier (e.g. `tool:chatgpt`, `model:gpt-4o`) |
| `name` | `string` | **Yes** | Human-readable canonical product/model name |
| `description` | `string` | **Yes** | Concise technical description (min 10, max 1000 characters) |
| `category` | `string` | **Yes** | Normalized taxonomy category within the registry |
| `source_category` | `string \| null` | No | Original pre-normalization taxonomy tag |
| `resource_type` | `string` | **Yes** | `AI Tool`, `AI Model`, or `Developer Resource` |
| `official_url` | `string` | **Yes** | Verified HTTPS canonical URL |
| `pricing` | `string` | **Yes** | Pricing tier (e.g. `Open Source`, `Free`, `Freemium`, `Paid`) |
| `pricing_class` | `string \| null` | No | Normalized classification: `free`, `freemium`, `paid`, `open-source` |
| `license` | `string \| null` | No | License string (e.g. `Apache 2.0`, `MIT`, `Proprietary`) |
| `open_source` | `boolean \| null`| No | Whether source code is open under an OSI-approved license |
| `self_hostable` | `boolean \| null`| No | Whether resource can be run locally or self-hosted |
| `tags` | `array[string]` | **Yes** | Searchable technical tags |
| `icon` | `string \| null` | No | Relative path to local verified icon asset |
| `verified` | `string` | **Yes** | Verification date: `YYYY-MM-DD` |
| `status` | `string` | **Yes** | Verification status: `verified`, `partially_verified`, `deprecated` |
| `evidence` | `array[[label, url]]` | **Yes** | Primary source provenance pairs |

---

## Registry-Specific Contracts

### 1. AI Tools (`schemas/ai-tool.schema.json`)
- `org`: Developer or parent company organization.
- `platform`: Target operating platforms (`Web`, `Desktop`, `Mobile`, etc.).
- `hosting`: Hosting architecture (`Cloud`, `Self-hosted`, `Hybrid`).
- `initials`: Fallback two-letter monogram.

### 2. AI Models (`schemas/ai-model.schema.json`)
- `publisher`: Lab or vendor releasing the model weights or service.
- `family`: Model family / architecture series (e.g. `GPT`, `Claude`, `Llama`).
- `weights`: `open`, `closed`, `hybrid`, or `unspecified`.
- `open_weights`: Boolean indicating downloadable weights.
- `params`: Parameter size notation (e.g. `8B`, `70B`, `405B`).
- `context`: Context window length (e.g. `128K tokens`, `1M tokens`).
- `context_k`: Numeric context window length in thousands of tokens.
- `moe`: Boolean indicating Mixture-of-Experts routing.
- `modalities`: Supported input/output modalities (e.g. `["Text", "Vision"]`).

### 3. Developer Resources (`schemas/developer-resource.schema.json`)
- `resource_subtype`: Granular functional role (e.g. `Agent Framework`, `Vector Database`).
- `documentation_url`: Official technical documentation URL.
- `repository_url`: Open-source code repository URL.
- `programming_languages`: Supported languages (e.g. `["Python", "TypeScript"]`).
- `developer_quick_start`: Verified Quick Start reference object:
  - `available`: Boolean flag.
  - `package_name`: Package manager registry name.
  - `installation`: List of CLI commands (`pip`, `npm`, `uv`, `docker`, `curl`).
  - `documentation`: Official documentation URL and title.
  - `github`: Repository details (owner, repo, license).
  - `supported_languages`: SDK language support list.
  - `examples`: Executable code examples with prerequisites, env vars, and expected output.
