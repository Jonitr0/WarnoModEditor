from PySide6 import QtWidgets
from PySide6.QtCore import Qt

from src.utils import icon_manager, string_dict
from src.utils.color_manager import *

from src.ndf_parser.napo_entities.napo_collection import *


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
        group_name_selector = StringSelectionCombobox(name_token)
        header_layout.addWidget(group_name_selector)
        header_layout.addStretch(1)
        delete_button = QtWidgets.QPushButton("Delete")
        header_layout.addWidget(delete_button)

        self.platoon_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(self.platoon_layout)

        # TODO: display name, remove button
        # TODO: make collapsible
        # TODO: add platoon

    def add_platoon(self, name_token: str, unit_list: NapoVector):
        self.platoon_layout.addWidget(UnitPlatoonWidget(name_token, unit_list))


# represents one platoon/smart group in Operation Editor
class UnitPlatoonWidget(QtWidgets.QWidget):
    def __init__(self, name_token: str, unit_list: NapoVector, parent=None):
        super().__init__(parent)

        main_layout = QtWidgets.QHBoxLayout()
        self.setLayout(main_layout)

        platoon_name_selector = StringSelectionCombobox(name_token)
        main_layout.addWidget(platoon_name_selector)
        # TODO: name, remove
        # TODO: list units
        # TODO: add/remove units


# Combobox for selecting strings. Displays them as ingame but maps them to tokens
class StringSelectionCombobox(QtWidgets.QComboBox):
    _key_list = []

    def __init__(self, token: str = "", parent=None):
        super().__init__(parent)

        for key in self.key_list():
            self.addItem(string_dict.STRINGS[key], key)

        self.setEditable(True)
        self.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        self.setFocusPolicy(Qt.StrongFocus)

        if not token == "":
            self.set_index_for_token(token)

    def set_index_for_token(self, token: str):
        index = self.findData(token)
        self.setCurrentIndex(index)

    def key_list(self):
        # TODO: fix "Recon platoon" double mapping problem
        if self._key_list:
            return self._key_list

        values = list(string_dict.STRINGS.values())
        values_sorted = sorted(values)
        keys = list(string_dict.STRINGS.keys())

        for val in values_sorted:
            self._key_list.append(keys[values.index(val)])

        return self._key_list

    def wheelEvent(self, e) -> None:
        if self.hasFocus():
            super().wheelEvent(e)
        else:
            e.ignore()
