import os

from src.wme_widgets import main_widget
from src.utils import parser_utils


class ScriptParameter:
    def __init__(self, name: str, description: str, default_value):
        self.name = name
        self.description = description
        self.default_value = default_value


class BaseScript:
    def __init__(self):
        self.parameters: [ScriptParameter] = []
        # to make sure page checks if files can be safely edited
        self.edited_files: [str] = []
        # name displayed in script selector
        self.name = ""
        # description displayed in script runner page
        self.description = ""
        self.opened_files = {}

    def run(self, parameter_values: dict):
        # TODO: check if files can be safely edited
        self._run(parameter_values)
        main_widget.instance.show_loading_screen("Saving changes...")
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
