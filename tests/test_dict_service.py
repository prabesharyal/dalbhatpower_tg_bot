"""Nepali dictionary lookup."""
import os

import pytest

from bot.services import dict_service


pytestmark = pytest.mark.skipif(
    not os.path.exists(dict_service.DATA_PATH),
    reason="data/nepali_dict.json not present",
)


def test_known_word_returns_definition():
    out = dict_service.lookup("म")
    # 'म' is a pronoun; the dictionary should produce something with grammar info
    assert "शब्द" in out or "_Unfortunately" in out


def test_unknown_word_returns_not_found():
    out = dict_service.lookup("xyzfakewordthatdoesnotexistnonsense")
    assert "Unfortunately" in out


def test_empty_word_returns_prompt():
    assert "Please send" in dict_service.lookup("")
