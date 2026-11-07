# DevSpire Nexus Registry — SDK Installation Guide

---

## 1. Installation via Pip

Install the package directly from PyPI (or local wheel distribution):

```bash
# Standard installation
pip install nexus-registry

# Or with optional development/validation extras
pip install "nexus-registry[dev]"
```

---

## 2. Requirements & Compatibility

- **Python Version:** Python `>= 3.10` (Tested on 3.10, 3.11, 3.12, 3.13).
- **Runtime Dependencies:** **Zero.** The SDK requires only the Python standard library.
- **Platforms:** Windows, Linux, macOS (architecture independent `py3-none-any`).

---

## 3. Local Editable Installation (For Development)

If contributing or modifying datasets locally:

```bash
# Clone the repository
git clone https://github.com/kumaradoss16/DevSpire-Nexus-Registry.git
cd DevSpire-Nexus-Registry

# Install in editable mode
pip install -e .
```

---

## 4. Verification Smoke Test

Verify successful installation in your terminal:

```bash
python -c "import nexus_registry; print('nexus_registry version:', nexus_registry.__version__)"
nexus-registry version
```
