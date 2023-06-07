from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt

from src.utils import icon_manager, string_dict
from src.utils.color_manager import *

from src.ndf_parser.napo_entities.napo_collection import *

from src.wme_widgets.tab_pages import smart_cache
from src.wme_widgets import wme_essentials
from src.dialogs import essential_dialogs


# represents one group of smart groups in Operation Editor
class UnitCompanyWidget(QtWidgets.QWidget):
    delete_company = QtCore.Signal(int)
    value_changed = QtCore.Signal()

    def __init__(self, name_token: str, index: int, callback, parent=None):
        super().__init__(parent)

        self.collapse_icon = icon_manager.load_icon("chevron_down.png", COLORS.PRIMARY)
        self.expand_icon = icon_manager.load_icon("chevron_right.png", COLORS.PRIMARY)
        self.index = index
        self.platoon_count = 0
        self.collapsed = False
        self.callback = callback

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 10, 0)
        self.setLayout(main_layout)

        header_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(header_layout)

        self.collapse_button = QtWidgets.QToolButton()
        self.collapse_button.setFixedSize(32, 32)
        self.collapse_button.setIcon(self.collapse_icon)
        self.collapse_button.clicked.connect(self.on_collapse)
        header_layout.addWidget(self.collapse_button)

        self.index_label = QtWidgets.QLabel("Company " + str(index) + ":")
        header_layout.addWidget(self.index_label)

        self.company_name_selector = StringSelectionCombobox(name_token)
        self.company_name_selector.currentIndexChanged.connect(self.on_value_changed)
        header_layout.addWidget(self.company_name_selector)

        header_layout.addStretch(1)
        delete_button = QtWidgets.QPushButton("Remove Company")
        delete_button.clicked.connect(self.on_delete)
        header_layout.addWidget(delete_button)

        self.platoon_layout = QtWidgets.QVBoxLayout()
        self.platoon_layout.setContentsMargins(50, 0, 0, 0)
        main_layout.addLayout(self.platoon_layout)

        add_platoon_button = QtWidgets.QPushButton("Add Platoon to Company " + str(self.index))
        add_platoon_button.clicked.connect(self.on_add_platoon)
        add_platoon_button.setFixedWidth(400)
        self.platoon_layout.addWidget(add_platoon_button)
        self.platoon_layout.setAlignment(add_platoon_button, Qt.AlignCenter)

    def add_platoon(self, name_token: str, unit_list: NapoVector):
        self.platoon_count += 1
        platoon_widget = UnitPlatoonWidget(name_token, unit_list, self.callback, self.platoon_count)
        platoon_widget.delete_platoon.connect(self.delete_platoon)
        platoon_widget.value_changed.connect(self.on_value_changed)
        self.platoon_layout.insertWidget(self.platoon_layout.count() - 1, platoon_widget)
        return platoon_widget

    def on_add_platoon(self):
        self.add_platoon("", NapoVector())
        self.on_value_changed()

    def on_collapse(self):
        self.collapsed = not self.collapsed

        self.collapse_button.setIcon(self.expand_icon if self.collapsed else self.collapse_icon)

        for i in range(self.platoon_layout.count()):
            self.platoon_layout.itemAt(i).widget().setHidden(self.collapsed)

    def on_delete(self):
        self.delete_company.emit(self.index - 1)
        self.on_value_changed()

    def delete_platoon(self, index):
        dialog = essential_dialogs.ConfirmationDialog("Do you really want to remove Platoon " + str(index + 1) + "?",
                                                      "Confirm Deletion")
        if not dialog.exec():
            return

        platoon = self.platoon_layout.takeAt(index)
        if platoon.widget():
            platoon.widget().deleteLater()

        for i in range(self.platoon_layout.count() - 1):
            platoon = self.platoon_layout.itemAt(i).widget()
            platoon.update_index(i + 1)

        self.platoon_count -= 1
        self.on_value_changed()

    def update_index(self, index):
        self.index = index
        self.index_label.setText("Company " + str(index) + ":")
        
    def get_state(self):
        platoons = []
        for i in range(self.platoon_layout.count() - 1):
            platoon = self.platoon_layout.itemAt(i).widget()
            platoons.append(platoon.get_state())

        return {
            "name": self.company_name_selector.currentData(),
            "platoons": platoons
        }

    def on_value_changed(self):
        self.value_changed.emit()


