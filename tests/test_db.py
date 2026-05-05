"""ChatRegistry persists upserts to the on-disk JSON file."""
import json
import os

from bot.db import ChatRegistry


def test_upsert_and_read_back(tmp_path):
    db = ChatRegistry(db_path=str(tmp_path / "db.json"))
    db.upsert(42, "Alice", "alice", None)
    db.upsert(42, "Alice Updated", "alice", "Some Group")
    db.upsert(99, None, None, "Group X")

    data = json.loads(open(db.db_path, "r", encoding="utf-8").read())
    assert data["42"]["fullname"] == "Alice Updated"
    assert data["42"]["group"] == "Some Group"
    assert data["99"]["group"] == "Group X"
    assert sorted(db.all_chat_ids()) == ["42", "99"]


def test_missing_file_yields_empty(tmp_path):
    db = ChatRegistry(db_path=str(tmp_path / "missing.json"))
    assert list(db.all_chat_ids()) == []


def test_corrupt_file_treated_as_empty(tmp_path):
    p = tmp_path / "db.json"
    p.write_text("not json at all")
    db = ChatRegistry(db_path=str(p))
    db.upsert(1, "X", None, None)
    data = json.loads(open(db.db_path, "r", encoding="utf-8").read())
    assert data == {"1": {"fullname": "X", "username": None, "group": None}}
