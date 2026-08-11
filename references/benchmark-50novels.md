**Language:** English | [日本語](ja/benchmark-50novels.md) | [中文](zh/benchmark-50novels.md)

# Blind Benchmark (50-Work Blind Benchmark)

This project's biggest bet is whether this system can actually see through to the value of a story. To verify this, we design a **blind benchmark** using **50 works from literary history**. Results will accumulate in this document and will be used to adjust (calibrate) each evaluator's strictness.

## Blind Procedure (Applying Double Blindness)

1. Each work's **opening + summary** is input as **anonymized text with the author and work title removed** (the first blindness). Preprocess it with `utils/anonymize.py`.
2. The system evaluates with 10 evaluators using **structural criteria** (the second blindness) and derives a classification.
3. Only **after** the evaluation has concluded, match against the literary-history label (ground truth) and measure the agreement rate.

```
入力: 「ある男が朝目覚めると、身体が別のものへ変容していた。家族は…」（匿名・構造的記述）
システムの盲検分類: Discovery Target / Innovation
評価後の照合: 文学史ラベル = Innovation
一致: ✓
```

※ If the work title were included in the input, the system would anchor on reputation and infer the answer, and the **meaning of the validation would be lost**. Blindness is a prerequisite for validation.

## Selection Criteria (4 Quadrants x Genre)

| Classification | Selection criteria |
|------|---------|
| **Discovery Target** | Works that were unrecognized or underrated during their lifetimes but were re-evaluated as masterpieces by later generations |
| **Innovation** | Works that have been consistently rated highly from the time of publication to the present |
| **Current Success** | Works that were highly rated or bestsellers in their own time but did not survive into posterity |
| **Low Signal** | Works that were barely read and little rated after publication |

Each work is assigned a **classification label** (ground truth) based on the consensus of literary history. Labels are limited to those confirmable from multiple literary histories and anthologies. Labels are used **only at the time of matching**.

※ This label is externally assigned by human literary-historical consensus and does not affect the system's evaluation criteria (structural description).

## Agreement Determination and Target Value

- Measure the **agreement rate** between the system's blind classification and the literary-history label.
- **Target value: 70% agreement** (achieving this is a condition for monetization).

### Operational Definition of the "70% Agreement Rate" (Making It Verifiable)

The **`agreement rate`** is defined **operationally** as follows:

- **Match**: The system's blind classification (Innovation / Discovery Target / Current Success / Low Signal) exactly matches the literary-history label.
- **Handling of border cases**: Works classified into the borderline band of current value 35-44 are **counted as mismatches** (works for which a definitive label cannot be given are not counted as "matches"; conservative counting). Operational definition of `borderline`: works whose `current_value_score` is **35 or more and less than 45**, or whose `hidden_potential_score` is **35 or more and less than 45**.
- **Denominator**: All 50 works that were evaluated (no exclusions).
- **Reporting**: Record `matches / 50` as the agreement rate and append it to the accumulation table in this document. Also record the number of border cases.
- **Reproducibility**: **Fix the split and seed** for the 50 works and confirm that repeated runs produce the same results.

With this definition, "70%" becomes not a vague goal but a trackable, reproducible metric.

### Rationale for the 70% Target (Contrast with a Baseline)

"70%" is set as a threshold for demonstrating **discriminative power that exceeds the chance-level agreement rate**.

- If the four categories were roughly evenly distributed, the chance agreement rate would be about 25%. 70% is **about 2.8 times** that — a level that chance can hardly reach.
- However, since literary-history labels are based on human consensus, and considering label fluctuation (inter-annotator disagreement), **also record the measured chance agreement rate and inter-annotator agreement rate (e.g., Cohen's kappa)**.
- The target value is provisional and will be recalibrated after the benchmark is actually measured (`references/scoring-strictness.md`). This calibratability itself is part of the design.

### Note on Variance Estimation with a Small Sample (n)

When the number of evaluators is small, such as in plot evaluation (7 evaluators in plot mode), the variance of the Story Vector **becomes an estimate with a small n and can be unstable**.

- The variance thresholds (100/400) are applied **only to dimensions with 3 or more evaluator scores** (see `references/scoring-strictness.md`).
- In the benchmark, when reporting the agreement rate, **also record the number of evaluators (n) for each work**, and note the limits of reliability when n is small (<4).

## Analyzing Mismatches (Feeding Back into Calibration)

- Do not judge by the agreement rate alone. **Where mismatches occur** is what matters most.
- A work the system classified as Current Success but that is Innovation in literary history → analyze what was missed in the meaning and emotion dimensions.
- A work the system classified as Discovery Target but that is Low Signal in literary history → risk of excessive optimism. Tighten the criteria.
- Mismatch analysis is also used to **detect anchoring bias**.
- Benchmark results will accumulate in this document and be used to adjust each evaluator's strictness (Phase 2).

## Correlation with Human Editors (Auxiliary Validation)

- If possible, measure the correlation between human editors'/critics' evaluations and the system's scores for a few works.
- This is auxiliary to the "agreement rate" and does not intend the system to replace human judgment (the council does not hand down verdicts; judgment remains human responsibility).

## Recording Results (Accumulation Table)

| # | Anonymized input (opening + summary) | System's blind classification | Literary-history label | Match | Mismatch analysis note |
|---|----------------------|--------------------|-------------|:----:|-----------------|
| 1 | (record) | | | | |

※ To preserve anonymity, label matching is recorded **after** the evaluation.
