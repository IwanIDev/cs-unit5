import logging
from typing import List, Tuple
from PyQt6 import QtWidgets, uic, QtCore
from pathlib import Path
from user_manager import User, edit_user, UserDatabaseErrorException
import database as db
import werkzeug.security as ws
import pandas as pd
from utils import length_check


class EditUserException(Exception):
    def __init__(self, message=""):
        super().__init__(message)


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
        self.button_box: QtWidgets.QDialogButtonBox = self.findChild(QtWidgets.QDialogButtonBox, "buttonBox")
        self.save_button: QtWidgets.QPushButton = self.button_box.button(QtWidgets.QDialogButtonBox.StandardButton.Save)
        self.save_button.clicked.connect(lambda: self.confirm())

        self.user: User = user

        self.name: QtWidgets.QLineEdit = self.findChild(QtWidgets.QLineEdit, "nameInput")
        self.name.setText(self.user.username)
        self.password_box: QtWidgets.QLineEdit = self.findChild(QtWidgets.QLineEdit, "passwordInput")

    def confirm(self):
        name = self.name.text()
        password = self.password_box.text()
        if not length_check(password, 0, 64):
            msg = QtWidgets.QErrorMessage(self)
            msg.showMessage("Password must be between 2 and 64 characters long.")
            msg.exec()
            self.reject()
            return

        if password == "":
            password = self.user.password
        else:
            password = ws.generate_password_hash(password)
        if not length_check(name, 4, 32):
            msg = QtWidgets.QErrorMessage(self)
            msg.showMessage("Username must be between 4 and 32 characters long.")
            msg.exec()
            self.reject()
            return
        user = User(username=name, password=password, date_created=self.user.date_created)
        try:
            result = edit_user(self.database, user, self.user.username)
        except UserDatabaseErrorException as e:
            msg = QtWidgets.QErrorMessage(self)
            msg.showMessage(f"{e.__class__.__name__}: {str(e)}")
            msg.exec()
            self.reject()
            return
        if not result:
            msg = QtWidgets.QErrorMessage(self)
            msg.showMessage(f"{str(result)}")
            msg.exec()
            self.reject()
            return
        self.accept()
