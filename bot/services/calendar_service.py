"""Nepali calendar service backed by `nepali-calendar-utils`.

Replaces the old subprocess-based patro and homegrown BS<->AD code with the
maintained library. Output format keeps Devanagari digits / Nepali month names
because the user-facing strings have been stable for a long time.
"""
from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass

from dateutil.parser import parse as _parse_date

from nepali_calendar_utils.calendar_model.nepali_date_converter import NepaliDateConverter

# 1-based month index -> Devanagari Nepali month name
NEPALI_MONTHS_NP = [
    "", "बैशाख", "जेठ", "असार", "साउन", "भदौ", "असोज",
    "कार्तिक", "मंसिर", "पुष", "माघ", "फाल्गुन", "चैत्र",
]
NEPALI_MONTHS_EN = [
    "", "Baishakh", "Jestha", "Ashadh", "Shrawan", "Bhadra", "Ashwin",
    "Kartik", "Mangsir", "Poush", "Magh", "Falgun", "Chaitra",
]
WEEKDAYS_NP = ["आइतबार", "सोमबार", "मंगलबार", "बुधबार", "बिहीबार", "शुक्रबार", "शनिबार"]

_DEV_DIGITS = str.maketrans("0123456789", "०१२३४५६७८९")


def _to_devanagari(text: str) -> str:
    return text.translate(_DEV_DIGITS)


@dataclass
class NepaliDate:
    year: int
    month: int
    day: int

    def format_full(self) -> str:
        return _to_devanagari(
            f"{NEPALI_MONTHS_NP[self.month]} {self.day}, {self.year}"
        )


def _converter() -> NepaliDateConverter:
    return NepaliDateConverter()


def ad_to_bs(ad_date_str: str) -> str:
    """Parse a free-form AD date string and return a markdown BS date."""
    try:
        d = _parse_date(ad_date_str, fuzzy=True)
        cal = _converter().convert_english_to_nepali(d.year, d.month, d.day)
    except Exception:
        return "_Invalid date format._"
    np = NepaliDate(cal.year, cal.month, cal.day_of_month)
    return f"***{np.format_full()}***"


def bs_to_ad(bs_date_str: str) -> str:
    """Parse a free-form BS date string (Y-M-D / Y/M/D) and return markdown AD date."""
    try:
        parts = [int(p) for p in bs_date_str.replace("/", "-").split("-") if p]
        if len(parts) != 3:
            raise ValueError
        y, m, d = parts
        cal = _converter().convert_nepali_to_english(y, m, d)
    except Exception:
        return "_Invalid date format._"
    en = _dt.date(cal.year, cal.month, cal.day_of_month)
    return f"***{en.strftime('%B %d, %Y, %A')}***"


def now() -> str:
    """Current Nepali time + date in Devanagari and English."""
    cal = _converter().today_nepali_calendar
    now_t = _dt.datetime.now()
    np_str = _to_devanagari(now_t.strftime("%I:%M:%S %p"))
    np_str = np_str.replace("AM", "बिहान").replace("PM", "बेलुका")
    np_date = NepaliDate(cal.year, cal.month, cal.day_of_month).format_full()
    return (
        f"\t***{np_str}***\n***{np_date}***\n\n"
        f"\t*{now_t.strftime('%I:%M:%S %p')}*\n"
        f"{now_t.strftime('%A, %B %d, %Y')}\n"
        f"\t{NEPALI_MONTHS_EN[cal.month]} {cal.day_of_month}, {cal.year} B.S."
    )


def today() -> str:
    cal = _converter().today_nepali_calendar
    np_date = NepaliDate(cal.year, cal.month, cal.day_of_month).format_full()
    return (
        f"\t***{np_date}***\n"
        f"{NEPALI_MONTHS_EN[cal.month]} {cal.day_of_month}, {cal.year} B.S.\n\n"
        f"\t*{_dt.date.today().strftime('%A, %B %d, %Y')}*"
    )


def patro() -> str:
    """Render the current Nepali month as a calendar grid."""
    conv = _converter()
    cal = conv.today_nepali_calendar
    today_day = cal.day_of_month
    month_cal = conv.get_nepali_month_calendar(cal.year, cal.month)
    total_days = month_cal.total_days_in_month
    first_dow = month_cal.first_day_of_month  # 1=Sun ... 7=Sat

    header_np = f"{NEPALI_MONTHS_NP[cal.month]} {cal.year}"
    header_en = f"{NEPALI_MONTHS_EN[cal.month]} {cal.year} B.S."
    lines = [
        f"***{_to_devanagari(header_np)}***",
        f"_{header_en}_",
        "",
        " ".join(["आइ", "सो", "मं", "बु", "बि", "शु", "श"]),
    ]

    cells: list[str] = ["  "] * (first_dow - 1)
    for d in range(1, total_days + 1):
        marker = "*" if d == today_day else ""
        cells.append(f"{marker}{_to_devanagari(f'{d:>2}')}{marker}")
    while len(cells) % 7:
        cells.append("  ")

    for i in range(0, len(cells), 7):
        lines.append(" ".join(cells[i:i + 7]))
    return "\n".join(lines)
