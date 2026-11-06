# DevSpire Nexus Registry CLI Reference

`nexus-registry` is the command-line utility for inspecting, querying, and validating canonical datasets in the DevSpire Nexus Registry.

## Installation

```bash
# Install locally in development mode
pip install -e .

# Or run directly via Python module
python -m nexus_registry.cli --help
```

---

## Global Options

- `--version`: Show the CLI version and exit.
- `--root PATH`: Specify repository root directory (defaults to current repository root).

---

## Subcommands

### 1. `validate`
Performs offline verification against JSON Schemas, slug rules, and primary-source evidence requirements.

```bash
# Validate entire registry
nexus-registry validate

# Validate specific registry
nexus-registry validate --registry ai-tools
nexus-registry validate --registry ai-models
nexus-registry validate --registry developer-resources

# Output machine-readable JSON report
nexus-registry validate --json
```

**Exit Codes:**
- `0`: All datasets comply with schema rules (0 errors).
- `1`: Validation errors detected.

---

### 2. `search`
Search canonical resources by query keyword across name, description, tags, and category.

```bash
# General search
nexus-registry search "ollama"

# Filter by registry and category
nexus-registry search "embeddings" --registry developer --category "Embeddings & Rerankers"

# Limit results
nexus-registry search "vision" --limit 5
```

---

### 3. `info`
Inspect full metadata, evidence sources, and Quick Start availability for a resource slug ID.

```bash
nexus-registry info chatgpt
nexus-registry info gpt-4o
nexus-registry info langchain
```

---

### 4. `quickstart`
Print verified Developer Quick Start reference containing installation commands, official documentation links, GitHub repository, and code example.

```bash
nexus-registry quickstart langchain
nexus-registry quickstart qdrant
nexus-registry quickstart vllm
```

---

### 5. `categories`
List distinct taxonomy categories in the registry.

```bash
nexus-registry categories
nexus-registry categories --registry tools
nexus-registry categories --registry models
nexus-registry categories --registry developer
```

---

### 6. `stats`
Display catalog summary metrics, verification totals, and registry distributions.

```bash
nexus-registry stats
```
