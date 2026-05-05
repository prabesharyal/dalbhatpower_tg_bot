"""Rasifal index lookup (the pure logic; no network needed)."""
from bot.services.rasifal_service import _index_for, RASHIS


def test_numeric_in_range():
    assert _index_for("1") == 0
    assert _index_for("12") == 11


def test_numeric_out_of_range():
    assert _index_for("0") == -1
    assert _index_for("13") == -1


def test_nepali_name_match():
    assert _index_for("मेष") == 0
    assert _index_for("मीन") == 11


def test_english_name_match():
    assert _index_for("aries") == 0
    assert _index_for("capricorn") == 9
    assert _index_for("pisces") == 11


def test_unknown_returns_negative():
    assert _index_for("definitelynotarashi") == -2
    assert _index_for("") == -2


def test_all_rashis_have_aliases():
    for r in RASHIS:
        assert r["np"] and r["en"] and r["initials"]
