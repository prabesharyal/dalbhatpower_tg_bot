"""Calendar service backed by `nepali-calendar-utils`."""
import datetime as _dt

import pytest

from bot.services import calendar_service as cal


def test_ad_to_bs_basic():
    out = cal.ad_to_bs("2024-04-13")
    # 2024-04-13 corresponds to Baishakh 1, 2081 (rendered in Devanagari)
    assert "२०८१" in out
    assert "बैशाख" in out


def test_bs_to_ad_basic():
    out = cal.bs_to_ad("2081-01-01")
    assert "2024" in out


def test_now_contains_today_year_devanagari():
    out = cal.now()
    # Just sanity-check the english half includes the current AD year
    import datetime as _dt
    assert str(_dt.datetime.now().year) in out


def test_bs_to_ad_invalid():
    assert "Invalid" in cal.bs_to_ad("not a date")


def test_ad_to_bs_invalid():
    assert "Invalid" in cal.ad_to_bs("hello world")


def test_now_contains_today_year():
    out = cal.now()
    assert str(_dt.datetime.now().year) in out


def test_today_contains_year():
    out = cal.today()
    assert str(_dt.datetime.now().year) in out


def test_patro_renders_grid():
    out = cal.patro()
    # Header + weekday row + at least one date row
    assert out.count("\n") >= 4
    assert "आइ" in out  # weekday header in Nepali
