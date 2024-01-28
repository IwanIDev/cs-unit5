from .screen import Screen
from PyQt6 import QtCore, uic
from pathlib import Path


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
