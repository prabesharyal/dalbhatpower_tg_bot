"""Telethon-based userbot used to send files >50 MB.

The bot account can only upload up to 50 MB. For bigger files we authenticate
as a user account, send into a private storage chat, and forward the resulting
message back to the requester.
"""
from __future__ import annotations

import time
from telethon import TelegramClient
from telethon.tl.types import DocumentAttributeAudio, DocumentAttributeVideo

from bot.config import get_config
from bot.utils.files import format_seconds, get_readable_size
from bot.utils.loader import Loader
from bot.utils.media import extract_media_info


class Userbot:
    """Wraps Telethon uploads with progress reporting in the original chat."""

    last_edit_time: float = 0.0
    past_size: int = 0

    @classmethod
    def _client(cls) -> TelegramClient:
        cfg = get_config()
        return TelegramClient(cfg.tg_app_session_name, cfg.tg_app_api_id, cfg.tg_app_api_hash)

    @classmethod
    def _chat_id(cls) -> int:
        return get_config().tg_app_storage_chat_id

    @classmethod
    async def send_audio(cls, audio_file_path, update, context, title):
        with Loader("Uploading audio:", "Audio uploaded"):
            async with cls._client() as client:
                duration, _, _ = extract_media_info(audio_file_path, "audio")
                attrs = [DocumentAttributeAudio(voice=False, duration=duration)]
                msg = await update.message.reply_text(
                    f"🚀 Uploading: {title}\nSize: {get_readable_size(audio_file_path)}",
                    parse_mode="HTML", disable_web_page_preview=True,
                )
                return await client.send_file(
                    cls._chat_id(), audio_file_path,
                    attributes=attrs, supports_streaming=True,
                    progress_callback=lambda c, t: cls._progress(c, t, msg, title, audio_file_path, "", "Audio"),
                )

    @classmethod
    async def send_file(cls, file_path, update, context, title):
        with Loader("Uploading file:", "File uploaded"):
            async with cls._client() as client:
                msg = await update.message.reply_text(
                    f"🚀 Uploading...\n\n{title}",
                    parse_mode="MARKDOWN", disable_web_page_preview=True,
                )
                return await client.send_file(
                    cls._chat_id(), file_path, force_document=True,
                    progress_callback=lambda c, t: cls._progress(c, t, msg, title, file_path, title, "File"),
                )

    @classmethod
    async def send_video(cls, video_file_path, update, context, title):
        with Loader("Uploading video:", "Video uploaded"):
            async with cls._client() as client:
                duration, dims, thumb = extract_media_info(video_file_path, "video")
                w, h = dims.get("width", 1080), dims.get("height", 1920)
                attrs = [DocumentAttributeVideo(duration=duration, w=w, h=h, supports_streaming=True)]
                caption = (
                    f"🚀 Uploading Video: {title}\n"
                    f"Size: {get_readable_size(video_file_path)}\n"
                    f"Duration: {format_seconds(duration)}\n"
                    f"Dimensions: {w}x{h}"
                )
                msg = await update.message.reply_text(caption, parse_mode="HTML", disable_web_page_preview=True)
                return await client.send_file(
                    cls._chat_id(), video_file_path,
                    attributes=attrs, supports_streaming=True, thumb=thumb,
                    progress_callback=lambda c, t: cls._progress(c, t, msg, title, video_file_path, caption, "Video"),
                )

    @classmethod
    async def _progress(cls, current, total, message, title, file_path, extra_cap, kind):
        try:
            now = time.time()
            since = now - cls.last_edit_time
            pct = current / total if total else 0
            if pct >= 1.0:
                await message.delete()
                return
            if since < 10:
                return

            speed = max((current - cls.past_size), 0) / (1024 * 1024 * 10)
            cls.past_size = current
            remaining = max(total - current, 0) / (1024 * 1024)
            eta = format_seconds(remaining / speed) if speed > 0 else "?"

            blocks = 15
            done = int(pct * blocks)
            bar = "■" * done + "□" * (blocks - done)
            tail = "\n".join(extra_cap.split("\n")[2:]) if kind == "Video" else ""

            text = (
                f"🚀 Uploading {kind}: {title}\n\n"
                f"Size: {get_readable_size(file_path)}\n"
                f"Progress: {pct:.2%}\n"
                f"Speed: {speed:.2f} MB/s\n"
                f"ETA: {eta}\n"
                f"{tail}\n[{bar}]"
            )
            await message.edit_text(text, parse_mode="HTML", disable_web_page_preview=True)
            cls.last_edit_time = now
        except Exception as e:
            print(f"Userbot progress update failed: {e}")
