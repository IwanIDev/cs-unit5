import login_manager
from database import database
import PyQt6.QtWidgets as QtWidgets
from PyQt6.uic import loadUi
from PyQt6 import QtCore
import logging


class Screen(QtWidgets.QWidget):
    def __init__(self, master, title):
        super().__init__()
        layout = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel("Another Window")
        layout.addWidget(self.label)
        self.setLayout(layout)


def change_screen(new_screen: QtWidgets.QWidget):
    # if self._screen is not None:
    #    self._screen.destroy()
    # self._screen = new_screen.grid(row=1, column=0, padx=(5, 5), pady=(5, 5))
    window = new_screen
    window.show()


class App(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._screens = [
            LoginPage()
        ]
        self.setWindowTitle("Unit 5")
        self.setFixedSize(800, 600)

        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)
        self.stacked_widget = QtWidgets.QStackedWidget()
        for screen in self._screens:
            self.stacked_widget.addWidget(screen)
        self._layout.addWidget(self.stacked_widget)
        self.setCentralWidget(self.stacked_widget)
        self.change_screen(0)

    def change_screen(self, new_screen: int):
        self.stacked_widget.setCurrentIndex(0)


class LoginPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        file = QtCore.QFile("ui/qt/LoginPage.ui")
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
        QtWidgets.QMessageBox.information(self, title="Database", text=f"Data entered successfully!")
        message = QtWidgets.QMessageBox()
        message.setWindowTitle("User registered")
        message.setText(f"User {self.username.text()} registered successfully.")
        message.setIcon(QtWidgets.QMessageBox.Icon.Information)
        message.setDetailedText("Yeet")
        message.exec()
