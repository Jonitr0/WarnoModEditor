from src.wme_widgets.tab_pages.napo_pages import base_napo_controller
from src.wme_widgets.tab_pages.napo_pages.operation_editor import unit_widgets

from src.utils import ndf_scanner


class OperationEditorController(base_napo_controller.BaseNapoController):
    def __init__(self):
        super().__init__()
        
        self.player_deck_obj = None
        self.player_div_obj = None
        self.deck_pack_list = None
        self.current_op = ""
        self.current_player_div = ""

    def set_current_op(self, op: str):
        self.current_op = op

    def set_current_player_div(self, player_div: str):
        self.current_player_div = player_div

    def load_state_from_file(self) -> dict:
        # Decks.ndf: get units in battle group
        # DeckRules.ndf: get enemy units
        player_div = self.current_player_div
        self.player_deck_obj = self.get_parsed_object_from_ndf_file("GameData\\Generated\\Gameplay\\Decks\\Decks.ndf",
                                                                    player_div)
        self.player_div_obj = None
        self.deck_pack_list = self.player_deck_obj.by_member("DeckPackList").value

        units = sorted([i.removeprefix("Descriptor_Unit_") for i in
                        ndf_scanner.get_assignment_ids("GameData\\Generated\\Gameplay\\Gfx\\UniteDescriptor.ndf")])
        unit_widgets.UnitSelectionCombobox.units = units

        state = {"current_op": self.current_op, "companies": []}

        # get group list
        company_list = self.player_deck_obj.by_member("DeckCombatGroupList").value
        for i in range(len(company_list)):
            # get unit object
            company = company_list[i].value
            company_name = company.by_member("Name").value
            company_dict = {"name": company_name, "platoons": []}
            platoon_list = company.by_member("SmartGroupList").value
            for j in range(len(platoon_list)):
                # get platoon (index/availability mapping)
                platoon = platoon_list[j].value
                platoon_name = platoon.by_member("Name").value
                platoon_dict = {"name": platoon_name, "units": []}
                platoon_packs = platoon.by_member("PackIndexUnitNumberList").value
                for pack in platoon_packs:
                    # TODO: get pack data from parsed obj
                    # key: index in DeckPackList
                    # value: amount
                    pass
                company_dict["platoons"].append(platoon_dict)
            state["companies"].append(company_dict)

        # TODO: enemy BGs
        return state

    def write_state_to_file(self, state: dict):
        # Decks.ndf: save units in battle group
        # DeckRules.ndf: save enemy units
        # DivisionCostMatrix.ndf: adjust if needed
        # Packs.ndf: save availability constraints
        # Divisions.ndf: ?
        # DivisionRules.ndf: ?
        pass
