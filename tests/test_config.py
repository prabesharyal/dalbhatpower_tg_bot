"""Config loads required env vars and trips on missing ones."""
import pytest

from bot.config import Config


def test_loads_required_vars():
    cfg = Config.from_env()
    assert cfg.bot_token == "test-bot-token"
    assert cfg.tg_app_api_id == 12345
    assert cfg.admin_user_ids == (1, 2, 3)
    assert cfg.file_size_threshold_bytes == 50 * 1024 * 1024


def test_missing_required_raises(monkeypatch):
    monkeypatch.delenv("TG_BOT_TOKEN", raising=False)
    with pytest.raises(RuntimeError, match="TG_BOT_TOKEN"):
        Config.from_env()
