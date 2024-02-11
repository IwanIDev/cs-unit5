import logging
from PyQt6 import QtWidgets, uic, QtCore
from pathlib import Path
from book_manager import edit_book, Book, get_from_isbn
from database import database
import asyncio


class EditBooksDialog(QtWidgets.QDialog):
    def __init__(self, master, book: Book):
        super().__init__()
        self.master = master
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
        self.author = self.findChild(QtWidgets.QComboBox, "authorInput")
        self.author.addItem(self.book.author)

    def confirm(self):
        name = self.name.text()
        author = self.author.currentText()
        book = Book(title=name, author=author, date_of_publishing=self.book.date_published, isbn=self.book.isbn)
        result, success = edit_book(book=book, database=database)
        if not success:
            QtWidgets.QMessageBox.critical(self, "Error", f"Something went wrong, error was {result}")
            self.done(QtWidgets.QMessageBox.DialogCode.Rejected)
        message = QtWidgets.QMessageBox()
        message.setIcon(QtWidgets.QMessageBox.Icon.Information)
        message.setWindowTitle("Book Edited")
        message.setText(f"Book {name} edited.")
        message.exec()
        self.accept()
