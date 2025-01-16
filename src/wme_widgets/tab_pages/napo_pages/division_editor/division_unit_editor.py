from PySide6 import QtWidgets

from src.wme_widgets import wme_essentials, wme_collapsible
from src.utils import icon_manager
from src.utils.color_manager import *


class DivisionUnitEditor(wme_collapsible.WMECollapsible):
    def __init__(self, parent=None):
        super().__init__(title="Units", parent=parent)

        categories = ["LOG", "INF", "ART", "TNK", "REC", "AA", "HEL", "AIR"]

        for c in categories:
            category_widget = wme_collapsible.WMECollapsible(title=c)
            add_unit_button = QtWidgets.QPushButton(f"Add Unit to {c}")
            add_unit_button.setFixedWidth(200)
            category_widget.add_widget(DivisionUnitWidget())
            category_widget.add_widget(DivisionUnitWidget())
            category_widget.add_widget(add_unit_button)
            self.add_widget(category_widget)

    def get_state(self) -> dict:
        # sort units alphabetically for better comparison
        pass

    def set_state(self, state: dict):
        pass


class DivisionUnitWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        top_layout = QtWidgets.QHBoxLayout()
        layout.addLayout(top_layout)

        delete_button = QtWidgets.QToolButton()
        # TODO: proper delete icon
        delete_button.setToolTip("Remove unit from division")
        delete_button.setIcon(icon_manager.load_icon("titlebar/close.png", COLORS.PRIMARY))
        top_layout.addWidget(delete_button)

        self.unit_selector = wme_essentials.WMECombobox()
        top_layout.addWidget(self.unit_selector)
        self.duplication_label = QtWidgets.QLabel()
        self.duplication_label.setFixedSize(32, 32)
        # TODO: proper warning icon
        # TODO: orange warning color
        self.duplication_label.setPixmap(icon_manager.load_icon("error_log.png", COLORS.WARNING).pixmap(24))
        self.duplication_label.setToolTip("Duplicate Warning: This unit already exists in the division, this "
                                          "instance will be ignored.")
        top_layout.addWidget(self.duplication_label)
        top_layout.addStretch(1)

        label_0_vet = QtWidgets.QLabel()
        label_0_vet.setFixedSize(24, 24)
        label_0_vet.setPixmap(icon_manager.load_icon("minus.png", COLORS.PRIMARY).pixmap(24))
        label_0_vet.setToolTip("Availability at 0 experience")
        top_layout.addWidget(label_0_vet)
        selector_0_vet = wme_essentials.WMESpinbox()
        selector_0_vet.setRange(0, 999)
        top_layout.addWidget(selector_0_vet)

        label_1_vet = QtWidgets.QLabel()
        label_1_vet.setFixedSize(24, 24)
        label_1_vet.setPixmap(icon_manager.load_icon("1_exp.png", COLORS.PRIMARY).pixmap(24))
        label_1_vet.setToolTip("Availability at 1 experience")
        top_layout.addWidget(label_1_vet)
        selector_1_vet = wme_essentials.WMESpinbox()
        selector_1_vet.setRange(0, 999)
        top_layout.addWidget(selector_1_vet)

        label_2_vet = QtWidgets.QLabel()
        label_2_vet.setFixedSize(24, 24)
        label_2_vet.setPixmap(icon_manager.load_icon("2_exp.png", COLORS.PRIMARY).pixmap(24))
        label_2_vet.setToolTip("Availability at 2 experience")
        top_layout.addWidget(label_2_vet)
        selector_2_vet = wme_essentials.WMESpinbox()
        selector_2_vet.setRange(0, 999)
        top_layout.addWidget(selector_2_vet)

        label_3_vet = QtWidgets.QLabel()
        label_3_vet.setFixedSize(24, 24)
        label_3_vet.setPixmap(icon_manager.load_icon("3_exp.png", COLORS.PRIMARY).pixmap(24))
        label_3_vet.setToolTip("Availability at 3 experience")
        top_layout.addWidget(label_3_vet)
        selector_3_vet = wme_essentials.WMESpinbox()
        selector_3_vet.setRange(0, 999)
        top_layout.addWidget(selector_3_vet)

        transports_section = wme_collapsible.WMECollapsible(title="Transports")
        transports_section.add_widget(DivisionTransportWidget())
        transports_section.add_widget(DivisionTransportWidget())
        transports_section.set_collapsed(True)
        layout.addWidget(transports_section)

        wo_transport_widget = QtWidgets.QWidget()
        wo_transport_layout = QtWidgets.QHBoxLayout()
        wo_transport_widget.setLayout(wo_transport_layout)
        wo_transport_label = QtWidgets.QLabel("Available without transport:")
        wo_transport_checkbox = QtWidgets.QCheckBox()
        add_transport_button = QtWidgets.QPushButton("Add Transport")
        wo_transport_layout.addWidget(wo_transport_label)
        wo_transport_layout.addWidget(wo_transport_checkbox)
        wo_transport_layout.addWidget(add_transport_button)
        transports_section.set_corner_widget(wo_transport_widget)

    def get_state(self) -> dict:
        pass

    def set_state(self, state: dict):
        pass


class DivisionTransportWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)

        delete_button = QtWidgets.QToolButton()
        # TODO: proper delete icon
        delete_button.setToolTip("Remove transport from unit")
        delete_button.setIcon(icon_manager.load_icon("titlebar/close.png", COLORS.PRIMARY))
        layout.addWidget(delete_button)

        unit_selector = wme_essentials.WMECombobox()
        layout.addWidget(unit_selector)

        self.duplication_label = QtWidgets.QLabel()
        self.duplication_label.setFixedSize(32, 32)
        # TODO: proper warning icon
        # TODO: orange warning color
        self.duplication_label.setPixmap(icon_manager.load_icon("error_log.png", COLORS.WARNING).pixmap(24))
        self.duplication_label.setToolTip("Duplicate Warning: This transport already exists for the unit, this "
                                          "instance will be ignored.")
        layout.addWidget(self.duplication_label)
        layout.addStretch(1)


