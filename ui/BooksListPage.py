import logging
from typing import List
from .screen import Screen
from PyQt6 import QtCore, uic, QtWidgets
from pathlib import Path
from .CreateBookDiag import CreateBookDiag
from .EditBooksDialog import EditBooksDialog
from .ImageWidget import ImageWidget
import book_manager as bookman
from database import database


class ConfirmDeleteDialog(QtWidgets.QDialog):
    def __init__(self, book, parent=None):
        super().__init__(parent)
        self.book = book
        self.setWindowTitle("Confirm Delete Action")

        QBtn = QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(lambda: self.accept())
        self.buttonBox.rejected.connect(lambda: self.reject())

        self.layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel(f"Are you sure you want to delete book {self.book.title}?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def accept(self) -> None:
        logging.info(msg=f"Book {self.book} deleted.")
        self.done(QtWidgets.QDialog.DialogCode.Accepted)

    def reject(self) -> None:
        self.done(QtWidgets.QDialog.DialogCode.Rejected)


class BooksListPage(Screen):
    def __init__(self, master):
        super().__init__(master=master, title="Books Page")
        self.books = []
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

        self.listWidget = self.findChild(QtWidgets.QGridLayout, "booksList")
        self.refresh_books()

        self.addBookButton = self.findChild(QtWidgets.QPushButton, "addBookButton")
        self.addBookButton.clicked.connect(lambda: self.create_book())
        self.deleteBookButton = self.findChild(QtWidgets.QPushButton, "deleteButton")
        self.deleteBookButton.clicked.connect(lambda: self.delete_book())
        self.edit_button = self.findChild(QtWidgets.QPushButton, "editButton")
        self.edit_button.clicked.connect(lambda: self.edit_book())

    def get_books(self) -> List[bookman.Book]:
        result, success = bookman.get_all_books(database)
        if not success:
            QtWidgets.QMessageBox.critical(self, "Error", f"Couldn't retrieve books, read logs for error.")
            return []
        return result

    def set_books_table(self):
        for count, item in enumerate(self.books):
            book = ImageWidget(parent=self.master, book=item)
            logging.info(msg=f"{book}")
            self.listWidget.addWidget(book)

    def create_book(self):
        diag = CreateBookDiag(self.master)
        diag.setWindowTitle("Create Book")
        diag.exec()
        self.refresh_books()

    def delete_book(self):
        book_id = self.listWidget.currentRow()
        book = self.books[book_id]
        dialog = ConfirmDeleteDialog(parent=self.master, book=book)
        result = dialog.exec()

        if result != QtWidgets.QDialog.DialogCode.Accepted:
            return
        success = bookman.delete_book(database=database, book=book)
        if not success:
            QtWidgets.QMessageBox.critical(self, "Error", "Book couldn't be deleted, check logs for error.")
            return
        QtWidgets.QMessageBox.information(self, "Book deleted", f"Book {book.title} deleted.")
        self.refresh_books()

    def edit_book(self):
        book_id = self.listWidget.currentRow()
        book = self.books[book_id]
        dialog = EditBooksDialog(master=self.master, book=book)
        result = dialog.exec()

        if result != QtWidgets.QDialog.DialogCode.Accepted:
            return
        QtWidgets.QMessageBox.information(self, "Book Edited", "Book has been edited.")
        self.refresh_books()

    def refresh_books(self):
        self.books = self.get_books()
        self.set_books_table()
