"""Nepali dictionary lookup against the bundled ``nepali_dict.json``.

The data set is large (~31 MB) so we load and cache it once at first use.
"""
from __future__ import annotations

import json
import os
from functools import lru_cache

DATA_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "nepali_dict.json"
)


@lru_cache(maxsize=1)
def _load() -> list[dict]:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def lookup(word: str) -> str:
    """Return a markdown-formatted dictionary entry, or a 'not found' note."""
    word = (word or "").strip()
    if not word:
        return "_Please send a Nepali word to look up._"
    for item in _load():
        if item.get("word") == word:
            out = [f"शब्द: **{item['word']}**", "अर्थहरू:"]
            for definition in item.get("definitions", []):
                out.append(f"\t{definition.get('grammar', '')}")
                for sense in definition.get("senses", []):
                    out.append(f"\t\t- {sense}")
            return "\n".join(out)
    return "_Unfortunately, no such word was found in the database._"
