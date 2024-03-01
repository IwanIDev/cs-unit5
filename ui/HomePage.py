from .screen import Screen
from PyQt6 import QtCore, uic
from pathlib import Path
from PyQt6 import QtWidgets
from recommendations import get_suggested_books
from database import database
import asyncio
from .CreateBookDiag import CreateBookDiag


class HomePage(Screen):
    def __init__(self, master):
        super().__init__(master=master, title="Home Page")
        self.master = master
        path = Path(__file__).parent.resolve()
        path = path.joinpath("qt", "HomePage.ui")
        file = QtCore.QFile(str(path))
        file.open(QtCore.QIODevice.OpenModeFlag.ReadOnly)
        uic.loadUi(uifile=file, baseinstance=self)
        file.close()

        self.books_list: QtWidgets.QTableWidget = self.findChild(QtWidgets.QTableWidget, "books")
        self.books_list.setSelectionBehavior(QtWidgets.QTableWidget.SelectionBehavior.SelectRows)
        self.books_list.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.books_list.setColumnCount(4)
        self.suggested_books = asyncio.run(get_suggested_books(database))

        #if not self.suggested_books:
        #    self.books_list.addItem(str("No suggestions, try adding some books to your library."))
        for book in self.suggested_books:
            self.add_book(book)

    def add_book(self, book):
        row_position = self.books_list.rowCount()
        self.books_list.insertRow(row_position)
        self.books_list.setItem(row_position, 0, QtWidgets.QTableWidgetItem(book.title))
        self.books_list.setItem(row_position, 1, QtWidgets.QTableWidgetItem(book.author))
        self.books_list.setItem(row_position, 2, QtWidgets.QTableWidgetItem(book.date_published.strftime("%A %d %B %Y")))
        self.books_list.resizeRowToContents(row_position)
        self.books_list.resizeColumnsToContents()
