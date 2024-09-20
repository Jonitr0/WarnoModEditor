from src.wme_widgets import main_widget

import os
import shutil
import logging

import ndf_parse as ndf


# handles all parser functionality for a NAPO page
# TODO: no need for tmp mod, use stuff from roundtrip
class BaseNapoController:
    def __init__(self):
        self.mod = None

    def get_parsed_ndf_file(self, file_name: str):
        mod_path = main_widget.instance.get_loaded_mod_path()
        file_path = os.path.join(mod_path, file_name)

        if not self.mod:
            self.mod = ndf.Mod(mod_path, mod_path + "_wme_tmp")
            self.mod.check_if_src_is_newer()

        return self.mod.parse_src(file_path)

    def get_parsed_object_from_ndf_file(self, file_name: str, obj_name: str):
        file_obj = self.get_parsed_ndf_file(file_name)
        for row in file_obj:
            if row.namespace == obj_name:
                return row.value

        logging.warning("Object " + obj_name + " not found in " + file_name)
        return None

    def delete_tmp_mod(self):
        orig_path = main_widget.instance.get_loaded_mod_path()
        tmp_path = orig_path + "_wme_tmp"
        self.mod = None
        shutil.rmtree(tmp_path)

    def save_files_to_mod(self, files_to_objs: dict):
        # copy files from tmp dir to mod dir
        orig_path = main_widget.instance.get_loaded_mod_path()
        tmp_path = orig_path + "_wme_tmp"

        files = files_to_objs.keys()

        self.mod = ndf.Mod(orig_path, tmp_path)
        self.mod.check_if_src_is_newer()

        for file in files:
            orig_file_path = os.path.join(orig_path, file)
            tmp_file_path = os.path.join(tmp_path, file)

            with self.mod.edit(file) as obj:
                for index, elem in enumerate(files_to_objs[file]):
                    try:
                        obj[index] = elem
                    except IndexError:
                        elem_str = ndf.printer.string(elem)
                        elem_dict = ndf.expression(elem_str)
                        obj.add(**elem_dict)


            with open(orig_file_path, "w", encoding="utf-8") as f_orig, \
                    open(tmp_file_path, "r", encoding="utf-8") as f_tmp:
                for line in f_tmp:
                    f_orig.write(line)

        self.mod = None
        shutil.rmtree(tmp_path)

    def load_state_from_file(self) -> dict:
        pass

    def write_state_to_file(self, state: dict):
        pass
