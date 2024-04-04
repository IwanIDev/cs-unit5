import logging
from typing import List
from utils import get_platform_dir, length_check, get_temp_dir
from .screen import Screen
from PyQt6 import QtCore, uic, QtWidgets, QtGui
from pathlib import Path
from .CreateBookDiag import CreateBookDiag
from .EditBooksDialog import EditBooksDialog
from .SearchBooksDialog import SearchBooksDialog
from .ImageWidget import ImageWidget
import book_manager as bookman
from database import database
import webbrowser


def get_image(isbn) -> QtGui.QImage:
    image_path = get_platform_dir() / f"{isbn}.jpg"  # Kinda hardcoded path, but whatever
    try:
        with open(image_path, 'rb') as image_file:
            content = image_file.read()
        image = QtGui.QImage()
        image.loadFromData(content)
    except FileNotFoundError as e:
        bookman.create_thumbnail_from_book(str(isbn), database)
        try:
            with open(image_path, 'rb') as image_file:
                content = image_file.read()
            image = QtGui.QImage()
            image.loadFromData(content)
        except FileNotFoundError as e:
            logging.warning(msg=f"Could not load image {image_path} as it doesn't exist.")
            image = QtGui.QImage(QtCore.QSize(175, 175), QtGui.QImage.Format.Format_Indexed8)
            image.fill(QtGui.qRgb(255, 255, 255))  # Creates a white image instead.
    return image


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


class BooksLoader(QtCore.QThread):
    count_changed = QtCore.pyqtSignal(int)
    books_created = QtCore.pyqtSignal(list, list)

    def __init__(self, db, master):
        super().__init__()
        self._database = db
        self._master = master

    def get_books(self) -> List[bookman.Book]:
        try:
            result = bookman.get_all_books(self._database)
        except bookman.BookDatabaseException as e:
            return []
        return result

    def run(self) -> None:
        books = self.get_books()
        resulting_books = []
        book_pixmaps = []
        total = len(books)
        for count, book in enumerate(books):
            self.count_changed.emit(int((count/total)*100))
            book_already_exists = False
            for b in self._master.books:
                if b.title == book.title:
                    book_already_exists = True  # This is quite slow, O(n^2).
            if book_already_exists:
                continue
            resulting_books.append(book)
            image = QtGui.QPixmap.fromImage(get_image(book.isbn))
            book_pixmaps.append(image)
        self.books_created.emit(resulting_books, book_pixmaps)


