**Language:** [English](README.md) | 日本語 | [中文](README-zh.md)

# Examples — 小説サンプル

ジャンルごとに **執筆 → 評価 → リライト** のループを実演するサンプル集。

## フォルダ構成

| フォルダ | ジャンル | 内容 |
|----------|---------|------|
| `novel-sample/` | サンプル小説 | 評価対象のテキスト + Story Report |

各サンプルフォルダには:
- `input.md` — 評価対象の小説（匿名化前）
- `input-anonymized.md` — `utils/anonymize.py` で匿名化した本文（評価入力）
- `report-v1.json` — 初回評価（厳格スコア）
- `report-v2.json` — リライト後の再評価（ループの改善を実演）
- `report.md` — Markdown表示（GitHub / VSCodeプレビューで読める）

## 使い方

**入力の匿名化（第一の盲検）:**
```bash
python ../utils/anonymize.py input.md --author "著者名" --title "作品名" > input-anonymized.md
```

**評価を読む（Markdown化）:**
```bash
python ../utils/render_report.py --format md novel-sample/report-v2.json
```

**全評価者の個別レポートまで表示:**
```bash
python ../utils/render_report.py --individuals novel-sample/report-v2.json
```

**ループの改善を比較:**
```bash
python ../utils/compare_reports.py novel-sample/report-v1.json novel-sample/report-v2.json
```

**全サンプルの検証:**
```bash
for f in */report-*.json; do python3 ../utils/validate_output.py "$f"; done
```

## 個別評価レポート（individual_reports）

各レポートの `individual_reports` には**招集した全評価者の生データ**（`weaknesses`・`improvement_suggestions`・`narrative`）が入る。これは**リライトの材料として読む入力**である。

## 短編小説サンプル（short-story/）

`short-story/` は、あらすじ（plot）でなく**実際の短編小説（text）**のサンプルである。「最後の台詞」の設定を掌編（散文）として書いたもの。`content_type: text` のため、plotモードで未招集だった **prose-style・narrative-technique・reader-experience を含む全10体**で評価される。

| ファイル | 内容 |
|---------|------|
| `input.md` | 短編小説（v1→v2→v3） |
| `report-v1.json` | 初回評価（現在価値68/潜在71） |
| `report-v2.json` | ループ2（69/71、世界観+9） |
| `report-v3.json` | ユーザー指摘の是正後（**69/72、テーマ+6・品質+4**） |
| `report-v4.json` | 感覚的質感の追加（**70/72、文体+7**） |
| `report-v5.json` | 中盤の韻律と「紙」の比喩の整理（文体70維持） |
| `report-v6.json` | **最終稿**（冒頭の場景化・反復の刈り込み・鋳型の解消、**文体72**） |
| `report.md` | v6（最終稿）のMarkdown表示 |

**v3 はユーザー指摘の「ごめんなさい依存」を是正した版**: 謝罪の言葉に頼らず、応答を待つ言葉（「おかえり」→「ただいま」）で世界の規則（言葉は応答によって届く）を精確に体現する。謝罪（母）・別れ（娘）・帰還（老女/悠）の3つの語域を分離した。評価上、品質(54→62)とテーマ(78→83)が改善し、感傷の型と対称性の批判が解消された。

**v4 は文体評価（59）の指摘に応え、感覚的質感を追加した版**: 汗ばんだ母の手を握り返さない一瞬、乾いて紙を重ねたような老女の手、指先に挟まれた紙一枚の言葉、薄くなって破れかけた帳面とインクの匂い。prose-styleは59→**70**。

**v6 は最終稿**: 冒頭を帳面を開く場景で開き、世界の規則を道具を通して感覚化。『切り崩す』『渡る』の商業レジスターで「費やす/届く」の反復を刈り込み、中盤の二つの出会いの鋳型を解消。文体は**72**に到達。v1からの改善: 文体+9・世界観+9・テーマ+6・品質+4（現在価値 68→70）。

## 動作確認の注意（運用時）

`novel-sample/` は、story-council の **plotモード**（content_type: plot, mode: full）で3ループ評価した実例である:

| ファイル | 内容 |
|---------|------|
| `input.md` | あらすじ（v1→v2→v3） |
| `report-v1.json` | 初回評価（現在価値62/潜在65） |
| `report-v2.json` | ループ2（65/66） |
| `report-v3.json` | ループ3（**68/68**、+4.6平均改善） |
| `report.md` | v3のMarkdown表示 |

**運用上の注意**:
- 評価者エージェント（`agents/`）のネイティブ起動には、**Claude Codeの再起動（または `/agents`）が必要**。再起動前は、エージェントファイルのシステムプロンプトを読み込んで起動するフォールバック方式で運用できる。
- プロットモードでは `prose-style`・`narrative-technique`・`reader-experience` の3体は未招集となり、Story Vectorで `null` になる（`non_consulted_evaluators` に記録）。
- 3ループの改善推移から、評価→修正ループが機能することが確認できる。
