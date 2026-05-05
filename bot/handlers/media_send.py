"""Shared helpers for download handlers.

Every download handler used to duplicate ~80 lines for "send a single file (small
direct, large via userbot) or batch into a media group". This collapses that
into one place so every platform reaps the same fixes.
"""
from __future__ import annotations

import asyncio
import os
from typing import Iterable

from telegram import InputMediaPhoto, InputMediaVideo

from bot.config import get_config
from bot.userbot import Userbot
from bot.utils.files import remove_quietly
from bot.utils.loader import Loader
from bot.utils.media import extract_media_info, is_under_threshold

VIDEO_EXTS = (".mp4", ".webm", ".mkv", ".hevc", ".avc", ".mov")
PHOTO_EXTS = (".jpg", ".jpeg", ".webp", ".heic", ".png")
AUDIO_EXTS = (".mp3", ".wav", ".opus", ".ogg", ".m4a")


def _escape(s: str) -> str:
    return (s or "").replace("<", "&lt;").replace(">", "&gt;")


def make_caption(text: str, source_url: str | None = None) -> str:
    cap = _escape(text or "✨")
    if source_url:
        return f'<a href="{source_url}">{cap}</a>'
    return cap


def _kind(filename: str) -> str:
    low = filename.lower()
    if low.endswith(VIDEO_EXTS):
        return "video"
    if low.endswith(PHOTO_EXTS):
        return "photo"
    if low.endswith(AUDIO_EXTS):
        return "audio"
    return "document"


def _chunk(items: list, n: int) -> Iterable[list]:
    for i in range(0, len(items), n):
        yield items[i:i + n]


async def _forward_from_storage(update, context, resp_id: int, caption: str) -> None:
    cfg = get_config()
    try:
        await update.message.reply_copy(
            from_chat_id=cfg.tg_app_storage_chat_id,
            message_id=resp_id, caption=caption, parse_mode="HTML",
        )
    except Exception:
        await context.bot.copy_message(
            chat_id=update.message.chat_id,
            from_chat_id=cfg.tg_app_storage_chat_id,
            message_id=resp_id, caption=caption, parse_mode="HTML",
        )


async def _send_single(update, context, filename: str, caption: str) -> None:
    cfg = get_config()
    kind = _kind(filename)

    if not is_under_threshold(filename, cfg.file_size_threshold_bytes):
        # >50MB → userbot upload, then forward back into the user's chat.
        if kind == "audio":
            resp = await Userbot.send_audio(filename, update, context, caption)
        elif kind == "video":
            resp = await Userbot.send_video(filename, update, context, caption)
        else:
            resp = await Userbot.send_file(filename, update, context, caption)
        await _forward_from_storage(update, context, resp.id, caption)
        return

    common = dict(
        caption=caption, parse_mode="HTML", disable_notification=True,
        write_timeout=1000, connect_timeout=1000, read_timeout=1000,
    )
    if kind == "video":
        duration, dims, thumb = extract_media_info(filename, "video")
        with Loader("Uploading video", "Video uploaded"):
            await update.message.reply_video(
                video=open(filename, "rb"),
                duration=duration,
                width=dims.get("width", 0), height=dims.get("height", 0),
                thumbnail=open(thumb, "rb") if thumb and os.path.exists(thumb) else None,
                supports_streaming=True, **common,
            )
    elif kind == "photo":
        with Loader("Uploading photo", "Photo uploaded"):
            await update.message.reply_photo(photo=open(filename, "rb"), **common)
    elif kind == "audio":
        duration, _, _ = extract_media_info(filename, "audio")
        with Loader("Uploading audio", "Audio uploaded"):
            await update.message.reply_audio(audio=open(filename, "rb"), duration=duration, **common)
    else:
        with Loader("Uploading file", "File uploaded"):
            await update.message.reply_document(
                document=open(filename, "rb"),
                disable_content_type_detection=True,
                caption=caption, parse_mode="HTML", disable_notification=True,
            )


async def send_files(update, context, caption: str, files: list[str], source_url: str | None = None) -> None:
    """Send any number of files: 0 = caption-only reply, 1 = single send, >1 = media group(s)."""
    cap = make_caption(caption, source_url)

    if not files:
        await update.message.reply_html(cap)
        return

    if len(files) == 1:
        f = files[0]
        try:
            await _send_single(update, context, f, cap)
        finally:
            remove_quietly(f)
        return

    media: list = []
    for filename in files:
        kind = _kind(filename)
        first_in_chunk = (len(media) % 10 == 0)
        if kind == "video":
            media.append(InputMediaVideo(open(filename, "rb"),
                                         caption=cap if first_in_chunk else "",
                                         parse_mode="HTML"))
        elif kind == "photo":
            media.append(InputMediaPhoto(open(filename, "rb"),
                                         caption=cap if first_in_chunk else "",
                                         parse_mode="HTML"))

    with Loader("Uploading media group", "Media group uploaded"):
        for idx, chunk in enumerate(_chunk(media, 10)):
            try:
                await update.message.reply_media_group(
                    media=chunk, write_timeout=1000, connect_timeout=1000, read_timeout=1000,
                )
            except Exception:
                await context.bot.send_media_group(
                    chat_id=update.effective_chat.id, media=chunk,
                    write_timeout=1000, connect_timeout=1000, read_timeout=1000,
                )
            if idx < len(media) // 10:
                await asyncio.sleep(2)
    for f in files:
        remove_quietly(f)
