from .screen import Screen
from PyQt6 import QtCore, uic


class HomePage(Screen):
    def __init__(self, master):
        super().__init__(master=master, title="Home Page")
        self.master = master
        file = QtCore.QFile("ui/qt/HomePage.ui")
        file.open(QtCore.QIODevice.OpenModeFlag.ReadOnly)
        uic.loadUi(uifile=file, baseinstance=self)
        file.close()
