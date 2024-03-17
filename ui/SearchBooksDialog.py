from pathlib import Path
from typing import List, Tuple
import pandas as pd
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from book_manager import get_all_authors


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

        self.author_box: QtWidgets.QComboBox = self.findChild(QtWidgets.QComboBox, "author")
        self.authors = self.get_list_of_authors()
        for authorid, name in self.authors:
            self.author_box.addItem(f"{authorid}: {name}")

        self.button_box: QtWidgets.QDialogButtonBox = self.findChild(QtWidgets.QDialogButtonBox, "buttonBox")
        self.save_button = self.button_box.button(QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.save_button.clicked.connect(lambda: self.confirm())

    def confirm(self) -> None:
        name = self.book_name.text()
        author = self.author_box.currentText()
        authorid = self.authors[self.author_box.currentIndex()][0]
        #  Search logic here
        self.accept()

    def get_list_of_authors(self) -> List[Tuple[str, str]]:
        authors: pd.DataFrame = get_all_authors(self.database)
        list_authors: List = []
        for index, row in authors.iterrows():
            list_authors.append((str(row[0]), str(row[1]),))
        return list_authors
