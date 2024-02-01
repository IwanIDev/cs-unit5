from datetime import datetime

from PyQt6 import QtWidgets, uic, QtCore
from pathlib import Path
import logging
from user_manager import register_user, User
import asyncio
from database import database


class CreateUserDialog(QtWidgets.QDialog):
    def __init__(self, master):
        super().__init__()
        self.master = master
        path = Path(__file__).parent.resolve()
        path = path.joinpath("qt", "CreateUserDialog.ui")
        file = QtCore.QFile(str(path))
        file.open(QtCore.QIODevice.OpenModeFlag.ReadOnly)
        uic.loadUi(uifile=file, baseinstance=self)
        file.close()

        self.button_box = self.findChild(QtWidgets.QDialogButtonBox, "buttonBox")
        self.save_button = self.button_box.button(QtWidgets.QDialogButtonBox.StandardButton.Save)
        self.save_button.clicked.connect(lambda: self.confirm())

        self.username = self.findChild(QtWidgets.QLineEdit, "usernameInput")
        self.password = self.findChild(QtWidgets.QLineEdit, "passwordInput")

    def confirm(self):
        username = self.username.text()
        password = self.password.text()
        try:
            user = User(username=username, password=password, date_created=datetime.now())
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Error", f"Invalid input {username}, {password}.")
            return
        if user is None:
            QtWidgets.QMessageBox.warning(self, "Error", f"Invalid input {username}, {password}.")
            return
        result, success = register_user(username=username, password=password, database=database)
        if not success:
            QtWidgets.QMessageBox.warning(self, "Error", f"User couldn't be added to database. \
            {result}.")
            logging.critical(msg=f"User couldn't be added to database. {result}")
        message = QtWidgets.QMessageBox()
        message.setIcon(QtWidgets.QMessageBox.Icon.Information)
        message.setWindowTitle("User Created")
        message.setText(f"User {username} has been registered.")
        message.exec()
        self.accept()
