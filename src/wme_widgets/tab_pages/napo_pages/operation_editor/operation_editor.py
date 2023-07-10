import uuid
import os

from antlr4 import *

from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt

from src.wme_widgets.tab_pages.napo_pages.operation_editor import unit_widgets
from src.wme_widgets.tab_pages.napo_pages import base_napo_page
from src.wme_widgets import main_widget, wme_essentials

from src.dialogs import essential_dialogs

from src.ndf_parser.antlr_output.NdfGrammarLexer import NdfGrammarLexer
from src.ndf_parser.antlr_output.NdfGrammarParser import NdfGrammarParser

from src.ndf_parser import ndf_scanner
from src.ndf_parser.object_generator import napo_generator
from src.ndf_parser.ndf_converter import napo_to_ndf_converter

from src.ndf_parser.napo_entities.napo_collection import *
from src.ndf_parser.napo_entities.napo_assignment import *

PLAYER_DIVS = {
    "Black Horse's Last Stand": "Descriptor_Deck_US_11ACR_multi_HB_OP_01_DEP_PLAYER",
    "Red Juggernaut": "Descriptor_Deck_SOV_79_Gds_Tank_challenge_OP_03_STR_Player",
    "Backhand Blow": "Descriptor_Deck_US_3rd_Arm_challenge_OP_09_STB_Player",
    "The Kitzingen Ruse": "Descriptor_Deck_SOV_35_AirAslt_Brig_challenge_OP_12_AA_Player",
    "Götterdämmerung": "Descriptor_Deck_RDA_11MSD_challenge_OP_11_RGA_Player",
    "The Dieburg Salient": "Descriptor_Deck_FR_7e_Blindee_challenge_OP_15_LMS_Player",
}

PACK_PREFIX = {
    "Black Horse's Last Stand": "~/Descriptor_Deck_Pack_TOE_US_11ACR_multi_HB_",
    "Red Juggernaut": "~/Descriptor_Deck_Pack_TOE_SOV_79_Gds_Tank_challenge_",
    "Backhand Blow": "~/Descriptor_Deck_Pack_TOE_US_3rd_Arm_challenge_",
    "The Kitzingen Ruse": "~/Descriptor_Deck_Pack_TOE_SOV_35_AirAslt_Brig_challenge_",
    "Götterdämmerung": "~/Descriptor_Deck_Pack_TOE_RDA_11MSD_challenge_",
    "The Dieburg Salient": "~/Descriptor_Deck_Pack_TOE_FR_7e_Blindee_challenge_",
}


# Smart Group Button Size: SkirmishProductionMenuCombatGroupButton in UISpecificSkirmishProductionMenuView.ndf
# (width 120, font size 12)

