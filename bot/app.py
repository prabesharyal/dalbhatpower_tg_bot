"""Build the python-telegram-bot Application and register every handler."""
from __future__ import annotations

from functools import partial

from telegram.ext import (
    Application,
    CommandHandler,
    InlineQueryHandler,
    MessageHandler,
    filters,
)

from bot.config import get_config
from bot.handlers import admin, calendar, core, dictionary, downloads, gotra, nepse, rasifal


def build_application() -> Application:
    cfg = get_config()
    app = (
        Application.builder()
        .token(cfg.bot_token)
        .read_timeout(500)
        .write_timeout(1000)
        .get_updates_read_timeout(200)
        .connect_timeout(1000)
        .build()
    )

    # --- Core ---
    app.add_handler(CommandHandler("start", core.start))
    app.add_handler(CommandHandler("help", core.help_cmd))
    app.add_handler(CommandHandler("info", core.info))

    # --- Admin / messaging ---
    for cmd in ("send", "echo"):
        app.add_handler(CommandHandler(cmd, admin.echo))
    app.add_handler(CommandHandler("pin", admin.pin))
    app.add_handler(CommandHandler("unpin", admin.unpin))
    app.add_handler(CommandHandler("delete", admin.delete))
    for cmd in ("update", "broadcast", "sendall"):
        app.add_handler(CommandHandler(cmd, admin.broadcast))

    # --- Calendar ---
    for cmd in ("ad", "toad"):
        app.add_handler(CommandHandler(cmd, calendar.ad))
    for cmd in ("bs", "tobs"):
        app.add_handler(CommandHandler(cmd, calendar.bs))
    for cmd in ("now", "time"):
        app.add_handler(CommandHandler(cmd, calendar.now))
    for cmd in ("today", "date"):
        app.add_handler(CommandHandler(cmd, calendar.today))
    for cmd in ("patro", "calendar", "calender", "month"):
        app.add_handler(CommandHandler(cmd, calendar.patro))

    # --- Rasifal ---
    for cmd in ("rasifal", "rashi", "rasi", "rasiphal", "horoscope", "zodiac"):
        app.add_handler(CommandHandler(cmd, rasifal.rasifal))

    # --- Gotra ---
    for cmd in ("mygotra", "gotra"):
        app.add_handler(CommandHandler(cmd, gotra.my_gotra))
    app.add_handler(CommandHandler("sahagotri", gotra.sahagotri))
    app.add_handler(CommandHandler("findgotra", gotra.find_gotra))

    # --- NEPSE (links only) ---
    for cmd in ("nepse", "stock", "scrip"):
        app.add_handler(CommandHandler(cmd, nepse.nepse))

    # --- Downloaders ---
    app.add_handler(CommandHandler("video", downloads.video, block=True))
    app.add_handler(CommandHandler("audio", downloads.audio, block=True))

    for cmd in ("ig", "instagram"):
        app.add_handler(CommandHandler(cmd, downloads.instagram_dl, block=False))
    for cmd in ("igstory", "ig2", "igbackup", "rapidapi", "rapidig"):
        app.add_handler(CommandHandler(cmd, downloads.rapid_instagram_dl, block=False))

    for cmd in ("terabox", "tera"):
        app.add_handler(CommandHandler(cmd, downloads.terabox_dl, block=False))

    for cmd in ("facebook", "snapsave", "x", "twitter", "tweet", "fb", "reddit", "r"):
        app.add_handler(CommandHandler(cmd, downloads.multi_social_dl, block=False))
    app.add_handler(CommandHandler("tiktok", downloads.tiktok_dl, block=False))

    for cmd in ("tt", "yt", "ytv", "cobalt", "cvideo"):
        app.add_handler(CommandHandler(cmd, downloads.cobalt_dl, block=False))
    for cmd in ("ytm", "yta", "caudio", "ytaudio"):
        app.add_handler(CommandHandler(cmd, partial(downloads.cobalt_dl, audio=True), block=False))

    for cmd in ("download", "dwnld", "dwld", "file", "fdm", "dl", "direct_dl"):
        app.add_handler(CommandHandler(cmd, downloads.file_dl, block=False))

    # --- Inline dictionary ---
    app.add_handler(InlineQueryHandler(dictionary.inline_query))

    # --- Auto URL handlers (most specific first) ---
    app.add_handler(MessageHandler(
        filters.Regex(r"(?:https?://)?(?:(?:www|m)\.)?youtube\.com/shorts/[-a-zA-Z0-9]+") & ~filters.COMMAND,
        downloads.cobalt_dl, block=False,
    ))
    app.add_handler(MessageHandler(
        filters.Regex(r"(https:\/\/)?((www|m)\.)?(instagram\.)([\w]+)[\S]*") & ~filters.COMMAND,
        downloads.cobalt_dl, block=True,
    ))
    app.add_handler(MessageHandler(
        filters.Regex(r"((https:\/\/)?(((www\.)?tiktok\.com\/@[-a-z\.A-Z0-9_]+\/(video|photo)\/\d+)|(vt\.tiktok\.com\/[-a-zA-Z0-9]+)))") & ~filters.COMMAND,
        downloads.multi_social_dl, block=True,
    ))
    app.add_handler(MessageHandler(
        filters.Regex(r"(?:terabox(?:app|link|share)?\.com|terabox\.app|nephobox\.com|4funbox\.com|mirrobox\.com|momerybox\.com|gibibox\.com|goaibox\.com|terasharelink\.com|freeterabox\.com|1024(?:tera|terabox)\.com)") & ~filters.COMMAND,
        downloads.terabox_dl, block=True,
    ))
    app.add_handler(MessageHandler(
        filters.Regex(r"(https\:\/\/)?([w]+\.)?reddit\.com\/[A-Za-z_/0-9]+") & ~filters.COMMAND,
        downloads.multi_social_dl, block=True,
    ))
    app.add_handler(MessageHandler(
        filters.Regex(r"(https\:\/\/)?([w]+\.)?(facebook|fb)\.(com|watch)\/[A-Za-z_/0-9]+") & ~filters.COMMAND,
        downloads.multi_social_dl, block=True,
    ))
    app.add_handler(MessageHandler(
        filters.Regex(r"https?://(?:(?:www|m(?:obile)?)\.)?(?:twitter|x)\.com/") & ~filters.COMMAND,
        downloads.multi_social_dl, block=True,
    ))
    app.add_handler(MessageHandler(
        filters.Regex(r"https:\/\/www\.picuki\.com\/media\/(\d+)") & ~filters.COMMAND,
        downloads.instagram_dl, block=True,
    ))

    return app


def run() -> None:
    app = build_application()
    print("Application is running!")
    app.run_polling()
