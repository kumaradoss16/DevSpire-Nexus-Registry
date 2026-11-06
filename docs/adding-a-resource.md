# How to Add a Resource to DevSpire Nexus Registry

This guide explains how to format, validate, and submit a new resource entry.

---

## 1. Select the Correct Registry

| Registry | Target Scope | Example Resources |
|---|---|---|
| **AI Tools** (`datasets/ai-tools.json`) | End-user AI applications, SaaS platforms, web apps | ChatGPT, Claude, Midjourney, Cursor, v0 |
| **AI Models** (`datasets/ai-models.json`) | Foundation models, open weights, architectures | GPT-4o, Claude 3.5 Sonnet, Llama 3.1, FLUX.1 |
| **Developer Resources** (`datasets/developer-resources.json`) | SDKs, frameworks, vector databases, local runtimes | LangChain, Ollama, Qdrant, vLLM, LiteLLM |

---

## 2. Identifier Slug Rules

Every resource requires a globally unique slug identifier:
- Lowercase alphanumeric characters and single hyphens only: `^[a-z0-9]+(-[a-z0-9]+)*$`
- Must not collide with any existing record in ANY registry.
- Examples: `vllm`, `claude-3-5-sonnet`, `deepseek-r1`.

---

## 3. Minimum Record Format

### AI Tool Example:
```json
{
  "id": "my-tool",
  "name": "My Tool",
  "description": "Concise technical description of capability and scope (minimum 20 characters).",
  "category": "Coding & Development",
  "resource_type": "AI Tool",
  "official_url": "https://mytool.example.com",
  "pricing": "Freemium",
  "license": "Proprietary",
  "tags": ["Code-Generation", "IDE-Extension"],
  "verified": "2026-11-01",
  "status": "verified",
  "org": "Example Org",
  "canonical_id": "tool:my-tool",
  "evidence": [
    ["Official website", "https://mytool.example.com"],
    ["Documentation", "https://docs.mytool.example.com"]
  ]
}
```

### AI Model Example:
```json
{
  "id": "my-model-8b",
  "name": "My Model 8B",
  "description": "Open-weight foundation language model with instruction tuning.",
  "category": "Large Language Models",
  "resource_type": "AI Model",
  "official_url": "https://example.com/models/8b",
  "pricing": "Open Weights",
  "license": "Apache 2.0",
  "tags": ["Transformer", "Instruction-Tuned"],
  "verified": "2026-11-01",
  "status": "verified",
  "publisher": "Example Labs",
  "family": "MyModel",
  "weights": "open",
  "open_weights": true,
  "params": "8B",
  "context": "128K tokens",
  "context_k": 128,
  "moe": false,
  "modalities": ["Text"],
  "canonical_id": "model:my-model-8b",
  "evidence": [
    ["Hugging Face Model Card", "https://huggingface.co/example/my-model-8b"]
  ]
}
```

---

## 4. Local Validation

Before submitting your pull request, run:

```bash
nexus-registry validate
python scripts/generate_api.py
python -m unittest discover -s tests
```
