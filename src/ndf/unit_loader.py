# TODO: when a mod is loaded, start loading certain information of all units in the background
# TODO: show progress bar in main widget
# TODO: when unit editor exists, make a unit browser for main widget
import os

import ndf_parse as ndf


class UnitLoader:
    def __init__(self, mod_path: str):
        units_file_path = os.path.join(mod_path, r"GameData\Generated\Gameplay\Gfx\UniteDescriptor.ndf")
