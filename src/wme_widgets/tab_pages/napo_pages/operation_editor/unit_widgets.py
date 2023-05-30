from PySide6 import QtWidgets
from PySide6.QtCore import Qt

from src.utils import icon_manager, string_dict
from src.utils.color_manager import *

from src.ndf_parser.napo_entities.napo_collection import *

from src.wme_widgets.tab_pages import smart_cache
from src.wme_widgets import wme_essentials


# represents one group of smart groups in Operation Editor
class UnitCompanyWidget(QtWidgets.QWidget):
    def __init__(self, name_token: str, index: int, parent=None):
        super().__init__(parent)

        self.collapse_icon = icon_manager.load_icon("chevron_down.png", COLORS.PRIMARY)
        self.expand_icon = icon_manager.load_icon("chevron_right.png", COLORS.PRIMARY)
        self.index = index
        self.platoon_count = 0
        self.collapsed = False

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        header_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(header_layout)

        self.collapse_button = QtWidgets.QToolButton()
        self.collapse_button.setFixedSize(32, 32)
        self.collapse_button.setIcon(self.collapse_icon)
        self.collapse_button.clicked.connect(self.on_collapse)
        header_layout.addWidget(self.collapse_button)

        header_layout.addWidget(QtWidgets.QLabel("Company " + str(index) + ":"))

        group_name_selector = StringSelectionCombobox(name_token)
        header_layout.addWidget(group_name_selector)

        header_layout.addStretch(1)
        delete_button = QtWidgets.QPushButton("Remove Company")
        delete_button.clicked.connect(self.on_delete)
        header_layout.addWidget(delete_button)

        self.platoon_layout = QtWidgets.QVBoxLayout()
        self.platoon_layout.setContentsMargins(50, 0, 0, 0)
        main_layout.addLayout(self.platoon_layout)

    def add_platoon(self, name_token: str, unit_list: NapoVector, callback):
        self.platoon_count += 1
        self.platoon_layout.addWidget(UnitPlatoonWidget(name_token, unit_list, callback, self.platoon_count))

    def on_collapse(self):
        self.collapsed = not self.collapsed

        self.collapse_button.setIcon(self.expand_icon if self.collapsed else self.collapse_icon)

        for i in range(self.platoon_layout.count()):
            self.platoon_layout.itemAt(i).widget().setHidden(self.collapsed)

    def on_delete(self):
        print(self.parent())


packs_to_units_sc = smart_cache.SmartCache("GameData\\Generated\\Gameplay\\Decks\\Packs.ndf")
MAX_UNITS_PER_PLATOON = 3


