import sys
from datetime import datetime
from ui import App
import logging
from PyQt6 import QtWidgets
from pathlib import Path


def get_stylesheet(stylesheet: Path):
    with open(stylesheet, "r") as f:
        style = f.read()
    return style


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)8.8s] %(message)s",
        handlers=[logging.StreamHandler()],
    )
    app = QtWidgets.QApplication(sys.argv)
    window = App(app)
    window.show()
    app.exec()
