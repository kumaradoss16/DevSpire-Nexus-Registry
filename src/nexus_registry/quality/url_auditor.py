"""
URL syntax and bounded network reachability auditor for DevSpire Nexus Registry.
Separates deterministic local syntax validation from optional live network health checks.
"""

import re
import time
import urllib.parse
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

try:
    import urllib.request as urllib_request
    import urllib.error as urllib_error
except ImportError:
    urllib_request = None
    urllib_error = None

URL_SYNTAX_PATTERN = re.compile(
    r"^https?://"  # scheme
    r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # domain...
    r"localhost|"  # localhost...
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
    r"(?::\d+)?"  # optional port
    r"(?:/?|[/?]\S+)$", re.IGNORECASE
)

USER_AGENT = "DevSpireNexusRegistry-QualityAuditor/1.0 (+https://github.com/kumaradoss16/DevSpire-Nexus-Registry)"


class NetworkStatus(str, Enum):
    OK_200 = "200_ok"
    REDIRECT_3XX = "redirect_3xx"
    FORBIDDEN_403 = "forbidden_403"
    NOT_FOUND_404 = "not_found_404"
    RATE_LIMITED_429 = "rate_limited_429"
    SERVER_ERROR_5XX = "server_error_5xx"
    TIMEOUT = "timeout"
    CONNECTION_FAILED = "connection_failed"
    SKIPPED = "skipped"
    UNKNOWN = "unknown"


@dataclass
class URLAuditResult:
    url: str
    is_syntactically_valid: bool
    scheme: str = ""
    domain: str = ""
    network_status: NetworkStatus = NetworkStatus.SKIPPED
    http_code: Optional[int] = None
    error_message: Optional[str] = None
    latency_ms: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "url": self.url,
            "is_syntactically_valid": self.is_syntactically_valid,
            "scheme": self.scheme,
            "domain": self.domain,
            "network_status": self.network_status.value,
            "http_code": self.http_code,
            "error_message": self.error_message,
            "latency_ms": self.latency_ms,
        }


class URLAuditor:
    """Audits URL syntax and provides optional bounded network reachability checks."""

    @classmethod
    def validate_syntax(cls, url: Optional[str]) -> Tuple[bool, str, str]:
        """Check RFC 3986 syntax and return (is_valid, scheme, domain)."""
        if not url or not isinstance(url, str):
            return False, "", ""
        clean = url.strip()
        if not URL_SYNTAX_PATTERN.match(clean):
            return False, "", ""
        try:
            parsed = urllib.parse.urlparse(clean)
            scheme = parsed.scheme.lower()
            domain = parsed.netloc.lower()
            if scheme not in ("http", "https"):
                return False, scheme, domain
            if not domain:
                return False, scheme, domain
            return True, scheme, domain
        except Exception:
            return False, "", ""

    def audit_record_urls(
        self, record: Dict[str, Any], check_network: bool = False, timeout: int = 10
    ) -> List[URLAuditResult]:
        """Audit all URLs in a record (official_url, evidence links, repo/docs)."""
        results: List[URLAuditResult] = []
        urls_to_check = []

        if record.get("official_url"):
            urls_to_check.append(record["official_url"])
        if record.get("repository_url"):
            urls_to_check.append(record["repository_url"])
        if record.get("documentation_url"):
            urls_to_check.append(record["documentation_url"])

        for ev in record.get("evidence", []):
            if isinstance(ev, (list, tuple)) and len(ev) == 2 and isinstance(ev[1], str):
                urls_to_check.append(ev[1])

        # Deduplicate per record
        seen = set()
        for u in urls_to_check:
            if u not in seen:
                seen.add(u)
                valid, scheme, domain = self.validate_syntax(u)
                res = URLAuditResult(url=u, is_syntactically_valid=valid, scheme=scheme, domain=domain)
                if check_network and valid:
                    self._check_network(res, timeout)
                results.append(res)

        return results

    def _check_network(self, audit_res: URLAuditResult, timeout: int = 10):
        """Execute a polite, bounded HTTP HEAD/GET probe."""
        if urllib_request is None:
            audit_res.network_status = NetworkStatus.SKIPPED
            audit_res.error_message = "urllib.request unavailable"
            return

        start_time = time.time()
        req = urllib_request.Request(
            audit_res.url,
            headers={"User-Agent": USER_AGENT, "Accept": "*/*"},
            method="HEAD"
        )

        try:
            with urllib_request.urlopen(req, timeout=timeout) as response:
                audit_res.http_code = response.status
                audit_res.latency_ms = round((time.time() - start_time) * 1000, 2)
                if response.status == 200:
                    audit_res.network_status = NetworkStatus.OK_200
                elif 300 <= response.status < 400:
                    audit_res.network_status = NetworkStatus.REDIRECT_3XX
                else:
                    audit_res.network_status = NetworkStatus.OK_200
        except urllib_error.HTTPError as e:
            audit_res.http_code = e.code
            audit_res.latency_ms = round((time.time() - start_time) * 1000, 2)
            if e.code == 403:
                audit_res.network_status = NetworkStatus.FORBIDDEN_403
            elif e.code == 404:
                audit_res.network_status = NetworkStatus.NOT_FOUND_404
            elif e.code == 429:
                audit_res.network_status = NetworkStatus.RATE_LIMITED_429
            elif e.code >= 500:
                audit_res.network_status = NetworkStatus.SERVER_ERROR_5XX
            else:
                audit_res.network_status = NetworkStatus.UNKNOWN
            audit_res.error_message = f"HTTP {e.code}: {e.reason}"
        except urllib_error.URLError as e:
            audit_res.latency_ms = round((time.time() - start_time) * 1000, 2)
            if "timed out" in str(e.reason).lower():
                audit_res.network_status = NetworkStatus.TIMEOUT
            else:
                audit_res.network_status = NetworkStatus.CONNECTION_FAILED
            audit_res.error_message = str(e.reason)
        except Exception as e:
            audit_res.latency_ms = round((time.time() - start_time) * 1000, 2)
            audit_res.network_status = NetworkStatus.CONNECTION_FAILED
            audit_res.error_message = str(e)
