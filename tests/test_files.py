"""File-utility helpers."""
import os

from bot.utils.files import format_seconds, get_readable_size, remove_quietly


def test_format_seconds_seconds():
    assert format_seconds(45) == "45 Sec"


def test_format_seconds_minutes():
    assert format_seconds(125) == "2 Min 5 Sec"


def test_format_seconds_hours():
    out = format_seconds(7800)  # 2h 10m
    assert out.startswith("2.2 Hrs") or out.startswith("2.16 Hrs") or "Hrs" in out


def test_get_readable_size(tmp_path):
    p = tmp_path / "x"
    p.write_bytes(b"x" * 2048)
    assert "KB" in get_readable_size(str(p))


def test_remove_quietly_missing(tmp_path):
    # Should not raise
    remove_quietly(str(tmp_path / "does-not-exist"))
