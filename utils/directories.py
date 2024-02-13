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
        os_path = getenv("LOCALAPPDATA")
    elif operating_system == OperatingSystems.MACOS:
        os_path = "~/Library/Application Support"
    else:
        os_path = getenv("XDG_DATA_HOME", "~/.local/share")

    # join with LibraryApp dir
    path = Path(os_path).expanduser()
    path = path.resolve()
    path = Path.joinpath(path, "LibraryApp")
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_temp_dir() -> Path:
    operating_system = get_operating_system()
    if operating_system == OperatingSystems.WINDOWS:
        path = Path(getenv("LOCALAPPDATA")).absolute() / "LibraryApp"
    elif operating_system == OperatingSystems.MACOS:
        path = Path("/tmp").absolute() / "LibraryApp"
    else:
        path = Path("/tmp").absolute() / "LibaryApp"
    path = path.expanduser()
    path = path.resolve()
    path.mkdir(parents=True, exist_ok=True)
    return path
