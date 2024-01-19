import sys
from ui import App, LoginPage
import customtkinter
import logging
import os
from PyQt6 import QtWidgets

if __name__ == "__main__":
    customtkinter.set_default_color_theme("green")
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"), format="%(asctime)s %(levelname)s %(message)s")
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    #window = LoginPage()
    window.show()
    app.exec()
