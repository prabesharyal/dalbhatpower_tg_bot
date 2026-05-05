# DalBhatPower Telegram Bot

Telegram bot for Nepali utilities (calendar, dictionary, gotra, horoscope) and
downloading media from Instagram, YouTube, TikTok, Reddit, X (Twitter), Facebook,
and Terabox.

## Layout

```
bot/
├── app.py            Application setup + handler registration
├── config.py         Loads env vars (single source of truth)
├── db.py             JSON user/chat DB
├── userbot.py        Telethon for >50 MB uploads
├── handlers/         core, admin, calendar, rasifal, gotra, dictionary, nepse, downloads
├── services/         calendar_service, gotra_service, rasifal_service, dict_service
│   └── downloaders/  cobalt, ytdlp, instagram, tiktok, facebook, twitter,
│                     reddit, terabox, generic, insta_story_rapid
└── utils/            media (ffprobe), url_patterns, files, loader
data/                 nepali_dict.json, all_gotra_nep.json, db.json (created at runtime)
tests/                pytest suite
```

## Quick start

```bash
cp .env.example .env   # fill in real values
pip install -r requirements.txt
playwright install chromium    # only if you use the Instagram playwright fallback
python main.py
```

## Tests

```bash
pytest                       # fast tests only
pytest -m network            # also hit live services (gotrafinder.com etc.)
```

## What changed in v2.1

- **Gotra** — replaced the bundled JSON with the live [gotrafinder.com](https://gotrafinder.com/docs/) API.
- **Nepali calendar** — uses [`nepali-calendar-utils`](https://pypi.org/project/nepali-calendar-utils/) instead of the homegrown subprocess/regex stack.
- **NEPSE** — dropped the slow third-party scraper. `/nepse` now replies with links to NEPSE Alpha / Nepal Stock / Merolagani.
- **Reorganisation** — single `bot/` package with handlers / services / utils. Old `mytelegrammodules/`, `downloader/`, `NEPAL/`, `utils/` directories are gone.
- **Env vars** — `NEPSE` removed. `ADMIN_USER_IDS` added (CSV) so `/broadcast` is no longer hardcoded.
- **Shared media-send pipeline** — every download handler now calls one helper (`bot/handlers/media_send.py`), removing ~600 lines of copy-pasted upload code.
- **Tests** — `pytest` suite covers the pure modules (URL detection, calendar, dictionary, db, gotra service, rasifal index lookup).

## Adding a new downloader

1. Drop a module in `bot/services/downloaders/` exposing `download(url) -> (status, caption, [files])`.
2. Wire it in `bot/handlers/downloads.py`.
3. Register the command(s) in `bot/app.py`.
4. Add a test case to `tests/test_downloaders.py` (mark `@pytest.mark.network` if it hits real URLs).
