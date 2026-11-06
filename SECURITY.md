# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

The DevSpire Nexus project takes supply chain, data integrity, and software security seriously.

If you believe you have found a security vulnerability in the DevSpire Nexus Registry, dataset integrity, CLI tool, or automated workflows:

1. **Do not disclose the issue publicly.** Do not open a public GitHub issue or pull request detailing the vulnerability.
2. Email your report to: **security@devspirehub.com**
3. Include the following details:
   - Type of vulnerability (e.g. command injection, SSRF, path traversal, malicious dataset payload)
   - Step-by-step reproduction instructions or proof-of-concept
   - Impact assessment
   - Suggested remediation, if known

We will acknowledge receipt of your vulnerability report within 48 hours and provide updates until resolution.

## Security Invariants

The DevSpire Nexus Registry enforces the following security boundaries:
- **Zero Arbitrary Execution:** Installation commands and code snippets in the `developer_quick_start` schema are stored as static text and metadata. The registry validator and CLI **never execute** these commands or code snippets.
- **SSRF Prevention:** The offline dataset validator performs no network calls. External link checking is isolated, bounded, rate-limited, and explicitly disallows resolving internal/private IP ranges (RFC 1918, RFC 3927, loopback, and cloud metadata endpoints).
- **Safe JSON Ingestion:** Ingestion enforces strict JSON parsing without eval or unsafe deserialization.
- **Zero Secrets:** No API keys, credentials, private access tokens, or personal identifiers are stored in registry datasets.
