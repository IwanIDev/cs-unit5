from PyQt6 import QtWidgets, uic, QtCore
from pathlib import Path
import logging
from book_manager import get_from_isbn, add_book_to_database, IsbnInvalidException, BookDatabaseException, Book, add_copy, get_book_id, CopyOfBook, Location, get_locations, add_location
import asyncio
from database import database
from typing import List


class CreateLocationDialog(QtWidgets.QDialog):
    def __init__(self, master, db):
        super().__init__(master)
        self._master = master
        self._database = db
        self._layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(self._layout)

        label = QtWidgets.QLabel("Location Name")
        self._layout.addWidget(label)

        self.name: QtWidgets.QLineEdit = QtWidgets.QLineEdit(self)
        self._accept_button = QtWidgets.QDialogButtonBox.StandardButton.Ok
        self._buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        self._buttons.accepted.connect(lambda: self.save())
        self._buttons.rejected.connect(lambda: self.reject())
        self._layout.addWidget(self._buttons)

    def save(self):
        self.accept()
        return


class CopiesDialog(QtWidgets.QDialog):
    def __init__(self, master, num_copies: int, book: Book, locations: List[Location]):
        super().__init__(master)
        self.setFixedSize(400, 300)
        self._master = master
        self.location_names: List[str] = []
        locations.sort(key=lambda loc: int(loc.id))
        self._all_locations: List[Location] = locations
        self._locations: List[QtWidgets.QComboBox] = []
        self._book = book
        self._num_copies = num_copies
        self._ui_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._ui_layout)
        self.generate_copies_ui()

        self.confirm_button = QtWidgets.QPushButton(self)
        self.confirm_button.setText("Confirm")
        self.confirm_button.clicked.connect(lambda: self.create_copies())

        new_location_button = QtWidgets.QPushButton(self)
        new_location_button.setText("Add New Location")
        new_location_button.clicked.connect(lambda: self.new_location())
        self._ui_layout.addWidget(new_location_button)

    def update_ui(self):
        for item in self._locations:
            item.clear()
            for location in self._all_locations:
                item.addItem(f"{location.id}: {location.name}")

    def generate_copies_ui(self):
        for count in range(self._num_copies):
            widget = QtWidgets.QHBoxLayout(self)
            widget.addWidget(QtWidgets.QLabel(f"Copy number {count + 1} location: "))

            input_form = QtWidgets.QComboBox(self)
            for location in self._all_locations:
                input_form.addItem(f"{location.id}: {location.name}")
            widget.addWidget(input_form)
            self._locations.append(input_form)
            self._ui_layout.addLayout(widget)

    def create_copies(self):
        for location in self._locations:
            location_id = location.currentIndex()
            self.location_names.append(self._all_locations[location_id].name)
        self.accept()

    def new_location(self):
        dialog = CreateLocationDialog(self, database)
        res = dialog.exec()
        location_name = ""
        if res == QtWidgets.QDialog.DialogCode.Accepted:
            location_name = dialog.name.text()
            logging.warning(f"Location name: {location_name}")
        else:
            logging.warning(f"No location created, response code {str(res)}")
            return
        location = add_location(database, location_name)
        self._all_locations.append(location)
        self.update_ui()


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

        self.setFixedSize(400, 300)
        self.button_box = self.findChild(QtWidgets.QDialogButtonBox, "buttonBox")
        self.save_button = self.button_box.button(QtWidgets.QDialogButtonBox.StandardButton.Save)
        self.save_button.clicked.connect(lambda: self.confirm())

        self.isbn = self.findChild(QtWidgets.QLineEdit, "isbnInput")

        self.copies_box: QtWidgets.QSpinBox = self.findChild(QtWidgets.QSpinBox, "copiesBox")
        self.copies_box.setMinimum(1)

    def confirm(self):
        isbn = self.isbn.text()
        isbn = ''.join(ch for ch in isbn if ch.isdigit() or ch == "X")  # Strips all non-digit characters except X.
        num_copies = self.copies_box.value()
        if num_copies <= 0 or num_copies >= 11:  # This shouldn't be possible as the box has a max in the UI.
            logging.warning("User tried to submit wrong number of copies somehow.")
            QtWidgets.QMessageBox.warning(self, "Error", "You must have between 1 and 25 copies.")
            return

        #  Uses the Google Books API to get details about the book.
        #  Value error or IsbnInvalidException can both be thrown depending on what kind of error occurs.
        try:
            book = get_from_isbn(str(isbn), database)
        except ValueError:
            logging.critical(msg=f"Value error in isbn {isbn}")
            QtWidgets.QMessageBox.warning(self, "Error", f"Invalid ISBN {self.isbn.text()}.")
            return
        except IsbnInvalidException as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"{e.__class__.__name__}: {e.message}")
            logging.critical(msg=f"Book couldn't be created, invalid ISBN. {e.__class__.__name__}: {e.message}")
            return

        locations = get_locations(database)

        dialog = CopiesDialog(self, num_copies, book, locations)
        res = dialog.exec()
        locations = []
        if res == QtWidgets.QDialog.DialogCode.Accepted:
            locations = dialog.location_names
        else:
            logging.warning(f"Copies dialog cancelled with code {str(res)}.")
            self.reject()
            return

        try:
            result: Book = add_book_to_database(book=book, database=database)
        except BookDatabaseException as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"{e.__class__.__name__}: {e.message}")
            logging.critical(msg=f"Book couldn't be added to database: {e.__class__.__name__}: {e.message}")
            return

        for n, location in enumerate(locations):
            logging.warning(f"Adding copy {n}.")
            add_copy(database=database, book=result, owner_id=self.master.user.user_id, location_name=location)

        message = QtWidgets.QMessageBox()
        message.setIcon(QtWidgets.QMessageBox.Icon.Information)
        message.setWindowTitle("Book Created")
        message.setText(f"Book {book.title} has been added.")
        message.exec()
        self.accept()
