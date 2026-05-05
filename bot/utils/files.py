"""File/directory housekeeping helpers shared by download handlers."""
import os
import shutil


def clean_downloads_dir(path: str = "downloads") -> None:
    shutil.rmtree(os.path.join(os.getcwd(), path), ignore_errors=True)


def remove_quietly(file_path: str) -> None:
    try:
        os.remove(file_path)
    except OSError:
        pass


def get_readable_size(file_path: str) -> str:
    size = os.path.getsize(file_path)
    units = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size >= 1024 and i < len(units) - 1:
        size /= 1024
        i += 1
    return f"{size:.2f} {units[i]}"


def format_seconds(seconds: float) -> str:
    if seconds < 60:
        return f"{int(seconds)} Sec"
    if seconds < 3600:
        m, s = divmod(seconds, 60)
        return f"{int(m)} Min {int(s)} Sec"
    h, rem = divmod(seconds, 3600)
    m = rem // 60
    return f"{h:.1f} Hrs {int(m)} Mins"
