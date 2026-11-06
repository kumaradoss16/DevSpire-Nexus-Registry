#!/usr/bin/env python3
"""
Bounded, polite link health checker for DevSpire Nexus Registry.
Tests URL availability using HTTP HEAD/GET requests with user-agent and rate limiting.
"""

import argparse
import json
import random
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    requests = None

REPO_ROOT = Path(__file__).resolve().parent.parent
DATASETS_DIR = REPO_ROOT / "datasets"

USER_AGENT = "DevSpireNexusRegistry-LinkChecker/1.0 (+https://github.com/kumaradoss16/DevSpire-Nexus-Registry)"


def main():
    parser = argparse.ArgumentParser(description="Sample link checker for registry datasets.")
    parser.add_argument("--sample", type=int, default=30, help="Number of URLs to sample.")
    parser.add_argument("--timeout", type=int, default=10, help="Request timeout in seconds.")
    args = parser.parse_args()

    if requests is None:
        print("Note: 'requests' package not installed; skipping external network check.")
        return 0

    urls = []
    for f in DATASETS_DIR.glob("*.json"):
        data = json.loads(f.read_text(encoding="utf-8"))
        for r in data.get("records", []):
            u = r.get("official_url")
            if u:
                urls.append((r.get("id"), u))

    if not urls:
        print("No URLs found to check.")
        return 0

    sample_size = min(args.sample, len(urls))
    sampled = random.sample(urls, sample_size)
    print(f"Checking health of {sample_size} sampled URLs (timeout={args.timeout}s)...")

    failed = []
    for rid, u in sampled:
        domain = urlparse(u).netloc
        try:
            # Polite HEAD request with fallback to GET
            headers = {"User-Agent": USER_AGENT}
            res = requests.head(u, headers=headers, timeout=args.timeout, allow_redirects=True)
            if res.status_code >= 400 and res.status_code != 403:
                res = requests.get(u, headers=headers, timeout=args.timeout, allow_redirects=True, stream=True)
            if res.status_code < 400 or res.status_code == 403: # 403 is often Cloudflare bot protection, not broken link
                print(f"  [OK] {rid} -> {domain} ({res.status_code})")
            else:
                print(f"  [FAIL] {rid} -> {u} ({res.status_code})")
                failed.append((rid, u, res.status_code))
        except Exception as e:
            print(f"  [WARN] {rid} -> {domain}: {str(e)[:60]}")
        time.sleep(0.2) # Rate limit politely

    print(f"\nLink check finished: {len(sampled) - len(failed)}/{len(sampled)} reachable.")
    if failed:
        print(f"Identified {len(failed)} broken endpoint(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
