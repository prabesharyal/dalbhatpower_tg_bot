"""Nepali calendar handlers: /ad, /bs, /now, /today, /patro."""
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from bot.services import calendar_service as cal


def _arg(update: Update) -> str:
    return " ".join(update.message.text.split()[1:])


async def ad(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    arg = _arg(update)
    if not arg:
        await update.message.reply_markdown(
            "Usage: `/ad 2072-10-18`", reply_markup=ReplyKeyboardRemove(selective=True),
        )
        return
    await update.message.reply_markdown(cal.bs_to_ad(arg))


async def bs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    arg = _arg(update)
    if not arg:
        await update.message.reply_markdown(
            "Usage: `/bs 2000/10/08`", reply_markup=ReplyKeyboardRemove(selective=True),
        )
        return
    await update.message.reply_markdown(cal.ad_to_bs(arg))


async def now(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_markdown(cal.now())


async def today(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_markdown(cal.today())


async def patro(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_markdown(cal.patro())
