import PyQt6.QtWidgets as QtWidgets
from PyQt6 import QtGui
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
        # This is called when the screen is loaded, but might be called on other occasions, but it shouldn't cause bugs.
        logging.warning("showEvent on tab widget")
        self._first_time_viewed = False
        logging.warning("first time viewed")
        self.set_screens()

    def set_screens(self):
        self.clear()
        self.screens = {
            'Home': HomePage(self._master),
            'Books': BooksListPage(self._master),
            'Users': UserListPage(self._master),
            'Statistics': DataVis(self._master)
        }  # These screens are those accessible by all users.
        if self._master.user.user_type == UserType.ADMIN:  # The screens below are those that only admins can access.
            self.screens['Settings'] = Settings(self._master)
        for name, screen in self.screens.items():
            self.addTab(screen, name)  # Adds every screen to the tab widget.
        first_index = self.indexOf(self.screens['Home'])
        self.setCurrentIndex(first_index)  # Sets the home screen to the current tab.
        self.add_logout_button()

    def add_logout_button(self):
        # Creates the logout button and links it to the logout function.
        self.logout_button: QtWidgets.QToolButton = QtWidgets.QToolButton(self)
        self.logout_button.setText("Logout")
        self.logout_button.clicked.connect(lambda: self.logout())

        # Adds a table with no title, sets the tab itself to disabled, and adds the logout button to the bar.
        # This code is a roundabout way of adding a button as a tab with it not actually acting as a tab.
        # That makes it much simpler than having to somehow add a button to each screen.
        logout_label = QtWidgets.QLabel("Logout")
        self.addTab(logout_label, "")
        logout_button_index = self.indexOf(logout_label)
        self.setTabEnabled(logout_button_index, False)
        self.tabBar().setTabButton(logout_button_index, QtWidgets.QTabBar.ButtonPosition.RightSide, self.logout_button)

    def change_screen(self):
        pass

    def logout(self):
        self._master.logout()
