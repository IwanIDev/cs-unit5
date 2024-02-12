import logging
from typing import List
from .screen import Screen
from PyQt6 import QtCore, uic, QtWidgets
from pathlib import Path
from .CreateUserDialog import CreateUserDialog
import user_manager as userman
from database import database


class ConfirmDeleteDialog(QtWidgets.QDialog):
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.user = user
        self.setWindowTitle("Confirm Delete Action")

        QBtn = QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(lambda: self.accept())
        self.buttonBox.rejected.connect(lambda: self.reject())

        self.layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel(f"Are you sure you want to delete user {self.user.username}?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def accept(self) -> None:
        logging.info(msg=f"User {self.user} deleted.")
        self.done(QtWidgets.QDialog.DialogCode.Accepted)

    def reject(self) -> None:
        self.done(QtWidgets.QDialog.DialogCode.Rejected)


class UserListPage(Screen):
    def __init__(self, master):
        super().__init__(master=master, title="Users Page")
        self.master = master
        path = Path(__file__).parent.resolve()
        path = path.joinpath("qt", "UserListPage.ui")
        file = QtCore.QFile(str(path))
        file.open(QtCore.QIODevice.OpenModeFlag.ReadOnly)
        uic.loadUi(uifile=file, baseinstance=self)
        file.close()
        
        self.bookButton = self.findChild(QtWidgets.QPushButton, "booksButton")
        self.homeButton = self.findChild(QtWidgets.QPushButton, "homeButton")
        self.usersButton = self.findChild(QtWidgets.QPushButton, "usersButton")
        self.bookButton.clicked.connect(lambda: self.master.change_screen(2))
        self.homeButton.clicked.connect(lambda: self.master.change_screen(1))
        self.usersButton.clicked.connect(lambda: self.master.change_screen(3))

        self.listWidget = self.findChild(QtWidgets.QTableWidget, "tableWidget")
        self.listWidget.setSelectionBehavior(QtWidgets.QTableWidget.SelectionBehavior.SelectRows)
        self.listWidget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.users = self.get_users()
        self.listWidget.setRowCount(len(self.users))
        self.set_users_table()

        self.add_user_button = self.findChild(QtWidgets.QPushButton, "addButton")
        self.add_user_button.clicked.connect(lambda: self.create_user())
        self.delete_user_button = self.findChild(QtWidgets.QPushButton, "deleteButton")
        self.delete_user_button.clicked.connect(lambda: self.delete_user())
        self.edit_user_button = self.findChild(QtWidgets.QPushButton, "editButton")
        self.edit_user_button.clicked.connect(lambda: self.edit_user())

    def get_users(self) -> List[userman.User]:
        result, success = userman.get_all_users(database)
        if not success:
            QtWidgets.QMessageBox.critical(self, "Error", f"Couldn't retrieve users, read logs for error.")
            return []
        return result

    def set_users_table(self):
        for count, item in enumerate(self.users):
            self.listWidget.setItem(count, 0, QtWidgets.QTableWidgetItem(item.username))
            self.listWidget.setItem(count, 2, QtWidgets.QTableWidgetItem(item.date_created.strftime("%A %d %B %Y")))

    def create_user(self):
        diag = CreateUserDialog(self.master)
        diag.setWindowTitle("Create User")
        diag.exec()
        self.users = self.get_users()
        self.listWidget.setRowCount(len(self.users))
        self.set_users_table()

    def delete_user(self):
        user_id = self.listWidget.currentRow()
        user = self.users[user_id]
        dialog = ConfirmDeleteDialog(parent=self.master, user=user)
        result = dialog.exec()

        if result != QtWidgets.QDialog.DialogCode.Accepted:
            return
        success = userman.delete_user(database=database, user=user)
        if not success:
            QtWidgets.QMessageBox.critical(self, "Error", "User couldn't be deleted, check logs for error.")
            return
        QtWidgets.QMessageBox.information(self, "User deleted", f"User {user.username} deleted.")
        self.users = self.get_users()
        self.listWidget.setRowCount(len(self.users))
        self.set_users_table()

    def edit_user(self):
        QtWidgets.QMessageBox.information(self, "Work in Progress", f"Editing users not implemented yet, sorry.")
        return

