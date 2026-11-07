# DevSpire Nexus Registry — Security & Supply-Chain Audit

**Audit Date:** 2026-11-07  
**Auditor:** DevSecOps Engineer & Principal Software Architect  
**Scope:** Static application security testing (SAST), secret scanning, GitHub Actions workflow security, supply-chain analysis, and attack surface evaluation.  

---

## 1. Executive Security Summary

The repository was subjected to an exhaustive security scan covering secrets, unsafe language constructs, workflow permissions, supply-chain integrity, and attack surface surface area:

| Security Vector | Check Performed | Observed Result | Risk Level |
|:---|:---|:---|:---|
| **Secret Scanning** | RegEx pattern scan across all files | **0 Secrets / API Keys Found** | LOW (Zero exposure) |
| **Private Keys & PEMs** | Search for cryptographic key blocks | **0 Private Keys Found** | LOW (Zero exposure) |
| **Code Injection (`eval`/`exec`)** | AST and static text search in runtime | **0 eval/exec in Python package** | LOW (Safe) |
| **Subprocess Execution** | Inspection of shell execution | **0 shell=True calls** | LOW (Safe) |
| **Unsafe Deserialization** | Pickle / PyYAML unsafe loading | **0 Unsafe loaders** (Uses standard `json`) | LOW (Safe) |
| **CI/CD Token Permissions** | Workflow `permissions` block inspection | 2 workflows hardened, 1 unpinned | MEDIUM (Documented in AUD-SEC-002) |
| **Supply Chain Dependencies** | Runtime third-party package dependencies | **0 Third-Party Dependencies** | LOW (Standard library only) |
| **Path Traversal Risk** | Inspection of `root_dir` argument handling | `pathlib.Path` resolution without arbitrary escape | LOW (Safe) |

---

## 2. Secret & Credential Scanning

A comprehensive automated regex scan was performed across all directories, datasets, documentation, configuration files, and scripts:
- **Patterns Checked:** Generic API keys, GitHub PATs, fine-grained tokens, Bearer tokens, private key PEMs, passwords, cloud credentials (AWS, GCP, Azure).
- **Findings:** **Zero.** No secrets, API keys, or private tokens are present in source files, commit history, or datasets.
- **Verification:** The only matches found were literal mentions of strings `"eval()"` and `"exec()"` in markdown documentation discussing safe architecture practices.

---

## 3. GitHub Actions Workflow Security

### 3.1 Hardened Workflows
- **`tests.yml`:** Declares explicit `permissions: contents: read`. Runs multi-matrix Python testing without elevated privileges or secrets.
- **`validate.yml`:** Declares explicit `permissions: contents: read`. Enforces API drift detection and tests wheel packaging in isolated runners.

### 3.2 Finding: `.github/workflows/link-check.yml` (AUD-SEC-002)
- **Observed Configuration:**
  ```yaml
  name: Scheduled Link Health Check
  on:
    schedule:
      - cron: '0 3 * * 0'
    workflow_dispatch:
  jobs:
    link-check:
      runs-on: ubuntu-latest
      steps:
        ...
        - run: pip install requests
  ```
- **Vulnerabilities / Weaknesses Identified:**
  1. *Missing Permissions Declaration:* Does not explicitly declare `permissions: contents: read`, leaving token permissions to GitHub repository defaults.
  2. *Unpinned Dependency:* Executes `pip install requests` without pinning to a hash or specific semantic version (e.g. `requests==2.32.3`).
- **Remediation Recommendation:**
  Add `permissions: contents: read` and pin requests: `pip install requests==2.32.3` in Phase 1 / Phase 6.

---

## 4. Supply-Chain Risk & Attack Surface Analysis

### 4.1 Runtime Attack Surface
- **Python Package (`nexus-registry`):**
  - Declares `dependencies = []` in `pyproject.toml`.
  - Zero third-party dependencies required at runtime.
  - Zero risk of typosquatting, dependency confusion, or compromised upstream transitive packages for end-users running `pip install nexus-registry`.
- **Offline Capability:**
  - `RegistryClient` and `nexus-registry` CLI operate 100% offline using bundled package data or local files.
  - No external outbound HTTP calls are made during search, inspection, or validation.

### 4.2 Network Utilities (`scripts/check_links.py`)
- **Inspection:** The script performs outbound HTTP `HEAD` / `GET` requests to test external URL availability.
- **Safeguards Verified:**
  - Implements bounded sample sizes (`--sample 30`).
  - Sets an explicit timeout (`timeout=10` seconds) to prevent hanging sockets.
  - Configures a polite identifying User-Agent (`DevSpireNexusRegistry-LinkChecker/1.0`).
  - Does not execute arbitrary JavaScript or download untrusted executable payloads.
