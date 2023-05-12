import os
import re

from src.wme_widgets import main_widget


def get_assignment_ids(file_name: str) -> [str]:
    file_name = os.path.join(main_widget.MainWidget.instance.get_loaded_mod_path(), file_name)
    with open(file_name, mode="r", encoding="utf-8") as f:
        file_content = f.read()

    current_index = 0
    assignment_regex = re.compile("([\w\d_]+)\sis\s")

    # TODO: iterate over content

    return []
