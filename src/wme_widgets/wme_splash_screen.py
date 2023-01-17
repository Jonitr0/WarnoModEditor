from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt

from src.utils.resource_loader import get_resource_path
from src.utils.color_manager import *


class WMESplashScreen(QtWidgets.QSplashScreen):
    def __init__(self, text):
        super().__init__()

        pixmap = QtGui.QPixmap(get_resource_path("resources/img/splashscreen.png"))
        self.setPixmap(pixmap)

        self.showMessage(text, alignment=Qt.AlignLeft | Qt.AlignBottom, color=Qt.yellow)

        self.show()

    def mousePressEvent(self, event) -> None:
        return
