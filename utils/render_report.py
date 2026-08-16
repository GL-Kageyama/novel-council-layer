#!/usr/bin/env python3
"""Render a Novel Council Story Report (or a single evaluator output) as a
human-friendly visual report: classification badge, story-vector bar chart,
disagreement highlights, executive summary, and recommendations.

Usage:
    python utils/render_report.py < report.json
    python utils/render_report.py report.json
    python utils/render_report.py report.json -o report.md
    python utils/render_report.py report.json --lang ja

This is the presentation layer only. The machine contract is the JSON itself
(evaluators: schemas/novel-value-output.schema.json; council: the Story Report
structure in skills/story-council/SKILL.md). JSON stays the interchange
format; this script makes it readable by humans. The UI language is resolved
by --lang / NOVEL_COUNCIL_LANG / en (default).
"""

import json
import sys

from locale_loader import load_locale, resolve_lang, t

DIMENSION_KEYS = [
    "narrative_originality",
    "quality",
    "emotional_power",
    "plot_architecture",
    "character_depth",
    "prose_style",
    "theme_resonance",
    "world_building",
    "narrative_technique",
    "reader_experience",
    "admiration",
]

DIMENSIONS = []   # filled from locale in main()
CLASS_BADGE = {}  # filled from locale in main()
L = {}            # active locale

BAR_WIDTH = 36
LINE = "─" * 54

EVAL_TO_DIM = {
    "narrative-originality": "narrative_originality",
    "anti-generic-story-filter": "quality",
    "emotional-power": "emotional_power",
    "plot-architecture": "plot_architecture",
    "character-depth": "character_depth",
    "prose-style": "prose_style",
    "theme-resonance": "theme_resonance",
    "world-building": "world_building",
    "narrative-technique": "narrative_technique",
    "reader-experience": "reader_experience",
    "admiration": "admiration",
}


def bar(score):
    """Fixed 0-100 scale bar. High bars are deliberately rare to earn."""
    if score is None:
        return "░" * BAR_WIDTH
    filled = max(0, min(100, int(score))) * BAR_WIDTH // 100
    return "█" * filled + "░" * (BAR_WIDTH - filled)


def f(v):
    return "—" if v is None else f"{v:3d}"


def header(title):
    print(f"\n┌{'─' * 54}┐")
    print(f"│ {title}")
    print(f"└{'─' * 54}┘")


def vector_of(obj):
    """Read the composite vector from a council report (story_vector)."""
    return obj.get("story_vector") or obj.get("value_vector") or {}


def excluded_ids(obj):
    """Set of dimension keys excluded from aggregation.
    Normalizes evaluator_id (kebab-case) to story-vector dimension keys."""
    out = set()
    for e in (obj.get("excluded_evaluators") or []):
        eid = e.get("evaluator_id") if isinstance(e, dict) else e
        out.add(EVAL_TO_DIM.get(eid, eid))
    return out


def render_story_vector(vector):
    print(f"\n{t(L, 'render', 'vector_header')}")
    print(f"  {t(L, 'render', 'vector_cols'):16s} {t(L, 'render', 'vector_bar'):<{BAR_WIDTH}} {t(L, 'render', 'vector_score')}")
    any_scored = False
    for key, jp in DIMENSIONS:
        entry = (vector or {}).get(key)
        if isinstance(entry, dict):
            mean = entry.get("mean")
            variance = entry.get("variance")
            n = len(entry.get("scores") or [])
        else:
            mean = entry
            variance = None
            n = None
        if mean is None and variance is None:
            continue
        any_scored = True
        extra = ""
        if variance is not None:
            mark = "⚠⚠" if variance > 400 else ("⚠" if variance >= 100 else "")
            extra = f"  n={n} var={variance} {mark}"
        print(f"  {jp + ' (' + key + ')':24s} {bar(mean)} {f(mean)}{extra}")
    if not any_scored:
        print(f"  {t(L, 'render', 'no_scored_dimensions')}")