packs_to_units_sc = smart_cache.SmartCache("GameData\\Generated\\Gameplay\\Decks\\Packs.ndf")
MAX_UNITS_PER_PLATOON = 3


# represents one platoon/smart group in Operation Editor
class UnitPlatoonWidget(QtWidgets.QWidget):
    delete_platoon = QtCore.Signal(int)
    value_changed = QtCore.Signal()

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

        self.index_label = QtWidgets.QLabel("Platoon " + str(index) + ":")
        header_layout.addWidget(self.index_label)

        self.platoon_name_selector = StringSelectionCombobox(name_token)
        self.platoon_name_selector.currentIndexChanged.connect(self.on_value_changed)
        header_layout.addWidget(self.platoon_name_selector)

        header_layout.addStretch(1)
        delete_button = QtWidgets.QPushButton("Remove Platoon")
        delete_button.clicked.connect(self.on_delete)
        header_layout.addWidget(delete_button)

        self.unit_layout = QtWidgets.QVBoxLayout()
        self.unit_layout.setContentsMargins(50, 0, 0, 0)
        main_layout.addLayout(self.unit_layout)

        self.add_unit_button = QtWidgets.QPushButton("Add Unit to Platoon " + str(index))
        self.add_unit_button.clicked.connect(self.on_add_unit)
        self.add_unit_button.setFixedWidth(400)
        self.unit_layout.addWidget(self.add_unit_button)
        self.unit_layout.setAlignment(self.add_unit_button, Qt.AlignCenter)

        for pair in unit_list.value:
            index = pair.value[0].value
            count = pair.value[1].value
            self.add_unit(index, count, self.unit_layout.count() - 1)

    def add_unit(self, index: int, count: int, layout_index: int):
        unit_name, transport, exp_level = self.get_unit_name_for_index(index)
        self.add_unit_with_data(layout_index, count, exp_level, unit_name, transport)

    def add_unit_with_data(self, layout_index: int, count: int, exp_level: int, unit_name: str, transport: str):
        unit_widget = UnitSelectorWidget(layout_index, count, exp_level, unit_name, transport)
        unit_widget.delete_unit.connect(self.delete_unit)
        unit_widget.value_changed.connect(self.on_value_changed)
        self.unit_layout.insertWidget(self.unit_layout.count() - 1, unit_widget)
        # units widgets + button
        if self.unit_layout.count() > MAX_UNITS_PER_PLATOON:
            self.add_unit_button.setHidden(True)

    def on_add_unit(self):
        self.add_unit(0, 1, self.unit_layout.count() - 1)
        self.on_value_changed()

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

    def on_delete(self):
        self.delete_platoon.emit(self.index - 1)
        self.on_value_changed()

    def delete_unit(self, index):
        unit = self.unit_layout.takeAt(index)
        if unit.widget():
            unit.widget().deleteLater()

        for i in range(self.unit_layout.count() - 1):
            unit = self.unit_layout.itemAt(i).widget()
            unit.update_index(i)

        self.add_unit_button.setHidden(False)
        self.on_value_changed()

    def update_index(self, index):
        self.index = index
        self.index_label.setText("Platoon " + str(index) + ":")

    def get_state(self):
        units = []
        for i in range(self.unit_layout.count() - 1):
            unit = self.unit_layout.itemAt(i).widget()
            units.append(unit.get_state())

        return {
            "name": self.platoon_name_selector.currentData(),
            "units": units
        }

    def on_value_changed(self):
        self.value_changed.emit()


