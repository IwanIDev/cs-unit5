from .screen import Screen
from PyQt6 import QtCore, uic
from pathlib import Path
from PyQt6 import QtWidgets


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
        
        self.bookButton = self.findChild(QtWidgets.QPushButton, "booksButton")
        self.homeButton = self.findChild(QtWidgets.QPushButton, "homeButton")
        self.usersButton = self.findChild(QtWidgets.QPushButton, "usersButton")
        self.bookButton.clicked.connect(lambda: self.master.change_screen(2))
        self.homeButton.clicked.connect(lambda: self.master.change_screen(1))
        self.usersButton.clicked.connect(lambda: self.master.change_screen(3))

        self.listWidget = self.findChild(QtWidgets.QListWidget, "listWidget")
        self.listWidget.addItem('test')
