# DevSpire Nexus Registry — Baseline Test Report

**Execution Date:** November 6, 2026, 18:52:43 IST  
**Environment:** Windows 11 / Python 3.13.13  
**Auditor:** Software Quality Assurance Engineer  
**Status:** Baseline Established (100% Pass Rate on Existing Tests)

---

## 1. Automated Unit Test Execution

### Command:
```bash
python -m unittest discover -s H:\DevSpire-Nexus-Registry\tests -v
```

### Results Summary:
- **Discovered Tests:** 26
- **Passed:** 26
- **Failed:** 0
- **Skipped:** 0
- **Errors:** 0
- **Duration:** 0.432s

### Suite Breakdown:

| Test File | Test Method | Target | Result | Duration |
|---|---|---|---|---|
| `test_cli.py` | `test_cli_categories` | Categories subcommand | **PASS** | 0.04s |
| `test_cli.py` | `test_cli_info` | Info metadata lookup | **PASS** | 0.04s |
| `test_cli.py` | `test_cli_quickstart` | Quick Start formatted output | **PASS** | 0.04s |
| `test_cli.py` | `test_cli_search` | Keyword search query | **PASS** | 0.04s |
| `test_cli.py` | `test_cli_stats` | Registry summary metrics | **PASS** | 0.04s |
| `test_cli.py` | `test_cli_validate` | Schema validation CLI | **PASS** | 0.04s |
| `test_cli.py` | `test_cli_version` | Version output | **PASS** | 0.01s |
| `test_client.py` | `test_categories_and_stats` | SDK category & stat methods | **PASS** | 0.03s |
| `test_client.py` | `test_client_loads_datasets` | In-memory dataset caching | **PASS** | 0.03s |
| `test_client.py` | `test_get_quickstart` | SDK Quick Start parsing | **PASS** | 0.03s |
| `test_client.py` | `test_get_resource_by_id` | Slug ID indexed lookup | **PASS** | 0.03s |
| `test_client.py` | `test_search_resources` | Multi-registry keyword search | **PASS** | 0.03s |
| `test_datasets.py`| `test_global_id_uniqueness` | 1,003 global unique IDs check | **PASS** | 0.08s |
| `test_datasets.py`| `test_https_urls` | Verified HTTPS protocol check | **PASS** | 0.06s |
| `test_datasets.py`| `test_quickstart_contract` | 32 verified quick starts check | **PASS** | 0.05s |
| `test_datasets.py`| `test_record_counts` | Exact 403 / 300 / 300 counts | **PASS** | 0.04s |
| `test_datasets.py`| `test_required_common_fields` | Required non-null attributes | **PASS** | 0.05s |
| `test_datasets.py`| `test_slug_format` | Strict kebab-case regex match | **PASS** | 0.05s |
| `test_schemas.py` | `test_common_schema_properties` | Base contract definitions | **PASS** | 0.01s |
| `test_schemas.py` | `test_schema_files_exist` | 4 schema files presence | **PASS** | 0.01s |
| `test_schemas.py` | `test_schemas_are_valid_json` | Draft 2020-12 valid JSON syntax | **PASS** | 0.01s |
| `test_schemas.py` | `test_specialized_schemas_require_base`| allOf common inheritance | **PASS** | 0.01s |
| `test_validator.py`| `test_canonical_datasets_pass_validation` | 1,003 records pass validator | **PASS** | 0.35s |
| `test_validator.py`| `test_catches_invalid_slug` | Invalid slug rejection | **PASS** | 0.01s |
| `test_validator.py`| `test_catches_invalid_url_protocol` | Non-HTTP/S URL rejection | **PASS** | 0.01s |
| `test_validator.py`| `test_catches_missing_required_fields`| Missing field error detection | **PASS** | 0.01s |

---

## 2. CLI Execution Baseline

| Command | Status | Output Verification |
|---|---|---|
| `nexus-registry version` | **PASS (code 0)** | Prints `nexus-registry 1.0.0` |
| `nexus-registry stats` | **PASS (code 0)** | Prints 1,003 total resources, 403 tools, 300 models, 300 dev resources |
| `nexus-registry validate` | **PASS (code 0)** | `PASS [OK] Errors: 0 \| Warnings: 0` |
| `nexus-registry search "ollama"` | **PASS (code 0)** | Returns matching models and dev resources |
| `nexus-registry quickstart langchain` | **PASS (code 0)** | Formats pip/uv/npm commands and Python usage pipe |

---

## 3. Package Build & Standalone Limitations

- **Wheel Build:** Succeeded (`nexus_registry-1.0.0-py3-none-any.whl`, 13.3 KB).
- **Standalone Failure:** Wheel archive inspection confirmed **zero JSON files bundled**.
- **Result:** Running `RegistryClient()` in a clean environment without repository files yields 0 records.

---

## 4. Website Regression Test Baseline

DevSpire Nexus website test suites executed to establish baseline integrity:
- `node "H:\Devspirehub AI\.qa\qa-quickstart.js"`: **333/333 checks passed**.
- `node "H:\Devspirehub AI\.qa\qa-dev.js"`: **81/81 checks passed** (all viewports 320px–1440px).
