"""Tests for the gotrafinder.com integration.

Most tests run against canned responses so they're fast and offline.
Live tests are marked `network` and skipped by default — run with
`pytest -m network` to exercise the real API.
"""
import json
from unittest.mock import patch

import pytest

from bot.services import gotra_service as gs


# --- Canned response fixtures -------------------------------------------------

SEARCH_ARYAL = {
    "success": True, "type": "surname",
    "query": {"raw": "Aryal", "normalized": "aryal",
              "match": {"matchedValue": "Aryal", "matchType": "variation_en", "surnameId": 3}},
    "result": {"surname": {"id": 3, "slug": "aryal",
                           "root": {"en": "Aryal", "np": "अर्याल"}}},
}

SURNAME_ARYAL_FULL = {
    "success": True,
    "result": {
        "surname": {"id": 3, "slug": "aryal", "root": {"en": "Aryal", "np": "अर्याल"}},
        "lineages": [{
            "lineage": {"en": "Default"},
            "gotra": {"en": "Atreya", "np": "आत्रेय", "slug": "atreya"},
            "pravaras": [{"sequenceEn": "Atri, Archananasa, Shyabashwo"}],
        }],
    },
    "sahagotris": [{
        "gotra": {"en": "Atreya", "np": "आत्रेय", "slug": "atreya"},
        "surnames": [{"en": "Bagale", "np": "बगाले"},
                     {"en": "Ghotane Gurung", "np": "घोटाने गुरुङ"}],
    }],
}

SEARCH_GOTRA_ATREYA = {
    "success": True, "type": "gotra",
    "query": {"raw": "Atreya", "match": {"gotraId": 10}},
    "result": {"gotra": {"id": 10, "slug": "atreya"}},
}

GOTRA_ATREYA_FULL = {
    "success": True,
    "result": {
        "gotra": {"en": "Atreya", "np": "आत्रेय", "slug": "atreya"},
        "pravaras": [{"sequenceEn": "Atri, Archananasa, Shyabashwo"}],
        "surnames": [{"en": "Aryal", "np": "अर्याल"},
                     {"en": "Bagale", "np": "बगाले"}],
    },
}

NOT_FOUND = {"success": False, "type": "surname",
             "query": {"raw": "Xxx", "normalized": "xxx", "match": None}, "result": None}


def _fake_get(payloads):
    """Return a fake `_get` that pops payloads in order."""
    def _impl(path, **params):
        return payloads.pop(0)
    return _impl


# --- Surname lookup ----------------------------------------------------------

def test_search_surname_returns_typed_result():
    with patch.object(gs, "_get", side_effect=_fake_get([SEARCH_ARYAL, SURNAME_ARYAL_FULL])):
        result = gs.search_surname("Aryal")
    assert result is not None
    assert result.en == "Aryal"
    assert result.np == "अर्याल"
    assert result.gotras[0]["en"] == "Atreya"
    assert "Atri" in result.gotras[0]["pravara"]
    assert result.sahagotri_groups[0]["surnames"][0]["en"] == "Bagale"


def test_search_surname_not_found():
    with patch.object(gs, "_get", side_effect=_fake_get([NOT_FOUND])):
        assert gs.search_surname("DefinitelyNotASurname") is None


# --- Gotra lookup ------------------------------------------------------------

def test_search_gotra_returns_surnames():
    with patch.object(gs, "_get", side_effect=_fake_get([SEARCH_GOTRA_ATREYA, GOTRA_ATREYA_FULL])):
        result = gs.search_gotra("Atreya")
    assert result is not None
    assert result.en == "Atreya"
    assert {s["en"] for s in result.surnames} == {"Aryal", "Bagale"}


# --- Formatters --------------------------------------------------------------

def test_format_my_gotra_with_result():
    with patch.object(gs, "_get", side_effect=_fake_get([SEARCH_ARYAL, SURNAME_ARYAL_FULL])):
        result = gs.search_surname("Aryal")
    text = gs.format_my_gotra("Aryal", result)
    assert "Atreya" in text
    assert "Aryal" in text


def test_format_my_gotra_no_result():
    text = gs.format_my_gotra("Xxx", None)
    assert "No gotra" in text


def test_format_sahagotri():
    with patch.object(gs, "_get", side_effect=_fake_get([SEARCH_GOTRA_ATREYA, GOTRA_ATREYA_FULL])):
        result = gs.search_gotra("Atreya")
    text = gs.format_sahagotri("Atreya", result)
    assert "Aryal" in text and "Bagale" in text


# --- Live network tests (opt-in) ---------------------------------------------

@pytest.mark.network
def test_live_search_surname_aryal():
    result = gs.search_surname("Aryal")
    assert result is not None
    assert result.en.lower() == "aryal"
    assert any(g["en"].lower() == "atreya" for g in result.gotras)


@pytest.mark.network
def test_live_search_gotra_atreya():
    result = gs.search_gotra("Atreya")
    assert result is not None
    assert result.en.lower() == "atreya"
    assert len(result.surnames) > 0
