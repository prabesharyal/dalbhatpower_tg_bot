"""/echo, /pin, /unpin, /delete, /broadcast (admin only)."""
from telegram import Update
from telegram.ext import ContextTypes

from bot.config import get_config
from bot.db import ChatRegistry

_registry = ChatRegistry()


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message
    if msg.reply_to_message:
        await context.bot.copy_message(
            chat_id=update.effective_chat.id,
            from_chat_id=msg.reply_to_message.chat_id,
            message_id=msg.reply_to_message.message_id,
        )
    elif msg.caption:
        text = msg.caption[len("/send"):]
        await context.bot.copy_message(
            chat_id=update.effective_chat.id,
            from_chat_id=update.effective_chat.id,
            message_id=msg.message_id,
            caption=text or " ", disable_notification=True, parse_mode="HTML",
        )
    else:
        text = msg.text[len("/send "):]
        if text:
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text=text,
                disable_web_page_preview=True, disable_notification=True, parse_mode="HTML",
            )
    try:
        await msg.delete()
    except Exception:
        pass


async def pin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message
    if not msg.reply_to_message:
        await msg.reply_text("Reply to a message to pin it.")
        return
    try:
        await context.bot.pin_chat_message(
            msg.chat_id, msg.reply_to_message.message_id, disable_notification=True,
        )
    except Exception:
        await msg.reply_text("I don't have permission to pin messages here.")


async def unpin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message
    if not msg.reply_to_message:
        await msg.reply_text("Reply to a message to unpin it.")
        return
    try:
        await context.bot.unpin_chat_message(msg.chat_id, msg.reply_to_message.message_id)
    except Exception:
        await msg.reply_text("I don't have permission to unpin messages here.")


async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message
    if not msg.reply_to_message:
        await msg.reply_text("Reply to a message to delete it.")
        return
    try:
        await context.bot.delete_message(msg.chat_id, msg.reply_to_message.message_id)
    except Exception:
        await msg.reply_text("Not enough permission to delete.")


async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message
    user_id = msg.from_user.id
    cfg = get_config()
    if user_id not in cfg.admin_user_ids:
        await msg.reply_markdown_v2(
            "You are *__Unauthorized__* to perform this action\\."
            "\n>Only Bot Admins are allowed\\."
        )
        try:
            await msg.set_reaction(reaction="😭")
        except Exception:
            pass
        return

    if not msg.reply_to_message:
        await msg.reply_markdown_v2(
            "For *__Some Security Concerns__* this action requires replying to a message\\."
        )
        return

    src = msg.reply_to_message
    sent = 0
    for chat_id in _registry.all_chat_ids():
        try:
            await context.bot.copy_message(
                chat_id=int(chat_id),
                from_chat_id=src.chat_id,
                message_id=src.message_id,
            )
            sent += 1
        except Exception as e:
            print(f"Broadcast skipped {chat_id}: {e}")
    try:
        await msg.set_reaction(reaction="❤️‍🔥")
    except Exception:
        pass
    await msg.reply_text(f"Broadcast complete: sent to {sent} chats.")
