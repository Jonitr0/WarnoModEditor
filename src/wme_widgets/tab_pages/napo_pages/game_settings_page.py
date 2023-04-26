import os

from PySide6 import QtWidgets

from src.wme_widgets import main_widget
from src.wme_widgets.tab_pages.napo_pages import base_napo_page


class GameSettingsPage(base_napo_page.BaseNapoPage):
    def __init__(self):
        super().__init__()
        self.constants_napo = None
        self.starting_points = []

        main_widget.MainWidget.instance.show_loading_screen("loading GDConstantes.ndf...")

        self.setup_ui()
        self.update_page()

        main_widget.MainWidget.instance.hide_loading_screen()

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(
            QtWidgets.QLabel("Edit game settings such as starting points, income and victory conditions."))

        # TODO: create own list widget with: title, add button, input field, remove button
        self.starting_pts_list_widget = QtWidgets.QListWidget()
        main_layout.addWidget(self.starting_pts_list_widget)

        main_layout.addStretch(1)
        self.setLayout(main_layout)

    def update_page(self):
        file_path = os.path.join(main_widget.MainWidget.instance.get_loaded_mod_path(),
                                 "GameData\\Gameplay\\Constantes\\GDConstantes.ndf")

        self.constants_napo = self.get_napo_from_file(file_path)
        self.starting_points = self.constants_napo.find("WargameConstantes\\ConquestPossibleScores")

        self.starting_pts_list_widget.clear()
        str_starting_points = [str(i) for i in self.starting_points]
        self.starting_pts_list_widget.addItems(str_starting_points)
