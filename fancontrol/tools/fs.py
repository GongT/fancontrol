from pathlib import Path


def try_read_txt(path: Path, defaults="") -> str:
    try:
        return path.read_text().strip()
    except:
        return defaults


def try_read_int(path: Path, defaults=0) -> int:
    try:
        return int(path.read_text().strip(), 10)
    except:
        return defaults
