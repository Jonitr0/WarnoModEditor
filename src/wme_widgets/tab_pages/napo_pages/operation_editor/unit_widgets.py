from PySide6 import QtWidgets

from src.utils import icon_manager, string_dict
from src.utils.color_manager import *

from src.ndf_parser.napo_entities.napo_collection import *

from src.wme_widgets.tab_pages import smart_cache
from src.wme_widgets import wme_essentials


# represents one group of smart groups in Operation Editor
class UnitCompanyWidget(QtWidgets.QWidget):
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

    def add_platoon(self, name_token: str, unit_list: NapoVector, callback):
        self.platoon_layout.addWidget(UnitPlatoonWidget(name_token, unit_list, callback))


packs_to_units_sc = smart_cache.SmartCache("GameData\\Generated\\Gameplay\\Decks\\Packs.ndf")


# represents one platoon/smart group in Operation Editor
class UnitPlatoonWidget(QtWidgets.QWidget):
    def __init__(self, name_token: str, unit_list: NapoVector, callback, parent=None):
        super().__init__(parent)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)
        self.callback = callback

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
        unit_name, transport = self.get_unit_name_for_index(index)
        self.main_layout.addWidget(UnitSelectorWidget(count, unit_name, transport))

    def get_unit_name_for_index(self, index: int):
        deck_pack = self.callback.deck_pack_list.value[index]
        pack_name = deck_pack.get_raw_value("DeckPack").removeprefix("~/")
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

        # TODO: add unit exp
        # TODO: add optional transport

        return unit_name.removeprefix("Descriptor_Unit_"), transport_name


class UnitSelectorWidget(QtWidgets.QWidget):
    def __init__(self, count: int, unit_name: str = "", transport: str = None, parent=None):
        super().__init__(parent)

        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)

        count_spinbox = QtWidgets.QSpinBox()
        count_spinbox.setRange(1, 100)
        count_spinbox.setValue(count)
        layout.addWidget(count_spinbox)

        unit_selector = UnitSelectionCombobox(unit_name)
        layout.addWidget(unit_selector)

        transport_button = QtWidgets.QPushButton()
        layout.addWidget(transport_button)

        if transport:
            transport_selector = UnitSelectionCombobox(transport)
            layout.insertWidget(layout.count()-1, transport_selector)

            transport_button.setText("Remove Transport")
        else:
            transport_button.setText("Add transport")

        layout.addStretch(1)


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

    # TODO: make this work
    def focusInEvent(self, event) -> None:
        self.showPopup()
        super().focusInEvent(event)

    def focusOutEvent(self, event) -> None:
        self.hidePopup()
        super().focusOutEvent(event)
