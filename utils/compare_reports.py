#!/usr/bin/env python3
"""Compare two Novel Council Story Reports (before / after a revision) and
show the improvement per dimension. This powers the write → evaluate →
rewrite loop: run the council on v1, revise per the evaluators' material,
run the council on v2, then compare.

Usage:
    python utils/compare_reports.py before.json after.json
    python utils/compare_reports.py --before before.json --after after.json
    python utils/compare_reports.py before.json after.json --lang ja

Exit codes:
    0  compared (improvement or not — the report says which)
    1  usage / parse error
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

ARROWS = {"up": "▲", "down": "▼", "same": "—"}


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def dim_mean(report, key):
    vec = report.get("story_vector") or report.get("value_vector") or {}
    entry = vec.get(key)
    if isinstance(entry, dict):
        return entry.get("mean")
    return entry


def main():
    # Extract --lang first (it may appear anywhere in argv).
    argv = list(sys.argv[1:])
    lang = None
    if "--lang" in argv:
        i = argv.index("--lang")
        if i + 1 < len(argv):
            lang = argv[i + 1]
            del argv[i:i + 2]
    if argv and argv[0] == "--lang":  # defensive; not reached normally
        pass

    global DIMENSIONS, CLASS_BADGE, L
    L = load_locale(lang)
    DIMENSIONS = [(k, L["dimensions"][k]) for k in DIMENSION_KEYS]
    CLASS_BADGE = L["class_badges"]

    if len(argv) == 2:
        before_path, after_path = argv[0], argv[1]
    elif len(argv) == 4 and argv[0] == "--before" and argv[2] == "--after":
        before_path, after_path = argv[1], argv[3]
    else:
        print("Usage: python utils/compare_reports.py before.json after.json [--lang en|ja|zh]", file=sys.stderr)
        return 1

    try:
        before, after = load(before_path), load(after_path)
    except (OSError, json.JSONDecodeError) as e:
        print(f"Could not read reports: {e}", file=sys.stderr)
        return 1

    print("┌──────────────────────────────────────────────────────┐")
    print(f"│ {t(L, 'compare', 'header_title')}")
    print("└──────────────────────────────────────────────────────┘")

    print(f"\n  {t(L, 'compare', 'classification_change')}")
    bcls = CLASS_BADGE.get(before.get("classification"), before.get("classification", "?"))
    acls = CLASS_BADGE.get(after.get("classification"), after.get("classification", "?"))
    print(f"    {t(L, 'compare', 'before')}: {bcls}")
    print(f"    {t(L, 'compare', 'after')}:  {acls}")

    print(f"\n{t(L, 'compare', 'dims_title')}")
    cols = [c.strip() for c in t(L, "compare", "dims_cols").split("|")]
    print(f"  {cols[0]:22s} {cols[1]:>7s} {cols[2]:>6s} {cols[3]:>5s}")
    total = 0
    counted = 0
    changed = []
    for key, jp in DIMENSIONS:
        b = dim_mean(before, key)
        a = dim_mean(after, key)
        if b is None and a is None:
            continue
        if a is not None and b is not None:
            delta = a - b
            total += delta
            counted += 1
            if delta != 0:
                changed.append((jp, b, a, delta))
            arrow = ARROWS["up"] if delta > 0 else (ARROWS["down"] if delta < 0 else ARROWS["same"])
            b_s = f"{b:3d}" if b is not None else "  —"
            a_s = f"{a:3d}" if a is not None else "  —"
            d_s = f"{delta:+3d}" if b is not None and a is not None else "   "
            print(f"  {jp + ' (' + key + ')':28s} {b_s:>5s} {a_s:>5s} {arrow}{d_s}")
        else:
            print(f"  {jp + ' (' + key + ')':28s}   {'—' if b is None else b} -> {'—' if a is None else a}  ({t(L, 'compare', 'one_sided')})")

    if counted:
        avg = total / counted
        print(f"\n  {t(L, 'compare', 'average_change', count=counted, total=total, avg=avg)}")

    print(f"\n{t(L, 'compare', 'main_changes_title')}")
    if not changed:
        print(f"  {t(L, 'compare', 'no_significant_changes')}")
    else:
        changed_sorted = sorted(changed, key=lambda c: -abs(c[3]))
        for jp, b, a, d in changed_sorted[:6]:
            arrow = ARROWS["up"] if d > 0 else ARROWS["down"]
            print(f"  {arrow} {jp}: {b} → {a} ({d:+d})")

    print()
    print(t(L, "compare", "note_raw_values"))
    print(t(L, "compare", "note_rewrite_input"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
