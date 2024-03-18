from .LoginPage import LoginPage
from .HomePage import HomePage
from .BooksListPage import BooksListPage
from .UserListPage import UserListPage
from .MainWindow import MainWindow
import PyQt6.QtWidgets as QtWidgets
from .screen import Screen
import logging
from pathlib import Path
from utils import get_platform_dir
from user_manager import User
import json


class App(QtWidgets.QMainWindow):
    def __init__(self, master):
        super().__init__()
        self.window_title = ""
        self.window_subtitle = ""
        self.setFixedSize(800, 600)
        self.user = None

        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)
        self.title = QtWidgets.QLabel(parent=self)
        self.title.setText("")
        self._layout.addWidget(self.title)

        self._settings = {}
        self.update_settings()
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
        self._settings['title'] = title
        path = get_platform_dir() / "settings.json"
        with open(str(path), 'w') as f:
            json.dump(self._settings, f, indent=4)
        self.reset_title()

    def reset_title(self):
        self.window_title = self._settings.get('title')
        self.setWindowTitle(f"{self._settings.get('title')} - {self.window_subtitle}")

    def change_subtitle(self, subtitle: str):
        self.window_subtitle = subtitle
        self.reset_title()

    def update_settings(self):
        path = get_platform_dir() / "settings.json"
        loaded_settings = {}
        try:
            with open(str(path), 'r') as f:
                try:
                    loaded_settings = json.load(f)
                except ValueError as e:
                    logging.warning(f"No settings found, using default.")
                    loaded_settings = {
                        'title': "Unit 5"
                    }
        except FileNotFoundError as e:
            logging.warning(f"No settings found, using default.")
            loaded_settings = {
                'title': "Unit 5"
            }
        logging.warning(f"Loaded settings: {loaded_settings}")
        self._settings.update(loaded_settings)
        self.reset_title()
