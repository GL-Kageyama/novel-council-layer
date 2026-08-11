**Language:** English | [日本語](ja/revision-loop.md) | [中文](zh/revision-loop.md)

# Revision Loop (Evaluation → Rewrite Loop)

The evaluation results of this layer are **not the final output**. They are **input** for the writer, editor, or generative AI to use in rewriting. This section defines the guidelines for running this loop.

## Loop Flow

```
① 執筆（v1）
    ↓
② 評価（story-council / mode:full）※二重の盲検
    ↓
③ revision_direction（次回の修正方向）を確認
    ↓
④ リライト（書き手 or 生成AI）
    ↓
⑤ 再評価
    ↓
⑥ 比較（compare_reports.py で改善度を確認）
    ↓
⑦ 目標に達するか頭打ちになるまで繰り返す
```

Each evaluator's `weaknesses`, `improvement_suggestions`, and `expected_disagreement_points` are stored as material for concrete rewrite instructions.

## Iteration Modes (iteration)

Two modes control the evaluation→rewrite loop. The essence of the loop is managing "in which direction to revise" after each round of evaluation.

| iteration | Behavior | When to use |
|-----------|----------|-------------|
| `confirm` (default) | After outputting the Story Report, does not start the next iteration until a human/writer approves `revision_direction` | When you want to check direction changes each time |
| `persistent` | Finalizes `revision_direction` at the first evaluation; subsequent iterations do not reconsider that direction and only report progress toward the `axis` | When you want to set a direction and then polish |

## Loop Guidelines

- **Evaluation does not discard raw data** (synthetic narratives are auxiliary; the source material remains in the JSON).
- **Field names are fixed and consistent** (per `schemas/novel-value-output.schema.json`). The rewrite side can read paths with hardcoded lookups.
- Do not judge by averages alone; **also look at variance and disagreement** (a single dimension may spike without changing the whole).
- **Stop the loop when improvement plateaus** (risk of over-correcting and losing the original strengths).
- Do not generate the rewrite instructions themselves. The writer, editor, or generative AI composes instructions from the material in `individual_reports`.

## Comparing Improvement

```bash
python utils/compare_reports.py before.json after.json
```

Output example:

```
🔄 執筆 → 評価 → リライト ループの比較

  分類の変化:
    before: 🔍 Discovery Target
    after:  ⭐ Innovation

【次元別の改善】
  プロット構造 (plot_architecture)  45 → 70  ▲ +25
  人物の深さ (character_depth)      50 → 68  ▲ +18
  テーマ (theme_resonance)          52 → 66  ▲ +14
  平均変化（評価された10次元）: +9.4
```

## Handling Disagreement

Disagreement (`disagreement_map`) is **signal**, not noise. Stories that split evaluators sharply are often the most interesting. Use disagreement as a clue for rewriting:

- When evaluators split sharply on a dimension → that dimension is "undetermined as to whether it is a strength or a weakness," and there is room to set a direction through rewriting.
- Everyone agrees it is low → a clear weakness. Fix it with priority.
- Everyone agrees it is high → a strength. Do not break it in rewriting (record it in `revision_direction.preserve`).
