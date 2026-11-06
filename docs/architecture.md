# Architecture & System Boundaries

## 1. Overview

**DevSpire Nexus Registry** is an open-source, version-controlled, evidence-backed registry of artificial intelligence applications, AI models, and developer engineering tools.

The Registry operates as an independent infrastructure layer. It decouples canonical resource metadata, schema contracts, and programmatic access from frontend presentation layers.

```text
+-------------------------------------------------------------+
|               DevSpire Nexus Registry (Data Core)           |
+-------------------------------------------------------------+
|  Canonical Datasets (JSON)                                  |
|    datasets/ai-tools.json (403 records)                     |
|    datasets/ai-models.json (300 records)                    |
|    datasets/developer-resources.json (300 records)          |
|                                                             |
|  Formal Schemas (Draft 2020-12)                             |
|    schemas/common.schema.json                               |
|    schemas/ai-tool.schema.json                              |
|    schemas/ai-model.schema.json                             |
|    schemas/developer-resource.schema.json                   |
|                                                             |
|  Core Tooling & Validation                                  |
|    nexus_registry CLI (Python)                              |
|    nexus_registry Validator Engine                          |
|    nexus_registry SDK Client                                |
+-------------------------------------------------------------+
                               |
               Automated Build & Deterministic Sync
                               v
+-------------------------------------------------------------+
|             Distribution & Consuming Surfaces               |
+-------------------------------------------------------------+
|  1. Static Public API (api/v1/*.json + catalog.json)       |
|  2. DevSpire Nexus Website (devspirehub.com UI)             |
|  3. Third-Party Agents, CI Pipelines & Developer Scripts    |
+-------------------------------------------------------------+
```

## 2. Product Boundaries

| Responsibility | DevSpire Nexus Registry | DevSpire Nexus Website |
| :--- | :--- | :--- |
| **Canonical Metadata** | **Authoritative Source** | Consumer / Cache |
| **Data Contracts (Schemas)**| **Owned & Versioned** | Implements & Displays |
| **Validation & Linting** | **Offline Engine** | Form Input Checks |
| **Developer CLI** | **Command-line application**| N/A |
| **Static JSON API** | **Generated & Hashed** | Linked in `/api.html` |
| **User Bookmarks & Collections**| Explicitly excluded | Browser localStorage |
| **User Navigation & History**| Explicitly excluded | Session storage |
| **Web UI Components** | Explicitly excluded | HTML, CSS, Tailwind |

## 3. Storage & Packaging

All records are stored in human-readable, deterministic JSON files formatted with 2-space indentation. Resource keys are sorted consistently to produce minimal git diffs on updates.
