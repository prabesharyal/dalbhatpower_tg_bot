"""URL detection routes each platform's links to the right downloader."""
import pytest

from bot.utils import url_patterns as up


@pytest.mark.parametrize("url, expected", [
    ("https://www.instagram.com/p/abc123/", "instagram"),
    ("https://instagram.com/reel/abc/", "instagram"),
    ("https://www.tiktok.com/@user/video/12345", "tiktok"),
    ("https://vt.tiktok.com/ABCDE/", "tiktok"),
    ("https://www.youtube.com/shorts/xyz", "youtube_shorts"),
    ("https://reddit.com/r/aww/comments/abc/", "reddit"),
    ("https://www.facebook.com/watch?v=1", "facebook"),
    ("https://twitter.com/user/status/1", "twitter"),
    ("https://x.com/user/status/1", "twitter"),
    ("https://www.terabox.com/foo", "terabox"),
    ("https://www.picuki.com/media/1234", "picuki"),
    ("https://example.com/random", None),
])
def test_detect_platform(url, expected):
    assert up.detect_platform(url) == expected


def test_find_urls_extracts_multiple():
    text = "check https://x.com/foo and www.example.com/bar"
    urls = up.find_urls(text)
    assert any("x.com" in u for u in urls)
    assert any("example.com" in u for u in urls)


def test_find_urls_empty():
    assert up.find_urls("") == []
    assert up.find_urls(None) == []
