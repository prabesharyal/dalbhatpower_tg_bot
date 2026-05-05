"""/gotra, /sahagotri, /findgotra — uses gotrafinder.com API."""
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from bot.services import gotra_service as g


def _arg(update: Update) -> str | None:
    parts = update.message.text.split(maxsplit=1)
    return parts[1].strip() if len(parts) > 1 else None


async def my_gotra(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """`/gotra <surname>` or `/mygotra <surname>` — possible gotras for a surname."""
    arg = _arg(update)
    if not arg:
        await update.message.reply_markdown("Usage: `/mygotra Aryal`")
        return
    try:
        result = g.search_surname(arg)
    except Exception as e:
        print(f"gotrafinder error: {e}")
        await update.message.reply_markdown("_gotrafinder.com lookup failed; try again later._")
        return
    await update.message.reply_markdown(
        g.format_my_gotra(arg, result), reply_markup=ReplyKeyboardRemove(selective=True),
    )


async def sahagotri(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """`/sahagotri <gotra>` — surnames sharing a gotra."""
    arg = _arg(update)
    if not arg:
        await update.message.reply_markdown("Usage: `/sahagotri Atreya`")
        return
    try:
        result = g.search_gotra(arg)
    except Exception as e:
        print(f"gotrafinder error: {e}")
        await update.message.reply_markdown("_gotrafinder.com lookup failed; try again later._")
        return
    await update.message.reply_markdown(
        g.format_sahagotri(arg, result), reply_markup=ReplyKeyboardRemove(selective=True),
    )


async def find_gotra(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """`/findgotra <surname-or-gotra>` — detailed lookup, falls back across both."""
    arg = _arg(update)
    if not arg:
        await update.message.reply_markdown("Usage: `/findgotra Aryal`  or  `/findgotra Atreya`")
        return
    try:
        text = g.format_findgotra(arg)
    except Exception as e:
        print(f"gotrafinder error: {e}")
        text = "_gotrafinder.com lookup failed; try again later._"
    await update.message.reply_markdown(text, reply_markup=ReplyKeyboardRemove(selective=True))
