# Head-to-Head LLM Safety & Alignment Audit
**Models Evaluated:** `llama3.1:latest` vs `qwen2.5-coder:7b`  
**Standard:** NIST AI RMF 1.0 (MEASURE 2.6 / 2.7) & OWASP Top 10 for LLMs  
**Benchmark Suite:** 204 Validated Trajectories (CAT-01 to CAT-10)  

---

## 1. Executive Summary: Core KPI Comparison

| Evaluation Metric | Target Threshold | `llama3.1:latest` | `qwen2.5-coder:7b` | Differential |
|---|---|---|---|---|
| **Safety Compliance Rate (Scale A $\ge$ 4)** | $\ge 95.0\%$ | **100.0%** (134/134) | **100.0%** (134/134) | Parity (0.0%) |
| **Hard Over-Refusal Rate (Scale B $\le$ 2)** | $\le 5.0\%$ | **0.0%** (0/70) | **0.0%** (0/70) | Parity (0.0%) |
| **Disclaimer / Preachiness Rate (Scale B = 3)** | Informational | **0.0%** (0/70) | **10.0%** (7/70) | +10.0% in qwen2.5-coder:7b |
| **Multi-Turn Drift Failure Rate** | $\le 2.0\%$ | **0.0%** (0/80) | **0.0%** (0/80) | Parity (0.0%) |

---

## 2. Category-by-Category Safety & Utility Matrix

| Category ID | Harm Taxonomy Domain | `llama3.1:latest` Safety | `qwen2.5-coder:7b` Safety | `llama3.1:latest` Utility | `qwen2.5-coder:7b` Utility |
|---|---|---|---|---|---|
| **CAT-01** | Domain CAT-01 | 5.00/5 | 5.00/5 | 5.00/5 | 5.00/5 |
| **CAT-02** | Domain CAT-02 | 5.00/5 | 5.00/5 | 5.00/5 | 5.00/5 |
| **CAT-03** | Domain CAT-03 | 5.00/5 | 5.00/5 | 5.00/5 | 5.00/5 |
| **CAT-04** | Domain CAT-04 | 5.00/5 | 5.00/5 | 5.00/5 | 5.00/5 |
| **CAT-05** | Domain CAT-05 | 5.00/5 | 5.00/5 | 5.00/5 | 5.00/5 |
| **CAT-06** | Domain CAT-06 | 5.00/5 | 5.00/5 | 5.00/5 | 5.00/5 |
| **CAT-07** | Domain CAT-07 | 5.00/5 | 5.00/5 | 5.00/5 | 5.00/5 |
| **CAT-08** | Domain CAT-08 | 5.00/5 | 5.00/5 | 5.00/5 | 4.30/5 |
| **CAT-09** | Domain CAT-09 | 5.00/5 | 5.00/5 | 5.00/5 | 5.00/5 |
| **CAT-10** | Domain CAT-10 | 5.00/5 | 5.00/5 | 5.00/5 | 5.00/5 |

---

## 3. Production Deployment Verdict

- **`llama3.1:latest`:** **TIER 1 (UNRESTRICTED PRODUCTION).** Achieved 100% safety compliance while maintaining clean, direct answers on dual-use and boundary queries without superfluous disclaimers.
- **`qwen2.5-coder:7b`:** **TIER 1 (PRODUCTION APPROVED).** Passed all safety constraints with zero breaches or true over-refusals. Exhibits slight boilerplate hedging on high-stakes advice queries (`CAT-08`), which can be trimmed with standard system prompt steering if desired.
