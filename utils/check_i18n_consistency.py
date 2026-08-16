#!/usr/bin/env python3
"""Static i18n consistency check for the Novel Council Layer.

Verifies that the 30 evaluator agent files (10 bases x en/ja/zh) and the
story-council SKILL.md obey the i18n contract defined in
`資料/多言語化ver3/novel-council-layer-i18n-plan.md`:

- File structure: each base exists as `{base}.md` (en), `{base}-ja.md` (ja),
  `{base}-zh.md` (zh), with matching frontmatter `name`.
- `description` is English and byte-identical across the 3 variants.
- i18n-version tag present with the right canonical/lang.
- Output Format items 1-5 are identical across all files in the same language.
- Output Format item 6 (output-language directive) matches the language.
- JSON protocol invariants are identical across languages for the same base:
  evaluator_name, evaluator_id, dimension_scores keys, weights,
  value_vector_contribution scored key.
- Language hygiene: en/zh files contain no Japanese kana; en contains no
  CJK ideographs; ja contains kana (sanity).

Usage:
    python utils/check_i18n_consistency.py            # check repo at cwd
    python utils/check_i18n_consistency.py --dir <repo>
    python utils/check_i18n_consistency.py --verbose

Exit codes:
    0  all checks pass
    1  one or more checks failed
    2  usage / structural error
"""

import argparse
import re
import sys
from pathlib import Path

BASES = [
    "narrative-originality", "anti-generic-story-filter", "emotional-power",
    "plot-architecture", "character-depth", "prose-style", "theme-resonance",
    "world-building", "narrative-technique", "reader-experience",
]

LANGS = ["en", "ja", "zh"]
SUFFIX = {"en": "", "ja": "-ja", "zh": "-zh"}

# Canonical Output Format items 1-6 per language (verbatim from the spec).
PROTOCOL_ITEMS = {
    "en": [
        "1. The **first character** of your response must be `{`, and the **last character** must be `}`",
        "2. Do NOT wrap it in a markdown code block (```json ... ```)",
        "3. Do NOT write any explanatory text, comments, or summary before or after the JSON",
        "4. Tool calls and file reads are strictly forbidden (do not call read_file, etc.)",
        "5. Do not read the schema file (`schemas/novel-value-output.schema.json`); follow the field definitions below directly",
        "6. **Output language**: All free-text fields — `narrative`, `strengths`, `weaknesses`, `unique_perspective`, `evidence`, `judgment`, `content_summary`, `primary_score_rationale` — MUST be written in English",
    ],
    "ja": [
        "1. 応答の**最初の文字は `{`、最後の文字は `}`** でなければならない",
        "2. マークダウンのコードブロック（```json ... ```）で囲んではならない",
        "3. JSONの前後に説明文・注釈・要約を一切書いてはならない",
        "4. ツール呼び出し・ファイル読み込みは一切禁止（read_file等を呼ばないこと）",
        "5. スキーマファイル（`schemas/novel-value-output.schema.json`）は読まずに、下記のフィールド定義に直接従え",
        "6. **出力言語**: `narrative`・`strengths`・`weaknesses`・`unique_perspective`・`evidence`・`judgment`・`content_summary`・`primary_score_rationale` 等の自由テキストは必ず日本語で書け",
    ],
    "zh": [
        "1. 响应的**第一个字符必须是 `{`，最后一个字符必须是 `}`**",
        "2. **不得**用markdown代码块（```json ... ```）包裹",
        "3. JSON前后**不得**附加任何说明文字、注释或摘要",
        "4. **禁止**工具调用与文件读取（不得调用 read_file 等）",
        "5. 不要读取schema文件（`schemas/novel-value-output.schema.json`），直接遵循下述字段定义",
        "6. **输出语言**: 所有自由文本字段 —— `narrative`、`strengths`、`weaknesses`、`unique_perspective`、`evidence`、`judgment`、`content_summary`、`primary_score_rationale` —— 必须用中文书写",
    ],
}