def render_disagreement(vector):
    print(f"\n{t(L, 'render', 'disagreement_header')}")
    found = False
    for key, jp in DIMENSIONS:
        entry = (vector or {}).get(key)
        if not isinstance(entry, dict):
            continue
        scores = entry.get("scores") or []
        variance = entry.get("variance")
        if variance is None or len(set(scores)) < 2:
            continue
        found = True
        level = t(L, "disagreement_levels", "severe") if variance > 400 else (
            t(L, "disagreement_levels", "medium") if variance >= 100 else t(L, "disagreement_levels", "light"))
        print(f"  [{level}] {jp}({key}): スコア={scores}")
    if not found:
        print(f"  {t(L, 'disagreement_levels', 'none')}")


def contrast_pairs(vector, excluded=(), limit=4):
    """Cross-dimension contrasts (high axis >= 70 vs low axis <= 25), skipping
    excluded evaluators, most striking first."""
    scores = {}
    for key, jp in DIMENSIONS:
        if key in excluded:
            continue
        entry = (vector or {}).get(key)
        mean = entry.get("mean") if isinstance(entry, dict) else entry
        if mean is not None:
            scores[key] = mean
    pairs = []
    for hk, hv in scores.items():
        if hv < 70:
            continue
        for lk, lv in scores.items():
            if lk == hk or lv > 25:
                continue
            pairs.append((hk, hv, lk, lv))
    pairs.sort(key=lambda p: -(p[1] - p[3]))
    return pairs[:limit]


def render_contrasts(vector, excluded=()):
    pairs = contrast_pairs(vector, excluded)
    if pairs:
        jp = {d[0]: d[1] for d in DIMENSIONS}
        print(f"\n{t(L, 'render', 'contrasts_header')}")
        for hk, hv, lk, lv in pairs:
            print(f"  ⚡ {jp[hk]}({hk}) {hv}  vs  {jp[lk]}({lk}) {lv}")
        print(f"  {t(L, 'render', 'contrasts_note')}")


def render_council(obj, show_ind=False):
    header(t(L, "render", "report_title"))
    badge = CLASS_BADGE.get(obj.get("classification"), obj.get("classification", "?"))
    print(f"\n  {t(L, 'render', 'classification')} {badge}")

    current = obj.get("current_value_score")
    hidden = obj.get("hidden_potential_score")
    if current is not None or hidden is not None:
        cbar = bar(current)
        hbar = bar(hidden)
        print(f"\n  {t(L, 'render', 'current_value')} {f(current)}  {cbar}")
        print(f"  {t(L, 'render', 'hidden_potential')} {f(hidden)}  {hbar}")

    print(f"\n  {t(L, 'render', 'subject')} {obj.get('content_summary', '—')}")
    print(f"  {t(L, 'render', 'domain_consulted', domain=obj.get('domain', '—'), count=len(obj.get('evaluators_consulted', []) or []))}")

    nc = obj.get("non_consulted_evaluators") or []
    if nc:
        print(f"  {t(L, 'render', 'non_consulted_title')}")
        for e in nc:
            eid = e.get("evaluator_id") if isinstance(e, dict) else e
            reason = e.get("reason", "") if isinstance(e, dict) else ""
            print(f"    · {eid}: {reason or t(L, 'render', 'reason_fallback')}")

    excl = obj.get("excluded_evaluators") or []
    if excl:
        print(f"  {t(L, 'render', 'excluded_title')}")
        for e in excl:
            eid = e.get("evaluator_id") if isinstance(e, dict) else e
            reason = e.get("reason", "") if isinstance(e, dict) else ""
            print(f"    · {eid}: {reason or t(L, 'render', 'reason_fallback')}")

    vector = vector_of(obj)
    render_story_vector(vector)
    render_disagreement(vector)
    render_contrasts(vector, excluded_ids(obj))

    if obj.get("executive_summary"):
        print(f"\n{t(L, 'render', 'executive_summary_title')}\n  {obj['executive_summary']}")

    if obj.get("consensus_summary"):
        print(f"\n{t(L, 'render', 'consensus_title')}\n  {obj['consensus_summary']}")

    recs = obj.get("recommendations") or []
    if recs:
        print(f"\n{t(L, 'render', 'recommendations_title')}")
        for i, r in enumerate(recs, 1):
            print(f"  {i}. {r}")

    rd = obj.get("revision_direction")
    if rd:
        mode = rd.get("iteration") or "confirm"
        label = t(L, "iteration_labels", mode) if mode in ("confirm", "persistent") else mode
        print(f"\n{t(L, 'render', 'revision_direction_title', mode=label)}")
        if rd.get("statement"):
            print(f"  {t(L, 'render', 'direction')} {rd['statement']}")
        axis = rd.get("axis") or []
        if axis:
            print(f"  {t(L, 'render', 'axis')} {', '.join(axis)}")
        keep = rd.get("preserve") or []
        if keep:
            print(f"  {t(L, 'render', 'preserve')} {', '.join(keep)}")

    caves = obj.get("caveats") or []
    if caves:
        print(f"\n{t(L, 'render', 'caveats_title')}")
        for c in caves:
            print(f"  · {c}")

    ind = obj.get("individual_reports") or []
    if ind:
        if show_ind:
            print(f"\n{t(L, 'render', 'individuals_title', count=len(ind))}")
            for r in ind:
                render_evaluator(r)
        else:
            print(f"\n{t(L, 'render', 'individuals_hidden', count=len(ind))}")


