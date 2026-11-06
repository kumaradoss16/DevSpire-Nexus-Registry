# Attribution & Citation Guidelines

When using, redistributing, or publishing works derived from the **DevSpire Nexus Registry** datasets, please include attribution as required by the ODC-By v1.0 license.

---

## 1. Web Applications and Software

Include a visible hyperlink or footer reference:

```html
Data powered by <a href="https://github.com/kumaradoss16/DevSpire-Nexus-Registry">DevSpire Nexus Registry</a> (DevSpireHub.com)
```

Or text credit:
> "Data source: DevSpire Nexus Registry (https://github.com/kumaradoss16/DevSpire-Nexus-Registry), licensed under ODC-By 1.0."

---

## 2. Academic & Research Publications

Please cite the repository as specified in [`CITATION.cff`](CITATION.cff):

### BibTeX:
```bibtex
@misc{devspire_nexus_registry_2026,
  author = {Kumaradoss and DevSpire Nexus Contributors},
  title = {DevSpire Nexus Registry: Canonical Data Infrastructure for AI and Software Engineering},
  year = {2026},
  publisher = {GitHub},
  howpublished = {\url{https://github.com/kumaradoss16/DevSpire-Nexus-Registry}}
}
```

### APA:
> Kumaradoss, & DevSpire Nexus Contributors. (2026). *DevSpire Nexus Registry: Canonical Data Infrastructure for AI and Software Engineering*. GitHub. https://github.com/kumaradoss16/DevSpire-Nexus-Registry

---

## 3. Automated Agents & AI Datasets

If you use this registry as training data, RAG retrieval context, or agent tools, provide attribution in your system documentation or API metadata:

```json
{
  "dataset_provenance": "DevSpire Nexus Registry",
  "repository": "https://github.com/kumaradoss16/DevSpire-Nexus-Registry",
  "license": "ODC-By 1.0"
}
```
