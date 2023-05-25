from PySide6 import QtWidgets

from src.utils import icon_manager, string_dict
from src.utils.color_manager import *


# represents one group of smart groups in Operation Editor
class UnitGroupWidget(QtWidgets.QWidget):
    def __init__(self, name_token: str, parent=None):
        super().__init__(parent)

        self.collapse_icon = icon_manager.load_icon("chevron_down.png", COLORS.PRIMARY)
        self.expand_icon = icon_manager.load_icon("chevron_right.png", COLORS.PRIMARY)

        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        header_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(header_layout)

        collapse_button = QtWidgets.QToolButton()
        collapse_button.setFixedSize(32, 32)
        collapse_button.setIcon(self.collapse_icon)
        header_layout.addWidget(collapse_button)
        header_layout.addWidget(QtWidgets.QLabel(string_dict.get_string(name_token)))
        header_layout.addStretch(1)

        # TODO: display name, remove button
        # TODO: make collapsible
        # TODO: add platoon


# represents one platoon/smart group in Operation Editor
class UnitPlatoonWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # TODO: name, remove
        # TODO: list units
        # TODO: add/remove units


# Combobox for selecting strings. Displays them as ingame but maps them to tokens
class StringSelectionCombobox(QtWidgets.QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        # TODO: token/name mapping