def render_evaluator(obj):
    header(f"🔎 {obj.get('evaluator_name', obj.get('evaluator_id', 'Evaluator'))}")
    badge = CLASS_BADGE.get(obj.get("classification"), obj.get("classification", "?"))
    print(f"\n  {t(L, 'render', 'evaluator_class_confidence', badge=badge, conf=f(obj.get('confidence')))}")
    print(f"\n  {t(L, 'render', 'primary_score')} {f(obj.get('primary_score'))}  {bar(obj.get('primary_score'))}")
    if obj.get("primary_score_rationale"):
        print(f"  {t(L, 'render', 'rationale')} {obj['primary_score_rationale']}")

    ds = obj.get("dimension_scores") or {}
    if ds:
        print(f"\n{t(L, 'render', 'dimensions_title')}")
        for name, d in ds.items():
            w = d.get("weight", 0)
            print(f"  {name:24s} {bar(d.get('score'))} {f(d.get('score'))}  (w={w})")
            if d.get("evidence"):
                print(f"    ↳ {d['evidence']}")

    if obj.get("unique_perspective"):
        print(f"\n{t(L, 'render', 'unique_perspective_title')}\n  {obj['unique_perspective']}")

    if obj.get("expected_disagreement_points"):
        print(f"\n{t(L, 'render', 'disagreement_points_title')}")
        for p in obj["expected_disagreement_points"]:
            print(f"  · {p.get('evaluator_type')}: {p.get('predicted_stance')}")

    if obj.get("narrative"):
        print(f"\n{t(L, 'render', 'narrative_title')}\n  {obj['narrative']}")


def md_bar(score, width=20):
    """Compact bar for Markdown table cells."""
    if score is None:
        return "—"
    filled = max(0, min(100, int(score))) * width // 100
    return "█" * filled + "░" * (width - filled)


def md_val(v):
    return "—" if v is None else f"{v}"


