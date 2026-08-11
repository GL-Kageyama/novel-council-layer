**Language:** English | [日本語](ja/scoring-strictness.md) | [中文](zh/scoring-strictness.md)

# Scoring Strictness (Strict Scoring Standards, Novel Edition)

Scoring is deliberately strict **because the purpose of this council is not to "praise good novels" but to "see through to stories worth reading."** Discriminative power lies in the relative differences between scores; a low absolute score does not mean "poorly rated" but "mediocre and safe."

## Common Score Bands

| Band | Meaning (in novels) | Expected frequency |
|------|--------------------|--------------------|
| 0-10 | Serious defect. Does not function as a story | Rare |
| 11-30 | Weak. Merely steals the reader's time | Somewhat common |
| 31-50 | Safe and mediocre. Readable, but the time spent reading changed nothing | **Largest population** |
| 51-70 | Truly good. The time spent reading was a valuable experience | Somewhat rare |
| 71-90 | Exceptional. Something in one's life moved after reading | Rare |
| 91-100 | Will remain in literary history | Almost never given |

## Iron Rules of Novel-Specific Judgment

1. **Judge by "the time spent reading."** Ask not about the writer's intent, but whether "this time was worth it" as the reader's experience.
2. **Ask yourself before scoring**: "Is this really a reading experience above 50? Does anything remain after reading?" When in doubt, score low. **"Readable" does not reach 50.**
3. **Mediocrity falls to low scores.** "Easy-to-read, safe entertainment" lands in the 20-40 range.
4. **Deduct points for sentimentality.** Formulaic emotion is not a genuine emotional experience. Appreciate the **aesthetics of restraint** — emotion that grows stronger through what is left unsaid.
5. **Evaluate meaning and beauty by experience, not by explanation.** Rather than "it discusses a deep theme," evaluate it as an experience: "the displacement after reading, the depth of rereading, sensory texture."
6. **The input is the text alone (the first blind).** Evaluate without knowing the author's name, the work's title, or its standing in literary history. Anchoring to reputation is the greatest distortion in evaluation.
7. **The criteria are structural (the second blind).** Judge by structural description, not proper nouns. Details in `references/structural-calibration.md`. Ask not "does it resemble a famous work" but "does this structure produce valuable time."

## Calibration Reference Points (Structural)

| Reference point | Assumed score | Reason |
|-----------------|---------------|--------|
| A readable work that leaves nothing behind | 20-40 | The time spent reading changed nothing |
| A work with one excellent scene | 45-60 | Partially genuine value |
| A completed work with structure, style, theme, and characters in place | 65-85 | A true reading experience |
| A work that becomes part of one's life after reading | 85-95 | Rare value. The ending recontextualizes the opening; rereading opens a different story |

## Handling Variance and Disagreement

- Scores are on a **0〜100 integer scale** (conforming to `schemas/novel-value-output.schema.json`).
- Do not judge by the mean alone; also look at **variance and disagreement** (a single dimension may spike without changing the whole).
- Disagreement is signal, not noise. Save it verbatim in `disagreement_map` (see `references/revision-loop.md`).
- Missing dimensions (unsummoned in plot mode) are excluded from the variance calculation.

### Note on Variance Estimation with Small Samples (n)

When the number of evaluators is small, such as in plot evaluation (7 in plot mode), the variance is **an estimate at small n and can be unstable**. Especially around n=3, **a single outlier can flip the threshold judgment**.

- The variance threshold (100/400) judgment is performed **only on dimensions with 3 or more evaluator scores**.
- **On dimensions with n < 4, do not use the variance threshold for "definitive classification."** Treat the threshold as **a signal that launches Phase 4 (verbatim review of disagreement)**, and save the disagreement to `disagreement_map`. **Only on dimensions that reach n ≥ 4** is the variance used for classification judgment.
- On dimensions with n=3〜4, place more weight on **the range of scores (min-max) and the content of the disagreement** than on the variance value itself.
- When reporting the mean, variance, and range, **always state n (the number of evaluators)** (the `scores` array of the council's Story Vector holds n).

## Status of Thresholds

Thresholds (current value 45, potential value 45, etc.) are **relative guidelines**, and are readjusted in the Meta Value Layer (Phase 4) based on actual data (`references/benchmark-50novels.md`).
