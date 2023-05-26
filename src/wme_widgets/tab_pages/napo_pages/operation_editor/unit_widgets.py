from PySide6 import QtWidgets

from src.utils import icon_manager, string_dict
from src.utils.color_manager import *

from src.ndf_parser.napo_entities.napo_collection import *

from src.wme_widgets import wme_essentials


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

        # TODO: make collapsible

    def add_platoon(self, name_token: str, unit_list: NapoVector, all_units: [str]):
        self.platoon_layout.addWidget(UnitPlatoonWidget(name_token, unit_list, all_units))


# represents one platoon/smart group in Operation Editor
class UnitPlatoonWidget(QtWidgets.QWidget):
    def __init__(self, name_token: str, unit_list: NapoVector, all_units: [str], parent=None):
        super().__init__(parent)

        UnitSelectionCombobox.units = all_units

        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)

        platoon_name_selector = StringSelectionCombobox(name_token)
        self.main_layout.addWidget(platoon_name_selector)
        # TODO: name, remove
        # TODO: list units
        # TODO: add/remove units

        for pair in unit_list.value:
            index = pair.value[0].value
            count = pair.value[1].value
            self.add_unit(index, count)

    def add_unit(self, index: int, count: int):
        unit_name = self.get_unit_name_for_index(index)
        self.main_layout.addWidget(UnitSelectorWidget(count, unit_name))

    def get_unit_name_for_index(self, index: int):
        # TODO
        return ""


class UnitSelectorWidget(QtWidgets.QWidget):
    def __init__(self, count: int, unit_name: str = "", parent=None):
        super().__init__(parent)

        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)

        count_spinbox = QtWidgets.QSpinBox()
        count_spinbox.setRange(1, 100)
        count_spinbox.setValue(count)
        layout.addWidget(count_spinbox)

        unit_selector = UnitSelectionCombobox(unit_name)
        layout.addWidget(unit_selector)

        # TODO: transport if applicable


# Combobox for selecting strings. Displays them as ingame but maps them to tokens
class StringSelectionCombobox(wme_essentials.WMECombobox):
    def __init__(self, token: str = "", parent=None):
        super().__init__(parent)

        for key in string_dict.STRINGS.keys():
            self.addItem(string_dict.STRINGS[key], key)

        if not token == "":
            self.set_index_for_token(token)

    def set_index_for_token(self, token: str):
        index = self.findData(token)
        self.setCurrentIndex(index)


class UnitSelectionCombobox(wme_essentials.WMECombobox):
    units = []

    def __init__(self, unit_name: str = "", parent=None):
        super().__init__(parent)

        self.addItems(self.units)

        if not unit_name == "":
            self.findText(unit_name)
