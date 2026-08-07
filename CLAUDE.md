# Novel Council Layer

## プロジェクトのアイデンティティ

これは**小説評議会（Novel Council Layer）**である。複数のAI評価者エージェントが異なる物語の視点から小説を評価し、合議スキルによって構造化されたStory Reportを生成するClaude Codeエージェント群。

> **役割分担**: このレイヤーは**評価専用**である。作品の**執筆**は、書き手・編集者・生成AIに譲る。このリポジトリは「書く」ことではなく「物語の価値を見抜く」ことを担い、その評価結果を次回のリライトへ渡す材料として整える。

## 核となるテーゼ

**物語は時間のなかで読まれる。** 小説はオブジェクトではなく、読者の内面で時間のなかに展開する体験である。評価の対象は「読まれる時間の質」であって、作品の属性ではない。

物語評価に固有の7つの問い:
1. **時間の質** —— この物語は読者の時間をどう使わせるか？
2. **情報の配分** —— 何を、いつ、誰に明かすか？
3. **語りの距離** —— 誰が語り、どの距離から語るか？
4. **空白の設計** —— 読者が埋めるべき隙間は意図的に設計されているか？
5. **文体と時間の一致** —— 文体は読む速度と感覚をコントロールしているか？
6. **再読の深さ** —— 二度目に読むとき、同じ本は別の本になるか？
7. **読後の変位** —— 読後、人生の何かが動いた感覚が残るか？

## 核となる哲学

- **物語は時間の芸術**: 評価の対象は「読まれる時間の質」。
- **多声的評価**: 異なる視点を持つ複数の評価者による合議。
- **不一致こそシグナル**: 評価者間の対立は平均化せず、そのまま保存する。
- **二重の盲検**: 入力（作者名・作品名）と基準（固有名詞）の両方から名声を遮断する。埋もれた名作の発見を守る前提。
- **生成より評価**: 物語の価値を見抜くことが競争領域。

## ディレクトリ規約

- `agents/{name}.md` — 評価者エージェントの正本（10体）。ペルソナベースの専門家として独立したサブエージェントで起動される
- `skills/story-council/SKILL.md` — 合議オーケストレーターの正本（唯一のスキル）
- `.claude/agents/` — プロジェクト内検出用symlink（評価者エージェント）
- `.claude/skills/` — プロジェクト内検出用symlink（合議オーケストレーター）
- `~/.claude/agents/`, `~/.claude/skills/` — グローバルインストール先（`./install.sh` で設定、どこからでも呼べる）
- `.claude-plugin/` — プラグイン配布定義（`/plugin marketplace add` 用）
- `schemas/` — 構造化出力のJSONスキーマ
- `references/` — 物語評価の理論基盤（テーゼの系譜・構造的キャリブレーション・盲検・ベンチマーク）
- `examples/` — サンプル入力と出力
- `utils/` — 匿名化・バリデーション・視覚化・比較ユーティリティ

## 評価者の呼び出し方

**合議はスキル、評価者はサブエージェント**で呼び出す。この役割分担はアーキテクチャの要である——評価者は互いの結果を知らずに独立評価しなければならない。スキルは同じコンテキストを共有するため、独立評価には不向き。評価者をサブエージェントとして起動することで、コンテキストが隔離される。

### 合議全体（推奨）

```
Skill: story-council
Args: {"content": "...", "content_type": "text", "domain": "pure-literature"}
```

合議は以下を実行する:
1. 入力の物語サブドメインを判定
2. 関連する評価者エージェントを選択（anti-generic-filter は常に含める）
3. 各評価者をサブエージェントとして起動（Agent tool経由、互いの結果を知らずに独立評価）
4. Story Reportに統合
5. すべての不一致を保存

### プロット評価モード（あらすじでも評価できる）

