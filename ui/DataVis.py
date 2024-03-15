import logging
from pathlib import Path
from typing import List

from .screen import Screen
from PyQt6 import QtCore, QtGui, QtWidgets, QtSvg, uic
from PIL import Image, ImageQt
from data_analysis import top_genres_chart, all_books_chart
from database import database
from export_manager import generate_pdf
from io import BytesIO


class DataVis(Screen):
    def __init__(self, master=None):
        super().__init__(master, title="Statistics and Data Visualisation")
        self.master = master
        path = Path(__file__).parent.resolve()
        path = path.joinpath("qt", "DataVis.ui")
        file = QtCore.QFile(str(path))
        file.open(QtCore.QIODevice.OpenModeFlag.ReadOnly)
        uic.loadUi(uifile=file, baseinstance=self)
        file.close()

        self.vertical_layout: QtWidgets.QVBoxLayout = self.findChild(QtWidgets.QVBoxLayout, "verticalLayout")

        self.export_button: QtWidgets.QPushButton = self.findChild(QtWidgets.QPushButton, "exportButton")
        self.export_button.clicked.connect(lambda: self.export())

        self.get_charts()

    def get_charts(self):
        charts: List[Image] = [
            top_genres_chart(database)
        ]
        for chart in charts:
            qt_image = ImageQt.ImageQt(chart)
            image_widget = QtWidgets.QLabel("")
            image_pix = QtGui.QPixmap.fromImage(qt_image)
            image_widget.setPixmap(image_pix)
            image_widget.resize(image_pix.size())
            self.vertical_layout.addWidget(image_widget)

    def export(self):
        default_dir = Path.home().resolve()
        file_str, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save PDF File", str(default_dir), "PDF Files (*.pdf)")
        if file_str == "":
            return
        if not file_str.endswith('.pdf'):
            file_str += '.pdf'
        file = Path(file_str).resolve()
        generate_pdf(file, database)  # No error handling yet.
        QtWidgets.QMessageBox.information(self, "PDF Saved", "PDF Saved Successfully!")
