import logging
from pathlib import Path
from .screen import Screen
from PyQt6 import QtCore, QtGui, QtWidgets, QtSvg
from PIL import Image, ImageQt
from data_analysis import top_genres_chart
from database import database
from export_manager import generate_pdf
from io import BytesIO


class DataVis(Screen):
    def __init__(self, master=None):
        super().__init__(master, title="Statistics and Data Visualisation")
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        self.export_button = QtWidgets.QPushButton()
        self.export_button.setParent(self)
        self.export_button.setText("Export")
        self.export_button.clicked.connect(lambda: self.export())
        self.layout.addWidget(self.export_button)
        #  The following is temporary code
        image_pillow: Image = top_genres_chart(database)
        image_qt = ImageQt.ImageQt(image_pillow)
        image_widget = QtWidgets.QLabel("")
        image_pix = QtGui.QPixmap.fromImage(image_qt)
        image_widget.setPixmap(image_pix)
        image_widget.resize(image_pix.size())
        self.layout.addWidget(image_widget)

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
