# DevSpire Nexus Registry — Static API Practical Examples

Practical, tested integration examples demonstrating how to consume the DevSpire Nexus Registry across languages and tools.

---

## 1. JavaScript / TypeScript Fetch Example

Fetch and filter AI Tools directly in the browser or Node.js runtime:

```javascript
const API_BASE = "https://raw.githubusercontent.com/kumaradoss16/DevSpire-Nexus-Registry/main/api/v1";

async function getCodingTools() {
  const res = await fetch(`${API_BASE}/tools.json`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);

  const data = await res.json();
  const codingTools = data.items.filter(item => item.category === "Coding & Development");
  
  console.log(`Found ${codingTools.length} coding tools.`);
  return codingTools;
}
```

*Executable script:* [`examples/api/javascript/fetch_tools.js`](file:///H:/DevSpire-Nexus-Registry/examples/api/javascript/fetch_tools.js)

---

## 2. Python Requests Example

Query AI Models using standard HTTP without installing the local SDK:

```python
import urllib.request
import json

url = "https://raw.githubusercontent.com/kumaradoss16/DevSpire-Nexus-Registry/main/api/v1/models.json"
req = urllib.request.Request(url, headers={"User-Agent": "MyAgent/1.0"})

with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode("utf-8"))

models = data.get("items", [])
print(f"Loaded {len(models)} models.")
```

*Executable script:* [`examples/api/python/fetch_tools.py`](file:///H:/DevSpire-Nexus-Registry/examples/api/python/fetch_tools.py)

---

## 3. Shell / cURL Direct Download & Checksum Verification

Download and verify data integrity in Unix bash / CI pipelines:

```bash
# 1. Download manifest and endpoint
curl -sSL "https://raw.githubusercontent.com/kumaradoss16/DevSpire-Nexus-Registry/main/api/v1/catalog.json" -o catalog.json
curl -sSL "https://raw.githubusercontent.com/kumaradoss16/DevSpire-Nexus-Registry/main/api/v1/tools.json" -o tools.json

# 2. Compute SHA-256 hash
sha256sum tools.json
```

*Executable script:* [`examples/api/curl/download_registry.sh`](file:///H:/DevSpire-Nexus-Registry/examples/api/curl/download_registry.sh)

---

## 4. Release-Pinned Consumption Strategy

To avoid moving latest-version updates, pin downloads to immutable Git tags:

```text
https://raw.githubusercontent.com/kumaradoss16/DevSpire-Nexus-Registry/v1.0.0/api/v1/tools.json
```
Replacing `main` with `v1.0.0` guarantees that your application always receives an immutable, unchanging snapshot of the registry data.
