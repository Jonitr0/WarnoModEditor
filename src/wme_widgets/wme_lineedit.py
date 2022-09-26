from PySide6 import QtWidgets
from src.utils.color_manager import *


class WMELineEdit(QtWidgets.QLineEdit):
    def __init__(self, parent: QtWidgets.QWidget = None):
        super().__init__(parent)
        self.textChanged.connect(self.on_text_changed)
        self.on_text_changed()

    def on_text_changed(self):
        if self.text() == "":
            self.setStyleSheet("QLineEdit { color: " + get_color_key(COLORS.SECONDARY_LIGHT.value) + "; font: italic; }")
        else:
            self.setStyleSheet("QLineEdit { color: " + get_color_key(COLORS.PRIMARY.value) + "; }")
