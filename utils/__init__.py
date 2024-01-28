from pathlib import Path
from platformdirs import PlatformDirs
import logging


def get_platform_dir() -> Path:
    dirs = PlatformDirs(appname="LibraryApp", appauthor="IwanI")
    path = Path(dirs.user_data_dir).resolve()
    path.mkdir(parents=True, exist_ok=True)
    logging.info(msg=f"{str(path)}")
    return path
