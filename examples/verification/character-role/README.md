# character-role 本格検証（Phase 4）実行パッケージ

[検証計画](../../../../資料/キャラクターのロール構想/実装/検証計画.md)（事前登録）の実行用素材と手順。素材は**事前に固定済み**。数値を見てから素材や規則を変えない。

## 前提（必読）

- **評価者の実実行は、`cd novel-council-layer` で起動した新セッションで行う**。ルート起動だと evaluator がレジストリに載らない（既知の制約）。
- 実行言語は `ja`。単体 evaluator は `character-role-ja` / `hook-ja` を直接呼ぶ（story-council 経由でなく）。
- 素材は日本語。`content_type` は V1/V3/V4 が `plot`、V2 が `text`。

## 打ち切り規則（固定・V1〜V3 に適用）

- 各比較は対象条件版（A）と対照条件版（B）を n=1 から開始。
- **勝ち**＝ A の `primary_score` ＞ B の `primary_score`。
- **打ち切り**：完了 run の累積勝率 ≤ 50% かつ 平均差 ≤ 0 → その項目を打ち切り、負の結果を開示。
- **継続**：累積勝率 ＞ 50% → n=3 までサンプル追加。
- 判定は各 run 完了ごとに機械的に行う。規則自体は変えない。負の結果（打ち切り）も必ず [measurement.md](measurement.md) に記録する。

## 実行手順

### V1 5軸の判定力
1. `character-role-ja`（plot mode）を [V1/A_ロールあり.md](V1/A_ロールあり.md) に呼ぶ → JSON 保存。
2. `character-role-ja`（plot mode）を [V1/B_ロールなし.md](V1/B_ロールなし.md) に呼ぶ → JSON 保存。
3. 判定：A の `primary_score` ＞ B、かつ stake・autonomy の次元スコアが A＞B か。打ち切り判定を [measurement.md](measurement.md) に記録。

### V2 ロールの効果
1. `character-forge` で [V2/premise.md](V2/premise.md) から [V2/A_手順.md](V2/A_手順.md)（2b ロール確定）→ design.md → `fast-draft` → 草稿保存。
2. 同 premise から [V2/B_手順.md](V2/B_手順.md)（核のみ・ロール小見出しなし）→ design.md → `fast-draft` → 草稿保存。
3. `character-role-ja`（text mode）で A・B 両草稿を評価。
4. 判定：A の `primary_score` ＞ B（consistency・autonomy の上昇を期待）。

### V3 伏線マップの効果
1. `hook-ja`（plot mode）を [V3/A_伏線あり.md](V3/A_伏線あり.md) に呼ぶ → JSON 保存。
2. `hook-ja`（plot mode）を [V3/B_伏線なし_後出し.md](V3/B_伏線なし_後出し.md) に呼ぶ → JSON 保存。
3. 判定：A の `primary_score` ＞ B（進み・間合いが差を分けるはず）。

### V4 プロフィール数値の妥当性（照合・打ち切り不適用）
1. [V4/目標プロフィール.md](V4/目標プロフィール.md) の目標値を確認。
2. `character-role-ja`（plot mode）を [V4/あらすじ.md](V4/あらすじ.md) に呼ぶ → JSON 保存。
3. 照合：stake/challenge/autonomy/fusion を 0-1 に正規化し、目標値との絶対差の平均 ≤ 0.2 か診断（consistency は対象外）。

## 出力の検証と保存

- 各 evaluator の出力 JSON は `python utils/validate_output.py --json <file>` で検証。
- **崩れた JSON は手で直さず再生成**（[[broken-output-regenerate]]）。3回再試行しても失敗したら `excluded_evaluators` に理由を明記（黙って落とさない）。
- 一次スコア・各軸・打ち切り判定を [measurement.md](measurement.md) に累積記録する。

## 出力言語

`lang=ja` で実行。`character-role-ja` / `hook-ja` の自由テキストは日本語で書かれること。
