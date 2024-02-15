import sys
from ui import App
import logging
import os
from PyQt6 import QtWidgets
import qdarktheme
from pathlib import Path


def get_stylesheet(stylesheet: Path):
    with open(stylesheet, "r") as f:
        style = f.read()
    return style


if __name__ == "__main__":
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"), format="%(asctime)s %(levelname)s %(message)s")
    app = QtWidgets.QApplication(sys.argv)
    #qdarktheme.setup_theme()
    window = App()
    window.show()
    app.exec()
