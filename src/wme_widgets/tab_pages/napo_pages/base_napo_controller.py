from src.wme_widgets import main_widget
from src.utils import parser_utils

import os
import shutil
import logging


# handles all parser functionality for a NAPO page
# TODO: remove controllers, put functionality directly into pages
class BaseNapoController:
    def get_parsed_ndf_file(self, file_name: str):
        mod_path = main_widget.instance.get_loaded_mod_path()
        file_path = os.path.join(mod_path, file_name)

        return parser_utils.get_parsed_ndf_file(file_path)

    def get_parsed_object_from_ndf_file(self, file_name: str, obj_name: str):
        file_obj = self.get_parsed_ndf_file(file_name)
        for row in file_obj:
            if row.namespace == obj_name:
                return row.value

        logging.warning("Object " + obj_name + " not found in " + file_name)
        return None

    def save_files_to_mod(self, files_to_objs: dict):
        mod_path = main_widget.instance.get_loaded_mod_path()

        files = files_to_objs.keys()

        for file in files:
            text = parser_utils.get_text_from_ndf_obj(files_to_objs[file])
            file_path = os.path.join(mod_path, file)
            with open(file_path, "w") as f:
                f.write(text)

    def load_state_from_file(self) -> dict:
        pass

    def write_state_to_file(self, state: dict):
        pass
