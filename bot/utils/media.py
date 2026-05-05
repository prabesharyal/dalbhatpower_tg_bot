"""ffprobe / ffmpeg helpers for extracting media metadata and thumbnails."""
from __future__ import annotations

import json
import os
import random
import string
import subprocess


def generate_random_string(length: int = 10) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def extract_media_info(media_file_path: str, media_type: str):
    """Return (duration_seconds, {width, height}, thumbnail_path).

    `dimensions` is empty for audio. `thumbnail_path` is None for audio.
    """
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "stream=duration,width,height",
        "-of", "json", media_file_path,
    ]
    duration: int = 0
    dimensions: dict = {}
    try:
        out = subprocess.check_output(cmd).decode("utf-8")
        info = json.loads(out)["streams"][0]
        if info.get("duration"):
            duration = int(float(info["duration"]))
        if "width" in info and "height" in info:
            dimensions = {"width": int(info["width"]), "height": int(info["height"])}
    except (subprocess.CalledProcessError, KeyError, IndexError, ValueError):
        pass

    thumbnail_path = None
    if media_type == "video":
        thumbnail_path = extract_video_thumbnail(media_file_path)
    return duration, dimensions, thumbnail_path


def extract_video_thumbnail(video_path: str) -> str:
    out_dir = os.path.join(os.getcwd(), "downloads")
    os.makedirs(out_dir, exist_ok=True)
    thumbnail = os.path.join(out_dir, generate_random_string() + ".jpg")
    subprocess.run(
        ["ffmpeg", "-i", video_path, "-ss", "00:00:01", "-vframes", "1", thumbnail, "-y"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    return thumbnail


def is_under_threshold(file_path: str, threshold_bytes: int) -> bool:
    """True iff the file exists and is smaller than `threshold_bytes`."""
    if not os.path.exists(file_path):
        return False
    return os.path.getsize(file_path) < threshold_bytes
