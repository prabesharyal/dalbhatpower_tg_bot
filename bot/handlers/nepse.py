"""/nepse — replies with links to live stock pages.

The previous version hit a slow third-party scraper that often timed out and
broke the snappy feel of the bot. We now just point users at the official sites.
"""
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes

NEPSE_REPLY = (
    "📈 *NEPSE quick-look*\n\n"
    "Live data is heavy to scrape, so here are the canonical sources:\n\n"
    "• [NEPSE Alpha](https://nepsealpha.com)\n"
    "• [Nepal Stock Exchange](https://www.nepalstock.com)\n"
    "• [Merolagani](https://merolagani.com)\n\n"
    "For a single scrip, search the symbol on NEPSE Alpha or Merolagani — much faster than this bot."
)


async def nepse(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_markdown(
        NEPSE_REPLY,
        reply_markup=ReplyKeyboardRemove(selective=True),
        disable_web_page_preview=True,
    )
