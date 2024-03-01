import logging
from typing import List, Tuple
from PyQt6 import QtWidgets, uic, QtCore
from pathlib import Path
from book_manager import edit_book, Book, get_author_from_id, get_all_authors
from user_manager import User, edit_user, UserDatabaseErrorException
import database as db
import pandas as pd


class EditUserDialog(QtWidgets.QDialog):
    def __init__(self, master, user: User, database: db.Database):
        super().__init__(parent=master)
        self.master = master
        self.database = database
        path = Path(__file__).parent.resolve()
        path = path.joinpath("qt", "EditUserDialog.ui")
        file = QtCore.QFile(str(path))
        file.open(QtCore.QIODevice.OpenModeFlag.ReadOnly)
        uic.loadUi(uifile=file, baseinstance=self)
        file.close()

        self.setFixedSize(400, 300)
        self.button_box = self.findChild(QtWidgets.QDialogButtonBox, "buttonBox")
        self.save_button = self.button_box.button(QtWidgets.QDialogButtonBox.StandardButton.Save)
        self.save_button.clicked.connect(lambda: self.confirm())

        self.user = user

        self.name = self.findChild(QtWidgets.QLineEdit, "nameInput")
        self.name.setText(self.user.username)
        self.author_box = self.findChild(QtWidgets.QComboBox, "passwordInput")

    def confirm(self):
        name = self.name.text()
        password = self.password.text()
        user = User(username=name, password=password, date_created=self.user.date_created)
        try:
            result = edit_book(self.database, user)
        except UserDatabaseErrorException as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Something went wrong, error {str(e)}")
            self.done(QtWidgets.QMessageBox.DialogCode.Rejected)
            return
        if not result:
            QtWidgets.QMessageBox.critical(self, "Error", f"Something went wrong, error was {result}")
            self.done(QtWidgets.QMessageBox.DialogCode.Rejected)
            return
        message = QtWidgets.QMessageBox()
        message.setIcon(QtWidgets.QMessageBox.Icon.Information)
        message.setWindowTitle("Book Edited")
        message.setText(f"Book {name} edited.")
        message.exec()
        self.accept()
