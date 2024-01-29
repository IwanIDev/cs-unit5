from typing import List
from .screen import Screen
from PyQt6 import QtCore, uic
from pathlib import Path
from PyQt6 import QtWidgets
from .CreateBookDiag import CreateBookDiag


def get_books() -> List[tuple]:
    return [("Book One", "Two"), ("Book Two", "Three")]


class BooksListPage(Screen):
    def __init__(self, master):
        super().__init__(master=master, title="Books Page")
        self.master = master
        path = Path(__file__).parent.resolve()
        path = path.joinpath("qt", "BooksListPage.ui")
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
        self.books = get_books()
        self.listWidget.setRowCount(len(self.books))
        self.set_books_table()

        self.addBookButton = self.findChild(QtWidgets.QPushButton, "addBookButton")
        self.addBookButton.clicked.connect(lambda: self.createBook())

    def set_books_table(self):
        for count, item in enumerate(self.books):
            self.listWidget.setItem(count, 0, QtWidgets.QTableWidgetItem(item[0]))
            self.listWidget.setItem(count, 1, QtWidgets.QTableWidgetItem(item[1]))

    def create_book(self):
        diag = CreateBookDiag(self.master)
        diag.setWindowTitle("Create Book")
        diag.setWindowIcon(QtWidgets.QMessageBox.Icon.Information)
        diag.exec()
