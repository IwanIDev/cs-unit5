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

        self.layout = self.findChild(QtWidgets.QVBoxLayout, "verticalLayout")
        self.image = QtGui.QPixmap.fromImage(self.get_image())
        self.image_widget = QtWidgets.QLabel("")
        self.image_widget.setPixmap(self.image)
        self.image_widget.resize(self.image.width(), self.image.height())
        self.layout.insertWidget(0, self.image_widget)

        self.title = self.findChild(QtWidgets.QLabel, 'title')
        self.title.setText(self.book.title)

        self.author = self.findChild(QtWidgets.QLabel, 'author')
        self.author.setText(self.book.author)

        self.date_published = self.findChild(QtWidgets.QLabel, 'datePublished')
        self.date_published.setText(self.book.date_published.strftime("%d/%m/%Y"))

    def get_image(self) -> QtGui.QImage:
        image_path = get_platform_dir() / f"{self.book.isbn}.jpg"  # Kinda hardcoded path, but whatever
        try:
            with open(image_path, 'rb') as image_file:
                content = image_file.read()
            image = QtGui.QImage()
            image.loadFromData(content)
        except FileNotFoundError as e:
            logging.warning(msg=f"Could not load image {image_path} as it doesn't exist.")
            image = QtGui.QImage(QtCore.QSize(175, 175), QtGui.QImage.Format.Format_Indexed8)
            image.fill(QtGui.qRgb(255, 255, 255))  # Creates a white image instead.
        except UnidentifiedImageError as e:
            logging.warning(msg=f"Could not load image {image_path} as it isn't an image?")
            image = QtGui.QImage(QtCore.QSize(175, 175), QtGui.QImage.Format.Format_Indexed8)
            image.fill(QtGui.qRgb(255, 255, 255))
        return image
