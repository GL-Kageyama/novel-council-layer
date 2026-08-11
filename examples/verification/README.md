# i18n Verification Outputs（言語別動作確認）

This folder holds the per-language runtime verification outputs of the i18n (en/ja/zh) changes.
These are **UI-layer** verifications of the `utils/` tools on the existing example report
(`examples/short-story/report-v6.json`, a ja measurement example). The JSON protocol itself is
language-neutral and unchanged.

| File | Tool | Language | What it proves |
|------|------|----------|----------------|
| `report-v6-render-en.md` / `-ja.md` / `-zh.md` | `utils/render_report.py --lang` | en / ja / zh | Report headings, classification badges, dimension labels, section titles render in each language. `--lang` selection works. |
| `compare-v2-v6-en.txt` / `-ja.txt` / `-zh.txt` | `utils/compare_reports.py --lang` | en / ja / zh | Before/after comparison header and per-dimension columns are localized. |
| `anonymize-en.txt` / `-ja.txt` | `utils/anonymize.py --lang` | en / ja | Placeholder differs per language: en `[Anonymous]`, ja `〔匿名〕`. Redaction report localized. |

Run any of them again with:

```bash
python utils/render_report.py examples/short-story/report-v6.json -o examples/verification/report-v6-render-en.md --lang en
python utils/compare_reports.py examples/short-story/report-v2.json examples/short-story/report-v6.json --lang zh
printf 'sample\n' | python utils/anonymize.py --author "sample" --lang ja
```

## What this does NOT cover

The **council-level** runtime verification (running the `story-council` skill and the 30 evaluator
agents in each language) is documented in
`資料/多言語化ver3/novel-council-runtime-verification-runbook.md`. It requires a **new Claude Code
session** after `./install.sh --local`, because the agent registry is loaded at session start.
