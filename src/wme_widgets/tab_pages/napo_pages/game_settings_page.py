import logging
import os

from PySide6 import QtWidgets, QtGui

from src.wme_widgets import main_widget
from src.wme_widgets.tab_pages.napo_pages import base_napo_page
from src.wme_widgets.tab_pages.napo_pages import napo_list_widget
from src.dialogs import essential_dialogs

from src.utils import icon_manager
from src.utils.color_manager import *

from src.ndf_parser.napo_entities.napo_entity import *


class GameSettingsPage(base_napo_page.BaseNapoPage):
    def __init__(self):
        super().__init__()
        self.destruction_income_widget = BaseIncomeWidget(self, "Destruction base income: ")
        self.conquest_income_widget = BaseIncomeWidget(self, "Conquest base income: ")
        self.starting_pts_list_widget = napo_list_widget.NapoListWidget("Starting Points in Skirmish and Multiplayer",
                                                                        "\\d+")
        self.conquest_score_list_widget = napo_list_widget.NapoListWidget("Conquest Scores", "\\d+")
        self.constants_napo = None
        self.starting_points = []
        self.conquest_scores = []
        self.conquest_income = 0
        self.conquest_tick = 0.
        self.destruction_income = 0
        self.destruction_tick = 0.

        self.setup_ui()
        self.update_page()

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout()

        # TODO: toolbar and scroll area could go to base_napo_page
        tool_bar = QtWidgets.QToolBar()
        main_layout.addWidget(tool_bar)

        save_action = tool_bar.addAction(icon_manager.load_icon("save.png", COLORS.PRIMARY), "Save (Ctrl + S)")
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_changes)

        restore_icon = QtGui.QIcon()
        restore_icon.addPixmap(icon_manager.load_pixmap("restore.png", COLORS.PRIMARY), QtGui.QIcon.Normal)
        restore_icon.addPixmap(icon_manager.load_pixmap("restore.png", COLORS.SECONDARY_LIGHT), QtGui.QIcon.Disabled)

        self.restore_action = tool_bar.addAction(restore_icon, "Discard changes and restore page (F5)")
        self.restore_action.setShortcut("F5")
        self.restore_action.triggered.connect(self.on_restore)
        self.restore_action.setEnabled(False)

        self.unsaved_status_change.connect(self.on_unsaved_changed)

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)

        scroll_widget = QtWidgets.QWidget()
        scroll_area.setWidget(scroll_widget)
        scroll_layout = QtWidgets.QVBoxLayout()
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_widget.setLayout(scroll_layout)

        self.starting_pts_list_widget.list_updated.connect(self.on_starting_points_changed)
        scroll_layout.addWidget(self.starting_pts_list_widget)

        self.conquest_score_list_widget.list_updated.connect(self.on_conquest_scores_changed)
        scroll_layout.addWidget(self.conquest_score_list_widget)

        scroll_layout.addWidget(self.conquest_income_widget)

        scroll_layout.addWidget(self.destruction_income_widget)

        # TODO: add more options (destruction score, income,...)

        scroll_layout.addStretch(1)
        self.setLayout(main_layout)

    def on_restore(self):
        if not essential_dialogs.ConfirmationDialog("Your changes will be discarded! Are you sure?", "Warning!").exec():
            return
        self.update_page()

    def on_unsaved_changed(self, unsaved: bool, widget):
        self.restore_action.setEnabled(unsaved)

    def update_page(self):
        main_widget.MainWidget.instance.show_loading_screen("loading GDConstantes.ndf...")

        file_path = os.path.join(main_widget.MainWidget.instance.get_loaded_mod_path(),
                                 "GameData\\Gameplay\\Constantes\\GDConstantes.ndf")

        self.constants_napo = self.get_napo_from_file(file_path)

        self.starting_points = self.constants_napo.get_value("WargameConstantes\\ArgentInitialSetting")
        self.starting_pts_list_widget.update_list(self.starting_points)
        self.conquest_scores = self.constants_napo.get_value("WargameConstantes\\ConquestPossibleScores")
        self.conquest_score_list_widget.update_list(self.conquest_scores)

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

    def _save_changes(self) -> bool:
        try:
            starting_points = self.starting_pts_list_widget.list_widget.all_item_labels()
            conquest_scores = self.conquest_score_list_widget.list_widget.all_item_labels()

            default_starting_points = starting_points[0]
            if starting_points.__contains__("1500"):
                default_starting_points = "1500"
            elif len(starting_points) > 2:
                default_starting_points = starting_points[2]

            self.constants_napo.set_value("WargameConstantes\\ArgentInitialSetting", starting_points,
                                          len(starting_points) * [NapoDatatype.Integer])
            self.constants_napo.set_value("WargameConstantes\\DefaultArgentInitial", default_starting_points,
                                          [NapoDatatype.Integer])
            self.constants_napo.set_value("WargameConstantes\\ConquestPossibleScores", conquest_scores,
                                          len(conquest_scores) * [NapoDatatype.Integer])

            # write to file
            file_path = os.path.join(main_widget.MainWidget.instance.get_loaded_mod_path(),
                                     "GameData\\Gameplay\\Constantes\\GDConstantes.ndf")
            self.write_napo_file(file_path, self.constants_napo)

            # set own variables
            self.starting_points = [int(i) for i in starting_points]
            self.conquest_scores = [int(i) for i in conquest_scores]
        except Exception as e:
            logging.error("Error while saving game settings: " + str(e))
            return False
        return True


class BaseIncomeWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget = None, label_text: str = ""):
        super().__init__(parent)

        main_layout = QtWidgets.QHBoxLayout()
        self.setLayout(main_layout)

        main_layout.addWidget(QtWidgets.QLabel(label_text))
        self.points_spin_box = QtWidgets.QSpinBox()
        self.points_spin_box.setRange(0, 10000)
        main_layout.addWidget(self.points_spin_box)
        main_layout.addWidget(QtWidgets.QLabel(" points every "))
        self.tick_spin_box = QtWidgets.QDoubleSpinBox()
        self.tick_spin_box.setRange(0.1, 36000.)
        main_layout.addWidget(self.tick_spin_box)
        main_layout.addWidget(QtWidgets.QLabel(" seconds"))
        main_layout.addStretch(1)

    def set_values(self, income: int, tick: float):
        self.points_spin_box.setValue(income)
        self.tick_spin_box.setValue(tick)

    def get_values(self):
        return int(self.points_spin_box.text()), float(self.tick_spin_box.text())