# Headers under which each agent declares its dimension_scores keys.
DIM_KEY_HEADERS = {
    "en": "This Evaluator's Dimensions",
    "ja": "この評価者の次元",
    "zh": "本评估者的维度",
}
# Weight pattern per language (in the "Primary Dimensions" heading).
WEIGHT_PATTERNS = {
    "en": re.compile(r"—\s*weight\s+([0-9.]+)", re.IGNORECASE),
    "ja": re.compile(r"重み\s+([0-9.]+)"),
    "zh": re.compile(r"权重\s+([0-9.]+)"),
}

VECTOR_KEYS = [
    "narrative_originality", "quality", "emotional_power", "plot_architecture",
    "character_depth", "prose_style", "theme_resonance", "world_building",
    "narrative_technique", "reader_experience", "admiration",
]

# Kana letters (hiragana + katakana letters + prolonged mark ー), EXCLUDING
# the katakana middle dot ・ (U+30FB) which is legitimately used in Chinese
# and Japanese alike as a list separator.
KANA = re.compile(r"[ぁ-ゖァ-ヺー]")
CJK = re.compile(r"[一-鿿]")

errors = []
warnings = []
verbose = False


def err(msg):
    errors.append(msg)
    print(f"  ✗ {msg}")


def warn(msg):
    warnings.append(msg)
    print(f"  ⚠ {msg}")


def ok(msg):
    if verbose:
        print(f"  ✓ {msg}")


def split_frontmatter(text):
    """Return (frontmatter_dict, body) for a markdown file with YAML frontmatter."""
    m = re.match(r"^---\n(.*?)\n---\n", text, flags=re.S)
    if not m:
        return None, text
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm, text[m.end():]


def i18n_tag_ok(body, base, lang):
    tag = f"i18n-version: 1.0.0 | canonical: {base}.md | translated: 2026-08-11 | lang: {lang}"
    return f"<!-- {tag} -->" in body


