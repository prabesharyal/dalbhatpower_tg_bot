"""Gotra/surname lookup backed by the public gotrafinder.com JSON API.

Docs: https://gotrafinder.com/docs/

Keeping the network call thin: we hit /api/search and /api/surname/{slug}
and reshape the response into the bot's existing message templates so handlers
don't need to know the API exists.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import requests

API_BASE = "https://gotrafinder.com"
TIMEOUT = 10


@dataclass
class SurnameResult:
    slug: str
    en: str
    np: Optional[str]
    gotras: list[dict]  # [{en, np, slug, lineage_en, pravara}]
    sahagotri_groups: list[dict]  # [{gotra_en, gotra_np, surnames:[...]}]


@dataclass
class GotraResult:
    slug: str
    en: str
    np: Optional[str]
    pravaras: list[str]
    surnames: list[dict]  # [{en, np}]


class GotraFinderError(Exception):
    pass


def _get(path: str, **params) -> dict:
    resp = requests.get(f"{API_BASE}{path}", params=params, timeout=TIMEOUT,
                        headers={"User-Agent": "DalBhatPowerBot/2.1"})
    resp.raise_for_status()
    return resp.json()


def search_surname(query: str) -> Optional[SurnameResult]:
    """Look up a surname (English/Nepali/variation). Returns None if not found."""
    data = _get("/api/search", q=query, type="surname")
    if not data.get("success"):
        return None
    slug = data["query"]["match"]["surnameId"] if data["query"].get("match") else None
    if slug is None:
        return None
    # /api/search returns just the surname; the full payload (with sahagotris)
    # comes from /api/surname/{slug}.
    surname_slug = data["result"]["surname"]["slug"]
    full = _get(f"/api/surname/{surname_slug}")
    if not full.get("success"):
        return None
    surname = full["result"]["surname"]
    lineages = full["result"].get("lineages", []) or []
    gotras = [
        {
            "en": ln["gotra"]["en"],
            "np": ln["gotra"].get("np"),
            "slug": ln["gotra"]["slug"],
            "lineage_en": (ln.get("lineage") or {}).get("en"),
            "pravara": (ln.get("pravaras") or [{}])[0].get("sequenceEn"),
        }
        for ln in lineages
    ]
    sahagotris = [
        {
            "gotra_en": grp["gotra"]["en"],
            "gotra_np": grp["gotra"].get("np"),
            "surnames": [{"en": s["en"], "np": s.get("np")} for s in grp.get("surnames", [])],
        }
        for grp in (full.get("sahagotris") or [])
    ]
    return SurnameResult(
        slug=surname["slug"],
        en=surname["root"]["en"],
        np=surname["root"].get("np"),
        gotras=gotras,
        sahagotri_groups=sahagotris,
    )


def search_gotra(query: str) -> Optional[GotraResult]:
    """Look up a gotra (English/Nepali). Returns None if not found."""
    data = _get("/api/search", q=query, type="gotra")
    if not data.get("success"):
        return None
    if not data["query"].get("match"):
        return None
    gotra_slug = data["result"]["gotra"]["slug"]
    full = _get(f"/api/gotra/{gotra_slug}")
    if not full.get("success"):
        return None
    g = full["result"]["gotra"]
    # /api/gotra returns surnames as either {en, np, ...} or wrapped
    # {surname: {en, np, ...}, lineage: {...}} entries — handle both.
    raw_surnames = full["result"].get("surnames") or []
    surnames = []
    for s in raw_surnames:
        inner = s.get("surname") if isinstance(s, dict) and "surname" in s else s
        if isinstance(inner, dict) and "en" in inner:
            surnames.append({"en": inner["en"], "np": inner.get("np")})
    return GotraResult(
        slug=g["slug"],
        en=g["en"],
        np=g.get("np"),
        pravaras=[p.get("sequenceEn") or p.get("description") or ""
                  for p in (full["result"].get("pravaras") or [])],
        surnames=surnames,
    )


# --- Markdown formatters used by handlers ---

def format_my_gotra(query: str, result: Optional[SurnameResult]) -> str:
    if not result or not result.gotras:
        return f"_No gotra found for surname *{query}*._"
    lines = [f"तपाइको थर ({result.en} / {result.np or '-'}) को सम्भावित गोत्रहरू:"]
    for g in result.gotras:
        line = f"• *{g['en']}* ({g['np'] or '-'})"
        if g.get("lineage_en") and g["lineage_en"].lower() != "default":
            line += f" — _lineage:_ {g['lineage_en']}"
        if g.get("pravara"):
            line += f"\n   _pravara:_ {g['pravara']}"
        lines.append(line)
    return "\n".join(lines)


def format_sahagotri(query: str, result: Optional[GotraResult]) -> str:
    if not result or not result.surnames:
        return f"_No surnames found for gotra *{query}*._"
    surnames = ", ".join(s["en"] for s in result.surnames)
    out = [f"गोत्र *{result.en}* ({result.np or '-'}) मा पर्ने थरहरू:", surnames]
    if result.pravaras:
        out.append("\n_Pravaras:_ " + "; ".join(p for p in result.pravaras if p))
    return "\n".join(out)


def format_findgotra(query: str) -> str:
    """Try both surname and gotra lookup; return whichever matches first."""
    surname = search_surname(query)
    if surname and surname.gotras:
        parts = [format_my_gotra(query, surname)]
        if surname.sahagotri_groups:
            parts.append("\n*Sahagotri थरहरू:*")
            for grp in surname.sahagotri_groups:
                names = ", ".join(s["en"] for s in grp["surnames"][:30])
                parts.append(f"• *{grp['gotra_en']}* ({grp['gotra_np'] or '-'}): {names}")
        return "\n".join(parts)
    gotra = search_gotra(query)
    if gotra:
        return format_sahagotri(query, gotra)
    return f"_No surname or gotra matched *{query}*._"