# represents one platoon/smart group in Operation Editor
class UnitPlatoonWidget(QtWidgets.QWidget):
    def __init__(self, name_token: str, unit_list: NapoVector, callback, index, parent=None):
        super().__init__(parent)

        self.collapse_icon = icon_manager.load_icon("chevron_down.png", COLORS.PRIMARY)
        self.expand_icon = icon_manager.load_icon("chevron_right.png", COLORS.PRIMARY)
        self.callback = callback
        self.index = index
        self.collapsed = False

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        header_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(header_layout)

        self.collapse_button = QtWidgets.QToolButton()
        self.collapse_button.setFixedSize(32, 32)
        self.collapse_button.setIcon(self.collapse_icon)
        self.collapse_button.clicked.connect(self.on_collapse)
        header_layout.addWidget(self.collapse_button)

        header_layout.addWidget(QtWidgets.QLabel("Platoon " + str(index) + ":"))

        self.platoon_name_selector = StringSelectionCombobox(name_token)
        header_layout.addWidget(self.platoon_name_selector)

        header_layout.addStretch(1)
        delete_button = QtWidgets.QPushButton("Remove Platoon")
        header_layout.addWidget(delete_button)

        self.unit_layout = QtWidgets.QVBoxLayout()
        self.unit_layout.setContentsMargins(50, 0, 0, 0)
        main_layout.addLayout(self.unit_layout)

        self.add_unit_button = QtWidgets.QPushButton("Add Unit to Platoon " + str(index))
        self.add_unit_button.setFixedWidth(400)
        self.unit_layout.addWidget(self.add_unit_button)
        self.unit_layout.setAlignment(self.add_unit_button, Qt.AlignCenter)
        # TODO: remove
        # TODO: add/remove units

        for pair in unit_list.value:
            index = pair.value[0].value
            count = pair.value[1].value
            self.add_unit(index, count)

    def add_unit(self, index: int, count: int):
        unit_name, transport, exp_level = self.get_unit_name_for_index(index)
        self.unit_layout.insertWidget(self.unit_layout.count() - 1,
                                      UnitSelectorWidget(count, exp_level, unit_name, transport))
        # units widgets + button
        if self.unit_layout.count() > MAX_UNITS_PER_PLATOON:
            self.add_unit_button.setHidden(True)

    def get_unit_name_for_index(self, index: int):
        deck_pack = self.callback.deck_pack_list.value[index]
        pack_name = deck_pack.get_raw_value("DeckPack").removeprefix("~/")
        exp_level = deck_pack.get_raw_value("ExperienceLevel")
        try:
            transport_name = deck_pack.get_raw_value("Transport").removeprefix("~/Descriptor_Unit_")
        except Exception:
            transport_name = None

        global packs_to_units_sc
        if packs_to_units_sc.contains(pack_name):
            unit_name = packs_to_units_sc.get(pack_name)
        else:
            pack = self.callback.get_napo_from_object("GameData\\Generated\\Gameplay\\Decks\\Packs.ndf", pack_name)
            unit_name = pack.get_raw_value(pack_name +
                                           "\\TransporterAndUnitsList\\TDeckTransporterAndUnitsDescriptor"
                                           "\\UnitDescriptor")
            packs_to_units_sc.set(pack_name, unit_name)

        return unit_name.removeprefix("Descriptor_Unit_"), transport_name, exp_level

    def on_collapse(self):
        self.collapsed = not self.collapsed

        self.collapse_button.setIcon(self.expand_icon if self.collapsed else self.collapse_icon)

        for i in range(self.unit_layout.count()):
            self.unit_layout.itemAt(i).widget().setHidden(self.collapsed)


class UnitSelectorWidget(QtWidgets.QWidget):
    def __init__(self, count: int, exp_level: int = 0, unit_name: str = "", transport: str = None, parent=None):
        super().__init__(parent)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(50, 0, 0, 0)
        self.setLayout(main_layout)

        separator = QtWidgets.QWidget()
        separator.setObjectName("separator")
        separator.setFixedHeight(1)
        main_layout.addWidget(separator)

        top_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(top_layout)

        count_spinbox = wme_essentials.WMESpinbox()
        count_spinbox.setRange(1, 100)
        count_spinbox.setValue(count)
        top_layout.addWidget(count_spinbox)
        top_layout.addWidget(QtWidgets.QLabel("x"))

        unit_selector = UnitSelectionCombobox(unit_name)
        top_layout.addWidget(unit_selector)

        top_layout.addWidget(QtWidgets.QLabel("Experience: "))
        exp_selector = wme_essentials.WMECombobox()
        exp_selector.addItem(icon_manager.load_icon("minus.png", COLORS.PRIMARY), "", 0)
        exp_selector.addItem(icon_manager.load_icon("1_exp.png", COLORS.PRIMARY), "", 1)
        exp_selector.addItem(icon_manager.load_icon("2_exp.png", COLORS.PRIMARY), "", 2)
        exp_selector.addItem(icon_manager.load_icon("3_exp.png", COLORS.PRIMARY), "", 3)
        exp_selector.setCurrentIndex(exp_level)
        top_layout.addWidget(exp_selector)

        top_layout.addStretch(1)
        delete_button = QtWidgets.QPushButton("Remove Unit")
        top_layout.addWidget(delete_button)

        bottom_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(bottom_layout)

        transport_label = QtWidgets.QLabel("Transport: ")
        bottom_layout.addWidget(transport_label)
        transport_button = QtWidgets.QPushButton()
        bottom_layout.addWidget(transport_button)

        if transport:
            transport_selector = UnitSelectionCombobox(transport)
            bottom_layout.insertWidget(1, transport_selector)

            transport_button.setText("Remove Transport")
        else:
            transport_label.setHidden(True)
            transport_button.setText("Add transport")

        bottom_layout.addStretch(1)


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
            self.setCurrentIndex(self.findText(unit_name))
