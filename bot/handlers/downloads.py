"""All download-related command handlers.

Each handler:
1. Cleans the downloads directory
2. Pulls every URL out of the message text
3. Dispatches to the right downloader service
4. Sends the resulting media via :mod:`bot.handlers.media_send`
"""
from __future__ import annotations

import re

from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from bot.handlers.media_send import send_files
from bot.services.downloaders.cobalt import cobalt
from bot.services.downloaders.facebook import Facebook
from bot.services.downloaders.generic import FileDownloader
from bot.services.downloaders.instagram import ig_dlp
from bot.services.downloaders.insta_story_rapid import rapid_ig
from bot.services.downloaders.reddit import Reddit
from bot.services.downloaders.terabox import terabox_dlp
from bot.services.downloaders.tiktok import tt_dlp
from bot.services.downloaders.twitter import Twitter
from bot.services.downloaders.ytdlp import theOPDownloader
from bot.utils import url_patterns
from bot.utils.files import clean_downloads_dir


async def _react_fail(update: Update, message: str = "") -> None:
    if message:
        await update.message.reply_markdown(message, reply_markup=ReplyKeyboardRemove(selective=True))
    try:
        await update.message.set_reaction(reaction="😭")
    except Exception:
        pass


async def _react_ok(update: Update) -> None:
    try:
        await update.message.set_reaction(reaction="❤️‍🔥")
    except Exception:
        pass


# ---------- yt-dlp: full-quality video / audio ----------

async def video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    clean_downloads_dir()
    dl = theOPDownloader()
    for url in url_patterns.find_urls(update.message.text):
        caption, filename, ok = dl.download_video(url)
        if ok:
            await send_files(update, context, caption, [filename], url)
        else:
            await _react_fail(update, "_yt-dlp couldn't download this link._")


async def audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    clean_downloads_dir()
    dl = theOPDownloader()
    for url in url_patterns.find_urls(update.message.text):
        caption, filename, ok = dl.download_audio(url)
        if ok:
            await send_files(update, context, caption, [filename], url)
        else:
            await _react_fail(update, "_yt-dlp couldn't download this audio._")


# ---------- Cobalt: universal fallback ----------

async def cobalt_dl(update: Update, context: ContextTypes.DEFAULT_TYPE, audio: bool = False) -> None:
    clean_downloads_dir()
    text = update.message.text
    parts = text.split(" ", 1)
    target_text = parts[1] if len(parts) > 1 else text
    urls = url_patterns.find_urls(target_text)
    if not urls:
        await _react_fail(update, "_That doesn't look like a link._")
        return
    for url in urls:
        status, caption, files = cobalt(url, audio=audio).download()
        if not status or not files:
            await _react_fail(update, f"_Couldn't download {url} via cobalt._")
            continue
        await send_files(update, context, caption, files, url)
        await _react_ok(update)


# ---------- Instagram: cobalt -> picuki/playwright fallback ----------

async def instagram_dl(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    clean_downloads_dir()
    text = update.message.text
    if url_patterns.INSTAGRAM_STORY.search(text):
        await rapid_instagram_dl(update, context)
        return

    matches = url_patterns.INSTAGRAM_OR_PICUKI.findall(text)
    if not matches:
        await _react_fail(update, "_Send a real Instagram post/reel link._")
        return
    for m in matches:
        url = "https://" + m[0]
        status, caption, files = cobalt(url, audio=False).download()
        if not status:
            try:
                status, caption, files = await ig_dlp(url).download()
            except Exception as e:
                print(f"ig_dlp failed for {url}: {e}")
        if not status:
            await _react_fail(update, f"_Couldn't download {url}._")
            continue
        await send_files(update, context, caption, files, url)


async def rapid_instagram_dl(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """RapidAPI fallback for Instagram stories or links cobalt can't handle."""
    clean_downloads_dir()
    pattern = re.compile(r"(instagram\.com\/(p|reel|reels|stories)\/([\w\-]+)(\/[\d]+)?)")
    matches = pattern.findall(update.message.text)
    if not matches:
        await _react_fail(update, "_Send a real Instagram link._")
        return
    for m in matches:
        url = "https://" + m[0]
        status, caption, files = rapid_ig(url).download()
        if status and files:
            await send_files(update, context, caption, files, url)
        else:
            await _react_fail(update, f"_RapidAPI couldn't fetch {url}._")


# ---------- Multi-social: Facebook / Twitter / Reddit / TikTok ----------

async def multi_social_dl(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    clean_downloads_dir()
    for url in url_patterns.find_urls(update.message.text):
        platform = url_patterns.detect_platform(url)
        try:
            if platform == "reddit":
                check, caption, files = Reddit(url).main()
            elif platform == "facebook":
                check, caption, files = Facebook.downloader(url)
            elif platform == "twitter":
                check, caption, files = Twitter().get_tweet(url)
            elif platform == "tiktok":
                check, caption, files = tt_dlp(url).download()
            else:
                continue
        except Exception as e:
            print(f"{platform} download failed: {e}")
            await _react_fail(update, f"_Couldn't download {url}._")
            continue
        if check and (files or caption):
            await send_files(update, context, caption, files, url)
        else:
            await _react_fail(update)


# ---------- TikTok-only convenience entry point ----------

async def tiktok_dl(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    clean_downloads_dir()
    for url in url_patterns.find_urls(update.message.text):
        if url_patterns.TIKTOK.match(url):
            check, caption, files = tt_dlp(url).download()
            if check and files:
                await send_files(update, context, caption, files, url)
            else:
                await _react_fail(update)


# ---------- Terabox ----------

async def terabox_dl(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    clean_downloads_dir()
    for url in url_patterns.find_urls(update.message.text):
        check, caption, files = terabox_dlp(url)
        if check and files:
            await send_files(update, context, caption, files, url)
        else:
            await _react_fail(update, f"_Terabox download failed for {url}._")


# ---------- Generic file downloader ----------

async def file_dl(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    clean_downloads_dir()
    for url in url_patterns.find_urls(update.message.text):
        check, caption, filename = FileDownloader().download_file(url)
        if check and filename:
            await send_files(update, context, caption, [filename], url)
        else:
            await _react_fail(update, f"_Couldn't download {url}._")