def render_council_md(obj, show_ind=False):
    """Readable Markdown report (suitable for .md files / GitHub preview)."""
    Lmd = []
    Lmd.append("# 📖 Novel Council Story Report")
    Lmd.append("")
    Lmd.append(f"> **{t(L, 'render', 'classification')}** {CLASS_BADGE.get(obj.get('classification'), obj.get('classification', '?'))}")
    Lmd.append("")

    # Summary table
    Lmd.append(t(L, "render", "md_summary_title"))
    Lmd.append("")
    Lmd.append(f"| {t(L, 'render', 'md_summary_col_item')} | {t(L, 'render', 'md_summary_col_value')} |")
    Lmd.append("|------|-----|")
    Lmd.append(f"| {t(L, 'render', 'md_subject')} | {obj.get('content_summary', '—')} |")
    Lmd.append(f"| {t(L, 'render', 'md_domain')} | {obj.get('domain', '—')} |")
    Lmd.append(f"| {t(L, 'render', 'md_consulted')} | {len(obj.get('evaluators_consulted', []) or [])} |")
    Lmd.append(f"| {t(L, 'render', 'md_current')} | {md_val(obj.get('current_value_score'))} |")
    Lmd.append(f"| {t(L, 'render', 'md_hidden')} | {md_val(obj.get('hidden_potential_score'))} |")
    Lmd.append("")

    # Non-consulted evaluators (plot mode etc.)
    nc = obj.get("non_consulted_evaluators") or []
    if nc:
        Lmd.append(t(L, "render", "md_non_consulted_title"))
        Lmd.append("")
        Lmd.append(f"| {t(L, 'render', 'md_col_evaluator')} | {t(L, 'render', 'md_col_reason')} |")
        Lmd.append("|--------|------|")
        for e in nc:
            eid = e.get("evaluator_id") if isinstance(e, dict) else e
            reason = e.get("reason", "") if isinstance(e, dict) else ""
            Lmd.append(f"| `{eid}` | {reason or t(L, 'render', 'reason_fallback')} |")
        Lmd.append("")

    # Excluded evaluators
    excl = obj.get("excluded_evaluators") or []
    if excl:
        Lmd.append(t(L, "render", "md_excluded_title"))
        Lmd.append("")
        Lmd.append(f"| {t(L, 'render', 'md_col_evaluator')} | {t(L, 'render', 'md_col_reason')} |")
        Lmd.append("|--------|------|")
        for e in excl:
            eid = e.get("evaluator_id") if isinstance(e, dict) else e
            reason = e.get("reason", "") if isinstance(e, dict) else ""
            Lmd.append(f"| `{eid}` | {reason or t(L, 'render', 'reason_fallback')} |")
        Lmd.append("")

    # Story vector
    Lmd.append(t(L, "render", "md_vector_title"))
    Lmd.append("")
    Lmd.append(f"| {t(L, 'render', 'md_vector_cols')} |")
    Lmd.append("|------|:------:|:----:|------|")
    vec = vector_of(obj)
    any_scored = False
    for key, jp in DIMENSIONS:
        entry = vec.get(key)
        if isinstance(entry, dict):
            mean = entry.get("mean")
            variance = entry.get("variance")
            scores = entry.get("scores") or []
        else:
            mean = entry
            variance = None
            scores = []
        if mean is None and variance is None:
            continue
        any_scored = True
        v = f"{variance}" if variance is not None else "—"
        n = f" (n={len(scores)})" if scores else ""
        Lmd.append(f"| {jp} (`{key}`) | {md_val(mean)} | {v}{n} | `{md_bar(mean)}` |")
    if not any_scored:
        Lmd.append(t(L, "render", "md_no_scored"))
    Lmd.append("")

    # Disagreement
    Lmd.append(t(L, "render", "md_disagreement_title"))
    Lmd.append("")
    found = False
    for key, jp in DIMENSIONS:
        entry = vec.get(key)
        if not isinstance(entry, dict):
            continue
        scores = entry.get("scores") or []
        variance = entry.get("variance")
        if variance is None or len(set(scores)) < 2:
            continue
        found = True
        level = t(L, "disagreement_levels", "severe") if variance > 400 else (
            t(L, "disagreement_levels", "medium") if variance >= 100 else t(L, "disagreement_levels", "light"))
        Lmd.append(f"- **[{level}]** {jp}（`{key}`）: スコア = {scores}")
    if not found:
        Lmd.append(t(L, "render", "md_disagreement_none"))
    Lmd.append("")

    # Contrasts (skip excluded evaluators, show most striking)
    pairs = contrast_pairs(vec, excluded_ids(obj))
    if pairs:
        Lmd.append(t(L, "render", "md_contrasts_title"))
        Lmd.append("")
        Lmd.append(f"| {t(L, 'render', 'md_contrasts_cols')} |")
        Lmd.append("|-----------|-----------|")
        idx = {d[0]: d[1] for d in DIMENSIONS}
        for hk, hv, lk, lv in pairs:
            Lmd.append(f"| {idx[hk]}（`{hk}`）{hv} | {idx[lk]}（`{lk}`）{lv} |")
        Lmd.append("")
        Lmd.append(t(L, "render", "md_contrasts_note"))
        Lmd.append("")

    if obj.get("executive_summary"):
        Lmd.append(t(L, "render", "md_executive_title"))
        Lmd.append("")
        Lmd.append(f"> {obj['executive_summary']}")
        Lmd.append("")

    if obj.get("consensus_summary"):
        Lmd.append(t(L, "render", "md_consensus_title"))
        Lmd.append("")
        Lmd.append(obj["consensus_summary"])
        Lmd.append("")

    recs = obj.get("recommendations") or []
    if recs:
        Lmd.append(t(L, "render", "md_recommendations_title"))
        Lmd.append("")
        for i, r in enumerate(recs, 1):
            Lmd.append(f"{i}. {r}")
        Lmd.append("")

    rd = obj.get("revision_direction")
    if rd:
        mode = rd.get("iteration") or "confirm"
        label = t(L, "iteration_labels", mode) if mode in ("confirm", "persistent") else mode
        Lmd.append(t(L, "render", "md_revision_title", mode=label))
        Lmd.append("")
        if rd.get("statement"):
            Lmd.append(f"> {rd['statement']}")
            Lmd.append("")
        if rd.get("axis"):
            Lmd.append(t(L, "render", "md_axis"))
            for a in rd["axis"]:
                Lmd.append(f"- {a}")
            Lmd.append("")
        if rd.get("preserve"):
            Lmd.append(t(L, "render", "md_preserve"))
            for p in rd["preserve"]:
                Lmd.append(f"- {p}")
            Lmd.append("")

    caves = obj.get("caveats") or []
    if caves:
        Lmd.append(t(L, "render", "md_caveats_title"))
        Lmd.append("")
        for c in caves:
            Lmd.append(f"- {c}")
        Lmd.append("")

    ind = obj.get("individual_reports") or []
    if ind:
        if show_ind:
            Lmd.append(t(L, "render", "md_individuals_all_title"))
            Lmd.append("")
            for r in ind:
                Lmd.append("")
                Lmd.append(render_evaluator_md(r))
        else:
            Lmd.append(t(L, "render", "md_individuals_material_title"))
            Lmd.append("")
            Lmd.append(t(L, "render", "md_individuals_material_body"))
            Lmd.append("")

    return "\n".join(Lmd)


