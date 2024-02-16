from .screen import Screen
from pathlib import Path
from PyQt6 import uic
import PyQt6.QtCore as QtCore
import PyQt6.QtWidgets as QtWidgets
from backup_manager import export_tables_to_csv
from database import database

class Settings(Screen):
    def __init__(self, master):
        super().__init__(master, "Settings")
        self.master = master
        path = Path(__file__).parent.resolve()
        path = path.joinpath("qt", "Settings.ui")
        file = QtCore.QFile(str(path))
        file.open(QtCore.QIODevice.OpenModeFlag.ReadOnly)
        uic.loadUi(uifile=file, baseinstance=self)
        file.close()

        self.export_button = self.findChild(QtWidgets.QPushButton, "exportButton")
        self.export_button.clicked.connect(lambda: self.csv_export())

    def csv_export(self):
        tables = database.tables.keys()
        export_tables_to_csv(list(tables))
        QtWidgets.QMessageBox.information(self, "Export", "Export successful.")
