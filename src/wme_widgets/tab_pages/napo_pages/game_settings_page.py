from PySide6 import QtWidgets, QtCore

from src.wme_widgets import main_widget, wme_essentials, wme_list_widget
from src.wme_widgets.tab_pages.napo_pages import base_napo_page

from src.utils.parser_utils import *


class GameSettingsPage(base_napo_page.BaseNapoPage):
    def __init__(self):
        super().__init__()
        self.destruction_income_widget = BaseIncomeWidget(self, "Destruction base income: ")
        self.conquest_income_widget = BaseIncomeWidget(self, "Conquest base income: ")
        self.starting_pts_list_widget = wme_list_widget.WMEListWidget("Starting Points in Skirmish and Multiplayer",
                                                                        "\\d+", fixed_length=True)
        self.conquest_score_list_widget = wme_list_widget.WMEListWidget("Conquest Scores", "\\d+")
        self.destruction_score_list_widget = wme_list_widget.WMEListWidget(
            "Destruction Scores", "\\d+", fixed_length=True)

        self.add_help_button()

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(scroll_area)

        scroll_widget = QtWidgets.QWidget()
        scroll_area.setWidget(scroll_widget)
        self.scroll_layout = QtWidgets.QVBoxLayout()
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_widget.setLayout(self.scroll_layout)

        self.scroll_layout.addWidget(self.starting_pts_list_widget)
        self.scroll_layout.addWidget(self.conquest_score_list_widget)
        self.scroll_layout.addWidget(self.conquest_income_widget)
        self.scroll_layout.addWidget(self.destruction_score_list_widget)
        self.scroll_layout.addWidget(self.destruction_income_widget)

        self.scroll_layout.addStretch(1)

        self.update_page()

        # connect slots
        self.starting_pts_list_widget.list_updated.connect(self.on_state_changed)
        self.conquest_score_list_widget.list_updated.connect(self.on_state_changed)
        self.conquest_income_widget.value_changed.connect(self.on_state_changed)
        self.destruction_score_list_widget.list_updated.connect(self.on_state_changed)
        self.destruction_income_widget.value_changed.connect(self.on_state_changed)

        self.help_file_path = "Help_GameSettingsEditor.md"

    def get_state(self):
        starting_points = self.starting_pts_list_widget.list_widget.all_item_labels()
        conquest_scores = self.conquest_score_list_widget.list_widget.all_item_labels()
        destruction_scores = self.destruction_score_list_widget.list_widget.all_item_labels()
        destruction_scores.append("0")

        conquest_income, conquest_tick = self.conquest_income_widget.get_values()
        destruction_income, destruction_tick = self.destruction_income_widget.get_values()

        default_starting_points = starting_points[0]
        if starting_points.__contains__("1500"):
            default_starting_points = "1500"
        elif len(starting_points) > 2:
            default_starting_points = starting_points[2]

        return {
            "starting_points": starting_points,
            "conquest_tick": conquest_tick,
            "conquest_income": conquest_income,
            "conquest_scores": conquest_scores,
            "destruction_tick": destruction_tick,
            "destruction_income": destruction_income,
            "destruction_scores": destruction_scores,
            "default_starting_points": default_starting_points,
        }

    def _set_state(self, state: dict):
        self.starting_pts_list_widget.update_list(state["starting_points"])
        self.conquest_score_list_widget.update_list(state["conquest_scores"])
        destruction_scores = state["destruction_scores"].copy()
        if destruction_scores.__contains__("0"):
            destruction_scores.remove("0")
        self.destruction_score_list_widget.update_list(destruction_scores)

        self.conquest_income_widget.set_values(state["conquest_income"], state["conquest_tick"])
        self.destruction_income_widget.set_values(state["destruction_income"],
                                                  state["destruction_tick"])

        self.unsaved_changes = state != self.saved_state

    def get_state_file_name(self) -> str:
        return "GameSettings"

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
                for k, v in dest_table.items():
                    new_v = []
                    for entry in v:
                        new_v.append(int(entry))
                    dest_table[k] = new_v
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


class BaseIncomeWidget(QtWidgets.QWidget):
    value_changed = QtCore.Signal(int, float)

    def __init__(self, parent: QtWidgets.QWidget = None, label_text: str = ""):
        super().__init__(parent)

        main_layout = QtWidgets.QHBoxLayout()
        self.setLayout(main_layout)

        main_layout.addWidget(QtWidgets.QLabel(label_text))
        self.points_spin_box = wme_essentials.WMESpinbox()
        self.points_spin_box.setRange(0, 10000)
        self.points_spin_box.valueChanged.connect(self.on_value_changed)
        main_layout.addWidget(self.points_spin_box)

        main_layout.addWidget(QtWidgets.QLabel(" points every "))
        self.tick_spin_box = wme_essentials.WMEDoubleSpinbox()
        self.tick_spin_box.setRange(0.01, 36000.)
        self.tick_spin_box.valueChanged.connect(self.on_value_changed)
        main_layout.addWidget(self.tick_spin_box)

        main_layout.addWidget(QtWidgets.QLabel(" seconds"))
        main_layout.addStretch(1)

    def set_values(self, income: int, tick: float):
        self.points_spin_box.setValue(income)
        self.tick_spin_box.setValue(tick)

    def get_values(self):
        return int(self.points_spin_box.text()), float(self.tick_spin_box.text().replace(",", "."))

    def on_value_changed(self, _):
        income, tick = self.get_values()
        self.value_changed.emit(income, tick)
