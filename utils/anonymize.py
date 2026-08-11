#!/usr/bin/env python3
"""Anonymize a novel input for double-blind evaluation (the first blind).

Removes author names and work titles from the text before it is handed to
the evaluator agents, so evaluation is based on the text alone. This is the
preprocessing step for the first blind (input anonymization) described in
the Novel Council strategy (double-blind evaluation, §4).

Usage:
    python utils/anonymize.py input.txt --author "著者名" --title "作品名" > anonymized.txt
    cat input.txt | python utils/anonymize.py --author "名前A" --author "名前B"
    python utils/anonymize.py input.txt --author "名前" --report
    python utils/anonymize.py input.txt --lang ja

Options:
    --author NAME     Author name to redact (repeatable)
    --title TITLE     Work title to redact (repeatable)
    --name NAME       Any proper noun to redact (repeatable; generic alias)
    --placeholder TEXT   Replacement text (default: locale-specific, e.g. 〔匿名〕 for ja)
    --report          Print a redaction summary to stderr
    --lang LANG       UI language (en, ja, zh; default: NOVEL_COUNCIL_LANG or en)
    --help            Show this help

The redaction is a plain string replacement over the whole text, including
occurrences inside sentences. Titles are also replaced when they appear
enclosed in 《》 or 『』 brackets.
"""

import argparse
import sys

from locale_loader import load_locale, t


def read_input(path):
    if path:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return sys.stdin.read()


def redact(text, names, placeholder):
    """Replace every occurrence of each name with the placeholder.
    Returns (redacted_text, counts_by_name)."""
    counts = {}
    for name in names:
        if not name:
            continue
        n = text.count(name)
        if n > 0:
            text = text.replace(name, placeholder)
        counts[name] = n
    return text, counts


def main():
    parser = argparse.ArgumentParser(
        prog="anonymize.py",
        description="Anonymize a novel input (remove author/title names) for double-blind evaluation.",
    )
    parser.add_argument("input", nargs="?", help="input text file (default: stdin)")
    parser.add_argument("--author", action="append", default=[], help="author name to redact (repeatable)")
    parser.add_argument("--title", action="append", default=[], help="work title to redact (repeatable)")
    parser.add_argument("--name", action="append", default=[], help="any proper noun to redact (repeatable)")
    parser.add_argument("--placeholder", default=None, help="replacement text (default: locale-specific)")
    parser.add_argument("--report", action="store_true", help="print a redaction summary to stderr")
    parser.add_argument("--lang", default=None, help="UI language (en, ja, zh; default: NOVEL_COUNCIL_LANG or en)")
    args = parser.parse_args()

    L = load_locale(args.lang)
    if args.placeholder is None:
        args.placeholder = t(L, "anonymize", "placeholder_default")

    try:
        text = read_input(args.input)
    except OSError as e:
        print(f"Could not read input: {e}", file=sys.stderr)
        return 2

    names = list(args.author) + list(args.title) + list(args.name)

    # Also redact bracketed forms of titles: 《title》 and 『title』
    bracketed = []
    for title in args.title:
        if title:
            bracketed.append(f"《{title}》")
            bracketed.append(f"『{title}』")
    names = names + bracketed

    redacted, counts = redact(text, names, args.placeholder)

    if args.report:
        total = sum(counts.values())
        for name in args.author + args.title + args.name:
            if name:
                print(t(L, "anonymize", "redacted_line", count=counts.get(name, 0), name=name), file=sys.stderr)
        print(t(L, "anonymize", "redacted_summary", total=total, placeholder=args.placeholder), file=sys.stderr)

    sys.stdout.write(redacted)
    return 0


if __name__ == "__main__":
    sys.exit(main())
