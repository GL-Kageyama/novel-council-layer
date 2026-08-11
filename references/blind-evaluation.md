**Language:** English | [日本語](ja/blind-evaluation.md) | [中文](zh/blind-evaluation.md)

# Blind Evaluation (Double-Blind)

To keep evaluation from being pulled by proper nouns — the fame of author names and work titles — this layer evaluates with **double-blinding**. It consists of blinding (anonymization of inputs) and structural calibration (removal of proper nouns from the criteria).

## Why Blind Evaluation: Recognizing Anchoring Bias

Neither humans nor AI can avoid **anchoring to fame (stereotyping)**. This is not merely a distortion of evaluation. It is a danger that **directly undermines this project's core mission — the discovery of buried masterpieces**. Evaluations anchored to fame underestimate unknown works and overestimate famous ones. That way, the "buried masterpieces" that should be discovered will never be discovered.

## The First Blind: Anonymization of Inputs

> **Evaluation is based on the text alone. Evaluators evaluate without knowing the author name, work title, or literary-historical assessment.**

- **Anonymization of inputs**: When feeding into evaluation, remove the author name and work title, and pass only the text.
- **Implementation**: Preprocess with `utils/anonymize.py` (specify targets with `--author` and `--title`, replacing them with `〔匿名〕`). The council orchestrator (story-council) passes **only anonymized text** to the evaluators.
- **Information restriction on evaluators**: Necessary context such as genre is provided, but information that induces fame is not.

## The Second Blind: Structural Calibration (Removal of Proper Nouns from Evaluation Criteria)

The first blind alone is insufficient. If the evaluation criteria were written with proper nouns such as "works like ○○" or "the standard of ××," then even if the input is anonymized, **the evaluator's judgment would be pulled by the fame of those proper nouns**. Therefore, proper nouns are removed from the evaluation criteria themselves.

> **Evaluation criteria and calibration are defined by structural descriptions, not proper nouns (author names, work titles).**

See `references/structural-calibration.md` for details.

## Handling Stylistic Identification (Stylometry)

Anonymization is not perfect — **the style itself can leak the author**. Structural calibration also partially addresses this residual risk. Even if an evaluator associates stylistic features with a known author, **as long as the judgment criteria are structural, the evaluation is directed toward structure, not fame**. Even when one recognizes "this style belongs to a famous author," the question asked is whether "this structure produces valuable time."

## Handover to the Meta Value Layer

The rigor of blinding (leaks in anonymization, fame leaks from context, contamination of the evaluation criteria with proper nouns) is monitored in the **Meta Value Layer (Bias Detection)** of Phase 4. Evaluation bias is detected through inconsistency analysis of benchmarks and divergence between evaluators.

## Blind Evaluation Checklist

Before conducting an evaluation, confirm the following:

1. Is there no author name or work title left in the input text (has `utils/anonymize.py` been run)?
2. Is there no contamination of the evaluator agents' prompts/calibration with proper nouns?
3. Does context information such as genre not contain content that induces fame?
4. Is the evaluation result not being compared against literary-historical assessments (comparison is done only **after** evaluation, within benchmarks)?
