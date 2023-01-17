from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt

from src.utils.resource_loader import get_resource_path

instance = None


class WMESplashScreen(QtWidgets.QSplashScreen):
    def __init__(self, text):
        super().__init__()

        pixmap = QtGui.QPixmap(get_resource_path("resources/img/splashscreen.png"))
        self.setPixmap(pixmap)

        self.showMessage(text, alignment=Qt.AlignLeft | Qt.AlignBottom, color=Qt.yellow)

        self.show()

        global instance
        instance = self

    def mousePressEvent(self, event) -> None:
        return