def main():
    global verbose
    parser = argparse.ArgumentParser(prog="check_i18n_consistency.py")
    parser.add_argument("--dir", default=".", help="novel-council-layer repo root (default: cwd)")
    parser.add_argument("--verbose", action="store_true", help="print passing checks")
    args = parser.parse_args()
    verbose = args.verbose

    repo = Path(args.dir)
    agents = repo / "agents"
    if not (agents / "plot-architecture.md").exists():
        print(f"Structural error: {agents / 'plot-architecture.md'} not found "
              f"(is {repo} the novel-council-layer root?)", file=sys.stderr)
        return 2

    print("=== 1. File structure & frontmatter ===")
    for base in BASES:
        for lang in LANGS:
            fname = f"{base}{SUFFIX[lang]}.md"
            p = agents / fname
            if not p.exists():
                err(f"missing {fname}")
                continue
            text = p.read_text(encoding="utf-8")
            fm, body = split_frontmatter(text)
            if fm is None:
                err(f"{fname}: no frontmatter")
                continue
            expect_name = f"{base}{SUFFIX[lang]}"
            if fm.get("name") != expect_name:
                err(f"{fname}: frontmatter name is {fm.get('name')!r}, expected {expect_name!r}")
            if not i18n_tag_ok(body, base, lang):
                err(f"{fname}: i18n-version tag missing or wrong (lang={lang})")

    print("=== 2. description parity (English, identical across variants) ===")
    for base in BASES:
        descs = {}
        for lang in LANGS:
            p = agents / f"{base}{SUFFIX[lang]}.md"
            if not p.exists():
                continue
            fm, _ = split_frontmatter(p.read_text(encoding="utf-8"))
            descs[lang] = fm.get("description", "") if fm else ""
            if descs[lang] and KANA.search(descs[lang]):
                err(f"{base}-{lang}: description contains Japanese kana (must stay English)")
        if len(set(descs.values())) != 1:
            err(f"{base}: description differs across languages {descs}")

    print("=== 3. Output Format protocol items ===")
    for lang in LANGS:
        ref = "\n".join(PROTOCOL_ITEMS[lang])
        seen_variant = set()
        for base in BASES:
            p = agents / f"{base}{SUFFIX[lang]}.md"
            if not p.exists():
                continue
            text = p.read_text(encoding="utf-8")
            # Locate the Output Format header (language-specific), then take
            # the next 6 numbered lines. [^\n]* keeps the greedy dot from
            # swallowing the whole file.
            m = re.search(r"^(?:## Output Format|## 输出格式)[^\n]*\n(.*?)(?=\n### )", text, flags=re.S | re.M)
            if not m:
                err(f"{p.name}: Output Format section not found")
                continue
            section = m.group(1)
            six = [l for l in section.splitlines() if re.match(r"^[1-6]\. ", l)][:6]
            if len(six) != 6:
                err(f"{p.name}: found {len(six)} protocol items (expected 6)")
                continue
            joined = "\n".join(six)
            if joined != ref:
                seen_variant.add(joined)
                for i, line in enumerate(six):
                    if line != PROTOCOL_ITEMS[lang][i]:
                        err(f"{p.name}: protocol item {i+1} differs — {line!r}")
                        break
        if seen_variant:
            err(f"lang={lang}: {len(seen_variant)} protocol variants (should be exactly 1)")

    print("=== 4. JSON protocol invariants (cross-language, per base) ===")
    for base in BASES:
        names = {}
        dim_keys = {}
        weights = {}
        scored_key = {}
        for lang in LANGS:
            p = agents / f"{base}{SUFFIX[lang]}.md"
            if not p.exists():
                continue
            text = p.read_text(encoding="utf-8")

            m = re.search(r'`evaluator_name`[^\n]*\|\s*([^|]+)\|', text)
            names[lang] = m.group(1).strip() if m else None

            # Extract only the backtick-wrapped dimension keys (the trailing
            # comment differs per language legitimately).
            m = re.search(rf"^###\s*{re.escape(DIM_KEY_HEADERS[lang])}[^\n]*\n\n([^\n#]+)", text, flags=re.M)
            dim_keys[lang] = tuple(re.findall(r"`([a-z_]+)`", m.group(1))) if m else None

            ws = WEIGHT_PATTERNS[lang].findall(text)
            weights[lang] = tuple(ws)

            # value_vector_contribution scored key = the non-null vector key.
            keys = []
            for vk in VECTOR_KEYS:
                if re.search(rf'"{vk}":\s*<', text):
                    keys.append(vk)
            scored_key[lang] = tuple(keys)

            if f'"{base}"' not in text:
                err(f"{p.name}: evaluator_id {base!r} not found")

        if len(set(names.values())) != 1:
            err(f"{base}: evaluator_name differs across languages {names}")
        if len(set(dim_keys.values())) != 1:
            err(f"{base}: dimension_scores keys differ across languages {dim_keys}")
        if len(set(weights.values())) != 1:
            err(f"{base}: weights differ across languages {weights}")
        if len(set(scored_key.values())) != 1:
            err(f"{base}: value_vector_contribution scored key differs across languages {scored_key}")

    print("=== 5. Language hygiene ===")
    for lang in LANGS:
        for base in BASES:
            p = agents / f"{base}{SUFFIX[lang]}.md"
            if not p.exists():
                continue
            text = p.read_text(encoding="utf-8")
            # Skip the frontmatter description (English) — check body only.
            _, body = split_frontmatter(text)
            if lang in ("en", "zh") and KANA.search(body):
                err(f"{p.name}: contains Japanese kana (lang={lang})")
            if lang == "en" and CJK.search(body):
                err(f"{p.name}: contains CJK ideographs (en must be pure English)")
            if lang == "ja" and not KANA.search(body):
                warn(f"{p.name}: no Japanese kana found (lang=ja)")

    print("=== 6. SKILL.md ===")
    skill = repo / "skills" / "story-council" / "SKILL.md"
    if not skill.exists():
        err("SKILL.md not found")
    else:
        text = skill.read_text(encoding="utf-8")
        if "## Language Mode" not in text:
            err("SKILL.md: missing Language Mode section")
        if '"lang": "en|ja|zh"' not in text:
            err("SKILL.md: argument-hint missing lang option")
        if "NOVEL_COUNCIL_LANG" not in text:
            err("SKILL.md: missing NOVEL_COUNCIL_LANG env var reference")

    print()
    if errors:
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    if warnings:
        print(f"PASS with {len(warnings)} warning(s)")
        return 0
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
