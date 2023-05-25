# TODO (0.3):
# TODO: Descriptor_Deck_US_11ACR_multi_HB_OP_01_DEP_PLAYER
# TODO: add Units to DivisionRules.ndf
# TODO: change Descriptor in Packs.ndf
# TODO: change availability in DeckCombatGroupList in Decks.ndf

from PySide6 import QtWidgets

from src.wme_widgets.tab_pages.napo_pages import base_napo_page
from src.wme_widgets import main_widget

from src.dialogs import essential_dialogs

from src.ndf_parser import ndf_scanner

# TODO: add new operations
PLAYER_DIVS = {
    "Black Horse's Last Stand": "Descriptor_Deck_US_11ACR_multi_HB_OP_01_DEP_PLAYER",
    "Red Juggernaut": "Descriptor_Deck_SOV_79_Gds_Tank_challenge_OP_03_STR_Player"
}


class OperationEditor(base_napo_page.BaseNapoPage):
    def __init__(self):
        super().__init__()

        self.op_combobox = QtWidgets.QComboBox()
        self.op_combobox.addItems(["Black Horse's Last Stand", "Red Juggernaut"])
        self.op_combobox.currentIndexChanged.connect(self.on_new_op_selected)

        self.last_op_index = 0

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

        self.player_deck_napo = None
        # TODO: read Decks.ndf, get CombatGroups and DeckPackList
        # TODO: get actual units from Packs.ndf
        # TODO: create Widgets
        # TODO: on save: update availability in CombatGroups, add any needed Packs to DeckPackList and Packs.ndf
        # TODO: add new units to DivisionRules.ndf

        self.update_page()

    def on_new_op_selected(self, index: int):
        if index == self.last_op_index:
            return

        if self.unsaved_changes:
            dialog = essential_dialogs.AskToSaveDialog(self.op_combobox.currentText())
            res = dialog.exec()
            if not res:
                self.op_combobox.setCurrentIndex(self.last_op_index)
                return
            elif dialog.save_changes:
                self.save_changes()

        self.last_op_index = index
        self.update_page()

    def update_page(self):
        main_widget.MainWidget.instance.show_loading_screen("loading files...")

        player_div = PLAYER_DIVS[self.op_combobox.currentText()]
        self.player_deck_napo = self.get_napo_from_object("GameData\\Generated\\Gameplay\\Decks\\Decks.ndf", player_div)

        # get group list
        group_list = self.player_deck_napo.get_napo_value(player_div + "\\DeckCombatGroupList")
        for i in range(len(group_list)):
            # get unit object
            group = group_list.value[i]
            group_name = group.get_raw_value("Name")
            print(group_name)
            platoon_list = group.get_napo_value("SmartGroupList")
            for j in range(len(platoon_list)):
                # get platoon (index/availability mapping)
                platoon = platoon_list.value[j]
                platoon_name = platoon.get_raw_value("Name")
                platoon_packs = platoon.get_napo_value("PackIndexUnitNumberList")
                print(platoon_name)
                # TODO: create a predefined list of names for players to choose from

        main_widget.MainWidget.instance.hide_loading_screen()
