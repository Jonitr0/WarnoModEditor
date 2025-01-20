from PySide6 import QtWidgets, QtCore

from src.wme_widgets import wme_essentials, wme_collapsible, main_widget
from src.utils import icon_manager
from src.utils.color_manager import *

actual_categories = {
    "LOG": "Logistic",
    "INF": "Infantry",
    "ART": "Art",
    "TNK": "Tanks",
    "REC": "Recons",
    "AA": "DCA",
    "HEL": "Helis",
    "AIR": "Planes",
}


class DivisionUnitEditor(wme_collapsible.WMECollapsible):
    def __init__(self, parent=None):
        super().__init__(title="Units", parent=parent)

        categories = ["LOG", "INF", "ART", "TNK", "REC", "AA", "HEL", "AIR"]

        for c in categories:
            category_widget = wme_collapsible.WMECollapsible(title=c)
            add_unit_button = QtWidgets.QPushButton(f"Add Unit to {c}")
            add_unit_button.setFixedWidth(200)
            category_widget.add_widget(DivisionUnitWidget(c))
            category_widget.add_widget(add_unit_button)
            self.add_widget(category_widget)

    def get_state(self) -> dict:
        # sort units alphabetically for better comparison
        pass

    def set_state(self, state: dict):
        pass


class DivisionUnitWidget(QtWidgets.QWidget):
    request_delete = QtCore.Signal(QtWidgets.QWidget)

    def __init__(self, category, parent=None):
        super().__init__(parent)
        self.category = category

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        top_layout = QtWidgets.QHBoxLayout()
        layout.addLayout(top_layout)

        delete_button = QtWidgets.QToolButton()
        delete_button.setToolTip("Remove unit from division")
        delete_button.setFixedSize(32, 32)
        delete_button.setIcon(icon_manager.load_icon("trash.png", COLORS.PRIMARY))
        delete_button.clicked.connect(lambda: self.request_delete.emit(self))
        top_layout.addWidget(delete_button)

        self.unit_selector = wme_essentials.WMECombobox()

        all_units = main_widget.instance.unit_loader.get_units()
        unit_names = [u["name"] for u in all_units if u["category"] == actual_categories[self.category]]

        self.unit_selector.addItems(unit_names)
        top_layout.addWidget(self.unit_selector)
        self.duplication_label = QtWidgets.QLabel()
        self.duplication_label.setFixedSize(32, 32)
        self.duplication_label.setPixmap(icon_manager.load_icon("warning.png", COLORS.WARNING).pixmap(24))
        self.duplication_label.setToolTip("Duplicate Warning: This unit already exists in the division, this "
                                          "instance will be ignored.")
        top_layout.addWidget(self.duplication_label)
        top_layout.addStretch(1)

        label_0_vet = QtWidgets.QLabel()
        label_0_vet.setFixedSize(24, 24)
        label_0_vet.setPixmap(icon_manager.load_icon("minus.png", COLORS.PRIMARY).pixmap(24))
        label_0_vet.setToolTip("Availability at 0 experience")
        top_layout.addWidget(label_0_vet)
        self.selector_0_vet = wme_essentials.WMESpinbox()
        self.selector_0_vet.setRange(0, 999)
        top_layout.addWidget(self.selector_0_vet)

        label_1_vet = QtWidgets.QLabel()
        label_1_vet.setFixedSize(24, 24)
        label_1_vet.setPixmap(icon_manager.load_icon("1_exp.png", COLORS.PRIMARY).pixmap(24))
        label_1_vet.setToolTip("Availability at 1 experience")
        top_layout.addWidget(label_1_vet)
        self.selector_1_vet = wme_essentials.WMESpinbox()
        self.selector_1_vet.setRange(0, 999)
        top_layout.addWidget(self.selector_1_vet)

        label_2_vet = QtWidgets.QLabel()
        label_2_vet.setFixedSize(24, 24)
        label_2_vet.setPixmap(icon_manager.load_icon("2_exp.png", COLORS.PRIMARY).pixmap(24))
        label_2_vet.setToolTip("Availability at 2 experience")
        top_layout.addWidget(label_2_vet)
        self.selector_2_vet = wme_essentials.WMESpinbox()
        self.selector_2_vet.setRange(0, 999)
        top_layout.addWidget(self.selector_2_vet)

        label_3_vet = QtWidgets.QLabel()
        label_3_vet.setFixedSize(24, 24)
        label_3_vet.setPixmap(icon_manager.load_icon("3_exp.png", COLORS.PRIMARY).pixmap(24))
        label_3_vet.setToolTip("Availability at 3 experience")
        top_layout.addWidget(label_3_vet)
        self.selector_3_vet = wme_essentials.WMESpinbox()
        self.selector_3_vet.setRange(0, 999)
        top_layout.addWidget(self.selector_3_vet)

        self.transports_section = wme_collapsible.WMECollapsible(title="Transports")
        self.transports_section.set_collapsed(True)
        layout.addWidget(self.transports_section)

        wo_transport_widget = QtWidgets.QWidget()
        wo_transport_layout = QtWidgets.QHBoxLayout()
        wo_transport_widget.setLayout(wo_transport_layout)
        wo_transport_label = QtWidgets.QLabel("Available without transport:")
        self.wo_transport_checkbox = QtWidgets.QCheckBox()
        add_transport_button = QtWidgets.QPushButton("Add Transport")
        add_transport_button.clicked.connect(self.add_transport_widget)
        wo_transport_layout.addWidget(wo_transport_label)
        wo_transport_layout.addWidget(self.wo_transport_checkbox)
        wo_transport_layout.addWidget(add_transport_button)
        self.transports_section.set_corner_widget(wo_transport_widget)

    def get_transports(self) -> list:
        transports = []
        for w in self.transports_section.item_layout.children():
            if isinstance(w, DivisionTransportWidget) and not w.duplication_label.isVisible():
                transports.append(w.unit_selector.currentText())
        return transports

    def get_state(self) -> dict:
        return {
            "unit": self.unit_selector.currentText(),
            "availability": [
                self.selector_0_vet.value(),
                self.selector_1_vet.value(),
                self.selector_2_vet.value(),
                self.selector_3_vet.value(),
            ],
            "transports": [
                self.get_transports()
            ],
        }

    def set_state(self, state: dict):
        self.unit_selector.setCurrentText(state["unit"])
        for i, v in enumerate(state["availability"]):
            getattr(self, f"selector_{i}_vet").setValue(v)
        for t in state["transports"]:
            w = self.add_transport_widget()
            w.unit_selector.setCurrentText(t)

    def add_transport_widget(self):
        widget = DivisionTransportWidget()
        widget.request_delete.connect(lambda w: self.transports_section.item_layout.removeWidget(w))
        self.transports_section.set_collapsed(False)
        self.transports_section.add_widget(widget)
        self.check_transports_for_duplicates()
        return widget

    def check_transports_for_duplicates(self):
        transports = self.get_transports()
        for w in self.transports_section.item_layout.children():
            if isinstance(w, DivisionTransportWidget):
                if w.unit_selector.currentText() in transports:
                    w.duplication_label.setVisible(True)
                else:
                    w.duplication_label.setVisible(False)


