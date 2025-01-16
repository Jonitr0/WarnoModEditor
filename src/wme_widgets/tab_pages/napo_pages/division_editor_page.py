from PySide6 import QtGui, QtWidgets, QtCore

from src.wme_widgets.tab_pages.napo_pages import base_napo_page
from src.wme_widgets import wme_essentials, wme_collapsible
from src.utils import icon_manager
from src.utils.color_manager import *


class DivisionEditorPage(base_napo_page.BaseNapoPage):
    def __init__(self):
        super().__init__()

        # setup toolbar

        new_div_action = QtGui.QAction(icon=icon_manager.load_icon("file.png", COLORS.PRIMARY),
                                       text='New Division (Ctrl + N)')
        new_div_action.triggered.connect(self.on_new_division)
        new_div_action.setShortcut('Ctrl+N')
        self.tool_bar.insertAction(self.tool_bar.actions()[0], new_div_action)

        div_selector = wme_essentials.WMECombobox()
        div_selector.currentIndexChanged.connect(self.on_division_changed)
        self.tool_bar.insertWidget(self.tool_bar.actions()[2], div_selector)
        # load all available divisions

        self.add_help_button()

        # setup main page

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(scroll_area)

        scroll_widget = QtWidgets.QWidget()
        scroll_area.setWidget(scroll_widget)
        self.scroll_layout = QtWidgets.QVBoxLayout()
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_widget.setLayout(self.scroll_layout)

        # properties editor
        self.property_editor = DivisionPropertiesEditor()
        self.scroll_layout.addWidget(self.property_editor)

        # activation point editor
        self.action_point_editor = DivisionSlotMatrixEditor()
        self.scroll_layout.addWidget(self.action_point_editor)

        # unit editor
        self.unit_editor = DivisionUnitEditor()
        self.scroll_layout.addWidget(self.unit_editor)

        self.scroll_layout.addStretch(1)

        self.update_page()

    def on_new_division(self):
        # open a dialog
        # possibility to copy existing division
        pass

    def on_division_changed(self):
        # load division data
        pass

    def to_json(self) -> dict:
        return {
            "props_collapsed": self.property_editor.collapsed,
            "points_collapsed": self.action_point_editor.collapsed,
            "units_collapsed": self.unit_editor.collapsed
        }

    def from_json(self, json_obj: dict):
        self.property_editor.set_collapsed(json_obj["props_collapsed"])
        self.action_point_editor.set_collapsed(json_obj["points_collapsed"])
        self.unit_editor.set_collapsed(json_obj["units_collapsed"])


class DivisionPropertiesEditor(wme_collapsible.WMECollapsible):
    def __init__(self, parent=None):
        super().__init__(title="Properties", parent=parent)
        form_layout = QtWidgets.QFormLayout()
        form_widget = QtWidgets.QWidget()
        form_widget.setLayout(form_layout)
        self.add_widget(form_widget)

        # needs to be able to find existing strings
        self.name_token_edit = wme_essentials.WMELineEdit()
        form_layout.addRow("Name Token:", self.name_token_edit)

        self.alliance_combobox = wme_essentials.WMECombobox(editable=False)
        self.alliance_combobox.addItems(["NATO", "PACT"])
        form_layout.addRow("Alliance:", self.alliance_combobox)

        # needs to list available countries
        self.nation_combobox = wme_essentials.WMECombobox()
        form_layout.addRow("Nation:", self.nation_combobox)

        self.rating_combobox = wme_essentials.WMECombobox(editable=False)
        self.rating_combobox.addItems(["A", "B", "C"])
        form_layout.addRow("Division Rating:", self.rating_combobox)

        self.type_combobox = wme_essentials.WMECombobox()
        form_layout.addRow("Division Type:", self.type_combobox)

        # needs to be able to load existing icon or import new one
        self.icon_lineedit = wme_essentials.WMELineEdit()
        form_layout.addRow("Emblem:", self.icon_lineedit)


class SlotMatrixComboBox(wme_essentials.WMECombobox):
    value_changed = QtCore.Signal(str, int, int)

    def __init__(self, row: int, col: int, parent: QtWidgets.QWidget = None):
        super().__init__(parent)
        self.row = row
        self.col = col
        self.currentTextChanged.connect(lambda t: self.value_changed.emit(t, self.row, self.col))


class DivisionSlotMatrixEditor(wme_collapsible.WMECollapsible):
    def __init__(self, parent=None):
        super().__init__(title="Activation Points", parent=parent)
        # TODO: maybe replace with table
        self.grid_layout = QtWidgets.QGridLayout()
        grid_widget = QtWidgets.QWidget()
        grid_widget.setLayout(self.grid_layout)
        self.add_widget(grid_widget)

        row_names = ["LOG:", "INF:", "ART:", "TNK:", "REC:", "AA:", "HEL:", "AIR:"]
        selection = ["-"]
        for i in range(10):
            selection.append(str(i))

        # rows
        for i in range(8):
            self.grid_layout.addWidget(QtWidgets.QLabel(row_names[i]), i, 0)
            for j in range(10):
                combobox = SlotMatrixComboBox(i, j)
                combobox.addItems(selection)
                combobox.setCurrentIndex(1)
                combobox.value_changed.connect(self.on_value_changed)
                self.grid_layout.addWidget(combobox, i, j + 1)

        form_layout = QtWidgets.QFormLayout()
        form_widget = QtWidgets.QWidget()
        form_widget.setLayout(form_layout)
        self.add_widget(form_widget)

        self.ap_spinbox = wme_essentials.WMESpinbox()
        self.ap_spinbox.setRange(0, 100)
        self.ap_spinbox.setValue(50)
        form_layout.addRow("Activation Points:", self.ap_spinbox)

    def on_value_changed(self, val: str, row: int, col: int):
        if val == "-":
            for i in range(9 - col):
                w = self.grid_layout.itemAtPosition(row, col + i + 2).widget()
                w.setCurrentText("-")
        elif col <= 9:
            for i in range(col + 1):
                w = self.grid_layout.itemAtPosition(row, i + 1).widget()
                if w.currentText() == "-":
                    if i == 0:
                        w.setCurrentText("0")
                    else:
                        last = self.grid_layout.itemAtPosition(row, i).widget()
                        w.setCurrentText(last.currentText())


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


class DivisionUnitWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # transports (popup?)
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        top_layout = QtWidgets.QHBoxLayout()
        layout.addLayout(top_layout)

        delete_button = QtWidgets.QToolButton()
        # TODO: proper delete icon
        delete_button.setToolTip("Remove Unit from Division")
        delete_button.setIcon(icon_manager.load_icon("titlebar/close.png", COLORS.PRIMARY))
        top_layout.addWidget(delete_button)

        self.unit_selector = wme_essentials.WMECombobox()
        top_layout.addWidget(self.unit_selector)
        # TODO: duplication warning in new universal warning color (orange)
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

