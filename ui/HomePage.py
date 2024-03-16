from .screen import Screen
from PyQt6 import QtCore, uic
from pathlib import Path
from PyQt6 import QtWidgets
from recommendations import get_suggested_books
from database import database
from book_manager import Book
from typing import List
import asyncio
from .CreateBookDiag import CreateBookDiag


class RecommendationsLoader(QtCore.QThread):
    def __init__(self, db, master):
        super().__init__()
        self._database = db
        self._master = master

    def run(self) -> None:
        suggested_books = get_suggested_books(database)

        for book in suggested_books:
            self._master.add_book(book)


class HomePage(Screen):
    def __init__(self, master):
        super().__init__(master=master, title="Home Page")
        self.suggested_books = []
        self.master = master
        path = Path(__file__).parent.resolve()
        path = path.joinpath("qt", "HomePage.ui")
        file = QtCore.QFile(str(path))
        file.open(QtCore.QIODevice.OpenModeFlag.ReadOnly)
        uic.loadUi(uifile=file, baseinstance=self)
        file.close()

        self.window_layout = self.layout()

        self.books_list: QtWidgets.QTableWidget = self.findChild(QtWidgets.QTableWidget, "books")
        self.books_list.setSelectionBehavior(QtWidgets.QTableWidget.SelectionBehavior.SelectRows)
        self.books_list.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.books_list.setColumnCount(4)

        self.progress_bar: QtWidgets.QProgressBar = QtWidgets.QProgressBar()
        self.progress_bar.setRange(0, 1)
        self.window_layout.addWidget(self.progress_bar)

        self._books: List[Book] = []

    def showEvent(self, event):
        self.load_recommended_books()

    def load_recommended_books(self):
        self.progress_bar.setRange(0, 0)
        self.loader: QtCore.QThread = RecommendationsLoader(database, self)
        self.loader.finished.connect(lambda: self.finished_loading())
        self.loader.start()

    def finished_loading(self):
        self.progress_bar.setRange(0, 1)

    def add_book(self, book: Book):
        for b in self._books:
            if b.title == book.title:
                return  # Avoids adding multiple books, but does add a lot more processing time.
        self._books.append(book)
        row_position = self.books_list.rowCount()
        self.books_list.insertRow(row_position)
        self.books_list.setItem(row_position, 0, QtWidgets.QTableWidgetItem(book.title))
        self.books_list.setItem(row_position, 1, QtWidgets.QTableWidgetItem(book.author))
        self.books_list.setItem(row_position, 2, QtWidgets.QTableWidgetItem(book.date_published.strftime("%A %d %B %Y")))
        self.books_list.resizeRowToContents(row_position)
        self.books_list.resizeColumnsToContents()
