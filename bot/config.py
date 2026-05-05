"""Centralised runtime configuration loaded from environment variables.

All env vars are read once at import time. Missing required vars raise at startup
so problems surface immediately, not deep inside a request handler.
"""
from __future__ import annotations

import os
from dataclasses import dataclass


def _require(name: str) -> str:
    val = os.environ.get(name)
    if not val:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return val


@dataclass(frozen=True)
class Config:
    # Bot (python-telegram-bot)
    bot_token: str

    # Userbot (Telethon, for >50MB uploads)
    tg_app_api_id: int
    tg_app_api_hash: str
    tg_app_session_name: str
    tg_app_storage_chat_id: int

    # Optional integrations
    rasifal_api_url: str | None
    rapidapi_key: str | None
    youtube_api_key: str | None

    # App constants
    admin_user_ids: tuple[int, ...]
    file_size_threshold_bytes: int
    download_dir: str

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            bot_token=_require("TG_BOT_TOKEN"),
            tg_app_api_id=int(_require("TG_APP_API_ID")),
            tg_app_api_hash=_require("TG_APP_API_HASH"),
            tg_app_session_name=_require("TG_APP_SHORT_NAME"),
            tg_app_storage_chat_id=int(_require("TG_APP_CHAT_ID")),
            rasifal_api_url=os.environ.get("RASIFAL"),
            rapidapi_key=os.environ.get("X_RapidAPI_Key"),
            youtube_api_key=os.environ.get("YT_APIV2"),
            admin_user_ids=tuple(
                int(x.strip())
                for x in os.environ.get("ADMIN_USER_IDS", "996638940").split(",")
                if x.strip()
            ),
            file_size_threshold_bytes=50 * 1024 * 1024,
            download_dir=os.path.abspath(
                os.path.join(os.getcwd(), "downloads")
            ),
        )


_config: Config | None = None


def get_config() -> Config:
    global _config
    if _config is None:
        _config = Config.from_env()
    return _config
