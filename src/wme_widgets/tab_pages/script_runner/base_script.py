import os
import logging
import time

from src.wme_widgets import main_widget
from src.wme_widgets.tab_pages import base_tab_page
from src.utils import parser_utils


class ScriptParameter:
    def __init__(self, name: str, description: str, default_value):
        self.name = name
        self.description = description
        self.default_value = default_value


class BaseScript:
    def __init__(self):
        self.parameters: [ScriptParameter] = []
        # name displayed in script selector
        self.name = ""
        # description displayed in script runner page
        self.description = ""
        self.opened_files = {}
        self.page: base_tab_page.BaseTabPage = None

    def run(self, parameter_values: dict):
        logging.info(f"Running script {self.name}")
        start_time = time.time()
        self._run(parameter_values)
        logging.info(f"Script {self.name} finished in {time.time() - start_time:.2f} seconds")
        main_widget.instance.show_loading_screen("Saving changes...")
        for file in self.opened_files.keys():
            full_path = os.path.join(main_widget.instance.get_loaded_mod_path(), file)
            self.page.file_paths.add(full_path)
            self.page.unsaved_changes = True
        if not self.page.save_changes():
            self.page.unsaved_changes = False
            return
        for file in self.opened_files.keys():
            text = parser_utils.get_text_from_ndf_obj(self.opened_files[file])
            full_path = os.path.join(main_widget.instance.get_loaded_mod_path(), file)
            with open(full_path, "w") as f:
                f.write(text)

    def _run(self, parameter_values: dict):
        # to be overwritten with actual script
        pass

    def add_parameter(self, name: str, description: str, default_value):
        self.parameters.append(ScriptParameter(name, description, default_value))

    def get_parsed_ndf_file(self, file_path: str):
        full_path = os.path.join(main_widget.instance.get_loaded_mod_path(), file_path)
        self.opened_files[file_path] = parser_utils.get_parsed_ndf_file(full_path)
        return self.opened_files[file_path]
