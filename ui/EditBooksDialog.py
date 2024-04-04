import logging
from typing import List, Tuple
from PyQt6 import QtWidgets, uic, QtCore
from pathlib import Path
from book_manager import edit_book, Book, get_author_from_id, get_all_authors, get_author_id
import database as db
import pandas as pd
from utils import length_check


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
        self.author_box: QtWidgets.QComboBox = self.findChild(QtWidgets.QComboBox, "authorInput")
        author_name = self.book.author

        self.all_authors = self.get_list_of_authors()
        logging.warning(f"All authors: {self.all_authors}")
        idx = 0
        for count, author in enumerate(self.all_authors):
            if author[1] == author_name:
                idx = count
            self.author_box.addItem(f"{author[0]}: {author[1]}")
        self.author_box.setCurrentIndex(idx)

    def confirm(self):
        name = self.name.text()
        if not length_check(name, 1, 64):
            msg = QtWidgets.QErrorMessage(self)
            msg.showMessage("Book title must be at least 1 and at most 64 characters.")
            msg.exec()
            self.reject()
            return
        author = self.author_box.currentText()
        author_id = self.all_authors[self.author_box.currentIndex()][0]
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
        author = get_author_id(self.book.author.name, self.database)
        if author is None:
            return "Couldn't get author."
        return str(author.name)

    def get_list_of_authors(self) -> List[Tuple[str, str]]:
        authors: pd.DataFrame = get_all_authors(self.database)
        list_authors: List = []
        for index, row in authors.iterrows():
            list_authors.append((str(row[0]), str(row[1]),))
        return list_authors
