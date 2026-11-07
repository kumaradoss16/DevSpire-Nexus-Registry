"""
Duplicate and identity integrity auditor for DevSpire Nexus Registry.
Detects duplicate identifiers, slugs, canonical IDs, and classifies shared/conflicting URLs.
"""

import urllib.parse
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple


class DuplicateClassification(str, Enum):
    EXACT_DUPLICATE = "exact_duplicate"
    PROBABLE_DUPLICATE = "probable_duplicate"
    SHARED_LEGITIMATE_URL = "shared_legitimate_url"
    POTENTIAL_CONFLICT = "potential_conflict"


@dataclass
class DuplicateFinding:
    normalized_url: str
    records: List[Dict[str, str]]  # list of {"registry": reg, "id": id, "name": name, "raw_url": url}
    classification: DuplicateClassification
    reason: str
    recommended_action: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "normalized_url": self.normalized_url,
            "classification": self.classification.value,
            "reason": self.reason,
            "recommended_action": self.recommended_action,
            "records": self.records,
        }


@dataclass
class UniquenessReport:
    total_records: int = 0
    duplicate_ids: List[Dict[str, Any]] = field(default_factory=list)
    cross_registry_id_collisions: List[Dict[str, Any]] = field(default_factory=list)
    duplicate_canonical_ids: List[Dict[str, Any]] = field(default_factory=list)
    url_findings: List[DuplicateFinding] = field(default_factory=list)

    @property
    def has_identity_conflicts(self) -> bool:
        return (
            len(self.duplicate_ids) > 0 or
            len(self.cross_registry_id_collisions) > 0 or
            len(self.duplicate_canonical_ids) > 0
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_records": self.total_records,
            "has_identity_conflicts": self.has_identity_conflicts,
            "duplicate_id_count": len(self.duplicate_ids),
            "duplicate_ids": self.duplicate_ids,
            "cross_registry_collision_count": len(self.cross_registry_id_collisions),
            "cross_registry_id_collisions": self.cross_registry_id_collisions,
            "duplicate_canonical_id_count": len(self.duplicate_canonical_ids),
            "duplicate_canonical_ids": self.duplicate_canonical_ids,
            "shared_url_count": len(self.url_findings),
            "url_findings": [f.to_dict() for f in self.url_findings],
        }