class OperationEditor(base_napo_page.BaseNapoPage):
    value_changed = QtCore.Signal()

    def __init__(self):
        super().__init__()

        self.op_combobox = wme_essentials.WMECombobox()
        self.op_combobox.addItems(PLAYER_DIVS.keys())
        self.op_combobox.currentIndexChanged.connect(self.on_new_op_selected)

        self.last_op_index = 0
        self.saved_state = None

        self.tool_bar.addSeparator()

        op_selector = QtWidgets.QWidget()
        op_selector_layout = QtWidgets.QHBoxLayout()
        op_selector_layout.setContentsMargins(8, 0, 8, 0)
        op_selector.setLayout(op_selector_layout)
        self.tool_bar.addWidget(op_selector)

        op_selector_layout.addWidget(QtWidgets.QLabel("Operation: "))
        op_selector_layout.addWidget(self.op_combobox)

        self.player_deck_napo = None
        self.player_div_napo = None
        self.deck_pack_list = None
        self.matrix_napo = None

        self.help_file_path = "Help_OperationEditor.html"

        self.open_file(os.path.join(main_widget.instance.get_loaded_mod_path(),
                                    "GameData\\Generated\\Gameplay\\Decks\\Divisions.ndf"))
        self.open_file(os.path.join(main_widget.instance.get_loaded_mod_path(),
                                    "GameData\\Generated\\Gameplay\\Decks\\DivisionRules.ndf"))

        self.update_page()

    def on_new_op_selected(self, index: int):
        if index == self.last_op_index:
            return

        if self.unsaved_changes:
            dialog = essential_dialogs.AskToSaveDialog(self.op_combobox.itemText(self.last_op_index))
            res = dialog.exec()
            if not res:
                self.op_combobox.setCurrentIndex(self.last_op_index)
                return
            elif dialog.save_changes:
                self.save_changes()

        self.last_op_index = index
        self.update_page()

    def update_page(self):
        main_widget.instance.show_loading_screen("Loading operation files...")

        self.clear_layout()

        player_div = PLAYER_DIVS[self.op_combobox.currentText()]
        self.player_deck_napo = self.get_napo_from_object("GameData\\Generated\\Gameplay\\Decks\\Decks.ndf", player_div)
        self.player_div_napo = None
        self.deck_pack_list = self.player_deck_napo.value[0].value.get_napo_value("DeckPackList")
        if not self.matrix_napo:
            self.matrix_napo = self.get_napo_from_file("GameData\\Gameplay\\Decks\\DivisionCostMatrix.ndf")

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
            company_widget = self.add_company(company_name, i + 1)
            platoon_list = company.get_napo_value("SmartGroupList")
            for j in range(len(platoon_list)):
                # get platoon (index/availability mapping)
                platoon = platoon_list.value[j]
                platoon_name = platoon.get_raw_value("Name")
                platoon_packs = platoon.get_napo_value("PackIndexUnitNumberList")
                company_widget.add_platoon(platoon_name, platoon_packs)

        self.saved_state = self.get_state()
        self.unsaved_changes = False

        main_widget.instance.hide_loading_screen()

    def _save_changes(self) -> bool:
        state = self.get_state()
        units_in_deck_list = {}
        company_list = NapoVector()
        all_packs = ndf_scanner.get_assignment_ids("GameData\\Generated\\Gameplay\\Decks\\Packs.ndf")

        for company in state["companies"]:
            company_napo = NapoObject()
            company_napo.obj_type = "TDeckCombatGroupDescriptor"

            company_name_assign = NapoAssignment()
            company_name_assign.member = True
            company_name_assign.id = "Name"
            company_name_assign.value = napo_from_value(company["name"], [NapoDatatype.String_single])
            company_napo.append(company_name_assign)

            platoon_list_assign = NapoAssignment()
            platoon_list_assign.member = True
            platoon_list_assign.id = "SmartGroupList"
            platoon_list_assign.value = NapoVector()
            company_napo.append(platoon_list_assign)

            for platoon in company["platoons"]:
                platoon_napo = NapoObject()
                platoon_napo.obj_type = "TDeckSmartGroupDescriptor"

                platoon_name_assign = NapoAssignment()
                platoon_name_assign.member = True
                platoon_name_assign.id = "Name"
                platoon_name_assign.value = napo_from_value(platoon["name"], [NapoDatatype.String_single])
                platoon_napo.append(platoon_name_assign)

                unit_list_assign = NapoAssignment()
                unit_list_assign.member = True
                unit_list_assign.id = "PackIndexUnitNumberList"
                unit_list_assign.value = NapoVector()
                platoon_napo.append(unit_list_assign)

                for unit in platoon["units"]:
                    units_in_deck_list["~/Descriptor_Unit_" + unit["unit_name"]] = unit

                    index = self.get_index_for_unit(unit)

                    pack_name = PACK_PREFIX[self.op_combobox.currentText()].removeprefix("~/") + unit["unit_name"]
                    if not all_packs.__contains__(pack_name):
                        self.create_pack_for_unit(pack_name, "Descriptor_Unit_" + unit["unit_name"])
                        all_packs.append(pack_name)

                    unit_pair = NapoPair()
                    unit_pair.append(napo_from_value(index, [NapoDatatype.Integer]))
                    unit_pair.append(napo_from_value(unit["count"], [NapoDatatype.Integer]))

                    unit_list_assign.value.append(unit_pair)

                platoon_list_assign.value.append(platoon_napo)

            company_list.append(company_napo)

        division_name = self.player_deck_napo.value[0].value.get_raw_value("DeckDivision")
        self.check_division_rules(units_in_deck_list, division_name)

        self.player_deck_napo.value[0].value.set_napo_value("DeckCombatGroupList", company_list)

        player_div = PLAYER_DIVS[self.op_combobox.currentText()]
        self.write_napo_object("GameData\\Generated\\Gameplay\\Decks\\Decks.ndf", player_div, self.player_deck_napo)

        if self.player_div_napo:
            self.write_napo_object("GameData\\Generated\\Gameplay\\Decks\\Divisions.ndf",
                                   division_name.removeprefix("~/"), self.player_div_napo)
        else:
            self.player_div_napo = self.get_napo_from_object("GameData\\Generated\\Gameplay\\Decks\\Divisions.ndf",
                                                             division_name.removeprefix("~/"))

        # get cost matrix name
        cost_matrix_name = self.player_div_napo.value[0].value.get_raw_value("CostMatrix")

        # create new dummy matrix
        matrix = {}
        matrix_types = []
        categories = ["Logistic", "reco", "infanterie", "tank", "support",
                      "at", "dca", "art", "Helis", "air", "defense"]
        slots = 20

        for cat in categories:
            matrix_types.append(NapoDatatype.Reference)
            matrix["EDefaultFactories/" + cat] = [0] * slots
            for i in range(slots):
                matrix_types.append(NapoDatatype.Integer)

        matrix_types.reverse()

        for i in range(len(self.matrix_napo.value)):
            assign = self.matrix_napo.value[i]
            if assign.id == cost_matrix_name:
                napo_map = napo_from_value(matrix, matrix_types)
                assign.value = napo_map
                self.matrix_napo.value[i] = assign
                break

        self.write_napo_file("GameData\\Gameplay\\Decks\\DivisionCostMatrix.ndf", self.matrix_napo)

        self.saved_state = state
        return True

    def get_index_for_unit(self, unit) -> int:
        deck_pack = NapoObject()
        deck_pack.obj_type = "TDeckPackDescription"

        exp_assign = NapoAssignment()
        exp_assign.id = "ExperienceLevel"
        exp_assign.member = True
        exp_assign.value = napo_from_value(unit["exp"], [NapoDatatype.Integer])
        deck_pack.append(exp_assign)

        pack_assign = NapoAssignment()
        pack_assign.id = "DeckPack"
        pack_assign.member = True
        pack_name = PACK_PREFIX[self.op_combobox.currentText()] + unit["unit_name"]
        pack_assign.value = napo_from_value(pack_name, [NapoDatatype.Reference])
        deck_pack.append(pack_assign)

        if unit["transport"]:
            transport_assign = NapoAssignment()
            transport_assign.id = "Transport"
            transport_assign.member = True
            transport_name = "~/Descriptor_Unit_" + unit["transport"]
            transport_assign.value = napo_from_value(transport_name, [NapoDatatype.Reference])
            deck_pack.append(transport_assign)

        if not self.deck_pack_list.contains(deck_pack):
            self.deck_pack_list.value.append(deck_pack)
            return len(self.deck_pack_list) - 1
        else:
            return self.deck_pack_list.value.index(deck_pack)

    def create_pack_for_unit(self, pack_name: str, unit_name: str):
        pack_assign = NapoAssignment()
        pack_assign.id = pack_name
        pack_descriptor = NapoObject()
        pack_descriptor.obj_type = "TDeckPackDescriptor"
        pack_assign.value = pack_descriptor

        desc_id_assign = NapoAssignment()
        desc_id_assign.member = True
        desc_id_assign.id = "DescriptorId"
        desc_id_assign.value = napo_from_value("GUID:{" + str(uuid.uuid4()) + "}", [NapoDatatype.GUID])
        pack_descriptor.append(desc_id_assign)

        cfg_assign = NapoAssignment()
        cfg_assign.member = True
        cfg_assign.id = "CfgName"
        cfg_assign.value = napo_from_value(pack_name.removeprefix("Descriptor_Deck_Pack_"),
                                           [NapoDatatype.String_single])
        pack_descriptor.append(cfg_assign)

        unit_list_assign = NapoAssignment()
        unit_list_assign.member = True
        unit_list_assign.id = "TransporterAndUnitsList"
        unit_list_assign.value = NapoVector()
        pack_descriptor.append(unit_list_assign)

        unit_desc = NapoObject()
        unit_desc.obj_type = "TDeckTransporterAndUnitsDescriptor"
        unit_list_assign.value.append(unit_desc)

        unit_desc_member = NapoAssignment()
        unit_desc_member.member = True
        unit_desc_member.id = "UnitDescriptor"
        unit_desc_member.value = napo_from_value(unit_name, [NapoDatatype.Reference])
        unit_desc.append(unit_desc_member)

        converter = napo_to_ndf_converter.NapoToNdfConverter()
        pack_text = converter.convert_entity(pack_assign)

        packs_path = main_widget.instance.get_loaded_mod_path() + "\\GameData\\Generated\\Gameplay\\Decks\\Packs.ndf"
        with open(packs_path, "a", encoding="utf-8") as f:
            f.write(pack_text)

        division_name = self.player_deck_napo.value[0].value.get_raw_value("DeckDivision").removeprefix("~/")
        if not self.player_div_napo:
            self.player_div_napo = self.get_napo_from_object("GameData\\Generated\\Gameplay\\Decks\\Divisions.ndf",
                                                             division_name)

        pack_list = self.player_div_napo.value[0].value.get_raw_value("PackList")
        pack_list["~/" + pack_name] = 100

        dtypes = []
        for i in range(len(pack_list)):
            dtypes.append(NapoDatatype.Integer)
            dtypes.append(NapoDatatype.Reference)

        self.player_div_napo.value[0].value.set_raw_value("PackList", pack_list, dtypes)

    def check_division_rules(self, units_in_deck_list: [dict], div_name: str):
        div_rule_text, start, end = ndf_scanner.get_map_value_range(
            "GameData\\Generated\\Gameplay\\Decks\\DivisionRules.ndf", "DivisionRules", div_name)

        # make this an assignment
        div_rule_text = "test is " + div_rule_text

        input_stream = InputStream(div_rule_text)
        lexer = NdfGrammarLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = NdfGrammarParser(stream)
        tree = parser.ndf_file()

        listener = napo_generator.NapoGenerator(parser)
        walker = ParseTreeWalker()
        walker.walk(listener, tree)

        pair_napo = listener.assignments[0].value
        list_napo = pair_napo.value[1].get_napo_value("UnitRuleList")

        for entry in list_napo.value:
            unit_name = entry.get_raw_value("UnitDescriptor")
            entry.set_raw_value("NumberOfUnitInPack", 9999, [NapoDatatype.Integer])
            try:
                transport_list = entry.get_raw_value("AvailableTransportList")
            except:
                transport_list = None

            if units_in_deck_list.__contains__(unit_name):
                unit_info = units_in_deck_list.pop(unit_name)
                # add transport to list
                if unit_info["transport"]:
                    if transport_list:
                        if not transport_list.__contains__("~/Descriptor_Unit_" + unit_info["transport"]):
                            transport_list.append("~/Descriptor_Unit_" + unit_info["transport"])
                    else:
                        transport_list = ["~/Descriptor_Unit_" + unit_info["transport"]]
                    entry.set_raw_value("AvailableTransportList", transport_list,
                                        len(transport_list) * [NapoDatatype.Reference])
                    entry.set_raw_value("AvailableWithoutTransport", False, [NapoDatatype.Boolean])
                else:
                    entry.set_raw_value("AvailableWithoutTransport", True, [NapoDatatype.Boolean])

        for unit_info in units_in_deck_list.values():
            entry = NapoObject()
            entry.obj_type = "TDeckUniteRule"

            unit_assign = NapoAssignment()
            unit_assign.id = "UnitDescriptor"
            unit_assign.member = True
            unit_assign.value = napo_from_value("~/Descriptor_Unit_" + unit_info["unit_name"], [NapoDatatype.Reference])
            entry.append(unit_assign)

            avail_assign = NapoAssignment()
            avail_assign.id = "AvailableWithoutTransport"
            avail_assign.member = True
            avail_assign.value = napo_from_value(False if unit_info["transport"] else True, [NapoDatatype.Boolean])
            entry.append(avail_assign)

            if unit_info["transport"]:
                transport_assign = NapoAssignment()
                transport_assign.id = "AvailableTransportList"
                transport_assign.member = True
                transport_assign.value = napo_from_value(["~/Descriptor_Unit_" + unit_info["transport"]],
                                                         [NapoDatatype.Reference])
                entry.append(transport_assign)

            num_pack_assign = NapoAssignment()
            num_pack_assign.id = "NumberOfUnitInPack"
            num_pack_assign.member = True
            num_pack_assign.value = napo_from_value(9999, [NapoDatatype.Integer])
            entry.append(num_pack_assign)

            exp_assign = NapoAssignment()
            exp_assign.id = "NumberOfUnitInPackXPMultiplier"
            exp_assign.member = True
            exp_assign.value = napo_from_value(4 * [1.0], 4 * [NapoDatatype.Float])
            entry.append(exp_assign)

            list_napo.value.append(entry)

        # rebuild napo
        pair_napo.value[1].set_napo_value("UnitRuleList", list_napo)

        file_path = os.path.join(main_widget.instance.get_loaded_mod_path(),
                                 "GameData\\Generated\\Gameplay\\Decks\\DivisionRules.ndf")
        converter = napo_to_ndf_converter.NapoToNdfConverter()
        ndf_text = converter.convert_entity(pair_napo)

        with open(file_path, "r", encoding="utf-8") as f:
            file_content = f.read()

        file_content = ndf_text.join([file_content[:start], file_content[end:]])
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(file_content)

    def add_company(self, company_name: str, index: int):
        company_widget = unit_widgets.UnitCompanyWidget(company_name, index, self)
        company_widget.delete_company.connect(self.on_delete_company)
        company_widget.value_changed.connect(self.on_value_changed)
        self.scroll_layout.insertWidget(self.scroll_layout.count() - 2, company_widget)
        return company_widget

    def on_add_company(self):
        self.add_company("", self.scroll_layout.count() - 1)
        self.on_value_changed()

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

    def get_state(self):
        companies = []
        for i in range(self.scroll_layout.count() - 2):
            company = self.scroll_layout.itemAt(i).widget()
            companies.append(company.get_state())

        return {
            "current_op": self.op_combobox.currentText(),
            "companies": companies
        }

    def set_state(self, state: dict):
        self.op_combobox.currentIndexChanged.disconnect(self.on_new_op_selected)
        self.op_combobox.setCurrentIndex(self.op_combobox.findText(state["current_op"]))
        self.op_combobox.currentIndexChanged.connect(self.on_new_op_selected)

        self.clear_layout()

        player_div = PLAYER_DIVS[self.op_combobox.currentText()]
        self.player_deck_napo = self.get_napo_from_object("GameData\\Generated\\Gameplay\\Decks\\Decks.ndf", player_div)
        self.player_div_napo = None
        self.deck_pack_list = self.player_deck_napo.value[0].value.get_napo_value("DeckPackList")

        add_company_button = QtWidgets.QPushButton("Add Company")
        add_company_button.clicked.connect(self.on_add_company)
        add_company_button.setFixedWidth(400)
        self.scroll_layout.addWidget(add_company_button)
        self.scroll_layout.setAlignment(add_company_button, Qt.AlignCenter)
        self.scroll_layout.addStretch(1)

        index = 1
        for company in state["companies"]:
            company_widget = self.add_company(company["name"], index)
            index += 1
            for platoon in company["platoons"]:
                platoon_widget = company_widget.add_platoon(platoon["name"], NapoVector())
                unit_index = 0
                for unit in platoon["units"]:
                    platoon_widget.add_unit_with_data(unit_index, unit["count"], unit["exp"], unit["unit_name"],
                                                      unit["transport"])
                    unit_index += 1

        self.unsaved_changes = self.saved_state != state
        # TODO: why is page updated here?

    def get_state_file_name(self) -> str:
        operation_name = self.op_combobox.currentText()
        operation_name = operation_name.replace(" ", "")
        operation_name = operation_name.replace("'", "")
        return operation_name

    def to_json(self) -> dict:
        page_json = {"currentOp": self.op_combobox.currentText()}
        return page_json

    def from_json(self, json_obj: dict):
        self.op_combobox.setCurrentIndex(self.op_combobox.findText(json_obj["currentOp"]))

    def on_value_changed(self):
        new_status = self.get_state()
        self.unsaved_changes = new_status != self.saved_state