class BooksListPage(Screen):
    COLUMN_COUNT = 8

    def __init__(self, master):
        super().__init__(master=master, title="Books Page")
        self.books = []
        self.book_pixmaps = []
        self.master = master
        self._first_time_viewing = True
        path = Path(__file__).parent.resolve()
        path = path.joinpath("qt", "BooksListPage.ui")
        file = QtCore.QFile(str(path))
        file.open(QtCore.QIODevice.OpenModeFlag.ReadOnly)
        uic.loadUi(uifile=file, baseinstance=self)
        file.close()

        self.window_layout: QtWidgets.QLayout = self.layout()

        self.list_widget: QtWidgets.QTableWidget = self.findChild(QtWidgets.QTableWidget, "tableWidget")
        self.list_widget.setSelectionBehavior(QtWidgets.QTableWidget.SelectionBehavior.SelectRows)
        self.list_widget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.list_widget.setColumnCount(self.COLUMN_COUNT)

        self.list_widget.setHorizontalHeaderLabels([
            "Cover",
            "ISBN",
            "Title",
            "Author",
            "Date Published",
            "Number of Copies",
            "Locations of Copies",
            "Info"
        ])

        self.addBookButton = self.findChild(QtWidgets.QPushButton, "addBookButton")
        self.addBookButton.clicked.connect(lambda: self.create_book())
        self.deleteBookButton = self.findChild(QtWidgets.QPushButton, "deleteButton")
        self.deleteBookButton.clicked.connect(lambda: self.delete_book())
        self.edit_button = self.findChild(QtWidgets.QPushButton, "editButton")
        self.edit_button.clicked.connect(lambda: self.edit_book())
        self.search_button: QtWidgets.QPushButton = self.findChild(QtWidgets.QPushButton, "searchButton")
        self.search_button.clicked.connect(lambda: self.search_books())

        self.progress_bar: QtWidgets.QProgressBar = QtWidgets.QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.window_layout.addWidget(self.progress_bar)

    def showEvent(self, a0):
        if not self._first_time_viewing:
            return
        self._first_time_viewing = False
        self.load_books()

    def load_books(self):
        self.progress_bar.setHidden(False)  # Reveals the loading bar as it might have been hidden earlier.
        self.books = []
        self.loader = BooksLoader(database, self)
        self.loader.finished.connect(lambda: self.finished_loading_books())
        self.loader.count_changed.connect(lambda x: self.count_changed(x))
        self.loader.books_created.connect(lambda x, y: self.books_created(x, y))
        self.loader.start()

    def count_changed(self, value: int):
        self.progress_bar.setValue(value)

    def books_created(self, books: List, pixmaps: List):
        self.books = books
        self.book_pixmaps = pixmaps

    def finished_loading_books(self):
        self.progress_bar.setHidden(True)  # Hides the loading bar as it doesn't need to be shown anymore.
        self.set_books_table()

    def get_books(self) -> List[bookman.Book]:
        result, success = bookman.get_all_books(database)
        if not success:
            QtWidgets.QMessageBox.critical(self, "Error", f"Couldn't retrieve books, read logs for error.")
            return []
        return result

    def set_book(self, item: bookman.Book, count):
        copies = bookman.get_copies_from_book(database, item)
        locations = ""
        for copy in copies:
            locations += str(copy.location.name + "\n")
        image: QtWidgets.QLabel = self.book_pixmaps[count]
        image_widget = QtWidgets.QLabel("")
        image_widget.setPixmap(image)
        image_widget.resize(image.width(), image.height())
        self.list_widget.insertRow(count)
        self.list_widget.setCellWidget(count, 0, image_widget)
        self.list_widget.setItem(count, 1, QtWidgets.QTableWidgetItem(item.isbn))
        self.list_widget.setItem(count, 2, QtWidgets.QTableWidgetItem(item.title))
        self.list_widget.setItem(count, 3, QtWidgets.QTableWidgetItem(item.author.name))
        self.list_widget.setItem(count, 4, QtWidgets.QTableWidgetItem(item.date_published.strftime("%A %d %B %Y")))
        self.list_widget.setItem(count, 5, QtWidgets.QTableWidgetItem(f"{str(len(copies))} copies."))
        self.list_widget.setItem(count, 6, QtWidgets.QTableWidgetItem(locations))

        if item.info_link != "":
            book_url_button: QtWidgets.QPushButton = QtWidgets.QPushButton(self)
            book_url_button.setText("Info")
            url: QtCore.QUrl = QtCore.QUrl(item.info_link)
            book_url_button.clicked.connect(lambda: QtGui.QDesktopServices.openUrl(url))
            self.list_widget.setCellWidget(count, 7, book_url_button)
            self.list_widget.resizeColumnToContents(7)
            book_url_button.adjustSize()
        self.list_widget.resizeColumnToContents(0)
        self.list_widget.resizeRowToContents(count)

    def set_books_table(self):
        self.list_widget.clear()
        self.list_widget.setRowCount(0)
        for count, item in enumerate(self.books):
            self.set_book(item, count)

    def create_book(self):
        diag = CreateBookDiag(self.master)
        diag.setWindowTitle("Create Book")
        diag.exec()
        self.refresh_books()

    def delete_book(self):
        book_id = self.list_widget.currentRow()
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
        book_id = self.list_widget.currentRow()
        book = self.books[book_id]
        dialog = EditBooksDialog(master=self.master, book=book, database=database)
        result = dialog.exec()

        if result != QtWidgets.QDialog.DialogCode.Accepted:
            return
        QtWidgets.QMessageBox.information(self, "Book Edited", "Book has been edited.")
        self.refresh_books()

    def refresh_books(self):
        self.load_books()

    def search_books(self):
        dialog = SearchBooksDialog(master=self.master, database=database)
        result = dialog.exec()
