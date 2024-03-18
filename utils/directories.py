from os import getenv
from pathlib import Path
import sys
import logging
from enum import Enum


class OperatingSystems(Enum):
    WINDOWS = 1
    MACOS = 2
    LINUX = 3


def get_operating_system() -> OperatingSystems:
    if sys.platform.startswith("win"):
        return OperatingSystems.WINDOWS
    elif sys.platform.startswith("darwin"):
        return OperatingSystems.MACOS
    else:
        return OperatingSystems.LINUX


def get_platform_dir() -> Path:
    operating_system = get_operating_system()
    if operating_system == OperatingSystems.WINDOWS:
        os_path = Path(getenv("LOCALAPPDATA")).expanduser()
    elif operating_system == OperatingSystems.MACOS:
        os_path = Path("~/Library/Application Support").expanduser()
    elif operating_system == OperatingSystems.LINUX:
        os_path = Path(getenv("XDG_DATA_HOME", "~/.local/share")).expanduser()
    else:
        os_path = Path(__file__).parent.expanduser()

    # join with LibraryApp dir
    path = Path(os_path).expanduser()
    path = path.resolve()
    path = Path.joinpath(path, "LibraryApp")
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_temp_dir() -> Path:
    operating_system = get_operating_system()
    if operating_system == OperatingSystems.WINDOWS:
        path = Path(getenv("TEMP")).absolute() / "LibraryApp"
    elif operating_system == OperatingSystems.MACOS:
        path = Path("/tmp").absolute() / "LibraryApp"
    else:
        path = Path("/tmp").absolute() / "LibaryApp"
    path = path.expanduser()
    path = path.resolve()
    path.mkdir(parents=True, exist_ok=True)
    return path
