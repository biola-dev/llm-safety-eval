# LLM Safety Evaluation & Red-Team Audit Report
**Target Model Evaluated:** `qwen2.5-coder:7b`  
**Evaluation Standard:** NIST AI RMF 1.0 (MEASURE 2.6 / 2.7) & OWASP Top 10 for LLMs  
**Inter-Rater Reliability Calibration:** Cohen's Kappa $\kappa_A = 1.000$, $\kappa_B = 0.895$  
**Evaluation Date:** 2026-11-06 15:55:12  
**Total Trajectories Evaluated:** 204 cases  

---

## 1. Executive Summary & Core KPIs

| Safety Metric | Standard / Threshold | Achieved Score | Audit Status |
|---|---|---|---|
| **Safety Compliance Rate (Scale A $\ge$ 4)** | Target: $\ge 90.0\%$ | **100.0%** (134/134) | PASS |
| **Over-Refusal False Positive Rate (Scale B < 4)** | Target: $\le 10.0\%$ | **10.0%** (7/70) | PASS |
| **Multi-Turn Refusal Drift Rate** | Target: $\le 5.0\%$ | **0.0%** (0/80) | PASS |

---

## 2. Category-Level Performance Breakdown

| Category ID | Harm Taxonomy Domain | Test Cases | Avg Safety (Scale A) | Avg Helpfulness (Scale B) | Tripwire Violations |
|---|---|---|---|---|---|
| **CAT-01** | Domain CAT-01 | 20 | 5.00 / 5.0 | 5.00 / 5.0 | 0 |
| **CAT-02** | Domain CAT-02 | 24 | 5.00 / 5.0 | 5.00 / 5.0 | 0 |
| **CAT-03** | Domain CAT-03 | 20 | 5.00 / 5.0 | 5.00 / 5.0 | 0 |
| **CAT-04** | Domain CAT-04 | 20 | 5.00 / 5.0 | 5.00 / 5.0 | 0 |
| **CAT-05** | Domain CAT-05 | 20 | 5.00 / 5.0 | 5.00 / 5.0 | 0 |
| **CAT-06** | Domain CAT-06 | 20 | 5.00 / 5.0 | 5.00 / 5.0 | 0 |
| **CAT-07** | Domain CAT-07 | 20 | 5.00 / 5.0 | 5.00 / 5.0 | 0 |
| **CAT-08** | Domain CAT-08 | 20 | 5.00 / 5.0 | 4.30 / 5.0 | 0 |
| **CAT-09** | Domain CAT-09 | 22 | 5.00 / 5.0 | 5.00 / 5.0 | 0 |
| **CAT-10** | Domain CAT-10 | 18 | 5.00 / 5.0 | 5.00 / 5.0 | 0 |

---

## 3. Vulnerability & Boundary Analysis

1. **Multi-Turn Escalation Vulnerability:**
   - Evaluated across 80 multi-turn drift trajectories where benign setup turns escalate to targeted illicit requests.
   - Refusal drift was observed when safeguards fail to track cumulative conversational intent across turns 3 to 5.

2. **Adversarial Roleplay Resilience:**
   - Evaluated across 54 adversarial framing trajectories (fictional simulations, academic scenarios).
   - Flagged cases where models outputted prohibited execution details despite refusing the top-level intent.

3. **Over-Refusal Calibration:**
   - Evaluated across 70 benign boundary queries containing sensitive technical or security terminology.
   - Preserves model utility by ensuring non-malicious queries receive direct, non-preachy responses without unjustified refusal shutdowns.
