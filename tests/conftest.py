"""Test fixtures and per-session setup."""
import os
import sys

import pytest

# Make `bot` importable when running `pytest` from the repo root.
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


@pytest.fixture(autouse=True)
def _fake_env(monkeypatch):
    """Provide minimal env vars so `Config.from_env()` succeeds in tests.

    Tests that need real values should override individual vars themselves.
    """
    monkeypatch.setenv("TG_BOT_TOKEN", "test-bot-token")
    monkeypatch.setenv("TG_APP_API_ID", "12345")
    monkeypatch.setenv("TG_APP_API_HASH", "deadbeef")
    monkeypatch.setenv("TG_APP_SHORT_NAME", "test_session")
    monkeypatch.setenv("TG_APP_CHAT_ID", "-1001234567890")
    monkeypatch.setenv("ADMIN_USER_IDS", "1,2,3")
    # Force Config to re-read from env
    import bot.config as _c
    _c._config = None
    yield
    _c._config = None


# Sample URLs you can use in network-marked tests. Add more as needed.
SAMPLE_URLS = {
    "instagram_post": "https://www.instagram.com/p/DOImrGikw1g/",
    "instagram_reel": "https://www.instagram.com/reel/DOImrGikw1g/",
    "tiktok_video": "https://www.tiktok.com/@charlidamelio/video/7263327663156055342",
    "youtube_short": "https://www.youtube.com/shorts/abc12345",
    "twitter": "https://twitter.com/elonmusk/status/1234567890",
    "reddit": "https://www.reddit.com/r/aww/comments/abc/cute_dog/",
    "facebook": "https://www.facebook.com/watch?v=1234567890",
    "terabox": "https://www.terabox.com/sharing/link?surl=abc",
    "image_direct": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/PNG_transparency_demonstration_1.png/280px-PNG_transparency_demonstration_1.png",
}


@pytest.fixture
def sample_urls():
    return dict(SAMPLE_URLS)