class UnitSelectorWidget(QtWidgets.QWidget):
    delete_unit = QtCore.Signal(int)
    value_changed = QtCore.Signal()

    def __init__(self, index: int, count: int, exp_level: int = 0, unit_name: str = "",
                 transport: str = None, parent=None):
        super().__init__(parent)

        self.index = index

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(50, 0, 0, 0)
        self.setLayout(main_layout)

        separator = QtWidgets.QWidget()
        separator.setObjectName("separator")
        separator.setFixedHeight(1)
        main_layout.addWidget(separator)

        top_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(top_layout)

        self.count_spinbox = wme_essentials.WMESpinbox()
        self.count_spinbox.setRange(1, 100)
        self.count_spinbox.setValue(count)
        self.count_spinbox.valueChanged.connect(self.on_value_changed)
        top_layout.addWidget(self.count_spinbox)
        top_layout.addWidget(QtWidgets.QLabel("x"))

        self.unit_selector = UnitSelectionCombobox(unit_name)
        self.unit_selector.currentIndexChanged.connect(self.on_value_changed)
        top_layout.addWidget(self.unit_selector)

        top_layout.addWidget(QtWidgets.QLabel("Experience: "))
        self.exp_selector = wme_essentials.WMECombobox()
        self.exp_selector.addItem(icon_manager.load_icon("minus.png", COLORS.PRIMARY), "", 0)
        self.exp_selector.addItem(icon_manager.load_icon("1_exp.png", COLORS.PRIMARY), "", 1)
        self.exp_selector.addItem(icon_manager.load_icon("2_exp.png", COLORS.PRIMARY), "", 2)
        self.exp_selector.addItem(icon_manager.load_icon("3_exp.png", COLORS.PRIMARY), "", 3)
        self.exp_selector.setCurrentIndex(exp_level)
        self.exp_selector.currentIndexChanged.connect(self.on_value_changed)
        top_layout.addWidget(self.exp_selector)

        top_layout.addStretch(1)
        delete_button = QtWidgets.QPushButton("Remove Unit")
        delete_button.clicked.connect(self.on_delete)
        top_layout.addWidget(delete_button)

        bottom_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(bottom_layout)

        self.transport_label = QtWidgets.QLabel("Transport: ")
        self.transport_label.setHidden(bool(transport))
        bottom_layout.addWidget(self.transport_label)
        self.transport_selector = UnitSelectionCombobox(transport)
        self.transport_selector.currentIndexChanged.connect(self.on_value_changed)
        bottom_layout.addWidget(self.transport_selector)
        self.transport_button = QtWidgets.QPushButton()
        self.transport_button.clicked.connect(self.on_transport)
        bottom_layout.addWidget(self.transport_button)

        self.on_transport(False)

        bottom_layout.addStretch(1)

    def on_transport(self, emit: bool = True):
        # add transport
        if self.transport_label.isHidden():
            self.transport_label.setHidden(False)
            self.transport_selector.setHidden(False)
            self.transport_button.setText("Remove Transport")
        # remove transport
        else:
            self.transport_label.setHidden(True)
            self.transport_selector.setHidden(True)
            self.transport_button.setText("Add Transport")

        if emit:
            self.value_changed.emit()

    def on_delete(self):
        self.delete_unit.emit(self.index)

    def update_index(self, index):
        self.index = index

    def get_state(self):
        return {
            "unit_name": self.unit_selector.currentText(),
            "count": self.count_spinbox.value(),
            "exp": self.exp_selector.currentIndex(),
            "transport": self.transport_selector.currentText() if not self.transport_selector.isHidden() else None
        }

    def on_value_changed(self):
        self.value_changed.emit()


# Combobox for selecting strings. Displays them as ingame but maps them to tokens
class StringSelectionCombobox(wme_essentials.WMECombobox):
    def __init__(self, token: str = "", parent=None):
        super().__init__(parent)

        for key in string_dict.STRINGS.keys():
            self.addItem(string_dict.STRINGS[key], key)

        if not (token == "" or token is None):
            self.set_index_for_token(token)

    def set_index_for_token(self, token: str):
        index = self.findData(token)
        self.setCurrentIndex(index)


class UnitSelectionCombobox(wme_essentials.WMECombobox):
    units = []

    def __init__(self, unit_name: str = "", parent=None):
        super().__init__(parent)

        self.addItems(self.units)

        if not (unit_name == "" or unit_name is None):
            self.setCurrentIndex(self.findText(unit_name))
