import os

from PySide6 import QtWidgets

from src.wme_widgets import main_widget
from src.wme_widgets.tab_pages.napo_pages import base_napo_page
from src.wme_widgets.tab_pages.napo_pages import napo_list_widget


class GameSettingsPage(base_napo_page.BaseNapoPage):
    def __init__(self):
        super().__init__()
        self.constants_napo = None
        self.starting_points = []

        self.setup_ui()
        self.update_page()

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout()

        self.starting_pts_list_widget = napo_list_widget.NapoListWidget("Starting Points")
        main_layout.addWidget(self.starting_pts_list_widget)

        main_layout.addStretch(1)
        self.setLayout(main_layout)

    def update_page(self):
        main_widget.MainWidget.instance.show_loading_screen("loading GDConstantes.ndf...")

        file_path = os.path.join(main_widget.MainWidget.instance.get_loaded_mod_path(),
                                 "GameData\\Gameplay\\Constantes\\GDConstantes.ndf")

        self.constants_napo = self.get_napo_from_file(file_path)
        self.starting_points = self.constants_napo.find("WargameConstantes\\ConquestPossibleScores")

        self.starting_pts_list_widget.update_list(self.starting_points)

        main_widget.MainWidget.instance.hide_loading_screen()
