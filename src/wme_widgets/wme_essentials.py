from PySide6 import QtWidgets
from PySide6.QtCore import Qt

from src.utils.color_manager import *


class WMELineEdit(QtWidgets.QLineEdit):
    def __init__(self, parent: QtWidgets.QWidget = None):
        super().__init__(parent)
        self.placeholder_color = COLORS.SECONDARY_LIGHT
        if theme_manager.is_light_theme():
            self.placeholder_color = COLORS.SECONDARY_TEXT

        self.textChanged.connect(self.on_text_changed)
        self.on_text_changed()

    def on_text_changed(self):
        if self.text() == "":
            self.setStyleSheet("QLineEdit { color: " + get_color_for_key(self.placeholder_color.value) +
                               "; font: italic; }")
        else:
            self.setStyleSheet("QLineEdit { color: " + get_color_for_key(COLORS.PRIMARY.value) + "; }")


class WMECombobox(QtWidgets.QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditable(True)
        self.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        self.setFocusPolicy(Qt.StrongFocus)

    def wheelEvent(self, e) -> None:
        if self.hasFocus():
            super().wheelEvent(e)
        else:
            e.ignore()
