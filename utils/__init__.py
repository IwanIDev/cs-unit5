from pathlib import Path
import sys
from os import getenv


def get_platform_dir() -> Path:
    # get os specific path
    if sys.platform.startswith("win"):
        os_path = getenv("LOCALAPPDATA")
    elif sys.platform.startswith("darwin"):
        os_path = "~/Library/Application Support"
    else:
        # linux
        os_path = getenv("XDG_DATA_HOME", "~/.local/share")

    # join with SwagLyrics dir
    path = Path(os_path) / "LibraryApp"
    path.mkdir(parents=True, exist_ok=True)
    return path.expanduser()
