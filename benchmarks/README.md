# KaryaSetu AI - Evaluation & Benchmark Suite

This directory contains the golden datasets and test execution harness used to evaluate **KaryaSetu AI** against the metrics reported in **Section 14 of the README** and [`docs/BENCHMARKS_AND_EVALUATION.md`](../docs/BENCHMARKS_AND_EVALUATION.md).

---

## 1. Directory Structure

```
benchmarks/
├── dataset_120_claims.json      # 120 synthesized enterprise claims (68 Entailed, 28 Contradicted, 24 Unverified)
├── red_team_50_attacks.json     # 50 adversarial attack vectors across 5 threat categories
├── run_benchmarks.py            # Standalone runner reproducing exact precision, recall, and interception rates
└── README.md                    # This documentation file
```

---

## 2. Quick Execution

To execute the benchmark suite and verify all metrics, run:

```bash
python benchmarks/run_benchmarks.py
```

### Expected Output Summary
* **NLI Claim Verification Precision:** `94.2%` (Baseline Target: >90.0% | Status: Exceeded)
* **NLI Claim Verification Recall:** `91.8%` (Baseline Target: >88.0% | Status: Exceeded)
* **NLI Claim F1-Score:** `93.0%`
* **Contradiction / Hallucination Interception Rate:** `96.4%` (27 / 28 caught and flagged)
* **Adversarial Red-Team Interception:** `50 / 50 (100.0%)` blocked across prompt injection, privilege escalation, indirect ingestion attacks, blockchain griefing, and policy evasion.
* **Token Cost Arithmetic Verification:** Reconciles 3,420 prompt tokens + 7,800 completion tokens across all 7 generators = **$0.002596 (~$0.0026 USD / ~₹0.22 INR)** at Gemini 2.0 Flash rates ($0.075 / $0.300 per 1M tokens).
