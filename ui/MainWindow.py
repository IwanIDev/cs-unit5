import PyQt6.QtWidgets as QtWidgets
from .HomePage import HomePage
from .BooksListPage import BooksListPage
from .UserListPage import UserListPage
from .Settings import Settings


class MainWindow(QtWidgets.QTabWidget):
    def __init__(self, master=None):
        super().__init__(master)
        self.screens = {
            'Home': HomePage(self),
            'Books': BooksListPage(self),
            'Users': UserListPage(self),
            'Settings': Settings(self)
        }  # TODO: Access control here, don't show screens not accessible by user.
        for name, screen in self.screens.items():
            self.addTab(screen, name)

    def change_screen(self):
        pass