class DivisionTransportWidget(QtWidgets.QWidget):
    request_delete = QtCore.Signal(QtWidgets.QWidget)
    unit_changed = QtCore.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)

        delete_button = QtWidgets.QToolButton()
        delete_button.setToolTip("Remove transport from unit")
        delete_button.setIcon(icon_manager.load_icon("trash.png", COLORS.PRIMARY))
        delete_button.setFixedSize(32, 32)
        delete_button.clicked.connect(lambda: self.request_delete.emit(self))
        layout.addWidget(delete_button)

        unit_selector = wme_essentials.WMECombobox()
        all_units = main_widget.instance.unit_loader.get_units()
        unit_names = [u["name"] for u in all_units if u["is_transport"]]
        unit_selector.addItems(unit_names)
        unit_selector.currentTextChanged.connect(lambda t: self.unit_changed.emit(t))
        layout.addWidget(unit_selector)

        self.duplication_label = QtWidgets.QLabel()
        self.duplication_label.setFixedSize(32, 32)
        self.duplication_label.setPixmap(icon_manager.load_icon("warning.png", COLORS.WARNING).pixmap(24))
        self.duplication_label.setToolTip("Duplicate Warning: This transport already exists for the unit, this "
                                          "instance will be ignored.")
        layout.addWidget(self.duplication_label)
        layout.addStretch(1)
