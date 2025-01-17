from PySide6 import QtGui, QtWidgets

from src.wme_widgets.tab_pages.napo_pages.division_editor import (division_properties_editor,
                                                                  division_slot_matrix_editor, division_unit_editor)
from src.wme_widgets.tab_pages.napo_pages import base_napo_page
from src.wme_widgets import wme_essentials
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

        # TODO: better a load button with a dialog
        div_selector = wme_essentials.WMECombobox()
        div_selector.currentIndexChanged.connect(self.on_division_changed)
        self.tool_bar.insertWidget(self.tool_bar.actions()[2], div_selector)
        # load all available divisions

        # TODO: add "delete division" function

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
        self.property_editor = division_properties_editor.DivisionPropertiesEditor()
        self.scroll_layout.addWidget(self.property_editor)

        # activation point editor
        self.action_point_editor = division_slot_matrix_editor.DivisionSlotMatrixEditor()
        self.scroll_layout.addWidget(self.action_point_editor)

        # unit editor
        self.unit_editor = division_unit_editor.DivisionUnitEditor()
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