class UniquenessChecker:
    """Audits record identities and URL uniqueness across canonical registries."""

    TRACKING_PARAMS = {
        "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
        "ref", "source", "fbclid", "gclid", "msclkid"
    }

    KNOWN_PROBABLE_DUPLICATES = {
        ("cohere-rerank-3", "cohere-rerank-v3"),
        ("cogvideox", "cogvideox-5b"),
        ("tensorrt-llm-triton", "tensorrt-llm-backend"),
        ("cutlass", "nvidia-cutlass"),
        ("triton-client", "triton-inference-client"),
        ("safetensors", "huggingface-safetensors"),
        ("tokenizers", "huggingface-tokenizers"),
    }

    @classmethod
    def normalize_url(cls, url: Optional[str]) -> str:
        """Normalize URL for consistent comparison without altering semantic targets."""
        if not url:
            return ""
        try:
            parsed = urllib.parse.urlparse(url.strip())
            scheme = parsed.scheme.lower() or "https"
            netloc = parsed.netloc.lower()

            # Strip default ports
            if netloc.endswith(":443") and scheme == "https":
                netloc = netloc[:-4]
            elif netloc.endswith(":80") and scheme == "http":
                netloc = netloc[:-3]

            # Strip leading www.
            if netloc.startswith("www."):
                netloc = netloc[4:]

            # Strip trailing slash on path
            path = parsed.path.rstrip("/")

            # Filter out known tracking query parameters
            query_pairs = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
            filtered_query = [
                (k, v) for k, v in query_pairs if k.lower() not in cls.TRACKING_PARAMS
            ]
            clean_query = urllib.parse.urlencode(filtered_query)

            # Rebuild clean URL
            normalized = f"{scheme}://{netloc}{path}"
            if clean_query:
                normalized += f"?{clean_query}"
            return normalized
        except Exception:
            return url.strip().lower()

    def audit(self, registry_datasets: Dict[str, List[Dict[str, Any]]]) -> UniquenessReport:
        """Run complete within-registry and cross-registry identity and URL audit."""
        report = UniquenessReport()
        global_ids: Dict[str, List[str]] = {}
        global_canonical_ids: Dict[str, List[str]] = {}
        url_map: Dict[str, List[Dict[str, str]]] = {}

        total = 0
        for reg_name, records in registry_datasets.items():
            total += len(records)
            seen_local_ids: Set[str] = set()

            for r in records:
                rid = r.get("id", "")
                can_id = r.get("canonical_id", "")
                rname = r.get("name", "")
                raw_url = r.get("official_url", "")

                # 1. Local duplicate check
                if rid in seen_local_ids:
                    report.duplicate_ids.append({
                        "registry": reg_name,
                        "id": rid,
                        "name": rname
                    })
                seen_local_ids.add(rid)

                # 2. Global cross-registry ID check
                if rid in global_ids:
                    global_ids[rid].append(reg_name)
                else:
                    global_ids[rid] = [reg_name]

                # 3. Canonical ID check
                if can_id:
                    if can_id in global_canonical_ids:
                        global_canonical_ids[can_id].append(reg_name)
                    else:
                        global_canonical_ids[can_id] = [reg_name]

                # 4. URL mapping
                if raw_url:
                    norm_url = self.normalize_url(raw_url)
                    if norm_url not in url_map:
                        url_map[norm_url] = []
                    url_map[norm_url].append({
                        "registry": reg_name,
                        "id": rid,
                        "name": rname,
                        "raw_url": raw_url,
                    })

        report.total_records = total

        # Check cross-registry collisions
        for rid, regs in global_ids.items():
            if len(regs) > 1:
                report.cross_registry_id_collisions.append({
                    "id": rid,
                    "registries": regs
                })

        for can_id, regs in global_canonical_ids.items():
            if len(regs) > 1:
                report.duplicate_canonical_ids.append({
                    "canonical_id": can_id,
                    "registries": regs
                })

        # Classify shared URLs
        for norm_url, rec_list in url_map.items():
            if len(rec_list) > 1:
                classification, reason, action = self._classify_shared_url(rec_list, norm_url)
                report.url_findings.append(DuplicateFinding(
                    normalized_url=norm_url,
                    records=rec_list,
                    classification=classification,
                    reason=reason,
                    recommended_action=action
                ))

        return report

    def _classify_shared_url(
        self, records: List[Dict[str, str]], normalized_url: str
    ) -> Tuple[DuplicateClassification, str, str]:
        """Classify shared URLs based on domain patterns, identifiers, and publisher contexts."""
        r_ids = {r["id"] for r in records}
        r_names = {r["name"].lower() for r in records}

        # Check for known probable duplicates (same resource cataloged under variant slugs)
        for pair in self.KNOWN_PROBABLE_DUPLICATES:
            if set(pair).issubset(r_ids):
                return (
                    DuplicateClassification.PROBABLE_DUPLICATE,
                    f"Variant identifiers '{' vs '.join(pair)}' represent the exact same product at destination.",
                    "Review in Phase 2 for canonical alias migration. Retain both IDs until migration approved."
                )

        # Exact name match with different IDs
        if len(r_names) == 1 and len(records) > 1:
            return (
                DuplicateClassification.PROBABLE_DUPLICATE,
                f"Identical resource name '{list(r_names)[0]}' cataloged under different identifiers.",
                "Review candidate records for consolidation or alias linkage."
            )

        # Monorepos or model families (e.g. whisper checkpoints, gemini docs, flash-attention versions)
        is_monorepo_or_family = (
            "github.com" in normalized_url or
            "huggingface.co" in normalized_url or
            "ai.google.dev" in normalized_url or
            "modelcontextprotocol.io" in normalized_url or
            "qodo.ai" in normalized_url or
            "blackforestlabs.ai" in normalized_url
        )

        if is_monorepo_or_family:
            return (
                DuplicateClassification.SHARED_LEGITIMATE_URL,
                "Shared legitimate parent repository, vendor portal, or multi-checkpoint documentation hub.",
                "Preserve distinct records. Both represent legitimate individual entities."
            )

        return (
            DuplicateClassification.SHARED_LEGITIMATE_URL,
            "Multiple distinct resources from the same organization sharing a common root URL.",
            "Preserve records; verify that specific sub-paths or documentation links are provided in evidence."
        )
