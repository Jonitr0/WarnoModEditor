import logging
import uuid

import ndf_parse

from src.wme_widgets.tab_pages.napo_pages import base_napo_controller
from src.wme_widgets.tab_pages.napo_pages.operation_editor import unit_widgets

from src.utils import ndf_scanner

PACK_PREFIX = {
    "Black Horse's Last Stand": "TOE_US_11ACR_multi_HB_",
    "Red Juggernaut": "TOE_SOV_79_Gds_Tank_challenge_",
    "Backhand Blow": "TOE_US_3rd_Arm_challenge_",
    "The Kitzingen Ruse": "TOE_SOV_35_AirAslt_Brig_challenge_",
    "Götterdämmerung": "TOE_RDA_11MSD_challenge_",
    "The Dieburg Salient": "TOE_FR_7e_Blindee_challenge_",
    "Hold Until Relieved": "TOE_UK_Blues_Royals_challenge_",
    # TODO: Sledgehammer
}


class OperationEditorController(base_napo_controller.BaseNapoController):
    def __init__(self):
        super().__init__()

        self.player_deck_obj = None
        self.div_rules_obj = None
        self.deck_pack_list = None
        self.packs = None
        self.current_op = ""
        self.current_player_div = ""
        self.current_enemy_divs = []

    def set_current_op(self, op: str):
        self.current_op = op

    def set_current_player_div(self, player_div: str):
        self.current_player_div = player_div

    def set_current_enemy_divs(self, enemy_divs: [str]):
        self.current_enemy_divs = enemy_divs

    def load_state_from_file(self) -> dict:
        player_div = self.current_player_div
        self.player_deck_obj = self.get_parsed_object_from_ndf_file("GameData\\Generated\\Gameplay\\Decks\\Decks.ndf",
                                                                    player_div)
        self.deck_pack_list = self.player_deck_obj.by_member("DeckPackList").value
        self.packs = self.get_parsed_ndf_file("GameData\\Generated\\Gameplay\\Decks\\Packs.ndf")

        units = sorted([i.removeprefix("Descriptor_Unit_") for i in
                        ndf_scanner.get_assignment_ids("GameData\\Generated\\Gameplay\\Gfx\\UniteDescriptor.ndf")])
        unit_widgets.UnitSelectionCombobox.units = units

        state = {"current_op": self.current_op, "companies": [], "enemy_divs": []}
        deck_pack_list = self.player_deck_obj.by_member("DeckPackList").value

        # get group list
        company_list = self.player_deck_obj.by_member("DeckCombatGroupList").value
        for i in range(len(company_list)):
            # get unit object
            company = company_list[i].value
            company_name = company.by_member("Name").value.replace("\"", "")
            company_dict = {"name": company_name, "platoons": []}
            platoon_list = company.by_member("SmartGroupList").value
            for j in range(len(platoon_list)):
                # get platoon (index/availability mapping)
                platoon = platoon_list[j].value
                platoon_name = platoon.by_member("Name").value.replace("\"", "")
                platoon_dict = {"name": platoon_name, "units": []}
                platoon_packs = platoon.by_member("PackIndexUnitNumberList").value
                for pack in platoon_packs:
                    index = int(pack.value[0])
                    unit_info = self.get_unit_info_from_pack(index, deck_pack_list)
                    unit_info["count"] = int(pack.value[1])
                    platoon_dict["units"].append(unit_info)
                company_dict["platoons"].append(platoon_dict)
            state["companies"].append(company_dict)

        # enemy BGs
        self.div_rules_obj = None
        enemy_divs = self.current_enemy_divs
        for enemy_div in enemy_divs:
            enemy_div_obj = self.get_parsed_object_from_ndf_file(
                "GameData\\Generated\\Gameplay\\Decks\\Decks.ndf", enemy_div)
            enemy_div_name = enemy_div_obj.by_member("DeckDivision").value
            enemy_div_dict = {"name": enemy_div, "units": []}
            enemy_div_pack_list = enemy_div_obj.by_member("DeckPackList").value
            for i in range(len(enemy_div_pack_list)):
                unit = self.get_unit_info_from_pack(i, enemy_div_pack_list)
                unit["count"] = self.get_count_form_div_rules(unit["unit_name"], enemy_div_name)
                enemy_div_dict["units"].append(unit)
            state["enemy_divs"].append(enemy_div_dict)
        return state

    def get_unit_info_from_pack(self, pack_index: int, deck_pack_list: ndf_parse.List) -> dict:
        pack = deck_pack_list[pack_index].value
        pack_name = pack.by_member("DeckPack").value.removeprefix("~/")
        unit_name = ""
        for pack_info in self.packs:
            if pack_info.namespace == pack_name:
                unit_name = pack_info.value.by_member("TransporterAndUnitsList").value[0].value. \
                    by_member("UnitDescriptor").value.removeprefix("$/GFX/Unit/Descriptor_Unit_")
                break
        if unit_name == "":
            logging.warning(f"Could not find unit name for pack {pack_name}")
        exp = int(pack.by_member("ExperienceLevel").value)
        try:
            transport = pack.by_member("Transport").value
            transport = transport.removeprefix("$/GFX/Unit/Descriptor_Unit_")
        except ValueError:
            transport = None
        return {"unit_name": unit_name, "exp": exp, "transport": transport}

    def get_count_form_div_rules(self, unit_name: str, div_name: str) -> int:
        if not self.div_rules_obj:
            div_rules = self.get_parsed_object_from_ndf_file(
                "GameData\\Generated\\Gameplay\\Decks\\DivisionRules.ndf", "DivisionRules")
            self.div_rules_obj = div_rules.by_member("DivisionRules").value

        div_unit_list = self.div_rules_obj.by_key(div_name).value.by_member("UnitRuleList").value
        for unit in div_unit_list:
            if unit.value.by_member("UnitDescriptor").value == "$/GFX/Unit/Descriptor_Unit_" + unit_name:
                return int(unit.value.by_member("NumberOfUnitInPack").value)

        logging.warning("Unit " + unit_name + " not found for " + div_name + " in DivisionRules.ndf")
        return 0

    def write_state_to_file(self, state: dict):
        # Decks.ndf: save units in battle group
        self.write_decks_ndf(state)
        # DeckRules.ndf: save enemy units
        # TODO: check if cost matrix file has changed
        # DivisionCostMatrix.ndf: adjust if needed
        # Packs.ndf: save availability constraints
        # TODO: set operation cost matrix, not MP matrix
        # Divisions.ndf: add packs of added units, adjust pack counts
        # DivisionRules.ndf: save enemy unit counts
        # save all files once all changes have been applied
        decks = self.get_parsed_ndf_file("GameData\\Generated\\Gameplay\\Decks\\Decks.ndf")
        for i, deck in enumerate(decks):
            if deck.namespace == self.current_player_div:
                decks[i].value = self.player_deck_obj
                break

        files = {
            "GameData\\Generated\\Gameplay\\Decks\\Decks.ndf": decks,
            "GameData\\Generated\\Gameplay\\Decks\\Packs.ndf": self.packs,
        }

        self.save_files_to_mod(files)

    def write_decks_ndf(self, state: dict):
        # get list of all units
        all_units = []
        for company in state["companies"]:
            for platoon in company["platoons"]:
                for unit in platoon["units"]:
                    all_units.append(unit)
        pack_list = ndf_parse.model.List()
        pack_indices = {}
        self.packs = self.get_parsed_ndf_file("GameData\\Generated\\Gameplay\\Decks\\Packs.ndf")
        for unit in all_units:
            key = str(unit["unit_name"]) + str(unit["exp"]) + str(unit["transport"])
            if key in pack_indices:
                continue
            pack_name = "Descriptor_Deck_Pack_" + PACK_PREFIX[self.current_op] + unit["unit_name"]
            # create pack if it does not already exist
            if not any(pack.namespace == pack_name for pack in self.packs):
                self.create_pack(pack_name, unit["unit_name"])
            pack_text = "TDeckPackDescription( ExperienceLevel = " + str(unit["exp"]) + "\nDeckPack = ~/" + pack_name
            if unit["transport"]:
                pack_text += ("\nTransport = $/GFX/Unit/Descriptor_Unit_" + unit["transport"])
            pack_text += ")"
            pack_dict = ndf_parse.expression(pack_text)
            pack_list.add(**pack_dict)
            pack_indices[key] = len(pack_list) - 1
        self.player_deck_obj.by_member("DeckPackList").value = pack_list

        company_list = ndf_parse.model.List()
        for company in state["companies"]:
            company_name = company["name"]
            company_text = "TDeckCombatGroupDescriptor (Name = \"" + company_name + "\"\nSmartGroupList = [])"
            company_dict = ndf_parse.expression(company_text)
            company_list.add(**company_dict)
            for platoon in company["platoons"]:
                platoon_name = platoon["name"]
                platoon_text = "TDeckSmartGroupDescriptor (Name = \"" + platoon_name + "\"\nPackIndexUnitNumberList = [])"
                platoon_dict = ndf_parse.expression(platoon_text)
                company_list[-1].value.by_member("SmartGroupList").value.add(**platoon_dict)
                for unit in platoon["units"]:
                    key = str(unit["unit_name"]) + str(unit["exp"]) + str(unit["transport"])
                    unit_index = pack_indices[key]
                    unit_text = "(" + str(unit_index) + "," + str(unit["count"]) + ")"
                    unit_dict = ndf_parse.expression(unit_text)
                    (company_list[-1].value.by_member("SmartGroupList").value[-1].value.
                     by_member("PackIndexUnitNumberList").value.add(**unit_dict))
        self.player_deck_obj.by_member("DeckCombatGroupList").value = company_list

    def create_pack(self, pack_name: str, unit_name: str):
        pack_text = (pack_name + " is TDeckPackDescriptor ( DescriptorId = GUID:{" + str(uuid.uuid4()) +
                     "}\nCfgName = \'" + PACK_PREFIX[self.current_op] + unit_name + "\'\nTransporterAndUnitsList = [ "
                     "TDeckTransporterAndUnitsDescriptor (UnitDescriptor = $/GFX/Unit/Descriptor_Unit_" + unit_name +
                     "), ] )")
        pack_dict = ndf_parse.expression(pack_text)
        self.packs.add(**pack_dict)
