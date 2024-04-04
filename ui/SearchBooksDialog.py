import logging
from pathlib import Path
from typing import List, Tuple
import pandas as pd
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from book_manager import get_all_authors, get_all_books, search_book, Book, BooksSearchException, get_locations, \
    Location, get_copies_from_book
from datetime import datetime


class SearchResultsDialog(QtWidgets.QDialog):
    def __init__(self, master, table: QtWidgets.QTableWidget):
        super().__init__(master)
        self.setFixedSize(800, 600)
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(table)


class SearchBooksDialog(QtWidgets.QDialog):
    def __init__(self, master, database):
        super().__init__(master)
        self._master = master
        self.database = database
        path = Path(__file__).parent.resolve()
        path = path.joinpath("qt", "SearchBooksDialog.ui")
        file = QtCore.QFile(str(path))
        file.open(QtCore.QIODevice.OpenModeFlag.ReadOnly)
        uic.loadUi(uifile=file, baseinstance=self)
        file.close()

        self.book_name: QtWidgets.QLineEdit = self.findChild(QtWidgets.QLineEdit, "bookName")
        self.all_books = get_all_books(self.database)
        self.book_titles = [str(x.title) for x in self.all_books]
        self.books_model = QtCore.QStringListModel(self)
        self.books_model.setStringList(self.book_titles)
        self.book_completer: QtWidgets.QCompleter = QtWidgets.QCompleter()
        self.book_completer.setModel(self.books_model)
        self.book_completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        self.book_name.setCompleter(self.book_completer)

        self.author_box: QtWidgets.QComboBox = self.findChild(QtWidgets.QComboBox, "author")
        self.authors = self.get_list_of_authors()
        self.authors.insert(0, ('', ''))
        for authorid, name in self.authors:
            self.author_box.addItem(f"{authorid} {name}")

        self.location_box: QtWidgets.QComboBox = self.findChild(QtWidgets.QComboBox, "locations")
        self.locations = get_locations(database)
        self.location_box.addItem("")
        for location in self.locations:
            self.location_box.addItem(f"{location.id} {location.name}")

        self.button_box: QtWidgets.QDialogButtonBox = self.findChild(QtWidgets.QDialogButtonBox, "buttonBox")
        self.save_button = self.button_box.button(QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.save_button.clicked.connect(lambda: self.confirm())

    def confirm(self) -> None:
        name = self.book_name.text()
        author = self.author_box.currentText()
        authorid = self.authors[self.author_box.currentIndex()][0]
        if self.location_box.currentIndex() == 0:
            location = None
        else:
            location = self.locations[self.location_box.currentIndex() - 1]

        try:
            books: List[Book] = search_book(name, authorid, self.database)
        except BooksSearchException as e:
            msg = QtWidgets.QErrorMessage(self)
            msg.showMessage(f"Error while searching, {e.__class__.__name__}: {str(e)}.")
            msg.exec()
            self.reject()
            return
        if not books:  # Books list is empty.
            msg = QtWidgets.QErrorMessage(self)
            msg.showMessage(f"No results.")
            msg.exec()
            self.reject()
            return

        table = QtWidgets.QTableWidget(self)
        table.setColumnCount(6)
        rows = -1
        for count, book in enumerate(books):
            copies = get_copies_from_book(self.database, book)
            copies_to_keep = []
            if location is not None:
                for i, copy in enumerate(copies):
                    if copy.location.id == location.id:
                        copies_to_keep.append(copy)
                if len(copies_to_keep) <= 0:
                    continue
            locations_list = [str(x.location.name) for x in copies]
            locations = ', '.join(locations_list)
            rows += 1

            table.insertRow(int(rows))

            table.setItem(rows, 0, QtWidgets.QTableWidgetItem(str(book.isbn)))
            table.setItem(rows, 1, QtWidgets.QTableWidgetItem(book.title))
            table.setItem(rows, 2, QtWidgets.QTableWidgetItem(book.author.name))
            table.setItem(rows, 3, QtWidgets.QTableWidgetItem(book.date_published.strftime("%A %d %B %Y")))
            table.setItem(rows, 4, QtWidgets.QTableWidgetItem(f"{str(len(copies))} copies."))
            table.setItem(rows, 5, QtWidgets.QTableWidgetItem(locations))

        table.setSelectionBehavior(QtWidgets.QTableWidget.SelectionBehavior.SelectRows)
        table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        table.resizeColumnsToContents()
        table.resizeRowsToContents()
        results = SearchResultsDialog(self, table)
        results.exec()
        self.accept()

    def get_list_of_authors(self) -> List[Tuple[str, str]]:
        authors: pd.DataFrame = get_all_authors(self.database)
        list_authors: List = []
        for index, row in authors.iterrows():
            list_authors.append((str(row[0]), str(row[1]),))
        return list_authors
