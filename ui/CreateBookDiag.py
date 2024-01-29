from PyQt6 import QtWidgets, uic, QtCore
from pathlib import Path
from PyQt6.QtWidgets import QDialogButtonBox
import logging


class CreateBookDiag(QtWidgets.QDialog):
    def __init__(self, master):
        super().__init__()
        self.master = master
        path = Path(__file__).parent.resolve()
        path = path.joinpath("qt", "CreateBooksDiag.ui")
        file = QtCore.QFile(str(path))
        file.open(QtCore.QIODevice.OpenModeFlag.ReadOnly)
        uic.loadUi(uifile=file, baseinstance=self)
        file.close()

        self.button_box = self.findChild(QtWidgets.QDialogButtonBox, "buttonBox")
        self.button_box.button(QtWidgets.QDialogButtonBox.StandardButton.Save).clicked.connect(lambda: self.confirm())

    def confirm(self):
        logging.log(level=logging.INFO, msg="Ok Button Clicked!")
