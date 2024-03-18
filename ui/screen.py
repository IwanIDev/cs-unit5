from PyQt6 import QtWidgets


class Screen(QtWidgets.QWidget):
    def __init__(self, master, title):
        super().__init__()
        self._master = master
        self._layout = self.layout()
