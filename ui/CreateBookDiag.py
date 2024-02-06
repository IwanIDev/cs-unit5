from PyQt6 import QtWidgets, uic, QtCore
from pathlib import Path
import logging
from book_manager import get_from_isbn, add_book_to_database, IsbnInvalidException, BookDatabaseException
import asyncio
from database import database


class CreateBookDiag(QtWidgets.QDialog):
    def __init__(self, master):
        super().__init__()
        self.master = master
        path = Path(__file__).parent.resolve()
        path = path.joinpath("qt", "CreateBooksDiag.ui")
        file = QtCore.QFile(str(path))
        file.open(QtCore.QIODevice.OpenModeFlag.ReadOnly)
        uic.loadUi(uifile=file, baseinstance=self)
        file.close()

        self.button_box = self.findChild(QtWidgets.QDialogButtonBox, "buttonBox")
        self.save_button = self.button_box.button(QtWidgets.QDialogButtonBox.StandardButton.Save)
        self.save_button.clicked.connect(lambda: self.confirm())

        self.isbn = self.findChild(QtWidgets.QLineEdit, "isbnInput")

    def confirm(self):
        isbn = self.isbn.text()
        isbn = ''.join(ch for ch in isbn if ch.isdigit())
        try:
            success = asyncio.run(get_from_isbn(str(isbn)))
        except ValueError:
            logging.critical(msg=f"Value error in isbn {isbn}")
            QtWidgets.QMessageBox.warning(self, "Error", f"Invalid ISBN {self.isbn.text()}.")
            return
        except IsbnInvalidException as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"{e.__class__.__name__}: {e.message}")
            logging.critical(msg=f"Book couldn't be created, invalid ISBN. {e.__class__.__name__}: {e.message}")
            return

        try:
            result = add_book_to_database(book=book, database=database)
        except BookDatabaseException as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"{e.__class__.__name__}: {e.message}")
            logging.critical(msg=f"Book couldn't be added to database: {e.__class__.__name__}: {e.message}")
            return

        message = QtWidgets.QMessageBox()
        message.setIcon(QtWidgets.QMessageBox.Icon.Information)
        message.setWindowTitle("Book Created")
        message.setText(f"{book.isbn}, {book.title}, {book.author}")
        message.exec()
        self.accept()
