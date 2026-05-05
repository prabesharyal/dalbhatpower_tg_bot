"""Inline Nepali dictionary handler (`@bot <word>` in any chat)."""
from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from bot.services import dict_service


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.inline_query.query
    if not query:
        return
    definition = dict_service.lookup(query)
    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title=query,
            description=definition[:120],
            input_message_content=InputTextMessageContent(definition, parse_mode=ParseMode.MARKDOWN),
        )
    ]
    await update.inline_query.answer(results)
