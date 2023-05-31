from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt

from src.wme_widgets.tab_pages.napo_pages.operation_editor import unit_widgets
from src.wme_widgets.tab_pages.napo_pages import base_napo_page
from src.wme_widgets import main_widget, wme_essentials

from src.dialogs import essential_dialogs

from src.ndf_parser import ndf_scanner

PLAYER_DIVS = {
    "Black Horse's Last Stand": "Descriptor_Deck_US_11ACR_multi_HB_OP_01_DEP_PLAYER",
    "Red Juggernaut": "Descriptor_Deck_SOV_79_Gds_Tank_challenge_OP_03_STR_Player",
    "Backhand Blow": "Descriptor_Deck_US_3rd_Arm_challenge_OP_09_STB_Player",
    "The Kitzingen Ruse": "Descriptor_Deck_SOV_35_AirAslt_Brig_challenge_OP_12_AA_Player"
}


class OperationEditor(base_napo_page.BaseNapoPage):
    value_changed = QtCore.Signal()

    def __init__(self):
        super().__init__()

        self.op_combobox = wme_essentials.WMECombobox()
        self.op_combobox.addItems(PLAYER_DIVS.keys())
        self.op_combobox.currentIndexChanged.connect(self.on_new_op_selected)

        self.last_op_index = 0
        self.saved_status = None

        self.tool_bar.addSeparator()

        op_selector = QtWidgets.QWidget()
        op_selector_layout = QtWidgets.QHBoxLayout()
        op_selector.setLayout(op_selector_layout)
        self.tool_bar.addWidget(op_selector)

        op_selector_layout.addWidget(QtWidgets.QLabel("Operation: "))
        op_selector_layout.addWidget(self.op_combobox)

        self.player_deck_napo = None
        self.deck_pack_list = None
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

        # clear layout
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        player_div = PLAYER_DIVS[self.op_combobox.currentText()]
        self.player_deck_napo = self.get_napo_from_object("GameData\\Generated\\Gameplay\\Decks\\Decks.ndf", player_div)
        self.deck_pack_list = self.player_deck_napo.value[0].value.get_napo_value("DeckPackList")

        units = sorted([i.removeprefix("Descriptor_Unit_") for i in
                        ndf_scanner.get_assignment_ids("GameData\\Generated\\Gameplay\\Gfx\\UniteDescriptor.ndf")])
        unit_widgets.UnitSelectionCombobox.units = units

        add_company_button = QtWidgets.QPushButton("Add Company")
        add_company_button.clicked.connect(self.on_add_company)
        add_company_button.setFixedWidth(400)
        self.scroll_layout.addWidget(add_company_button)
        self.scroll_layout.setAlignment(add_company_button, Qt.AlignCenter)
        self.scroll_layout.addStretch(1)

        # get group list
        company_list = self.player_deck_napo.get_napo_value(player_div + "\\DeckCombatGroupList")
        for i in range(len(company_list)):
            # get unit object
            company = company_list.value[i]
            company_name = company.get_raw_value("Name")
            company_widget = self.add_company(company_name, i+1)
            company_widget.value_changed.connect(self.on_value_changed)
            platoon_list = company.get_napo_value("SmartGroupList")
            for j in range(len(platoon_list)):
                # get platoon (index/availability mapping)
                platoon = platoon_list.value[j]
                platoon_name = platoon.get_raw_value("Name")
                platoon_packs = platoon.get_napo_value("PackIndexUnitNumberList")
                company_widget.add_platoon(platoon_name, platoon_packs)

        self.saved_status = self.get_status()
        self.unsaved_changes = False

        main_widget.MainWidget.instance.hide_loading_screen()

    def add_company(self, company_name: str, index: int):
        company_widget = unit_widgets.UnitCompanyWidget(company_name, index, self)
        company_widget.delete_company.connect(self.on_delete_company)
        self.scroll_layout.insertWidget(self.scroll_layout.count() - 2, company_widget)
        return company_widget

    def on_add_company(self):
        company_widget = self.add_company("", self.scroll_layout.count() - 1)
        self.on_value_changed()
        # TODO: add empty/default platoon

    def on_delete_company(self, index):
        dialog = essential_dialogs.ConfirmationDialog("Do you really want to remove Company " + str(index + 1) + "?",
                                                      "Confirm Deletion")
        if not dialog.exec():
            return

        company = self.scroll_layout.takeAt(index)
        if company.widget():
            company.widget().deleteLater()

        for i in range(self.scroll_layout.count() - 2):
            company = self.scroll_layout.itemAt(i).widget()
            company.update_index(i + 1)

        self.on_value_changed()

    def get_status(self):
        companies = []
        for i in range(self.scroll_layout.count() - 2):
            company = self.scroll_layout.itemAt(i).widget()
            companies.append(company.get_status())

        return companies

    def to_json(self) -> dict:
        page_json = {"currentOp": self.op_combobox.currentText()}
        return page_json

    def from_json(self, json_obj: dict):
        self.op_combobox.setCurrentIndex(self.op_combobox.findText(json_obj["currentOp"]))

    def on_value_changed(self):
        new_status = self.get_status()
        self.unsaved_changes = new_status != self.saved_status
