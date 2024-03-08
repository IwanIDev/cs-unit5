import logging
from typing import List, Tuple
from PyQt6 import QtWidgets, uic, QtCore
from pathlib import Path
from book_manager import edit_book, Book, get_author_from_id, get_all_authors, get_author_id
import database as db
import pandas as pd


class EditBooksDialog(QtWidgets.QDialog):
    def __init__(self, master, book: Book, database: db.Database):
        super().__init__(master)
        self.master = master
        self.database = database
        path = Path(__file__).parent.resolve()
        path = path.joinpath("qt", "EditBooksDialog.ui")
        file = QtCore.QFile(str(path))
        file.open(QtCore.QIODevice.OpenModeFlag.ReadOnly)
        uic.loadUi(uifile=file, baseinstance=self)
        file.close()

        self.setFixedSize(400, 300)
        self.button_box = self.findChild(QtWidgets.QDialogButtonBox, "buttonBox")
        self.save_button = self.button_box.button(QtWidgets.QDialogButtonBox.StandardButton.Save)
        self.save_button.clicked.connect(lambda: self.confirm())

        self.book = book

        self.name = self.findChild(QtWidgets.QLineEdit, "nameInput")
        self.name.setText(self.book.title)
        self.author_box = self.findChild(QtWidgets.QComboBox, "authorInput")
        author_name = self.get_author()
        self.author_box.addItem(str(author_name))

        self.all_authors = get_all_authors(self.database)

    def confirm(self):
        name = self.name.text()
        author = self.author_box.currentText()
        author_id = get_author_id(author, self.database)
        book = Book(title=name,
                    author=author_id,
                    date_of_publishing=self.book.date_published,
                    isbn=self.book.isbn,
                    genre=self.book.genre
                    )
        result, success = edit_book(book=book, database=self.database)
        if not success:
            QtWidgets.QMessageBox.critical(self, "Error", f"Something went wrong, error was {result}")
            self.done(QtWidgets.QMessageBox.DialogCode.Rejected)
        message = QtWidgets.QMessageBox()
        message.setIcon(QtWidgets.QMessageBox.Icon.Information)
        message.setWindowTitle("Book Edited")
        message.setText(f"Book {name} edited.")
        message.exec()
        self.accept()

    def get_author(self) -> str:
        author = get_author_from_id(self.book.author, self.database)
        if author is None:
            return "Couldn't get author."
        return str(author)

    def get_list_of_authors(self) -> List[Tuple[str, str]]:
        authors: pd.DataFrame = get_all_authors(self.database)
        list_authors: List = []
        for index, row in authors.iterrows():
            list_authors.append((str(row[0]), str(row[1])))
        return list_authors
