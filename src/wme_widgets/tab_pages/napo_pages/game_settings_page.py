import logging
import os.path

from PySide6 import QtWidgets, QtCore

from src.wme_widgets import main_widget, wme_essentials
from src.wme_widgets.tab_pages.napo_pages import base_napo_page
from src.wme_widgets.tab_pages.napo_pages import napo_list_widget

from src.ndf_parser.napo_entities.napo_entity import *


class GameSettingsPage(base_napo_page.BaseNapoPage):
    def __init__(self):
        super().__init__()
        self.destruction_income_widget = BaseIncomeWidget(self, "Destruction base income: ")
        self.conquest_income_widget = BaseIncomeWidget(self, "Conquest base income: ")
        self.starting_pts_list_widget = napo_list_widget.NapoListWidget("Starting Points in Skirmish and Multiplayer",
                                                                        "\\d+", fixed_length=True)
        self.conquest_score_list_widget = napo_list_widget.NapoListWidget("Conquest Scores", "\\d+")
        self.destruction_score_list_widget = napo_list_widget.NapoListWidget(
            "Destruction Scores", "\\d+", fixed_length=True)
        self.constants_napo = None
        self.saved_state = None

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

        self.help_file_path = "Help_GameSettingsEditor.html"

    def update_page(self):
        main_widget.instance.show_loading_screen("loading GDConstantes.ndf...")

        self.constants_napo = self.get_napo_from_file("GameData\\Gameplay\\Constantes\\GDConstantes.ndf")
        self.saved_state = {
            "starting_points": self.constants_napo.get_raw_value("WargameConstantes\\ArgentInitialSetting"),
            "conquest_tick": self.constants_napo.get_raw_value(
                "WargameConstantes\\TimeBeforeEarningCommandPoints\\CombatRule/CaptureTheFlag"),
            "conquest_income": self.constants_napo.get_raw_value(
                "WargameConstantes\\BaseIncome\\CombatRule/CaptureTheFlag"),
            "conquest_scores": self.constants_napo.get_raw_value("WargameConstantes\\ConquestPossibleScores"),
            "destruction_tick": self.constants_napo.get_raw_value(
                "WargameConstantes\\TimeBeforeEarningCommandPoints\\CombatRule/Destruction"),
            "destruction_income": self.constants_napo.get_raw_value(
                "WargameConstantes\\BaseIncome\\CombatRule/Destruction"),
            "destruction_scores": self.constants_napo.get_raw_value(
                "WargameConstantes\\DestructionScoreToReachSetting"),
            "default_starting_points": self.constants_napo.get_raw_value("WargameConstantes\\DefaultArgentInitial"),
        }

        self.set_state(self.saved_state)

        main_widget.instance.hide_loading_screen()

    def _save_changes(self) -> bool:
        state = self.get_state()

        dest_table = {}
        dest_types = [NapoDatatype.Integer] * (len(state["destruction_scores"]) + 1) * len(state["destruction_scores"])
        for val in state["starting_points"]:
            dest_table[val] = state["destruction_scores"]

        self.constants_napo.set_raw_value("WargameConstantes\\ArgentInitialSetting", state["starting_points"],
                                          len(state["starting_points"]) * [NapoDatatype.Integer])
        self.constants_napo.set_raw_value("WargameConstantes\\DefaultArgentInitial", state["default_starting_points"],
                                          [NapoDatatype.Integer])
        self.constants_napo.set_raw_value("WargameConstantes\\ConquestPossibleScores", state["conquest_scores"],
                                          len(state["conquest_scores"]) * [NapoDatatype.Integer])
        self.constants_napo.set_raw_value("WargameConstantes\\DestructionScoreToReachSetting",
                                          state["destruction_scores"], len(state["destruction_scores"]) *
                                          [NapoDatatype.Integer])
        self.constants_napo.set_raw_value("WargameConstantes\\VictoryTypeDestructionLevelsTable", dest_table,
                                          dest_types)
        self.constants_napo.set_raw_value("WargameConstantes\\BaseIncome\\CombatRule/CaptureTheFlag",
                                          state["conquest_income"], [NapoDatatype.Integer])
        self.constants_napo.set_raw_value(
            "WargameConstantes\\TimeBeforeEarningCommandPoints\\CombatRule/CaptureTheFlag",
            state["conquest_tick"], [NapoDatatype.Float])
        self.constants_napo.set_raw_value("WargameConstantes\\BaseIncome\\CombatRule/Destruction",
                                          state["destruction_income"], [NapoDatatype.Integer])
        self.constants_napo.set_raw_value(
            "WargameConstantes\\TimeBeforeEarningCommandPoints\\CombatRule/Destruction",
            state["destruction_tick"], [NapoDatatype.Float])

        # write to file
        self.write_napo_file("GameData\\Gameplay\\Constantes\\GDConstantes.ndf", self.constants_napo)

        self.saved_state = state

        return True

    def on_state_changed(self):
        if self.saved_state != self.get_state():
            self.unsaved_changes = True

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

    def set_state(self, state: dict):
        self.starting_pts_list_widget.update_list(state["starting_points"])
        self.conquest_score_list_widget.update_list(state["conquest_scores"])
        destruction_scores = state["destruction_scores"]
        if destruction_scores.__contains__(0):
            destruction_scores.remove(0)
        self.destruction_score_list_widget.update_list(destruction_scores)

        self.conquest_income_widget.set_values(state["conquest_income"], state["conquest_tick"])
        self.destruction_income_widget.set_values(state["destruction_income"],
                                                  state["destruction_tick"])

        self.unsaved_changes = state != self.saved_state

    def get_state_file_name(self) -> str:
        return "GameSettings"


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
