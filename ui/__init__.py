from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk
from PySide6.QtCore import QFile
import login_manager
from database import database
import PyQt6.QtWidgets as QtWidgets
from PyQt6.uic import loadUi
from PyQt6 import QtCore

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
        self.setWindowTitle("Unit 5")
        self.setFixedSize(800, 600)

        self._screen = None
        change_screen(LoginPage(self))


class LoginPage(QtWidgets.QWidget):
    def __init__(self, master):
        super().__init__()
        file = QtCore.QFile(":/newPrefix/window.ui")
        file.open(QtCore.QFile.ReadOnly)
        loadUi(file, self)
        file.close()

        login_button = self.findChild(QtWidgets.QPushButton, "loginButton")
        login_button.clicked.connect(self.login_user())
        register_button = self.findChild(QtWidgets.QPushButton, "registerButton")
        register_button.clicked.connect(self.register_user())

    def login_user(self):
        result, success = login_manager.login_user(username=self.username.get(), password=self.password.get(),
                                                   database=database)
        if not success:
            messagebox.showerror(title="Database error", message=result)
            return
        messagebox.showinfo(title="Login successful", message=f"Login was successful.")

    def register_user(self):
        result = login_manager.register_user(username=self.username.get(),
                                             password=self.password.get(),
                                             database=database)
        if isinstance(result, str):
            messagebox.showerror(title="Database error", message=result)
            return
        messagebox.showinfo(title="Data entered", message="Data entered into database!")


class StartPage(Screen):
    def __init__(self, master):
        super().__init__(master=master, title="Welcome")

        self.username = tk.StringVar(self)
        self.password = tk.StringVar(self)

        ctk.CTkLabel(self, text="Username").grid(row=0, column=0)
        ctk.CTkEntry(self, textvariable=self.username).grid(row=0, column=1)
        ctk.CTkLabel(self, text="Password").grid(row=1, column=0)
        ctk.CTkEntry(self, textvariable=self.password, show="●").grid(row=1, column=1)

        register_button = QtWidgets.QPushButton(
            parent=self,
            text="Register",
        )
        register_button.clicked.connect(self.register_user())

        login_button = ctk.CTkButton(
            self,
            text="Login",
            command=self.login_user
        ).grid(row=3, column=1, pady=(5, 5))

    def login_user(self):
        result, success = login_manager.login_user(username=self.username.get(), password=self.password.get(),
                                                   database=database)
        if not success:
            messagebox.showerror(title="Database error", message=result)
            return
        messagebox.showinfo(title="Login successful", message=f"Login was successful.")

    def register_user(self):
        result = login_manager.register_user(username=self.username.get(),
                                             password=self.password.get(),
                                             database=database)
        if isinstance(result, str):
            messagebox.showerror(title="Database error", message=result)
            return
        messagebox.showinfo(title="Data entered", message="Data entered into database!")


class PageOne(Screen):
    def __init__(self, master):
        super().__init__(master=master, title="Page One")
        ctk.CTkLabel(self, text="This is page one").grid(row=0, column=0)
        ctk.CTkButton(
            self,
            text="Open start page",
            command=lambda: master.change_screen(StartPage(master)),
        ).grid(row=1, column=0)
