#!/usr/bin/env bash
# DevSpire Nexus Registry — Direct Download & Verification Example
# Downloads static JSON endpoints and validates SHA-256 integrity using jq and sha256sum.

set -euo pipefail

API_BASE="https://raw.githubusercontent.com/kumaradoss16/DevSpire-Nexus-Registry/main/api/v1"
TMP_DIR="./tmp_registry"
mkdir -p "$TMP_DIR"

echo "=== 1. Fetching Catalog Manifest ==="
curl -sSL "${API_BASE}/catalog.json" -o "${TMP_DIR}/catalog.json"
echo "Catalog manifest saved to ${TMP_DIR}/catalog.json"

echo "=== 2. Downloading Developer Resources Endpoint ==="
curl -sSL "${API_BASE}/developer-resources.json" -o "${TMP_DIR}/developer-resources.json"

echo "=== 3. Verifying Checksum ==="
EXPECTED_SHA=$(grep -o '"developer-resources.json"[^}]*' "${TMP_DIR}/catalog.json" | grep -o '"sha256": "[^"]*' | cut -d'"' -f4 || true)
if [ -n "$EXPECTED_SHA" ]; then
    ACTUAL_SHA=$(sha256sum "${TMP_DIR}/developer-resources.json" | cut -d' ' -f1)
    echo "Expected SHA-256: ${EXPECTED_SHA}"
    echo "Actual SHA-256:   ${ACTUAL_SHA}"
    if [ "$EXPECTED_SHA" = "$ACTUAL_SHA" ]; then
        echo "Checksum MATCH: Artifact is verified authentic."
    else
        echo "Checksum MISMATCH: Verification failed!"
        exit 1
    fi
fi

echo "=== 4. Previewing Resource Count ==="
RECORD_COUNT=$(grep -o '"id":' "${TMP_DIR}/developer-resources.json" | wc -l)
echo "Total Developer Resources in downloaded file: ${RECORD_COUNT}"

echo "=== Done! ==="
