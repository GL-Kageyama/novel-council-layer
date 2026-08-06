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
