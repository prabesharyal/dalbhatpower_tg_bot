"""Nepali horoscope (Rashifal) lookups via the configured RASIFAL endpoint."""
from __future__ import annotations

import json
from typing import Optional

import requests
from rapidfuzz import fuzz

from bot.config import get_config

# 12 zodiac entries with Nepali name, initials, and English aliases.
RASHIS = [
    {"np": "मेष", "initials": "चु, चे, चो, ला, लि, लु, ले, लो, अ", "en": "mesh aries"},
    {"np": "वृष", "initials": "इ, उ, ए, ओ, वा, वि, वु, वे, वो", "en": "brishabha vrisav taurus"},
    {"np": "मिथुन", "initials": "का, कि, कु, घ, ङ, छ, के, को, हा", "en": "mithun gemini"},
    {"np": "कर्कट", "initials": "हि, हु, हे, हो, डा, डि, डु, डे, डो", "en": "karkat cancer"},
    {"np": "सिंह", "initials": "मा, मि, मु, मे, मो, टा, टि, टु, टे", "en": "simha singh leo"},
    {"np": "कन्या", "initials": "टो, पा, पि, पु, ष, ण, ठ, पे, पो", "en": "kanya virgo"},
    {"np": "तुला", "initials": "रा, रि, रु, रे, रो, ता, ति, तु, ते", "en": "tula libra"},
    {"np": "वृश्चिक", "initials": "तो, ना, नि, नु, ने, नो, या, यि, यु", "en": "vrishchik scorpio"},
    {"np": "धनु", "initials": "ये, यो, भा, भि, भु, धा, फा, ढा, भे", "en": "dhanu sagittarius"},
    {"np": "मकर", "initials": "भो, जा, जि, जु, जे, जो, ख, खि, खु", "en": "makar capricorn"},
    {"np": "कुम्भ", "initials": "गु, गे, गो, सा, सि, सु, से, सो, दा", "en": "kumbh aquarius"},
    {"np": "मीन", "initials": "दि, दु, थ, झ, ञ, दे, दो, चा, चि", "en": "meen pisces"},
]


def _index_for(query: str) -> int:
    """Return 0-11 for a recognised rashi, -1 for invalid number, -2 for no match."""
    query = (query or "").strip()
    if not query:
        return -2
    if query.isdigit():
        n = int(query) - 1
        return n if 0 <= n <= 11 else -1
    # Direct Nepali name match
    for i, r in enumerate(RASHIS):
        if r["np"] in query:
            return i
    # English fuzzy match
    best_idx, best_score = -2, 0
    for i, r in enumerate(RASHIS):
        score = fuzz.partial_ratio(query.lower(), r["en"])
        if score > best_score:
            best_idx, best_score = i, score
    return best_idx if best_score >= 80 else -2


def _fetch() -> Optional[dict]:
    cfg = get_config()
    if not cfg.rasifal_api_url:
        return None
    try:
        resp = requests.get(cfg.rasifal_api_url, timeout=10)
        resp.raise_for_status()
        return json.loads(resp.json()["list"][0]["value"])
    except Exception as e:
        print(f"Rasifal fetch failed: {e}")
        return None


def all_horoscopes() -> str:
    info = _fetch()
    if not info:
        return "_Could not fetch rashifal right now._"
    out = [f"आज मिति **{info['date']}** को राशिफल।\n"]
    for item in info["items"]:
        out.append(f"***{item['rashi']}:***\n\t_{item['initials']}_\n`{item['desc']}`\n")
    return "\n".join(out)


def horoscope(query: str) -> tuple[str, int]:
    """Return (markdown, rashi_index 0-11 or sentinel 69)."""
    idx = _index_for(query)
    if idx == -1:
        return "Please enter value in proper range [1-12].", 69
    if idx == -2:
        return "No such horoscope exists.", 69
    info = _fetch()
    if not info:
        return "_Could not fetch rashifal right now._", 69
    item = info["items"][idx]
    desc = item["desc"].split("\r")[0] if idx == 11 else item["desc"]
    out = (
        f"मिति : *{info['date']}*\n\n"
        f"राशि : ***{item['rashi']}***\n\nअक्षर : *{item['initials']}*\n\n"
        f"राशिफल : {desc}"
    )
    return out, idx
