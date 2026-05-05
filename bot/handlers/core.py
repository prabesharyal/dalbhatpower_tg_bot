"""/start, /help, /info handlers — registered first so users always have a path in."""
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from bot.db import ChatRegistry

_registry = ChatRegistry()


HELP_TEXT = """ ‎ ‎ ‎ ‎ ‎ ‎ ‎***@DalBhatPowerBot***
‎ ‎ ‎ ‎ ‎ ‎ ‎__(v2.1 — clean rewrite)__

***Core***
`/start` — Check the bot is alive
`/help`  — This menu
`/info`  — Your or this group's info

***Messaging***
`/echo something` — Copies a message
`/pin` / `/unpin` / `/delete` — Manage replied messages

***Auto link handling*** (just paste a link in chat)
TikTok / Facebook / Reddit / Twitter / Instagram / YouTube Shorts / Terabox

***Nepali tools***
`/ad 2072-10-18` — BS → AD
`/bs 2000/10/08` — AD → BS
`/now` / `/today` / `/patro`
`/rashi makar` — Single horoscope (or `/rashi` for all)
`/sahagotri Atreya` — Surnames sharing a gotra
`/mygotra Aryal` — Possible gotras for a surname
`/findgotra Aryal` — Detailed lookup (uses gotrafinder.com)
`@dalbhatpowerbot नमस्ते` — Inline Nepali dictionary

***Downloads***
`/video <link>` / `/audio <link>` — yt-dlp (1080p / mp3, up to 2 GB)
`/cobalt <link>` / `/caudio <link>` — Universal cobalt fallback
`/ig`, `/x`, `/fb`, `/r`, `/tt`, `/yt` — Per-platform shortcuts
`/igstory <link>` — Instagram stories (RapidAPI)
`/terabox <link>` — Terabox files
`/download <link>` — Generic file downloader

***Stocks***
`/nepse` — Stock info links (lightweight; bot does not scrape)
"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    msg = update.message
    print(f"{user.full_name} : {user.id} - /start")
    _registry.upsert(
        chat_id=msg.chat_id,
        fullname=msg.chat.full_name,
        username=msg.chat.username,
        group=msg.chat.title,
    )
    await msg.reply_html(
        f"Dear {user.mention_html()}, the bot is active. Send /help for commands.",
        reply_markup=ReplyKeyboardRemove(selective=True),
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_markdown(HELP_TEXT, reply_markup=ReplyKeyboardRemove(selective=True))


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message
    if msg.chat.type in ("group", "supergroup"):
        text = f"Group Name: {msg.chat.title}\nID: `{msg.chat.id}`"
    elif context.args:
        try:
            user = await context.bot.get_chat(context.args[0])
            text = (
                f"Username: @{user.username}\n" if user.username else ""
            ) + f"First Name: {user.first_name}\nLast Name: {user.last_name}\nID: `{user.id}`"
        except Exception as e:
            text = f"User not found: {e}"
    else:
        u = msg.from_user
        text = (
            (f"Username: @{u.username}\n" if u.username else "")
            + f"First Name: {u.first_name}\nLast Name: {u.last_name}\nID: `{u.id}`"
        )
    await msg.reply_markdown(text, reply_markup=ReplyKeyboardRemove(selective=True))
