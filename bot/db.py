"""Tiny JSON-backed user/chat registry.

Stores `{chat_id: {fullname, username, group}}` so /broadcast can fan out
messages to everyone who has ever issued /start.
"""
from __future__ import annotations

import json
import os
import threading
from typing import Iterable

DEFAULT_DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "db.json")
_lock = threading.Lock()


class ChatRegistry:
    def __init__(self, db_path: str = DEFAULT_DB_PATH) -> None:
        self.db_path = os.path.abspath(db_path)
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    def _read(self) -> dict:
        try:
            with open(self.db_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _write(self, data: dict) -> None:
        tmp = self.db_path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        os.replace(tmp, self.db_path)

    def upsert(self, chat_id: int | str, fullname: str | None,
               username: str | None, group: str | None) -> None:
        with _lock:
            data = self._read()
            data[str(chat_id)] = {
                "fullname": fullname,
                "username": username,
                "group": group,
            }
            self._write(data)

    def all_chat_ids(self) -> Iterable[str]:
        return list(self._read().keys())
