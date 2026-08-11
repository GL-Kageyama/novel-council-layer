**Language:** [English](../revision-loop.md) | [日本語](../ja/revision-loop.md) | 中文

# 修订循环（评价 → 重写循环）

这个层次的评价结果**并非最终成果**。它们是供作者、编辑或生成式 AI 进行重写的**输入**。此处定义运行这一循环的指南。

## 循环流程

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

每位评价者的 `weaknesses`、`improvement_suggestions`、`expected_disagreement_points` 会被保存下来，作为具体改写指示的素材。

## 迭代模式（iteration）

控制评价 → 重写循环有两种模式。循环的本质在于管理"每轮评价之后应该向哪个方向修改"。

| iteration | 行为 | 适用场景 |
|-----------|------|------------|
| `confirm`（默认） | 输出 Story Report 之后，在人类/作者批准 `revision_direction` 之前，不开始下一轮迭代 | 希望每次检查方向转变 |
| `persistent` | 在首次评价时确定 `revision_direction`，后续迭代不再重新考虑该方向，只报告对 `axis` 的达成度 | 希望确定方向后持续打磨 |

## 循环指南

- **评价不丢弃原始数据**（合成叙述只是辅助，素材保留在 JSON 中）。
- **字段名固定且一致**（遵循 `schemas/novel-value-output.schema.json`）。重写方可以按固定路径读取。
- 不要只凭平均值判断，**也要看方差和不一致**（即使某个维度突出，整体也可能不变）。
- 当改进**趋于停滞时就停止循环**（过度修改有失去原有优点的风险）。
- 不直接生成改写指示。作者、编辑或生成式 AI 从 `individual_reports` 的素材中综合出指示。

## 改进度比较

```bash
python utils/compare_reports.py before.json after.json
```

输出示例:

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

## 不一致的处理

不一致（`disagreement_map`）不是噪声，而是**信号**。引发评价者激烈分歧的故事往往最有趣。将不一致作为改写的线索：

- 某个维度上评价者激烈分歧 → 该维度"尚未确定是优点还是缺点"，通过改写仍有确定方向的空间。
- 所有人一致认为偏低 → 明确的弱点，优先修正。
- 所有人一致认为偏高 → 优点，改写时不要破坏它（记录在 `revision_direction.preserve` 中）。
