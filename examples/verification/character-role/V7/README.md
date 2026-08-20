# V7 挑戦の具現化・再検証（A=改訂2要素 / B=名詞）

## ― Phase 6 §8 再設計の事前登録 ―

Phase 6 の3要素化（Phase6_挑戦の具現化.md §8）は負・打ち切り n=3（challenge 通算 +2 ≈ 0、autonomy 3/3 下落 -6/-24/-10）で撤回された。本検証は、再設計の2要素書式（**敵の名指し × 敵の抵抗の段階**）が challenge を引き上げ、かつ autonomy を崩さないかを、セッション分離（書き手＝soul-voice-teller 独立・評価＝novel-council-layer 新セッション）で compare する。

> **事前登録の原則**（matrix-early-stopping と同じ）: 打ち切り規則・分離手順・素材の変数を、データを見る前に固定する。本 README の作成をもって登録点とする。

## 問い

> design.md の「挑戦」を2要素（敵の名指し × 敵の抵抗の段階・最終対峙はクライマックス・能動の主語は主人公）で書いた場合と、名詞のみで書いた場合で、fast-draft の草稿の challenge が変わるか。能動の主語を主人公に戻し・敵を抵抗（応答）に据えることで、V6 の失敗（autonomy 3/3 下落）を避けつつ challenge を上げられるか。

**成功基準**: A（2要素）の `challenge` ＞ B（名詞）。かつ autonomy が V6 のように一貫して下落しないこと。

## A/B の定義

| 版 | 書式 | 期待 |
|---|---|---|
| **A（対象・改訂2要素）** | 挑戦＝敵の名指し × 敵の抵抗の段階（制止→拒否→威圧→最終対峙・クライマックス）。能動の主語は主人公。敵は抵抗（応答）。 | challenge が上がり、autonomy も維持 |
| **B（対照・名詞）** | 挑戦＝名詞のみ（V6 の B と同一素材）。 | 静止した挑戦（低 challenge の既知） |

題材は V6 と同じ3題材（run 1=経営者・静止、run 2=看護師・静止、run 3=刑事・対決系）。

## 素材（固定済み）

| 題材 | A（2要素） | B（名詞） |
|---|---|---|
| 経営者（野村） | `writer-A/design.md` | `writer-B/design.md` |
| 看護師（水野） | `n2/writer-A/design.md` | `n2/writer-B/design.md` |
| 刑事（沢木） | `n3/writer-A/design.md` | `n3/writer-B/design.md` |

両 design.md の差分は「挑戦」項目とシーン表の抵抗段階の有無のみ（事件・結末・他人物・文体・賭け・能動の原理は同一）。

## 実行手順（3 セッション）

### 書き手セッション 1（soul-voice-teller・独立）→ `draft_1.md`

- 作業ディレクトリに `writer-A/design.md` を `design.md` として置き、`/fast-draft` を実行。
- **指示（固定・これ以外を伝えない）**:
  > 以下の design.md に忠実に従い、fast-draft で草稿を書け。design.md に書かれていることだけを草稿に展開し、書かれていない設定を足しすぎないこと。
- 出力を `draft_1.md` に保存。
- **禁止**: 仮説・比較・「A/B」「挑戦」「自律性」への言及。どちらが対象条件かの示唆。

### 書き手セッション 2（soul-voice-teller・独立）→ `draft_2.md`

- 同様に `writer-B/design.md` から `draft_2.md` を生成。**指示はセッション 1 と同一文言**。
- **禁止**: 同上。セッション 1 の存在・内容はセッション 2 に持ち込まない（独立セッション）。

### 評価セッション（novel-council-layer 内・新セッション）

1. `character-role-ja`（text mode）を `draft_1.md`・`draft_2.md` に呼ぶ（盲検。評価者はどちらが A か知らない）。
2. 出力 JSON を `python utils/validate_output.py --json` で検証。崩れたら手で直さず再生成（broken-output-regenerate）。
3. 両方の `challenge`・`autonomy`・`primary_score` を記録してから、`key.md` を開いて A/B を復元。

## 打ち切り規則（固定）

- 各比較は n=1 から開始。**勝ち**＝ A の `primary_score` ＞ B（対象次元は `challenge`、副次で `autonomy` の下落有無を確認）。
- **打ち切り**: 完了 run の累積勝率 ≤ 50% かつ 平均差 ≤ 0 → 負の結果を開示して打ち切り。
- **継続**: 累積勝率 ＞ 50% → n=3 までサンプル追加。
- 判定は各 run 完了ごとに機械的に行う。規則自体は変えない。負の結果も [measurement.md](../measurement.md) に記録する。

## 記録

`measurement.md` に「V7 挑戦の具現化・再検証（A=改訂2要素 / B=名詞）」節を新設して追記。5軸内訳（stake/challenge/consistency/autonomy/fusion の A/B）を run ごとに記録。
