"""Compiled URL regexes used by handlers to detect platform from message text.

Single source of truth: handlers and the auto-URL message handlers both import
from here so we don't end up with three different "what is a TikTok URL"
patterns drifting apart.
"""
import re

URL_GENERIC = re.compile(r"([^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})")

INSTAGRAM = re.compile(r"(https:\/\/)?((www|m)\.)?((instagram\.)([\w]+))[\S]*")
INSTAGRAM_POST = re.compile(r"(instagram\.com\/(p|reel|reels)\/([\w\-]+))")
INSTAGRAM_STORY = re.compile(
    r"instagram\.com\/(stories)\/([\w\.\_\-]+)\/([\d]+)(\/)?(\?)?.*"
)
INSTAGRAM_OR_PICUKI = re.compile(
    r"((instagram\.com\/(p|reel|reels)\/([\w\-]+))|(www\.picuki\.com\/media\/(\d+)))"
)
PICUKI = re.compile(r"https:\/\/www\.picuki\.com\/media\/(\d+)")

TIKTOK = re.compile(
    r"((https:\/\/)?(((www\.)?tiktok\.com\/@[-a-z\.A-Z0-9_]+\/(video|photo)\/\d+)|(vt\.tiktok\.com\/[-a-zA-Z0-9]+)))"
)
YOUTUBE_SHORTS = re.compile(
    r"(?:https?://)?(?:(?:www|m)\.)?youtube\.com/shorts/[-a-zA-Z0-9]+"
)
REDDIT = re.compile(r"(https\:\/\/)?([w]+\.)?reddit\.com\/[A-Za-z_/0-9]+")
FACEBOOK = re.compile(
    r"(https\:\/\/)?([w]+\.)?(facebook|fb)\.(com|watch)\/[A-Za-z_/0-9]+(.php\?(id|v)=[\d]+)?"
)
TWITTER = re.compile(
    r"https?://(?:(?:www|m(?:obile)?)\.)?(?:(?:twitter|x)\.com|twitter3e4tixl4xyajtrzo62zg5vztmjuricljdp2c5kshju4avyoid\.onion)/"
)
TERABOX = re.compile(
    r"(?:terabox(?:app|link|share)?\.com|terabox\.app|nephobox\.com|4funbox\.com|"
    r"mirrobox\.com|momerybox\.com|gibibox\.com|goaibox\.com|terasharelink\.com|"
    r"freeterabox\.com|1024(?:tera|terabox)\.com)"
)


def detect_platform(url: str) -> str | None:
    """Return one of: instagram, tiktok, reddit, facebook, twitter, terabox, youtube_shorts, picuki, or None."""
    if PICUKI.match(url):
        return "picuki"
    if INSTAGRAM.match(url):
        return "instagram"
    if TIKTOK.match(url):
        return "tiktok"
    if YOUTUBE_SHORTS.match(url):
        return "youtube_shorts"
    if REDDIT.match(url):
        return "reddit"
    if FACEBOOK.match(url):
        return "facebook"
    if TWITTER.match(url):
        return "twitter"
    if TERABOX.search(url):
        return "terabox"
    return None


def find_urls(text: str) -> list[str]:
    return URL_GENERIC.findall(text or "")
