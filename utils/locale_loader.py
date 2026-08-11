#!/usr/bin/env python3
"""Shared locale loader for the Novel Council Layer utilities.

Language resolution order (standard three-tier pattern):
    1. CLI flag `--lang {en,ja,zh}`   (passed explicitly by callers)
    2. Environment variable `NOVEL_COUNCIL_LANG`
    3. Default `en`

The locale files under `locales/{en,ja,zh}.json` share one key structure; a
missing key in any language is a bug and is reported on load.
"""

import json
import os
import sys

_ENV_VAR = "NOVEL_COUNCIL_LANG"
_DEFAULT_LANG = "en"
_SUPPORTED = ("en", "ja", "zh")

_CACHE = {}


def resolve_lang(cli_lang=None):
    """Resolve the active language from CLI / env / default (in that order)."""
    lang = cli_lang or os.environ.get(_ENV_VAR) or _DEFAULT_LANG
    lang = lang.lower()
    if lang not in _SUPPORTED:
        sys.stderr.write(
            f"Warning: unsupported language '{lang}' (supported: {', '.join(_SUPPORTED)}), "
            f"falling back to '{_DEFAULT_LANG}'\n"
        )
        return _DEFAULT_LANG
    return lang


def load_locale(lang=None):
    """Load the locale dict for a language. Cached; validates key parity vs en."""
    lang = resolve_lang(lang)
    if lang not in _CACHE:
        base = os.path.join(os.path.dirname(__file__), "..", "locales")
        with open(os.path.join(base, f"{lang}.json"), encoding="utf-8") as f:
            locale = json.load(f)
        if lang != _DEFAULT_LANG:
            # Structural guard: every language must expose the same top-level keys as en.
            with open(os.path.join(base, f"{_DEFAULT_LANG}.json"), encoding="utf-8") as f:
                en = json.load(f)
            _check_keys(locale, en, prefix="")
        _CACHE[lang] = locale
    return _CACHE[lang]


def _check_keys(locale, en, prefix):
    missing = set(en.keys()) - set(locale.keys())
    extra = set(locale.keys()) - set(en.keys())
    if missing:
        raise KeyError(f"locale is missing keys vs en: {sorted(prefix + k for k in missing)}")
    if extra:
        raise KeyError(f"locale has extra keys vs en: {sorted(prefix + k for k in extra)}")
    for k in en.keys():
        if isinstance(en[k], dict) and isinstance(locale.get(k), dict):
            _check_keys(locale[k], en[k], prefix=f"{prefix}{k}.")


def t(locale, section, key, **kwargs):
    """Fetch and format a locale string: t(locale, 'render', 'subject')."""
    value = locale[section][key]
    if kwargs:
        return value.format(**kwargs)
    return value