def render_evaluator_md(obj):
    Lmd = []
    Lmd.append(f"# 🔎 {obj.get('evaluator_name', obj.get('evaluator_id', 'Evaluator'))}")
    Lmd.append("")
    badge = CLASS_BADGE.get(obj.get("classification"), obj.get("classification", "?"))
    Lmd.append(f"> **{t(L, 'render', 'classification')}** {badge}  |  {t(L, 'render', 'confidence_label')}: {md_val(obj.get('confidence'))}")
    Lmd.append("")
    Lmd.append(f"**{t(L, 'render', 'primary_score')}** {md_val(obj.get('primary_score'))}  `{md_bar(obj.get('primary_score'))}`")
    if obj.get("primary_score_rationale"):
        Lmd.append("")
        Lmd.append(f"*{obj['primary_score_rationale']}*")
    Lmd.append("")
    ds = obj.get("dimension_scores") or {}
    if ds:
        Lmd.append(t(L, "render", "md_evaluator_dimensions_title"))
        Lmd.append("")
        Lmd.append(f"| {t(L, 'render', 'md_evaluator_dim_cols')} |")
        Lmd.append("|------|:------:|:----:|")
        for name, d in ds.items():
            Lmd.append(f"| {name} | {md_val(d.get('score'))} | {d.get('weight', '—')} |")
            if d.get("evidence"):
                Lmd.append(f"| ↳ {d['evidence']} | | |")
        Lmd.append("")
    if obj.get("unique_perspective"):
        Lmd.append(t(L, "render", "md_evaluator_unique_title"))
        Lmd.append("")
        Lmd.append(obj["unique_perspective"])
        Lmd.append("")
    if obj.get("expected_disagreement_points"):
        Lmd.append(t(L, "render", "md_evaluator_disagreement_title"))
        Lmd.append("")
        for p in obj["expected_disagreement_points"]:
            Lmd.append(f"- **{p.get('evaluator_type')}**: {p.get('predicted_stance')}")
        Lmd.append("")
    if obj.get("narrative"):
        Lmd.append(t(L, "render", "md_evaluator_narrative_title"))
        Lmd.append("")
        Lmd.append(obj["narrative"])
        Lmd.append("")
    return "\n".join(Lmd)


