import os

from src.wme_widgets import main_widget

from src.wme_widgets.tab_pages.napo_pages import base_napo_page


class GameSettingsPage(base_napo_page.BaseNapoPage):
    def __init__(self):
        super().__init__()

        main_widget.MainWidget.instance.show_loading_screen("loading GDConstantes.ndf...")

        file_path = os.path.join(main_widget.MainWidget.instance.get_loaded_mod_path(),
                                 "GameData\\Gameplay\\Constantes\\GDConstantes.ndf")
        self.constants_napo = self.get_napo_from_file(file_path)

        main_widget.MainWidget.instance.hide_loading_screen()