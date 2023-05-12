# TODO (0.3):
# TODO: Descriptor_Deck_US_11ACR_multi_HB_OP_01_DEP_PLAYER
# TODO: add Units to DivisionRules.ndf
# TODO: change Descriptor in Packs.ndf
# TODO: change availability in DeckCombatGroupList in Decks.ndf

# TODO: create NDF scanner to get top level assignment IDs

from PySide6 import QtWidgets

from src.wme_widgets.tab_pages.napo_pages import base_napo_page

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

        ndf_scanner.get_assignment_ids("GameData\\Generated\\Gameplay\\Gfx\\UniteDescriptor.ndf")
