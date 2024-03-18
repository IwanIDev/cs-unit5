import logging
import user_manager
from database import database
from .screen import Screen
from PyQt6 import QtWidgets, QtCore
from PyQt6.uic import loadUi
from pathlib import Path
from utils import length_check


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

        self.login_button: QtWidgets.QPushButton = self.findChild(QtWidgets.QPushButton, "loginButton")
        self.login_button.clicked.connect(self.login_user)
        self.register_button = self.findChild(QtWidgets.QPushButton, "registerButton")
        self.register_button.clicked.connect(self.register_user)

        self.login_button.setAutoDefault(True)

        self.username = self.findChild(QtWidgets.QLineEdit, "usernameForm")
        self.password = self.findChild(QtWidgets.QLineEdit, "passwordForm")

    def login_user(self):
        try:
            user = user_manager.login_user(username=self.username.text(), password=self.password.text(),
                                    database=database)
        except user_manager.LoginUserException as e:
            message = QtWidgets.QMessageBox()
            message.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            message.setWindowTitle("Error occurred.")
            message.setText(f"{e.__class__.__name__}: {e.message}")
            message.exec()
            return
        message = QtWidgets.QMessageBox()
        message.setIcon(QtWidgets.QMessageBox.Icon.Information)
        message.setWindowTitle("User logged in!")
        message.setText("User logged in successfully!")
        message.exec()
        self.master.user = user
        self.master.change_screen(1)

    def register_user(self):
        username = self.username.text()
        password = self.password.text()

        try:
            user_manager.register_user(username=username,
                                       password=password,
                                       database=database)
        except user_manager.RegisterUserException as e:
            message = QtWidgets.QMessageBox()
            message.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            message.setWindowTitle("Error occurred.")
            message.setText(f"{e.__class__.__name__}: {e.message}")
            message.exec()
            return
        message = QtWidgets.QMessageBox()
        message.setWindowTitle("User registered")
        message.setText(f"User {self.username.text()} registered successfully.")
        message.setIcon(QtWidgets.QMessageBox.Icon.Information)
        message.exec()
