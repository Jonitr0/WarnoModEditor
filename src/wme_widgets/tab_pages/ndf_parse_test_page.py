import logging

from src.wme_widgets.tab_pages import base_tab_page
from src.wme_widgets import main_widget

import ndf_parse as ndf


class NdfParseTestPage(base_tab_page.BaseTabPage):
    def __init__(self):
        super().__init__()

        mod = ndf.Mod(main_widget.instance.get_loaded_mod_path(), main_widget.instance.get_loaded_mod_path() + "tgt")
        mod.check_if_src_is_newer()

        with mod.edit(r"GameData\Generated\Gameplay\Gfx\UniteDescriptor.ndf") as unit_desc:
            for unit in unit_desc:
                name = unit.namespace
                logging.info(name)
