import PyQt6.QtWidgets as QtWidgets
from user_manager import UserType
import logging
from .HomePage import HomePage
from .BooksListPage import BooksListPage
from .UserListPage import UserListPage
from .Settings import Settings
from .DataVis import DataVis


class MainWindow(QtWidgets.QTabWidget):
    def __init__(self, master):
        super().__init__(master)
        self.screens = None
        self._master = master
        self._first_time_viewed = True

    def showEvent(self, a0, QShowEvent=None):
        logging.warning("showEvent on tab widget")
        if not self._first_time_viewed:
            return
        self._first_time_viewed = False
        logging.warning("first time viewed")
        self.set_screens()

    def set_screens(self):
        self.screens = {
            'Home': HomePage(self._master),
            'Books': BooksListPage(self._master),
            'Users': UserListPage(self._master),
            'Statistics': DataVis(self._master)
        }  # TODO: Access control here, don't show screens not accessible by user.
        logging.warning(f"User type {self._master.user.user_type}")
        if self._master.user.user_type == UserType.ADMIN:
            self.screens['Settings'] = Settings(self._master)
        for name, screen in self.screens.items():
            self.addTab(screen, name)

    def change_screen(self):
        pass
