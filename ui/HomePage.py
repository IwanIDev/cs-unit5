from .screen import Screen
from PyQt6 import QtCore, uic
from pathlib import Path
from PyQt6 import QtWidgets
from recommendations import get_suggested_books
from database import database
import asyncio


class HomePage(Screen):
    def __init__(self, master):
        super().__init__(master=master, title="Home Page")
        self.master = master
        path = Path(__file__).parent.resolve()
        path = path.joinpath("qt", "HomePage.ui")
        file = QtCore.QFile(str(path))
        file.open(QtCore.QIODevice.OpenModeFlag.ReadOnly)
        uic.loadUi(uifile=file, baseinstance=self)
        file.close()

        self.listWidget = self.findChild(QtWidgets.QListWidget, "listWidget")
        self.suggested_books = asyncio.run(get_suggested_books(database))
        if not self.suggested_books:
            self.listWidget.addItem(str("No suggestions, try adding some books to your library."))
        for book in self.suggested_books:
            self.listWidget.addItem(str(book))
