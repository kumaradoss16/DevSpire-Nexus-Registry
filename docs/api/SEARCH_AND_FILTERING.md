# DevSpire Nexus Registry — Search & Filtering Specification

**Specification Version:** 1.0.0  
**Effective Date:** 2026-11-07  
**Scope:** Search capabilities, tokenization, case-normalization, client-side execution, and SDK filtering behavior.

---

## 1. Architectural Model: Client-Side & SDK Execution

DevSpire Nexus Registry is distributed as **static, pre-rendered JSON files** without dynamic query servers:

- **Static JSON API:** Endpoints (`/api/v1/tools.json`, etc.) return the complete, canonical collection of records. Filtering and search are performed **client-side** in the consumer's application (browser, script, or agent).
- **Python SDK:** Provides native, high-performance in-memory search and filtering via `client.search()`.

---

## 2. Python SDK Search Capabilities

The SDK method `RegistryClient.search()` provides flexible query execution:

```python
results = client.search(
    query="vector database",
    registry="developer",        # Optional: "tools", "models", "developer"
    category="Vector Databases & RAG", # Optional: exact category name
    limit=10                     # Optional: max results (default: 20)
)
```

### Search Matching Behavior
1. **Searchable Fields:** The search engine indexes:
   - `name` (Resource Title)
   - `description` (Summary Text)
   - `category` (Taxonomy Classification)
   - `resource_type` (Entity Type)
   - `tags` (Keyword Array)
2. **Case Normalization:** All queries and target strings are converted to lowercase before evaluation (`query.lower() in haystack.lower()`).
3. **Sub-token Matching:** Partial matches are supported (e.g. searching `"lang"` matches `"LangChain"` and `"SGLang"`).
4. **Ordering & Performance:** Matches are evaluated sequentially; results are bounded by `limit`. Full catalog evaluation executes in under **2 milliseconds**.

---

## 3. Client-Side JavaScript Filtering Example

In browser or Node.js environments:

```javascript
// Filter tools by category and search keyword
function filterTools(tools, category, query) {
  const q = query.toLowerCase().trim();
  return tools.filter(tool => {
    const matchesCategory = !category || tool.category.toLowerCase() === category.toLowerCase();
    const haystack = `${tool.name} ${tool.description} ${tool.tags.join(" ")}`.toLowerCase();
    const matchesQuery = !q || haystack.includes(q);
    return matchesCategory && matchesQuery;
  });
}
```
