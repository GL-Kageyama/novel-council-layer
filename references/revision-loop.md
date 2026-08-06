# Revision Loop（評価→リライトループ）

このレイヤーの評価結果は**最終成果ではない**。書き手・編集者・生成AIがリライトするための**入力**である。このループを回すための指針を定義する。

## ループの流れ

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

各評価者の `weaknesses`・`improvement_suggestions`・`expected_disagreement_points` は、リライトの具体的な指示の材料として保存される。

## 反復モード（iteration）

評価→リライトループの制御には、2つのモードがある。ループの本質は「1ターン評価ごとに、どの方向に修正するか」を管理することにある。

| iteration | 動作 | 使いどころ |
|-----------|------|------------|
| `confirm`（デフォルト） | Story Report を出力した後、人間・書き手が `revision_direction` を承認するまで次の反復を開始しない | 方向転換を都度チェックしたい |
| `persistent` | 初回の評価で `revision_direction` を確定し、以降の反復はその方向を再考せず、`axis` への到達度だけを報告する | 方向を決めて磨き込みたい |

## ループの指針

- **評価は生データを捨てない**（合成ナラティブは補助。素材はJSONに残る）。
- **フィールド名は固定・一貫**（`schemas/novel-value-output.schema.json` 準拠）。リライト側はパスを決め打ちで読める。
- 平均だけで判断せず、**分散と不一致**も見る（1次元が突出しても全体は変わらないことがある）。
- 改善が**頭打ちになったらループを止める**（過修正で元の良さを失うリスク）。
- リライト指示そのものは生成しない。書き手・編集者・生成AIが `individual_reports` の素材から指示を合成する。

## 改善度の比較

```bash
python utils/compare_reports.py before.json after.json
```

出力例:

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

## 不一致の扱い

不一致（`disagreement_map`）はノイズではなく**シグナル**である。激しく割れる物語はしばしば最も興味深い。不一致はリライトの手がかりとして使う:

- ある次元で評価者が激しく割れた → その次元は「強みか弱点かが未決定」であり、リライトで方向を定める余地がある。
- 全員が一致して低い → 明確な弱点。優先的に修正する。
- 全員が一致して高い → 強み。リライトで壊さない（`revision_direction.preserve` に記録する）。
