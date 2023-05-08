import logging
import os

from PySide6 import QtWidgets, QtCore, QtGui

from src.wme_widgets import main_widget
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
        self.starting_points = []
        self.conquest_scores = []
        self.destruction_scores = []
        self.conquest_income = 0
        self.conquest_tick = 0.
        self.destruction_income = 0
        self.destruction_tick = 0.

        self.scroll_layout.addWidget(self.starting_pts_list_widget)
        self.scroll_layout.addWidget(self.conquest_score_list_widget)
        self.scroll_layout.addWidget(self.conquest_income_widget)
        self.scroll_layout.addWidget(self.destruction_score_list_widget)
        self.scroll_layout.addWidget(self.destruction_income_widget)

        self.scroll_layout.addStretch(1)

        self.update_page()

        # connect slots
        self.starting_pts_list_widget.list_updated.connect(self.on_starting_points_changed)
        self.conquest_score_list_widget.list_updated.connect(self.on_conquest_scores_changed)
        self.conquest_income_widget.value_changed.connect(self.on_conquest_income_changed)
        self.destruction_score_list_widget.list_updated.connect(self.on_destruction_scores_changed)
        self.destruction_income_widget.value_changed.connect(self.on_destruction_income_changed)

        self.help_file_path = "Help_GameSettingsEditor.html"

    def update_page(self):
        main_widget.MainWidget.instance.show_loading_screen("loading GDConstantes.ndf...")

        file_path = os.path.join(main_widget.MainWidget.instance.get_loaded_mod_path(),
                                 "GameData\\Gameplay\\Constantes\\GDConstantes.ndf")

        self.constants_napo = self.get_napo_from_file(file_path)

        self.starting_points = self.constants_napo.get_value("WargameConstantes\\ArgentInitialSetting")
        self.starting_pts_list_widget.update_list(self.starting_points)
        self.conquest_scores = self.constants_napo.get_value("WargameConstantes\\ConquestPossibleScores")
        self.conquest_score_list_widget.update_list(self.conquest_scores)
        self.destruction_scores = self.constants_napo.get_value("WargameConstantes\\DestructionScoreToReachSetting")
        destruction_scores = self.destruction_scores
        destruction_scores.remove(0)
        self.destruction_score_list_widget.update_list(destruction_scores)

        self.conquest_income = self.constants_napo.get_value("WargameConstantes\\BaseIncome\\CombatRule/CaptureTheFlag")
        self.conquest_tick = self.constants_napo.get_value(
            "WargameConstantes\\TimeBeforeEarningCommandPoints\\CombatRule/CaptureTheFlag")
        self.conquest_income_widget.set_values(self.conquest_income, self.conquest_tick)

        self.destruction_income = self.constants_napo.get_value("WargameConstantes\\BaseIncome\\CombatRule/Destruction")
        self.destruction_tick = self.constants_napo.get_value(
            "WargameConstantes\\TimeBeforeEarningCommandPoints\\CombatRule/Destruction")
        self.destruction_income_widget.set_values(self.destruction_income, self.destruction_tick)

        main_widget.MainWidget.instance.hide_loading_screen()

    def on_starting_points_changed(self, starting_points: [str]):
        # convert to int list
        starting_points = [int(i) for i in starting_points]
        if self.starting_points != starting_points:
            self.unsaved_changes = True

    def on_conquest_scores_changed(self, conquest_scores: [str]):
        # convert to int list
        conquest_scores = [int(i) for i in conquest_scores]
        if self.conquest_scores != conquest_scores:
            self.unsaved_changes = True

    def on_destruction_scores_changed(self, destruction_scores: [str]):
        # convert to int list
        destruction_scores = [int(i) for i in destruction_scores]
        destruction_scores.append(0)
        if self.destruction_scores != destruction_scores:
            self.unsaved_changes = True

    def on_conquest_income_changed(self, conquest_income: int, conquest_tick: float):
        if self.conquest_income != conquest_income or self.conquest_tick != conquest_tick:
            self.unsaved_changes = True

    def on_destruction_income_changed(self, destruction_income: int, destruction_tick: float):
        if self.destruction_income != destruction_income or self.destruction_tick != destruction_tick:
            self.unsaved_changes = True

    def _save_changes(self) -> bool:
        try:
            starting_points = self.starting_pts_list_widget.list_widget.all_item_labels()
            conquest_scores = self.conquest_score_list_widget.list_widget.all_item_labels()
            destruction_scores = self.destruction_score_list_widget.list_widget.all_item_labels()
            destruction_scores.append("0")

            conquest_income, conquest_tick = self.conquest_income_widget.get_values()
            dest_income, dest_tick = self.destruction_income_widget.get_values()

            default_starting_points = starting_points[0]
            if starting_points.__contains__("1500"):
                default_starting_points = "1500"
            elif len(starting_points) > 2:
                default_starting_points = starting_points[2]

            dest_table = {}
            dest_types = [NapoDatatype.Integer] * (len(destruction_scores) + 1) * len(destruction_scores)
            for val in starting_points:
                dest_table[val] = destruction_scores

            self.constants_napo.set_value("WargameConstantes\\ArgentInitialSetting", starting_points,
                                          len(starting_points) * [NapoDatatype.Integer])
            self.constants_napo.set_value("WargameConstantes\\DefaultArgentInitial", default_starting_points,
                                          [NapoDatatype.Integer])
            self.constants_napo.set_value("WargameConstantes\\ConquestPossibleScores", conquest_scores,
                                          len(conquest_scores) * [NapoDatatype.Integer])
            self.constants_napo.set_value("WargameConstantes\\DestructionScoreToReachSetting", destruction_scores,
                                          len(destruction_scores) * [NapoDatatype.Integer])
            self.constants_napo.set_value("WargameConstantes\\VictoryTypeDestructionLevelsTable", dest_table, dest_types)
            self.constants_napo.set_value("WargameConstantes\\BaseIncome\\CombatRule/CaptureTheFlag", conquest_income,
                                          [NapoDatatype.Integer])
            self.constants_napo.set_value(
                "WargameConstantes\\TimeBeforeEarningCommandPoints\\CombatRule/CaptureTheFlag",
                conquest_tick, [NapoDatatype.Float])
            self.constants_napo.set_value("WargameConstantes\\BaseIncome\\CombatRule/Destruction", dest_income,
                                          [NapoDatatype.Integer])
            self.constants_napo.set_value(
                "WargameConstantes\\TimeBeforeEarningCommandPoints\\CombatRule/Destruction",
                dest_tick, [NapoDatatype.Float])

            # write to file
            file_path = os.path.join(main_widget.MainWidget.instance.get_loaded_mod_path(),
                                     "GameData\\Gameplay\\Constantes\\GDConstantes.ndf")
            self.write_napo_file(file_path, self.constants_napo)

            # set own variables
            self.starting_points = [int(i) for i in starting_points]
            self.conquest_scores = [int(i) for i in conquest_scores]
            self.destruction_scores = [int(i) for i in destruction_scores]

            self.conquest_income = int(conquest_income)
            self.conquest_tick = float(conquest_tick)
            self.destruction_income = int(dest_income)
            self.destruction_tick = float(dest_tick)

        except Exception as e:
            logging.error("Error while saving game settings: " + str(e))
            return False
        return True


class BaseIncomeWidget(QtWidgets.QWidget):
    value_changed = QtCore.Signal(int, float)

    def __init__(self, parent: QtWidgets.QWidget = None, label_text: str = ""):
        super().__init__(parent)

        main_layout = QtWidgets.QHBoxLayout()
        self.setLayout(main_layout)

        main_layout.addWidget(QtWidgets.QLabel(label_text))
        self.points_spin_box = QtWidgets.QSpinBox()
        self.points_spin_box.setRange(0, 10000)
        self.points_spin_box.valueChanged.connect(self.on_value_changed)
        main_layout.addWidget(self.points_spin_box)

        main_layout.addWidget(QtWidgets.QLabel(" points every "))
        self.tick_spin_box = QtWidgets.QDoubleSpinBox()
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
