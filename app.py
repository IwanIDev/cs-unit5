import sys
from ui import App
import logging
import os
from PyQt6 import QtWidgets
from utils import get_platform_dir


if __name__ == "__main__":
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"), format="%(asctime)s %(levelname)s %(message)s")
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    app.exec()
