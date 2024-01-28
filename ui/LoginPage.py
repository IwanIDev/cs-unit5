import logging
import login_manager
from database import database
from .screen import Screen
from PyQt6 import QtWidgets, QtCore
from PyQt6.uic import loadUi
from pathlib import Path


class LoginPage(Screen):
    def __init__(self, master):
        super().__init__(master=master, title="Login or Register")
        self.master = master
        path = Path(__file__).parent.resolve()
        path = path.joinpath("qt", "LoginPage.ui")
        file = QtCore.QFile(str(path))
        file.open(QtCore.QIODevice.OpenModeFlag.ReadOnly)
        loadUi(uifile=file, baseinstance=self)
        file.close()

        self.login_button = self.findChild(QtWidgets.QPushButton, "loginButton")
        self.login_button.clicked.connect(self.login_user)
        self.register_button = self.findChild(QtWidgets.QPushButton, "registerButton")
        self.register_button.clicked.connect(self.register_user)

        self.username = self.findChild(QtWidgets.QLineEdit, "usernameForm")
        self.password = self.findChild(QtWidgets.QLineEdit, "passwordForm")

    def login_user(self):
        result, success = login_manager.login_user(username=self.username.text(), password=self.password.text(),
                                                   database=database)
        if not success:
            message = QtWidgets.QMessageBox()
            message.setIcon(QtWidgets.QMessageBox.Icon.Information)
            message.setWindowTitle("Error occured.")
            message.setText(f"{result}.\n Please try again.")
            message.exec()
            return
        message = QtWidgets.QMessageBox()
        message.setIcon(QtWidgets.QMessageBox.Icon.Information)
        message.setWindowTitle("User logged in!")
        message.setText("User logged in successfully!")
        message.setDetailedText(f"Username: {self.username.text()}")
        message.exec()
        self.master.change_screen(1)

    def register_user(self):
        result = login_manager.register_user(username=self.username.text(),
                                             password=self.password.text(),
                                             database=database)
        logging.log(level=logging.INFO, msg=f"{result}")
        logging.log(level=logging.INFO, msg=str(isinstance(result, str)))
        if isinstance(result, str):
            message = QtWidgets.QMessageBox()
            message.setWindowTitle("Error occured.")
            message.setText(f"{result}")
            message.exec()
            return
        message = QtWidgets.QMessageBox()
        message.setWindowTitle("User registered")
        message.setText(f"User {self.username.text()} registered successfully.")
        message.setIcon(QtWidgets.QMessageBox.Icon.Information)
        message.setDetailedText("Yeet")
        message.exec()
