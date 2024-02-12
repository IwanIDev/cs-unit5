import logging
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
    path = Path(os_path).resolve()
    path = Path.joinpath(path, "LibraryApp")
    logging.warn(msg=f"{path}")
    path.mkdir(parents=True, exist_ok=True)
    return path.expanduser()


def isbn_check_digit(isbn: int) -> bool:
    digits = [int(x) for x in str(isbn)]
    lastDigit = digits.pop()
    newDigits = []
    for count, digit in enumerate(digits):
        place = count + 1
        if place % 2 == 0:
            newDigits.append(digit * 3)
        else:
            newDigits.append(digit)
    total = 0
    for digit in newDigits:
        total = total + digit
    modulo = total % 10
    checkDigit = modulo if modulo == 0 else 10 - modulo
    return lastDigit == checkDigit


