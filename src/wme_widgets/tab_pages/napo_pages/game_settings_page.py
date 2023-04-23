import os

from src.wme_widgets import main_widget

from src.wme_widgets.tab_pages.napo_pages import base_napo_page


class GameSettingsPage(base_napo_page.BaseNapoPage):
    def __init__(self):
        super().__init__()

        file_path = os.path.join(main_widget.MainWidget.instance.get_loaded_mod_path(),
                                 "GameData\\Gameplay\\Constantes\\GDConstantes.ndf")
        print(file_path)
