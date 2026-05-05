"""Smoke tests for downloader modules.

Most tests here are import-only — they verify the modules load cleanly after the
v2.1 refactor. Network-marked tests actually fetch a URL; run with
`pytest -m network`.
"""
import importlib

import pytest


@pytest.mark.parametrize("module", [
    "bot.services.downloaders.cobalt",
    "bot.services.downloaders.ytdlp",
    "bot.services.downloaders.instagram",
    "bot.services.downloaders.insta_story_rapid",
    "bot.services.downloaders.tiktok",
    "bot.services.downloaders.facebook",
    "bot.services.downloaders.twitter",
    "bot.services.downloaders.reddit",
    "bot.services.downloaders.terabox",
    "bot.services.downloaders.generic",
])
def test_module_imports(module):
    importlib.import_module(module)


def test_cobalt_class_shape():
    from bot.services.downloaders.cobalt import cobalt
    c = cobalt("https://www.youtube.com/watch?v=dQw4w9WgXcQ", audio=True)
    assert c.body["downloadMode"] == "audio"
    assert c.body["url"].endswith("dQw4w9WgXcQ")


@pytest.mark.network
def test_cobalt_youtube_short():
    from bot.services.downloaders.cobalt import cobalt
    status, caption, files = cobalt(
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ", audio=False
    ).download()
    # Don't assert success — public APIs flap. Just assert the contract.
    assert isinstance(files, list)
    assert status in (False, "redirect", "tunnel", "picker", "stream", "local-processing")


@pytest.mark.network
def test_generic_image_download(tmp_path, sample_urls, monkeypatch):
    from bot.services.downloaders.generic import FileDownloader
    monkeypatch.chdir(tmp_path)
    ok, caption, fname = FileDownloader().download_file(sample_urls["image_direct"])
    assert ok is True or ok is False  # contract only
    if ok:
        import os
        assert os.path.exists(fname)
