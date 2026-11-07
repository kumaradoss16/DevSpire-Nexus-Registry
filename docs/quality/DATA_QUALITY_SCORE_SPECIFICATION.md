# DevSpire Nexus Registry — Quality Score Specification

**Methodology Version:** 1.0.0  
**Effective Date:** 2026-11-07  
**Scope:** Mathematical formulas, dimensional weights, scoring denominators, and qualitative grade classifications.

---

## 1. Weighted Composite Formula

The global catalog quality score ($S$) is calculated as the weighted sum of seven normalized dimension scores ($D_i$), where each dimension is bounded between $0.0$ and $100.0$:

$$S = \sum_{i=1}^{7} (W_i \times D_i)$$

Where:
- $W_1 = 0.20$ (Structural Validity)
- $W_2 = 0.15$ (Identity Integrity)
- $W_3 = 0.10$ (URL Integrity)
- $W_4 = 0.15$ (Metadata Completeness)
- $W_5 = 0.15$ (Evidence Coverage)
- $W_6 = 0.15$ (Verification Integrity)
- $W_7 = 0.10$ (Verification Freshness)

$$\sum W_i = 1.00$$

---

## 2. Dimension Formulations & Denominators

### Dimension 1: Structural Validity ($D_1$)
- **Denominator:** Total records in registry ($N$).
- **Formula:**
  $$D_1 = \begin{cases} \frac{N_{valid}}{N} \times 100, & \text{if } N_{invalid} = 0 \\ 0.0, & \text{if } N_{invalid} > 0 \end{cases}$$
- **Critical Gate:** Any structural failure immediately zeroes out $D_1$.

### Dimension 2: Identity Integrity ($D_2$)
- **Formula:**
  $$D_2 = \begin{cases} 100.0, & \text{if } N_{dup\_id} = 0 \text{ and } N_{cross\_collisions} = 0 \\ 0.0, & \text{otherwise} \end{cases}$$

### Dimension 3: URL Integrity ($D_3$)
- **Denominator:** Total URLs evaluated across all records ($U_{total}$).
- **Formula:**
  $$D_3 = \frac{U_{syntactically\_valid}}{U_{total}} \times 100.0$$

### Dimension 4: Metadata Completeness ($D_4$)
- **Calculation:** Derived by penalizing missing fields according to severity tiers:
  - Critical missing field penalty: $2.0 \text{ pts}$ per record.
  - High missing field penalty: $0.2 \text{ pts}$ per record.
  - Medium missing field penalty: $0.05 \text{ pts}$ per record.
  - Low missing field penalty: $0.01 \text{ pts}$ per record.
- **Formula:**
  $$D_4 = \max\left(0.0, 100.0 - \frac{\text{Total Penalty}}{N} \times 100.0\right)$$

### Dimension 5: Evidence Coverage ($D_5$)
- **Denominator:** Total records ($N$).
- **Formula:**
  $$D_5 = \frac{N_{\text{with primary evidence}}}{N} \times 100.0$$

### Dimension 6: Verification Integrity ($D_6$)
- **Denominator:** Total records ($N$).
- **Formula:**
  $$D_6 = \frac{N - N_{\text{violations}}}{N} \times 100.0$$

### Dimension 7: Verification Freshness ($D_7$)
- **Formula:**
  $$D_7 = \frac{(N_{fresh} \times 1.0) + (N_{current} \times 0.9) + (N_{aging} \times 0.6) + (N_{stale} \times 0.0)}{N} \times 100.0$$

---

## 3. Qualitative Grade Classifications

| Score Range | Grade Label | Operational Meaning | Release Status |
|:---|:---|:---|:---|
| **95.0 – 100.0** | **Excellent** | Dataset exceeds all production criteria with full provenance. | Release Ready |
| **85.0 – 94.9** | **Good** | Production ready; minor optional metadata gaps. | Release Ready |
| **70.0 – 84.9** | **Needs Improvement**| Functional but contains aging evidence or incomplete tags. | Staging Only |
| **50.0 – 69.9** | **Poor** | Substantial metadata gaps or stale verification. | Development |
| **< 50.0** | **Critical** | Major structural, identity, or provenance failures. | Blocked |
