from .LoginPage import LoginPage
from .HomePage import HomePage
from .BooksListPage import BooksListPage
from .UserListPage import UserListPage
from .MainWindow import MainWindow
import PyQt6.QtWidgets as QtWidgets
from .screen import Screen
import logging
from user_manager import User


class App(QtWidgets.QMainWindow):
    def __init__(self, master):
        super().__init__()
        self.window_title = ""
        self.window_subtitle = ""
        self.change_title("Unit 5")
        self.setFixedSize(800, 600)
        self.user = None

        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)
        self.title = QtWidgets.QLabel(parent=self)
        self.title.setText("")
        self._layout.addWidget(self.title)

        self.loading_box = QtWidgets.QDialog()
        self.loading_box.show()

        self._screens = [
            LoginPage(self),
            MainWindow(self)
        ]
        self.stacked_widget = QtWidgets.QStackedWidget()
        for stacked_screen in self._screens:
            self.stacked_widget.addWidget(stacked_screen)
        self._layout.addWidget(self.stacked_widget)
        self.setCentralWidget(self.stacked_widget)
        self.loading_box.done(0)
        self.change_screen(0)

    def change_screen(self, new_screen: int):
        logging.log(level=logging.INFO, msg=f"Change to screen {new_screen}")
        self.stacked_widget.setCurrentIndex(new_screen)

    def change_title(self, title: str):
        self.window_title = title
        self.reset_title()

    def reset_title(self):
        self.setWindowTitle(f"{self.window_title} - {self.window_subtitle}")

    def change_subtitle(self, subtitle: str):
        self.window_subtitle = subtitle
        self.reset_title()
