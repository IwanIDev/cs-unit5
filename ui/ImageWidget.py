import PyQt6.QtWidgets as QtWidgets
import PyQt6.QtGui as QtGui
import PyQt6.QtCore as QtCore
from PyQt6 import uic
from utils import get_platform_dir
from PIL import ImageQt, Image, UnidentifiedImageError
import logging
from pathlib import Path


class ImageWidget(QtWidgets.QWidget):
    def __init__(self, book, parent=None):
        super().__init__(parent)
        self.book = book
        path = Path(__file__).parent.resolve()
        path = path.joinpath("qt", "ImageWidget.ui")
        file = QtCore.QFile(str(path))
        file.open(QtCore.QIODevice.OpenModeFlag.ReadOnly)
        uic.loadUi(uifile=file, baseinstance=self)
        file.close()

        self.image_frame = self.findChild(QtWidgets.QVBoxLayout, 'imageFrame')
        self.image = self.get_image()
        self.image_frame.addWidget(self.image)
        self.title = self.findChild(QtWidgets.QLabel, 'title')
        self.title.setText(self.book.title)

        self.author = self.findChild(QtWidgets.QLabel, 'author')
        self.author.setText(self.book.author)

        self.date_published = self.findChild(QtWidgets.QLabel, 'datePublished')
        self.date_published.setText(self.book.date_published.strftime("%d/%m/%Y"))

    def get_image(self):
        image_path = get_platform_dir().resolve() / f"{self.book.isbn}.jpg"  # Kinda hardcoded path, but whatever
        try:
            image_pil = Image.open(image_path)
            image = ImageQt.ImageQt(image_pil)
        except FileNotFoundError as e:
            logging.warning(msg=f"Could not load image {image_path} as it doesn't exist.")
            image = QtGui.QImage(QtCore.QSize(175, 175), QtGui.QImage.Format.Format_Indexed8)
            image.fill(QtGui.qRgb(255, 255, 255))  # Creates a white image instead.
        except UnidentifiedImageError as e:
            logging.warning(msg=f"Could not load image {image_path} as it isn't an image?")
            image = QtGui.QImage(QtCore.QSize(175, 175), QtGui.QImage.Format.Format_Indexed8)
            image.fill(QtGui.qRgb(255, 255, 255))
        pixmap = QtGui.QPixmap.fromImage(image)
        label = QtWidgets.QLabel()
        label.setPixmap(pixmap)
        return label
