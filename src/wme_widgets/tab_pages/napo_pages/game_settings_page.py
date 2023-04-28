import logging
import os

from PySide6 import QtWidgets

from src.wme_widgets import main_widget
from src.wme_widgets.tab_pages.napo_pages import base_napo_page
from src.wme_widgets.tab_pages.napo_pages import napo_list_widget

from src.utils import icon_manager
from src.utils.color_manager import *

from src.ndf_parser.napo_entities.napo_entity import *


class GameSettingsPage(base_napo_page.BaseNapoPage):
    def __init__(self):
        super().__init__()
        self.constants_napo = None
        self.starting_points = []

        self.setup_ui()
        self.update_page()

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout()

        tool_bar = QtWidgets.QToolBar()
        main_layout.addWidget(tool_bar)

        save_action = tool_bar.addAction(icon_manager.load_icon("save.png", COLORS.PRIMARY), "Save (Ctrl + S)")
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_changes)

        self.starting_pts_list_widget = napo_list_widget.NapoListWidget("Starting Points", "\\d+")
        self.starting_pts_list_widget.list_updated.connect(self.on_starting_points_changed)
        main_layout.addWidget(self.starting_pts_list_widget)

        # TODO: add scroll area
        # TODO: add more options (destruction score, income,...)

        main_layout.addStretch(1)
        self.setLayout(main_layout)

    def update_page(self):
        main_widget.MainWidget.instance.show_loading_screen("loading GDConstantes.ndf...")

        file_path = os.path.join(main_widget.MainWidget.instance.get_loaded_mod_path(),
                                 "GameData\\Gameplay\\Constantes\\GDConstantes.ndf")

        self.constants_napo = self.get_napo_from_file(file_path)
        self.starting_points = self.constants_napo.get_value("WargameConstantes\\ConquestPossibleScores")

        self.starting_pts_list_widget.update_list(self.starting_points)

        main_widget.MainWidget.instance.hide_loading_screen()

    def on_starting_points_changed(self, starting_points: [str]):
        # convert to int list
        starting_points = [int(i) for i in starting_points]
        if self.starting_points != starting_points:
            self.unsaved_changes = True

    def _save_changes(self) -> bool:
        try:
            starting_points = self.starting_pts_list_widget.list_widget.all_item_labels()
            self.constants_napo.set_value("WargameConstantes\\ConquestPossibleScores", starting_points,
                                          len(starting_points) * [NapoDatatype.Integer])

            # write to file
            file_path = os.path.join(main_widget.MainWidget.instance.get_loaded_mod_path(),
                                     "GameData\\Gameplay\\Constantes\\GDConstantes.ndf")
            self.write_napo_file(file_path, self.constants_napo)

            # set own variable
            self.starting_points = [int(i) for i in starting_points]
        except Exception as e:
            logging.error("Error while saving game settings: " + str(e))
            return False
        return True

