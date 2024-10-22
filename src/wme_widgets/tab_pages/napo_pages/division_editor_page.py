from PySide6 import QtGui, QtWidgets

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

        # properties editor:
        self.property_editor = DivisionPropertiesEditor()
        self.scroll_layout.addWidget(self.property_editor)

        # action point editor (collapsible)
        # collapsible category editors: Gridlayout? Transport Popup Menu?

        self.scroll_layout.addStretch(1)

        self.update_page()

    def on_new_division(self):
        # open a dialog
        # possibility to copy existing division
        pass

    def on_division_changed(self):
        # load division data
        pass


class DivisionPropertiesEditor(wme_collapsible.WMECollapsible):
    def __init__(self, parent=None):
        super().__init__(title="Division Properties", parent=parent)
        form_layout = QtWidgets.QFormLayout()
        form_widget = QtWidgets.QWidget()
        form_widget.setLayout(form_layout)
        self.add_widget(form_widget)

        self.internal_name_edit = wme_essentials.WMELineEdit()
        form_layout.addRow("Internal Name", self.internal_name_edit)

        # needs to be able to find existing strings
        self.name_token_edit = wme_essentials.WMELineEdit()
        form_layout.addRow("Name Token", self.name_token_edit)

        self.alliance_combobox = wme_essentials.WMECombobox(editable=False)
        self.alliance_combobox.addItems(["NATO", "PACT"])
        form_layout.addRow("Alliance", self.alliance_combobox)

        # needs to list available countries
        self.nation_combobox = wme_essentials.WMECombobox()
        form_layout.addRow("Nation", self.nation_combobox)

        self.rating_combobox = wme_essentials.WMECombobox(editable=False)
        self.rating_combobox.addItems(["A", "B", "C"])
        form_layout.addRow("Division Rating", self.rating_combobox)

        self.type_combobox = wme_essentials.WMECombobox()
        form_layout.addRow("Division Type", self.type_combobox)

        # needs to be able to load existing icon or import new one
        self.icon_lineedit = wme_essentials.WMELineEdit()
        form_layout.addRow("Icon", self.icon_lineedit)