`content_type: "plot"` を指定すると、執筆前の構想・簡単なあらすじでも評価できる。散文・語り・読書体験が存在しないため、`prose-style`, `narrative-technique`, `reader-experience` の3体は未招集となり、残り7体（narrative-originality, anti-generic-filter, emotional-power, plot-architecture, character-depth, theme-resonance, world-building）で評価する。

```
Skill: story-council
Args: {"content": "簡単なあらすじ...", "content_type": "plot", "domain": "genre-fiction"}
```

### 単一評価者

特定の視点だけを評価したい場合。評価者はサブエージェントとして起動する。

```
Agent tool, subagent_type: plot-architecture
Prompt: {"content": "...", "content_type": "text", "domain": "genre-fiction"}
```

インストール済みプラグインとして実行している場合は、プラグインスコープ名（`novel-council-layer:plot-architecture`）を使う。

## 出力規約

すべての評価者出力は `schemas/novel-value-output.schema.json` に準拠した有効なJSONでなければならない。

```bash
python utils/validate_output.py < output.json
python utils/validate_output.py --json output.json   # 機械可読な検証結果
```

**自動リトライ**: 合議スキルは各評価者の出力を `validate_output.py --json` で**決定的に検証**し、不合格なら同じ評価者を**最大3回再起動**する（フィードバックにエラー内容を含める）。3回リトライ後も不合格なら `excluded_evaluators` に `reason: "JSON validation failed after 3 retries"` として明示的に記録する。**サイレントドロップ禁止。**

**入力は匿名化する（第一の盲検）:**

```bash
python utils/anonymize.py input.txt --author "著者名" --title "作品名" > anonymized.txt
```

## ツール群

| ツール | 役割 |
|--------|------|
| `utils/anonymize.py` | **入力の匿名化**——作者名・作品名を除去し、盲検評価の前提を作る（第一の盲検） |
| `utils/validate_output.py` | 評価者出力のスキーマ検証。`--json` フラグで機械可読な結果を出力（合議スキルの自動リトライが利用） |
| `utils/render_report.py` | Story Report の視覚表示（10次元バーチャート・分類バッジ・次元間の対立）。`-o report.md` でMarkdown文書として保存、`--individuals` で全個別レポート表示 |
| `utils/compare_reports.py` | リライト前後の差分比較（評価→リライトループ用） |

## 評価出力は「入力」として設計されている

**このレイヤーの評価結果は、それ自体が最終成果ではない。** 書き手・編集者・生成AIがリライトするための**入力**である。

- 合議は**リライト指示そのものを生成しない**。それは書き手・編集者・生成AIの責務。
- 代わりに、`individual_reports` に各評価者の**生の素材**（`weaknesses`・`improvement_suggestions`・`expected_disagreement_points`・`narrative`）を完全に保存する。
- フィールド名は固定・一貫（`schemas/novel-value-output.schema.json` 準拠）。
- 合成ナラティブ（executive_summary等）は補助であり、生データを捨てない。

**評価 → リライトループ:**
```
評価 → revision_direction（次回の修正方向）→ リライト → 再評価
  → compare_reports.py で改善度確認 → 繰り返し
```

## 重要原則

- 評価者は自分の専門領域の次元だけをスコアする。専門外は `null` を返す。
- **二重の盲検を徹底する**: 入力は匿名、基準は構造的。固有名詞（作家名・作品名）を評価の場から排除する。
- 不一致を予測するのは評価者の義務である。
- 評価は外交的であってはならない。率直さが価値。
- スコアリングは**意図的に厳格**である。高得点は稀。**「読める」では50に届かない。**
- 感傷は減点する。**抑制の美学**——語らないことで強まる感情——を評価する。
- オーケストレーターは評価者に判断を指示しない。招集して統合するだけ。
- 合議は判決を下さない。最終的な価値判断は人間の責任である。

## インストール

```bash
./install.sh            # グローバル: ~/.claude/agents/ + ~/.claude/skills/（どこからでも呼べる）
./install.sh --local    # プロジェクト: .claude/agents/ + .claude/skills/
./install.sh --uninstall
```