def main():
    args = [a for a in sys.argv[1:]]
    out_format = "console"
    out_file = None
    show_ind = False
    lang = None
    format_set = False
    positional = []
    i = 0
    while i < len(args):
        a = args[i]
        if a in ("--format", "-f") and i + 1 < len(args):
            out_format = args[i + 1]
            format_set = True
            i += 2
        elif a in ("--output", "-o") and i + 1 < len(args):
            out_file = args[i + 1]
            i += 2
        elif a in ("--individuals", "--ind"):
            show_ind = True
            i += 1
        elif a in ("--lang", "-l") and i + 1 < len(args):
            lang = args[i + 1]
            i += 2
        elif a in ("--help", "-h"):
            print("Usage: python utils/render_report.py [--format console|md] [--output FILE] [--individuals] [--lang en|ja|zh] [report.json]",
                  file=sys.stderr)
            return 0
        else:
            positional.append(a)
            i += 1

    # Activate locale (module globals used by the render functions).
    global DIMENSIONS, CLASS_BADGE, L
    L = load_locale(lang)
    DIMENSIONS = [(k, L["dimensions"][k]) for k in DIMENSION_KEYS]
    CLASS_BADGE = L["class_badges"]

    # Auto-detect Markdown output: -o report.md produces MD without --format.
    if not format_set and out_file and out_file.endswith(".md"):
        out_format = "md"

    if out_format not in ("console", "md"):
        print("--format must be 'console' or 'md'", file=sys.stderr)
        return 1
    if len(positional) > 1:
        print("Usage: python utils/render_report.py [--format console|md] [--output FILE] [report.json]",
              file=sys.stderr)
        return 2

    try:
        if positional:
            with open(positional[0], encoding="utf-8") as f:
                obj = json.load(f)
        else:
            obj = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"Could not read input: {e}", file=sys.stderr)
        return 2

    if isinstance(obj, dict) and "report_id" in obj:
        text = render_council_md(obj, show_ind) if out_format == "md" else _console_council(obj, show_ind)
    elif isinstance(obj, dict) and "evaluator_id" in obj:
        text = render_evaluator_md(obj) if out_format == "md" else _console_evaluator(obj)
    else:
        print("Input is neither a council report (report_id) nor an evaluator output (evaluator_id).",
              file=sys.stderr)
        return 1

    if out_file:
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(text + "\n")
        print(t(L, "render", "wrote", path=out_file))
    else:
        print(text)
    return 0


def _console_council(obj, show_ind=False):
    import io
    buf = io.StringIO()
    import contextlib
    with contextlib.redirect_stdout(buf):
        render_council(obj, show_ind)
    return buf.getvalue()


def _console_evaluator(obj):
    import io
    buf = io.StringIO()
    import contextlib
    with contextlib.redirect_stdout(buf):
        render_evaluator(obj)
    return buf.getvalue()


if __name__ == "__main__":
    sys.exit(main())
