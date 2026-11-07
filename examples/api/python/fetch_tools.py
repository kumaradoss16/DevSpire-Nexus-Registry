#!/usr/bin/env python3
"""
DevSpire Nexus Registry — Python Requests Static API Example
Demonstrates querying the static JSON API over HTTP without using the local SDK.
"""

import urllib.request
import json

API_BASE_URL = "https://raw.githubusercontent.com/kumaradoss16/DevSpire-Nexus-Registry/main/api/v1"


def main():
    print("Fetching AI Models from DevSpire Nexus Registry...")
    url = f"{API_BASE_URL}/models.json"

    req = urllib.request.Request(
        url,
        headers={"User-Agent": "DevSpireNexusRegistry-Example/1.0", "Accept": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        models = data.get("items", [])
        meta = data.get("_meta", {})
        print(f"Successfully retrieved {len(models)} models! (API version: {meta.get('api_version')})\n")

        # 1. Inspect a model record
        sample = next((m for m in models if m.get("id") == "gpt-4o"), models[0])
        print(f"Model: {sample.get('name')} (Family: {sample.get('family', 'N/A')})")
        print(f"URL:   {sample.get('official_url')}")
        print(f"Context Window: {sample.get('context', 'N/A')}")
        print(f"Weights: {sample.get('weights')} (Open Weights: {sample.get('open_weights')})")

        # 2. Filter open weights models
        open_models = [m for m in models if m.get("open_weights") is True]
        print(f"\nTotal Open-Weights Models: {len(open_models)} / {len(models)}")
        print("Top 3 Open Weights Models:")
        for m in open_models[:3]:
            print(f"  • {m.get('name')} ({m.get('id')})")

    except Exception as e:
        print(f"Error fetching API data: {e}")


if __name__ == "__main__":
    main()
