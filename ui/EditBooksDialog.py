from PyQt6 import QtWidgets, uic, QtCore
from pathlib import Path
import logging
from book_manager import get_from_isbn, add_book_to_database
import asyncio
from database import database


class EditBooksDialog(QtWidgets.QDialog):
    def __init__(self, master):
        super().__init__()
        self.master = master
        path = Path(__file__).parent.resolve()
        path = path.joinpath("qt", "EditBooksDialog.ui")
        file = QtCore.QFile(str(path))
        file.open(QtCore.QIODevice.OpenModeFlag.ReadOnly)
        uic.loadUi(uifile=file, baseinstance=self)
        file.close()

        self.button_box = self.findChild(QtWidgets.QDialogButtonBox, "buttonBox")
        self.save_button = self.button_box.button(QtWidgets.QDialogButtonBox.StandardButton.Save)
        self.save_button.clicked.connect(lambda: self.confirm())

        self.name = self.findChild(QtWidgets.QLineEdit, "nameInput")
        self.author = self.findChild(QtWidgets.QComboBox, "authorInput")

    def confirm(self):
        name = self.name.text()

        message = QtWidgets.QMessageBox()
        message.setIcon(QtWidgets.QMessageBox.Icon.Information)
        message.setWindowTitle("Book Edited")
        message.setText(f"Book {name} edited.")
        message.exec()
        self.accept()
