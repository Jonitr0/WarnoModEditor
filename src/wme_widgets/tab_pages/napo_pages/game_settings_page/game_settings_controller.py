from src.wme_widgets.tab_pages.napo_pages import base_napo_controller

from src.utils.parser_utils import *


class GameSettingsController(base_napo_controller.BaseNapoController):
    def write_state_to_file(self, state: dict):
        dest_table = {}
        for val in state["starting_points"]:
            dest_table[val] = state["destruction_scores"]

        gdc_file_obj = self.get_parsed_ndf_file("GameData\\Gameplay\\Constantes\\GDConstantes.ndf")
        for obj_row in gdc_file_obj:
            obj = obj_row.value

            if obj_row.namespace == "WargameConstantes":
                obj.by_member("ArgentInitialSetting").value = py_list_to_parsed_list(state["starting_points"])
                obj.by_member("DefaultArgentInitial").value = str(state["default_starting_points"])
                obj.by_member("ConquestPossibleScores").value = py_list_to_parsed_list(state["conquest_scores"])
                obj.by_member("DestructionScoreToReachSetting").value = \
                    py_list_to_parsed_list(state["destruction_scores"])
                obj.by_member("VictoryTypeDestructionLevelsTable").value = py_map_to_parsed_map(dest_table)
                obj.by_member("BaseIncome").value.by_key("CombatRule/Conquest").value = str(state["conquest_income"])
                obj.by_member("BaseIncome").value.by_key("CombatRule/Destruction").value = \
                    str(state["destruction_income"])
                obj.by_member("TimeBeforeEarningCommandPoints").value.by_key("CombatRule/Conquest").value = \
                    str(state["conquest_tick"])
                obj.by_member("TimeBeforeEarningCommandPoints").value.by_key("CombatRule/Destruction").value = \
                    str(state["destruction_tick"])

        # write to file
        self.save_files_to_mod({"GameData\\Gameplay\\Constantes\\GDConstantes.ndf": gdc_file_obj})

    def load_state_from_file(self) -> dict:
        gdc_file_obj = self.get_parsed_ndf_file("GameData\\Gameplay\\Constantes\\GDConstantes.ndf")
        self.delete_tmp_mod()
        for obj_row in gdc_file_obj:
            obj = obj_row.value

            if obj_row.namespace == "WargameConstantes":
                state = {
                    "starting_points": parsed_list_to_py_list(obj.by_member("ArgentInitialSetting"), str),
                    "conquest_tick": float(obj.by_member("TimeBeforeEarningCommandPoints").value.by_key(
                        "CombatRule/Conquest").value),
                    "conquest_income": int(obj.by_member("BaseIncome").value.by_key("CombatRule/Conquest").value),
                    "conquest_scores": parsed_list_to_py_list(obj.by_member("ConquestPossibleScores"), str),
                    "destruction_tick": float(obj.by_member("TimeBeforeEarningCommandPoints").value.by_key(
                        "CombatRule/Destruction").value),
                    "destruction_income": int(obj.by_member("BaseIncome").value.by_key("CombatRule/Destruction").value),
                    "destruction_scores": parsed_list_to_py_list(obj.by_member("DestructionScoreToReachSetting"),
                                                                 str),
                    "default_starting_points": str(obj.by_member("DefaultArgentInitial").value),
                }

        return state
