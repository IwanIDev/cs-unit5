from .LoginPage import LoginPage
from .HomePage import HomePage
from .BooksListPage import BooksListPage
from .UserListPage import UserListPage
from .MainWindow import MainWindow
import PyQt6.QtWidgets as QtWidgets
from .screen import Screen
import logging


class App(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Unit 5")
        self.setFixedSize(800, 600)

        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)
        self.title = QtWidgets.QLabel(parent=self)
        self.title.setText("")
        self._layout.addWidget(self.title)
        self._screens = [
            LoginPage(self),
            MainWindow(self)
        ]
        self.stacked_widget = QtWidgets.QStackedWidget()
        for stacked_screen in self._screens:
            self.stacked_widget.addWidget(stacked_screen)
        self._layout.addWidget(self.stacked_widget)
        self.setCentralWidget(self.stacked_widget)
        self.change_screen(0)

    def change_screen(self, new_screen: int):
        logging.log(level=logging.INFO, msg=f"Change to screen {new_screen}")
        self.stacked_widget.setCurrentIndex(new_screen)
