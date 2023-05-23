# TODO (0.3):
# TODO: Descriptor_Deck_US_11ACR_multi_HB_OP_01_DEP_PLAYER
# TODO: add Units to DivisionRules.ndf
# TODO: change Descriptor in Packs.ndf
# TODO: change availability in DeckCombatGroupList in Decks.ndf

from PySide6 import QtWidgets

from src.wme_widgets.tab_pages.napo_pages import base_napo_page
from src.wme_widgets import main_widget

from src.ndf_parser import ndf_scanner


class OperationEditor(base_napo_page.BaseNapoPage):
    def __init__(self):
        super().__init__()

        self.op_combobox = QtWidgets.QComboBox()
        self.op_combobox.addItems(["Black Horse's Last Stand", "Red Juggernaut"])

        self.tool_bar.addSeparator()

        op_selector = QtWidgets.QWidget()
        op_selector_layout = QtWidgets.QHBoxLayout()
        op_selector.setLayout(op_selector_layout)
        self.tool_bar.addWidget(op_selector)

        op_selector_layout.addWidget(QtWidgets.QLabel("Operation: "))
        op_selector_layout.addWidget(self.op_combobox)

        units = ndf_scanner.get_assignment_ids("GameData\\Generated\\Gameplay\\Gfx\\UniteDescriptor.ndf")
        units = [i.removeprefix("Descriptor_Unit_") for i in units]

        test_combobox = QtWidgets.QComboBox()
        test_combobox.setEditable(True)
        test_combobox.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        test_combobox.addItems(units)
        self.scroll_layout.addWidget(test_combobox)

        self.decks_napo = None
        self.packs_napo = None
        self.ddivisionrules_napo = None
        # TODO: read Decks.ndf, get CombatGroups and DeckPackList
        # TODO: get actual units from Packs.ndf
        # TODO: create Widgets
        # TODO: on save: update availability in CombatGroups, add any needed Packs to DeckPackList and Packs.ndf
        # TODO: add new units to DivisionRules.ndf

        #self.update_page()

    def update_page(self):
        main_widget.MainWidget.instance.show_loading_screen("loading files...")

        # TODO: load relevant parts only
        # TODO: "private" keyword in parser
        self.decks_napo = self.get_napo_from_file("GameData\\Generated\\Gameplay\\Decks\\Decks.ndf")
        self.packs_napo = self.get_napo_from_file("GameData\\Generated\\Gameplay\\Decks\\Packs.ndf")
        self.packs_napo = self.get_napo_from_file("GameData\\Generated\\Gameplay\\Decks\\DivisionRules.ndf")

        main_widget.MainWidget.instance.hide_loading_screen()
